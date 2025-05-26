import logging
import re
import json
import openai

from domain.model.port.llm_port import LlmPort
from infrastructure.adapter.openai.openai_config import OpenAiConfig

logger = logging.getLogger(__name__)


class OpenAiLlmAdapter(LlmPort):
    def __init__(self, config: OpenAiConfig):
        self.model = config.model
        self.api_key = config.api_key
        if not self.api_key or not self.api_key.startswith("sk-"):
            logger.warning("Missing or invalid OpenAI API key")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def call(self, prompt: str) -> dict:
        if not self.client:
            return {
                "intent": None,
                "error": "Missing or invalid OpenAI API key in .openddd/config.yaml"
            }

        try:
            logger.debug("Using OpenAI model: %s", self.model)
            logger.debug("Prompt sent to LLM:\n%s", prompt)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )

            content = response.choices[0].message.content
            logger.debug("Raw LLM response:\n%s", content)

            # Extract JSON if wrapped in ```json ... ```
            match = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)
            json_text = match.group(1).strip() if match else content.strip()

            parsed = json.loads(json_text)
            logger.debug("Parsed LLM response:\n%s", parsed)

            return parsed

        except json.JSONDecodeError as e:
            logger.warning("Failed to decode JSON from response: %s", e)
            return {"intent": None, "raw": content}

        except Exception as e:
            logger.exception("Unexpected error during LLM call")
            return {"intent": None, "error": str(e)}
