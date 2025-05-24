from domain.model.prompt.generate_code_prompt import GenerateCodePrompt
from infrastructure.service.llm_service import call_llm


def generate_code(state: dict) -> dict:
    prompt = GenerateCodePrompt(
        plan=state["plan"],
        domain_summary=state.get("domain_summary", "")
    ).as_prompt()

    response = call_llm(prompt)

    state["generated_files"] = response.get("files", [])
    return state
