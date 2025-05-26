import logging
import os
from domain.service.config_service import get_config_value


def configure_logging(debug: bool | None = None):
    if debug is None:
        debug = get_config_value("debug", False)

    level = logging.DEBUG if debug or os.getenv("DEBUG") == "1" else logging.INFO

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Suppress overly verbose logs from external libs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.INFO)
