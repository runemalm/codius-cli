import logging
from pathlib import Path

from infrastructure.services.code_scanner.code_scanner import scan_building_blocks

logger = logging.getLogger(__name__)


def extract_building_blocks(state: dict) -> dict:
    logger.debug("Running extract_domain_model...")

    project_root = Path(".").resolve()
    logger.debug("Scanning building blocks in project: %s", project_root)

    blocks = scan_building_blocks(project_root)

    logger.info("Extracted %d domain building blocks", len(blocks))

    # Store in state
    state["building_blocks"] = [b.to_dict() for b in blocks]

    return state
