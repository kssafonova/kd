from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
PAGE = ROOT / "app" / "page.tsx"


def norm(value: str) -> str:
    return " ".join(str(value or "").strip().lower().replace("ё", "е").split())

# Canonical UI swatch colors for product color names. The build fails for any
# catalog color not listed here so a product can never silently fall back to gray.
COLOR_HEX = {
    "белый": "#F5F5F2",
    "молочный": "#EEE7DA",
    "айвори": "#F1E8D6",
    "слоновая кость": "#F0E6D2",
    "кремовый": "#E8D8BD",
    "экрю": "#DED0B6",
    "бежевый": "#CDB99B",
    "песочный": "#C7A77E",
    "льняной": "#BDA98A",
    "тауп": "#9C8B7B",
    "коричневый": "#765A46",
    "шоколадный": "#4E3528",
    "терракотовый": "#A55E44",
    "оранжевый": "#D98245",
    "желтый": "#D9B84E",
    "золотой": "#B89A5A",
    "золото": "#B89A5A",
    "серебряный": "#B9B9B4",
    "серебро": "#B9B9B4",
    "серый": "#969893",
    "светло-серый": "#C8C9C5",
    "темно-серый": "#5E615F",
    "графитовый": "#4E5354",
    "антрацит": "#3F4547",
    "черный": "#1D1D1B",
    "синий": "#496C8A",
    "темно-синий": "#1D3552",
    "ночной синий": "#142A45",
    "серо-синий": "#667B89",
    "голубой": "#93B8CB",
    "небесный": "#A7C7DA",
    "бирюзовый": "#5E9C9A",
    "зеленый": "#657A61",
    "светло-зеленый": "#9BAE90",
    "темно-зеленый": "#344E3D",
    "оливковый": "#777A4E",
    "хаки": "#77745B",
    "мятный": "#A7BFAF",
    "красный": "#9E403B",
    "темно-красный": "#743633",
    "бордовый": "#6B3038",
    "винный": "#6F3743",
    "розовый": "#D7A1A3",
    "пудровый": "#D8B0A4",
    "персиковый": "#DBA184",
    "лиловый": "#9B819C",
    "фиолетовый": "#76617D",
    "лавандовый": "#A79DBB",
    "прозрачный": "#F3F4F2",
    "дымчатый": "#8B8E8B",
    "янтарный": "#B67A3F",
    "мультиколор": "#9E9588",
    "разноцветный": "#9E9588",
}

with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
    rows = list(csv.DictReader(fh))
colors = sorted({str(row.get("Цвет") or "").strip() for row in rows if str(row.get("Цвет") or "").strip()})
unknown = [color for color in colors if norm(color) not in COLOR_HEX]
if unknown:
    raise SystemExit("CATALOG_COLOR_HEX_V102: unmapped colors: " + " | ".join(unknown))

entries = ",".join(f'{key!r}:"{value}"' for key, value in COLOR_HEX.items())
replacement = f'''const entityColorHex=(value:string)=>{{\n  const key=String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/\\s+/g," ");\n  const colors:Record<string,string>={{{entries}}};\n  return colors[key]??"#D8D5CF";\n}};'''
text = PAGE.read_text(encoding="utf-8")
pattern = r'const entityColorHex=\(value:string\)=>\{.*?\};(?=\nconst entityId=)'
updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit("CATALOG_COLOR_HEX_V102: entityColorHex function not found")
PAGE.write_text(updated, encoding="utf-8")
print(f"// CATALOG_COLOR_HEX_V102: mapped {len(colors)} catalog color names to explicit HEX values: " + ", ".join(colors))
