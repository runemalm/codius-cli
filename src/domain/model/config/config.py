from dataclasses import dataclass
from infrastructure.adapter.openai.openai_config import OpenAiConfig


@dataclass
class Config:
    openai: OpenAiConfig
    debug: bool = False
