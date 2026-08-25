from pathlib import Path
import subprocess
import sys

scripts = [
    "sync-workbook-product-specs.py",
    "restore-quick-add-flow.py",
    "add-remote-image-loader.py",
    "sync-updated-product-image-urls.py",
    "apply-pdp-reference-gallery.py",
    "normalize-single-color-swatches.py",
    "apply-story-builder-v2.py",
    "refine-story-builder-v2.py",
    "redesign-home-reference.py",
    "add-home-bedroom-feature.py",
    "refine-homepage-editorial.py",
    "remove-editorial-tabs.py",
    "add-editorial-scenario-navigation.py",
    "add-constructor-home-cta.py",
    "apply-product-catalog-rules-v1.py",
    "apply-catalog-category-mapping.py",
    "apply-product-pricing-merchandising-v1.py",
    "apply-pdp-collection-recommendations-v1.py",
    "highlight-menu-solutions-v1.py",
    "remove-retired-editorials-v1.py",
    "refine-editorial-tabs-v1.py",
    "add-ice-pattern-products-v1.py",
    "fix-ice-pattern-2000-2004-types.py",
    "apply-product-preview-rules-v1.py",
    "add-editorial-story-overlay-v1.py",
    "redesign-home-magazine-v2.py",
    "redesign-home-commerce-v3.py",
    "redesign-home-v4.py",
    "merge-home-traditions-collections-v1.py",
    "refine-home-v7.py",
    "refine-home-v8.py",
    "refine-home-v9.py",
    "refine-home-togas-v10.py",
    "refine-home-ux-v11.py",
    "refine-home-v11-video.py",
    "add-mobile-gift-wrap-flow-v1.py",
    "refine-cart-controls-v19.py",
    "apply-auth-flow-v20.py",
    "redesign-collections-v23.py",
    "redesign-collections-v34.py",
    "refine-green-salon-v35.py",
    "refine-red-lines-v36.py",
    "refine-winter-fairy-v37.py",
    "redesign-ready-solutions-v38.py",
    "redesign-ready-solutions-hero-v39.py",
    "redesign-commerce-zara-kultura-v41.py",
    "redesign-commerce-hypotheses-v42.py",
    "fix-commerce-v42-crosssell.py",
    "redesign-commerce-clarity-v43.py",
    "redesign-home-zara-kultura-v44.py",
    "redesign-home-sketch-v45.py",
    "redesign-ready-solutions-constructor-v46.py",
]

root = Path(__file__).resolve().parents[1]
script_dir = root / "scripts"
log_path = root / "migration-errors.txt"
results = []
failed = []

# catalog-data.ts is now a lightweight runtime overlay over catalog-data-base.ts.
# These older one-off catalog migration scripts expect the full productList to live
# directly in catalog-data.ts, so rerunning them is no longer valid. Their changes
# are already present in catalog-data-base.ts and the current source tree.
legacy_catalog_patches = {
    "sync-updated-product-image-urls.py",
    "apply-product-catalog-rules-v1.py",
    "add-ice-pattern-products-v1.py",
    "fix-ice-pattern-2000-2004-types.py",
    "apply-product-preview-rules-v1.py",
}
uses_catalog_overlay = (root / "app" / "catalog-data-base.ts").exists()

for name in scripts:
    path = script_dir / name
    if not path.exists():
        failed.append(name)
        results.append(f"\n===== {name} =====\nERROR: script not found\n")
        continue

    if uses_catalog_overlay and name in legacy_catalog_patches:
        results.append(f"\n===== {name} =====\nSKIPPED: catalog-data runtime overlay is active; legacy catalog patch already materialized in catalog-data-base.ts\n")
        continue

    # The story builder patch is intentionally conditional in the old workflow.
    if name == "apply-story-builder-v2.py":
        page = (root / "app" / "page.tsx").read_text(encoding="utf-8")
        if "story-v2-layer" in page:
            results.append(f"\n===== {name} =====\nSKIPPED: adaptive story builder already present\n")
            continue

    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    results.append(f"\n===== {name} =====\nexit={proc.returncode}\n{proc.stdout}\n")
    if proc.returncode != 0:
        failed.append(name)

log_path.write_text("".join(results), encoding="utf-8")

if failed:
    print("Migration patch failures:", ", ".join(failed))
    print(f"Full log: {log_path}")
    sys.exit(1)

print("All migration patches completed successfully")
