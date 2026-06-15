import subprocess
from pathlib import Path
import sys



def get_last_seen():
    pass

def get_current_head():
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout

        
    
def write_new_last_seen():
    
   # This function writes a new last_seen hash to the text file 'git-summary-state' in the .git directory if it exists and exits with code 1 otherwise.
    path = Path.cwd() / ".git"
    if path.is_dir() == False:
        print("Exited with error code: 1")
        sys.exit("Git repository not initialized. Please initialize a git repository via \'git init\' or otherwise run this in a directory with a valid git repository.")
    with (path / 'git-summary-state.txt').open('w') as state:
        state.write(f"last_seen: {get_current_head()}")
         
def main():


if __name__ == "__main__":
    main()