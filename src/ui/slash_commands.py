from rich.console import Console
from rich.panel import Panel

from di import container
from domain.services.session_service import (
    get_active_session,
    create_and_activate_session,
    save_session,
)
from infrastructure.services.code_scanner.code_scanner import CodeScannerService
from infrastructure.services.project_metadata_service import ProjectMetadataService
from infrastructure.services.project_scanner_service import ProjectScannerService

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
    "/diff": "Show git diff of working directory",
    "/building-blocks": "Show building blocks in the current codebase",
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

    elif command == "/new":
        session = create_and_activate_session()
        console.print(f"[green]✅ Created new session:[/green] {session.id}")
        save_session(session)

    elif command == "/building-blocks":
        project_metadata_service = container.resolve(ProjectMetadataService)
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

        console.print("[green]✅ Showing building blocks completed.[/green]")
