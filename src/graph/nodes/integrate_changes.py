import logging
import re

logger = logging.getLogger(__name__)


def integrate_changes(state: dict) -> dict:
    logger.debug("Running integrate_changes...")

    intents = state.get("intent", [])

    # Group intents by type for easier access
    aggregates_by_target = {
        i["target"]: i for i in intents if i.get("intent") == "add_aggregate"
    }
    repositories_by_target = {
        i["target"]: i for i in intents if i.get("intent") == "add_repository"
    }

    for target, repo_intent in repositories_by_target.items():
        aggregate_intent = aggregates_by_target.get(target)
        if not aggregate_intent:
            continue  # No matching aggregate to enrich

        _inject_missing_properties_from_queries(
            aggregate_intent, repo_intent
        )

    return state


def _inject_missing_properties_from_queries(aggregate_intent: dict, repository_intent: dict):
    """Infer and inject missing aggregate properties based on repository query method names."""
    details = aggregate_intent.setdefault("details", {})
    existing_props = {p["name"] for p in details.get("properties", [])}

    new_props = []

    for method in repository_intent.get("details", {}).get("custom_methods", []):
        name = method.get("name", "")
        parameters = method.get("parameters", [])

        if not name.endswith("Async"):
            continue

        name_base = name[:-5]

        if name_base.startswith("GetBy") or name_base.startswith("FindBy") or name_base.startswith("FindWith"):
            suffix = name_base.replace("GetBy", "").replace("FindBy", "").replace("FindWith", "")
            if suffix:
                prop_name = _to_pascal_case(suffix)

                if prop_name not in existing_props:
                    param_match = _find_parameter_by_pascal_case(parameters, prop_name)
                    prop_type = param_match["type"] if param_match else "string"

                    logger.debug(
                        "Inferred missing property '%s' of type '%s' from method '%s'",
                        prop_name, prop_type, name
                    )

                    new_props.append({
                        "name": prop_name,
                        "type": prop_type
                    })

    if new_props:
        details.setdefault("properties", []).extend(new_props)
        logger.info(
            "Added %d inferred property(ies) to aggregate '%s': %s",
            len(new_props),
            aggregate_intent["target"],
            [p["name"] for p in new_props]
        )


def _find_parameter_by_pascal_case(parameters, pascal_name: str):
    """Matches parameters by converting their names to PascalCase for comparison."""
    for param in parameters:
        if _to_pascal_case(param.get("name", "")) == pascal_name:
            return param
    return None


def _to_pascal_case(name: str) -> str:
    """Converts a suffix like 'nickname' or 'favouriteColor' to PascalCase ('Nickname', 'FavouriteColor')"""
    if not name:
        return name

    # Split on word boundaries if camelCase or snake_case
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', name)
    return ''.join(word.capitalize() for word in words)
