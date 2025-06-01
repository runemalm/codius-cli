from pathlib import Path
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text

from di import container
from domain.model.config.approval_mode import ApprovalMode
from domain.model.plan.plan_step_type import PlanStepType
from domain.services import session_service
from domain.services.config_service import ConfigService
from ui.approval_ui import show_approval_ui


def preview(state: dict) -> dict:
    session_id = session_service.get_active_session_id()
    generated_dir = Path(f".openddd/sessions/{session_id}/generated")
    console = Console()
    session = PromptSession()

    files_on_disk = list(generated_dir.rglob("*.cs"))
    deletions = [p for p in state.get("plan", []) if p["type"] == "delete_file"]

    if not files_on_disk and not deletions:
        console.print("[bold red]⚠️ No files generated.[/bold red]")
        state["approval"] = "abort"
        return state

    console.print("[bold underline]The assistant proposes the following changes:[/bold underline]\n")

    # Show added/updated files
    for path in files_on_disk:
        content = path.read_text()
        rel_path = path.relative_to(generated_dir)
        syntax = Syntax(content, "csharp", theme="monokai", line_numbers=True)
        panel = Panel(syntax, title=f"[green]{rel_path}[/green]", border_style="green")
        console.print(panel)

    # Show deletions
    for item in deletions:
        file_path = Path(item["path"])
        if file_path.exists():
            try:
                content = file_path.read_text()
                syntax = Syntax(content, "csharp", theme="monokai", line_numbers=True)
            except Exception:
                syntax = Text("(Unable to preview content)", style="dim")

            panel = Panel(
                syntax,
                title=f"[red]{file_path.relative_to(Path.cwd())}[/red]",
                border_style="red"
            )
            console.print(panel)
        else:
            console.print(Panel(
                Text("(File not found for preview)", style="dim"),
                title=f"[red]{file_path}[/red]",
                border_style="red"
            ))

    config = container.resolve(ConfigService).get_config()

    has_deletions = any(
        PlanStepType.is_destructive(item.get("type"))
        for item in state.get("plan", [])
    )

    if config.approval_mode == ApprovalMode.AUTO:
        if has_deletions:
            console.print(
                "[yellow]⚠️ Destructive change detected. Approval is required.[/yellow]")
        else:
            state["approval"] = "apply"
            return state

    # Manual approval path
    console.print("\nWould you like to apply these changes?")

    console.print("\nUse ↑/↓ to select an action, then press Enter:\n")
    response = show_approval_ui()

    if response in {"yes", "y", "apply"}:
        state["approval"] = "apply"
    elif response in {"no", "n", "abort"}:
        state["approval"] = "abort"
    elif response in {"change", "revise"}:
        console.print("Please describe what you'd like to change:")
        feedback = session.prompt("> ")
        state["approval"] = "revise"
        state["revision_feedback"] = feedback
    else:
        console.print("[red]Invalid choice. Please type yes, no, or change.[/red]")
        return preview(state)  # re-run prompt

    return state
