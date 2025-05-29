import logging
from pathlib import Path

from di import container
from infrastructure.services.code_scanner.code_scanner_service import CodeScannerService

logger = logging.getLogger(__name__)


def extract_building_blocks(state: dict) -> dict:
    logger.debug("Running extract_domain_model...")

    logger.debug("Scanning building blocks in project..")

    code_scanner_service = container.resolve(CodeScannerService)

    blocks = code_scanner_service.scan_building_blocks(state['project_metadata'])

    logger.info("Extracted %d domain building blocks", len(blocks))

    # Store in state
    state["building_blocks"] = [b.to_dict() for b in blocks]

    return state
