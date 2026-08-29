from __future__ import annotations

from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "product-source"
PAGE = ROOT / "app" / "page.tsx"
OUT = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
MARKER = "// FULL_CSV_CATALOG_V89"
SOURCE_GLOB = "products_part_*.csv"


def normalize_number(value: str) -> str:
    value = (value or "").strip()
    return value[:-2] if re.fullmatch(r"-?\d+\.0", value) else value


def normalize_image(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("/kd/images/"):
        return value[3:]
    github_pages = "https://kssafonova.github.io/kd"
    if value.startswith(github_pages + "/images/"):
        return value[len(github_pages):]
    if value.startswith("https://kultura-doma.ru/"):
        return "/images/imported-products/" + value.rstrip("/").split("/")[-1]
    if re.match(r"^https?://", value):
        return value
    if "/" not in value:
        return "/images/imported-products/" + value
    return value


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old, new, 1)


def read_source_rows() -> tuple[list[str], list[list[str]], int]:
    files = sorted(SOURCE_DIR.glob(SOURCE_GLOB))
    if not files:
        raise SystemExit(f"No authoritative CSV parts found in {SOURCE_DIR}")

    headers: list[str] | None = None
    raw_rows: list[list[str]] = []
    for path in files:
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh, delimiter=";")
            current_headers = next(reader, None)
            if not current_headers:
                continue
            if headers is None:
                headers = current_headers
            elif current_headers != headers:
                raise SystemExit(f"Header mismatch in {path.name}")
            raw_rows.extend(row for row in reader if any((cell or "").strip() for cell in row))

    if headers is None:
        raise SystemExit("Authoritative CSV source has no header")
    return headers, raw_rows, len(files)


def main() -> None:
    headers, raw_rows, source_parts = read_source_rows()
    positions: dict[str, list[int]] = {}
    for i, name in enumerate(headers):
        positions.setdefault(name, []).append(i)

    required = ["ID", "Артикул", "Название товара", "Цена", "Фото 1"]
    missing = [name for name in required if name not in positions]
    if missing:
        raise SystemExit("Missing CSV columns: " + ", ".join(missing))

    def get(row: list[str], name: str, occurrence: int = 0) -> str:
        indexes = positions.get(name, [])
        if occurrence >= len(indexes):
            return ""
        i = indexes[occurrence]
        return normalize_number(row[i] if i < len(row) else "")

    rows: list[dict[str, str]] = []
    for source in raw_rows:
        article = get(source, "Артикул").strip()
        name = get(source, "Название товара").strip()
        if not article or not name:
            continue
        rows.append({
            "Id": get(source, "ID"),
            "Артикул": article,
            "Название товара": name,
            "Цвет": get(source, "Цвет"),
            "Аромат": get(source, "Аромат"),
            "Размер": get(source, "Размер"),
            "Цена": get(source, "Цена"),
            "Старая цена": get(source, "Старая цена"),
            "Высота": get(source, "Высота"),
            "Ширина": get(source, "Ширина"),
            "Объем": get(source, "Объем"),
            "Диаметр": get(source, "Диаметр"),
            "Комплектация / Информация о размере": get(source, "Комплектация / информация о размере"),
            "Материал": get(source, "Материал"),
            "Состав": get(source, "Состав"),
            "Детали": get(source, "Детали"),
            "Коллекция": get(source, "Коллекция"),
            "Капсула": get(source, "Капсула", 0),
            "Категория": get(source, "Категория"),
            "Подкатегория": get(source, "Подкатегория"),
            "Товар входит в готовое решение": get(source, "Товар входит в готовое решение"),
            "Опционально входит в готовое решение": get(source, "Опционально входит в готовое решение"),
            "Описание готового решения": get(source, "Капсула", 1),
            "Превью фотография товара": normalize_image(get(source, "Фото 1")),
            "Вторая фотография товара в скролле": normalize_image(get(source, "Фото 2")),
            "Третья фотография в стролле": normalize_image(get(source, "Фото 3")),
        })

    if not rows:
        raise SystemExit("Authoritative CSV source has no product rows")

    # Fill only missing media values from another SKU of the same product.
    # Product attributes themselves are never inherited from the previous storefront dataset.
    by_variant: dict[tuple[str, str, str], list[str]] = {}
    by_article: dict[str, list[str]] = {}
    photo_fields = ["Превью фотография товара", "Вторая фотография товара в скролле", "Третья фотография в стролле"]
    for row in rows:
        key = (row["Артикул"], row["Цвет"].strip(), row["Аромат"].strip())
        photos = [row[field] for field in photo_fields]
        if any(photos):
            by_variant.setdefault(key, photos)
            by_article.setdefault(row["Артикул"], photos)
    for row in rows:
        key = (row["Артикул"], row["Цвет"].strip(), row["Аромат"].strip())
        fallback = by_variant.get(key) or by_article.get(row["Артикул"]) or []
        for i, field in enumerate(photo_fields):
            if not row[field] and i < len(fallback):
                row[field] = fallback[i]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    page = PAGE.read_text(encoding="utf-8")
    page = page.replace(
        'const XLSX_ENTITY_FILES:string[] = ["catalog_xlsx_full.csv"]; // FULL_XLSX_CATALOG_V88',
        'const XLSX_ENTITY_FILES:string[] = ["catalog_xlsx_full.csv"]; // FULL_CSV_CATALOG_V89',
        1,
    )
    page = page.replace("  offerId?: string;\n", "", 1)
    page = replace_required(
        page,
        '    const price=tablePrice>0?tablePrice:(existing?.price??0);',
        '    const price=tablePrice;',
        "table-only product price",
    )
    page = replace_required(
        page,
        '    incoming.push({...existing,id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,oldPrice:tableOldPrice>price?tableOldPrice:undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:colorRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery})),category:String(first["Категория"]||"").trim()||undefined,subcategory:String(first["Подкатегория"]||"").trim()||undefined,collection:String(first["Коллекция"]||"").trim()||undefined,capsule:String(first["Капсула"]||"").trim()||undefined,readySolution:String(first["Товар входит в готовое решение"]||"").trim()||undefined,optionalReadySolution:String(first["Опционально входит в готовое решение"]||"").trim()||undefined,offerId:String(first["Offer ID"]||"").trim()||undefined});',
        '    incoming.push({id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,oldPrice:tableOldPrice>price?tableOldPrice:undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:colorRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery})),category:String(first["Категория"]||"").trim()||undefined,subcategory:String(first["Подкатегория"]||"").trim()||undefined,collection:String(first["Коллекция"]||"").trim()||undefined,capsule:String(first["Капсула"]||"").trim()||undefined,readySolution:String(first["Товар входит в готовое решение"]||"").trim()||undefined,optionalReadySolution:String(first["Опционально входит в готовое решение"]||"").trim()||undefined});',
        "remove stale product fallback and offer id",
    )
    PAGE.write_text(page, encoding="utf-8")

    articles = {row["Артикул"] for row in rows}
    photos = {row[field] for row in rows for field in photo_fields if row[field]}
    print(
        f"{MARKER}: {len(rows)} SKU rows, {len(articles)} article products, "
        f"{len(photos)} referenced images, {source_parts} source parts -> {OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
