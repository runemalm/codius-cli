import logging

from codius.domain.model.plan_steps.create_file_step import CreateFileStep

logger = logging.getLogger(__name__)


def plan_aggregate(intent: dict, metadata: dict, existing_paths: set) -> tuple[list, list]:
    logger.debug("Planning aggregate creation...")

    aggregate_name = intent.get("target")
    details = intent.get("details", {})

    domain_path = metadata["domain_path"]
    root_namespace = metadata["root_namespace"]

    path = f"{domain_path}/Model/{aggregate_name}/{aggregate_name}.cs"
    namespace = f"{root_namespace}.Domain.Model.{aggregate_name}"

    if path in existing_paths:
        msg = f"⚠️ `{aggregate_name}` aggregate already exists. Skipping creation."
        logger.info(msg)
        return [], [msg]

    logger.debug("Creating aggregate file for '%s' at %s", aggregate_name, path)

    return ([CreateFileStep(
        path=path,
        description=f"Create aggregate root class for {aggregate_name}",
        template="aggregate_root",
        context={
            "aggregate_name": aggregate_name,
            "namespace": namespace,
            "description": details.get("description", ""),
            "properties": details.get("properties", []),
            "events": details.get("events", []),
            "commands": details.get("commands", [])
        }
    ).to_dict()], [])
