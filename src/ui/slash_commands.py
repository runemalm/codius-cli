from prompt_toolkit.shortcuts import radiolist_dialog
from rich.console import Console
from rich.panel import Panel

from di import container
from domain.model.config.approval_mode import ApprovalMode
from domain.services.config_service import ConfigService
from domain.services.session_service import (
    get_active_session,
    create_and_activate_session,
    save_session,
)
from infrastructure.services.code_scanner.code_scanner_service import CodeScannerService
from infrastructure.services.project_scanner_service import ProjectScannerService

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

    elif command == "/approval":
        config_service = container.resolve(ConfigService)
        config = config_service.get_config()
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
