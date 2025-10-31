# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hist is a command line tool for fuzzy-searching command history across Linux, Mac, and WSL.

## Current State

This is a new repository with minimal code. The project structure and implementation language have not yet been established.

## Cross-Platform Considerations

When implementing features, ensure compatibility across:
- Linux (native shell history: bash, zsh, fish)
- macOS (native shell history: bash, zsh)
- WSL (Windows Subsystem for Linux)

Shell history file locations vary by shell and platform:
- Bash: `~/.bash_history`
- Zsh: `~/.zsh_history`
- Fish: `~/.local/share/fish/fish_history`

## Development Considerations

- The tool should be fast and responsive for interactive use
- Fuzzy search should provide relevant results quickly, even with large history files
- Consider shell-specific history formats and timestamps
- Handle different character encodings gracefully
