import logging

from di import container
from infrastructure.services.project_scanner_service import ProjectScannerService

logger = logging.getLogger(__name__)


def extract_project_metadata(state: dict) -> dict:
    logger.debug("Running extract_project_metadata...")

    scanner = container.resolve(ProjectScannerService)

    metadata = scanner.extract_project_metadata()
    state["project_metadata"] = metadata

    logger.info("Extracted project metadata: %s", metadata)
    return state
