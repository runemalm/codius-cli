import os
from pathlib import Path

import pytest

from graph.nodes.extract_domain_model import extract_domain_model
from graph.nodes.generate_domain_vision import generate_domain_vision


@pytest.mark.requires_api  # Optional: mark if this node uses a live LLM call
def test_generate_domain_vision_from_real_project(project_path: Path):
    """Ensure the domain vision node returns a natural language summary based on the domain model."""
    original_cwd = Path.cwd()

    try:
        os.chdir(project_path)

        # Arrange: first extract domain model
        state = {}
        state = extract_domain_model(state)

        # Act: generate vision
        state = generate_domain_vision(state)

        # Assert
        vision = state.get("domain_vision")
        assert vision, "Expected domain_vision in state"
        assert isinstance(vision, str), "Vision statement should be a string"
        assert len(vision) > 20, "Vision statement should be a meaningful sentence"
        assert any(word in vision.lower() for word in ["system", "domain", "aggregates", "models"]), \
            f"Expected domain-related language in vision, got: {vision}"

    finally:
        os.chdir(original_cwd)
