import argparse
import logging
import os
import sys
import uuid

import pytest
from _pytest.fixtures import SubRequest
from pathlib import Path

from dependency_injection.container import DependencyContainer
from dotenv import load_dotenv

from codius.di import container, register_services
from codius.domain.model.config.approval_mode import ApprovalMode
from codius.domain.model.config.config import Config
from codius.domain.model.config.llm_provider import LlmProvider
from codius.infrastructure.adapter.llm.llm_config import LlmConfig
from codius.infrastructure.adapter.llm.openai.openai_config import OpenAiConfig

project_root = Path(__file__).parent.parent.resolve()
load_dotenv(dotenv_path=project_root / ".env")


@pytest.fixture(scope="session")
def bookstore_project_path() -> Path:
    """
    Path to the test project (Bookstore). Override this fixture if needed.
    """
    return Path("~/Projects/OpenDDD.NET/samples/Bookstore").expanduser()


@pytest.fixture(autouse=True, scope="session")
def configure_test_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


@pytest.fixture(autouse=True, scope="function")
def container_(request: SubRequest, bookstore_project_path: Path):
    if "integration" in request.keywords:
        test_container_name = f"test_{uuid.uuid4()}"
        DependencyContainer.configure_default_container_name(test_container_name)

        # Construct Config
        config = Config(
            llm=LlmConfig(
                provider=LlmProvider.OPENAI,
                openai=OpenAiConfig(
                    model="gpt-4o",
                    api_key=None  # Will use OPENAI_API_KEY from .env file..
                )
            ),
            approval_mode=ApprovalMode.SUGGEST,
            debug=True,
            debug_llm=True,
            log_level="debug"
        )

        # Mock args namespace
        args = argparse.Namespace(path=bookstore_project_path)

        # Register all dependencies using real register_services method
        register_services(config=config, args=args)

        yield container

        # Reset for isolation
        DependencyContainer.clear_instances()
    else:
        yield


@pytest.fixture(autouse=True)
def with_project_dir(request, bookstore_project_path: Path):
    if "integration" not in request.keywords:
        yield
        return

    original_cwd = Path.cwd()
    os.chdir(bookstore_project_path)
    try:
        yield
    finally:
        os.chdir(original_cwd)
