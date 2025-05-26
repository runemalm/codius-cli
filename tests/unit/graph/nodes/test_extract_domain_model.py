import os
from pathlib import Path

from graph.nodes.extract_domain_model import extract_domain_model


def test_adds_expected_domain_model_to_state(project_path: Path):
    original_cwd = Path.cwd()

    try:
        os.chdir(project_path)

        # Arrange
        state = {}

        # Act
        new_state = extract_domain_model(state)

        # Assert
        assert "domain_model" in new_state, "Expected domain_model key in state"
        assert isinstance(new_state["domain_model"], list), "domain_model should be a list"
        assert all("type" in bb and "name" in bb and "path" in bb for bb in new_state["domain_model"]), \
            "Each building block should have type, name, and path"

        # Basic content checks (you can expand these)
        block_types = {bb["type"] for bb in new_state["domain_model"]}
        assert "Aggregate Root" in block_types
        assert "Value Object" in block_types
        assert "Action" in block_types

        _assert_block_names(
            new_state["domain_model"],
            "Aggregate Root",
            expected={"Book", "Customer", "Order"}
        )
        _assert_block_names(
            new_state["domain_model"],
            "Entity",
            expected={"LineItem"}
        )
        _assert_block_names(
            new_state["domain_model"],
            "Value Object",
            expected={"Money"}
        )
        _assert_block_names(
            new_state["domain_model"],
            "Domain Event",
            expected={"CustomerRegistered"}
        )
        _assert_block_names(
            new_state["domain_model"],
            "Domain Event Listener",
            expected={"CustomerRegisteredListener"}
        )

    finally:
        os.chdir(original_cwd)


def _assert_block_names(result: list[dict], block_type: str, expected: set[str]):
    found = {bb["name"] for bb in result if bb["type"] == block_type}
    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing {block_type}s: {missing}"
    assert not extra, f"Unexpected {block_type}s: {extra}"