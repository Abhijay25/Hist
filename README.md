# Hist (Currently Vaulted - Does Not Work)

A Command Line tool to help fuzzy-search for command history. Works for Linux, Mac and WSL.

## Features

- 🔍 **Fuzzy search** through your shell command history
- ⚡ **Fast and responsive** terminal UI
- 🎯 **Arrow key navigation** for selecting commands
- 📝 **Command logging** (optional) to track executed commands
- 🐚 **Multi-shell support** - works with Bash, Zsh, and Fish

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/Hist.git
cd Hist

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Alternative: Run directly

If you prefer not to install, you can run directly:

```bash
# Install dependencies in a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install rich

# Run directly
./hist.py
```

## Usage

Simply run `hist` in your terminal:

```bash
hist
```

### Controls

- **Type** to search through your command history
- **↑/↓** arrow keys to navigate results
- **Enter** to execute the selected command
- **Ctrl+C** to exit

## How it works

Hist loads your shell command history from:
- `~/.bash_history` (Bash)
- `~/.zsh_history` (Zsh)
- `~/.local/share/fish/fish_history` (Fish)

Commands are deduplicated and filtered in real-time as you type. The fuzzy matching algorithm allows you to find commands even if you only remember part of the command.

## Development

### Running tests

```bash
python3 tests/test_hist.py
```

### Project structure

```
Hist/
├── hist.py              # Main CLI entry point
├── history_loader.py    # History loading and filtering
├── runner.py            # Command execution
├── utils.py             # Formatting and helpers
└── tests/
    └── test_hist.py     # Unit tests
```

## License

MIT License
