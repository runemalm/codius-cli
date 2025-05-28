from pathlib import Path

from prompt_toolkit import PromptSession
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

from domain.services import session_service


def preview(state: dict) -> dict:
    session_id = session_service.get_active_session_id()
    generated_dir = Path(f".openddd/sessions/{session_id}/generated")
    console = Console()
    session = PromptSession()

    files_on_disk = list(generated_dir.rglob("*.cs"))

    if not files_on_disk:
        console.print("[bold red]⚠️ No files generated.[/bold red]")
        state["approval"] = "abort"
        return state

    console.print("[bold underline]The assistant proposes the following changes:[/bold underline]\n")

    for path in files_on_disk:
        content = path.read_text()
        rel_path = path.relative_to(generated_dir)
        syntax = Syntax(content, "csharp", theme="monokai", line_numbers=True)
        panel = Panel(syntax, title=str(rel_path), border_style="cyan")
        console.print(panel)

    console.print("\nWould you like to apply these changes?")
    console.print("Type [bold green]yes[/bold green] to apply or [bold red]no[/bold red] to abort:")

    state["approval"] = session.prompt("> ").strip().lower()
    return state
