from domain.model.prompt.distill_intent_prompt import DistillIntentPrompt
from infrastructure.service.llm_service import call_llm


def distill_intent(state: dict) -> dict:
    # Build the prompt using your value object
    prompt = DistillIntentPrompt(
        user_input=state["user_input"],
        domain_summary=state.get("domain_summary", "")
    ).as_prompt()

    # Call the LLM (assumed to return parsed JSON or dict)
    response = call_llm(prompt)

    # Update state with distilled intent
    state["intent"] = response.get("intent")
    return state
