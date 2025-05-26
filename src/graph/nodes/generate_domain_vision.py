import logging

from dependency_injection.container import DependencyContainer

from infrastructure.service.llm_service import LlmService

logger = logging.getLogger(__name__)


def generate_domain_vision(state: dict) -> dict:
    domain_model = state.get("domain_model", [])
    if not domain_model:
        state["domain_vision"] = "⚠️ No domain model found."
        return state

    container = DependencyContainer.get_instance()
    llm_service = container.resolve(LlmService)

    # Build a summary string of building blocks
    summary = "\n".join(f"- {bb['type']}: {bb['name']}" for bb in domain_model)

    prompt = (
        "You are a software architect analyzing a domain-driven design codebase.\n"
        "Here is a list of domain model building blocks:\n\n"
        f"{summary}\n\n"
        "Write a short vision statement (2–3 sentences) that summarizes what this domain models, "
        "its main aggregates, and its overall purpose. Use natural language."
    )

    logger.debug("Calling LLM with domain model summary...")
    response = llm_service.call(prompt)

    state["domain_vision"] = response.get("text") or response.get("raw") or "⚠️ No vision returned."

    return state
