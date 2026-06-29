# Global CLI Installation Feature

## Overview
Convert whip from `python main.py <command>` to a globally accessible `whip <command>` command using setuptools entry points.

## Requirements

### User Installation
After installation, users should be able to:
```bash
pip install -e .
whip summarize
whip write
whip setup
```

From any directory on their machine.

### Configuration Storage
- Global config: `~/.whip/.env` (primary) → `~/.config/whip/.env` (fallback) → current directory (backward compatibility)
- Per-repository tracking: `.git/git-summary-state.txt` remains per repository
- `setup` command creates `~/.whip/` directory if it doesn't exist

### Entry Point
- `whip = main:main` - Maps `whip` command to `main()` function in main.py

## Implementation Details

### 1. Create pyproject.toml
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "whip-git-summarizer"
version = "0.1.0"
description = "AI-powered git change summarizer"
requires-python = ">=3.8"
dependencies = [
    "google-generativeai>=0.3.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

[project.scripts]
whip = "main:main"
```

### 2. Update config.py
- Add `get_config_path()` function that returns path to config file
  - Check `~/.whip/.env` first
  - Check `~/.config/whip/.env` second
  - Check current directory third
  - Return first that exists, or default to `~/.whip/.env` for new configs
- Update `load_model_config()` to use `get_config_path()`
- Update `save_config()` to:
  - Use `get_config_path()` to determine save location
  - Create parent directories if needed
  - Save to `~/.whip/.env` by default

### 3. No changes needed to main.py
- Existing `main()` function already works as entry point
- main.py already handles `.git/git-summary-state.txt` per repository

### 4. Update README
- Add "Installation" section with `pip install -e .`
- Update all command examples from `python main.py` to `whip`
- Add troubleshooting for entry point issues
- Document config file locations

## Error Handling

- If config directory cannot be created: Print warning, continue with current directory fallback
- If `~/.whip` already exists but is a file: Skip and use next fallback
- Invalid permissions: Gracefully fall back to current directory

## Testing Strategy

1. **Unit tests** for `get_config_path()` function
   - Test priority order of config locations
   - Test creation of directories
   - Test error handling

2. **Integration tests**
   - Run `pip install -e .` and verify `whip` command works
   - Run `whip setup` from different directories
   - Verify config is saved to `~/.whip/.env`
   - Verify `whip summarize` works globally

3. **Manual testing**
   - Install package
   - Run `whip setup` from home directory
   - Verify config file created in `~/.whip/.env`
   - Navigate to a git repo, run `whip write` and `whip summarize`
   - Verify state file still created per repo

## Design Rationale

**Why setuptools entry points:** Standard Python approach. Works cross-platform, automatically handles PATH installation, integrates with pip.

**Why `~/.whip/` as primary config location:** Explicit, doesn't pollute home directory, follows similar patterns (e.g., `~/.ssh/`, `~/.gnupg/`).

**Why keep state files per repository:** State tracking is repository-specific. Each repo has its own progress marker which should travel with the repo.

**Why backward compatibility with current directory:** Users who haven't installed globally can still use `python main.py` in the project directory.
