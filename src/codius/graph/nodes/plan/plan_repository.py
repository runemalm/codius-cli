import logging

from codius.domain.model.plan_steps.create_file_step import CreateFileStep

logger = logging.getLogger(__name__)


def plan_repository(intent: dict, metadata: dict, existing_paths: set) -> tuple[list, list]:
    logger.debug("Planning repository creation...")

    warnings = []
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

    if interface_path in existing_paths:
        msg = f"⚠️ Repository interface for `{aggregate}` already exists at `{interface_path}`. Skipping interface creation."
        logger.info(msg)
        warnings.append(msg)
    else:
        plan.append(CreateFileStep(
            path=interface_path,
            description=f"Create {interface_name} interface",
            template="repository/repository_interface",
            context={
                "aggregate_name": aggregate,
                "namespace": interface_namespace,
                "custom_methods": custom_methods
            }
        ).to_dict())

    for impl in implementations:
        persistence = impl["persistence"]
        database = impl.get("database")

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

        if full_path in existing_paths:
            msg = f"⚠️ Repository implementation already exists at `{full_path}`. Skipping `{class_name}` creation."
            logger.info(msg)
            warnings.append(msg)
        else:
            plan.append(CreateFileStep(
                path=full_path,
                description=f"Create {class_name} implementation of {interface_name}",
                template=template,
                context={
                    "aggregate_name": aggregate,
                    "domain_namespace": domain_namespace,
                    "implementation_namespace": impl_namespace,
                    "custom_methods": custom_methods
                }
            ).to_dict())

    return plan, warnings
