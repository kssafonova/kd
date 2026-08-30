from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
scripts = [
    root / "scripts" / "consolidate-image-assets-v111.py",
    root / "scripts" / "apply-catalog-master-v107.py",
    root / "scripts" / "apply-catalog-supplements-v112.py",
    root / "scripts" / "apply-priority-products-v120.py",
    root / "scripts" / "apply-spring-product-images-v118.py",
    root / "scripts" / "apply-diyaf-product-images-v119.py",
    root / "scripts" / "apply-product-images-v120.py",
    root / "scripts" / "remove-catalog-products-v121.py",
    root / "scripts" / "apply-catalog-preview-colors-v122.py",
    root / "scripts" / "verify-catalog-master-v107.py",
    root / "scripts" / "export-site-database-v126.py",
    root / "scripts" / "apply-pdp-size-quantity-v110.py",
    root / "scripts" / "apply-home-redesign-v113.py",
    root / "scripts" / "apply-home-zarahome-v114.py",
    root / "scripts" / "apply-home-hero-images-v115.py",
    root / "scripts" / "apply-home-category-images-v116.py",
    root / "scripts" / "apply-home-new-products-capsules-v117.py",
    root / "scripts" / "apply-catalog-filters-v123.py",
    root / "scripts" / "apply-catalog-filters-ux-v125.py",
]

logs = []
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
        diagnostics = "\n".join(logs)
        (root / "migration-errors.txt").write_text(diagnostics, encoding="utf-8")
        print(diagnostics)
        sys.exit(proc.returncode)

diagnostics = "\n".join(logs)
(root / "migration-errors.txt").write_text(diagnostics, encoding="utf-8")
print(diagnostics)