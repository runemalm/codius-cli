from dataclasses import dataclass


@dataclass(frozen=True)
class DistillIntentPrompt:
    user_input: str
    domain_summary: str

    def as_prompt(self) -> str:
        return f"""
You are a modeling assistant for a DDD project.

Domain Summary:
{self.domain_summary}

User Message:
{self.user_input}

Extract the user intent as a structured JSON.
"""
