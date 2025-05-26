import logging

from dependency_injection.container import DependencyContainer

from domain.model.prompt.plan_prompt import PlanPrompt
from infrastructure.service.llm_service import LlmService

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    intent = state.get("intent")
    if not intent:
        logger.warning("No intent found in state. Skipping planning.")
        state["plan"] = "⚠️ No intent found. Cannot plan changes."
        return state

    logger.debug("Planning changes for intent: %s", intent.get("intent", "unknown"))

    prompt = PlanPrompt(intent=intent).as_prompt()
    logger.debug("Constructed plan prompt (%d chars)", len(prompt))

    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    response = llm_service.call(prompt)
    logger.debug("LLM plan response received: %s", response)

    state["plan"] = response.get("plan") or response.get("raw") or "⚠️ No plan returned."
    return state
