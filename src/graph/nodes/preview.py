from prompt_toolkit import PromptSession
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel


def preview(state: dict) -> dict:
    files = state.get("generated_files", [])
    console = Console()
    session = PromptSession()

    if not files:
        console.print("[bold red]⚠️ No files generated.[/bold red]")
        state["approval"] = "abort"
        return state

    console.print("[bold underline]The assistant proposes the following changes:[/bold underline]\n")

    for f in files:
        syntax = Syntax(f["content"], "csharp", theme="monokai", line_numbers=True)
        panel = Panel(syntax, title=f["path"], border_style="cyan")
        console.print(panel)

    console.print("\nWould you like to apply these changes?")
    console.print("Type [bold green]yes[/bold green] to apply or [bold red]no[/bold red] to abort:")

    state["approval"] = session.prompt("> ").strip().lower()
    return state
