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
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;
  const heroSlides=[
    {
      label:"НОВАЯ ИСТОРИЯ",
      title:"Лунная сказка",
      text:"Ночная палитра, мягкий сатин и глубокий синий — спокойный дом, собранный как единая история.",
      desktopImage:"/assets/images/caps_luna_postel2.png",
      mobileImage:"/assets/images/caps_luna_postel.png",
      cta:"Смотреть капсулу",
      action:()=>openEditorial(editorials[1]),
    },
    {
      label:"КОЛЛЕКЦИЯ",
      title:"Ледяные узоры",
      text:"Белый, ледяной голубой и деликатная вышивка — предметы для тихой современной спальни.",
      desktopImage:"/assets/images/caps_led.png",
      mobileImage:"/assets/images/caps_led_podyshka.png",
      cta:"Смотреть коллекцию",
      action:()=>openEditorial(editorials[0]),
    },
    {
      label:"КУХНЯ И СТОЛОВАЯ",
      title:"Сервировка как часть дома",
      text:"Фарфор, текстиль и детали для стола, которые работают вместе, а не как отдельные предметы.",
      desktopImage:"/assets/images/time-table.png",
      mobileImage:"/assets/images/russian-service-blue.png",
      cta:"Смотреть посуду",
      action:()=>openCatalog("Посуда и сервировка"),
    },
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const [heroPaused,setHeroPaused]=useState(false);
  const heroTouchStart=useRef<number|null>(null);

  useEffect(()=>{
    if(heroPaused||typeof window==="undefined"||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),7600);
    return()=>window.clearInterval(timer);
  },[activeIndex,heroPaused,setSlide,heroSlides.length]);

  const shiftHero=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);
  const categories=[
    {title:"Новинки",meta:"СЕЙЧАС",image:"/assets/images/KD-PD-2000-WHITE01.png",action:()=>openCatalog("Все товары")},
    {title:"Постельное бельё",meta:"СПАЛЬНЯ",image:"/assets/images/blue-bedroom.png",action:()=>openCatalog("Постельное бельё")},
    {title:"Пледы и подушки",meta:"ТЕКСТИЛЬ",image:"/assets/images/sky-bolster.png",action:()=>openCatalog("Пледы и подушки")},
    {title:"Посуда и сервировка",meta:"СТОЛОВАЯ",image:"/assets/images/russian-service-blue.png",action:()=>openCatalog("Посуда и сервировка")},
    {title:"Капсулы",meta:"ИСТОРИИ",image:"/assets/images/caps_luna_serviz.png",action:()=>go("collections")},
    {title:"Готовые решения",meta:"ПРОСТРАНСТВА",image:"/assets/images/green.jpeg",action:()=>{window.location.href=constructorHref}},
  ];
  const newProducts=[2000,2004,2010].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const featuredCollection=editorials[1]??editorials[0];
  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/assets/images/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/assets/images/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/assets/images/caps_led.png",href:`${constructorHref}table-7/`},
  ];

  return <main className="home-zara-v45">
    <section className="h45-hero" aria-label="Главный баннер"
      onPointerEnter={()=>setHeroPaused(true)} onPointerLeave={()=>setHeroPaused(false)}
      onFocusCapture={()=>setHeroPaused(true)} onBlurCapture={()=>setHeroPaused(false)}
      onTouchStart={event=>{heroTouchStart.current=event.touches[0]?.clientX??null;setHeroPaused(true)}}
      onTouchEnd={event=>{const start=heroTouchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shiftHero(end<start?1:-1);heroTouchStart.current=null;setHeroPaused(false)}}>
      <picture className="h45-hero-media">
        <source media="(max-width: 700px)" srcSet={assetUrl(hero.mobileImage)}/>
        <img src={assetUrl(hero.desktopImage)} alt={hero.title}/>
      </picture>
      <div className="h45-hero-copy" aria-live="polite"><small className="h45-kicker">{hero.label}</small><h1>{hero.title}</h1><p>{hero.text}</p><button type="button" onClick={hero.action}>{hero.cta}<Icon name="arrow"/></button></div>
      <div className="h45-hero-controls"><div className="h45-hero-pages">{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===activeIndex?"active":""} aria-label={item.title} aria-current={index===activeIndex?"true":undefined} onClick={()=>setSlide(index)}/>)}</div><div className="h45-hero-arrows"><button type="button" aria-label="Предыдущий баннер" onClick={()=>shiftHero(-1)}><Icon name="arrow"/></button><button type="button" aria-label="Следующий баннер" onClick={()=>shiftHero(1)}><Icon name="arrow"/></button></div></div>
    </section>

    <section className="h45-categories">
      <div className="h45-shell"><div className="h45-categories-head"><span>Категории</span></div><div className="h45-category-rail">{categories.map(item=><button className="h45-category-card" type="button" key={item.title} onClick={item.action}><span><img src={assetUrl(item.image)} alt={item.title}/></span><strong>{item.title}</strong><small>{item.meta}</small></button>)}</div></div>
    </section>

    <section className="h45-new">
      <div className="h45-shell"><header className="h45-heading"><div><small className="h45-kicker">НОВИНКИ</small><h2>Новое поступление</h2><p>Три предмета крупным планом — меньше шума, больше внимания к материалу, цвету и форме.</p></div><button className="h45-link" type="button" onClick={()=>openCatalog("Все товары")}>Смотреть все <Icon name="arrow"/></button></header><div className="h45-new-grid">{newProducts.map(product=><ProductCard key={`home-v45-${product.id}`} product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div></div>
    </section>

    {featuredCollection&&<section className="h45-collection" aria-label="Коллекция"><button className="h45-collection-card" type="button" onClick={()=>openEditorial(featuredCollection)}><img src={assetUrl(featuredCollection.images[0])} alt={featuredCollection.name}/><span className="h45-collection-copy"><span><small>{featuredCollection.kind}</small><h2>{featuredCollection.name}</h2><p>{featuredCollection.lead}</p></span><span>Смотреть коллекцию</span></span></button></section>}

    <section className="h45-solutions">
      <div className="h45-shell"><header className="h45-heading"><div><small className="h45-kicker">ГОТОВЫЕ РЕШЕНИЯ</small><h2>Соберите пространство целиком</h2><p>Готовые сочетания товаров из нескольких коллекций — состав, цвет, размер и количество можно изменить.</p></div><a className="h45-link" href={constructorHref}>Все решения <Icon name="arrow"/></a></header><div className="h45-solution-grid">{solutions.map(item=><a className="h45-solution-card" href={item.href} key={item.title}><span className="h45-solution-media"><img src={assetUrl(item.image)} alt={item.title}/></span><span className="h45-solution-copy"><span><small>{item.room}</small><strong>{item.title}</strong></span><span>Настроить</span></span></a>)}</div></div>
    </section>

    <HomeBoutiques/>
  </main>;
}
'''

page = page[:start] + home + "\n\n" + page[end:]
page_path.write_text(page, encoding="utf-8")
print("Applied sketch-led adaptive homepage V45")
