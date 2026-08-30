from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "apply-site-database-v128.py"
text = TARGET.read_text(encoding="utf-8")

# The storefront's BoutiqueMap has a typed prop signature. The original V128
# regexp only matched untyped function signatures, so make the migration work
# with both forms and remain safe to run on every build.
old = "        pattern = rf'(function {function_name}\\([^)]*\\)\\{{\\n  )const boutiques=(\\[.*?\\]);'"
new = "        pattern = rf'(function {function_name}[^\\n]*\\{{\\n  )const boutiques=(\\[.*?\\]);'"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("SITE_DATABASE_FIX_V129: target regex signature not found")

# TypeScript infers the fallback payment instruments as a narrow literal union
# from the `as const` fallback. The database rows are ordinary strings, so the
# runtime membership check must deliberately operate on a string collection.
old_cash = 'method.instruments.includes("cash")'
new_cash = '(method.instruments as readonly string[]).includes("cash")'
if old_cash in text:
    text = text.replace(old_cash, new_cash, 1)
elif new_cash not in text:
    raise SystemExit("SITE_DATABASE_FIX_V129: payment instrument check not found")

TARGET.write_text(text, encoding="utf-8")
print("// SITE_DATABASE_FIX_V129: typed BoutiqueMap + payment instrument compatibility applied")
