from pathlib import Path
import re

path = Path("app/page.tsx")
source = path.read_text()

rich_content = r'''function RichContent({product}:{product:Product}){
  const night=product.id===4;
  const story=night?{
    eyebrow:"КАПСУЛА 04 · НИТИ ВРЕМЕНИ",
    title:"Дом, в котором вечер становится тише",
    intro:"Глубокий синий, мягкий свет и вышивка, напоминающая созвездия. История о спокойных ритуалах и вещах, которые остаются надолго.",
    hero:"/images/time-hero.png",
    portrait:"/images/night-editorial.png",
    detail:"/images/blue-bedroom.png",
    still:"/images/moon-plate.png",
    chapter:"СВЕТ И ТИШИНА",
    statement:"Тактильность важнее декора. Материал, свет и ритм пространства создают ощущение дома без лишних деталей.",
    caption:"Нити времени · ночная глава",
    quote:"Красота раскрывается не сразу — она живёт в фактуре, тени и прикосновении.",
    material:"САТИН",
    craft:"ВЫШИВКА",
    palette:"НОЧНОЙ СИНИЙ"
  }:{
    eyebrow:"КОЛЛЕКЦИЯ · РУССКИЙ УЗОР",
    title:"Орнамент как часть современной повседневности",
    intro:"Спокойная палитра, натуральные ткани и мотивы, знакомые по старым вышивкам. Не реконструкция прошлого, а лёгкое современное прочтение.",
    hero:"/images/russian-bedroom.png",
    portrait:"/images/poetry-editorial.png",
    detail:"/images/beige-bedroom.png",
    still:"/images/classic-bedroom.png",
    chapter:"НОВАЯ ТРАДИЦИЯ",
    statement:"Мы оставили орнамент главным акцентом, а всё остальное сделали тише: естественные оттенки, мягкий лён и много воздуха.",
    caption:"Русский узор · современная глава",
    quote:"Предмет становится личным, когда в нём есть память, но он остаётся свободным от буквального цитирования прошлого.",
    material:"ЛЁН И ХЛОПОК",
    craft:"ВЫШИВКА",
    palette:"МОЛОЧНЫЙ · ПЕСОЧНЫЙ"
  };
  return <section className={`rich-content rich-zara-story ${night?"rich-zara-night":"rich-zara-russian"}`}>
    <header className="zh-rich-intro">
      <p>{story.eyebrow}</p>
      <h2>{story.title}</h2>
      <span>{story.intro}</span>
    </header>

    <figure className="zh-rich-hero">
      <img src={assetUrl(story.hero)} alt={story.title}/>
      <figcaption>{story.caption}</figcaption>
    </figure>

    <section className="zh-rich-manifesto">
      <span>01</span>
      <div><p>{story.chapter}</p><h3>{story.statement}</h3></div>
    </section>

    <section className="zh-rich-asym">
      <figure className="zh-rich-tall"><img src={assetUrl(story.portrait)} alt="Атмосфера коллекции"/><figcaption>ATMOSPHERE / 01</figcaption></figure>
      <div className="zh-rich-copy"><span>02</span><p>ДЕТАЛИ</p><h3>{story.quote}</h3><small>Материалы и оттенки подобраны так, чтобы предметы легко сочетались между собой и оставались визуально спокойными.</small></div>
      <figure className="zh-rich-small"><img src={assetUrl(story.detail)} alt="Фактура и детали"/><figcaption>DETAIL / 02</figcaption></figure>
    </section>

    <figure className="zh-rich-wide-detail">
      <img src={assetUrl(story.still)} alt="Предметы коллекции в интерьере"/>
      <figcaption><span>03</span><p>Дом как редакционная история: предметы раскрываются через свет, масштаб и окружение.</p></figcaption>
    </figure>

    <section className="zh-rich-materials">
      <div><small>МАТЕРИАЛ</small><strong>{story.material}</strong></div>
      <div><small>ТЕХНИКА</small><strong>{story.craft}</strong></div>
      <div><small>ПАЛИТРА</small><strong>{story.palette}</strong></div>
    </section>

    <section className="zh-rich-closing"><p>04 · MADE FOR EVERYDAY RITUALS</p><h3>Предметы, которые не требуют особого случая.</h3></section>
  </section>;
}'''

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

source, rich_count = re.subn(r'function RichContent\(\{product\}:\{product:Product\}\)\{.*?\n\}(?=\n\nfunction ProductRecommendations)', rich_content, source, count=1, flags=re.S)
if rich_count != 1:
    raise SystemExit(f"RichContent replacement failed: {rich_count}")

source, editorial_count = re.subn(r'function EditorialView\(\{ editorial, selectProduct, favorite, favorites \}: \{ editorial:Editorial; selectProduct:\(product:Product\)=>void; favorite:\(id:number\)=>void; favorites:number\[\] \}\) \{.*?\n\}(?=\n\nfunction QuantityControl)', editorial_view, source, count=1, flags=re.S)
if editorial_count != 1:
    raise SystemExit(f"EditorialView replacement failed: {editorial_count}")

path.write_text(source)
print("Upgraded rich content and editorial storytelling")
