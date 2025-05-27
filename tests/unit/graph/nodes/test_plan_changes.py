from graph.nodes.plan_changes import plan_changes


def test_add_aggregate():
    """
    GIVEN this intent:

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

    THEN the plan should include:
    - Creating Customer.cs in src/Orientera/Domain/Model/Customer/
    - Namespace: Orientera.Domain.Model.Customer
    """

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
            "project_name": "Orientera",
            "root_namespace": "Orientera",
            "source_path": "src/",
            "domain_path": "src/Orientera/Domain",
            "infrastructure_path": "src/Orientera/Infrastructure",
            "application_path": "src/Orientera/Application",
            "interchange_path": "src/Orientera/Interchange",
            "tests_path": "src/Orientera.Tests"
        }
    }

    result = plan_changes(state)
    plan = result["plan"]

    assert len(plan) == 1
    change = plan[0]

    assert change["type"] == "create_file"
    assert change["path"] == "src/Orientera/Domain/Model/Customer/Customer.cs"
    assert change["template"] == "aggregate_root"
    assert change["context"]["aggregate_name"] == "Customer"
    assert change["context"]["namespace"] == "Orientera.Domain.Model.Customer"


def test_add_repository_when_efcore():
    """
    GIVEN this intent:

    {
        "intent": "add_repository",
        "target": "Customer"
    }

    And metadata indicating EfCore + Postgres

    THEN the plan should include:
    - Creating ICustomerRepository.cs in Domain.Model.Customer
    - Creating EfCoreCustomerRepository.cs in Infrastructure/Repositories/EfCore
    """

    state = {
        "intent": [
            {
                "intent": "add_repository",
                "target": "Customer"
            }
        ],
        "project_metadata": {
            "project_name": "Orientera",
            "root_namespace": "Orientera",
            "source_path": "src/",
            "domain_path": "src/Orientera/Domain",
            "infrastructure_path": "src/Orientera/Infrastructure",
            "application_path": "src/Orientera/Application",
            "interchange_path": "src/Orientera/Interchange",
            "tests_path": "src/Orientera.Tests",
            "persistence_provider": "EfCore",
            "database_provider": "Postgres"
        }
    }

    result = plan_changes(state)
    plan = result["plan"]

    assert len(plan) == 2

    interface_change = plan[0]
    assert interface_change["type"] == "create_file"
    assert interface_change["path"] == "src/Orientera/Domain/Customer/ICustomerRepository.cs"
    assert interface_change["template"] == "repository/repository_interface"
    assert interface_change["context"]["interface_name"] == "ICustomerRepository"
    assert interface_change["context"]["namespace"] == "Orientera.Domain.Model.Customer"

    impl_change = plan[1]
    assert impl_change["type"] == "create_file"
    assert impl_change["path"] == "src/Orientera/Infrastructure/Repositories/EfCore/EfCoreCustomerRepository.cs"
    assert impl_change["template"] == "repository/efcore_repository_implementation"
    assert impl_change["context"]["class_name"] == "EfCoreCustomerRepository"
    assert impl_change["context"]["interface_name"] == "ICustomerRepository"
    assert impl_change["context"]["namespace"] == "Orientera.Infrastructure.Repositories.EfCore"


def test_add_repository_when_openddd_postgres():
    """
    GIVEN this intent:

    {
        "intent": "add_repository",
        "target": "Customer"
    }

    And metadata indicating OpenDdd + Postgres

    THEN the plan should include:
    - Creating ICustomerRepository.cs in Domain.Model.Customer
    - Creating PostgresOpenDddCustomerRepository.cs in Infrastructure/Repositories/OpenDdd/Postgres/
    """

    state = {
        "intent": [
            {
                "intent": "add_repository",
                "target": "Customer"
            }
        ],
        "project_metadata": {
            "project_name": "Orientera",
            "root_namespace": "Orientera",
            "source_path": "src/",
            "domain_path": "src/Orientera/Domain",
            "infrastructure_path": "src/Orientera/Infrastructure",
            "application_path": "src/Orientera/Application",
            "interchange_path": "src/Orientera/Interchange",
            "tests_path": "src/Orientera.Tests",
            "persistence_provider": "OpenDdd",
            "database_provider": "Postgres"
        }
    }

    result = plan_changes(state)
    plan = result["plan"]

    assert len(plan) == 2

    interface_change = plan[0]
    assert interface_change["type"] == "create_file"
    assert interface_change["path"] == "src/Orientera/Domain/Customer/ICustomerRepository.cs"
    assert interface_change["template"] == "repository/repository_interface"
    assert interface_change["context"]["interface_name"] == "ICustomerRepository"
    assert interface_change["context"]["namespace"] == "Orientera.Domain.Model.Customer"

    impl_change = plan[1]
    assert impl_change["type"] == "create_file"
    assert impl_change["path"] == (
        "src/Orientera/Infrastructure/Repositories/OpenDdd/Postgres/PostgresOpenDddCustomerRepository.cs"
    )
    assert impl_change["template"] == "repository/postgres_openddd_repository_implementation"
    assert impl_change["context"]["class_name"] == "PostgresOpenDddCustomerRepository"
    assert impl_change["context"]["interface_name"] == "ICustomerRepository"
    assert impl_change["context"]["namespace"] == "Orientera.Infrastructure.Repositories.OpenDdd.Postgres"
