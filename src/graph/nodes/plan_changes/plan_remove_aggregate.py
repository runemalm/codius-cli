import logging
from pathlib import Path

from domain.model.plan_steps.delete_file_step import DeleteFileStep

logger = logging.getLogger(__name__)


def plan_remove_aggregate(intent: dict, metadata: dict) -> tuple[list, list]:
    logger.debug("Planning aggregate deletion...")

    aggregate_name = intent.get("target")
    domain_path = metadata["domain_path"]
    file_path = f"{domain_path}/Model/{aggregate_name}/{aggregate_name}.cs"

    if not Path(file_path).exists():
        msg = f"⚠️ Cannot delete `{aggregate_name}`: file does not exist at `{file_path}`."
        logger.warning(msg)
        return [], [msg]

    logger.debug("Deleting aggregate file at %s", file_path)

    return ([DeleteFileStep(
        path=file_path,
        description=f"Delete aggregate root class {aggregate_name}"
    ).to_dict()], [])
