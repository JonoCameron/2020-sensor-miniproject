from pathlib import Path
import argparse

# other code; argparse sets P.log value from command line

P = argparse.ArgumentParser(prog = 'data.json')
P.add_argument("log")
P = P.parse_args()

filename = Path(P.log).expanduser()

# other code

file = filename.open("a")

# other code

file.write("hello world" + "\n")
file.flush()

# other code
    
file.close()