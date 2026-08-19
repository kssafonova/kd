from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Build one shoppable product rail from all active Editorial capsules/collections.
# Keep the data tied to editorials so the homepage updates automatically when
# collection assortment changes.
if "const collectionProducts=" not in text:
    anchor = '  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;'
    insert = '''  const collectionProductIds=Array.from(new Set(editorials.flatMap(item=>item.productIds)));
  const collectionProducts=collectionProductIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
'''
    if anchor not in text:
        raise SystemExit("constructorHref anchor not found")
    text = text.replace(anchor, insert + anchor, 1)

# Collection cover cards are no longer used on the homepage.
text = re.sub(
    r'\n  const capsuleCards=\[\n[\s\S]*?\n  \];\n(?=  const collectionProductIds=|  const constructorHref=)',
    '\n',
    text,
    count=1,
)

replacement = r'''    <section className="hv4-traditions-collections" aria-label="Традиции, капсулы и коллекции">
      <div className="hv4-traditions-collections-shell">
        <div className="hv4-traditions-media">
          <img src={assetUrl("/images/russian-bedroom.png")} alt="Современная русская спальня"/>
          <img src={assetUrl("/images/editorial-table.webp")} alt="Сервировка дома"/>
          <img src={assetUrl("/images/time-hero.png")} alt="Предметы Культура дома"/>
          <div className="hv4-traditions-copy"><div><small>15 СЕКУНД · BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
        </div>

        <div className="hv4-traditions-collections-content">
          <header className="hv4-traditions-collections-head">
            <div><small>EDITORIAL</small><h2>Капсулы и коллекции</h2></div>
            <button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ EDITORIAL</button>
          </header>
          <ProductRail className="hv4-collection-product-rail" items={collectionProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
        </div>
      </div>
    </section>

'''

# Handles both states: the original two separate V4 sections after redesign-home-v4.py
# and an already merged section in the checked-in source.
pattern = r'    <section className="hv4-traditions(?:-collections)?"[\s\S]*?(?=    <section className="hv4-solutions")'
if not re.search(pattern, text):
    raise SystemExit("Traditions/collections homepage block not found")
text = re.sub(pattern, replacement, text, count=1)

PAGE.write_text(text, encoding="utf-8")
print("Merged traditions with a shoppable collection product rail and Editorial CTA")
