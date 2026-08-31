from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
scripts = [
    root / "scripts" / "prepare-route-split-v137.py",
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
    root / "scripts" / "build-site-runtime-v128.py",
    root / "scripts" / "export-filter-database-v127.py",
    root / "scripts" / "apply-pdp-size-quantity-v110.py",
    root / "scripts" / "apply-home-redesign-v113.py",
    root / "scripts" / "apply-home-zarahome-v114.py",
    root / "scripts" / "apply-home-hero-images-v115.py",
    root / "scripts" / "apply-home-category-images-v116.py",
    root / "scripts" / "apply-home-new-products-capsules-v117.py",
    root / "scripts" / "apply-catalog-filters-v123.py",
    root / "scripts" / "apply-catalog-filters-ux-v125.py",
    root / "scripts" / "fix-site-database-v129.py",
    root / "scripts" / "apply-site-database-v128.py",
    root / "scripts" / "apply-color-group-filters-v131.py",
    root / "scripts" / "build-site-runtime-v128.py",
    root / "scripts" / "apply-runtime-consumers-v130.py",
    root / "scripts" / "fix-table-driven-catalog-v136.py",
    root / "scripts" / "apply-table-driven-catalog-v135.py",
    root / "scripts" / "finalize-route-split-v137.py",
    root / "scripts" / "optimize-catalog-runtime-v138.py",
    root / "scripts" / "optimize-plp-images-v139.py",
    root / "scripts" / "restore-deferred-plp-gallery-v140.py",
    root / "scripts" / "fix-catalog-runtime-v141.py",
    root / "scripts" / "embed-catalog-products-v142.py",
    root / "scripts" / "finalize-catalog-plp-v143.py",
    root / "scripts" / "apply-kultura-performance-v145.py",
    root / "scripts" / "apply-kultura-navigation-v146.py",
    root / "scripts" / "apply-unified-kultura-menu-v147.py",
    root / "scripts" / "refine-home-plp-card-v148.py",
    root / "scripts" / "fix-mobile-header-actions-v149.py",
    root / "scripts" / "ensure-mobile-header-actions-v150.py",
    root / "scripts" / "apply-capsule-experience-v151.py",
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
