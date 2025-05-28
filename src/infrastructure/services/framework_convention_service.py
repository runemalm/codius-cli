from pathlib import Path


def get_source_root() -> str:
    return "src/"

def get_tests_path() -> str:
    return "src/Tests"

def get_interchange_path() -> str:
    return "src/Interchange"

def get_layer_path(layer: str) -> str:
    return f"src/{layer}"

def get_namespace_base(project_dir: Path) -> str:
    # Fallback if LLM fails: use folder name
    return project_dir.resolve().name

def get_aggregate_structure() -> str:
    return "Domain/{AggregateName}/{AggregateName}.cs"

def get_aggregate_path(name: str) -> str:
    return f"src/Domain/{name}/{name}.cs"

def get_namespace_for(layer: str, name: str, base: str) -> str:
    return f"{base}.{layer}.{name}"
