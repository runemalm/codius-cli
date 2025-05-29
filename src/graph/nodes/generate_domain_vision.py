import logging

from di import container
from infrastructure.services.llm_service import LlmService

logger = logging.getLogger(__name__)


def generate_domain_vision(state: dict) -> dict:
    domain_model = state.get("domain_model", [])
    if not domain_model:
        state["domain_vision"] = "⚠️ No domain model found."
        return state

    llm_service = container.resolve(LlmService)

    # Build a summary string of building blocks
    summary = "\n".join(f"- {bb['type']}: {bb['name']}" for bb in domain_model)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a software architect specializing in domain-driven design (DDD) "
                "and responsible for analyzing codebases built with the OpenDDD.NET framework. "
                "OpenDDD.NET enforces clear separation of concerns between aggregates, actions, domain services, events, "
                "and infrastructure components. The goal is to enable maintainable, modular systems with clearly defined responsibilities."
            )
        },
        {
            "role": "user",
            "content": (
                "Below is a list of domain model building blocks, categorized by their type.\n\n"
                f"{summary}\n\n"
                "Based on this, write a short **vision statement** (2–3 sentences) that:\n"
                "- Identifies the **domain’s primary purpose** (e.g. e-commerce, medical records)\n"
                "- Describes the **main aggregate roots** and their roles\n"
                "- Highlights how the structure reflects DDD best practices\n"
                "- Avoids vague or overly general phrasing\n\n"
                "Use clear, directive language suitable for grounding AI-powered code generation."
            )
        }
    ]

    logger.debug("Calling LLM with domain model summary...")

    state["domain_vision"] = llm_service.call_chat(messages).strip()

    return state
