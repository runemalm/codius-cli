import logging
import re
import json

from domain.model.config.config import Config
from domain.model.port.llm_port import LlmPort
from utils import print_highlighted

logger = logging.getLogger(__name__)


class LlmService:
    def __init__(self, llm_port: LlmPort, config: Config):
        self.llm = llm_port
        self.config = config

    def call_prompt(self, prompt: str) -> str:
        logger.debug("Calling LLM services with prompt...")
        if self.config.debug_llm:
            print_highlighted(prompt, title="📨 Prompt Sent to LLM")

        try:
            response = self.llm.call_prompt(prompt)
        except Exception as e:
            logger.error("Error while calling LLM: %s", e)
            raise RuntimeError(
                "❌ Failed to call LLM service. Please try again later.") from e

        if self.config.debug_llm:
            print_highlighted(response, title="🧠 LLM Response")

        return response

    def call_chat(self, messages: list[dict]) -> str:
        logger.debug("Calling LLM services with chat messages...")
        if self.config.debug_llm:
            for msg in messages:
                print_highlighted(msg["content"],
                                  title=f"📨 {msg['role'].title()} Message")

        response = self.llm.call_chat(messages)

        if self.config.debug_llm:
            print_highlighted(response, title="🧠 LLM Response")

        return response

    def try_extract_json(self, response: str) -> dict:
        """Try to parse a JSON object from a markdown-wrapped LLM response."""
        match = re.search(r"```(?:json)?\s*(.*?)```", response, re.DOTALL)
        json_text = match.group(1).strip() if match else response.strip()

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON from LLM response: %s", e)
            return {"error": "invalid_json", "raw": response}
