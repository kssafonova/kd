from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
script = root / "scripts" / "sync-canonical-table-storefront-v85.py"
page = root / "app" / "page.tsx"

proc = subprocess.run(
    [sys.executable, str(script)],
    cwd=root,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if proc.returncode != 0:
    (root / "migration-errors.txt").write_text(proc.stdout, encoding="utf-8")
    print(proc.stdout)
    sys.exit(proc.returncode)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f"{label}: source fragment not found")


text = page.read_text(encoding="utf-8")
text = replace_once(
    text,
    '  rows.forEach(row=>{const key=`${row["Артикул"]}|${row["Название товара"]}`;const list=grouped.get(key)||[];list.push(row);grouped.set(key,list)});',
    '  rows.forEach(row=>{const key=String(row["Артикул"]||"").trim();const list=grouped.get(key)||[];list.push(row);grouped.set(key,list)});',
    "article-only product grouping",
)
text = replace_once(
    text,
    '  // The canonical table may reuse one article for distinct named products, so article+name is the storefront entity key.\n  // CANONICAL_TABLE_SYNC_V85',
    '  // Product identity follows the canonical article: every table row with the same article is one product with SKU variants.\n  // ARTICLE_PRIMARY_GROUPING_V86\n  // CANONICAL_TABLE_SYNC_V85',
    "article grouping marker",
)
text = replace_once(
    text,
    '    const existing=products.find(product=>String(product.article||"").trim()===article&&String(product.name||"").trim()===name);',
    '    const existing=products.find(product=>String(product.article||"").trim()===article);',
    "article-only existing product lookup",
)
page.write_text(text, encoding="utf-8")

message = proc.stdout + "\nArticle-primary storefront grouping applied\n"
(root / "migration-errors.txt").write_text(message, encoding="utf-8")
print(message)
