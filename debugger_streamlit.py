import subprocess
import sys

if __name__ == "__main__":
    subprocess.call([sys.executable, "-m", "streamlit", "run", "demo_interface.py"])
