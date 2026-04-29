from __future__ import annotations

import subprocess
from typing import Sequence



def run_command(args: Sequence[str]) -> str:
    completed = subprocess.run(
        list(args),
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout
