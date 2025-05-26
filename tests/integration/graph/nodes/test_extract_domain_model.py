from pathlib import Path
from graph.nodes.extract_building_blocks import extract_building_blocks


def test_adds_expected_building_blocks_to_state(project_path: Path):
    # Arrange
    state = {}

    # Act
    new_state = extract_building_blocks(state)

    # Assert: domain_model exists and is a list
    assert "domain_model" in new_state, "Expected domain_model key in state"
    building_blocks = new_state["domain_model"]
    assert isinstance(building_blocks, list), "domain_model should be a list"

    # Assert: required keys exist in each building block
    for bb in building_blocks:
        assert isinstance(bb, dict), "Each building block should be a dict"
        assert "type" in bb and "name" in bb and "path" in bb, "Each building block should have type, name, and path"
        assert "namespace" in bb, "Each building block should include namespace"
        assert "properties" in bb and isinstance(bb["properties"], list), "Each building block should have a list of properties"
        assert "methods" in bb and isinstance(bb["methods"], list), "Each building block should have a list of methods"

    # Basic content checks
    block_types = {bb["type"] for bb in building_blocks}
    assert "Aggregate Root" in block_types
    assert "Value Object" in block_types
    assert "Action" in block_types

    _assert_block_names(building_blocks, "Aggregate Root", expected={"Book", "Customer", "Order"})
    _assert_block_names(building_blocks, "Entity", expected={"LineItem"})
    _assert_block_names(building_blocks, "Value Object", expected={"Money"})
    _assert_block_names(building_blocks, "Domain Event", expected={"CustomerRegistered"})
    _assert_block_names(building_blocks, "Domain Event Listener", expected={"CustomerRegisteredListener"})


def _assert_block_names(result: list[dict], block_type: str, expected: set[str]):
    found = {bb["name"] for bb in result if bb["type"] == block_type}
    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing {block_type}s: {missing}"
    assert not extra, f"Unexpected {block_type}s: {extra}"
