from __future__ import annotations

from pathlib import Path
import csv
import posixpath
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
SOURCE_DIR = ROOT / "scripts" / "product-source"
PUBLIC_IMAGES = ROOT / "public" / "images"
BUILT_IMAGES = ROOT / "images"
IMAGE_DIR = PUBLIC_IMAGES / "imported-products"
PHOTO_FIELDS = [
    "Превью фотография товара",
    "Вторая фотография товара в скролле",
    "Третья фотография в стролле",
]
RAW_PHOTO_FIELDS = ["Фото 1", "Фото 2", "Фото 3"]
MARKER = "// IMPORTED_PRODUCT_IMAGES_V90"


def image_basename(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme else value
    return posixpath.basename(path.rstrip("/"))


def build_source_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for base in (PUBLIC_IMAGES, BUILT_IMAGES):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.parent != IMAGE_DIR:
                index.setdefault(path.name, path)
    return index


def raw_url_candidates() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for source_path in sorted(SOURCE_DIR.glob("products_part_*.csv")):
        with source_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh, delimiter=";")
            raw = list(reader)
        if not raw:
            continue
        header = raw[0]
        indices = [header.index(name) for name in RAW_PHOTO_FIELDS if name in header]
        for row in raw[1:]:
            for index in indices:
                value = (row[index] if index < len(row) else "").strip()
                filename = image_basename(value)
                if not filename:
                    continue
                candidates = result.setdefault(filename, [])
                if value.startswith(("http://", "https://")):
                    if value not in candidates:
                        candidates.append(value)
                elif value.startswith("/kd/"):
                    url = "https://kssafonova.github.io" + value
                    if url not in candidates:
                        candidates.append(url)
                elif "/" not in value:
                    url = "https://kultura-doma.ru/public/src/images/gallery/catalog/" + filename
                    if url not in candidates:
                        candidates.append(url)
    return result


def fetch_image(filename: str, candidates: list[str]) -> tuple[str, str | None, str | None]:
    target = IMAGE_DIR / filename
    fallback = f"https://kultura-doma.ru/public/src/images/gallery/catalog/{filename}"
    urls = list(dict.fromkeys([*candidates, fallback]))
    last_error: str | None = None
    for url in urls:
        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0 Kultura-Doma-Catalog-Sync/1.0"})
            with urlopen(request, timeout=20) as response:
                payload = response.read()
                content_type = (response.headers.get("Content-Type") or "").lower()
            if len(payload) < 256:
                last_error = f"too small ({len(payload)} bytes) from {url}"
                continue
            if content_type and "image" not in content_type and "octet-stream" not in content_type:
                last_error = f"not an image ({content_type}) from {url}"
                continue
            target.write_bytes(payload)
            return filename, url, None
        except Exception as exc:
            last_error = f"{url}: {exc}"
    return filename, None, last_error


def main() -> None:
    if not CATALOG.exists():
        raise SystemExit(f"Missing generated catalog: {CATALOG}")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = reader.fieldnames or []

    missing_columns = [field for field in PHOTO_FIELDS if field not in fields]
    if missing_columns:
        raise SystemExit("Missing photo columns: " + ", ".join(missing_columns))

    referenced: set[str] = set()
    for row in rows:
        for field in PHOTO_FIELDS:
            filename = image_basename(row.get(field, ""))
            if not filename:
                row[field] = ""
                continue
            referenced.add(filename)
            row[field] = f"/images/imported-products/{filename}"

    source_index = build_source_index()
    copied: list[str] = []
    missing_files: list[str] = []
    for filename in sorted(referenced):
        target = IMAGE_DIR / filename
        if target.is_file():
            continue
        source = source_index.get(filename)
        if source and source.is_file():
            shutil.copy2(source, target)
            copied.append(filename)
        else:
            missing_files.append(filename)

    downloaded: list[str] = []
    download_errors: dict[str, str] = {}
    if missing_files:
        candidates = raw_url_candidates()
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {
                pool.submit(fetch_image, filename, candidates.get(filename, [])): filename
                for filename in missing_files
            }
            for future in as_completed(futures):
                filename, source_url, error = future.result()
                if source_url:
                    downloaded.append(filename)
                else:
                    download_errors[filename] = error or "download failed"

    unresolved = sorted(filename for filename in missing_files if not (IMAGE_DIR / filename).is_file())
    if unresolved:
        sample = ", ".join(unresolved[:30])
        suffix = "" if len(unresolved) <= 30 else f" … +{len(unresolved)-30} more"
        first_error = download_errors.get(unresolved[0], "")
        raise SystemExit(
            f"{len(unresolved)} table image filenames remain unavailable after local lookup and source-URL download: "
            f"{sample}{suffix}. First error: {first_error}"
        )

    with CATALOG.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"{MARKER}: {len(rows)} SKU rows, {len(referenced)} unique table image filenames, "
        f"{len(copied)} copied locally, {len(downloaded)} restored from table source URLs -> /images/imported-products/"
    )


if __name__ == "__main__":
    main()
