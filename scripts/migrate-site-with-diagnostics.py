from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
scripts = [
    root / "scripts" / "materialize-grouped-source-v97.py",
    root / "scripts" / "sync-grouped-catalog-v97.py",
    root / "scripts" / "verify-grouped-images-v99.py",
    root / "scripts" / "apply-grouped-catalog-v93.py",
    root / "scripts" / "apply-grouped-catalog-v94.py",
    root / "scripts" / "apply-grouped-catalog-v95.py",
    root / "scripts" / "apply-grouped-catalog-v96.py",
    root / "scripts" / "apply-grouped-catalog-v98.py",
    root / "scripts" / "apply-grouped-catalog-v100.py",
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
