from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

replacement = r'''function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  const homeSlides=[
    {kicker:"КОЛЛЕКЦИЯ · СПАЛЬНЯ",title:"Ледяные узоры",description:"Холодный свет, белый текстиль и прозрачный голубой — история тихого зимнего утра.",image:"/images/editorial/caps_led.png",label:"ЛЕДЯНЫЕ УЗОРЫ",editorialId:"ice"},
    {kicker:"КАПСУЛА · НОЧНЫЕ РИТУАЛЫ",title:"Лунная сказка",description:"Глубокий синий, сатин и фарфор для спальни и позднего чаепития.",image:"/images/editorial/caps_luna_postel.png",label:"ЛУННАЯ СКАЗКА",editorialId:"luna"},
    {kicker:"ДОМ · СЕРВИРОВКА",title:"Стол как история",description:"Посуда, текстиль и детали, которые собирают домашний ритуал в единый образ.",image:"/images/buyan-editorial.png",label:"СЕРВИРОВКА",editorialId:null},
    {kicker:"ДОМ · ТЕКСТИЛЬ",title:"Тихая спальня",description:"Спокойные фактуры и мягкая палитра для ежедневного пространства отдыха.",image:"/images/beige-bedroom.png",label:"СПАЛЬНЯ",editorialId:null},
  ];
  const activeIndex=((slide%homeSlides.length)+homeSlides.length)%homeSlides.length;
  const current=homeSlides[activeIndex];
  const featuredProducts=[2000,2004,2,7].map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const categoryCards=[
    {title:"Спальня",meta:"ПОСТЕЛЬНОЕ БЕЛЬЁ · ТЕКСТИЛЬ",image:"/images/blue-bedroom.png"},
    {title:"Сервировка",meta:"ПОСУДА · СТОЛОВЫЙ ТЕКСТИЛЬ",image:"/images/moon-plate.png"},
    {title:"Ванная",meta:"ТЕКСТИЛЬ ДЛЯ ДОМА",image:"/images/classic-bedroom.png"},
    {title:"Декор",meta:"АКЦЕНТЫ ДЛЯ ИНТЕРЬЕРА",image:"/images/beige-bedroom.png"},
  ];
  const openHero=()=>{
    if(current.editorialId){
      const item=editorials.find(editorial=>editorial.id===current.editorialId);
      if(item){openEditorial(item);return;}
    }
    go("catalog");
  };

  return <main className="home-magazine-v2">
    <section className="home-magazine-hero">
      <div className="home-magazine-hero-media"><img src={assetUrl(current.image)} alt={current.title}/></div>
      <div className="home-magazine-hero-copy">
        <small>{current.kicker}</small>
        <h1>{current.title}</h1>
        <p>{current.description}</p>
        <button className="home-magazine-hero-cta" type="button" onClick={openHero}><span>{current.editorialId?"СМОТРЕТЬ ИСТОРИЮ":"СМОТРЕТЬ КАТЕГОРИЮ"}</span><Icon name="arrow"/></button>
      </div>
      <div className="home-magazine-hero-nav">
        <div className="home-magazine-hero-tabs">{homeSlides.map((item,index)=><button type="button" key={item.label} className={index===activeIndex?"active":""} onClick={()=>setSlide(index)}>{item.label}</button>)}</div>
        <div className="home-magazine-hero-arrows"><button type="button" onClick={()=>setSlide((activeIndex+homeSlides.length-1)%homeSlides.length)} aria-label="Предыдущий слайд"><Icon name="arrow"/></button><button type="button" onClick={()=>setSlide((activeIndex+1)%homeSlides.length)} aria-label="Следующий слайд"><Icon name="arrow"/></button></div>
      </div>
    </section>

    <section className="home-magazine-intro">
      <small>01 / ДОМ КАК ИСТОРИЯ</small>
      <div><h2>Не просто предметы для дома — готовые образы, в которых вещи уже связаны друг с другом.</h2><p>Коллекции, капсулы и сценарии помогают увидеть не отдельный товар, а целое пространство: спальню, сервировку, подарок или домашний ритуал.</p></div>
    </section>

    <section className="home-magazine-lead">
      <button className="home-magazine-lead-main" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}><img src={assetUrl("/images/editorial/caps_led_podyshka.png")} alt="Ледяные узоры — интерьер"/></button>
      <button className="home-magazine-lead-detail" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}><img src={assetUrl("/images/editorial/caps_led_podyshka2.png")} alt="Ледяные узоры — детали"/></button>
      <div className="home-magazine-lead-copy"><small>02 / EDITORIAL · КОЛЛЕКЦИЯ</small><h3>Ледяные узоры</h3><p>История о холодном свете, воздухе и предметах, которые собирают спокойную спальню в единый образ.</p><button className="home-magazine-text-link" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></button></div>
    </section>

    <section className="home-magazine-categories">
      <header className="home-magazine-section-head"><div><small>03 / КАТАЛОГ</small><h2>Пространства дома</h2></div><button type="button" onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></header>
      <div className="home-magazine-category-grid">{categoryCards.map(card=><button className="home-magazine-category-card" type="button" key={card.title} onClick={()=>go("catalog")}><img src={assetUrl(card.image)} alt={card.title}/><span><strong>{card.title}</strong><small>{card.meta}</small></span></button>)}</div>
    </section>

    <section className="home-magazine-stories">
      <header className="home-magazine-section-head"><div><small>04 / КАПСУЛЫ И КОЛЛЕКЦИИ</small><h2>Истории для дома</h2></div><button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ →</button></header>
      <div className="home-magazine-story-grid">
        <button className="home-magazine-story-card" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="luna")!)}><img src={assetUrl("/images/editorial/caps_luna_postel2.png")} alt="Лунная сказка"/><span className="home-magazine-story-copy"><small>КАПСУЛА</small><strong>Лунная сказка</strong><em>СМОТРЕТЬ ИСТОРИЮ →</em></span></button>
        <button className="home-magazine-story-card" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}><img src={assetUrl("/images/editorial/caps_led_serviz.png")} alt="Ледяные узоры"/><span className="home-magazine-story-copy"><small>КОЛЛЕКЦИЯ</small><strong>Ледяные узоры</strong><em>СМОТРЕТЬ ИСТОРИЮ →</em></span></button>
      </div>
    </section>

    <section className="home-magazine-products">
      <header className="home-magazine-section-head"><div><small>05 / ВЫБОР РЕДАКЦИИ</small><h2>Предметы из историй</h2></div><button type="button" onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></header>
      <ProductRail className="home-magazine-product-rail" items={featuredProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="home-magazine-constructor">
      <div className="home-magazine-constructor-copy"><small>06 / ГОТОВОЕ РЕШЕНИЕ</small><h2>Соберите дом по сценарию</h2><p>Выберите готовую атмосферу, замените отдельные предметы на альтернативы, настройте размеры и соберите весь образ одной логикой.</p><a href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`}>ОТКРЫТЬ КОНСТРУКТОР →</a></div>
      <div className="home-magazine-constructor-media"><img src={assetUrl("/images/editorial/caps_luna_serviz3.png")} alt="Конструктор готовых решений"/></div>
    </section>

    <section className="home-magazine-closing"><small>КУЛЬТУРА ДОМА</small><h2>Предметы, с которыми остаётся вечное.</h2><p>Современный дом, русская культурная память и вещи, которые хочется соединять в собственные семейные истории.</p><button type="button" onClick={()=>go("collections")}>ОТКРЫТЬ EDITORIAL →</button></section>
  </main>;
}'''

pattern = r'function HomeView\([\s\S]*?\n}\n\nfunction CatalogView'
if not re.search(pattern, text):
    raise SystemExit("HomeView block not found")
text = re.sub(pattern, replacement + '\n\nfunction CatalogView', text, count=1)

# Keep the final render signature aligned with the redesigned HomeView.
old_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}'
new_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
if old_render in text:
    text = text.replace(old_render,new_render,1)

path.write_text(text,encoding="utf-8")
print("Applied final editorial magazine homepage redesign")
