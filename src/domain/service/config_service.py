from pathlib import Path
import yaml
from typing import Optional

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
        "debug": False,
        "debug_llm": False
    }

    def __init__(self, config: Optional[Config] = None):
        self._structured_config: Optional[Config] = config

    def ensure_config_file_exists(self) -> None:
        if not self.CONFIG_FILE.exists():
            print("🛠  Project configuration not found. Creating .openddd/config.yaml...")
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with self.CONFIG_FILE.open("w") as f:
                yaml.dump(self.DEFAULT_CONFIG, f)
            print(f"✅ Created {self.CONFIG_FILE}. Please update your config before using the CLI.\n")
        else:
            print(f"📦 Using project config: {self.CONFIG_FILE}")

    def load_config_from_file(self) -> None:
        with self.CONFIG_FILE.open("r") as f:
            raw = yaml.safe_load(f) or {}
        self._structured_config = self._parse_structured(raw)

    def _parse_structured(self, raw: dict) -> Config:
        openai_section = raw.get("openai", {})
        return Config(
            openai=OpenAiConfig(
                model=openai_section.get("model", "gpt-4o"),
                api_key=openai_section.get("api_key", "")
            ),
            debug=raw.get("debug", False),
            debug_llm=raw.get("debug_llm", False),
        )

    def get_config(self) -> Config:
        if self._structured_config is None:
            raise RuntimeError("Config has not been loaded. Call `load_config_from_file()` first.")
        return self._structured_config
