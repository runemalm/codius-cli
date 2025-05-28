import logging

logger = logging.getLogger(__name__)


def plan_changes(state: dict) -> dict:
    logger.debug("Running plan_changes...")

    plan = []
    project_metadata = state.get("project_metadata")
    logger.debug("Project metadata loaded: %s", project_metadata)

    for raw_intent in state.get("intent", []):
        logger.debug("Processing raw intent: %s", raw_intent)

        # Enforce conventions
        intent_type = raw_intent.get("intent")
        if intent_type == "add_aggregate":
            intent = _enforce_aggregate_conventions(raw_intent)
            plan.extend(_plan_aggregate(intent, project_metadata))
        elif intent_type == "add_repository":
            intent = _enforce_repository_conventions(raw_intent)
            plan.extend(_plan_repository(intent, project_metadata))
        else:
            logger.warning("Unsupported intent type: %s", intent_type)

    logger.debug("Generated plan with %d changes", len(plan))
    state["plan"] = plan
    return state


def _enforce_aggregate_conventions(intent: dict) -> dict:
    logger.debug("Enforcing aggregate conventions...")

    details = intent.setdefault("details", {})
    details.setdefault("properties", [])
    details.setdefault("commands", [])
    details.setdefault("events", [])

    return intent


def _enforce_repository_conventions(intent: dict) -> dict:
    logger.debug("Enforcing repository conventions...")

    details = intent.setdefault("details", {})
    methods = details.get("custom_methods", [])

    for method in methods:
        method.setdefault("is_async", True)

        name = method.get("name")
        if name and not name.endswith("Async"):
            method["name"] = f"{name}Async"

        method.setdefault("parameters", [])

    return intent


def _plan_aggregate(intent: dict, metadata: dict) -> list:
    """Generate plan items for an add_aggregate intent."""
    logger.debug("Planning aggregate creation...")

    aggregate_name = intent.get("target")
    details = intent.get("details", {})

    domain_path = metadata["domain_path"]
    root_namespace = metadata["root_namespace"]

    path = f"{domain_path}/Model/{aggregate_name}/{aggregate_name}.cs"
    namespace = f"{root_namespace}.Domain.Model.{aggregate_name}"

    logger.debug("Creating aggregate file for '%s' at %s", aggregate_name, path)

    return [{
        "type": "create_file",
        "path": path,
        "description": f"Create aggregate root class for {aggregate_name}",
        "template": "aggregate_root",
        "context": {
            "aggregate_name": aggregate_name,
            "namespace": namespace,
            "description": details.get("description", ""),
            "properties": details.get("properties", []),
            "events": details.get("events", []),
            "commands": details.get("commands", [])
        }
    }]


def _plan_repository(intent: dict, metadata: dict) -> list:
    """Generate plan items for an add_repository intent."""
    logger.debug("Planning repository creation...")

    plan = []
    aggregate = intent.get("target")
    details = intent.get("details", {})
    custom_methods = details.get("custom_methods", [])
    implementations = details.get("implementations", [])

    default_persistence = metadata.get("persistence_provider", "OpenDDD")
    default_database = metadata.get("database_provider", "Postgres")

    if not implementations:
        logger.debug("No implementations provided. Using default persistence/database.")
        implementations.append({"persistence": default_persistence})
        if default_persistence.lower() == "openddd":
            implementations[-1]["database"] = default_database
    else:
        for impl in implementations:
            impl.setdefault("persistence", default_persistence)
            if impl["persistence"].lower() == "openddd":
                impl.setdefault("database", default_database)

    domain_path = metadata["domain_path"]
    infrastructure_path = metadata["infrastructure_path"]
    root_namespace = metadata["root_namespace"]

    interface_name = f"I{aggregate}Repository"
    interface_namespace = f"{root_namespace}.Domain.Model.{aggregate}"
    interface_path = f"{domain_path}/Model/{aggregate}/{interface_name}.cs"

    logger.debug("Creating interface file at %s", interface_path)

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

    for impl in implementations:
        persistence = impl["persistence"]
        database = impl.get("database")
        logger.debug("Planning implementation: %s with DB: %s", persistence, database)

        if persistence.lower() == "efcore":
            class_name = f"EfCore{aggregate}Repository"
            rel_path = f"Repositories/EfCore/{class_name}.cs"
            impl_namespace = f"{root_namespace}.Infrastructure.Repositories.EfCore"
            template = "repository/efcore_repository_implementation"

        elif persistence.lower() == "openddd":
            if not database:
                raise ValueError("OpenDDD persistence requires a database provider")
            class_name = f"{database}OpenDdd{aggregate}Repository"
            rel_path = f"Repositories/OpenDdd/{database}/{class_name}.cs"
            impl_namespace = f"{root_namespace}.Infrastructure.Repositories.OpenDdd.{database}"
            template = f"repository/{database.lower()}_openddd_repository_implementation"

        else:
            raise ValueError(f"Unsupported persistence provider: {persistence}")

        full_path = f"{infrastructure_path}/{rel_path}"
        domain_namespace = f"{root_namespace}.Domain.Model.{aggregate}"

        logger.debug("Creating implementation file at %s", full_path)

        plan.append({
            "type": "create_file",
            "path": full_path,
            "template": template,
            "description": f"Create {class_name} implementation of {interface_name}",
            "context": {
                "aggregate_name": aggregate,
                "domain_namespace": domain_namespace,
                "implementation_namespace": impl_namespace,
                "custom_methods": custom_methods
            }
        })

    return plan
