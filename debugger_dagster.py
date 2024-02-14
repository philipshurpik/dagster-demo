import subprocess
import sys

if __name__ == "__main__":
    subprocess.call([sys.executable, "-m", "dagster", "dev"])
