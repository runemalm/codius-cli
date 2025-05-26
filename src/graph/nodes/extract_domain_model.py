import logging
from pathlib import Path

from infrastructure.service.code_scanner.code_scanner import scan_building_blocks

logger = logging.getLogger(__name__)


def extract_domain_model(state: dict) -> dict:
    logger.debug("Running extract_domain_model...")

    project_root = Path(".").resolve()
    logger.debug("Scanning building blocks in project: %s", project_root)

    blocks = scan_building_blocks(project_root)

    domain_model = [
        {
            "type": block.type.value,
            "name": block.name,
            "path": str(block.file_path.relative_to(project_root))
        }
        for block in blocks
    ]

    logger.info("Extracted %d domain building blocks", len(domain_model))

    # Store in state
    state["domain_model"] = domain_model

    return state
