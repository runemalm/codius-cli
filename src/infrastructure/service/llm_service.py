import logging

from domain.model.port.llm_port import LlmPort

logger = logging.getLogger(__name__)


class LlmService:
    def __init__(self, llm_port: LlmPort):
        self.llm = llm_port

    def call(self, prompt: str) -> dict:
        logger.debug("Calling LLM service via port...")
        return self.llm.call(prompt)
