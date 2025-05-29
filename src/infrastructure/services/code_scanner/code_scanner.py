import re
from pathlib import Path
from typing import List, Dict

from infrastructure.services.code_scanner.model.building_block import BuildingBlock
from infrastructure.services.code_scanner.model.building_block_type import BuildingBlockType


class CodeScannerService:
    def scan_building_blocks(self, project_metadata: Dict) -> List[BuildingBlock]:
        return sorted(
            self._scan_domain_layer(project_metadata),
            key=lambda bb: (bb.type.value, bb.name)
        ) + sorted(
            self._scan_application_layer(project_metadata),
            key=lambda bb: (bb.type.value, bb.name)
        ) + sorted(
            self._scan_infrastructure_layer(project_metadata),
            key=lambda bb: (bb.type.value, bb.name)
        )

    def _scan_domain_layer(self, project_metadata: Dict) -> List[BuildingBlock]:
        domain_path = Path(project_metadata["domain_path"])
        blocks = []

        for file_path in domain_path.rglob("*.cs"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            class_name = file_path.stem

            if re.search(rf'\bclass\s+{class_name}\s*:\s*AggregateRootBase<', content):
                blocks.append(self._create_building_block(BuildingBlockType.AGGREGATE_ROOT, class_name, file_path))
            elif re.search(rf'\bclass\s+{class_name}\s*:\s*EntityBase<', content):
                blocks.append(self._create_building_block(BuildingBlockType.ENTITY, class_name, file_path))
            elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIValueObject\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.VALUE_OBJECT, class_name, file_path))
            elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIDomainEvent\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.DOMAIN_EVENT, class_name, file_path))
            elif re.search(r'\binterface\s+I\w+Repository\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.REPOSITORY, class_name, file_path))
            elif "IDomainService" in content:
                blocks.append(self._create_building_block(BuildingBlockType.DOMAIN_SERVICE, class_name, file_path))
            elif "Ports" in str(file_path) and re.search(rf'\binterface\s+I\w+\s*:\s*.*\bIPort\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.PORT, class_name, file_path))

        return blocks

    def _scan_application_layer(self, project_metadata: Dict) -> List[BuildingBlock]:
        application_path = Path(project_metadata["application_path"])
        blocks = []

        for file_path in application_path.rglob("*.cs"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            class_name = file_path.stem

            if re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIAction<', content):
                blocks.append(self._create_building_block(BuildingBlockType.ACTION, class_name, file_path))
            elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bICommand\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.COMMAND, class_name, file_path))
            elif "EventListenerBase" in content:
                if class_name.endswith("IntegrationEventListener"):
                    blocks.append(self._create_building_block(BuildingBlockType.INTEGRATION_EVENT_LISTENER, class_name, file_path))
                else:
                    blocks.append(self._create_building_block(BuildingBlockType.DOMAIN_EVENT_LISTENER, class_name, file_path))

        return blocks

    def _scan_infrastructure_layer(self, project_metadata: Dict) -> List[BuildingBlock]:
        infrastructure_path = Path(project_metadata["infrastructure_path"])
        blocks = []

        for file_path in infrastructure_path.rglob("*.cs"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            class_name = file_path.stem

            if "IInfrastructureService" in content:
                blocks.append(self._create_building_block(BuildingBlockType.INFRASTRUCTURE_SERVICE, class_name, file_path))
            elif "Adapters" in str(file_path) and re.search(rf'\bclass\s+{class_name}\s*:\s*I\w+Port\b', content):
                blocks.append(self._create_building_block(BuildingBlockType.ADAPTER, class_name, file_path))

        return blocks

    def _create_building_block(self, block_type: BuildingBlockType, name: str, file_path: Path) -> BuildingBlock:
        content = file_path.read_text(encoding="utf-8", errors="ignore")

        namespace_match = re.search(r'namespace\s+([\w\.]+)', content)
        namespace = namespace_match.group(1) if namespace_match else None

        properties = re.findall(r'public\s+\w+\s+(\w+)\s*\{', content)
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\([^)]*\)\s*\{', content)

        return BuildingBlock(
            type=block_type,
            name=name,
            file_path=file_path,
            namespace=namespace,
            properties=sorted(set(properties)),
            methods=sorted(set(methods)),
        )
