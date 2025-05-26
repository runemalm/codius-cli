import logging
from dependency_injection.container import DependencyContainer
from infrastructure.service.project_scanner_service import ProjectScannerService

logger = logging.getLogger(__name__)


def extract_project_metadata(state: dict) -> dict:
    logger.debug("Running extract_project_metadata...")

    container = DependencyContainer.get_instance()
    scanner = container.resolve(ProjectScannerService)

    namespace = scanner.extract_project_namespace()
    state["project_namespace"] = namespace

    logger.info("Extracted project_namespace: %s", namespace)
    return state
