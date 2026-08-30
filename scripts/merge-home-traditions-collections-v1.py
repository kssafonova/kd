from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Keep the collection-product declaration local to HomeView and deterministic.
text = re.sub(
    r'\n  const collectionProductIds=Array\.from\(new Set\(editorials\.flatMap\(item=>item\.productIds\)\)\);\n  const collectionProducts=collectionProductIds\.map\(id=>products\.find\(product=>product\.id===id\)\)\.filter\(\(product\):product is Product=>Boolean\(product\)\);\n',
    '\n',
    text,
    count=1,
)

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
          <img src={assetUrl("/assets/images/russian-bedroom.png")} alt="Современная русская спальня"/>
          <img src={assetUrl("/assets/images/editorial-table.webp")} alt="Сервировка дома"/>
          <img src={assetUrl("/assets/images/time-hero.png")} alt="Предметы Культура дома"/>
          <div className="hv4-traditions-copy"><div><small>BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
        </div>

        <div className="hv4-traditions-collections-content">
          <header className="hv4-traditions-collections-head">
            <div><small>EDITORIAL</small><h2>Капсулы и коллекции</h2></div>
            <div className="hv4-head-actions">
              <button className="hv4-rail-arrow prev" type="button" aria-label="Товары коллекций назад" onClick={()=>scrollHomeRail("home-collection-rail",-1)}><Icon name="arrow"/></button>
              <button className="hv4-rail-arrow" type="button" aria-label="Товары коллекций вперёд" onClick={()=>scrollHomeRail("home-collection-rail",1)}><Icon name="arrow"/></button>
              <button className="hv4-text-cta" type="button" onClick={()=>go("collections")}>СМОТРЕТЬ EDITORIAL</button>
            </div>
          </header>
          <div id="home-collection-rail"><ProductRail className="hv4-collection-product-rail" items={collectionProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/></div>
        </div>
      </div>
    </section>

'''

pattern = r'    <section className="hv4-traditions(?:-collections)?"[\s\S]*?(?=    <section className="hv4-solutions")'
if not re.search(pattern, text):
    raise SystemExit("Traditions/collections homepage block not found")
text = re.sub(pattern, replacement, text, count=1)

PAGE.write_text(text, encoding="utf-8")
print("Merged traditions with white shoppable collection product rail, controls and Editorial CTA")
