import logging

from domain.model.plan_steps.modify_file_step import ModifyFileStep

logger = logging.getLogger(__name__)


def plan_add_aggregate_method(intent: dict, metadata: dict, existing_paths: set) -> tuple[list, list]:
    logger.debug("Planning to add method to aggregate...")

    aggregate_name = intent.get("target")
    method = intent.get("method", {})
    placement = intent.get("placement", {})  # optional
    hint = intent.get("hint")  # optional

    domain_path = metadata["domain_path"]
    root_namespace = metadata["root_namespace"]
    path = f"{domain_path}/Model/{aggregate_name}/{aggregate_name}.cs"

    if path not in existing_paths:
        msg = f"⚠️ Aggregate `{aggregate_name}` not found at expected path: {path}"
        logger.warning(msg)
        return [], [msg]

    step = ModifyFileStep(
        path=path,
        description=f"Add method `{method['name']}` to aggregate `{aggregate_name}`",
        modification="add_method",
        context={
            "aggregate_name": aggregate_name,
            "namespace": f"{root_namespace}.Domain.Model.{aggregate_name}",
            "method": method,
            "placement": placement,
            "reasoning_hint": hint
        }
    )

    return [step.to_dict()], []
