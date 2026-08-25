from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

start = page.find("function HomeView(")
end = page.find("function CatalogView(", start)
if start < 0 or end < 0:
    raise SystemExit("V45 HomeView anchors not found")

home = r'''function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_SKETCH_ZARA_KULTURA_V45
  const heroSlides=[
    {label:"КАПСУЛА",title:"Лунная сказка",subtitle:"Тихая история для спальни и позднего чаепития",desktopImage:"/images/editorial/caps_luna_postel2.png",mobileImage:"/images/editorial/caps_luna_postel.png",cta:"Смотреть коллекцию",action:()=>openEditorial(editorials[1])},
    {label:"КОЛЛЕКЦИЯ",title:"Ледяные узоры",subtitle:"Светлая зимняя палитра, вышивка и мягкие фактуры",desktopImage:"/images/editorial/caps_led.png",mobileImage:"/images/editorial/caps_led_podyshka.png",cta:"Смотреть коллекцию",action:()=>openEditorial(editorials[0])},
    {label:"ПОСУДА И СЕРВИРОВКА",title:"Дом начинается с ритуалов",subtitle:"Фарфор, текстиль и предметы для красивой повседневности",desktopImage:"/images/time-table.png",mobileImage:"/images/russian-service-blue.png",cta:"Смотреть каталог",action:()=>openCatalog("Посуда и сервировка")},
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const [paused,setPaused]=useState(false);
  const touchStart=useRef<number|null>(null);
  useEffect(()=>{
    if(paused||typeof window==="undefined"||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),7000);
    return()=>window.clearInterval(timer);
  },[activeIndex,paused,setSlide,heroSlides.length]);
  const shift=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);

  const categories=[
    {title:"Постельное бельё",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Пледы",image:"/images/products/KD-PD-2003-BLUE01.png",category:"Пледы и подушки"},
    {title:"Подушки",image:"/images/products/KD-PD-2000-WHITE01.png",category:"Пледы и подушки"},
    {title:"Посуда",image:"/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {title:"Сервировка",image:"/images/time-table.png",category:"Посуда и сервировка"},
    {title:"Декор",image:"/images/beige-bedroom.png",category:"Все товары"},
  ];
  const newProducts=[2000,2004,2010,2003,4,10,5,6].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const collection=editorials[1]??editorials[0];
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;
  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/images/constructor/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/images/constructor/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/images/products/KD-PD-2000-WHITE01.png",href:`${constructorHref}table-7/`},
  ];

  return <main className="home-sketch-v45">
    <section className="hs45-hero" aria-label="Главный баннер"
      onPointerEnter={()=>setPaused(true)} onPointerLeave={()=>setPaused(false)}
      onTouchStart={event=>{touchStart.current=event.touches[0]?.clientX??null;setPaused(true)}}
      onTouchEnd={event=>{const start=touchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shift(end<start?1:-1);touchStart.current=null;setPaused(false)}}>
      <picture><source media="(max-width:700px)" srcSet={assetUrl(hero.mobileImage)}/><img src={assetUrl(hero.desktopImage)} alt={hero.title}/></picture>
      <div className="hs45-hero-overlay"/>
      <div className="hs45-hero-copy"><small>{hero.label}</small><h1>{hero.title}</h1><p>{hero.subtitle}</p><button type="button" onClick={hero.action}>{hero.cta}</button></div>
      <div className="hs45-hero-nav"><div>{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===activeIndex?"active":""} onClick={()=>setSlide(index)} aria-label={item.title}/>)}</div><span><button type="button" onClick={()=>shift(-1)} aria-label="Назад">←</button><button type="button" onClick={()=>shift(1)} aria-label="Вперёд">→</button></span></div>
    </section>

    <section className="hs45-categories hs45-shell" aria-labelledby="hs45-categories-title">
      <header className="hs45-head"><div><small>КАТАЛОГ</small><h2 id="hs45-categories-title">Категории</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>Весь каталог →</button></header>
      <div className="hs45-category-row">{categories.map(item=><button type="button" key={item.title} onClick={()=>openCatalog(item.category)}><span><img src={assetUrl(item.image)} alt={item.title}/></span><strong>{item.title}</strong></button>)}</div>
    </section>

    <section className="hs45-new hs45-shell" aria-labelledby="hs45-new-title">
      <header className="hs45-head"><div><small>НОВИНКИ</small><h2 id="hs45-new-title">Новое поступление</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>Смотреть всё →</button></header>
      <div className="hs45-product-grid">{newProducts.slice(0,4).map(product=><ProductCard key={`home-v45-${product.id}`} product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>
    </section>

    {collection&&<section className="hs45-collection" aria-labelledby="hs45-collection-title">
      <button type="button" className="hs45-collection-media" onClick={()=>openEditorial(collection)}><img src={assetUrl(collection.images[0])} alt={collection.name}/></button>
      <div className="hs45-collection-copy"><small>{collection.kind}</small><h2 id="hs45-collection-title">{collection.name}</h2><p>{collection.lead}</p><button type="button" onClick={()=>openEditorial(collection)}>Смотреть коллекцию →</button></div>
    </section>}

    <section className="hs45-solutions hs45-shell" aria-labelledby="hs45-solutions-title">
      <header className="hs45-head"><div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2 id="hs45-solutions-title">Пространства, собранные за вас</h2></div><a href={constructorHref}>Все решения →</a></header>
      <div className="hs45-solution-grid">{solutions.map(item=><a href={item.href} key={item.title}><span className="hs45-solution-media"><img src={assetUrl(item.image)} alt={item.title}/></span><span className="hs45-solution-copy"><small>{item.room}</small><strong>{item.title}</strong><em>Собрать решение →</em></span></a>)}</div>
    </section>

    <section className="hs45-boutiques-intro hs45-shell"><small>БУТИКИ</small><h2>Культура Дома рядом</h2><p>Посмотрите материалы, оттенки и фактуры вживую.</p></section>
    <HomeBoutiques/>
  </main>;
}
'''

page = page[:start] + home + "\n\n" + page[end:]
page_path.write_text(page, encoding="utf-8")
print("Applied sketch-aligned adaptive homepage V45")
