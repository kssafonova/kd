from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_master.csv"

# CATALOG_PREVIEW_COLORS_V122
# The catalog ProductCard uses the first color variant generated for an article.
# Keep all SKU/color variants, but order the requested preview color first.
EXACT_ARTICLE_PREFERENCES = {
    "KD-PD-2001": ("ночной синий",),       # Тарелка «Ледяные узоры»
    "KD-PD-2000": ("ледяной голубой",),    # Декоративная подушка «Ледяные узоры»
    "KD-PD-1026": ("синий",),              # Плед из кружева
    "KD-PD-1023": ("синий",),              # Подушка с кружевом
}

COLLECTION_PREFERENCES = {
    # For Texture prefer black; if a product has no black variant, use brown.
    "текстура": ("черный", "коричневый"),
    "оренбургские узоры": ("бежевый",),
}


def norm(value):
    text = unicodedata.normalize("NFC", str(value or "")).strip().casefold()
    return text.replace("ё", "е")


text = CATALOG.read_text(encoding="utf-8")
if not text:
    raise SystemExit("CATALOG_PREVIEW_COLORS_V122: catalog_master.csv is empty")

# Records may contain line breaks inside text fields. Every product record starts with
# an article at the beginning of a physical line, so split only at those boundaries.
chunks = re.split(r"(?=^KD-PD-)", text, flags=re.MULTILINE)
if len(chunks) < 2:
    raise SystemExit("CATALOG_PREVIEW_COLORS_V122: no product records found")

header_chunk = chunks[0]
header_line = header_chunk.rstrip("\r\n")
header = header_line.split(";")
required_columns = ["Артикул", "Название товара", "Цвет", "Коллекция"]
missing_columns = [name for name in required_columns if name not in header]
if missing_columns:
    raise SystemExit("CATALOG_PREVIEW_COLORS_V122: missing columns " + ", ".join(missing_columns))

idx = {name: header.index(name) for name in required_columns}
records = []
for position, chunk in enumerate(chunks[1:]):
    if chunk.endswith("\r\n"):
        raw = chunk[:-2]
    elif chunk.endswith("\n"):
        raw = chunk[:-1]
    else:
        raw = chunk
    parts = raw.split(";")
    if len(parts) != len(header):
        raise SystemExit(
            f"CATALOG_PREVIEW_COLORS_V122: malformed catalog record at position {position + 1}; "
            f"fields={len(parts)} expected={len(header)}"
        )
    records.append({
        "chunk": chunk,
        "article": parts[idx["Артикул"]].strip(),
        "name": parts[idx["Название товара"]].strip(),
        "color": parts[idx["Цвет"]].strip(),
        "collection": parts[idx["Коллекция"]].strip(),
    })

article_positions = {}
for position, record in enumerate(records):
    article_positions.setdefault(record["article"], []).append(position)

missing_exact = sorted(set(EXACT_ARTICLE_PREFERENCES) - set(article_positions))
if missing_exact:
    raise SystemExit("CATALOG_PREVIEW_COLORS_V122: missing exact articles " + ", ".join(missing_exact))

changed_articles = []
preview_report = []

for article, positions in article_positions.items():
    article_records = [records[position] for position in positions]
    collection = norm(article_records[0]["collection"])
    preferences = EXACT_ARTICLE_PREFERENCES.get(article) or COLLECTION_PREFERENCES.get(collection)
    if not preferences:
        continue

    normalized_preferences = tuple(norm(color) for color in preferences)
    colors = [norm(record["color"]) for record in article_records]
    available_preference = next((color for color in normalized_preferences if color in colors), None)
    if available_preference is None:
        raise SystemExit(
            f"CATALOG_PREVIEW_COLORS_V122: {article} ({article_records[0]['name']}) has no requested preview color; "
            f"available={','.join(record['color'] for record in article_records)}; "
            f"wanted={','.join(preferences)}"
        )

    rank = {color: index for index, color in enumerate(normalized_preferences)}
    ordered = sorted(
        enumerate(article_records),
        key=lambda pair: (rank.get(norm(pair[1]["color"]), len(rank)), pair[0]),
    )
    ordered_records = [record for _, record in ordered]

    if [record["chunk"] for record in ordered_records] != [record["chunk"] for record in article_records]:
        changed_articles.append(article)

    for position, record in zip(positions, ordered_records):
        records[position] = record

    first_color = norm(ordered_records[0]["color"])
    if first_color != available_preference:
        raise SystemExit(
            f"CATALOG_PREVIEW_COLORS_V122: failed to put preferred color first for {article}; "
            f"got={ordered_records[0]['color']} expected={available_preference}"
        )
    preview_report.append(f"{article}={ordered_records[0]['color']}")

output = header_chunk + "".join(record["chunk"] for record in records)
if len(records) != len(chunks) - 1:
    raise SystemExit("CATALOG_PREVIEW_COLORS_V122: row count changed unexpectedly")
CATALOG.write_text(output, encoding="utf-8")

print(
    "CATALOG_PREVIEW_COLORS_V122: preferred catalog previews applied; "
    f"target_articles={len(preview_report)}; reordered_articles={len(changed_articles)}; "
    f"reordered={','.join(changed_articles) or 'none'}; previews={' | '.join(preview_report)}"
)
