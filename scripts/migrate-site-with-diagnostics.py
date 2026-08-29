from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
script = root / "scripts" / "sync-full-xlsx-catalog-v88.py"
proc = subprocess.run(
    [sys.executable, str(script)],
    cwd=root,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
diagnostics = f"$ {script.name}\n{proc.stdout}"
(root / "migration-errors.txt").write_text(diagnostics, encoding="utf-8")
print(diagnostics)
if proc.returncode != 0:
    sys.exit(proc.returncode)
