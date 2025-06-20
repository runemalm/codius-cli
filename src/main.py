import argparse
import di

from tree_sitter import Language, Parser

from pathlib import Path
from di import container
from domain.services.session_service import SessionService
from infrastructure.services.logging_service import LoggingService
from infrastructure.services.project_initializer_service import ProjectInitializerService
from infrastructure.services.tree_sitter_service import TreeSitterService
from ui.shell import run_shell


def main():
    parser = argparse.ArgumentParser(prog="openddd")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="(Optional) Path to the target OpenDDD.NET project directory"
    )
    args = parser.parse_args()

    # Load config
    project_initializer = ProjectInitializerService(project_path=args.path)
    project_initializer.ensure_config_file_exists()
    config = project_initializer.load_config()

    # Register dependencies with container
    di.register_services(config=config, args=args)

    # Initialize logging
    logging_service = container.resolve(LoggingService)
    logging_service.configure()

    # Start new session, if current is old or don't exist
    session_service = container.resolve(SessionService)
    session = session_service.get_or_create_active_session()
    if session and session.should_be_replaced():
        session = session_service.create_and_activate_session()
        print(f"🆕 Started new session: {session.id}")

    # Run the assistant
    run_shell()


if __name__ == "__main__":
    main()
