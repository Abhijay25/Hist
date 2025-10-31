#!/usr/bin/env python3
"""Module for loading and processing shell command history."""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter


class HistoryLoader:
    """Loads and processes shell command history from various sources."""

    def __init__(self):
        """Initialize the history loader."""
        self.history_files = self._detect_history_files()
        self.command_frequency: Counter = Counter()

    def _detect_history_files(self) -> List[Path]:
        """
        Detect available shell history files.

        Returns:
            List of Path objects for existing history files.
        """
        home = Path.home()
        potential_files = [
            home / ".bash_history",
            home / ".zsh_history",
            home / ".local" / "share" / "fish" / "fish_history",
        ]
        return [f for f in potential_files if f.exists()]

    def load_history(self) -> List[str]:
        """
        Load history from all available shell history files.

        Returns:
            List of command strings, deduplicated and cleaned.
        """
        commands = []

        for history_file in self.history_files:
            try:
                commands.extend(self._parse_history_file(history_file))
            except Exception as e:
                # Silently skip files that can't be read
                # TODO: Add logging for debugging
                continue

        # Deduplicate while preserving order (most recent first)
        seen = set()
        deduplicated = []
        for cmd in reversed(commands):
            if cmd and cmd not in seen:
                seen.add(cmd)
                deduplicated.append(cmd)

        # Reverse to get most recent first
        deduplicated.reverse()

        # Update frequency counter
        self.command_frequency.update(deduplicated)

        return deduplicated

    def _parse_history_file(self, filepath: Path) -> List[str]:
        """
        Parse a shell history file.

        Args:
            filepath: Path to the history file.

        Returns:
            List of command strings.
        """
        commands = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                if '.zsh_history' in filepath.name or filepath.name == '.zsh_history':
                    # Zsh history format: : timestamp:duration;command
                    for line in f:
                        line = line.strip()
                        if line.startswith(':'):
                            # Parse zsh extended history format
                            parts = line.split(';', 1)
                            if len(parts) == 2:
                                commands.append(parts[1])
                        else:
                            commands.append(line)
                elif 'fish_history' in filepath.name or filepath.name == 'fish_history':
                    # Fish history format: YAML-like with "- cmd:" entries
                    for line in f:
                        line = line.strip()
                        if line.startswith('- cmd:'):
                            cmd = line[6:].strip()
                            commands.append(cmd)
                else:
                    # Bash and other simple formats
                    for line in f:
                        line = line.strip()
                        if line:
                            commands.append(line)
        except Exception as e:
            # Return what we have so far
            pass

        return commands

    def filter_history(self, history: List[str], query: str) -> List[str]:
        """
        Filter history based on fuzzy search query.

        Args:
            history: List of command strings.
            query: Search query string.

        Returns:
            Filtered list of commands matching the query.
        """
        if not query:
            return history

        query_lower = query.lower()
        filtered = []

        for cmd in history:
            # Simple fuzzy matching: check if all characters in query appear in order
            if self._fuzzy_match(cmd.lower(), query_lower):
                filtered.append(cmd)

        return filtered

    def _fuzzy_match(self, text: str, pattern: str) -> bool:
        """
        Check if pattern characters appear in text in order (fuzzy match).

        Args:
            text: Text to search in.
            pattern: Pattern to search for.

        Returns:
            True if pattern matches text fuzzily.
        """
        if not pattern:
            return True

        pattern_idx = 0
        for char in text:
            if char == pattern[pattern_idx]:
                pattern_idx += 1
                if pattern_idx == len(pattern):
                    return True

        return pattern_idx == len(pattern)

    def rank_by_frequency(self, commands: List[str]) -> List[Tuple[str, int]]:
        """
        Rank commands by usage frequency.

        Args:
            commands: List of command strings.

        Returns:
            List of (command, frequency) tuples sorted by frequency.
        """
        # TODO: Implement frequency-based ranking
        return [(cmd, self.command_frequency.get(cmd, 1)) for cmd in commands]
