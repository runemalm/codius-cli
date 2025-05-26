import re
from pathlib import Path
from typing import List

from infrastructure.service.code_scanner.model.building_block import BuildingBlock
from infrastructure.service.code_scanner.model.building_block_type import BuildingBlockType


def scan_building_blocks(project_root: Path) -> List[BuildingBlock]:
    return sorted(
        scan_domain_layer(project_root)
        + scan_application_layer(project_root)
        + scan_infrastructure_layer(project_root),
        key=lambda bb: (bb.type.value, bb.name)
    )


def scan_domain_layer(project_root: Path) -> List[BuildingBlock]:
    blocks = []

    for file_path in project_root.rglob("*.cs"):
        if "Domain" not in file_path.parts:
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        class_name = file_path.stem

        if re.search(rf'\bclass\s+{class_name}\s*:\s*AggregateRootBase<', content):
            blocks.append(_bb(BuildingBlockType.AGGREGATE_ROOT, class_name, file_path))
        elif re.search(rf'\bclass\s+{class_name}\s*:\s*EntityBase<', content):
            blocks.append(_bb(BuildingBlockType.ENTITY, class_name, file_path))
        elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIValueObject\b', content):
            blocks.append(_bb(BuildingBlockType.VALUE_OBJECT, class_name, file_path))
        elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIDomainEvent\b', content):
            blocks.append(_bb(BuildingBlockType.DOMAIN_EVENT, class_name, file_path))
        elif re.search(r'\binterface\s+I\w+Repository\b', content):
            blocks.append(_bb(BuildingBlockType.REPOSITORY, class_name, file_path))
        elif "IDomainService" in content:
            blocks.append(_bb(BuildingBlockType.DOMAIN_SERVICE, class_name, file_path))
        elif "Ports" in str(file_path) and re.search(rf'\binterface\s+I\w+\s*:\s*.*\bIPort\b', content):
            blocks.append(_bb(BuildingBlockType.PORT, class_name, file_path))

    return blocks



def scan_application_layer(project_root: Path) -> List[BuildingBlock]:
    blocks = []

    for file_path in project_root.rglob("*.cs"):
        if "Application" not in file_path.parts:
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        class_name = file_path.stem

        if re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bIAction<', content):
            blocks.append(_bb(BuildingBlockType.ACTION, class_name, file_path))
        elif re.search(rf'\bclass\s+{class_name}\s*:\s*.*\bICommand\b', content):
            blocks.append(_bb(BuildingBlockType.COMMAND, class_name, file_path))
        elif "EventListenerBase" in content:
            if class_name.endswith("IntegrationEventListener"):
                blocks.append(_bb(BuildingBlockType.INTEGRATION_EVENT_LISTENER, class_name, file_path))
            else:
                blocks.append(_bb(BuildingBlockType.DOMAIN_EVENT_LISTENER, class_name, file_path))

    return blocks


def scan_infrastructure_layer(project_root: Path) -> List[BuildingBlock]:
    blocks = []

    for file_path in project_root.rglob("*.cs"):
        if "Infrastructure" not in file_path.parts:
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        class_name = file_path.stem

        if "IInfrastructureService" in content:
            blocks.append(_bb(BuildingBlockType.INFRASTRUCTURE_SERVICE, class_name, file_path))
        elif "Adapters" in str(file_path) and re.search(rf'\bclass\s+{class_name}\s*:\s*I\w+Port\b', content):
            blocks.append(_bb(BuildingBlockType.ADAPTER, class_name, file_path))

    return blocks


def _bb(block_type: BuildingBlockType, name: str, file_path: Path) -> BuildingBlock:
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # Extract namespace
    namespace_match = re.search(r'namespace\s+([\w\.]+)', content)
    namespace = namespace_match.group(1) if namespace_match else None

    # Extract public properties (simple heuristic)
    properties = re.findall(r'public\s+\w+\s+(\w+)\s*\{', content)

    # Extract public methods (skip constructors and properties)
    methods = re.findall(r'public\s+\w+\s+(\w+)\s*\([^)]*\)\s*\{', content)

    return BuildingBlock(
        type=block_type,
        name=name,
        file_path=file_path,
        namespace=namespace,
        properties=sorted(set(properties)),
        methods=sorted(set(methods)),
    )
