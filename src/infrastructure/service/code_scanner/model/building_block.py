from dataclasses import dataclass
from pathlib import Path

from infrastructure.service.code_scanner.model.building_block_type import \
    BuildingBlockType


@dataclass
class BuildingBlock:
    type: BuildingBlockType
    name: str
    file_path: Path
