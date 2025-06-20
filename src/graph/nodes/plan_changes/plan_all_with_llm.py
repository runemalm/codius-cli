import logging
from pathlib import Path

from di import container
from infrastructure.services.llm_service import LlmService
from domain.model.prompts.plan_all_with_llm_prompt import PlanAllWithLlmPrompt

logger = logging.getLogger(__name__)


def plan_all_with_llm(state: dict) -> dict:
    logger.debug("Running plan_all_with_llm with state keys: %s", list(state.keys()))

    try:
        prompt = PlanAllWithLlmPrompt(
            intents=state["intent"],
            sources=state["sources"],
            project_metadata=state["project_metadata"]
        ).as_prompt()

        logger.debug("Constructed plan_all_with_llm prompt (%d chars)", len(prompt))

        llm_service = container.resolve(LlmService)

        logger.debug("Calling LLM to generate plan...")
        response = llm_service.call_prompt(prompt)
        logger.debug("LLM response received.")
    except Exception as e:
        logger.error("Error during plan_all_with_llm: %s", e)
        state["plan"] = [{"operation": "error", "error_message": str(e)}]
        return state

    state["plan"] = llm_service.try_extract_json(response)
    return state
