import logging

from .plan_aggregate import plan_aggregate
from .plan_repository import plan_repository
from .plan_remove_aggregate import plan_remove_aggregate
from .plan_add_aggregate_method import plan_add_aggregate_method

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    logger.debug("Running plan...")

    plan = []
    warnings = []

    metadata = state.get("project_metadata", {})
    building_blocks = state.get("building_blocks", [])
    existing_paths = {bb["file_path"] for bb in building_blocks}

    for intent in state.get("intent", []):
        intent_type = intent.get("intent")
        logger.debug("Processing intent: %s", intent)

        try:
            if intent_type == "add_aggregate":
                steps, step_warnings = plan_aggregate(intent, metadata, existing_paths)
            elif intent_type == "add_aggregate_method":
                steps, step_warnings = plan_add_aggregate_method(intent, metadata, existing_paths)
            elif intent_type == "remove_aggregate":
                steps, step_warnings = plan_remove_aggregate(intent, metadata)
            elif intent_type == "add_repository":
                steps, step_warnings = plan_repository(intent, metadata, existing_paths)
            else:
                warning = f"⚠️ Unsupported intent: `{intent_type}` for `{intent.get('target')}`"
                logger.warning(warning)
                warnings.append(warning)
                continue

            plan.extend(steps)
            warnings.extend(step_warnings)

        except Exception as e:
            logger.exception("Error planning intent: %s", intent)
            warnings.append(f"❌ Error planning `{intent_type}` for `{intent.get('target')}`: {str(e)}")

    state["plan"] = plan
    state["plan_warnings"] = warnings
    return state
