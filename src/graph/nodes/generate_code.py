from domain.services import session_service
from jinja2 import Environment, FileSystemLoader, select_autoescape

from pathlib import Path

import logging

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


def generate_code(state: dict) -> dict:
    jinja_env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(disabled_extensions=("cs",)),
        trim_blocks=True,
        lstrip_blocks=True
    )

    plan = state.get("plan", [])
    project_root = state["project_metadata"]["project_root"]
    session_id = session_service.get_active_session_id()
    output_dir = Path(f".openddd/sessions/{session_id}/generated")

    all_files = []

    for file_plan in plan:
        template_name = file_plan.get("template")
        context = file_plan.get("context", {})
        absolute_path = Path(file_plan["path"]).resolve()
        relative_path = absolute_path.relative_to(project_root)

        try:
            # Load and render template
            template = jinja_env.get_template(f"{template_name}.cs.j2")
            rendered = template.render(**context)

            # Write file
            file_path = output_dir / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(rendered.strip(), encoding="utf-8")

            logger.debug("Generated file from template: %s", file_path)

            all_files.append({
                "path": str(relative_path),
                "content": rendered.strip()
            })

        except Exception as e:
            logger.error("Failed to generate file from template '%s': %s", template_name,
                         e)

    state["generated_files"] = all_files
    return state
