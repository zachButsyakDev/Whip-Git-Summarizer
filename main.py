import subprocess
from pathlib import Path
import ai_module as ai
import sys
from config import save_config



def get_last_seen():
    path = Path.cwd() / ".git"
    if path.is_dir() == False:
        print("Exited with error code: 1")
        sys.exit("Git repository not initialized. Please initialize a git repository via \'git init\' or otherwise run this in a directory with a valid git repository.")
    with(path / 'git-summary-state.txt').open('r') as state:
        return state.read().strip()

def get_current_head() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip()


def resolve_commit_specifier(specifier_type, specifier_value):
    """Resolve -n or --to-commit flag to actual commit hash."""
    try:
        if specifier_type == "-n":
            n = int(specifier_value)
            if n <= 0:
                sys.exit("Flag -n requires a positive integer.")
            result = subprocess.run(["git", "rev-list", "--max-count=" + str(n), "HEAD"], 
                                  capture_output=True, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                sys.exit(f"Invalid commit specifier: -n {n}")
            commits = result.stdout.strip().split('\n')
            if len(commits) < n:
                sys.exit(f"Only {len(commits)} commit(s) available, but -n {n} requested.")
            return commits[-1]
        elif specifier_type == "--to-commit":
            result = subprocess.run(["git", "rev-parse", specifier_value], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                sys.exit(f"Invalid commit specifier: {specifier_value}")
            return result.stdout.strip()
    except ValueError:
        sys.exit(f"Flag -n requires a positive integer.")

def get_delta(from_commit=None, use_state_file=True) -> str:
    head = get_current_head()
    
    if from_commit is None:
        if use_state_file:
            from_commit = get_last_seen()
        else:
            sys.exit("No commit specifier provided.")
    
    if head == from_commit:
        sys.exit("No changes since last seen commit.")
    
    result = subprocess.run(["git", "diff", from_commit, head], capture_output=True, text=True)
    return result.stdout

    
def write_new_last_seen():
    
   # This function writes a new last_seen hash to the text file 'git-summary-state' in the .git directory if it exists and exits with code 1 otherwise.
    path = Path.cwd() / ".git"
    if path.is_dir() == False:
        print("Exited with error code: 1")
        sys.exit("Git repository not initialized. Please initialize a git repository via \'git init\' or otherwise run this in a directory with a valid git repository.")
    with (path / 'git-summary-state.txt').open('w') as state:
        state.write(f"{get_current_head()}")


def setup():
    """Interactive setup for model configuration."""
    print("Model Configuration Setup\n")
    
    provider = input("Provider type (gemini/openai/ollama): ").strip().lower()
    if provider not in ["gemini", "openai", "ollama"]:
        sys.exit("Invalid provider type.")
    
    model = input("Model name: ").strip()
    if not model:
        sys.exit("Model name is required.")
    
    api_key = None
    endpoint = None
    
    if provider == "gemini":
        api_key = input("API Key (press Enter to use GEMINI_API_KEY env var): ").strip() or None
    elif provider == "openai":
        api_key = input("API Key: ").strip()
        if not api_key:
            sys.exit("API Key is required for OpenAI.")
        endpoint = input("Endpoint URL (press Enter for default OpenAI): ").strip() or "https://api.openai.com/v1"
    elif provider == "ollama":
        endpoint = input("Endpoint URL (press Enter for default localhost): ").strip() or "http://localhost:11434"
    
    save_config(provider, model, api_key, endpoint)
    print("\nConfiguration saved to .env")

         
def main():
    if len(sys.argv) < 2:
        sys.exit("No arguments provided. Use 'write', 'summarize', or 'setup'.")
    
    lowercase_argv = [word.lower() for word in sys.argv]
    if lowercase_argv[1] == "write":
        write_new_last_seen()
        return
    elif lowercase_argv[1] == "summarize":
        to_commit = None
        use_state_file = True
        
        if len(sys.argv) > 2:
            if sys.argv[2] == "-n" and len(sys.argv) > 3:
                to_commit = resolve_commit_specifier("-n", sys.argv[3])
                use_state_file = False
            elif sys.argv[2] == "--to-commit" and len(sys.argv) > 3:
                to_commit = resolve_commit_specifier("--to-commit", sys.argv[3])
                use_state_file = False
            else:
                sys.exit("Invalid flag usage. Use: whip summarize [-n <number> | --to-commit <hash>]")
        
        print(ai.summarize(get_delta(to_commit, use_state_file)))
        return
    elif lowercase_argv[1] == "setup":
        setup()
        return
    else:
        sys.exit("Invalid CLI arguments. Use arguments 'write', 'summarize', or 'setup'.")
    
if  __name__ == "__main__":
    main()