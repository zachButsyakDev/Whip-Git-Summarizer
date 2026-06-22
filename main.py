import subprocess
from pathlib import Path
import ai_module as ai
import sys



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


def get_delta() -> str:
    head = get_current_head()
    last_seen = get_last_seen()
    if head == last_seen:
        sys.exit("No changes since last seen commit.")
    result = subprocess.run(["git", "diff", head, last_seen], capture_output=True, text=True)
    return result.stdout

    
def write_new_last_seen():
    
   # This function writes a new last_seen hash to the text file 'git-summary-state' in the .git directory if it exists and exits with code 1 otherwise.
    path = Path.cwd() / ".git"
    if path.is_dir() == False:
        print("Exited with error code: 1")
        sys.exit("Git repository not initialized. Please initialize a git repository via \'git init\' or otherwise run this in a directory with a valid git repository.")
    with (path / 'git-summary-state.txt').open('w') as state:
        state.write(f"{get_current_head()}")
         
def main():
    if len(sys.argv) < 2:
        sys.exit("No arguments provided. Use 'write' or 'summarize'.")
    
    
    lowercase_argv = [word.lower() for word in sys.argv]
    if lowercase_argv[1] == "write":
        write_new_last_seen()
        return
    elif lowercase_argv[1] == "summarize": 
        print(ai.summarize(get_delta()))
        return
    else:
        sys.exit("Invalid CLI arguments. Use arguments \'write/summarize.\'")
    
if  __name__ == "__main__":
    main()