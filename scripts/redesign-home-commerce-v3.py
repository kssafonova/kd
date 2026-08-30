from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

replacement = r'''function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  const heroSlides=[
    {eyebrow:"КОЛЛЕКЦИЯ · НОВИНКА",title:"Ледяные узоры",description:"Прохладный свет, вышивка и глубокий синий — готовая история для спокойной спальни.",image:"/assets/images/caps_led.png",editorialId:"ice",nav:"ЛЕДЯНЫЕ УЗОРЫ"},
    {eyebrow:"КАПСУЛА · СПАЛЬНЯ",title:"Лунная сказка",description:"Ночной синий, мягкий сатин и фарфор для домашних ритуалов после заката.",image:"/assets/images/caps_luna_postel.png",editorialId:"luna",nav:"ЛУННАЯ СКАЗКА"},
    {eyebrow:"КУХНЯ И СТОЛОВАЯ",title:"Дом начинается со стола",description:"Посуда, текстиль и детали сервировки, которые собирают пространство в единый образ.",image:"/assets/images/buyan-editorial.png",editorialId:null,nav:"СЕРВИРОВКА"},
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const newProducts=[2000,2004,2010,2003].map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const storyProducts=[2000,2003,2004].map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const categoryCards=[
    {title:"Спальня",meta:"ПОСТЕЛЬНОЕ БЕЛЬЁ · ПЛЕДЫ · ПОДУШКИ",image:"/assets/images/blue-bedroom.png"},
    {title:"Кухня и столовая",meta:"ПОСУДА · СЕРВИРОВКА",image:"/assets/images/buyan-editorial.png"},
    {title:"Декор",meta:"АКЦЕНТЫ ДЛЯ ИНТЕРЬЕРА",image:"/assets/images/beige-bedroom.png"},
    {title:"Ванная",meta:"ТЕКСТИЛЬ · АКСЕССУАРЫ",image:"/assets/images/classic-bedroom.png"},
  ];
  const openHeroStory=()=>{
    if(hero.editorialId){
      const editorial=editorials.find(item=>item.id===hero.editorialId);
      if(editorial){openEditorial(editorial);return;}
    }
    go("catalog");
  };

  return <main className="home-commerce-v3">
    <section className="hc-hero">
      <div className="hc-hero-media"><img src={assetUrl(hero.image)} alt={hero.title}/></div>
      <div className="hc-hero-overlay"/>
      <div className="hc-hero-copy">
        <small>{hero.eyebrow}</small>
        <h1>{hero.title}</h1>
        <p>{hero.description}</p>
        <div className="hc-hero-actions">
          <button className="hc-primary-link" type="button" onClick={openHeroStory}>{hero.editorialId?"СМОТРЕТЬ КОЛЛЕКЦИЮ":"СМОТРЕТЬ КАТЕГОРИЮ"} <Icon name="arrow"/></button>
          <button className="hc-secondary-link" type="button" onClick={()=>go("catalog")}>КУПИТЬ ПРЕДМЕТЫ</button>
        </div>
      </div>
      <nav className="hc-hero-nav" aria-label="Главные истории">
        <div>{heroSlides.map((item,index)=><button key={item.nav} type="button" className={index===activeIndex?"active":""} onClick={()=>setSlide(index)}><span>{String(index+1).padStart(2,"0")}</span>{item.nav}</button>)}</div>
        <div className="hc-hero-arrows"><button type="button" aria-label="Предыдущая история" onClick={()=>setSlide((activeIndex+heroSlides.length-1)%heroSlides.length)}><Icon name="arrow"/></button><button type="button" aria-label="Следующая история" onClick={()=>setSlide((activeIndex+1)%heroSlides.length)}><Icon name="arrow"/></button></div>
      </nav>
    </section>

    <nav className="hc-quick-nav" aria-label="Быстрый переход по каталогу">
      {["НОВИНКИ","СПАЛЬНЯ","КУХНЯ И СТОЛОВАЯ","ДЕКОР","ВАННАЯ"].map(item=><button type="button" key={item} onClick={()=>go("catalog")}>{item}<Icon name="arrow"/></button>)}
    </nav>

    <section className="hc-products hc-new">
      <header className="hc-section-head">
        <div><small>НОВОЕ В КОЛЛЕКЦИИ</small><h2>Новинки</h2></div>
        <button type="button" onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ</button>
      </header>
      <ProductRail className="hc-product-rail" items={newProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="hc-story-shop">
      <button className="hc-story-media" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}><img src={assetUrl("/assets/images/caps_led_podyshka.png")} alt="Коллекция Ледяные узоры"/><span>EDITORIAL · SHOP THE STORY</span></button>
      <div className="hc-story-copy">
        <small>КОЛЛЕКЦИЯ · ЛЕДЯНЫЕ УЗОРЫ</small>
        <h2>Соберите образ целиком</h2>
        <p>Вещи уже подобраны по цвету, фактуре и настроению. Откройте историю, выберите нужные предметы и размеры — или начните с отдельных товаров.</p>
        <button className="hc-text-link" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></button>
      </div>
      <div className="hc-story-products"><ProductRail className="hc-story-product-rail" items={storyProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/></div>
    </section>

    <section className="hc-categories">
      <header className="hc-section-head">
        <div><small>КАТАЛОГ</small><h2>Для каждой комнаты</h2></div>
        <button type="button" onClick={()=>go("catalog")}>ВЕСЬ КАТАЛОГ</button>
      </header>
      <div className="hc-category-grid">{categoryCards.map((card,index)=><button type="button" className={`hc-category hc-category-${index+1}`} key={card.title} onClick={()=>go("catalog")}><img src={assetUrl(card.image)} alt={card.title}/><span><strong>{card.title}</strong><small>{card.meta}</small><em>СМОТРЕТЬ →</em></span></button>)}</div>
    </section>

    <section className="hc-editorial">
      <header className="hc-section-head">
        <div><small>КАПСУЛЫ И КОЛЛЕКЦИИ</small><h2>Истории, которые можно купить</h2></div>
        <button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ</button>
      </header>
      <div className="hc-editorial-grid">
        <button type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="luna")!)}><img src={assetUrl("/assets/images/caps_luna_postel2.png")} alt="Лунная сказка"/><span><small>КАПСУЛА</small><strong>Лунная сказка</strong><em>СМОТРЕТЬ ИСТОРИЮ →</em></span></button>
        <button type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}><img src={assetUrl("/assets/images/caps_led_serviz.png")} alt="Ледяные узоры"/><span><small>КОЛЛЕКЦИЯ</small><strong>Ледяные узоры</strong><em>СМОТРЕТЬ ИСТОРИЮ →</em></span></button>
      </div>
    </section>

    <section className="hc-solution">
      <div className="hc-solution-copy"><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2>Не выбирайте по одному. Соберите пространство.</h2><p>Готовые сценарии объединяют предметы в законченный образ. Можно заменить альтернативы, выбрать размеры и добавить весь набор в корзину одним действием.</p><a href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`}>ОТКРЫТЬ ГОТОВЫЕ РЕШЕНИЯ <Icon name="arrow"/></a></div>
      <div className="hc-solution-media"><img src={assetUrl("/assets/images/caps_luna_serviz3.png")} alt="Готовые решения для дома"/></div>
    </section>

    <section className="hc-service" aria-label="Преимущества сервиса">
      <div><small>01</small><strong>Бесплатная доставка</strong><span>при заказе от 15 000 ₽</span></div>
      <div><small>02</small><strong>Наличие в бутиках</strong><span>проверяйте перед покупкой</span></div>
      <div><small>03</small><strong>Помощь с выбором</strong><span>подбор предметов и готовых образов</span></div>
    </section>

    <section className="hc-brand"><small>КУЛЬТУРА ДОМА</small><h2>Современный дом с культурной памятью.</h2><p>Предметы, текстиль и сервировка, которые соединяются в личные семейные истории.</p><button type="button" onClick={()=>go("collections")}>ОТКРЫТЬ КАПСУЛЫ И КОЛЛЕКЦИИ</button></section>
  </main>;
}'''

pattern = r'function HomeView\([\s\S]*?\n}\n\nfunction CatalogView'
if not re.search(pattern, text):
    raise SystemExit("HomeView block not found")
text = re.sub(pattern, replacement + '\n\nfunction CatalogView', text, count=1)

old_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}'
new_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
if old_render in text:
    text = text.replace(old_render,new_render,1)

path.write_text(text,encoding="utf-8")
print("Applied premium conversion-focused homepage V3")
