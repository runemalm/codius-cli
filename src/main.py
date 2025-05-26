from dependency_injection.container import DependencyContainer

from domain.service.config_service import ConfigService
from infrastructure.service.di_service import setup_di
from infrastructure.service.logging_service import LoggingService
from ui.shell import run_shell


def main():
    # Setup DI container
    setup_di()

    # Initialize configuration and logging
    container = DependencyContainer.get_instance()
    container.resolve(ConfigService).ensure_config_exists()
    container.resolve(LoggingService).configure()

    # Run shell
    run_shell()


if __name__ == "__main__":
    main()
