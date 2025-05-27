from domain.model.prompt.generate_code_prompt import GenerateCodePrompt
from domain.service import session_service
from infrastructure.service.llm_service import LlmService
from dependency_injection.container import DependencyContainer

from pathlib import Path

import logging

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


def generate_code(state: dict) -> dict:
    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    plan = state.get("plan", [])
    session_id = session_service.get_active_session_id()
    output_dir = Path(f".openddd/sessions/{session_id}/generated")

    all_files = []

    for file_plan in plan:
        template_name = file_plan.get("template")
        example = load_template_example(template_name) if template_name else ""

        prompt = GenerateCodePrompt(
            plan=file_plan,
            building_blocks=state.get("building_blocks", []),
            example=example
        ).as_prompt()

        logger.debug("Generated code prompt:\n%s", prompt)

        response = llm_service.call_prompt(prompt)
        parsed = llm_service.try_extract_json(response)

        files = parsed.get("files", [])
        if not isinstance(files, list):
            logger.warning("LLM returned invalid files list: %s", files)
            continue

        for f in files:
            try:
                relative_path = f["path"]
                content = f["content"]
                file_path = output_dir / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding="utf-8")
                logger.debug("Wrote generated file: %s", file_path)
                all_files.append(f)
            except Exception as e:
                logger.error("Failed to write generated file: %s", e)

    state["generated_files"] = all_files
    return state


def load_template_example(template_name: str) -> str:
    path = TEMPLATE_DIR / f"{template_name}.cs"
    if not path.exists():
        raise FileNotFoundError(f"Template does not exist: {path}")
    return path.read_text(encoding="utf-8").strip()
