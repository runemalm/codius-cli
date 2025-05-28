import logging
import os

from domain.services.config_service import ConfigService


class LoggingService:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def configure(self, level_override: str | None = None):
        config = self.config_service.get_config()

        # Priority: explicit arg > config file > DEBUG env
        level_str = (
            level_override
            or config.log_level
            or ("debug" if config.debug or os.getenv("DEBUG") == "1" else "info")
        ).lower()

        level = self._parse_log_level(level_str)

        logging.basicConfig(
            level=level,
            format="[%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )

        self._suppress_external_noise()

    def _parse_log_level(self, level: str) -> int:
        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        return levels.get(level.lower(), logging.INFO)

    def _suppress_external_noise(self):
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
