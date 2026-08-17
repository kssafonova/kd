from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

prices = {
    2000: 7990,
    2001: 6990,
    2003: 12990,
    2004: 5990,
    2010: 9990,
}

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

for product_id, price in prices.items():
    article = f"KD-PD-{product_id}"

    catalog_pattern = rf'(makeProduct\({product_id},"{re.escape(article)}","[^"]+","[^"]+",)\d+(,\[)'
    catalog, count_catalog = re.subn(catalog_pattern, rf'\g<1>{price}\g<2>', catalog, count=1)
    if count_catalog != 1:
        raise SystemExit(f"Could not set catalog price for {article}")

    page_pattern = rf'(\{{ id:{product_id}, name:"[^"]+", note:"[^"]+", price:)\d+(, image:)'
    page, count_page = re.subn(page_pattern, rf'\g<1>{price}\g<2>', page, count=1)
    if count_page != 1:
        raise SystemExit(f"Could not set storefront price for {article}")

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Ice Patterns prices applied:", ", ".join(f"KD-PD-{key}={value}" for key, value in prices.items()))
