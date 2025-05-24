from rich.console import Console
from prompt_toolkit import PromptSession

console = Console()
prompt_session = PromptSession()

def ask_user(prompt: str, key: str = "approval") -> callable:
    """
    Returns a LangGraph node that will pause and ask the user for input,
    storing the response in state[key].
    """
    def tool(state: dict) -> dict:
        console.print()
        console.print("[bold yellow]Assistant wants your input:[/bold yellow]")
        console.print(prompt)
        console.print()

        response = prompt_session.prompt("[bold green]>[/bold green] ").strip()
        state[key] = response
        return state

    return tool
