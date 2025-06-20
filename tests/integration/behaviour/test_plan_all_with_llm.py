import pytest
from graph.nodes.plan_changes.plan_all_with_llm import plan_all_with_llm


@pytest.mark.integration
def test_plan_add_invoice_method_real_llm(tmp_path):
    # Arrange: write minimal source file for the aggregate
    source_file = tmp_path / "Domain" / "Model" / "Invoice" / "Invoice.cs"
    source_file.parent.mkdir(parents=True, exist_ok=True)
    source_file.write_text("// public class Invoice { public void RegisterPayment() {} }")

    state = {
        "intent": [
            {
                "intent": "add_aggregate_method",
                "target": "Invoice",
                "building_block_type": "AGGREGATE_ROOT",
                "method": {
                    "name": "CalculateBalance",
                    "parameters": [],
                    "return_type": "decimal",
                    "is_async": False,
                    "location": {
                        "position": "after",
                        "reference": "RegisterPayment"
                    },
                    "implementation": {
                        "type": "generate",
                        "hint": "Return total minus sum of payments"
                    }
                }
            }
        ],
        "sources": {
            str(source_file): source_file.read_text()
        },
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
    result = plan_all_with_llm(state)

    # Assert
    assert "plan" in result
    plan = result["plan"]
    assert isinstance(plan, list)
    assert any(step.get("type") in ("modify_file", "create_file") for step in plan)

    # Optional: print for manual inspection
    for step in plan:
        print(step)
