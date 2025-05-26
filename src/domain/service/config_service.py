from pathlib import Path
import yaml

from domain.model.config.config import Config
from infrastructure.adapter.openai.openai_config import OpenAiConfig


class ConfigService:
    CONFIG_DIR = Path(".openddd")
    CONFIG_FILE = CONFIG_DIR / "config.yaml"

    DEFAULT_CONFIG = {
        "openai": {
            "model": "gpt-4o",
            "api_key": "sk-... # Replace with your OpenAI API key"
        },
        "debug": False
    }

    def __init__(self):
        self._raw_config = None
        self._structured_config = None

    def ensure_config_exists(self) -> None:
        if not self.CONFIG_FILE.exists():
            print("🛠  Project configuration not found. Creating .openddd/config.yaml...")
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with self.CONFIG_FILE.open("w") as f:
                yaml.dump(self.DEFAULT_CONFIG, f)
            print(f"✅ Created {self.CONFIG_FILE}. Please update your config before using the CLI.\n")
        else:
            print(f"📦 Using project config: {self.CONFIG_FILE}")

    def _load_config(self) -> dict:
        self.ensure_config_exists()
        with self.CONFIG_FILE.open("r") as f:
            return yaml.safe_load(f) or {}

    def _load_structured_config(self) -> Config:
        openai_section = self._raw_config.get("openai", {})
        return Config(
            openai=OpenAiConfig(
                model=openai_section.get("model", "gpt-4o"),
                api_key=openai_section.get("api_key", "")
            ),
            debug=self._raw_config.get("debug", False)
        )

    def _ensure_loaded(self):
        if self._raw_config is None:
            self._raw_config = self._load_config()
            self._structured_config = self._load_structured_config()

    def get(self, key: str, default=None):
        self._ensure_loaded()
        return self._raw_config.get(key, default)

    def get_config(self) -> Config:
        self._ensure_loaded()
        return self._structured_config
