# Commit History Summarization Feature

## Overview
Enable users to summarize git changes up to any previous commit hash, not just the last-seen commit. This allows flexibility in reviewing commit history at different points.

## Requirements

### User Input Method
Users specify the target commit using CLI flags:
- `whip summarize --to-commit <hash>` - Summarize to a specific commit hash
- `whip summarize -n <number>` - Summarize to the n'th previous commit (e.g., `-n 5` goes back 5 commits from HEAD)

Both flags are mutually exclusive; only one should be used per invocation.

### Behavior

**Commit Resolution:**
- If `--to-commit` is specified, resolve the commit hash (support short hashes and refs)
- If `-n` is specified, use `git rev-list` to get the n'th commit from HEAD
- If neither flag is provided, use the default behavior (last-seen to HEAD)

**Validation:**
- Validate that the specified commit exists in the repository
- If specified commit is older than last-seen: reject with error message "Target commit is before last-seen commit. Cannot summarize backward."
- If specified commit equals or is newer than HEAD: reject with error message "Target commit must be before HEAD."

### State File Behavior
After summarization completes, the state file (`.git/git-summary-state.txt`) **remains unchanged**. This ensures:
- User can review history at different points without modifying tracking state
- Only explicit `whip write` command updates the state file
- Multiple summaries can be generated without affecting the next full summarization

## Implementation Details

### CLI Argument Parsing
- Extend `main.py` argument parsing to handle `--to-commit` and `-n` flags
- Parse flags after the "summarize" command: `whip summarize [--to-commit <hash> | -n <number>]`

### Git Operations
- Use `git rev-list HEAD` to resolve commit numbers
- Use `git rev-parse` to resolve and validate commit hashes
- Compute diff using specified commit as the "from" point instead of last-seen

### Function Additions
- `get_delta(to_commit=None)` - Extend existing function to accept optional target commit
  - If `to_commit` is None, use last-seen (current behavior)
  - If `to_commit` is provided, use it as the "from" point for diff
- `resolve_commit_specifier(specifier)` - New function to convert `-n` or `--to-commit` values to actual commit hash
  - For `-n N`: run `git rev-list --max-count=N HEAD | tail -1` to get the n'th commit
  - For `--to-commit <hash>`: validate hash exists, return it

### Error Messages
- "No changes since last seen commit." - When last-seen == HEAD and no custom commit specified
- "Target commit is before last-seen commit. Cannot summarize backward." - Invalid target
- "Target commit must be before HEAD." - Target is at or past HEAD
- "Invalid commit specifier: <specifier>" - Commit not found or invalid format
- "Flag -n requires a positive integer." - Invalid -n value

## Usage Examples

```bash
# Summarize changes from last-seen to HEAD (existing behavior)
whip summarize

# Summarize from 5 commits ago to HEAD
whip summarize -n 5

# Summarize to a specific commit hash
whip summarize --to-commit abc1234

# Update state file only after explicit write command
whip write
```

## Testing Strategy

1. **Unit tests** for `resolve_commit_specifier()` function
   - Test `-n` flag resolution
   - Test `--to-commit` hash validation
   - Test error cases (invalid commit, out of range, etc.)

2. **Integration tests** for modified `get_delta()` function
   - Test with real git repository
   - Verify correct diff is returned for various target commits
   - Verify state file remains unchanged after summarization

3. **CLI tests** for argument parsing
   - Test valid flag combinations
   - Test mutual exclusivity of `--to-commit` and `-n`
   - Test invalid flag usage

## Design Rationale

**Why no automatic state file update:** Keeping state unchanged allows users to explore history without committing to a new "last-seen" point. Only explicit `whip write` command updates tracking state.

**Why both flag styles:** `-n` is simpler for "go back N commits", while `--to-commit` is explicit for "summarize to this specific point".

**Why reject backward summarization:** The state file represents a forward-moving checkpoint. Allowing backward summarization could create confusion about which commits have been reviewed.
