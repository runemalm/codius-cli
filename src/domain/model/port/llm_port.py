from abc import ABC, abstractmethod


class LlmPort(ABC):
    @abstractmethod
    def call(self, prompt: str) -> dict:
        """Send a prompt to the LLM and return structured response as dict."""
        pass
