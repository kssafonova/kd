from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

start = page.find("function HomeView(")
end = page.find("function CatalogView(", start)
if start < 0 or end < 0:
    raise SystemExit("V44 HomeView anchors not found")

home = r'''function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_ZARA_KULTURA_V44
  const heroSlides=[
    {
      label:"КАПСУЛА",
      title:"Лунная сказка",
      text:"Ночная палитра, сатин и глубокий синий — спокойная история для спальни и позднего чаепития.",
      desktopImage:"/assets/images/caps_luna_postel2.png",
      mobileImage:"/assets/images/caps_luna_postel.png",
      cta:"Смотреть историю",
      action:()=>openEditorial(editorials[1]),
    },
    {
      label:"КОЛЛЕКЦИЯ",
      title:"Ледяные узоры",
      text:"Морозный свет, белый и ледяной голубой. Текстиль и предметы, собранные в одну тихую зимнюю композицию.",
      desktopImage:"/assets/images/caps_led.png",
      mobileImage:"/assets/images/caps_led_podyshka.png",
      cta:"Открыть коллекцию",
      action:()=>openEditorial(editorials[0]),
    },
    {
      label:"КУХНЯ И СТОЛОВАЯ",
      title:"Сервировка как часть интерьера",
      text:"Фарфор, текстиль и детали для стола — не отдельные предметы, а единая домашняя сцена.",
      desktopImage:"/assets/images/time-table.png",
      mobileImage:"/assets/images/russian-service-blue.png",
      cta:"Смотреть посуду",
      action:()=>openCatalog("Посуда и сервировка"),
    },
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const [heroPaused,setHeroPaused]=useState(false);
  const [brandPlaying,setBrandPlaying]=useState(true);
  const heroTouchStart=useRef<number|null>(null);
  const brandVideoRef=useRef<HTMLVideoElement>(null);

  useEffect(()=>{
    if(heroPaused||typeof window==="undefined"||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),7600);
    return()=>window.clearInterval(timer);
  },[activeIndex,heroPaused,setSlide,heroSlides.length]);

  const shiftHero=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);
  const toggleBrandVideo=()=>{
    const video=brandVideoRef.current;
    if(!video)return;
    if(video.paused){void video.play();setBrandPlaying(true)}
    else{video.pause();setBrandPlaying(false)}
  };

  const newProducts=[2000,2004,2010,2003,4,10,5,6].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const stories:Editorial[]=[editorials[1],editorials[0]].filter((item):item is Editorial=>Boolean(item));
  const categories=[
    {eyebrow:"СПАЛЬНЯ",title:"Постельное бельё",image:"/assets/images/blue-bedroom.png",category:"Постельное бельё"},
    {eyebrow:"КУХНЯ И СТОЛОВАЯ",title:"Посуда и сервировка",image:"/assets/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {eyebrow:"ТЕКСТИЛЬ И ДЕКОР",title:"Пледы и подушки",image:"/assets/images/beige-bedroom.png",category:"Пледы и подушки"},
  ];
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;
  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/assets/images/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/assets/images/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/assets/images/caps_led.png",href:`${constructorHref}table-7/`},
  ];

  return <main className="home-zara-v44">
    <nav className="zh44-topnav" aria-label="Разделы главной">
      <button type="button" onClick={()=>openCatalog("Все товары")}>Новинки</button>
      <button type="button" onClick={()=>openCatalog("Постельное бельё")}>Спальня</button>
      <button type="button" onClick={()=>openCatalog("Посуда и сервировка")}>Кухня и столовая</button>
      <button type="button" onClick={()=>openCatalog("Пледы и подушки")}>Декор</button>
      <button type="button" onClick={()=>go("collections")}>Капсулы и коллекции</button>
      <a href={constructorHref}>Готовые решения</a>
    </nav>

    <section className="zh44-hero" aria-label="Главная история"
      onPointerEnter={()=>setHeroPaused(true)} onPointerLeave={()=>setHeroPaused(false)}
      onFocusCapture={()=>setHeroPaused(true)} onBlurCapture={()=>setHeroPaused(false)}
      onTouchStart={event=>{heroTouchStart.current=event.touches[0]?.clientX??null;setHeroPaused(true)}}
      onTouchEnd={event=>{const start=heroTouchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shiftHero(end<start?1:-1);heroTouchStart.current=null;setHeroPaused(false)}}>
      <picture className="zh44-hero-media">
        <source media="(max-width: 700px)" srcSet={assetUrl(hero.mobileImage)}/>
        <img src={assetUrl(hero.desktopImage)} alt={hero.title}/>
      </picture>
      <div className="zh44-hero-copy" aria-live="polite">
        <small className="zh44-kicker">{hero.label}</small>
        <h1>{hero.title}</h1>
        <p>{hero.text}</p>
        <div className="zh44-hero-actions">
          <button type="button" onClick={hero.action}>{hero.cta}<Icon name="arrow"/></button>
          <button type="button" onClick={()=>openCatalog("Все товары")}>Новинки</button>
        </div>
      </div>
      <div className="zh44-hero-controls">
        <div className="zh44-hero-dots" aria-label="Истории на главной">{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===activeIndex?"active":""} aria-label={item.title} aria-current={index===activeIndex?"true":undefined} onClick={()=>setSlide(index)}/>)}</div>
        <div className="zh44-hero-arrows"><button type="button" aria-label="Предыдущая история" onClick={()=>shiftHero(-1)}><Icon name="arrow"/></button><button type="button" aria-label="Следующая история" onClick={()=>shiftHero(1)}><Icon name="arrow"/></button></div>
      </div>
    </section>

    <section className="zh44-new zh44-section">
      <div className="zh44-shell">
        <header className="zh44-section-head"><div><small className="zh44-kicker">НОВОЕ ПОСТУПЛЕНИЕ</small><h2 className="zh44-title">Новые предметы</h2><p>Текстиль, фарфор и детали для дома — единая спокойная подборка без лишней витринной перегрузки.</p></div><button className="zh44-link" type="button" onClick={()=>openCatalog("Все товары")}>Смотреть всё <Icon name="arrow"/></button></header>
        <ProductRail className="zh44-product-grid" items={newProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
      </div>
    </section>

    <section className="zh44-editorials" aria-label="Капсулы и коллекции">
      <div className="zh44-editorial-grid">{stories.map(item=><button className="zh44-editorial-card" type="button" key={item.id} onClick={()=>openEditorial(item)}>
        <img src={assetUrl(item.images[0])} alt={item.name}/>
        <span className="zh44-editorial-copy"><small>{item.kind}</small><h2>{item.name}</h2><p>{item.lead}</p><span>Смотреть историю</span></span>
      </button>)}</div>
    </section>

    <section className="zh44-categories zh44-section">
      <div className="zh44-shell">
        <header className="zh44-section-head"><div><small className="zh44-kicker">ДОМ ПО ПРОСТРАНСТВАМ</small><h2 className="zh44-title">Выберите комнату</h2><p>Три ключевых раздела прототипа — только те категории, в которых уже есть полноценный ассортимент и работающий товарный сценарий.</p></div></header>
        <div className="zh44-category-grid">{categories.map(item=><button className="zh44-category-card" type="button" key={item.title} onClick={()=>openCatalog(item.category)}><span className="zh44-category-media"><img src={assetUrl(item.image)} alt={item.title}/></span><span className="zh44-category-copy"><span><small>{item.eyebrow}</small><strong>{item.title}</strong></span><span>Смотреть</span></span></button>)}</div>
      </div>
    </section>

    <section className="zh44-film" aria-label="История бренда">
      <video ref={brandVideoRef} autoPlay loop muted playsInline preload="metadata" poster={assetUrl("/assets/images/russian-bedroom.png")} onPlay={()=>setBrandPlaying(true)} onPause={()=>setBrandPlaying(false)}>
        <source media="(max-width: 700px)" src={assetUrl("/videos/home-mobile.mp4")} type="video/mp4"/>
        <source src={assetUrl("/videos/home-desktop.mp4")} type="video/mp4"/>
      </video>
      <div className="zh44-film-copy"><small>КУЛЬТУРА ДОМА</small><h2>Традиции в каждом доме</h2><p>Современный взгляд на русскую культуру дома: тишина материалов, ритуалы сервировки и вещи, которые живут рядом годами.</p><button className="zh44-film-toggle" type="button" onClick={toggleBrandVideo}>{brandPlaying?"Пауза":"Смотреть"}</button></div>
    </section>

    <section className="zh44-solutions zh44-section">
      <div className="zh44-shell">
        <header className="zh44-section-head"><div><small className="zh44-kicker">ГОТОВЫЕ РЕШЕНИЯ</small><h2 className="zh44-title">Дом, собранный в единую историю</h2><p>Готовые сочетания предметов из нескольких коллекций. Внутри можно изменить состав, цвет, размер и количество.</p></div><a className="zh44-link" href={constructorHref}>Все решения <Icon name="arrow"/></a></header>
        <div className="zh44-solution-grid">{solutions.map(item=><a className="zh44-solution-card" href={item.href} key={item.title}><span className="zh44-solution-media"><img src={assetUrl(item.image)} alt={item.title}/></span><span className="zh44-solution-copy"><span><small>{item.room}</small><strong>{item.title}</strong></span><span>Настроить</span></span></a>)}</div>
      </div>
    </section>

    <HomeBoutiques/>
  </main>;
}
'''

page = page[:start] + home + "\n\n" + page[end:]
page_path.write_text(page, encoding="utf-8")
print("Applied Zara Home inspired adaptive homepage V44")
