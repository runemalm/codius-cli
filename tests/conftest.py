import logging
import os
import sys

import pytest
from _pytest.fixtures import SubRequest
from pathlib import Path

from dependency_injection.container import DependencyContainer

from domain.model.config.config import Config
from domain.model.port.llm_port import LlmPort
from domain.service.config_service import ConfigService
from infrastructure.adapter.openai.openai_config import OpenAiConfig
from infrastructure.adapter.openai.openai_llm_adapter import OpenAiLlmAdapter
from infrastructure.service.llm_service import LlmService


@pytest.fixture(scope="session")
def project_path() -> Path:
    """
    Path to the test project (Bookstore). Override this fixture if needed.
    """
    return Path("~/Projects/OpenDDD.NET/samples/Bookstore/src/Bookstore").expanduser()


@pytest.fixture(autouse=True, scope="session")
def configure_test_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


@pytest.fixture(autouse=True, scope="function")
def container(request: SubRequest):
    if "integration" in request.keywords:
        # Setup
        container = DependencyContainer.get_instance()

        config = Config(
            openai=OpenAiConfig(
                model="gpt-4o",
                api_key="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"
            ),
            debug=True,
            debug_llm=True,
        )

        # Register all dependencies
        container.register_instance(Config, config)
        container.register_singleton(ConfigService,
             constructor_args={
                 "config": config
             }
        )
        container.register_transient(LlmService)
        container.register_transient(LlmPort, OpenAiLlmAdapter,
             constructor_args={"config": config.openai}
        )

        yield container

        DependencyContainer._instances = {}
    else:
        yield


@pytest.fixture(autouse=True)
def with_project_dir(request, project_path: Path):
    if "integration" not in request.keywords:
        yield
        return

    original_cwd = Path.cwd()
    os.chdir(project_path)
    try:
        yield
    finally:
        os.chdir(original_cwd)
