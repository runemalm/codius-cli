import logging

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    intent = state.get("intent", {})

    if not isinstance(intent, dict):
        logger.warning("Expected structured intent but got: %s", intent)
        state["plan"] = []
        return state

    if intent.get("intent") == "add_aggregate":
        aggregate_name = intent.get("target")
        layer = intent.get("layer", "domain")
        details = intent.get("details", {})

        # Build change plan
        changes = [{
            "type": "create_file",
            "path": f"{layer.capitalize()}/{aggregate_name}/{aggregate_name}.cs",
            "description": f"Create aggregate root class for {aggregate_name}",
            "template": "aggregate_root",
            "context": {
                "aggregate_name": aggregate_name,
                "namespace": f"{state['project_namespace']}.{layer.capitalize()}.{aggregate_name}",
                "description": details.get("description", ""),
                "properties": details.get("properties", []),
                "events": details.get("events", []),
                "commands": details.get("commands", [])
            }
        }]
        state["plan"] = changes
        return state

    # fallback
    state["plan"] = []
    return state
