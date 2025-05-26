from pathlib import Path

import pytest

from graph.nodes.extract_domain_model import extract_domain_model
from graph.nodes.generate_domain_vision import generate_domain_vision


@pytest.mark.makes_llm_calls
@pytest.mark.integration
def test_generate_domain_vision_from_real_project(project_path: Path):
    """Ensure the domain vision node returns a natural language summary based on the domain model."""

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
    assert any(word in vision.lower() for word in ["customer", "order", "book"]), \
        f"Expected domain-related language in vision, got: {vision}"
