#!/usr/bin/env python3
"""Utility functions for formatting, logging, and helpers."""

import sys
from typing import List
from rich.console import Console
from rich.text import Text
from rich.panel import Panel


console = Console()


def format_command_list(commands: List[str], max_display: int = 10,
                       selected_idx: int = -1, query: str = "") -> str:
    """
    Format list of commands for display.

    Args:
        commands: List of command strings.
        max_display: Maximum number of commands to display.
        selected_idx: Index of currently selected command (-1 for none).
        query: Search query to highlight in results.

    Returns:
        Formatted string for display.
    """
    if not commands:
        return "No commands found."

    lines = []
    display_count = min(len(commands), max_display)

    for i in range(display_count):
        cmd = commands[i]
        prefix = "▶ " if i == selected_idx else "  "

        # Highlight query matches
        if query:
            highlighted = highlight_query(cmd, query)
            lines.append(f"{prefix}{highlighted}")
        else:
            lines.append(f"{prefix}{cmd}")

    if len(commands) > max_display:
        lines.append(f"  ... and {len(commands) - max_display} more")

    return "\n".join(lines)


def highlight_query(text: str, query: str) -> str:
    """
    Highlight query characters in text.

    Args:
        text: Text to highlight in.
        query: Query string to highlight.

    Returns:
        Text with highlighted query matches.
    """
    # Simple implementation - just return the text for now
    # TODO: Implement proper highlighting with rich markup
    return text


def truncate_command(command: str, max_length: int = 80) -> str:
    """
    Truncate long commands for display.

    Args:
        command: Command string.
        max_length: Maximum length before truncation.

    Returns:
        Truncated command string.
    """
    if len(command) <= max_length:
        return command
    return command[:max_length - 3] + "..."


def print_error(message: str):
    """
    Print error message to console.

    Args:
        message: Error message to display.
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_info(message: str):
    """
    Print info message to console.

    Args:
        message: Info message to display.
    """
    console.print(f"[blue]ℹ[/blue] {message}")


def print_success(message: str):
    """
    Print success message to console.

    Args:
        message: Success message to display.
    """
    console.print(f"[green]✓[/green] {message}")


def clear_lines(n: int):
    """
    Clear n lines from terminal.

    Args:
        n: Number of lines to clear.
    """
    # Move cursor up n lines and clear each
    for _ in range(n):
        sys.stdout.write('\033[F')  # Move cursor up one line
        sys.stdout.write('\033[K')  # Clear line
    sys.stdout.flush()


def get_terminal_height() -> int:
    """
    Get terminal height in lines.

    Returns:
        Number of lines in terminal.
    """
    try:
        import shutil
        return shutil.get_terminal_size().lines
    except:
        return 24  # Default fallback


def get_terminal_width() -> int:
    """
    Get terminal width in columns.

    Returns:
        Number of columns in terminal.
    """
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except:
        return 80  # Default fallback
