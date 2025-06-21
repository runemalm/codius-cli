import logging

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

from infrastructure.services.openddd_convention_service import OpenDddConventionService
from infrastructure.services.tree_sitter_service import TreeSitterService

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


def generate_code(state: dict) -> dict:
    from di import container

    session_id = state.get('session_id')
    output_dir = Path(f".openddd/sessions/{session_id}/generated")

    convention_service = container.resolve(OpenDddConventionService)

    jinja_env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(disabled_extensions=("cs",)),
        trim_blocks=True,
        lstrip_blocks=True
    )

    plan = state.get("plan", [])
    project_root = Path(state["project_metadata"]["project_root"])
    all_files = []

    created_files_map = {}

    # Group modify steps by target file
    modify_groups = defaultdict(list)
    create_steps = []

    for step in plan:
        if step["type"] == "modify_file":
            modify_groups[step["path"]].append(step)
        else:
            create_steps.append(step)

    # Process file creations
    for step in create_steps:
        result = handle_create_file(step, jinja_env, output_dir, project_root)

        if result:
            all_files.append(result)
            created_files_map[step["path"]] = result["content"]

    # Process all modifications per file in sequence
    for path, steps in modify_groups.items():
        result = handle_modify_file(
            path,
            steps,
            jinja_env,
            output_dir,
            project_root,
            created_files_map,
            convention_service
        )

        if result:
            # Remove any previous entry for this file (created earlier)
            all_files = [f for f in all_files if f["path"] != result["path"]]
            all_files.append(result)

    state["generated_files"] = all_files
    return state


def handle_create_file(
    file_plan: dict,
    jinja_env: Environment,
    output_dir: Path,
    project_root: Path
) -> dict | None:

    from di import container

    convention_service = container.resolve(OpenDddConventionService)

    template_name = file_plan.get("template")
    context = file_plan.get("context", {})
    absolute_path = Path(file_plan["path"]).resolve()
    relative_path = absolute_path.relative_to(project_root)

    try:
        template = jinja_env.get_template(f"{template_name}.cs.j2")
        rendered = template.render(**context)
        formatted = convention_service.format_class_code(rendered)

        file_path = output_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(formatted.strip(), encoding="utf-8")

        logger.debug("Generated file from template: %s", file_path)

        return {
            "path": str(relative_path),
            "content": formatted.strip()
        }

    except Exception as e:
        logger.error("Failed to generate file from template '%s': %s", template_name, e)
        return None


def handle_modify_file(
    path: str,
    steps: list[dict],
    jinja_env: Environment,
    output_dir: Path,
    project_root: Path,
    created_files_map: dict[str, str],
    convention_service: OpenDddConventionService
) -> dict | None:
    absolute_path = Path(path).resolve()
    relative_path = absolute_path.relative_to(project_root)

    file_path_str = str(project_root / relative_path)

    # If created earlier in this session, use that version
    if file_path_str in created_files_map:
        current_code = created_files_map[file_path_str]
    else:
        try:
            current_code = (project_root / relative_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.warning("Target file for modification not found: %s", path)
            return None

    for step in steps:
        modification = step["modification"]
        context = step["context"]

        if modification == "add_method":
            code = render_method_template(context, jinja_env)
            current_code = inject_method_ast_based(current_code, code, context.get("placement"))

        elif modification == "add_property":
            code = render_property_template(context, jinja_env)
            current_code = inject_property_ast_based(current_code, code)

        else:
            raise Exception(f"Unsupported modification type: {modification}")

    # Write modified code
    file_path = output_dir / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    formatted_code = convention_service.format_class_code(current_code)
    file_path.write_text(formatted_code.strip(), encoding="utf-8")

    return {
        "path": str(relative_path),
        "content": formatted_code.strip()
    }


def render_method_template(context: dict, jinja_env: Environment) -> str:
    method = context["method"]

    if "body" in method and method["body"].strip():
        params = ", ".join(f"{p['type']} {p['name']}" for p in method.get("parameters", []))
        returns = method.get("returns", "void")
        name = method["name"]
        body = method["body"].strip()

        return f"""public {returns} {name}({params})
{{
    {body}
}}"""

    # fallback to Jinja template if no explicit body
    template = jinja_env.get_template("aggregate_method.cs.j2")
    return template.render(**context)


def inject_method_ast_based(source_code: str, method_code: str, placement: dict | None) -> str:

    tree_sitter_service = container.resolve(TreeSitterService)
    tree = tree_sitter_service.parse_code(source_code)

    reference = placement.get("reference") if placement else None
    insert_pos = None

    def find_insertion_point(node):
        nonlocal insert_pos

        if node.type == "class_declaration":
            body_node = next((child for child in node.children if child.type == "declaration_list"), None)
            if not body_node:
                return False

            reference_found = False
            last_method = None

            for child in body_node.children:
                if child.type == "method_declaration":
                    method_name = _extract_method_name(source_code, child)
                    if method_name == reference:
                        insert_pos = child.end_byte
                        reference_found = True
                        break
                    last_method = child

            if not reference_found:
                insert_pos = last_method.end_byte if last_method else body_node.start_byte + 1  # after {
            return True

        for child in node.children:
            if find_insertion_point(child):
                return True
        return False

    found = find_insertion_point(tree.root_node)

    if not found or insert_pos is None:
        logger.warning("Could not locate class or reference method. Appending at end of file.")
        return source_code + "\n\n" + method_code

    before = source_code[:insert_pos].rstrip()
    after = source_code[insert_pos:].lstrip()
    return before + "\n\n" + _indent_block(method_code.strip()) + "\n    " + after


def _extract_method_name(source: str, node) -> str:
    for child in node.children:
        if child.type == "identifier":
            return source[child.start_byte:child.end_byte]
    return ""


def render_property_template(context: dict, jinja_env: Environment) -> str:
    prop = context["property"]
    type_ = prop["type"]
    name = prop["name"]
    default = prop.get("default")

    if default is not None:
        return f"public {type_} {name} {{ get; set; }} = {default};"
    else:
        return f"public {type_} {name} {{ get; set; }}"


def inject_property_ast_based(source_code: str, property_code: str) -> str:

    tree_sitter_service = container.resolve(TreeSitterService)
    tree = tree_sitter_service.parse_code(source_code)

    insert_pos = None
    class_indent = "    "

    def find_class_body(node):
        nonlocal insert_pos, class_indent

        if node.type == "class_declaration":
            # Estimate indent level from class start
            line_start = source_code.rfind("\n", 0, node.start_byte) + 1
            class_indent = " " * (node.start_byte - line_start)

            # Find last property or method or start of class body
            body_node = next((c for c in node.children if c.type == "declaration_list"), None)
            if not body_node:
                return False

            # Insert at beginning of declaration_list
            insert_pos = body_node.start_byte + 1
            return True

        for child in node.children:
            if find_class_body(child):
                return True
        return False

    found = find_class_body(tree.root_node)

    if not found or insert_pos is None:
        logger.warning("Class declaration not found. Appending at end.")
        return source_code + "\n\n" + property_code

    before = source_code[:insert_pos].rstrip()
    after = source_code[insert_pos:].lstrip()

    indented_property = _indent_block(property_code.strip(), spaces=len(class_indent.expandtabs()))
    return before + "\n" + class_indent + indented_property + "\n\n    " + after


def _indent_block(code: str, spaces: int = 8) -> str:
    return "\n".join(" " * spaces + line if line.strip() else "" for line in code.splitlines())
