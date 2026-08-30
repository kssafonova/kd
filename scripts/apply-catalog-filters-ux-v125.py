from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

if "CATALOG_FILTERS_UX_V125" in text:
    print("// CATALOG_FILTERS_UX_V125: already applied")
    raise SystemExit(0)

marker = "// CATALOG_FILTERS_V123"
if marker not in text:
    raise SystemExit("CATALOG_FILTERS_UX_V125: CATALOG_FILTERS_V123 marker not found")
text = text.replace(marker, marker + "\n// CATALOG_FILTERS_UX_V125", 1)

old_toolbar = '''    <div className="catalog-tools catalog-tools-v123">
      <label className="catalog-sort-v123"><span>Сортировка</span><select value={sort} onChange={event=>changeSort(event.target.value as CatalogSortV123)} aria-label="Сортировка товаров"><option value="popular">По популярности</option><option value="price_asc">Сначала дешевле</option><option value="price_desc">Сначала дороже</option></select></label>
      <button className="catalog-filter-trigger-v123" type="button" onClick={openFilters}><Icon name="filter"/><span>Фильтры</span>{activeCount>0&&<b>{activeCount}</b>}</button>
    </div>'''
new_toolbar = '''    <div className="catalog-tools catalog-tools-v123">
      <button className="catalog-filter-trigger-v123" type="button" onClick={openFilters}><span>Фильтры</span>{activeCount>0&&<b>{activeCount}</b>}</button>
      <label className="catalog-sort-v123"><span>Сортировка</span><span className="catalog-sort-select-v125"><select value={sort} onChange={event=>changeSort(event.target.value as CatalogSortV123)} aria-label="Сортировка товаров"><option value="popular">По популярности</option><option value="price_asc">Сначала дешевле</option><option value="price_desc">Сначала дороже</option></select><Icon name="chevron"/></span></label>
    </div>'''
if old_toolbar not in text:
    raise SystemExit("CATALOG_FILTERS_UX_V125: toolbar signature not found")
text = text.replace(old_toolbar, new_toolbar, 1)

replacements = [
    (
        r'\{subcategoryOptions\.length>0&&<section className="catalog-filter-section-v123"><h3>Тип товара</h3><div className="catalog-filter-options-v123">(.*?)</div></section>\}',
        lambda m: '{subcategoryOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={draft.subcategories.length>0}><summary><span>Тип товара</span>{draft.subcategories.length>0&&<b>{draft.subcategories.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">' + m.group(1) + '</div></div></details>}'
    ),
    (
        r'\{\(collectionOptions\.length>0\|\|capsuleOptions\.length>0\)&&<section className="catalog-filter-section-v123"><h3>Коллекция / капсула</h3><div className="catalog-filter-options-v123">(.*?)</div></section>\}',
        lambda m: '{(collectionOptions.length>0||capsuleOptions.length>0)&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={(draft.collections.length+draft.capsules.length)>0}><summary><span>Коллекция / капсула</span>{(draft.collections.length+draft.capsules.length)>0&&<b>{draft.collections.length+draft.capsules.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">' + m.group(1) + '</div></div></details>}'
    ),
    (
        r'\{materialOptions\.length>0&&<section className="catalog-filter-section-v123"><h3>Материал</h3><div className="catalog-filter-options-v123">(.*?)</div></section>\}',
        lambda m: '{materialOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={draft.materials.length>0}><summary><span>Материал</span>{draft.materials.length>0&&<b>{draft.materials.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">' + m.group(1) + '</div></div></details>}'
    ),
    (
        r'\{sizeOptions\.length>0&&<section className="catalog-filter-section-v123"><h3>Размер</h3><div className="catalog-filter-options-v123">(.*?)</div></section>\}',
        lambda m: '{sizeOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={draft.sizes.length>0}><summary><span>Размер</span>{draft.sizes.length>0&&<b>{draft.sizes.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">' + m.group(1) + '</div></div></details>}'
    ),
    (
        r'\{colorOptions\.length>0&&<section className="catalog-filter-section-v123"><h3>Цвет</h3><div className="catalog-filter-options-v123 catalog-filter-colors-v123">(.*?)</div></section>\}',
        lambda m: '{colorOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={draft.colors.length>0}><summary><span>Цвет</span>{draft.colors.length>0&&<b>{draft.colors.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123 catalog-filter-colors-v123">' + m.group(1) + '</div></div></details>}'
    ),
    (
        r'\{\(minCatalogPrice>0\|\|maxCatalogPrice>0\)&&<section className="catalog-filter-section-v123"><h3>Цена</h3>(.*?)</section>\}',
        lambda m: '{(minCatalogPrice>0||maxCatalogPrice>0)&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125" defaultOpen={Boolean(draft.priceFrom||draft.priceTo)}><summary><span>Цена</span>{(draft.priceFrom||draft.priceTo)&&<b>1</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125">' + m.group(1) + '</div></details>}'
    ),
]

for pattern, replacement in replacements:
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"CATALOG_FILTERS_UX_V125: section signature not found: {pattern[:60]}")

page_path.write_text(text, encoding="utf-8")
print("// CATALOG_FILTERS_UX_V125: toolbar simplified; filter groups converted to accessible accordions; active groups reopen on drawer mount")
