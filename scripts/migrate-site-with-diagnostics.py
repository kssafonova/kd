from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
scripts = [
    root / "scripts" / "sync-full-xlsx-catalog-v88.py",
    root / "scripts" / "apply-grouped-catalog-v93.py",
    root / "scripts" / "apply-grouped-catalog-v94.py",
    root / "scripts" / "apply-grouped-catalog-v95.py",
    root / "scripts" / "apply-grouped-catalog-v96.py",
]

logs=[]
for script in scripts:
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    logs.append(f"$ {script.name}\n{proc.stdout}")
    if proc.returncode != 0:
        diagnostics="\n".join(logs)
        (root / "migration-errors.txt").write_text(diagnostics, encoding="utf-8")
        print(diagnostics)
        sys.exit(proc.returncode)

diagnostics="\n".join(logs)
(root / "migration-errors.txt").write_text(diagnostics, encoding="utf-8")
print(diagnostics)
