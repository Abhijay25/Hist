#!/usr/bin/env python3
"""
Unit tests for Hist CLI tool.

Tests cover history loading, deduplication, filtering, and command execution.
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from history_loader import HistoryLoader
from runner import CommandRunner


class TestHistoryLoader(unittest.TestCase):
    """Test cases for HistoryLoader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.loader = HistoryLoader()
        # Mock history data
        self.mock_bash_history = [
            "ls -la",
            "cd /home/user",
            "git status",
            "python script.py",
            "ls -la",  # Duplicate
            "grep 'pattern' file.txt",
        ]
        self.mock_zsh_history = [
            ": 1234567890:0;ls -la",
            ": 1234567891:0;cd /tmp",
            ": 1234567892:0;vim config.txt",
        ]

    def test_fuzzy_match(self):
        """Test fuzzy matching algorithm."""
        # Test exact matches
        self.assertTrue(self.loader._fuzzy_match("hello world", "hello"))
        self.assertTrue(self.loader._fuzzy_match("hello world", "world"))

        # Test fuzzy matches
        self.assertTrue(self.loader._fuzzy_match("hello world", "hw"))
        self.assertTrue(self.loader._fuzzy_match("git status", "gst"))
        self.assertTrue(self.loader._fuzzy_match("python script.py", "psp"))
        self.assertTrue(self.loader._fuzzy_match("git status", "sta"))  # Characters in order

        # Test non-matches
        self.assertFalse(self.loader._fuzzy_match("hello world", "xyz"))
        self.assertFalse(self.loader._fuzzy_match("git status", "tsg"))  # Wrong order

    def test_filter_history(self):
        """Test history filtering."""
        history = [
            "ls -la",
            "cd /home/user",
            "git status",
            "python script.py",
            "grep 'pattern' file.txt",
        ]

        # Test filtering with query (note: "git" matches both "git status" and "grep" via fuzzy matching)
        filtered = self.loader.filter_history(history, "gits")
        self.assertIn("git status", filtered)
        self.assertEqual(len(filtered), 1)

        # Test fuzzy filtering
        filtered = self.loader.filter_history(history, "psp")
        self.assertIn("python script.py", filtered)

        # Test empty query returns all
        filtered = self.loader.filter_history(history, "")
        self.assertEqual(len(filtered), len(history))

    def test_deduplication(self):
        """Test that duplicate commands are removed."""
        # Create temp history file with duplicates
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_history') as f:
            f.write("\n".join(self.mock_bash_history))
            temp_file = f.name

        try:
            # Mock the history files
            with patch.object(self.loader, 'history_files', [Path(temp_file)]):
                commands = self.loader.load_history()

                # Check that duplicates are removed
                self.assertEqual(len(commands), len(set(commands)))

                # Check that "ls -la" appears only once
                ls_count = sum(1 for cmd in commands if cmd == "ls -la")
                self.assertEqual(ls_count, 1)
        finally:
            os.unlink(temp_file)

    def test_parse_bash_history(self):
        """Test parsing bash history format."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_history') as f:
            f.write("\n".join(self.mock_bash_history))
            temp_file = Path(f.name)

        try:
            commands = self.loader._parse_history_file(temp_file)
            self.assertGreater(len(commands), 0)
            self.assertIn("ls -la", commands)
            self.assertIn("git status", commands)
        finally:
            temp_file.unlink()

    def test_parse_zsh_history(self):
        """Test parsing zsh history format."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.zsh_history') as f:
            f.write("\n".join(self.mock_zsh_history))
            temp_file = Path(f.name)

        try:
            commands = self.loader._parse_history_file(temp_file)
            self.assertGreater(len(commands), 0)
            self.assertIn("ls -la", commands)
            self.assertIn("cd /tmp", commands)
            self.assertIn("vim config.txt", commands)
        finally:
            temp_file.unlink()

    def test_empty_history(self):
        """Test handling of empty history."""
        with patch.object(self.loader, 'history_files', []):
            commands = self.loader.load_history()
            self.assertEqual(len(commands), 0)


class TestCommandRunner(unittest.TestCase):
    """Test cases for CommandRunner class."""

    def setUp(self):
        """Set up test fixtures."""
        # Use temp log file
        self.temp_log = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_log.close()
        self.runner = CommandRunner(log_file=Path(self.temp_log.name))

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_log.name):
            os.unlink(self.temp_log.name)

    @patch('subprocess.run')
    def test_execute_command(self, mock_run):
        """Test command execution."""
        # Mock successful execution
        mock_run.return_value = MagicMock(returncode=0)

        result = self.runner.execute("echo 'test'", log=False)
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        """Test command execution failure handling."""
        # Mock failed execution
        mock_run.return_value = MagicMock(returncode=1)

        result = self.runner.execute("false", log=False)
        self.assertFalse(result)

    def test_command_logging(self):
        """Test that commands are logged correctly."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            # Execute command with logging
            self.runner.execute("echo 'test'", log=True)

            # Check log file exists and contains command
            self.assertTrue(os.path.exists(self.temp_log.name))

            with open(self.temp_log.name, 'r') as f:
                log_content = f.read()
                self.assertIn("echo 'test'", log_content)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def test_load_filter_workflow(self):
        """Test complete workflow of loading and filtering history."""
        loader = HistoryLoader()

        # Create mock history
        mock_commands = [
            "git status",
            "git commit -m 'test'",
            "python script.py",
            "ls -la",
            "cd /tmp",
        ]

        # Test filtering workflow
        filtered = loader.filter_history(mock_commands, "git")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all("git" in cmd for cmd in filtered))

        # Test fuzzy filtering
        filtered = loader.filter_history(mock_commands, "psp")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], "python script.py")


def run_tests():
    """Run all tests."""
    unittest.main()


if __name__ == "__main__":
    run_tests()
