from dependency_injection.container import DependencyContainer

from domain.model.port.llm_port import LlmPort
from domain.service.config_service import ConfigService
from infrastructure.adapter.openai.openai_llm_adapter import OpenAiLlmAdapter
from infrastructure.service.llm_service import LlmService
from infrastructure.service.logging_service import LoggingService


def setup_di():
    container = DependencyContainer.get_instance()

    # Register all dependencies
    container.register_singleton(ConfigService)
    container.register_singleton(LoggingService)
    container.register_transient(LlmService)
    container.register_transient(LlmPort, OpenAiLlmAdapter,
        constructor_args={
            "config": container.resolve(ConfigService).get_config().openai
        }
    )

    return container
