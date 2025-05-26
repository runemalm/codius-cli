from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from domain.service.config_service import ConfigService
from domain.service.session_service import create_and_activate_session, \
    get_active_session, \
    get_or_create_active_session, save_session
from infrastructure.service.graph_service import run_graph

from dependency_injection.container import DependencyContainer


console = Console()

# Slash command definitions
SLASH_COMMANDS = {
    "/clear": "Clear conversation history and free up context",
    "/clearhistory": "Clear command history",
    "/compact": "Compact conversation history with optional summary",
    "/history": "Open command history",
    "/sessions": "Browse previous sessions",
    "/new": "Start a new modeling session",
    "/help": "Show list of commands",
    "/model": "Open model selection panel",
    "/approval": "Open approval mode selection panel",
    "/bug": "Generate GitHub issue URL with session log",
    "/diff": "Show git diff of working directory"
}

slash_completer = WordCompleter(SLASH_COMMANDS.keys(), sentence=True)


def get_project_root() -> str:
    return str(Path(".").resolve())


def render_header():
    console.print(
        Panel.fit(
            "● [bold cyan]OpenDDD CLI Assistant[/bold cyan] [dim](MVP)[/dim]",
            padding=(0, 2),
            border_style="cyan",
        )
    )


def render_session_info():
    container = DependencyContainer.get_instance()
    config_service = container.resolve(ConfigService)

    session = get_or_create_active_session()
    workdir = get_project_root()
    model = config_service.get_config().openai.model
    log_level = config_service.get_config().log_level

    console.print(Panel.fit(
        f"[bold]Session:[/bold] {session.id}\n"
        f"[bold]Workdir:[/bold] {workdir}\n"
        f"[bold]Model:[/bold] {model}\n"
        f"[bold]Log level:[/bold] {log_level}",
        border_style="green",
    ))


def render_assistant_message(message: str):
    console.print(Panel.fit(
        message,
        title="[cyan]Assistant",
        border_style="cyan",
        padding=(1, 2),
    ))


def dispatch_command(command):
    session = get_active_session()

    if command == "/clear":
        session.clear()
        console.print("[green]✅ Session state and history cleared.[/green]")
        save_session(session)

    elif command == "/clearhistory":
        session.clear_history()
        console.print("[green]✅ History cleared but modeling context preserved.[/green]")
        save_session(session)

    elif command.startswith("/compact"):
        session.compact_history()
        console.print("[green]✅ History compacted with summary retained in context.[/green]")
        save_session(session)

    elif command == "/new":
        session = create_and_activate_session()
        console.print(f"[green]✅ Created new session:[/green] {session.id}")
        save_session(session)


def run_shell():
    console.clear()
    render_header()
    render_session_info()
    console.print(Panel.fit("[dim]Type your modeling request or use slash-commands like /diff[/dim]"))

    prompt_session = PromptSession(completer=slash_completer)

    while True:
        try:
            user_input = prompt_session.prompt("\n> ")

            if user_input.strip().lower() in {"exit", "quit"}:
                console.print("[dim]Goodbye![/dim] 👋")
                break

            # Get active session
            session = get_active_session()

            # Handle slash-commands
            if user_input.startswith("/"):
                command = user_input.strip().split()[0]
                if command in SLASH_COMMANDS:
                    console.print(f"[bold yellow]Running command:[/bold yellow] {command}")
                    dispatch_command(command)
                    render_session_info()
                else:
                    console.print(f"[red]Unknown command:[/red] {command}")
                continue

            # Run assistant, get assistant_message
            assistant_message = run_graph(session, user_input)

            # Save session
            save_session(session)

            # Render final message
            render_assistant_message(assistant_message)

        except KeyboardInterrupt:
            console.print("\n[dim]Exited with Ctrl+C[/dim]")
            break
