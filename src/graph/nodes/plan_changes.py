import logging

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    logger.debug("Running plan_changes...")

    plan = []
    project_metadata = state.get("project_metadata")

    for intent in state.get("intent", []):
        if intent.get("intent") == "add_aggregate":
            aggregate_name = intent.get("target")
            layer = intent.get("layer", "domain")
            details = intent.get("details", {})

            changes = [{
                "type": "create_file",
                "path": f"{project_metadata[f'domain_path']}/Model/{aggregate_name}/{aggregate_name}.cs",
                "description": f"Create aggregate root class for {aggregate_name}",
                "template": "aggregate_root",
                "context": {
                    "aggregate_name": aggregate_name,
                    "namespace": f"{project_metadata['root_namespace']}.Domain.Model.{aggregate_name}",
                    "description": details.get("description", ""),
                    "properties": details.get("properties", []),
                    "events": details.get("events", []),
                    "commands": details.get("commands", [])
                }
            }]
            plan.extend(changes)

    state["plan"] = plan
    return state
