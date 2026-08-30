from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

# Restore the combined Collections + Capsules experience that existed before
# the separate story-index / lookbook flow. Keep later SKU/PDP changes intact.
text = text.replace(
    'type View = "home" | "catalog" | "collections" | "capsules" | "editorial" | "product";',
    'type View = "home" | "catalog" | "collections" | "editorial" | "product";'
)

text = text.replace(
    '      {view === "collections" && <CollectionsView mode="collections" openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}\n'
    '      {view === "capsules" && <CollectionsView mode="capsules" openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}\n',
    '      {view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}\n'
)

home_story_pattern = r'''    <section className="home-story-gateway">.*?</section>\n\n    <section className="section products-section">'''
home_story_replacement = '''    <section className="editorial"><img src={assetUrl("/assets/images/time-hero.png")} alt="Капсула Нити времени"/><div><p>НОВАЯ КАПСУЛА</p><h2>Нити времени</h2><span>Вдохновлена движением звёзд<br/>и бесконечной красотой ночного неба.</span><button onClick={() => go("collections")}>ОТКРЫТЬ ИСТОРИЮ →</button></div></section>\n\n    <section className="section products-section">'''
text = re.sub(home_story_pattern, home_story_replacement, text, count=1, flags=re.S)

text = text.replace(
    '<button className="menu-feature" onClick={()=>go("collections")}>КОЛЛЕКЦИИ</button><button className="menu-feature" onClick={()=>go("capsules")}>КАПСУЛЫ & STORIES</button>',
    '<button className="menu-feature" onClick={()=>go("collections")}>КАПСУЛЫ И КОЛЛЕКЦИИ</button>'
)
text = text.replace(
    '<button onClick={()=>go("capsules")}>EDITORIAL / LOOKBOOK</button>',
    '<button onClick={()=>go("collections")}>EDITORIAL</button>'
)

collections_view = r'''function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  const [kind,setKind]=useState("ВСЕ");
  const visible=editorials.filter(item=>kind==="ВСЕ"||(kind==="КАПСУЛЫ"&&item.kind==="КАПСУЛА")||(kind==="КОЛЛЕКЦИИ"&&item.kind==="КОЛЛЕКЦИЯ"));
  return <div className="collections page"><div className="section-head"><p>EDITORIAL</p><h1>Коллекции и капсулы</h1></div><div className="center-tabs">{["ВСЕ","КАПСУЛЫ","КОЛЛЕКЦИИ"].map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div><div className="collection-grid">{visible.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ {item.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ"} <Icon name="arrow"/></span></div></button></article>)}</div></div>;
}'''
text, count = re.subn(
    r'function CollectionsView\([\s\S]*?\n\}(?=\n\nfunction EditorialView)',
    collections_view,
    text,
    count=1,
    flags=re.S
)
if count != 1 and 'function CollectionsView({ openEditorial }' not in text:
    raise SystemExit(f"CollectionsView restore failed: {count}")

editorial_view = r'''function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const variant=editorial.id==="time"?"cinematic":editorial.id==="buyan"?"offset":editorial.id==="poetry"?"magazine":"gallery";
  const chapter=editorial.id==="time"?"NIGHT STUDY":editorial.id==="buyan"?"SUMMER TABLE":editorial.id==="poetry"?"POETRY OF HOME":"FOLKLORE REFRAMED";
  const index=editorial.id==="time"?"01":editorial.id==="buyan"?"02":editorial.id==="poetry"?"03":"04";
  const productImage=items[0]?.image||editorial.images[0];

  return <div className={`editorial-page zara-editorial editorial-variant-${variant}`}>
    <section className="zh-editorial-cover">
      <img src={assetUrl(editorial.images[0])} alt={editorial.name}/>
      <div className="zh-editorial-cover-copy"><span>{index} / EDITORIAL</span><p>{editorial.kind}</p><h1>{editorial.name}</h1></div>
    </section>

    <section className="zh-editorial-lead">
      <p>{chapter}</p>
      <h2>{editorial.lead}</h2>
      <span>{editorial.description}</span>
    </section>

    <section className="zh-editorial-spread">
      <figure className="zh-editorial-spread-main"><img src={assetUrl(editorial.images[1])} alt={`История ${editorial.name}`}/><figcaption>01 / STORY</figcaption></figure>
      <div className="zh-editorial-spread-copy"><span>{index}</span><p>THE STORY</p><h3>{editorial.detail}</h3></div>
    </section>

    {variant==="magazine"&&<section className="zh-editorial-type-page"><span>WORDS / OBJECTS / HOME</span><h2>Красота начинается с паузы между вещами.</h2><p>Редакционная композиция строится как журнальный разворот: крупный текст, свободное поле и один выразительный предмет.</p></section>}

    {variant==="offset"&&<section className="zh-editorial-side-note"><p>02 / TABLE STORY</p><h3>Сервировка не как набор предметов, а как готовая сцена для долгого разговора.</h3></section>}

    <section className="zh-editorial-mosaic">
      <figure className="zh-editorial-mosaic-a"><img src={assetUrl(editorial.images[2])} alt="Деталь коллекции"/><figcaption>DETAIL / 02</figcaption></figure>
      <figure className="zh-editorial-mosaic-b"><img src={assetUrl(editorial.images[3])} alt="Образ коллекции"/><figcaption>ATMOSPHERE / 03</figcaption></figure>
      <div className="zh-editorial-mosaic-copy"><span>03</span><p>OBJECTS IN CONTEXT</p><h3>Вещи раскрываются через масштаб, фактуру и соседство с другими предметами.</h3></div>
    </section>

    <figure className="zh-editorial-full-frame">
      <img src={assetUrl(productImage)} alt={`Предмет из ${editorial.name}`}/>
      <figcaption><span>04</span><p>SHOP THE STORY</p></figcaption>
    </figure>

    {variant==="gallery"&&<section className="zh-editorial-quote"><p>FOLKLORE / NOW</p><h2>Традиция может звучать современно, когда её не копируют буквально.</h2></section>}
    {variant==="cinematic"&&<section className="zh-editorial-quote"><p>NIGHT / LIGHT / TEXTURE</p><h2>Спокойный интерьер строится не из декора, а из света, материалов и ритма.</h2></section>}

    <section className="editorial-products zh-editorial-products">
      <div className="editorial-products-head"><div><p>SHOP THE STORY</p><h2>Предметы {editorial.kind==="КАПСУЛА"?"капсулы":"коллекции"}</h2></div></div>
      <div className="product-grid">{items.map(item=><ProductCard product={item} key={`${editorial.id}-${item.id}`} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
    </section>
  </div>;
}'''

# Replace only EditorialView. Keep LookbookViewer because PDP rich-content still uses it.
text, count = re.subn(
    r'function EditorialView\([\s\S]*?\n\}(?=\n\nfunction LookbookViewer)',
    editorial_view,
    text,
    count=1,
    flags=re.S
)
if count != 1 and 'editorial-page zara-editorial' not in text:
    raise SystemExit(f"EditorialView restore failed: {count}")

path.write_text(text, encoding="utf-8")
print("Restored original combined collections and capsules experience")
