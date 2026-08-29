from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
script = root / "scripts" / "sync-canonical-table-storefront-v85.py"
proc = subprocess.run(
    [sys.executable, str(script)],
    cwd=root,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
(root / "migration-errors.txt").write_text(proc.stdout, encoding="utf-8")
if proc.returncode != 0:
    print(proc.stdout)
    sys.exit(proc.returncode)
print(proc.stdout)
