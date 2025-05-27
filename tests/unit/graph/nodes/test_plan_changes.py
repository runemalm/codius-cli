from graph.nodes.plan_changes import plan_changes


def test_plan_changes_uses_project_metadata():
    # Arrange
    state = {
        "intent": [
            {
                "intent": "add_aggregate",
                "target": "Customer",
                "layer": "domain",
                "details": {
                    "description": "Represents a customer in the system.",
                    "properties": [{"name": "Id", "type": "Guid"}],
                    "events": [{"name": "CustomerCreated"}],
                    "commands": [{"name": "CreateCustomer"}]
                }
            }
        ],
        "project_metadata": {
            "source_path": "src",
            "tests_path": "src/Bookstore.Tests",
            "domain_path": "src/Bookstore/Domain",
            "application_path": "src/Bookstore/Application",
            "infrastructure_path": "src/Bookstore/Infrastructure",
            "interchange_path": "src/Bookstore/Interchange",
            "project_name": "Bookstore",
            "root_namespace": "Bookstore",
        }
    }

    # Act
    result = plan_changes(state)

    # Assert
    plan = result.get("plan")
    assert plan is not None, "Expected 'plan' in state"
    assert len(plan) == 1

    change = plan[0]
    assert change["type"] == "create_file"
    assert change["path"] == "src/Bookstore/Domain/Model/Customer/Customer.cs"
    assert change["template"] == "aggregate_root"
    assert change["description"] == "Create aggregate root class for Customer"

    context = change["context"]
    assert context["aggregate_name"] == "Customer"
    assert context["namespace"] == "Bookstore.Domain.Model.Customer"
    assert context["description"] == "Represents a customer in the system."
    assert context["properties"] == [{"name": "Id", "type": "Guid"}]
    assert context["events"] == [{"name": "CustomerCreated"}]
    assert context["commands"] == [{"name": "CreateCustomer"}]
