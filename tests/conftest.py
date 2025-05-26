import logging
import sys

import pytest
from pathlib import Path


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
