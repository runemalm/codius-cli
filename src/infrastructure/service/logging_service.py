import logging
import os

from domain.service.config_service import ConfigService


class LoggingService:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def configure(self, debug: bool | None = None):
        if debug is None:
            debug = self.config_service.get_config().debug or os.getenv("DEBUG") == "1"

        level = logging.DEBUG if debug else logging.INFO

        logging.basicConfig(
            level=level,
            format="[%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )

        self._suppress_external_noise()

    def _suppress_external_noise(self):
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.INFO)
