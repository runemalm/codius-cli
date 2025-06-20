from pathlib import Path

from graph.nodes.extract_building_blocks import extract_building_blocks
from infrastructure.services.code_scanner.model.building_block_type import BuildingBlockType


def test_adds_expected_building_blocks_to_state(bookstore_project_path: Path):
    # Arrange
    state = {
        "project_metadata": {
            "project_root": str(bookstore_project_path),
            "source_path": str(bookstore_project_path / "src"),
            "domain_path": bookstore_project_path / "src/Bookstore/Domain",
            "application_path": bookstore_project_path / "src/Bookstore/Application",
            "infrastructure_path": bookstore_project_path / "src/Bookstore/Infrastructure",
        }
    }

    # Act
    new_state = extract_building_blocks(state)

    # Assert: building_blocks exists and is a list of dicts
    assert "building_blocks" in new_state, "Expected building_blocks key in state"
    building_blocks = new_state["building_blocks"]
    assert isinstance(building_blocks, list), "building_blocks should be a list"

    for bb in building_blocks:
        assert isinstance(bb, dict), "Each building block should be a dict"
        assert set(bb.keys()).issuperset({"type", "name", "file_path", "namespace", "properties", "methods"}), \
            "Each building block must include required fields"
        assert isinstance(bb["type"], str), "type should be a string (enum value)"
        assert isinstance(bb["name"], str), "name should be a string"
        assert isinstance(bb["file_path"], str), "file_path should be a string"
        assert isinstance(bb["properties"], list), "properties should be a list"
        assert isinstance(bb["methods"], list), "methods should be a list"

    # Content checks
    block_types = {bb["type"] for bb in building_blocks}
    assert BuildingBlockType.AGGREGATE_ROOT.value in block_types
    assert BuildingBlockType.VALUE_OBJECT.value in block_types
    assert BuildingBlockType.ACTION.value in block_types

    _assert_block_names(building_blocks, BuildingBlockType.AGGREGATE_ROOT, expected={"Book", "Customer", "Order"})
    _assert_block_names(building_blocks, BuildingBlockType.ENTITY, expected={"LineItem"})
    _assert_block_names(building_blocks, BuildingBlockType.VALUE_OBJECT, expected={"Money"})
    _assert_block_names(building_blocks, BuildingBlockType.DOMAIN_EVENT, expected={"CustomerRegistered"})
    _assert_block_names(building_blocks, BuildingBlockType.DOMAIN_EVENT_LISTENER, expected={"CustomerRegisteredListener"})


def _assert_block_names(blocks: list[dict], block_type: BuildingBlockType, expected: set[str]):
    found = {bb["name"] for bb in blocks if bb["type"] == block_type.value}
    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing {block_type.value}s: {missing}"
    assert not extra, f"Unexpected {block_type.value}s: {extra}"
