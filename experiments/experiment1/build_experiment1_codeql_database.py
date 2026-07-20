""This script creates the database for codeql consisting of the datasets.""

from __future__ import annotations

import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
OUTPUT_ROOT = ROOT / "outputs" / "experiment2_static_baselines"
SOURCE_TREE = OUTPUT_ROOT / "source_tree"
CODEQL_DB = OUTPUT_ROOT / "codeql_db"


def run_command(command: list[str], timeout: int = 1800):
    start = time.time()
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr, round(time.time() - start, 3)


def main() -> int:
    if not SOURCE_TREE.exists():
        raise FileNotFoundError(
            f"Source tree not found: {SOURCE_TREE}\n"
            "Run scripts/prepare_experiment2_static_dataset.py first."
        )

    if CODEQL_DB.exists():
        print(f"Removing old database: {CODEQL_DB}")
        shutil.rmtree(CODEQL_DB)

    command = [
        "codeql",
        "database",
        "create",
        str(CODEQL_DB),
        "--language=python",
        f"--source-root={SOURCE_TREE}",
        "--overwrite",
    ]

    print("Building Experiment 2 CodeQL database...")
    print(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Source tree: {SOURCE_TREE}")
    print(f"Database path: {CODEQL_DB}")
    print("\nCommand:")
    print(" ".join(command))

    returncode, stdout, stderr, latency = run_command(command)

    print("\nCodeQL database create finished.")
    print(f"Return code: {returncode}")
    print(f"Latency seconds: {latency}")

    if stdout.strip():
        print("\nSTDOUT:")
        print(stdout)

    if stderr.strip():
        print("\nSTDERR:")
        print(stderr)

    if returncode != 0:
        print("\nDatabase creation failed.")
        return returncode

    if not CODEQL_DB.exists():
        print("\nDatabase folder was not created.")
        return 1

    db_files = list(CODEQL_DB.rglob("*"))
    print("\nDatabase creation verified.")
    print(f"Database exists: {CODEQL_DB}")
    print(f"Database file count: {len(db_files)}")

    print("\nNext step after verification:")
    print("Create/run the CodeQL analysis script against this database.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())