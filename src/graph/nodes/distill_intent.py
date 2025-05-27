import logging

from dependency_injection.container import DependencyContainer

from domain.model.prompt.distill_intent_prompt import DistillIntentPrompt
from infrastructure.service.llm_service import LlmService

logger = logging.getLogger(__name__)


def distill_intent(state: dict) -> dict:
    logger.debug("Running distill_intent with state keys: %s", list(state.keys()))

    prompt = DistillIntentPrompt(user_input=state["user_input"]).as_prompt()
    logger.debug("Constructed distill intent prompt (%d chars)", len(prompt))

    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    logger.debug("Calling LLM to distill intent...")
    response = llm_service.call_prompt(prompt)
    logger.debug("LLM response received.")

    parsed = llm_service.try_extract_json(response)

    if isinstance(parsed, list):
        logger.debug("Multiple intents detected (%d)", len(parsed))
        state["intent"] = parsed
    elif isinstance(parsed, dict):
        logger.debug("Extracted intent: %s", parsed.get("intent"))
        state["intent"] = [parsed]  # always normalize to list
    else:
        logger.warning("Unexpected intent format: %s", type(parsed))
        state["intent"] = []

    return state
