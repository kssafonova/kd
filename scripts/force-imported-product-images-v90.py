from __future__ import annotations

from pathlib import Path
import csv
import html
import posixpath
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
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
UA = "Mozilla/5.0 Kultura-Doma-Catalog-Sync/1.0"

# Exact same-product local image fallbacks. The destination filename always remains
# exactly the filename specified in the authoritative CSV.
LOCAL_SAME_PRODUCT_FALLBACKS = {
    "6a2034e4b2241_big.jpg": "68e774cfc2fb9_big.jpg",
    "6a2034e501385_big.jpg": "68e774cfc2fb9_big.jpg",
    "KD-PD-1128-DARK02.png": "KD-PD-1128-DARK01.png",
}

# Historical source URLs for the files below return 404. For those files only,
# resolve the current product page and use that same product's main image while
# preserving the exact table filename in imported-products.
PRODUCT_PAGE_FALLBACKS: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]] = {
    "69f218d992ea2_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/dorozhki",
        ("Дорожка Дияф",),
        ("https://kultura-doma.ru/product/dorozhka-diyaf",),
    ),
    "69f21944646fb_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/pleysmaty",
        ("Плейсмат Весна",),
        ("https://kultura-doma.ru/product/pleysmat-vesna",),
    ),
    "69f2194651ed2_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/pleysmaty",
        ("Плейсмат Весна",),
        ("https://kultura-doma.ru/product/pleysmat-vesna",),
    ),
    "69f21947d5ab9_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/pleysmaty",
        ("Плейсмат Весна",),
        ("https://kultura-doma.ru/product/pleysmat-vesna",),
    ),
    "6a394b019545c_big.jpg": (
        "https://kultura-doma.ru/catalog/kollekcii",
        ("Чайник заварочный Дияф",),
        ("https://kultura-doma.ru/product/chaynik-zavarochnyy-diyaf",),
    ),
    "6a3a77ab1a012_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/blyuda",
        ("Блюдо овальное Овация",),
        ("https://kultura-doma.ru/product/blyudo-ovalnoe-ovaciya",),
    ),
    "6a3a861013057_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/salatniki",
        ("Салатник Овация",),
        ("https://kultura-doma.ru/product/salatnik-ovaciya",),
    ),
    "6a428351b8c77_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/salfetki",
        ("Салфетка Дияф",),
        ("https://kultura-doma.ru/product/salfetka-diyaf",),
    ),
    "6a43757392be9_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка закусочная Весна",),
        ("https://kultura-doma.ru/product/tarelka-zakusochnaya-vesna",),
    ),
    "6a43757500ab8_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка закусочная Весна",),
        ("https://kultura-doma.ru/product/tarelka-zakusochnaya-vesna",),
    ),
    "6a437575b95e7_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка закусочная Весна",),
        ("https://kultura-doma.ru/product/tarelka-zakusochnaya-vesna",),
    ),
    "6a43757d69bf8_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка обеденная Весна",),
        ("https://kultura-doma.ru/product/tarelka-obedennaya-vesna",),
    ),
    "6a43757dac52e7_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка обеденная Весна",),
        ("https://kultura-doma.ru/product/tarelka-obedennaya-vesna",),
    ),
    "6a43757e29529_big.jpg": (
        "https://kultura-doma.ru/catalog/posuda-i-servirovka/tarelki",
        ("Тарелка обеденная Весна",),
        ("https://kultura-doma.ru/product/tarelka-obedennaya-vesna",),
    ),
    "6a5756979a0b7_big.jpg": (
        "https://kultura-doma.ru/catalog/stolovaya/skaterti",
        ("Скатерть Дияф",),
        ("https://kultura-doma.ru/product/skatert-s-vyshivkoy-diyaf",),
    ),
    "IMG_9416.jpeg": (
        "https://kultura-doma.ru/catalog/dekor-dlya-doma/svechi-i-podsvechniki",
        ("Свеча Корона высокая, без аромата", "Свеча Корона"),
        ("https://kultura-doma.ru/product/svecha-korona-vysokaya-bez-aromata",),
    ),
    "images.jpeg": (
        "https://kultura-doma.ru/catalog/dekor-dlya-doma/svechi-i-podsvechniki",
        ("Свеча с ароматом Древо жизни Жар-птица", "Свеча с ароматом Сандал и Шалфей Жар-птица"),
        (),
    ),
    "images1.jpeg": (
        "https://kultura-doma.ru/catalog/dekor-dlya-doma/svechi-i-podsvechniki",
        ("Свеча с ароматом Древо жизни Жар-птица", "Свеча с ароматом Сандал и Шалфей Жар-птица"),
        (),
    ),
}


def image_basename(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme else value
    return posixpath.basename(path.rstrip("/"))


def normalize_text(value: str) -> str:
    value = html.unescape(value or "").strip().lower().replace("ё", "е")
    return re.sub(r"[^a-zа-я0-9]+", " ", value).strip()


def request_bytes(url: str, timeout: int = 25) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": UA})
    with urlopen(request, timeout=timeout) as response:
        payload = response.read()
        content_type = (response.headers.get("Content-Type") or "").lower()
    return payload, content_type


def request_text(url: str, timeout: int = 25) -> str:
    payload, _ = request_bytes(url, timeout)
    return payload.decode("utf-8", errors="replace")


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_href: str | None = None
        self.current_text: list[str] = []
        self.anchors: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        self.current_href = values.get("href")
        self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.current_href is not None:
            self.anchors.append((self.current_href, " ".join(self.current_text)))
            self.current_href = None
            self.current_text = []


def discover_product_urls(category_url: str, names: tuple[str, ...]) -> list[str]:
    try:
        source = request_text(category_url)
    except Exception:
        return []
    parser = AnchorParser()
    parser.feed(source)
    targets = [normalize_text(name) for name in names]
    matches: list[str] = []
    for href, text in parser.anchors:
        if "/product/" not in href:
            continue
        value = normalize_text(text)
        if not value:
            continue
        if any(target == value or target in value or value in target for target in targets):
            matches.append(urljoin(category_url, href))
    return list(dict.fromkeys(matches))


def product_main_image_url(page_url: str) -> str | None:
    try:
        source = request_text(page_url)
    except Exception:
        return None
    meta_patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
    ]
    for pattern in meta_patterns:
        match = re.search(pattern, source, flags=re.IGNORECASE)
        if match:
            return urljoin(page_url, html.unescape(match.group(1)))
    gallery = re.search(
        r'((?:https?:)?//[^"\'<>\s]+/public/src/images/gallery/catalog/[^"\'<>\s]+\.(?:jpg|jpeg|png|webp)|/public/src/images/gallery/catalog/[^"\'<>\s]+\.(?:jpg|jpeg|png|webp))',
        source,
        flags=re.IGNORECASE,
    )
    if gallery:
        return urljoin(page_url, html.unescape(gallery.group(1)))
    return None


def restore_from_current_product(filename: str) -> tuple[bool, str]:
    spec = PRODUCT_PAGE_FALLBACKS.get(filename)
    if not spec:
        return False, "no same-product fallback configured"
    category_url, names, explicit_urls = spec
    page_urls = list(dict.fromkeys([*explicit_urls, *discover_product_urls(category_url, names)]))
    errors: list[str] = []
    for page_url in page_urls:
        image_url = product_main_image_url(page_url)
        if not image_url:
            errors.append(f"no main image found on {page_url}")
            continue
        try:
            payload, content_type = request_bytes(image_url)
            if len(payload) < 256:
                errors.append(f"image too small from {image_url}")
                continue
            if content_type and "image" not in content_type and "octet-stream" not in content_type:
                errors.append(f"not an image ({content_type}) from {image_url}")
                continue
            (IMAGE_DIR / filename).write_bytes(payload)
            return True, f"{page_url} -> {image_url}"
        except Exception as exc:
            errors.append(f"{image_url}: {exc}")
    return False, "; ".join(errors[-3:]) or f"product page not discovered from {category_url}"


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
            payload, content_type = request_bytes(url, 20)
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
            row[field] = f"/assets/images/{filename}"

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

    same_product_local: list[str] = []
    for filename in list(unresolved):
        source_name = LOCAL_SAME_PRODUCT_FALLBACKS.get(filename)
        source = IMAGE_DIR / source_name if source_name else None
        if source and source.is_file():
            shutil.copy2(source, IMAGE_DIR / filename)
            same_product_local.append(filename)
    unresolved = sorted(filename for filename in unresolved if not (IMAGE_DIR / filename).is_file())

    same_product_web: list[str] = []
    same_product_errors: dict[str, str] = {}
    for filename in list(unresolved):
        restored, detail = restore_from_current_product(filename)
        if restored:
            same_product_web.append(filename)
        else:
            same_product_errors[filename] = detail
    unresolved = sorted(filename for filename in unresolved if not (IMAGE_DIR / filename).is_file())

    if unresolved:
        sample = ", ".join(unresolved[:30])
        suffix = "" if len(unresolved) <= 30 else f" … +{len(unresolved)-30} more"
        first = unresolved[0]
        first_error = same_product_errors.get(first) or download_errors.get(first, "")
        raise SystemExit(
            f"{len(unresolved)} table image filenames remain unavailable after exact lookup, historical URL recovery, "
            f"and same-product fallback: {sample}{suffix}. First error: {first_error}"
        )

    with CATALOG.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"{MARKER}: {len(rows)} SKU rows, {len(referenced)} unique table image filenames, "
        f"{len(copied)} copied by exact filename, {len(downloaded)} restored from table source URLs, "
        f"{len(same_product_local)} restored from same-product local media, "
        f"{len(same_product_web)} restored from current same-product pages -> /assets/images/"
    )


if __name__ == "__main__":
    main()
