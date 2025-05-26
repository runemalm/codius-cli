from dependency_injection.container import DependencyContainer

from domain.service.config_service import ConfigService
from infrastructure.service.di_service import setup_di
from infrastructure.service.logging_service import LoggingService
from ui.shell import run_shell


def main():
    setup_di()

    container = DependencyContainer.get_instance()

    config_service = container.resolve(ConfigService)
    config_service.ensure_config_file_exists()
    config_service.load_config_from_file()

    logging_service = container.resolve(LoggingService)
    logging_service.configure()

    run_shell()


if __name__ == "__main__":
    main()
