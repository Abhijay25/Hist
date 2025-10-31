# Claude Code Prompt: Developer-Optimized `Hist` CLI Tool

Generate a **fully working Python CLI tool called `Hist`** for macOS, Linux, and WSL. The tool should let users fuzzy-search their shell command history and execute commands. Requirements:

## Features

1. **Terminal UI**
   - Runs entirely in the **same terminal window**; do not open a full-screen interface.
   - A **search bar at the bottom**.
   - As the user types, history results update **live** above the search bar.
   - Use **Python `rich`** (`rich.live` or equivalent) for dynamic updating.

2. **Core functionality**
   - Load Bash/Zsh history (`~/.bash_history` or `~/.zsh_history`), deduplicate, optionally track frequency.
   - Filter history dynamically based on user input.
   - Display top N results above the search bar.
   - Let the user select a command (arrow keys or Enter) and confirm execution.
   - Execute commands safely in Bash using `subprocess.run(..., shell=True, executable="/bin/bash")`.

3. **Project structure**
Hist/
├── hist.py # main CLI entry point
├── history_loader.py # loads and processes history
├── runner.py # executes commands safely
├── utils.py # formatting, logging, helpers
└── tests/
└── test_hist.py # unit tests with mock history


4. **CLI Packaging**
   - Include `#!/usr/bin/env python3` in `hist.py`.
   - Include a `console_scripts` entry point for pip install so users can run `hist` anywhere.

5. **Optional Enhancements (can be TODOs)**
   - Logging executed commands to `~/.hist_log.txt`.
   - Ranking commands by usage frequency.
   - Edit selected command before execution.
   - Hotkeys for scrolling and exiting.

6. **Testing**
   - Include automated tests in `tests/test_hist.py` covering:
     - History loading and deduplication.
     - Dynamic filtering.
     - Command execution (mocked).
   - Provide mock history data for tests.

## Output Requirements
- Generate **full code for all files** in the structure above.
- Include **comments and TODOs** for enhancements.
- Live search bar with dynamic filtering must work in the same terminal window.
- Make it ready to run and test immediately after copying files.
