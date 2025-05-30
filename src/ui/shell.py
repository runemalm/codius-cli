from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from di import container
from domain.services.config_service import ConfigService
from domain.services.session_service import get_active_session, \
    get_or_create_active_session, save_session
from infrastructure.services.graph_service import run_graph

from infrastructure.services.project_metadata_service import ProjectMetadataService
from ui.slash_commands import SLASH_COMMANDS, handle_slash_command

console = Console()

slash_completer = WordCompleter(SLASH_COMMANDS.keys(), sentence=True)


def get_project_root() -> str:
    return str(Path(".").resolve())


def render_header():
    console.print(
        Panel.fit(
            "● [bold cyan]bygga[/bold cyan] [dim](alpha)[/dim]",
            padding=(0, 2),
            border_style="cyan",
        )
    )


def render_session_info():
    config_service = container.resolve(ConfigService)

    session = get_or_create_active_session()
    workdir = get_project_root()

    config = config_service.get_config()
    provider = config.llm.provider.value
    model = getattr(config.llm, provider).model.value
    approval_mode = config_service.get_config().approval_mode
    log_level = config_service.get_config().log_level

    console.print(Panel.fit(
        f"[bold]Session:[/bold] {session.id}\n"
        f"[bold]Workdir:[/bold] {workdir}\n"
        f"[bold]Provider:[/bold] {provider}\n"
        f"[bold]Model:[/bold] {model}\n"
        f"[bold]Log level:[/bold] {log_level}\n"
        f"[bold]Approval:[/bold] {approval_mode.value}",
        border_style="green",
    ))


def render_assistant_message(message: str):
    console.print(Panel.fit(
        message,
        title="[cyan]Assistant",
        border_style="cyan",
        padding=(1, 2),
    ))


def run_shell():
    console.clear()
    render_header()
    render_session_info()
    console.print(Panel.fit("[dim]Type your modeling request or use slash-commands like /diff[/dim]"))

    prompt_session = PromptSession(completer=slash_completer)

    console.print()
    while True:
        try:
            user_input = prompt_session.prompt("> ")

            if user_input.strip().lower() in {"exit", "quit"}:
                console.print("[dim]Goodbye![/dim] 👋")
                break

            if not user_input.strip():
                continue

            # Get active session
            session = get_active_session()

            # Handle slash-commands
            if user_input.startswith("/"):
                command = user_input.strip().split()[0]
                if command in SLASH_COMMANDS:
                    console.print(
                        f"[bold yellow]Running command:[/bold yellow] {command}")
                    handle_slash_command(command)
                    render_session_info()
                else:
                    console.print(f"[red]Unknown command:[/red] {command}")
                continue

            # Get DI container
            project_metadata_service = container.resolve(ProjectMetadataService)

            # Clear memory state
            session.clear_state()

            # Clear on-disk files
            project_metadata_service.clear_generated_files()

            # Run assistant
            assistant_message = run_graph(session, user_input)

            # Save session
            save_session(session)

            # Render final message
            render_assistant_message(assistant_message)

        except KeyboardInterrupt:
            console.print("\n[dim]Exited with Ctrl+C[/dim]")
            break
