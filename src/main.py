import di
from di import container
from domain.services.config_service import ConfigService
from domain.services.session_service import create_and_activate_session, \
    get_or_create_active_session
from infrastructure.services.logging_service import LoggingService
from ui.shell import run_shell


def main():
    di.register_services()

    config_service = container.resolve(ConfigService)
    config_service.ensure_config_file_exists()
    config_service.load_config_from_file()

    logging_service = container.resolve(LoggingService)
    logging_service.configure()

    session = get_or_create_active_session()
    if session and session.should_be_replaced():
        session = create_and_activate_session()
        print(f"🆕 Started new session: {session.id}")

    run_shell()


if __name__ == "__main__":
    main()
