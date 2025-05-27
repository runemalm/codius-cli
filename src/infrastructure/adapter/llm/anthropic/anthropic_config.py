from dataclasses import dataclass


@dataclass
class AnthropicConfig:
    model: str
    api_key: str
