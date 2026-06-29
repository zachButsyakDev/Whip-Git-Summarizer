# Whip - What Happened In Progrress - Git Change Summarizer

Whip uses AI to automatically summarize git commit history and code changes. It analyzes diffs between commits and generates human-readable summaries of what changed in your codebase.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd whip_git_summarizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in editable mode:
```bash
pip install -e .
```

4. Set up the global executable (choose one):

**Option A (Recommended - Automatic):**
```bash
python installer.py
```

**Option B (Manual):**
```bash
echo '#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/main.py" "$@"' > whip
chmod +x whip
mv whip ~/.local/bin/
```

### Verifying Installation

```bash
whip setup
```

If the command works, installation is complete.

## Quick Start

### 1. Initial Setup

Before first use, configure your AI provider:

```bash
whip setup
```

This will prompt you to choose:
- **Provider type**: `gemini`, `openai`, or `ollama`
- **Model name**: The specific model to use (e.g., `gpt-4`, `ollama-model-name`)
- **API Key**: Your authentication token (optional for local Ollama)
- **Endpoint URL**: API endpoint (optional for cloud providers, required for Ollama)

Configuration is saved to `.env` file.

### 2. Initialize Tracking State

After setting up the provider, initialize the git-summary state file:

```bash
whip write
```

This creates `.git/git-summary-state.txt` with the current HEAD commit hash. This marks the "last seen" point in your repository.

### 3. Summarize Changes

Summarize all changes since the last seen commit:

```bash
whip summarize
```

The AI will analyze the diff and output a summary of what changed.

## Commands Reference

### `whip setup`
**Purpose**: Configure your AI provider

**Prompts for**:
- Provider type (gemini/openai/ollama)
- Model name
- API key (if applicable)
- Endpoint URL (if applicable)

**Example**:
```bash
$ whip setup
Model Configuration Setup

Provider type (gemini/openai/ollama): openai
Model name: gpt-4
API Key: sk-your-api-key-here
Endpoint URL (press Enter for default OpenAI): 
Configuration saved to .env
```

### `whip write`
**Purpose**: Update the "last seen" commit to current HEAD

**Behavior**:
- Reads current HEAD commit hash
- Updates `.git/git-summary-state.txt` with new hash
- Use this after reviewing a summary to move forward

**Example**:
```bash
$ whip write
# (silently updates the state file)
```

### `whip summarize`
**Purpose**: Generate AI summary of changes since last seen commit

**Basic usage**:
```bash
whip summarize
```

**With commit history options**:

#### Summarize to N'th previous commit:
```bash
whip summarize -n 5
```
Summarizes from the 5th commit before HEAD to the current HEAD.

#### Summarize to specific commit:
```bash
whip summarize --to-commit abc1234
```
Summarizes from commit `abc1234` to current HEAD.

**Output**: AI-generated summary of code changes

**Important**: The state file is **not** automatically updated. Use `whip write` to advance the last-seen marker.

## Supported AI Providers

### Gemini
- **Setup**: Choose "gemini" provider
- **Requirements**: Google Gemini API key (or use `GEMINI_API_KEY` environment variable)
- **Best for**: Free tier availability

### OpenAI-compatible
- **Setup**: Choose "openai" provider
- **Requirements**: API key, endpoint URL
- **Supports**: OpenAI, Azure OpenAI, and any OpenAI-compatible API
- **Example endpoints**:
  - OpenAI: `https://api.openai.com/v1` (default)
  - Azure: `https://{resource}.openai.azure.com/v1`
  - Local: `http://localhost:8000/v1`

### Ollama (Local)
- **Setup**: Choose "ollama" provider
- **Requirements**: Ollama running locally
- **Default endpoint**: `http://localhost:11434`
- **Best for**: Privacy, offline usage, no API costs

## Usage Patterns

```bash
# Set up whip
whip setup

# Mark initial commit as reviewed
whip write

# Summarize changes since last marked commit
whip summarize

# Review and advance marker
whip write

# Review specific history without advancing marker:
whip summarize -n 10  # Last 10 commits
whip summarize --to-commit abc1234  # Up to specific commit
```

## State File Architecture

Whip uses a simple, persistent architecture to track reviewed commits:

```
Read:     Read .git/git-summary-state.txt for last-seen commit
Compare:  Get diff between last-seen and HEAD
Summarize: Pass diff to AI for analysis
Update:   `whip write` updates state file with new HEAD
```

The state file (`.git/git-summary-state.txt`) contains a single line: the commit hash of the last reviewed point.

**Key Points**:
- State file persists across sessions
- Only `whip write` advances the marker
- `whip summarize` never modifies state file
- You can review history at any point without affecting tracking

## Configuration

Configuration is stored in `~/.whip/.env` (or `~/.config/whip/.env` as fallback) with these variables:

```
CUSTOM_MODEL_PROVIDER=openai
CUSTOM_MODEL=gpt-4
CUSTOM_API_KEY=sk-your-key
CUSTOM_MODEL_ENDPOINT=https://api.openai.com/v1
```

**Optional fields by provider**:
- **Gemini**: `CUSTOM_API_KEY` optional (uses `GEMINI_API_KEY` if not set)
- **OpenAI**: `CUSTOM_API_KEY` required, `CUSTOM_MODEL_ENDPOINT` optional (defaults to OpenAI)
- **Ollama**: `CUSTOM_MODEL_ENDPOINT` optional (defaults to localhost:11434)

## Troubleshooting

### "Git repository not initialized"
Ensure you're running whip in a directory with a valid git repository (contains `.git` folder).

### "No changes since last seen commit"
The last-seen commit matches current HEAD. Either make new commits or use `-n` / `--to-commit` to review past history.

### "Target commit is before last-seen commit"
The commit you specified is older than the current tracking point. You can only summarize forward.

### "Invalid commit specifier"
The commit hash or number you provided doesn't exist or is invalid.

## Advanced Usage

### Review specific time period without advancing state
```bash
# See what changed 5 commits ago
whip summarize -n 5
# State file unchanged - use whip write when ready
```

### Audit specific commit range
```bash
whip summarize --to-commit abc1234
```

### Switch AI providers mid-project
```bash
whip setup
# Choose different provider - configuration overwrites previous
```

## Development

### Running tests
```bash
source venv/bin/activate
python -m pytest test_providers.py -v
```

### Project structure
```
whip_git_summarizer/
├── main.py                    # CLI interface and git operations
├── ai_module.py               # AI provider routing
├── config.py                  # Configuration management
├── model_provider.py          # Abstract provider interface
├── gemini_provider.py         # Gemini implementation
├── openai_provider.py         # OpenAI/compatible implementation
├── ollama_provider.py         # Ollama implementation
└── test_providers.py          # Unit tests
```

## Architecture

Whip implements a provider abstraction layer allowing multiple AI backends:

1. **Configuration** loads from `.env` at runtime
2. **Provider selection** routes to appropriate API
3. **Unified interface** (`summarize()` method) across all providers
4. **Fallback** to Gemini if no configuration found

Each provider handles its own API communication, formatting, and error handling.
