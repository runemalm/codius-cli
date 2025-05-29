from typing import List, Dict
from infrastructure.services.code_scanner.model.building_block import BuildingBlock
from infrastructure.services.code_scanner.scanners.bb_scanner import BuildingBlockScanner
from infrastructure.services.code_scanner.scanners.flow_scanner import FlowScanner


class CodeScannerService:
    def scan_building_blocks(self, project_metadata: Dict) -> List[BuildingBlock]:
        scanner = BuildingBlockScanner()
        return scanner.scan(project_metadata)

    def scan_flows(self, building_blocks: List[BuildingBlock]) -> List[FlowScanner.Flow]:
        scanner = FlowScanner()
        return scanner.scan(building_blocks)
