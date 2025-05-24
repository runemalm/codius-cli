from domain.model.prompt.plan_prompt import PlanPrompt
from infrastructure.service.llm_service import call_llm


def plan_changes(state: dict) -> dict:
    prompt = PlanPrompt(
        intent=state["intent"],
        domain_summary=state.get("domain_summary", "")
    ).as_prompt()

    response = call_llm(prompt)
    state["plan"] = response.get("plan")

    return state
