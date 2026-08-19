from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

replacement = r'''function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  const heroSlides=[
    {label:"НОВИНКИ",eyebrow:"НОВОЕ · КУЛЬТУРА ДОМА",title:"Новые истории дома",description:"Свежие предметы, текстиль и сервировка — спокойная современная интерпретация русской декоративной традиции.",desktopImage:"/images/time-hero.png",mobileImage:"/images/blue-bedding-vertical.png",action:()=>openCatalog("Все товары")},
    {label:"СПАЛЬНЯ",eyebrow:"СПАЛЬНЯ · НОВЫЙ СЕЗОН",title:"Тихая спальня",description:"Мягкие фактуры, холодный свет и спокойная палитра для пространства, в котором хочется замедлиться.",desktopImage:"/images/blue-bedroom.png",mobileImage:"/images/editorial/caps_luna_postel.png",action:()=>openCatalog("Постельное бельё")},
    {label:"ДЕКОР ДЛЯ ДОМА",eyebrow:"ДЕКОР · ДЕТАЛИ",title:"Дом в деталях",description:"Предметы, которые собирают интерьер: текстиль, посуда и декоративные акценты для ежедневных домашних ритуалов.",desktopImage:"/images/beige-bedroom.png",mobileImage:"/images/russian-bedroom.png",action:()=>openCatalog("Пледы и подушки")},
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];

  useEffect(()=>{
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),6500);
    return()=>window.clearInterval(timer);
  },[activeIndex,setSlide,heroSlides.length]);

  const categories=[
    {title:"Постельное бельё",meta:"СПАЛЬНЯ",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Пледы и подушки",meta:"ТЕКСТИЛЬ",image:"/images/sky-bolster.png",category:"Пледы и подушки"},
    {title:"Посуда и сервировка",meta:"СТОЛОВАЯ",image:"/images/moon-plate.png",category:"Посуда и сервировка"},
    {title:"Столовый текстиль",meta:"СЕРВИРОВКА",image:"/images/editorial-table.webp",category:"Столовый текстиль"},
    {title:"Домашняя одежда",meta:"ДЛЯ ДОМА",image:"/images/classic-bedroom.png",category:"Домашняя одежда"},
    {title:"Декор для дома",meta:"ИНТЕРЬЕР",image:"/images/beige-bedroom.png",category:"Все товары"},
    {title:"Ванная",meta:"ТЕКСТИЛЬ · ДЕТАЛИ",image:"/images/russian-bedroom.png",category:"Все товары"},
    {title:"Подарки",meta:"ИДЕИ ДЛЯ БЛИЗКИХ",image:"/images/time-collection.png",category:"Все товары"},
  ];

  const newProducts=[2000,2004,2010,2003,4,10,5,6].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const capsuleCards=[
    {id:"ice",kind:"КОЛЛЕКЦИЯ",title:"Ледяные узоры",image:"/images/editorial/caps_led_serviz.png"},
    {id:"luna",kind:"КАПСУЛА",title:"Лунная сказка",image:"/images/editorial/caps_luna_postel2.png"},
  ];
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;
  const solutions=[
    {room:"ГОСТИНАЯ",title:"Тихая гостиная",image:"/images/beige-bedroom.png"},
    {room:"СПАЛЬНЯ",title:"Синий бархат ночи",image:"/images/blue-bedroom.png"},
    {room:"КАБИНЕТ",title:"Кабинетное ретро",image:"/images/time-collection.png"},
    {room:"КУХНЯ",title:"Утро в зимнем саду",image:"/images/buyan-editorial.png"},
  ];

  return <main className="home-v4">
    <section className="hv4-hero" aria-label="Главные разделы">
      <picture className="hv4-hero-media">
        <source media="(max-width: 700px)" srcSet={assetUrl(hero.mobileImage)}/>
        <img src={assetUrl(hero.desktopImage)} alt={hero.title}/>
      </picture>
      <div className="hv4-hero-copy"><small>{hero.eyebrow}</small><h1>{hero.title}</h1><p>{hero.description}</p><button type="button" onClick={hero.action}>СМОТРЕТЬ <Icon name="arrow"/></button></div>
      <div className="hv4-hero-controls">
        <nav className="hv4-hero-tabs" aria-label="Слайды главной">{heroSlides.map((item,index)=><button type="button" key={item.label} className={index===activeIndex?"active":""} onClick={()=>setSlide(index)}>{item.label}</button>)}</nav>
        <div className="hv4-hero-arrows"><button type="button" aria-label="Предыдущий баннер" onClick={()=>setSlide((activeIndex+heroSlides.length-1)%heroSlides.length)}><Icon name="arrow"/></button><button type="button" aria-label="Следующий баннер" onClick={()=>setSlide((activeIndex+1)%heroSlides.length)}><Icon name="arrow"/></button></div>
      </div>
    </section>

    <section className="hv4-categories hv4-shell">
      <header className="hv4-head"><div><small>КАТАЛОГ</small><h2>Категории</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>ВЕСЬ КАТАЛОГ</button></header>
      <div className="hv4-category-rail" aria-label="Категории товаров">{categories.map(item=><button className="hv4-category-card" type="button" key={item.title} onClick={()=>openCatalog(item.category)}><img src={assetUrl(item.image)} alt={item.title}/><strong>{item.title}</strong><small>{item.meta}</small></button>)}</div>
    </section>

    <section className="hv4-new hv4-section hv4-shell">
      <header className="hv4-head"><div><small>НОВОЕ ПОСТУПЛЕНИЕ</small><h2>Новинки</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>СМОТРЕТЬ ВСЕ</button></header>
      <ProductRail className="hv4-new-rail" items={newProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="hv4-traditions" aria-label="Традиции в каждом доме">
      <div className="hv4-traditions-media">
        <img src={assetUrl("/images/russian-bedroom.png")} alt="Современная русская спальня"/>
        <img src={assetUrl("/images/editorial-table.webp")} alt="Сервировка дома"/>
        <img src={assetUrl("/images/time-hero.png")} alt="Предметы Культура дома"/>
        <div className="hv4-traditions-copy"><div><small>15 СЕКУНД · BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
      </div>
    </section>

    <section className="hv4-collections hv4-shell">
      <header className="hv4-head"><div><small>EDITORIAL</small><h2>Капсулы и коллекции</h2></div><button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ</button></header>
      <div className="hv4-collection-rail">{capsuleCards.map(card=>{
        const editorial=editorials.find(item=>item.id===card.id);
        return <button type="button" className="hv4-collection-card" key={card.id} onClick={()=>editorial&&openEditorial(editorial)}><img src={assetUrl(card.image)} alt={card.title}/><span><small>{card.kind}</small><strong>{card.title}</strong><em>СМОТРЕТЬ ИСТОРИЮ</em></span></button>;
      })}</div>
    </section>

    <section className="hv4-solutions">
      <div className="hv4-shell">
        <header className="hv4-head"><div><small>ГОТОВЫЕ СЦЕНАРИИ</small><h2>Готовые решения для вашего дома</h2></div><a href={constructorHref}>СМОТРЕТЬ ВСЕ</a></header>
        <div className="hv4-solution-rail">{solutions.map(item=><a className="hv4-solution-card" href={constructorHref} key={item.room}><img src={assetUrl(item.image)} alt={`${item.room}: ${item.title}`}/><span><small>{item.room}</small><strong>{item.title}</strong><em>СОБРАТЬ РЕШЕНИЕ</em></span></a>)}</div>
      </div>
    </section>

    <section className="hv4-brand-boutiques">
      <div className="hv4-brand-copy"><small>О БРЕНДЕ</small><h2>Культура дома — современный взгляд на русские традиции.</h2><p>Мы соединяем текстиль, посуду и предметы интерьера в спокойные, современные истории для дома — без декоративного шума, но с культурной памятью.</p><div className="hv4-boutiques-list" aria-label="Бутики"><span>МОСКВА · ПЕТРОВКА</span><span>САНКТ-ПЕТЕРБУРГ · НЕВСКИЙ</span><span>КАЗАНЬ · БАУМАНА</span></div><button type="button" onClick={()=>alert("Бутики: Москва · Петровка, Санкт-Петербург · Невский проспект, Казань · улица Баумана")}>НАШИ БУТИКИ</button></div>
      <div className="hv4-brand-media"><img src={assetUrl("/images/russian-bedroom.png")} alt="Культура дома — интерьер"/><span>КУЛЬТУРА ДОМА · БУТИКИ</span></div>
    </section>
  </main>;
}'''

pattern = r'function HomeView\([\s\S]*?\n}\n\nfunction CatalogView'
if not re.search(pattern, text):
    raise SystemExit("HomeView block not found")
text = re.sub(pattern, replacement + '\n\nfunction CatalogView', text, count=1)

old_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
new_render = '{view === "home" && <HomeView go={go} openCatalog={openCatalog} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
if old_render in text:
    text = text.replace(old_render,new_render,1)
elif new_render not in text:
    raise SystemExit("HomeView render call not found")

path.write_text(text,encoding="utf-8")
print("Applied homepage V4 storefront redesign")
