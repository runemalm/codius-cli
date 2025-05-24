from pathlib import Path
import yaml

CONFIG_DIR = Path(".openddd")
CONFIG_FILE = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG = {
    "openai_api_key": "sk-... # Replace with your OpenAI API key"
}

def ensure_project_config_exists() -> None:
    if not CONFIG_FILE.exists():
        print("🛠  Project configuration not found. Creating .openddd/config.yaml...")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE.open("w") as f:
            yaml.dump(DEFAULT_CONFIG, f)
        print(f"✅ Created {CONFIG_FILE}. Please update your OpenAI API key before using the CLI.\n")
    else:
        print(f"📦 Using project config: {CONFIG_FILE}")

def load_config() -> dict:
    ensure_project_config_exists()
    with CONFIG_FILE.open("r") as f:
        return yaml.safe_load(f)

def get_config_value(key: str, default=None):
    config = load_config()
    return config.get(key, default)
