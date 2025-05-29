from di import container, register_services
from domain.services.config_service import ConfigService
from infrastructure.services.logging_service import LoggingService
from ui.shell import run_shell


def main():
    register_services()

    config_service = container.resolve(ConfigService)
    config_service.ensure_config_file_exists()
    config_service.load_config_from_file()

    logging_service = container.resolve(LoggingService)
    logging_service.configure()

    run_shell()


if __name__ == "__main__":
    main()
