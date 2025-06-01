from getpass import getpass

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from di import container
from domain.model.config.anthropic.anthropic_llm_model import AnthropicModel
from domain.model.config.openai.openai_llm_model import OpenAiModel
from domain.services.config_service import ConfigService
from domain.services.session_service import (
    get_active_session,
    save_session, summarize_session,
)
from infrastructure.services.code_scanner.code_scanner_service import CodeScannerService
from infrastructure.services.project_scanner_service import ProjectScannerService
from ui.sessions_ui import show_sessions_panel
from utils import format_timestamp

MODEL_CHOICES = {
    "openai": list(OpenAiModel),
    "anthropic": list(AnthropicModel),
}

console = Console()

# Slash command definitions
SLASH_COMMANDS = {
    "/clear": "Clear conversation history and free up context",
    "/clearhistory": "Clear command history",
    "/compact": "Compact conversation history with optional summary",
    "/history": "Open session interaction history",
    "/sessions": "Browse previous sessions",
    "/help": "Show list of commands",
    "/model": "Open model selection panel",
    "/approval": "Open approval mode selection panel",
    "/diff": "Show git diff of working directory",
    "/visualize": "Visualize building blocks and driving adapter flows in the current codebase",
}


def handle_slash_command(command: str):
    session = get_active_session()

    config_service = container.resolve(ConfigService)
    config = config_service.get_config()

    if command == "/clear":
        session.clear()
        console.print("[green]✅ Session state and history cleared.[/green]")
        save_session(session)

    elif command == "/clearhistory":
        session.clear_history()
        console.print("[green]✅ History cleared but modeling context preserved.[/green]")
        save_session(session)

    elif command.startswith("/compact"):
        summarize_session(session)
        save_session(session)
        console.print("[bold green]✅ Session compacted.[/bold green]")
        if session.state.summary:
            console.print(f"\n[dim]Summary:[/dim]\n{session.state.summary}")

    elif command.startswith("/history"):
        history = session.history.messages

        if not history:
            console.print("[bold yellow]⚠️ No conversation history found.[/bold yellow]")
            return

        console.print(
            f"[bold underline green]Conversation History for session {session.id}[/bold underline green]\n")

        for message in history:
            role = message.role.lower()
            time_str = format_timestamp(message.timestamp)
            title = f"{role.capitalize()} — {time_str}"
            style = "magenta" if role == "user" else "cyan"
            content = Markdown(message.content)

            panel = Panel.fit(
                content,
                title=title,
                title_align="left",
                border_style=style,
                padding=(1, 2),
            )
            console.print(panel)

    elif command == "/sessions":
        show_sessions_panel()

    elif command == "/approval":
        current = config.approval_mode

        console.print(f"[bold]Current approval mode:[/bold] {current.value}")
        console.print("Choose how approvals should be handled:\n")
        console.print("  [1] suggest  – Ask before applying changes (default)")
        console.print("  [2] auto     – Automatically apply without asking\n")

        user_input = input("Enter choice [1-2]: ").strip()

        if user_input == "1":
            selected = "suggest"
        elif user_input == "2":
            selected = "auto"
        else:
            console.print("[yellow]No changes made.[/yellow]")
            return

        config_service.set_config_value("approval_mode", selected)
        console.print(
            f"[green]✅ Approval mode updated to:[/green] [bold]{selected}[/bold]")

    elif command == "/model":
        current_provider = config.llm.provider.value
        current_model = getattr(config.llm.openai, "model", None) \
            if current_provider == "openai" \
            else getattr(config.llm.anthropic, "model", None)

        console.print(f"[bold]Current LLM provider:[/bold] {current_provider}")
        console.print(f"[bold]Current model:[/bold] {current_model.value or '[not set]'}\n")

        # Build combined numbered choices
        all_combinations = []
        for provider, models in MODEL_CHOICES.items():
            for model in models:
                all_combinations.append((provider, model.value))

        # Show options
        console.print("Available LLM configurations:")
        for idx, (provider, model) in enumerate(all_combinations, 1):
            console.print(f"  [{idx}] {provider} → {model}")

        # Pick combination
        selection = input(f"\nSelect [1-{len(all_combinations)}]: ").strip()
        if not selection.isdigit() or not (1 <= int(selection) <= len(all_combinations)):
            console.print("[red]❌ Invalid selection. No changes made.[/red]")
            return

        provider, model = all_combinations[int(selection) - 1]

        # Prompt for API key if missing
        llm_section = getattr(config.llm, provider, None)
        if llm_section is None:
            raise ValueError(f"LLM config for provider '{provider}' not found.")

        current_key = llm_section.api_key

        if not current_key:
            key = getpass(
                f"Enter API key for {provider} (leave blank to skip): ").strip()
            if key:
                config_service.set_config_value(f"llm.{provider}.api_key", key)

        # Set provider and model
        config_service.set_config_value("llm.provider", provider)
        config_service.set_config_value(f"llm.{provider}.model", model)

        console.print(
            f"[green]✅ LLM updated to:[/green] [bold]{provider} → {model}[/bold]")

    elif command == "/help":
        commands = Table(show_header=False, box=None, padding=(0, 2))
        commands.add_row("[bold]/clear[/bold]", "clear screen & session context")
        commands.add_row("[bold]/clearhistory[/bold]", "clear only the session history")
        commands.add_row("[bold]/compact[/bold]", "condense history into a summary")
        commands.add_row("[bold]/history[/bold]", "show conversation history")
        commands.add_row("[bold]/sessions[/bold]", "browse previous sessions")
        commands.add_row("[bold]/help[/bold]", "show this help overlay")
        commands.add_row("[bold]/model[/bold]", "switch the LLM model in-session")
        commands.add_row("[bold]/approval[/bold]", "switch auto-approval mode")
        commands.add_row("[bold]/diff[/bold]", "view working tree git diff")
        commands.add_row("[bold]/visualize[/bold]", "show domain model overview (experimental)")

        shortcuts = Table(show_header=False, box=None, padding=(0, 2))
        shortcuts.add_row("[bold]Enter[/bold]", "send message")
        shortcuts.add_row("[bold]Ctrl+J[/bold]", "insert newline")
        shortcuts.add_row("[bold]Ctrl+C[/bold]", "quit assistant")

        console.print(Panel.fit(
            Group(
                "[bold underline]Available commands[/bold underline]\n",
                commands,
                "\n[bold underline]Keyboard shortcuts[/bold underline]\n",
                shortcuts
            ),
            title="🤖 DDD Coding Assistant Help",
            border_style="blue"
        ))

    elif command == "/visualize":
        handle_slash_command("/building-blocks")
        handle_slash_command("/flows")

    elif command == "/building-blocks":
        project_scanner_service = container.resolve(ProjectScannerService)
        code_scanner_service = container.resolve(CodeScannerService)

        # Extract metadata and building blocks
        project_metadata = project_scanner_service.extract_project_metadata()
        building_blocks = code_scanner_service.scan_building_blocks(project_metadata)

        # Group building blocks
        grouped = {}
        for bb in building_blocks:
            grouped.setdefault(bb.type, []).append(bb)

        # Render project metadata
        console.print(Panel.fit(
            f"[bold]Project Name:[/bold] {project_metadata['project_name']}\n"
            f"[bold]Root Namespace:[/bold] {project_metadata['root_namespace']}\n"
            f"[bold]Source Path:[/bold] {project_metadata['source_path']}",
            title="[green]Project Metadata[/green]",
            border_style="green",
            padding=(1, 2),
        ))

        # Render building blocks
        for bb_type, bbs in grouped.items():
            bb_list = "\n".join([f"- [cyan]{bb.name}[/cyan] ({bb.namespace})" for bb in bbs])
            console.print(Panel.fit(
                bb_list or "[dim]No items found.[/dim]",
                title=f"[bold magenta]{bb_type.value}s[/bold magenta]",
                border_style="magenta"
            ))

    elif command == "/flows":
        project_scanner_service = container.resolve(ProjectScannerService)
        code_scanner = CodeScannerService()

        # Step 1: Extract metadata and building blocks
        project_metadata = project_scanner_service.extract_project_metadata()
        building_blocks = code_scanner.scan_building_blocks(project_metadata)

        # Step 2: Scan flows using FlowScanner
        flows = code_scanner.scan_flows(building_blocks)

        if not flows:
            console.print("[dim]No flows found.[/dim]")
            return

        # Step 3: Render flows horizontally
        flow_lines = [flow.as_string() for flow in flows]
        console.print(
            Panel.fit("\n".join(flow_lines), title="Driving Adapter Flows", border_style="cyan")
        )


def _find_related_block(name: str, blocks, type_name: str):
    # Try exact match or similar suffix match (e.g., RegisterPersonCommand → RegisterPersonAction)
    for bb in blocks:
        if bb.type.name == type_name and name.replace("Command", "") in bb.name:
            return bb
    return None

def _find_called_block(action, blocks, valid_types):
    # Naive heuristic: match any method name to known domain logic class names
    for bb in blocks:
        if bb.type.name in valid_types:
            for method in action.methods:
                if method.lower().startswith(bb.name.lower()):
                    return bb
    return None
