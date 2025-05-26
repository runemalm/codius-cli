from domain.model.prompt.generate_code_prompt import GenerateCodePrompt
from infrastructure.service.llm_service import LlmService

from dependency_injection.container import DependencyContainer

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


def generate_code(state: dict) -> dict:
    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    plan = state.get("plan", [])

    all_files = []

    for file_plan in plan:
        template_name = file_plan.get("template")
        example = load_template_example(template_name) if template_name else ""

        prompt = GenerateCodePrompt(
            plan=file_plan,
            project_namespace=state.get("project_namespace", ""),
            building_blocks=state.get("building_blocks", []),
            example=example
        ).as_prompt()

        response = llm_service.call_prompt(prompt)
        parsed = llm_service.try_extract_json(response)
        files = parsed.get("files", [])

        all_files.extend(files)

    state["generated_files"] = all_files
    return state


def load_template_example(template_name: str) -> str:
    path = TEMPLATE_DIR / f"{template_name}.cs"
    if not path.exists():
        raise Exception(f"Template does not exist: {path}")
    return path.read_text(encoding="utf-8").strip()
