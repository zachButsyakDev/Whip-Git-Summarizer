#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def main():
    repo_dir = Path(__file__).parent.absolute()
    local_bin = Path.home() / ".local" / "bin"
    
    # Create ~/.local/bin if it doesn't exist
    local_bin.mkdir(parents=True, exist_ok=True)
    
    # Generate the whip executable script with absolute repo path
    script_content = f"""#!/bin/bash
source "{repo_dir}/venv/bin/activate"
python "{repo_dir}/main.py" "$@"
"""
    
    # Copy to ~/.local/bin
    target_script = local_bin / "whip"
    target_script.write_text(script_content)
    target_script.chmod(0o755)
    
    print("✓ Global whip executable created at ~/.local/bin/whip")
    
    # Check if ~/.local/bin is in PATH
    path_env = os.environ.get('PATH', '')
    if str(local_bin) not in path_env:
        print(f"\n⚠ Warning: ~/.local/bin is not in your PATH")
        print(f"Add this to your ~/.bashrc or ~/.zshrc:")
        print(f"  export PATH=\"$HOME/.local/bin:$PATH\"")
    else:
        print("✓ ~/.local/bin is in your PATH")

if __name__ == "__main__":
    main()
