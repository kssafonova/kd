from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
CSS = ROOT / "app" / "globals.css"
ASSETS = ROOT / "assets" / "images"

required_assets = [
    "home113-hero-desktop.svg",
    "home113-hero-mobile.svg",
    "home113-editorial-atlas.svg",
]
for filename in required_assets:
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"HOME_REDESIGN_V113: missing asset {filename}")

home_function = r'''function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_REDESIGN_V113 — supplied homepage ZIP, 47 source photographs represented.
  void onProduct; void favorite; void favorites; void onAdd; void openEditorial;
  const readyBase=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const heroSlides=[
    {eyebrow:"НОВИНКИ",title:"Новые истории дома",text:"Предметы, которые собирают пространство в цельный образ — от спальни до сервировки.",cta:"Смотреть новинки",action:()=>openCatalog()},
    {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой",text:"Сатин, мягкий свет и спокойные оттенки для пространства, в котором хочется остаться.",cta:"Перейти в спальню",action:()=>openCatalog("Постельное белье")},
    {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал",text:"Фарфор, текстиль и детали стола в современной культуре русского дома.",cta:"Смотреть сервировку",action:()=>openCatalog("Посуда и сервировка")},
  ];
  const active=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[active];
  const heroPosition=`${active*50}% 50%`;
  const atlasStyle=(index:number)=>({
    backgroundImage:`url("${assetUrl("/assets/images/home113-editorial-atlas.svg")}")`,
    backgroundSize:"600% 700%",
    backgroundPosition:`${(index%6)*20}% ${(Math.floor(index/6)*100)/6}%`,
  });
  const categories=[
    {title:"Спальня",note:"Постельное бельё",index:0,action:()=>openCatalog("Постельное белье")},
    {title:"Посуда и сервировка",note:"Кухня и столовая",index:1,action:()=>openCatalog("Посуда и сервировка")},
    {title:"Столовый текстиль",note:"Скатерти, салфетки, дорожки",index:2,action:()=>openCatalog("Столовый текстиль")},
    {title:"Декор",note:"Предметы для дома",index:3,action:()=>openCatalog("Декор для дома")},
    {title:"Текстиль для дома",note:"Пледы и подушки",index:4,action:()=>openCatalog("Пледы и подушки")},
    {title:"Ванная",note:"Для ежедневных ритуалов",index:5,action:()=>openCatalog()},
    {title:"Outlet",note:"Особые предложения",index:6,action:()=>openCatalog()},
  ];
  const capsules=[
    {title:"Нити",meta:"КАПСУЛА · ТЕКСТИЛЬ",copy:"Спокойная графика, прохладные оттенки и выразительная фактура.",indices:[7,8]},
    {title:"Феникс",meta:"КАПСУЛА · ДЕКОР",copy:"Тёплая палитра, огонь и золотистые детали для камерного интерьера.",indices:[9,10,11]},
    {title:"Лунная сказка",meta:"КАПСУЛА · СПАЛЬНЯ И СЕРВИРОВКА",copy:"Ночной синий, молочные оттенки и тонкие акценты объединяют дом в одну историю.",indices:[12,13,14,15,16,17]},
    {title:"Ледяные узоры",meta:"КАПСУЛА · ЗИМНЯЯ ИСТОРИЯ",copy:"Свет, хрустальная чистота и морозная графика в текстиле и фарфоре.",indices:[18,19,20,21]},
    {title:"Тайна",meta:"КАПСУЛА · ТЁМНАЯ ЭСТЕТИКА",copy:"Глубокие оттенки и тактильные материалы для выразительной, спокойной атмосферы.",indices:[22,23,24]},
  ];
  const solutions=[
    {title:"Зелёный салон",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Свежая сервировка с зелёными акцентами и светлым текстилем.",indices:[25,26],href:`${readyBase}/ready-solutions/green-salon/`},
    {title:"Красные линии",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Графичная композиция, построенная на красных акцентах и белом фарфоре.",indices:[27,28],href:`${readyBase}/ready-solutions/red-lines/`},
    {title:"Зимняя сказка",meta:"ГОТОВОЕ РЕШЕНИЕ · ДОМ",copy:"Сценарий для зимнего дома: спальня, стол и декор в единой холодной палитре.",indices:[29,30,31,32,33,34],href:`${readyBase}/ready-solutions/winter-fairy-tale/`},
    {title:"Пламя морских глубин",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Глубокий синий и тёплый свет — драматичная композиция для вечерней сервировки.",indices:[35,36,37],href:`${readyBase}/ready-solutions/`},
    {title:"Тёплый брутализм",meta:"ГОТОВОЕ РЕШЕНИЕ · ИНТЕРЬЕР",copy:"Кожа, дерево и сдержанные фактуры в собранном мужском интерьере.",indices:[38,39,40],href:`${readyBase}/ready-solutions/warm-brutalism/`},
  ];

  return <main className="home-v113">
    <nav className="home113-nav" aria-label="Навигация по главной">
      <button type="button" onClick={()=>openCatalog()}>Новинки</button>
      <button type="button" onClick={()=>openCatalog("Постельное белье")}>Спальня</button>
      <button type="button" onClick={()=>openCatalog("Посуда и сервировка")}>Кухня и столовая</button>
      <button type="button" onClick={()=>openCatalog("Декор для дома")}>Декор</button>
      <button type="button" onClick={()=>go("collections")}>Капсулы</button>
      <a href={`${readyBase}/ready-solutions/`}>Готовые решения</a>
    </nav>

    <section className="home113-hero" aria-label="Главные истории">
      <div className="home113-hero-art home113-hero-art-desktop" aria-hidden="true" style={{backgroundImage:`url("${assetUrl("/assets/images/home113-hero-desktop.svg")}")`,backgroundPosition:heroPosition}}/>
      <div className="home113-hero-art home113-hero-art-mobile" aria-hidden="true" style={{backgroundImage:`url("${assetUrl("/assets/images/home113-hero-mobile.svg")}")`,backgroundPosition:heroPosition}}/>
      <div className="home113-hero-shade"/>
      <div className="home113-hero-copy">
        <small>{hero.eyebrow}</small>
        <h1>{hero.title}</h1>
        <p>{hero.text}</p>
        <button type="button" onClick={hero.action}>{hero.cta}<span aria-hidden="true">↗</span></button>
      </div>
      <div className="home113-hero-controls" aria-label="Выбор баннера">{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===active?"is-active":""} onClick={()=>setSlide(index)}><span>{String(index+1).padStart(2,"0")}</span><b>{item.eyebrow}</b></button>)}</div>
    </section>

    <section className="home113-section home113-category-section">
      <header className="home113-section-head"><div><small>КАТАЛОГ</small><h2>Пространства дома</h2></div><p>Начните с комнаты или категории — дальше предметы складываются в общую композицию.</p></header>
      <div className="home113-category-rail">{categories.map(item=><button type="button" key={item.title} className="home113-category-card" onClick={item.action}><span className="home113-atlas-card" role="img" aria-label={item.title} style={atlasStyle(item.index)}/><strong>{item.title}</strong><small>{item.note}</small></button>)}</div>
    </section>

    <section className="home113-capsules">
      <header className="home113-editorial-head"><small>КАПСУЛЫ</small><h2>Истории в деталях</h2><p>Каждая капсула соединяет текстиль, сервировку и декор через цвет, материал и настроение.</p><button type="button" onClick={()=>go("collections")}>Смотреть все капсулы</button></header>
      <div className="home113-story-list">{capsules.map((item,storyIndex)=><article className="home113-story" key={item.title}>
        <div className="home113-story-copy"><small>{item.meta}</small><h3>{item.title}</h3><p>{item.copy}</p><button type="button" onClick={()=>go("collections")}>Открыть капсулу <span aria-hidden="true">↗</span></button></div>
        <div className="home113-photo-rail" aria-label={`Фотографии капсулы ${item.title}`}>{item.indices.map((atlasIndex,imageIndex)=><button type="button" key={atlasIndex} className="home113-photo-card" onClick={()=>go("collections")} aria-label={`${item.title}, фото ${imageIndex+1}`}><span role="img" aria-label={`${item.title}, фото ${imageIndex+1}`} style={atlasStyle(atlasIndex)}/></button>)}</div>
      </article>)}</div>
    </section>

    <section className="home113-solutions">
      <header className="home113-editorial-head home113-editorial-head-light"><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2>Интерьер уже собран</h2><p>Выберите готовую композицию как отправную точку и настройте предметы под своё пространство.</p><a href={`${readyBase}/ready-solutions/`}>Все готовые решения</a></header>
      <div className="home113-solution-list">{solutions.map(item=><article className="home113-solution" key={item.title}>
        <div className="home113-solution-copy"><small>{item.meta}</small><h3>{item.title}</h3><p>{item.copy}</p><a href={item.href}>Собрать решение <span aria-hidden="true">↗</span></a></div>
        <div className="home113-photo-rail home113-solution-rail" aria-label={`Фотографии решения ${item.title}`}>{item.indices.map((atlasIndex,imageIndex)=><a href={item.href} key={atlasIndex} className="home113-photo-card" aria-label={`${item.title}, фото ${imageIndex+1}`}><span role="img" aria-label={`${item.title}, фото ${imageIndex+1}`} style={atlasStyle(atlasIndex)}/></a>)}</div>
      </article>)}</div>
    </section>

    <HomeBoutiques/>
  </main>;
}'''

css_block = r'''/* HOME_REDESIGN_V113 */
.home-v113{--h113-ink:#161815;--h113-paper:#f5f2eb;--h113-soft:#e8e2d8;--h113-green:#202923;background:var(--h113-paper);color:var(--h113-ink);overflow:hidden}
.home113-nav{height:52px;display:flex;align-items:center;justify-content:center;gap:clamp(18px,3vw,48px);padding:0 24px;overflow-x:auto;white-space:nowrap;background:#f7f5ef;border-bottom:1px solid rgba(22,24,21,.12);scrollbar-width:none}
.home113-nav::-webkit-scrollbar,.home113-category-rail::-webkit-scrollbar,.home113-photo-rail::-webkit-scrollbar{display:none}
.home113-nav button,.home113-nav a{border:0;background:none;color:inherit;font:500 11px/1.1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:18px 0;cursor:pointer;text-decoration:none}
.home113-hero{position:relative;height:clamp(600px,64vw,900px);min-height:72vh;background:#252722;color:#fff;isolation:isolate}
.home113-hero-art{position:absolute;inset:0;background-repeat:no-repeat;background-size:300% 100%;transition:background-position .7s cubic-bezier(.2,.7,.2,1);z-index:-3}
.home113-hero-art-mobile{display:none}
.home113-hero-shade{position:absolute;inset:0;z-index:-2;background:linear-gradient(90deg,rgba(10,12,10,.52) 0%,rgba(10,12,10,.12) 48%,rgba(10,12,10,.08) 100%),linear-gradient(0deg,rgba(10,12,10,.42),transparent 48%)}
.home113-hero-copy{position:absolute;left:clamp(28px,6vw,96px);bottom:clamp(118px,13vw,180px);width:min(650px,70vw)}
.home113-hero-copy small,.home113-section-head small,.home113-editorial-head>small,.home113-story-copy small,.home113-solution-copy small{display:block;font:500 11px/1.25 Arial,sans-serif;letter-spacing:.17em;text-transform:uppercase}
.home113-hero-copy h1{font-family:"Tenor Sans",Georgia,serif;font-size:clamp(44px,6.2vw,94px);font-weight:400;line-height:.98;letter-spacing:-.025em;margin:14px 0 20px;max-width:720px}
.home113-hero-copy p{font:400 clamp(14px,1.2vw,17px)/1.55 Arial,sans-serif;max-width:510px;margin:0 0 28px;color:rgba(255,255,255,.88)}
.home113-hero-copy button,.home113-editorial-head button,.home113-editorial-head a,.home113-story-copy button,.home113-solution-copy a{display:inline-flex;align-items:center;gap:18px;border:0;border-bottom:1px solid currentColor;background:none;color:inherit;padding:0 0 7px;font:500 11px/1 Arial,sans-serif;letter-spacing:.13em;text-transform:uppercase;text-decoration:none;cursor:pointer}
.home113-hero-copy button span,.home113-story-copy button span,.home113-solution-copy a span{font-size:16px;font-weight:400}
.home113-hero-controls{position:absolute;left:clamp(28px,6vw,96px);right:clamp(28px,6vw,96px);bottom:34px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;border-top:1px solid rgba(255,255,255,.45)}
.home113-hero-controls button{position:relative;text-align:left;color:rgba(255,255,255,.66);border:0;background:none;padding:15px 0 0;display:flex;gap:13px;align-items:center;cursor:pointer;font:500 10px/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase}
.home113-hero-controls button::before{content:"";position:absolute;height:2px;left:0;right:100%;top:-1px;background:#fff;transition:right .35s ease}
.home113-hero-controls button.is-active{color:#fff}.home113-hero-controls button.is-active::before{right:0}.home113-hero-controls span{opacity:.7}.home113-hero-controls b{font-weight:500}
.home113-section{padding:clamp(72px,9vw,132px) 0}
.home113-section-head,.home113-editorial-head{padding:0 clamp(22px,5vw,76px);display:grid;grid-template-columns:minmax(300px,1.2fr) minmax(240px,.8fr);gap:40px;align-items:end;margin-bottom:42px}
.home113-section-head h2,.home113-editorial-head h2{font-family:"Tenor Sans",Georgia,serif;font-size:clamp(38px,5vw,72px);font-weight:400;line-height:1.02;letter-spacing:-.02em;margin:12px 0 0}
.home113-section-head p,.home113-editorial-head p{max-width:520px;margin:0;font:400 14px/1.65 Arial,sans-serif;color:#5f625d}
.home113-category-rail{display:flex;gap:14px;overflow-x:auto;padding:0 clamp(22px,5vw,76px) 10px;scroll-snap-type:x proximity;scrollbar-width:none}
.home113-category-card{flex:0 0 clamp(235px,23vw,360px);border:0;background:none;color:inherit;text-align:left;padding:0;cursor:pointer;scroll-snap-align:start}
.home113-atlas-card{display:block;width:100%;aspect-ratio:4/5;background-repeat:no-repeat;background-color:#ddd6cb;transition:transform .45s ease;transform:scale(1.001)}
.home113-category-card:hover .home113-atlas-card{transform:scale(1.018)}
.home113-category-card strong{display:block;font-family:"Tenor Sans",Georgia,serif;font-size:clamp(20px,2vw,28px);font-weight:400;line-height:1.15;margin-top:18px}
.home113-category-card small{display:block;margin-top:6px;color:#77766f;font:400 11px/1.3 Arial,sans-serif;letter-spacing:.04em}
.home113-capsules{padding:clamp(80px,10vw,150px) 0;background:#ede9e0}
.home113-editorial-head{align-items:start;margin-bottom:clamp(62px,8vw,110px)}
.home113-editorial-head>small{grid-column:1/-1;margin-bottom:-18px}.home113-editorial-head>p{align-self:end}.home113-editorial-head>button,.home113-editorial-head>a{grid-column:2;justify-self:start;margin-top:-17px}
.home113-story-list,.home113-solution-list{display:flex;flex-direction:column;gap:clamp(88px,11vw,170px)}
.home113-story,.home113-solution{display:grid;grid-template-columns:minmax(230px,.27fr) minmax(0,.73fr);gap:clamp(34px,5vw,78px);padding-left:clamp(22px,5vw,76px);align-items:start}
.home113-story-copy,.home113-solution-copy{padding-top:8px;padding-right:20px;position:sticky;top:30px}
.home113-story-copy h3,.home113-solution-copy h3{font-family:"Tenor Sans",Georgia,serif;font-weight:400;font-size:clamp(34px,4vw,60px);line-height:1.02;letter-spacing:-.02em;margin:13px 0 18px}
.home113-story-copy p,.home113-solution-copy p{font:400 13px/1.65 Arial,sans-serif;color:#686964;max-width:320px;margin:0 0 28px}
.home113-photo-rail{display:flex;gap:12px;overflow-x:auto;padding:0 clamp(22px,5vw,76px) 8px 0;scroll-snap-type:x mandatory;scrollbar-width:none}
.home113-photo-card{display:block;position:relative;flex:0 0 clamp(280px,34vw,520px);aspect-ratio:4/5;border:0;padding:0;background:#d9d4cb;overflow:hidden;scroll-snap-align:start;text-decoration:none;cursor:pointer}
.home113-photo-card>span{position:absolute;inset:0;display:block;background-repeat:no-repeat;transition:transform .45s ease;transform:scale(1.002)}
.home113-photo-card:hover>span{transform:scale(1.02)}
.home113-solutions{padding:clamp(90px,11vw,160px) 0;background:var(--h113-green);color:#f5f0e6}
.home113-editorial-head-light p,.home113-solutions .home113-solution-copy p{color:rgba(245,240,230,.68)}
.home113-solution{grid-template-columns:minmax(230px,.3fr) minmax(0,.7fr)}
.home113-solutions .home113-photo-card{background:#374039}
.home113-solutions+.home-boutiques{margin-top:0}
@media(max-width:760px){
  .home113-nav{justify-content:flex-start;height:46px;padding:0 18px;gap:25px}.home113-nav button,.home113-nav a{padding:16px 0;font-size:9px}
  .home113-hero{height:calc(100svh - 46px);min-height:620px;max-height:860px}.home113-hero-art-desktop{display:none}.home113-hero-art-mobile{display:block;background-size:300% 100%}
  .home113-hero-shade{background:linear-gradient(0deg,rgba(10,12,10,.6) 0%,rgba(10,12,10,.08) 62%)}
  .home113-hero-copy{left:22px;right:22px;bottom:115px;width:auto}.home113-hero-copy h1{font-size:clamp(42px,13vw,62px);max-width:90%}.home113-hero-copy p{font-size:13px;max-width:92%;margin-bottom:23px}
  .home113-hero-controls{left:22px;right:22px;bottom:24px;gap:9px}.home113-hero-controls button{padding-top:11px;gap:7px}.home113-hero-controls b{display:none}
  .home113-section{padding:72px 0}.home113-section-head,.home113-editorial-head{display:block;padding:0 22px;margin-bottom:30px}.home113-section-head h2,.home113-editorial-head h2{font-size:42px}.home113-section-head p,.home113-editorial-head p{font-size:13px;margin-top:20px;max-width:92%}.home113-editorial-head>small{margin-bottom:0}.home113-editorial-head>button,.home113-editorial-head>a{margin-top:23px}
  .home113-category-rail{padding:0 22px 8px;gap:10px}.home113-category-card{flex-basis:76vw}.home113-category-card strong{font-size:23px;margin-top:14px}
  .home113-capsules,.home113-solutions{padding:76px 0}.home113-story-list,.home113-solution-list{gap:82px}
  .home113-story,.home113-solution{display:block;padding-left:0}.home113-story-copy,.home113-solution-copy{position:static;padding:0 22px 24px}.home113-story-copy h3,.home113-solution-copy h3{font-size:40px;margin:10px 0 14px}.home113-story-copy p,.home113-solution-copy p{font-size:13px;margin-bottom:20px;max-width:92%}
  .home113-photo-rail{padding:0 22px 8px;gap:8px}.home113-photo-card{flex-basis:82vw}
}
/* END_HOME_REDESIGN_V113 */'''

page_text = PAGE.read_text(encoding="utf-8")
page_original = page_text
start = page_text.find("function HomeView(")
if start < 0:
    raise SystemExit("HOME_REDESIGN_V113: HomeView start not found")
end = page_text.find("\n\nfunction CatalogView(", start)
if end < 0:
    raise SystemExit("HOME_REDESIGN_V113: CatalogView boundary not found")
page_text = page_text[:start] + home_function + page_text[end:]
PAGE.write_text(page_text, encoding="utf-8")

css_text = CSS.read_text(encoding="utf-8")
css_original = css_text
pattern = re.compile(r"/\* HOME_REDESIGN_V113 \*/.*?/\* END_HOME_REDESIGN_V113 \*/", re.S)
if pattern.search(css_text):
    css_text = pattern.sub(css_block, css_text, count=1)
else:
    css_text = css_text.rstrip() + "\n\n" + css_block + "\n"
CSS.write_text(css_text, encoding="utf-8")

checks = [
    "HOME_REDESIGN_V113",
    "home113-editorial-atlas.svg",
    "home113-hero-desktop.svg",
    "home113-hero-mobile.svg",
    "indices:[38,39,40]",
    "indices:[29,30,31,32,33,34]",
    "Пространства дома",
    "Интерьер уже собран",
]
for marker in checks:
    if marker not in page_text and marker not in css_text:
        raise SystemExit(f"HOME_REDESIGN_V113: missing marker {marker}")

print(
    "// HOME_REDESIGN_V113: homepage rebuilt from supplied ZIP; "
    "3 desktop/mobile hero scenes + 7 categories + 18 capsule photos + 16 ready-solution photos; "
    f"page_changed={page_text != page_original}; css_changed={css_text != css_original}; assets=3 atlases verified"
)
