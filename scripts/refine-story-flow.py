from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

def sub_once(pattern: str, replacement: str, value: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, value, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return updated

text = text.replace(
    'type View = "home" | "catalog" | "collections" | "editorial" | "product";',
    'type View = "home" | "catalog" | "collections" | "capsules" | "editorial" | "product";'
)

old_routes = '''      {view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}
      {view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}'''
new_routes = '''      {view === "collections" && <CollectionsView mode="collections" openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}
      {view === "capsules" && <CollectionsView mode="capsules" openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}
      {view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}'''
if old_routes in text:
    text = text.replace(old_routes, new_routes)

old_home_editorial = '''    <section className="editorial"><img src={assetUrl("/images/time-hero.png")} alt="Капсула Нити времени"/><div><p>НОВАЯ КАПСУЛА</p><h2>Нити времени</h2><span>Вдохновлена движением звёзд<br/>и бесконечной красотой ночного неба.</span><button onClick={() => go("collections")}>ОТКРЫТЬ ИСТОРИЮ →</button></div></section>'''
new_home_editorial = '''    <section className="home-story-gateway">
      <div className="home-story-heading"><p>STORIES / LOOKBOOK</p><h2>Дом как журнал</h2><span>Коллекции — для выбора предметов. Капсулы — для настроения, образов и готовых интерьерных историй.</span></div>
      <div className="home-story-grid">
        <article className="home-story-card home-story-primary">
          <button className="home-story-media" onClick={()=>go("capsules")}><img src={assetUrl("/images/time-hero.png")} alt="Капсулы и editorial"/><span>01 / CAPSULES</span></button>
          <div><p>EDITORIAL CAPSULES</p><h3>Нити времени</h3><span>Короткие главы, визуальные истории и lookbook без перегрузки основного shopping-flow.</span><button onClick={()=>go("capsules")}>СМОТРЕТЬ КАПСУЛЫ →</button></div>
        </article>
        <article className="home-story-card home-story-secondary">
          <button className="home-story-media" onClick={()=>go("collections")}><img src={assetUrl("/images/poetry-editorial.png")} alt="Коллекции Культура дома"/><span>02 / COLLECTIONS</span></button>
          <div><p>COLLECTION INDEX</p><h3>Коллекции</h3><span>Отдельные страницы коллекций с товарами, историей и опциональным lookbook.</span><button onClick={()=>go("collections")}>СМОТРЕТЬ КОЛЛЕКЦИИ →</button></div>
        </article>
      </div>
    </section>'''
if old_home_editorial in text:
    text = text.replace(old_home_editorial, new_home_editorial)

text = text.replace(
    '<button className="menu-feature" onClick={()=>go("collections")}>КАПСУЛЫ И КОЛЛЕКЦИИ</button>',
    '<button className="menu-feature" onClick={()=>go("collections")}>КОЛЛЕКЦИИ</button><button className="menu-feature" onClick={()=>go("capsules")}>КАПСУЛЫ & STORIES</button>'
)
text = text.replace(
    '<button onClick={()=>go("collections")}>EDITORIAL</button>',
    '<button onClick={()=>go("capsules")}>EDITORIAL / LOOKBOOK</button>'
)

collections_fn = r'''function CollectionsView({ openEditorial, mode }: { openEditorial:(editorial:Editorial)=>void; mode:"collections"|"capsules" }) {
  const visible=editorials.filter(item=>mode==="capsules"?item.kind==="КАПСУЛА":item.kind==="КОЛЛЕКЦИЯ");
  const hero=visible[0];
  const secondary=visible[1]??visible[0];
  const collectionMode=mode==="collections";
  return <div className={`story-index page story-index-${mode}`}>
    <section className="story-index-hero">
      <button className="story-index-hero-media" onClick={()=>openEditorial(hero)}>
        <img src={assetUrl(hero.images[0])} alt={hero.name}/>
        <span>{collectionMode?"COLLECTION INDEX":"EDITORIAL CAPSULES"} / 01</span>
      </button>
      <div className="story-index-hero-copy">
        <p>{collectionMode?"КОЛЛЕКЦИИ":"КАПСУЛЫ & STORIES"}</p>
        <h1>{collectionMode?"Предметы, собранные в истории":"Короткие истории для дома"}</h1>
        <span>{collectionMode?"Каждая коллекция получила собственную страницу: сначала образ и товары, а журнальный контент открывается отдельно.":"Editorial-капсулы работают как вдохновение: образы, сцены и lookbook доступны по желанию и не удлиняют основной путь."}</span>
        <button onClick={()=>openEditorial(hero)}>ОТКРЫТЬ {hero.name.toUpperCase()} →</button>
      </div>
    </section>

    <section className="story-index-intro">
      <p>{collectionMode?"COLLECTION DIRECTORY":"EDITORIAL DIRECTORY"}</p>
      <div><h2>{collectionMode?"Все коллекции":"Капсулы и визуальные истории"}</h2><span>{collectionMode?"Выберите коллекцию, посмотрите ключевые предметы и при желании откройте lookbook.":"Каждая карточка ведёт на короткую страницу капсулы; полный журнал открывается отдельным экраном."}</span></div>
    </section>

    <section className="story-index-grid">
      {visible.map((item,index)=><article className={`story-index-card story-card-${index%3}`} key={item.id}>
        <button className="story-card-media" onClick={()=>openEditorial(item)}>
          <img src={assetUrl(item.images[(index+1)%item.images.length])} alt={item.name}/>
          <span>{String(index+1).padStart(2,"0")} / {item.kind}</span>
        </button>
        <div className="story-card-copy">
          <p>{item.kind}</p><h2>{item.name}</h2><span>{item.description}</span>
          <div><button onClick={()=>openEditorial(item)}>ОТКРЫТЬ СТРАНИЦУ →</button><button onClick={()=>openEditorial(item)}>LOOKBOOK</button></div>
        </div>
      </article>)}
    </section>

    <section className="story-index-feature">
      <button onClick={()=>openEditorial(secondary)}><img src={assetUrl(secondary.images[3])} alt={secondary.name}/><span>LOOKBOOK / {secondary.name}</span></button>
      <div><p>SHOP THE STORY</p><h2>{collectionMode?"Сначала предметы — потом история":"Не листать длинную статью, а открыть журнал тогда, когда хочется"}</h2><span>{collectionMode?"Страница коллекции остаётся коммерческой и компактной: образ, товары, детали и отдельный вход в editorial.":"На мобильном lookbook перелистывается горизонтально по главам и не увеличивает длину страницы."}</span></div>
    </section>
  </div>;
}'''

text = sub_once(
    r'function CollectionsView\([\s\S]*?\n}\n\nfunction EditorialView',
    collections_fn + '\n\nfunction EditorialView',
    text,
    "CollectionsView"
)

editorial_and_lookbook = r'''function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {
  const [lookbookOpen,setLookbookOpen]=useState(false);
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const isCapsule=editorial.kind==="КАПСУЛА";
  const eyebrow=isCapsule?"EDITORIAL CAPSULE":"COLLECTION";
  return <div className={`story-detail page story-detail-${isCapsule?"capsule":"collection"}`}>
    <section className="story-detail-hero">
      <img src={assetUrl(editorial.images[0])} alt={editorial.name}/>
      <div className="story-detail-copy"><p>{eyebrow}</p><h1>{editorial.name}</h1><span>{editorial.lead}</span><div><button className="primary story-open-lookbook" onClick={()=>setLookbookOpen(true)}>ОТКРЫТЬ LOOKBOOK</button><button className="story-scroll-products" onClick={()=>document.querySelector(".story-detail-products")?.scrollIntoView({behavior:"smooth"})}>СМОТРЕТЬ ПРЕДМЕТЫ ↓</button></div></div>
    </section>

    <section className="story-detail-summary">
      <div className="story-detail-summary-copy"><p>THE STORY / SHORT READ</p><h2>{editorial.description}</h2><span>{editorial.detail}</span><button onClick={()=>setLookbookOpen(true)}>ЧИТАТЬ КАК ЖУРНАЛ →</button></div>
      <button className="story-detail-summary-media" onClick={()=>setLookbookOpen(true)}><img src={assetUrl(editorial.images[1])} alt={`Lookbook ${editorial.name}`}/><span>OPEN LOOKBOOK</span></button>
    </section>

    <section className="story-detail-products">
      <div className="story-detail-products-head"><div><p>SHOP THE STORY</p><h2>Предметы {isCapsule?"капсулы":"коллекции"}</h2></div><span>{items.length} предмета</span></div>
      <ProductRail className="story-product-rail" items={items} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="story-lookbook-teaser">
      <button onClick={()=>setLookbookOpen(true)}><img src={assetUrl(editorial.images[2])} alt="Открыть визуальную главу"/><span>01 / MATERIALS</span></button>
      <button onClick={()=>setLookbookOpen(true)}><img src={assetUrl(editorial.images[3])} alt="Открыть интерьерную главу"/><span>02 / ATMOSPHERE</span></button>
      <div><p>DIGITAL LOOKBOOK</p><h2>Пять коротких глав вместо длинной страницы</h2><span>На desktop — полноэкранный журнальный разворот. На mobile — свайп по экранным главам с отдельным shoppable-финалом.</span><button onClick={()=>setLookbookOpen(true)}>ОТКРЫТЬ ЖУРНАЛ →</button></div>
    </section>

    {lookbookOpen&&<LookbookViewer editorial={editorial} items={items} close={()=>setLookbookOpen(false)} selectProduct={selectProduct}/>} 
  </div>;
}

function LookbookViewer({editorial,items,close,selectProduct}:{editorial:Editorial;items:Product[];close:()=>void;selectProduct?:(product:Product)=>void}){
  const [chapter,setChapter]=useState(0);
  const chapterLabels=["COVER","STORY","DETAILS","NOTE","SHOP"];
  useEffect(()=>{
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")close()};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  },[close]);
  const goChapter=(index:number)=>{
    setChapter(index);
    document.getElementById(`lookbook-${editorial.id}-${index}`)?.scrollIntoView({behavior:"smooth",block:"nearest",inline:"start"});
  };
  return <div className="lookbook-overlay" role="dialog" aria-modal="true" aria-label={`Lookbook ${editorial.name}`}>
    <button className="lookbook-backdrop" onClick={close} aria-label="Закрыть lookbook"/>
    <section className="lookbook-shell">
      <header className="lookbook-header"><div><span>{editorial.kind}</span><b>{editorial.name}</b></div><nav>{chapterLabels.map((label,index)=><button key={label} className={chapter===index?"active":""} onClick={()=>goChapter(index)}>{String(index+1).padStart(2,"0")} {label}</button>)}</nav><button className="lookbook-close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="lookbook-track">
        <article id={`lookbook-${editorial.id}-0`} className="lookbook-page lookbook-cover-page">
          <img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><p>01 / COVER</p><h2>{editorial.name}</h2><span>{editorial.lead}</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-1`} className="lookbook-page lookbook-story-page">
          <figure><img src={assetUrl(editorial.images[1])} alt="История коллекции"/><figcaption>PHOTOGRAPHY / STORY</figcaption></figure><div><p>02 / THE STORY</p><h2>{editorial.description}</h2><span>{editorial.detail}</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-2`} className="lookbook-page lookbook-details-page">
          <figure><img src={assetUrl(editorial.images[2])} alt="Детали коллекции"/></figure><figure><img src={assetUrl(editorial.images[3])} alt="Атмосфера коллекции"/></figure><div><p>03 / DETAILS</p><h2>Материал, свет и масштаб</h2><span>Вместо длинного текста — два визуальных кадра и короткая редакционная заметка.</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-3`} className="lookbook-page lookbook-note-page">
          <div><p>04 / EDITOR'S NOTE</p><h2>{editorial.id==="time"?"Тишина — тоже часть интерьера.":editorial.id==="buyan"?"Сервировка начинается с атмосферы.":editorial.id==="poetry"?"Дом хранит смысл в мелочах.":"Традиция становится современной, когда остаётся живой."}</h2><span>{editorial.lead}</span></div><img src={assetUrl(editorial.images[0])} alt="Редакционный кадр"/>
        </article>
        <article id={`lookbook-${editorial.id}-4`} className="lookbook-page lookbook-shop-page">
          <div className="lookbook-shop-head"><p>05 / SHOP THE STORY</p><h2>Предметы из истории</h2></div>
          <div className="lookbook-shop-grid">{items.map(item=><button key={item.id} onClick={()=>{close();selectProduct?.(item)}}><img src={assetUrl(item.image)} alt={item.name}/><span>{item.name}<b>{fmt(item.price)}</b></span></button>)}</div>
        </article>
      </div>
      <div className="lookbook-mobile-progress">{chapterLabels.map((_,index)=><button key={index} className={chapter===index?"active":""} onClick={()=>goChapter(index)} aria-label={`Глава ${index+1}`}/>)}</div>
    </section>
  </div>;
}'''

text = sub_once(
    r'function EditorialView\([\s\S]*?\n}\n\nfunction QuantityControl',
    editorial_and_lookbook + '\n\nfunction QuantityControl',
    text,
    "EditorialView"
)

rich_fn = r'''function RichContent({product,selectProduct}:{product:Product;selectProduct:(product:Product)=>void}){
  const [lookbookOpen,setLookbookOpen]=useState(false);
  const related=product.id===4?editorials.find(item=>item.id==="time"):editorials.find(item=>item.productIds.includes(product.id)&&item.kind==="КОЛЛЕКЦИЯ");
  if(!related)return null;
  const items=related.productIds.map(id=>products.find(item=>item.id===id)!).filter(Boolean);
  return <section className="pdp-story-entry">
    <button className="pdp-story-entry-media" onClick={()=>setLookbookOpen(true)}><img src={assetUrl(related.images[1])} alt={`История ${related.name}`}/><span>EDITORIAL / LOOKBOOK</span></button>
    <div className="pdp-story-entry-copy"><p>{related.kind}</p><h2>История «{related.name}»</h2><span>{related.description}</span><button onClick={()=>setLookbookOpen(true)}>СМОТРЕТЬ LOOKBOOK →</button></div>
    {lookbookOpen&&<LookbookViewer editorial={related} items={items} close={()=>setLookbookOpen(false)} selectProduct={selectProduct}/>} 
  </section>;
}'''

text = sub_once(
    r'function RichContent\([\s\S]*?\n}\n\nfunction ProductRecommendations',
    rich_fn + '\n\nfunction ProductRecommendations',
    text,
    "RichContent"
)

text = text.replace(
    '{product.hasRichContent&&<RichContent product={product}/>}<ProductRecommendations',
    '{product.hasRichContent&&<RichContent product={product} selectProduct={selectProduct}/>}<ProductRecommendations'
)

path.write_text(text, encoding="utf-8")
print("Refined collection, capsule, PDP editorial and lookbook flows.")
