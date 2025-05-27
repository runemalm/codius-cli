from dataclasses import dataclass
from typing import Optional

from domain.model.config.llm_provider import LlmProvider
from infrastructure.adapter.llm.anthropic.anthropic_config import AnthropicConfig
from infrastructure.adapter.llm.google.google_config import GoogleConfig
from infrastructure.adapter.llm.groq.groq_config import GroqConfig
from infrastructure.adapter.llm.mistral.mistral_config import MistralConfig
from infrastructure.adapter.llm.openai.openai_config import OpenAiConfig


@dataclass
class LlmConfig:
    provider: LlmProvider
    openai: Optional[OpenAiConfig] = None
    anthropic: Optional[AnthropicConfig] = None
    google: Optional[GoogleConfig] = None
    mistral: Optional[MistralConfig] = None
    groq: Optional[GroqConfig] = None
