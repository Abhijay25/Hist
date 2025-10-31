#!/usr/bin/env python3
"""
Hist - Command history fuzzy search tool.

A CLI tool for searching and executing commands from shell history.
"""

import sys
import tty
import termios
from typing import List, Optional
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

from history_loader import HistoryLoader
from runner import CommandRunner
from utils import print_error, print_success, print_info


class HistUI:
    """Interactive terminal UI for history search."""

    def __init__(self):
        """Initialize the UI."""
        self.console = Console()
        self.loader = HistoryLoader()
        self.runner = CommandRunner()
        self.query = ""
        self.selected_idx = 0
        self.max_display = 15
        self.history: List[str] = []
        self.filtered_history: List[str] = []

    def run(self):
        """Run the interactive history search UI."""
        # Load history
        print_info("Loading command history...")
        self.history = self.loader.load_history()

        if not self.history:
            print_error("No command history found.")
            sys.exit(1)

        print_success(f"Loaded {len(self.history)} commands from history.")
        self.console.print("\n[bold]Controls:[/bold] Type to search, ↑/↓ to select, Enter to execute, Ctrl+C to exit\n")

        self.filtered_history = self.history[:self.max_display]

        try:
            self._interactive_loop()
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Exited.[/yellow]")
            sys.exit(0)

    def _interactive_loop(self):
        """Main interactive input loop."""
        # Save terminal settings
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            # Set terminal to raw mode for character-by-character input
            tty.setraw(fd)

            while True:
                # Display current state
                self._render_ui()

                # Read single character
                char = sys.stdin.read(1)

                # Handle input
                if char == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                elif char == '\x1b':  # Escape sequence (arrow keys)
                    next1 = sys.stdin.read(1)
                    next2 = sys.stdin.read(1)
                    if next1 == '[':
                        if next2 == 'A':  # Up arrow
                            self._move_selection_up()
                        elif next2 == 'B':  # Down arrow
                            self._move_selection_down()
                elif char == '\r' or char == '\n':  # Enter
                    if self.filtered_history and 0 <= self.selected_idx < len(self.filtered_history):
                        selected_cmd = self.filtered_history[self.selected_idx]
                        self._execute_command(selected_cmd)
                        break
                elif char == '\x7f':  # Backspace
                    if self.query:
                        self.query = self.query[:-1]
                        self._update_filter()
                elif char.isprintable():
                    self.query += char
                    self._update_filter()

        finally:
            # Restore terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _render_ui(self):
        """Render the current UI state."""
        # Clear screen and move cursor to top
        self.console.clear()

        # Create display
        display_lines = []

        # Show filtered results
        if self.filtered_history:
            display_count = min(len(self.filtered_history), self.max_display)
            for i in range(display_count):
                cmd = self.filtered_history[i]
                if i == self.selected_idx:
                    display_lines.append(f"[bold green]▶ {cmd}[/bold green]")
                else:
                    display_lines.append(f"  {cmd}")

            if len(self.filtered_history) > self.max_display:
                display_lines.append(f"[dim]  ... and {len(self.filtered_history) - self.max_display} more[/dim]")
        else:
            display_lines.append("[yellow]No commands match your search.[/yellow]")

        # Display results
        self.console.print("\n".join(display_lines))

        # Show search bar at bottom
        self.console.print(f"\n[bold blue]Search:[/bold blue] {self.query}█")

    def _update_filter(self):
        """Update filtered history based on current query."""
        if self.query:
            self.filtered_history = self.loader.filter_history(self.history, self.query)
        else:
            self.filtered_history = self.history

        # Reset selection if needed
        if self.selected_idx >= len(self.filtered_history):
            self.selected_idx = max(0, len(self.filtered_history) - 1)

    def _move_selection_up(self):
        """Move selection up in the list."""
        if self.selected_idx > 0:
            self.selected_idx -= 1

    def _move_selection_down(self):
        """Move selection down in the list."""
        if self.selected_idx < len(self.filtered_history) - 1:
            self.selected_idx += 1

    def _execute_command(self, command: str):
        """
        Execute the selected command.

        Args:
            command: Command string to execute.
        """
        # Restore terminal
        self.console.clear()
        self.console.print(f"[bold green]Executing:[/bold green] {command}\n")

        # Execute command
        self.runner.execute(command, log=True)


def main():
    """Main entry point for the Hist CLI."""
    ui = HistUI()
    ui.run()


if __name__ == "__main__":
    main()
