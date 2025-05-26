from pathlib import Path
import logging

from domain.model.prompt.distill_intent_prompt import DistillIntentPrompt
from infrastructure.service.code_scanner.code_scanner import scan_building_blocks
from infrastructure.service.llm_service import call_llm

logger = logging.getLogger(__name__)


def distill_intent(state: dict) -> dict:
    logger.debug("Running distill_intent with state keys: %s", list(state.keys()))

    project_root = Path(".").resolve()

    # Generate or use existing domain summary
    if "domain_summary" not in state or not state["domain_summary"]:
        logger.debug("No domain summary in state — scanning project at %s", project_root)
        blocks = scan_building_blocks(project_root)
        domain_summary = "\n".join(f"- {b.type.value}: {b.name}" for b in blocks)
        logger.debug("Scanned %d building blocks from codebase", len(blocks))
    else:
        domain_summary = state["domain_summary"]
        logger.debug("Using existing domain summary from state (%d chars)", len(domain_summary))

    # Build prompt
    prompt = DistillIntentPrompt(
        user_input=state["user_input"],
        domain_summary=domain_summary
    ).as_prompt()
    logger.debug("Constructed distill intent prompt (%d chars)", len(prompt))

    # Call LLM
    logger.debug("Calling LLM to distill intent...")
    response = call_llm(prompt)
    logger.debug("LLM response received: %s", response)

    # Update state
    state["domain_summary"] = domain_summary
    state["intent"] = response
    logger.debug("Extracted intent: %s", response.get("intent"))

    return state
