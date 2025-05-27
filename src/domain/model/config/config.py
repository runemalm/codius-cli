from dataclasses import dataclass
from infrastructure.adapter.llm.llm_config import LlmConfig


@dataclass
class Config:
    llm: LlmConfig
    debug: bool = False
    debug_llm: bool = False
    log_level: str = "info"
