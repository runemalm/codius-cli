from dataclasses import dataclass

from domain.model.config.approval_mode import ApprovalMode
from infrastructure.adapter.llm.llm_config import LlmConfig


@dataclass
class Config:
    llm: LlmConfig
    approval_mode: ApprovalMode = ApprovalMode.SUGGEST
    debug: bool = False
    debug_llm: bool = False
    log_level: str = "info"
