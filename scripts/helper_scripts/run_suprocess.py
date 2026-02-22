import subprocess
from pathlib import Path

def run_cmd(cmd):
    try:
        print(f"Start running: {cmd}")
        code = subprocess.run(cmd, capture_output=True, text=True)
        print(f"returncode: {code.returncode}")
        print(f"stdout: \n {code.stdout}")
        print(f"stderr: \n {code.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error when running subprocess {cmd}\nError: {e}")

