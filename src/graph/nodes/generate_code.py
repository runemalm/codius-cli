from domain.model.prompt.generate_code_prompt import GenerateCodePrompt
from infrastructure.service.llm_service import LlmService

from dependency_injection.container import DependencyContainer


def generate_code(state: dict) -> dict:
    prompt = GenerateCodePrompt(
        plan=state["plan"],
        domain_summary=state.get("domain_summary", "")
    ).as_prompt()

    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    response = llm_service.call(prompt)

    state["generated_files"] = response.get("files", [])
    return state
