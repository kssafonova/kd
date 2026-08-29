from __future__ import annotations

from pathlib import Path
import csv
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "all_site_products_full.xlsx"
PAGE = ROOT / "app" / "page.tsx"
OUT = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
MARKER = "// FULL_XLSX_CATALOG_V88"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def col_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref or "A").group(0)
    value = 0
    for ch in letters:
        value = value * 26 + ord(ch) - 64
    return value - 1


def read_first_sheet(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iterfind(".//m:t", NS)))

        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        sheet = wb.find("m:sheets/m:sheet", NS)
        rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = rel_map[rid]
        sheet_path = "xl/" + target.lstrip("/") if not target.startswith("xl/") else target
        root = ET.fromstring(zf.read(sheet_path))

        rows: list[list[str]] = []
        for row in root.findall("m:sheetData/m:row", NS):
            values: dict[int, str] = {}
            for cell in row.findall("m:c", NS):
                idx = col_index(cell.attrib.get("r", "A1"))
                kind = cell.attrib.get("t")
                if kind == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iterfind(".//m:t", NS))
                else:
                    node = cell.find("m:v", NS)
                    raw = node.text if node is not None and node.text is not None else ""
                    if kind == "s" and raw:
                        value = shared[int(raw)]
                    elif kind == "b":
                        value = "TRUE" if raw == "1" else "FALSE"
                    else:
                        value = raw
                values[idx] = value
            if values:
                width = max(values) + 1
                current = [""] * width
                for idx, value in values.items():
                    current[idx] = value
                rows.append(current)
        return rows


def normalize_number(value: str) -> str:
    value = (value or "").strip()
    if re.fullmatch(r"-?\d+\.0", value):
        return value[:-2]
    return value


def normalize_image(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("/kd/images/"):
        return value[3:]
    prefix = "https://kssafonova.github.io/kd"
    if value.startswith(prefix + "/images/"):
        return value[len(prefix):]
    if value.startswith("https://kultura-doma.ru/"):
        return "/images/imported-products/" + value.rstrip("/").split("/")[-1]
    if re.match(r"^https?://", value):
        return value
    if "/" not in value:
        return "/images/imported-products/" + value
    return value


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old, new, 1)


def main() -> None:
    if not XLSX.exists():
        raise SystemExit(f"Missing {XLSX.name}")
    raw = read_first_sheet(XLSX)
    if len(raw) < 2:
        raise SystemExit("XLSX has no product rows")

    headers = raw[0]
    pos = {name: i for i, name in enumerate(headers)}
    required = ["ID", "Артикул", "Название товара", "Цена", "Фото 1"]
    missing = [name for name in required if name not in pos]
    if missing:
        raise SystemExit("Missing XLSX columns: " + ", ".join(missing))

    def get(row: list[str], name: str) -> str:
        i = pos.get(name)
        return normalize_number(row[i] if i is not None and i < len(row) else "")

    rows: list[dict[str, str]] = []
    for source in raw[1:]:
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
            "Капсула": get(source, "Капсула"),
            "Категория": get(source, "Категория"),
            "Подкатегория": get(source, "Подкатегория"),
            "Товар входит в готовое решение": get(source, "Товар входит в готовое решение"),
            "Опционально входит в готовое решение": get(source, "Опционально входит в готовое решение"),
            "Описание готового решения": get(source, "Капсула") if headers.count("Капсула") == 1 else "",
            "Превью фотография товара": normalize_image(get(source, "Фото 1")),
            "Вторая фотография товара в скролле": normalize_image(get(source, "Фото 2")),
            "Третья фотография в стролле": normalize_image(get(source, "Фото 3")),
            "Offer ID": get(source, "Offer ID"),
        })

    # Fill photo gaps from the same article + aroma/color, then from the article itself.
    by_variant: dict[tuple[str, str], list[str]] = {}
    by_article: dict[str, list[str]] = {}
    for row in rows:
        key = (row["Артикул"], (row["Аромат"] or row["Цвет"]).strip())
        photos = [row["Превью фотография товара"], row["Вторая фотография товара в скролле"], row["Третья фотография в стролле"]]
        if any(photos):
            by_variant.setdefault(key, photos)
            by_article.setdefault(row["Артикул"], photos)
    for row in rows:
        key = (row["Артикул"], (row["Аромат"] or row["Цвет"]).strip())
        fallback = by_variant.get(key) or by_article.get(row["Артикул"]) or []
        photo_keys = ["Превью фотография товара", "Вторая фотография товара в скролле", "Третья фотография в стролле"]
        for i, field in enumerate(photo_keys):
            if not row[field] and i < len(fallback):
                row[field] = fallback[i]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    page = PAGE.read_text(encoding="utf-8")
    page = replace_once(
        page,
        'const XLSX_ENTITY_FILES:string[] = []; // canonical data is loaded from the compressed table snapshot below',
        'const XLSX_ENTITY_FILES:string[] = ["catalog_xlsx_full.csv"]; // FULL_XLSX_CATALOG_V88',
        "full XLSX source",
    )
    page = replace_once(
        page,
        '  const extra=await loadCompressedEntityCsv();\n  const rows=[...chunks.flat(),...extra].filter(row=>row["Артикул"]&&row["Название товара"]);',
        '  const rows=chunks.flat().filter(row=>row["Артикул"]&&row["Название товара"]);',
        "disable stale compressed snapshot",
    )
    page = replace_once(
        page,
        '      const color=String(row["Цвет"]||"").trim()||"Без цвета";',
        '      const color=String(row["Аромат"]||row["Цвет"]||"").trim()||"Без цвета";',
        "aroma variants",
    )
    page = replace_once(
        page,
        'collection:String(row["Коллекция"]||"").trim()||undefined,price:',
        'collection:String(row["Коллекция"]||"").trim()||undefined,capsule:String(row["Капсула"]||"").trim()||undefined,price:',
        "capsule field",
    )
    page = replace_once(
        page,
        '  giftPackagingAvailable?: boolean;\n};',
        '  giftPackagingAvailable?: boolean;\n  category?: string;\n  subcategory?: string;\n  collection?: string;\n  capsule?: string;\n  readySolution?: string;\n  optionalReadySolution?: string;\n  offerId?: string;\n};',
        "product XLSX metadata fields",
    )
    page = replace_once(
        page,
        'incoming.push({...existing,id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,oldPrice:tableOldPrice>price?tableOldPrice:undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:colorRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery}))});',
        'incoming.push({...existing,id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,oldPrice:tableOldPrice>price?tableOldPrice:undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:colorRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery})),category:String(first["Категория"]||"").trim()||undefined,subcategory:String(first["Подкатегория"]||"").trim()||undefined,collection:String(first["Коллекция"]||"").trim()||undefined,capsule:String(first["Капсула"]||"").trim()||undefined,readySolution:String(first["Товар входит в готовое решение"]||"").trim()||undefined,optionalReadySolution:String(first["Опционально входит в готовое решение"]||"").trim()||undefined,offerId:String(first["Offer ID"]||"").trim()||undefined});',
        "product XLSX metadata mapping",
    )
    page = replace_once(
        page,
        'const catalogText=(product:Product)=>`${product.name} ${product.note}`.toLocaleLowerCase("ru-RU").replace(/ё/g,"е");',
        'const catalogText=(product:Product)=>`${product.name} ${product.note} ${product.category||""} ${product.subcategory||""}`.toLocaleLowerCase("ru-RU").replace(/ё/g,"е");',
        "catalog category metadata",
    )
    PAGE.write_text(page, encoding="utf-8")

    articles = {row["Артикул"] for row in rows}
    photos = {row[field] for row in rows for field in ("Превью фотография товара", "Вторая фотография товара в скролле", "Третья фотография в стролле") if row[field]}
    print(f"{MARKER}: {len(rows)} SKU rows, {len(articles)} article products, {len(photos)} referenced images -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
