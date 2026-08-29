from pathlib import Path
import colorsys
import csv
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
PAGE = ROOT / "app" / "page.tsx"


def norm(value: str) -> str:
    return " ".join(str(value or "").strip().lower().replace("ё", "е").split())

EXACT_HEX = {
    "белый": "#F5F5F2", "молочный": "#EEE7DA", "айвори": "#F1E8D6", "слоновая кость": "#F0E6D2",
    "кремовый": "#E8D8BD", "экрю": "#DED0B6", "бежевый": "#CDB99B", "песочный": "#C7A77E",
    "льняной": "#BDA98A", "тауп": "#9C8B7B", "коричневый": "#765A46", "шоколадный": "#4E3528",
    "терракотовый": "#A55E44", "оранжевый": "#D98245", "желтый": "#D9B84E", "горчичный": "#B38B3D",
    "золотой": "#B89A5A", "золото": "#B89A5A", "бронзовый": "#8E6F4A", "медный": "#A46645",
    "серебряный": "#B9B9B4", "серебро": "#B9B9B4", "серый": "#969893", "светло-серый": "#C8C9C5",
    "темно-серый": "#5E615F", "графитовый": "#4E5354", "антрацит": "#3F4547", "черный": "#1D1D1B",
    "синий": "#496C8A", "темно-синий": "#1D3552", "ночной синий": "#142A45", "серо-синий": "#667B89",
    "голубой": "#93B8CB", "небесный": "#A7C7DA", "бирюзовый": "#5E9C9A", "сапфировый": "#315B7B",
    "зеленый": "#657A61", "светло-зеленый": "#9BAE90", "темно-зеленый": "#344E3D", "оливковый": "#777A4E",
    "хаки": "#77745B", "мятный": "#A7BFAF", "изумрудный": "#3E705E", "красный": "#9E403B",
    "темно-красный": "#743633", "бордовый": "#6B3038", "винный": "#6F3743", "марсала": "#7B4647",
    "гранатовый": "#7A3337", "коралловый": "#C36C62", "розовый": "#D7A1A3", "пудровый": "#D8B0A4",
    "персиковый": "#DBA184", "лиловый": "#9B819C", "фиолетовый": "#76617D", "лавандовый": "#A79DBB",
    "сливовый": "#6F5368", "прозрачный": "#F3F4F2", "дымчатый": "#8B8E8B", "янтарный": "#B67A3F",
    "шампань": "#D3BC8D", "мультиколор": "#9E9588", "разноцветный": "#9E9588",
}

TOKEN_HEX = [
    ("ночн", "#142A45"), ("темно-син", "#1D3552"), ("серо-син", "#667B89"), ("небес", "#A7C7DA"),
    ("голуб", "#93B8CB"), ("сапфир", "#315B7B"), ("син", "#496C8A"), ("бирюз", "#5E9C9A"),
    ("изумруд", "#3E705E"), ("олив", "#777A4E"), ("хаки", "#77745B"), ("мят", "#A7BFAF"),
    ("зелен", "#657A61"), ("зелён", "#657A61"), ("гранат", "#7A3337"), ("марсал", "#7B4647"),
    ("борд", "#6B3038"), ("винн", "#6F3743"), ("темно-крас", "#743633"), ("крас", "#9E403B"),
    ("коралл", "#C36C62"), ("пудр", "#D8B0A4"), ("розов", "#D7A1A3"), ("персик", "#DBA184"),
    ("лаванд", "#A79DBB"), ("лилов", "#9B819C"), ("фиолет", "#76617D"), ("слив", "#6F5368"),
    ("шоколад", "#4E3528"), ("корич", "#765A46"), ("терракот", "#A55E44"), ("оранж", "#D98245"),
    ("янтар", "#B67A3F"), ("горчич", "#B38B3D"), ("желт", "#D9B84E"), ("золот", "#B89A5A"),
    ("бронз", "#8E6F4A"), ("медн", "#A46645"), ("сереб", "#B9B9B4"), ("антрац", "#3F4547"),
    ("графит", "#4E5354"), ("темно-сер", "#5E615F"), ("светло-сер", "#C8C9C5"), ("сер", "#969893"),
    ("черн", "#1D1D1B"), ("молоч", "#EEE7DA"), ("айвори", "#F1E8D6"), ("слонов", "#F0E6D2"),
    ("крем", "#E8D8BD"), ("экрю", "#DED0B6"), ("льня", "#BDA98A"), ("песоч", "#C7A77E"),
    ("беж", "#CDB99B"), ("тауп", "#9C8B7B"), ("шампан", "#D3BC8D"), ("бел", "#F5F5F2"),
    ("прозрач", "#F3F4F2"), ("дым", "#8B8E8B"), ("мульти", "#9E9588"), ("разноцвет", "#9E9588"),
]


def deterministic_hex(name: str) -> str:
    digest = hashlib.sha256(norm(name).encode("utf-8")).digest()
    hue = int.from_bytes(digest[:2], "big") / 65535.0
    saturation = 0.28 + (digest[2] / 255.0) * 0.22
    lightness = 0.48 + (digest[3] / 255.0) * 0.16
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return f"#{round(r*255):02X}{round(g*255):02X}{round(b*255):02X}"


def semantic_hex(name: str) -> str:
    key = norm(name)
    if key in EXACT_HEX:
        return EXACT_HEX[key]
    for token, value in TOKEN_HEX:
        if token in key:
            return value
    return deterministic_hex(key)

with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
    rows = list(csv.DictReader(fh))
colors = sorted({str(row.get("Цвет") or "").strip() for row in rows if str(row.get("Цвет") or "").strip()})
observed = {norm(color): semantic_hex(color) for color in colors}
if len(observed) != len({norm(color) for color in colors}):
    raise SystemExit("CATALOG_COLOR_HEX_V102: duplicate normalized color keys")

entries = ",".join(f'{key!r}:"{value}"' for key, value in observed.items())
replacement = f'''const entityColorHex=(value:string)=>{{\n  const key=String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/\\s+/g," ");\n  const colors:Record<string,string>={{{entries}}};\n  return colors[key]??"#8F8A82";\n}};'''
text = PAGE.read_text(encoding="utf-8")
pattern = r'const entityColorHex=\(value:string\)=>\{.*?\};(?=\nconst entityId=)'
updated, count = re.subn(pattern, lambda _: replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit("CATALOG_COLOR_HEX_V102: entityColorHex function not found")
PAGE.write_text(updated, encoding="utf-8")
print(f"// CATALOG_COLOR_HEX_V102: generated explicit HEX for {len(colors)} actual catalog colors")
for color in colors:
    print(f"// COLOR_HEX: {color} = {observed[norm(color)]}")
