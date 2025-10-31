#!/usr/bin/env python3
"""Module for safely executing shell commands."""

import subprocess
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class CommandRunner:
    """Handles safe execution of shell commands."""

    def __init__(self, log_file: Optional[Path] = None):
        """
        Initialize the command runner.

        Args:
            log_file: Optional path to log file for executed commands.
        """
        self.log_file = log_file or Path.home() / ".hist_log.txt"

    def execute(self, command: str, log: bool = True) -> bool:
        """
        Execute a shell command safely.

        Args:
            command: Command string to execute.
            log: Whether to log the command execution.

        Returns:
            True if execution was successful, False otherwise.
        """
        if log:
            self._log_command(command)

        try:
            # Execute command in bash shell
            # Using subprocess.run with shell=True for command history compatibility
            result = subprocess.run(
                command,
                shell=True,
                executable="/bin/bash",
                cwd=os.getcwd(),
            )

            return result.returncode == 0

        except Exception as e:
            # TODO: Add proper error logging
            return False

    def _log_command(self, command: str):
        """
        Log executed command to log file.

        Args:
            command: Command string to log.
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {command}\n"

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        except Exception:
            # Silently fail if logging doesn't work
            # TODO: Add proper error handling
            pass

    def confirm_execution(self, command: str) -> bool:
        """
        Ask user to confirm command execution.

        Args:
            command: Command to confirm.

        Returns:
            True if user confirms, False otherwise.
        """
        # This is a placeholder - actual confirmation happens in the UI
        # TODO: Implement in-UI confirmation dialog
        return True

    def edit_command(self, command: str) -> str:
        """
        Allow user to edit command before execution.

        Args:
            command: Original command string.

        Returns:
            Edited command string.
        """
        # TODO: Implement command editing feature
        # This could use readline or a simple input prompt
        return command
