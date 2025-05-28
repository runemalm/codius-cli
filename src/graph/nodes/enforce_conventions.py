import logging

logger = logging.getLogger(__name__)


def enforce_conventions(state: dict) -> dict:
    logger.debug("Running enforce_conventions...")

    enforced_intents = []

    for intent in state.get("intent", []):
        intent_type = intent.get("intent")

        if intent_type == "add_aggregate":
            enforced_intents.append(_enforce_aggregate_conventions(intent))
        elif intent_type == "add_repository":
            enforced_intents.append(_enforce_repository_conventions(intent))
        else:
            logger.warning("No conventions defined for intent type: %s", intent_type)
            enforced_intents.append(intent)

    state["intent"] = enforced_intents
    logger.debug("Enforced conventions on %d intent(s)", len(enforced_intents))
    return state


def _enforce_aggregate_conventions(intent: dict) -> dict:
    logger.debug("Enforcing aggregate conventions...")

    details = intent.setdefault("details", {})
    details.setdefault("properties", [])
    details.setdefault("commands", [])
    details.setdefault("events", [])

    return intent


def _enforce_repository_conventions(intent: dict) -> dict:
    logger.debug("Enforcing repository conventions...")

    details = intent.setdefault("details", {})
    methods = details.get("custom_methods", [])

    for method in methods:
        method.setdefault("is_async", True)

        name = method.get("name")
        if name and not name.endswith("Async"):
            method["name"] = f"{name}Async"

        method.setdefault("parameters", [])

    return intent
