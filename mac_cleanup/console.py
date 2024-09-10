"""Configuration of Rich console."""

from typing import Optional

from rich.console import Console
from rich.theme import Theme

console = Console(
    theme=Theme({"info": "cyan", "warning": "magenta", "danger": "bold red", "success": "bold green"}), record=True
)


def print_panel(text: str, title: Optional[str] = None) -> None:
    """
    Prints a rich panel with the given text.

    Args:
        text: Text to print in the panel
        title: Title of the panel
    """
    from rich.panel import Panel
    from rich.text import Text

    console.print(Panel(Text.from_markup(text, justify="center"), subtitle=title, subtitle_align="right"))
