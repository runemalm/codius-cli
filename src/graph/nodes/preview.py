from prompt_toolkit import PromptSession
from rich.console import Console


def preview(state: dict) -> dict:

    files = state.get("generated_files", [])
    file_list = "\n".join([f"• {f['path']}" for f in files])
    message = f"""
The assistant proposes the following changes:

{file_list}

Would you like to apply these changes?

Type [bold green]yes[/bold green] to apply or [bold red]no[/bold red] to abort:
"""
    console = Console()
    session = PromptSession()
    console.print(message)
    state["approval"] = session.prompt("> ").strip().lower()
    return state
