from enum import Enum
from pathlib import Path
import yaml
from typing import Any, Optional

from domain.model.config.anthropic.anthropic_llm_model import AnthropicModel
from domain.model.config.approval_mode import ApprovalMode
from domain.model.config.config import Config
from domain.model.config.llm_provider import LlmProvider
from domain.model.config.openai.openai_llm_model import OpenAiModel

from infrastructure.adapter.llm.anthropic.anthropic_config import AnthropicConfig
from infrastructure.adapter.llm.google.google_config import GoogleConfig
from infrastructure.adapter.llm.groq.groq_config import GroqConfig
from infrastructure.adapter.llm.llm_config import LlmConfig
from infrastructure.adapter.llm.mistral.mistral_config import MistralConfig
from infrastructure.adapter.llm.openai.openai_config import OpenAiConfig


class ConfigService:
    CONFIG_DIR = Path(".openddd")
    CONFIG_FILE = CONFIG_DIR / "config.yaml"

    DEFAULT_CONFIG = {
        "llm": {
            "provider": "openai",
            "openai": {
                "model": "gpt-4o",
                "api_key": "sk-... # Replace with your OpenAI API key"
            }
        },
        "approval_mode": ApprovalMode.SUGGEST.value,
        "debug": False,
        "debug_llm": False,
        "log_level": "warning"
    }

    def __init__(self, config: Optional[Config] = None):
        self._raw_config_dict: Optional[dict] = None
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
            self._raw_config_dict = yaml.safe_load(f) or {}
        self._structured_config = self._parse_structured(self._raw_config_dict)

    def _parse_structured(self, raw: dict) -> Config:
        llm_section = raw.get("llm", {})
        provider_str = llm_section.get("provider")
        try:
            provider = LlmProvider(provider_str)
        except ValueError:
            raise ValueError(f"Unsupported LLM provider: {provider_str}")

        llm_config = LlmConfig(provider=provider)

        openai = llm_section.get("openai", {})
        raw_model = openai.get("model") or "gpt-4o"
        llm_config.openai = OpenAiConfig(
            model=OpenAiModel(raw_model),
            api_key=openai.get("api_key", "")
        )

        anthropic = llm_section.get("anthropic", {})
        raw_model = anthropic.get("model") or "claude-3-opus"
        llm_config.anthropic = AnthropicConfig(
            model=AnthropicModel(raw_model),
            api_key=anthropic.get("api_key", "")
        )

        log_level = raw.get("log_level", "warning").lower()
        allowed_levels = {"debug", "info", "warning", "error", "critical"}
        if log_level not in allowed_levels:
            print(f"⚠️ Unknown log_level '{log_level}', falling back to 'warning'")
            log_level = "warning"

        approval_mode = ApprovalMode(raw.get("approval_mode", "suggest"))

        return Config(
            llm=llm_config,
            approval_mode=approval_mode,
            debug=raw.get("debug", False),
            debug_llm=raw.get("debug_llm", False),
            log_level=log_level,
        )

    def get_config(self) -> Config:
        if self._structured_config is None:
            raise RuntimeError("Config has not been loaded. Call `load_config_from_file()` first.")
        return self._structured_config

    def set_config_value(self, key: str, value: Any):
        if self._raw_config_dict is None:
            raise RuntimeError("Config has not been loaded yet.")

        keys = key.split(".")
        d = self._raw_config_dict
        for part in keys[:-1]:
            d = d.setdefault(part, {})
        d[keys[-1]] = value.value if isinstance(value, Enum) else value

        with open(self.CONFIG_FILE, "w") as f:
            yaml.dump(self._raw_config_dict, f, sort_keys=False)

        self._structured_config = self._parse_structured(self._raw_config_dict)
