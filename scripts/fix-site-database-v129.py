from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "apply-site-database-v128.py"
text = TARGET.read_text(encoding="utf-8")
old = "        pattern = rf'(function {function_name}\\([^)]*\\)\\{{\\n  )const boutiques=(\\[.*?\\]);'"
new = "        pattern = rf'(function {function_name}[^\\n]*\\{{\\n  )const boutiques=(\\[.*?\\]);'"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("SITE_DATABASE_FIX_V129: target regex signature not found")
TARGET.write_text(text, encoding="utf-8")
print("// SITE_DATABASE_FIX_V129: typed BoutiqueMap signature support applied")