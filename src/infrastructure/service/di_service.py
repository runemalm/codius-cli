from dependency_injection.container import DependencyContainer

from domain.model.config.config import Config
from domain.model.port.llm_port import LlmPort
from domain.service.config_service import ConfigService
from infrastructure.adapter.llm.openai.openai_llm_adapter import OpenAiLlmAdapter
from infrastructure.service.llm_service import LlmService
from infrastructure.service.logging_service import LoggingService
from infrastructure.service.project_scanner_service import ProjectScannerService


def setup_di():
    container = DependencyContainer.get_instance()

    # When py-dependency-injection supports optional arguments in constructors (Config),
    # we simply register config service and call ensure_file_exist from main instead..
    config_service = ConfigService()
    config_service.ensure_config_file_exists()
    config_service.load_config_from_file()
    container.register_instance(Config, config_service.get_config())
    container.register_instance(ConfigService, config_service)

    # Register rest of dependencies
    container.register_singleton(LoggingService)
    container.register_transient(ProjectScannerService)
    container.register_transient(LlmService)
    container.register_transient(LlmPort, OpenAiLlmAdapter,
        constructor_args={
            "config": container.resolve(ConfigService).get_config().llm.openai
        }
    )

    return container
