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
            custom_methods = details.get("custom_methods", [])
            implementations = details.get("implementations", [])

            # Fallback to providers in metadata, if not specified by user in intent
            default_persistence = project_metadata.get("persistence_provider", "OpenDDD")
            default_database = project_metadata.get("database_provider", "Postgres")

            # If no implementations were listed at all
            if not implementations:
                implementations.append({"persistence": default_persistence})
                if default_persistence.lower() == "openddd":
                    implementations[-1]["database"] = default_database
            else:
                for impl in implementations:
                    if "persistence" not in impl:
                        impl["persistence"] = default_persistence
                    if impl["persistence"].lower() == "openddd" and "database" not in impl:
                        impl["database"] = default_database

            # Paths
            domain_path = project_metadata["domain_path"]
            infrastructure_path = project_metadata["infrastructure_path"]
            root_namespace = project_metadata["root_namespace"]

            # Repository Interface
            interface_name = f"I{aggregate}Repository"
            interface_namespace = f"{root_namespace}.Domain.Model.{aggregate}"
            interface_path = f"{domain_path}/Model/{aggregate}/{interface_name}.cs"

            plan.append({
                "type": "create_file",
                "path": interface_path,
                "template": "repository/repository_interface",
                "description": f"Create {interface_name} interface",
                "context": {
                    "aggregate_name": aggregate,
                    "namespace": interface_namespace,
                    "custom_methods": custom_methods
                }
            })

            # Implementations
            for impl in implementations:
                persistence = impl["persistence"]
                database = impl.get("database")  # optional

                if persistence.lower() == "efcore":
                    class_name = f"EfCore{aggregate}Repository"
                    rel_path = f"Repositories/EfCore/{class_name}.cs"
                    implementation_namespace = f"{root_namespace}.Infrastructure.Repositories.EfCore"
                    template = "repository/efcore_repository_implementation"
                    domain_namespace = f"{root_namespace}.Domain.Model.{aggregate}"

                elif persistence.lower() == "openddd":
                    if database is None:
                        raise ValueError(
                            "OpenDDD persistence requires a database provider")
                    class_name = f"{database}OpenDdd{aggregate}Repository"
                    rel_path = f"Repositories/OpenDdd/{database}/{class_name}.cs"
                    implementation_namespace = f"{root_namespace}.Infrastructure.Repositories.OpenDdd.{database}"
                    template = f"repository/postgres_openddd_repository_implementation" if database.lower() == "postgres" else \
                        f"repository/sqlite_openddd_repository_implementation"  # add this template if needed
                    domain_namespace = f"{root_namespace}.Domain.Model.{aggregate}"

                else:
                    raise ValueError(f"Unsupported persistence provider: {persistence}")

                full_path = f"{infrastructure_path}/{rel_path}"

                plan.append({
                    "type": "create_file",
                    "path": full_path,
                    "template": template,
                    "description": f"Create {class_name} implementation of {interface_name}",
                    "context": {
                        "aggregate_name": aggregate,
                        "domain_namespace": domain_namespace,
                        "implementation_namespace": implementation_namespace,
                        "custom_methods": custom_methods
                    }
                })

    state["plan"] = plan
    return state
