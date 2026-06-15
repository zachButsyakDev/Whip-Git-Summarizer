import subprocess
from pathlib import Path
import sys



def get_last_seen():
    pass

def get_current_head():
    

        
    
def init():
    
   # This will run on every startup to see if a .git directory exists. If it does, it will set the HEAD commit as last_seen.
   # It will accomplish this by writing a text file "git-summary-state" to the .git directory
    
    path = Path.cwd() / ".git"
    if path.is_dir() == False:
        print("Exited with error code: 1")
        sys.exit("Git repository not initialized. Please initialize a git repository via \'git init\' or otherwise run this in a directory with a valid git repository.")
    with (path / 'git-summary-state.txt').open('w') as state:
        state.write("last_seen: {get_current_head()}")
    
         
def main():
    init()

if __name__ == "__main__":
    main()