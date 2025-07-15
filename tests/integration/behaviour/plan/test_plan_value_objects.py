import pytest
from codius.graph.nodes.plan_changes import plan_changes


@pytest.mark.integration
def test_plan_add_value_object_step(tmp_path):
    # Arrange: simulate minimal project structure
    state = {
        "intent": [
            {
                "intent": "add_value_object",
                "target": "Color",
                "properties": [
                    { "name": "Name", "type": "string" },
                    { "name": "HexCode", "type": "string" }
                ]
            }
        ],
        "sources": {},
        "project_metadata": {
            "project_name": "MyApp",
            "root_namespace": "MyApp",
            "project_root": str(tmp_path),
            "source_path": str(tmp_path),
            "domain_path": str(tmp_path / "Domain"),
            "application_path": str(tmp_path / "Application"),
            "infrastructure_path": str(tmp_path / "Infrastructure"),
            "interchange_path": str(tmp_path / "Interchange"),
            "tests_path": str(tmp_path / "Tests")
        }
    }

    # Act
    result = plan_changes(state)

    # Assert
    assert "plan" in result
    plan = result["plan"]
    assert isinstance(plan, list)

    create_steps = [step for step in plan if step.get("type") == "create_file"]
    assert any("Color.cs" in step.get("path", "") for step in create_steps)

    # Optional: print for manual inspection
    for step in plan:
        print(step)
