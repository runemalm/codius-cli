import logging

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    logger.debug("Running plan_changes...")

    plan = []
    project_metadata = state.get("project_metadata")

    for intent in state.get("intent", []):
        if intent.get("intent") == "add_aggregate":
            aggregate_name = intent.get("target")
            details = intent.get("details", {})

            changes = [{
                "type": "create_file",
                "path": f"{project_metadata[f'domain_path']}/Model/{aggregate_name}/{aggregate_name}.cs",
                "description": f"Create aggregate root class for {aggregate_name}",
                "template": "aggregate_root",
                "context": {
                    "aggregate_name": aggregate_name,
                    "namespace": f"{project_metadata['root_namespace']}.Domain.Model.{aggregate_name}",
                    "description": details.get("description", ""),
                    "properties": details.get("properties", []),
                    "events": details.get("events", []),
                    "commands": details.get("commands", [])
                }
            }]
            plan.extend(changes)

        elif intent.get("intent") == "add_repository":
            aggregate = intent.get("target")
            details = intent.get("details", {})
            implementations = details.get("implementations")

            # Repository Interface Path
            domain_path = project_metadata["domain_path"]
            interface_name = f"I{aggregate}Repository"
            interface_path = f"{domain_path}/Model/{aggregate}/{interface_name}.cs"

            # Add interface creation to plan
            plan.append({
                "type": "create_file",
                "path": interface_path,
                "template": "repository/repository_interface",
                "description": f"Create {interface_name} interface in domain model",
                "context": {
                    "aggregate_name": aggregate,
                    "interface_name": interface_name,
                    "namespace": f"{project_metadata['root_namespace']}.Domain.Model.{aggregate}",
                    "custom_methods": details.get("custom_methods", [])  # Optional
                }
            })

            # Determine implementations
            if not implementations:
                persistence = project_metadata.get("persistence_provider", "OpenDdd")
                database = project_metadata.get("database_provider", "Postgres")
                implementations = [{"persistence": persistence, "database": database}]

            for impl in implementations:
                persistence = impl["persistence"]
                database = impl.get("database")  # Optional for EfCore

                if persistence.lower() == "efcore":
                    class_name = f"EfCore{aggregate}Repository"
                    rel_path = f"Repositories/EfCore/{class_name}.cs"
                    namespace = f"{project_metadata['root_namespace']}.Infrastructure.Repositories.EfCore"
                else:
                    class_name = f"{database}{persistence}{aggregate}Repository"
                    rel_path = f"Repositories/{persistence}/{database}/{class_name}.cs"
                    namespace = f"{project_metadata['root_namespace']}.Infrastructure.Repositories.{persistence}.{database}"

                full_path = f"{project_metadata['infrastructure_path']}/{rel_path}"

                plan.append({
                    "type": "create_file",
                    "path": full_path,
                    "template": _resolve_repository_template(persistence, database),
                    "description": f"Create {class_name} implementation of {interface_name}",
                    "context": {
                        "aggregate_name": aggregate,
                        "interface_name": interface_name,
                        "class_name": class_name,
                        "namespace": namespace,
                        "persistence_provider": persistence,
                        "database_provider": database,
                        "custom_methods": details.get("custom_methods", [])  # Optional
                    }
                })

    state["plan"] = plan
    return state

def _resolve_repository_template(persistence: str, database: str | None) -> str:
    persistence = persistence.lower()
    database = (database or "").lower()

    if persistence == "efcore":
        return "repository/efcore_repository_implementation"
    elif persistence == "openddd":
        if database == "postgres":
            return "repository/postgres_openddd_repository_implementation"
        else:
            raise ValueError(f"No repository template for OpenDdd + {database}")
    else:
        raise ValueError(f"Unsupported persistence provider: {persistence}")

