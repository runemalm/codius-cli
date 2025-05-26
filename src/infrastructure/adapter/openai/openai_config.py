from dataclasses import dataclass


@dataclass
class OpenAiConfig:
    model: str = "gpt-4o"
    api_key: str = ""
