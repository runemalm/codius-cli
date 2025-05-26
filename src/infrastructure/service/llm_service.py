import logging

from domain.model.config.config import Config
from domain.model.port.llm_port import LlmPort
from utils import print_highlighted

logger = logging.getLogger(__name__)


class LlmService:
    def __init__(self, llm_port: LlmPort, config: Config):
        self.llm = llm_port
        self.config = config

    def call(self, prompt: str) -> dict:
        logger.debug("Calling LLM service via port...")
        if self.config.debug_llm:
            print_highlighted(prompt, title="📨 Prompt Sent to LLM")

        response = self.llm.call(prompt)

        if self.config.debug_llm:
            result_str = response if isinstance(response, str) else str(response)
            print_highlighted(result_str, title="🧠 LLM Response")

        return response
