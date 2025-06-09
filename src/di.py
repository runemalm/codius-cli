import argparse

from dependency_injection.container import DependencyContainer

from domain.model.config.config import Config
from domain.model.port.llm_port import LlmPort
from domain.services.config_service import ConfigService
from domain.services.session_service import SessionService

from infrastructure.adapter.llm.openai.openai_llm_adapter import OpenAiLlmAdapter
from infrastructure.repository.session_repository import SessionRepository
from infrastructure.services.code_scanner.code_scanner_service import CodeScannerService
from infrastructure.services.llm_service import LlmService
from infrastructure.services.logging_service import LoggingService
from infrastructure.services.project_metadata_service import ProjectMetadataService
from infrastructure.services.project_scanner_service import ProjectScannerService


container = DependencyContainer.get_instance()


def register_services(config: Config, args: argparse.Namespace):

    container.register_instance(Config, config)
    container.register_transient(
        ProjectMetadataService,
        constructor_args={"workdir": args.path}
    )
    container.register_scoped(ConfigService)
    container.register_scoped(SessionRepository)
    container.register_singleton(LoggingService)
    container.register_scoped(SessionService)
    container.register_scoped(ProjectScannerService)
    container.register_scoped(CodeScannerService)
    container.register_scoped(LlmService)
    container.register_scoped(LlmPort, OpenAiLlmAdapter)
