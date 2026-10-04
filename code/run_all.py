"""
ECO6067 Empirical Replication Project
Card & Krueger (1994)

Master script for reproducing the complete project.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = PROJECT_ROOT / "code"


def run_script(filename):
    script_path = CODE_DIR / filename

    print("\n" + "=" * 60)
    print(f"Running: {filename}")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True
    )


def main():

    run_script("01_inspect_data.py")

    run_script("02_clean_data.py")


if __name__ == "__main__":
    main()
