from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
globals_path = root / "app" / "globals.css"

# ---------- Ready solution wizard behavior ----------
ready = ready_path.read_text(encoding="utf-8")

# Removed base collections move into the additional-collection rail instead of disappearing.
old_extra = 'const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; return solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);'
new_extra = 'const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; const removedBase=baseCollections.filter((name)=>!activeCollections.some((active)=>norm(active)===norm(name))); const configured=solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name).filter((name)=>!activeCollections.some((active)=>norm(active)===norm(name))); return Array.from(new Map([...removedBase,...configured].map((name)=>[norm(name),name])).values()).slice(0,6);},[catalog,solution,baseCollections,activeCollections]);'
if old_extra in ready:
    ready = ready.replace(old_extra, new_extra, 1)

# Use the same compact editorial identity block on all three steps.
old_hero = '{step<3&&<section className={`rs71-hero ${step===2?"is-compact":""}`}><div className="rs71-hero-media"><RemoteImage src={solution.heroImage||baseRows[0]?.primary_image_url||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div><div className="rs71-hero-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно адаптировать под своё пространство.</p><div>{activeCollections.slice(0,6).map((c)=><span key={c}>{displayCollectionName(c)}</span>)}</div></div></section>}'
new_hero = '<section className="rs71-hero is-compact rs81-identity"><div className="rs71-hero-media"><RemoteImage src={solution.heroImage||baseRows[0]?.primary_image_url||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div><div className="rs71-hero-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно адаптировать под своё пространство.</p><div>{activeCollections.slice(0,6).map((c)=><span key={c}>{displayCollectionName(c)}</span>)}</div></div></section>'
if old_hero in ready:
    ready = ready.replace(old_hero, new_hero, 1)

# Header aligned with the storefront header language.
header_start = ready.find('function Header() {')
header_end = ready.find('function Footer()', header_start)
if header_start >= 0 and header_end > header_start:
    header = '''function Header() {
  return <><div className="rs71-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href="/">ПОДРОБНЕЕ</Link></div><header className="rs71-header rs81-header"><div className="rs81-header-left"><Link href="/?open=menu" className="rs81-hamburger" aria-label="Меню"><i/><i/><i/></Link><Link href="/?open=boutiques" className="rs81-boutiques">Бутики</Link></div><Link href="/" className="rs71-logo">КУЛЬТУРА ДОМА</Link><nav><Link href="/?open=search">Поиск</Link><Link href="/?open=account">Профиль</Link><Link href="/?open=favorites">Избранное</Link><Link href="/?open=cart">Корзина</Link></nav></header></>;
}
'''
    ready = ready[:header_start] + header + ready[header_end:]

if '// STOREFRONT_V81' not in ready:
    ready = ready.replace('// READY_SOLUTIONS_GROUPS_V80', '// READY_SOLUTIONS_GROUPS_V80\n// STOREFRONT_V81', 1)
ready_path.write_text(ready, encoding="utf-8")

# ---------- Echo media from the real CSV feed ----------
page = page_path.read_text(encoding="utf-8")
csv_path = root / "public" / "data" / "kultura_doma_full_constructor_eligible_catalog.csv"
echo_media = {}
if csv_path.exists():
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            name = str(row.get("product_name") or "")
            collection = str(row.get("collection") or "")
            if "камея" not in name.lower() and collection.lower() != "камея":
                continue
            article = str(row.get("vendor_code") or "").strip()
            primary = str(row.get("primary_image_url") or "").strip()
            gallery = [x.strip() for x in str(row.get("all_image_urls") or "").split("|") if x.strip()]
            if article and primary:
                echo_media[article] = {"image": primary, "gallery": list(dict.fromkeys([primary, *gallery]))}

media_marker = '// ECHO_CSV_MEDIA_V81'
if media_marker not in page and echo_media:
    anchor = 'products.push(...collectionEditorialProducts.filter'
    pos = page.find(anchor)
    if pos >= 0:
        block = media_marker + '\nconst echoCsvMediaByArticle:Record<string,{image:string;gallery:string[]}>=' + json.dumps(echo_media, ensure_ascii=False, separators=(",", ":")) + ';\ncollectionEditorialProducts.forEach(item=>{if(!item.name.includes("Эхо"))return;const article=item.skus?.[0]?.article||item.article||"";const media=echoCsvMediaByArticle[article];if(!media)return;item.image=media.image;item.gallery=media.gallery;item.skus=item.skus?.map(sku=>{const next=echoCsvMediaByArticle[sku.article]||media;return {...sku,image:next.image,gallery:next.gallery};});});\n'
        page = page[:pos] + block + page[pos:]

# ---------- Homepage V81 ----------
home_start = page.find('function HomeView(')
home_end = page.find('function CatalogView(', home_start)
if home_start >= 0 and home_end > home_start:
    home = r'''function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_STOREFRONT_V81
  const heroSlides=[
    {eyebrow:"НОВАЯ ИСТОРИЯ",title:"Дом как единая композиция",text:"Текстиль, сервировка и декор в современном русском прочтении.",image:"/images/editorial/caps_luna_postel2.png",mobile:"/images/editorial/caps_luna_postel.png",cta:"Смотреть коллекции",action:()=>go("collections")},
    {eyebrow:"ГОТОВЫЕ РЕШЕНИЯ",title:"Соберите пространство целиком",text:"Выберите готовую основу и измените только нужные предметы.",image:"/images/constructor/green.jpeg",mobile:"/images/constructor/green.jpeg",cta:"Выбрать решение",action:()=>{window.location.href=`${process.env.NEXT_PUBLIC_BASE_PATH??""}/ready-solutions/`}},
    {eyebrow:"СЕРВИРОВКА",title:"Предметы для ежедневных ритуалов",text:"Фарфор, стекло и текстиль, которые работают вместе.",image:"/images/time-table.png",mobile:"/images/russian-service-blue.png",cta:"Смотреть каталог",action:()=>openCatalog("Посуда и сервировка")},
  ];
  const active=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[active];
  const categories=[
    {title:"Постельное бельё",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Посуда и сервировка",image:"/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {title:"Пледы и подушки",image:"/images/beige-bedroom.png",category:"Пледы и подушки"},
    {title:"Декор для дома",image:"/images/editorial/caps_led_podyshka.png",category:"Декор для дома"},
    {title:"Свечи и диффузоры",image:"/images/editorial/caps_luna_serviz.png",category:"Свечи и диффузоры"},
    {title:"Для ванной",image:"/images/russian-bedroom.png",category:"Для ванной"},
  ];
  const collectionStories=editorials.slice(0,5);
  const readyBase=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const solutions=[
    {title:"Зеленый салон",space:"СТОЛОВАЯ",image:"/images/constructor/green.jpeg",href:`${readyBase}/ready-solutions/table-1/`},
    {title:"Красные линии",space:"СТОЛОВАЯ",image:"/images/constructor/redline1.jpeg",href:`${readyBase}/ready-solutions/table-2/`},
    {title:"Зимняя сказка",space:"СПАЛЬНЯ",image:"/images/editorial/caps_led.png",href:`${readyBase}/ready-solutions/table-7/`},
    {title:"Тёплый брутализм",space:"КАБИНЕТ",image:"/images/constructor/warm-brutalism.jpeg",href:`${readyBase}/ready-solutions/table-8/`},
  ];
  return <main className="home-v81">
    <nav className="home81-nav" aria-label="Категории">{categories.map(item=><button type="button" key={item.title} onClick={()=>openCatalog(item.category)}>{item.title}</button>)}<button type="button" onClick={()=>go("collections")}>Коллекции</button><a href={`${readyBase}/ready-solutions/`}>Готовые решения</a></nav>
    <section className="home81-hero"><picture><source media="(max-width:700px)" srcSet={assetUrl(hero.mobile)}/><img src={assetUrl(hero.image)} alt={hero.title}/></picture><div><small>{hero.eyebrow}</small><h1>{hero.title}</h1><p>{hero.text}</p><button type="button" onClick={hero.action}>{hero.cta}</button></div><nav>{heroSlides.map((item,index)=><button type="button" aria-label={item.title} className={index===active?"is-active":""} key={item.title} onClick={()=>setSlide(index)}/>)}</nav></section>
    <section className="home81-section home81-categories"><header><small>КАТАЛОГ</small><h2>Для каждой зоны дома</h2><p>Начните с категории или соберите пространство целиком.</p></header><div>{categories.map(item=><button type="button" key={item.title} onClick={()=>openCatalog(item.category)}><span><img src={assetUrl(item.image)} alt={item.title}/></span><strong>{item.title}</strong><small>Смотреть</small></button>)}</div></section>
    <section className="home81-collections"><div className="home81-collections-hero"><img src={assetUrl(collectionStories[0]?.images[0]||"/images/editorial/caps_led.png")} alt="Коллекции Культура Дома"/><div><small>КОЛЛЕКЦИИ</small><h2>Истории, которые связывают предметы</h2><p>Цвет, орнамент и материал продолжаются от сервировки до текстиля и декора.</p><button type="button" onClick={()=>go("collections")}>Все коллекции</button></div></div><div className="home81-collection-rail">{collectionStories.map(item=><button type="button" key={item.id} onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[0])} alt={item.name}/><span>{item.name}</span></button>)}</div></section>
    <section className="home81-section home81-solutions"><header><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2>Выберите настроение — состав можно изменить</h2><p>Готовая композиция становится отправной точкой: количество, коллекции и предметы настраиваются внутри.</p><a href={`${readyBase}/ready-solutions/`}>Все решения</a></header><div>{solutions.map(item=><a href={item.href} key={item.title}><span><img src={assetUrl(item.image)} alt={item.title}/></span><small>{item.space}</small><strong>{item.title}</strong><em>Настроить</em></a>)}</div></section>
    <HomeBoutiques/>
  </main>;
}
'''
    page = page[:home_start] + home + '\n\n' + page[home_end:]

page_path.write_text(page, encoding="utf-8")

# ---------- Final responsive visual system ----------
css = globals_path.read_text(encoding="utf-8")
marker = '/* STOREFRONT_V81 */'
if marker not in css:
    css += r'''

/* STOREFRONT_V81 */
:root{--v81-ink:#171717;--v81-muted:#777;--v81-line:#deddd9;--v81-bg:#fff;--v81-touch:44px}

/* Ready solution header */
.rs71-promo{height:28px;display:flex;align-items:center;justify-content:center;gap:14px;background:#f4f2ee;color:#1b1b1b;font-size:clamp(9px,.68vw,11px);letter-spacing:.08em}.rs71-promo a{text-decoration:underline;text-underline-offset:3px}.rs81-header{height:70px;padding:0 clamp(16px,3vw,48px);display:grid;grid-template-columns:1fr auto 1fr;align-items:center;background:#fff;border-bottom:1px solid #eee;position:relative;z-index:80}.rs81-header-left{display:flex;align-items:center;gap:22px}.rs81-hamburger{width:44px;height:44px;display:grid;align-content:center;gap:5px}.rs81-hamburger i{display:block;width:20px;height:1px;background:#111}.rs81-boutiques,.rs81-header nav a{font-size:12px;text-transform:uppercase;letter-spacing:.06em}.rs81-header .rs71-logo{font-size:clamp(17px,1.5vw,23px);letter-spacing:.16em;white-space:nowrap}.rs81-header nav{justify-self:end;display:flex;align-items:center;gap:clamp(12px,2vw,28px)}

/* Same compact identity block on steps 1/2/3 */
.rs71-shell{max-width:1600px;margin:0 auto;padding:0 clamp(16px,3.4vw,56px) 130px}.rs71-crumbs{margin:18px 0 12px}.rs71-hero.rs81-identity{display:grid!important;grid-template-columns:minmax(240px,38%) 1fr!important;min-height:0!important;height:clamp(170px,18vw,250px)!important;margin:0 0 18px!important;background:#f5f4f1!important;overflow:hidden}.rs71-hero.rs81-identity .rs71-hero-media{height:100%!important;min-height:0!important}.rs71-hero.rs81-identity .rs71-hero-media img{width:100%;height:100%;object-fit:cover}.rs71-hero.rs81-identity .rs71-hero-copy{position:static!important;color:#171717!important;padding:clamp(18px,2.5vw,38px)!important;display:flex!important;flex-direction:column;justify-content:center;align-items:flex-start;text-align:left!important;background:transparent!important}.rs71-hero.rs81-identity h1{font-size:clamp(24px,2.7vw,42px)!important;line-height:1.02;margin:8px 0 10px!important;font-weight:400}.rs71-hero.rs81-identity p{font-size:clamp(12px,.95vw,15px)!important;max-width:560px;margin:0 0 12px!important}.rs71-hero.rs81-identity small,.rs71-hero.rs81-identity span{font-size:clamp(9px,.72vw,11px)!important}.rs71-hero.rs81-identity .rs71-hero-copy>div{display:flex;gap:12px;flex-wrap:wrap}

/* Sticky, touch-safe rails */
.rs71-steps{position:sticky!important;top:0;z-index:55;background:rgba(255,255,255,.97);backdrop-filter:blur(10px);border-bottom:1px solid var(--v81-line);display:flex!important;overflow-x:auto;scrollbar-width:none}.rs71-steps::-webkit-scrollbar,.rs71-group-rail::-webkit-scrollbar,.rs71-filter-rails nav::-webkit-scrollbar{display:none}.rs71-steps button,.rs71-group-rail button,.rs71-filter-rails button,.rs71-person-rail button{min-height:var(--v81-touch);font-size:clamp(11px,.82vw,13px)!important;white-space:nowrap}.rs71-compose .rs71-group-rail{position:sticky;top:45px;z-index:50;background:#fff;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--v81-line)}.rs71-filter-rails{position:sticky;top:90px;z-index:49;background:#fff;padding:4px 0 8px}.rs71-filter-rails nav{display:flex;overflow-x:auto;scrollbar-width:none}.rs71-parameters>header h2,.rs71-compose>header h2{font-size:clamp(26px,3vw,46px)!important}.rs71-parameters>header p,.rs71-compose>header p{font-size:clamp(13px,1vw,16px)!important}.rs71-param-block h3{font-size:clamp(15px,1.25vw,20px)!important}

/* Product cards and checkbox */
.rs71-products{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:clamp(22px,2.5vw,42px) clamp(12px,1.7vw,26px)!important}.rs71-product-media{position:relative;aspect-ratio:1/1;overflow:hidden;background:#f5f4f1}.rs71-product-media img{width:100%;height:100%;object-fit:cover}.rs71-check{position:absolute!important;right:12px!important;bottom:12px!important;top:auto!important;left:auto!important;width:30px!important;height:30px!important;display:grid!important;place-items:center;background:#fff!important;border:0!important;box-shadow:0 0 0 1px rgba(0,0,0,.28)}.rs71-product.is-selected .rs71-check{background:#111!important;color:#fff!important;box-shadow:none}.rs71-product-copy h3{font-size:clamp(13px,1vw,16px)!important}.rs71-product-copy p,.rs71-product-copy strong{font-size:clamp(11px,.84vw,14px)!important}

/* Landing Ready Solutions */
.rs57-landing{max-width:1600px;margin:0 auto;padding:clamp(34px,5vw,80px) clamp(16px,3.4vw,56px) 90px}.rs57-intro.rs60-intro{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,.65fr);align-items:end;padding:0 0 clamp(34px,5vw,70px);border-bottom:1px solid #ddd}.rs57-intro h1{font-size:clamp(38px,6vw,92px)!important;font-weight:400;line-height:.92;letter-spacing:-.04em}.rs57-intro p{font-size:clamp(13px,1.05vw,16px)!important;line-height:1.55;max-width:520px}.rs57-index-head h2{font-size:clamp(24px,2.6vw,42px)!important}.rs62-space-filter{position:sticky;top:0;z-index:45;background:#fff;padding:10px 0;border-bottom:1px solid #ddd}.rs62-filter-rail{display:flex;overflow-x:auto;scrollbar-width:none}.rs62-filter-rail button{min-height:44px;white-space:nowrap;font-size:clamp(11px,.85vw,13px)}.rs57-solution-grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:clamp(34px,4vw,70px) clamp(14px,2vw,30px)!important}.rs57-solution-card{display:block!important;border:0!important;background:#fff!important}.rs57-solution-media{display:block;aspect-ratio:4/5;overflow:hidden;background:#f3f2ef}.rs57-solution-media img{width:100%;height:100%;object-fit:cover;transition:transform .45s ease}.rs57-solution-card:hover .rs57-solution-media img{transform:scale(1.015)}.rs57-solution-copy{padding:14px 0!important}.rs57-solution-copy h3{font-size:clamp(20px,1.8vw,30px)!important;font-weight:400}.rs57-solution-copy p{font-size:clamp(11px,.85vw,13px)!important}.rs57-card-cta{min-height:44px;display:inline-flex;align-items:center;border-bottom:1px solid #111!important;font-size:11px!important}

/* Collections landing */
.collections-v52{background:#fff}.collections-v52-intro{max-width:1600px;margin:0 auto;padding:clamp(48px,7vw,110px) clamp(16px,4vw,64px) clamp(30px,5vw,72px);display:grid;grid-template-columns:1fr minmax(280px,.6fr);align-items:end;border-bottom:1px solid #ddd}.collections-v52-intro h1{font-size:clamp(44px,7vw,108px)!important;font-weight:400;line-height:.9;letter-spacing:-.045em}.collections-v52-intro p{font-size:clamp(13px,1.05vw,16px)!important;line-height:1.6}.collections-v52-index{max-width:1600px;margin:0 auto;padding:clamp(28px,4vw,60px) clamp(16px,4vw,64px) 100px;display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:clamp(38px,5vw,80px) clamp(14px,2vw,30px)!important}.collections-v52-card{display:block!important;border:0!important}.collections-v52-card-media{display:block;width:100%;aspect-ratio:4/5;overflow:hidden;background:#f3f2ef}.collections-v52-card-media img{width:100%;height:100%;object-fit:cover}.collections-v52-card-copy{padding:14px 0!important}.collections-v52-card-copy h2{font-size:clamp(22px,2vw,34px)!important;font-weight:400}.collections-v52-card-copy p{font-size:clamp(12px,.9vw,14px)!important;line-height:1.5}.v52-story-products{grid-template-columns:repeat(3,minmax(0,1fr))!important}

/* Homepage */
.home-v81{background:#fff;color:#171717}.home81-nav{height:50px;display:flex;align-items:center;gap:clamp(18px,2.5vw,38px);padding:0 clamp(16px,3vw,48px);overflow-x:auto;scrollbar-width:none;border-bottom:1px solid #e6e4df;position:relative;z-index:10}.home81-nav::-webkit-scrollbar{display:none}.home81-nav button,.home81-nav a{min-height:44px;display:flex;align-items:center;white-space:nowrap;background:none;border:0;font-size:clamp(10px,.75vw,12px);text-transform:uppercase;letter-spacing:.06em}.home81-hero{height:min(78vh,860px);min-height:520px;position:relative;overflow:hidden}.home81-hero picture,.home81-hero picture img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.home81-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.42),rgba(0,0,0,.04) 62%)}.home81-hero>div{position:absolute;z-index:2;left:clamp(20px,6vw,90px);bottom:clamp(50px,9vw,130px);max-width:590px;color:#fff}.home81-hero h1{font-size:clamp(42px,6vw,92px);line-height:.93;font-weight:400;letter-spacing:-.045em;margin:10px 0 18px}.home81-hero p{font-size:clamp(13px,1.1vw,17px);line-height:1.5;max-width:470px}.home81-hero>div button,.home81-collections-hero button{margin-top:22px;min-height:44px;padding:0 0;border:0;border-bottom:1px solid currentColor;background:none;color:inherit;font-size:11px;text-transform:uppercase;letter-spacing:.08em}.home81-hero>nav{position:absolute;z-index:3;left:clamp(20px,6vw,90px);bottom:24px;display:flex;gap:8px}.home81-hero>nav button{width:42px;height:3px;border:0;background:rgba(255,255,255,.45);padding:0}.home81-hero>nav button.is-active{background:#fff}.home81-section{padding:clamp(60px,8vw,120px) clamp(16px,4vw,64px)}.home81-section>header{max-width:760px;margin-bottom:clamp(30px,4vw,58px)}.home81-section>header h2{font-size:clamp(34px,4.5vw,70px);line-height:1;font-weight:400;letter-spacing:-.035em;margin:8px 0 14px}.home81-section>header p{font-size:clamp(13px,1vw,16px);line-height:1.55}.home81-categories>div{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(28px,4vw,60px) clamp(12px,2vw,28px)}.home81-categories>div button{border:0;background:none;text-align:left;padding:0}.home81-categories>div button>span{display:block;aspect-ratio:4/5;overflow:hidden;background:#f3f2ef}.home81-categories img{width:100%;height:100%;object-fit:cover}.home81-categories strong{display:block;font-size:clamp(16px,1.5vw,24px);font-weight:400;margin:12px 0 4px}.home81-categories small{font-size:10px;text-transform:uppercase;text-decoration:underline;text-underline-offset:4px}.home81-collections{padding:0 clamp(16px,4vw,64px) clamp(70px,9vw,130px)}.home81-collections-hero{height:min(70vh,760px);position:relative;overflow:hidden}.home81-collections-hero>img{width:100%;height:100%;object-fit:cover}.home81-collections-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.38),transparent 60%)}.home81-collections-hero>div{position:absolute;z-index:2;left:clamp(20px,5vw,70px);bottom:clamp(30px,6vw,80px);max-width:520px;color:#fff}.home81-collections-hero h2{font-size:clamp(36px,5vw,74px);font-weight:400;line-height:.95;margin:8px 0 14px}.home81-collection-rail{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:12px}.home81-collection-rail button{border:0;background:none;padding:0;text-align:left}.home81-collection-rail img{width:100%;aspect-ratio:1/1;object-fit:cover}.home81-collection-rail span{display:block;margin-top:8px;font-size:clamp(12px,.95vw,15px)}.home81-solutions>header{position:relative}.home81-solutions>header>a{display:inline-block;margin-top:10px;border-bottom:1px solid #111;font-size:11px;text-transform:uppercase}.home81-solutions>div{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,1.6vw,24px)}.home81-solutions>div>a>span{display:block;aspect-ratio:4/5;overflow:hidden;background:#f3f2ef}.home81-solutions img{width:100%;height:100%;object-fit:cover}.home81-solutions a small,.home81-solutions a strong,.home81-solutions a em{display:block}.home81-solutions a small{margin-top:12px;font-size:9px;letter-spacing:.08em}.home81-solutions a strong{font-size:clamp(17px,1.5vw,24px);font-weight:400;margin:5px 0}.home81-solutions a em{font-style:normal;font-size:10px;text-decoration:underline;text-underline-offset:4px}

@media(max-width:1100px){.rs71-products{grid-template-columns:repeat(3,minmax(0,1fr))!important}.rs57-solution-grid,.collections-v52-index{grid-template-columns:repeat(2,minmax(0,1fr))!important}.v52-story-products{grid-template-columns:repeat(2,minmax(0,1fr))!important}.home81-solutions>div{grid-template-columns:repeat(2,minmax(0,1fr))}.home81-collection-rail{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){:root{--v81-touch:48px}.rs71-promo{height:24px}.rs81-header{height:56px;padding:0 14px;grid-template-columns:44px 1fr auto}.rs81-boutiques{display:none}.rs81-header-left{gap:0}.rs81-header .rs71-logo{justify-self:center;font-size:15px}.rs81-header nav{gap:0}.rs81-header nav a{display:none}.rs81-header nav a:last-child{display:flex;min-width:44px;min-height:44px;align-items:center;justify-content:flex-end;font-size:10px}.rs71-shell{padding:0 14px 110px}.rs71-crumbs{margin:10px 0}.rs71-hero.rs81-identity{grid-template-columns:38% 62%!important;height:132px!important;margin-bottom:10px!important}.rs71-hero.rs81-identity .rs71-hero-copy{padding:12px!important}.rs71-hero.rs81-identity h1{font-size:clamp(19px,6vw,25px)!important;margin:4px 0 6px!important}.rs71-hero.rs81-identity p{display:none}.rs71-hero.rs81-identity .rs71-hero-copy>div{gap:6px;max-height:28px;overflow:hidden}.rs71-steps{margin:0 -14px;padding:0 14px}.rs71-steps button{flex:0 0 auto;padding:0 18px!important}.rs71-compose .rs71-group-rail{top:48px;margin:0 -14px;padding:0 14px}.rs71-filter-rails{top:96px;margin:0 -14px;padding:4px 14px 8px}.rs71-products{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:26px 10px!important}.rs71-check{right:8px!important;bottom:8px!important;width:32px!important;height:32px!important}.rs71-collection-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.rs71-commerce{min-height:72px!important}.rs57-landing{padding:30px 14px 70px}.rs57-intro.rs60-intro,.collections-v52-intro{grid-template-columns:1fr;gap:18px}.rs57-intro h1{font-size:48px!important}.rs57-solution-grid,.collections-v52-index{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:34px 10px!important}.rs57-solution-copy p,.rs57-person-badges,.rs57-solution-copy>div:not(.rs57-person-badges){display:none!important}.rs57-solution-media,.collections-v52-card-media{aspect-ratio:3/4}.rs57-solution-copy h3{font-size:17px!important}.collections-v52-intro{padding:42px 14px 28px}.collections-v52-intro h1{font-size:54px!important}.collections-v52-index{padding:28px 14px 70px}.collections-v52-card-copy p{display:none}.collections-v52-card-copy h2{font-size:18px!important}.v52-story-products{grid-template-columns:repeat(2,minmax(0,1fr))!important}.home81-nav{padding:0 14px;gap:22px}.home81-hero{height:72svh;min-height:520px}.home81-hero:after{background:linear-gradient(0deg,rgba(0,0,0,.5),transparent 70%)}.home81-hero>div{left:18px;right:18px;bottom:64px}.home81-hero h1{font-size:46px}.home81-section{padding:58px 14px}.home81-section>header h2{font-size:38px}.home81-categories>div{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 10px}.home81-categories strong{font-size:15px}.home81-collections{padding:0 14px 70px}.home81-collections-hero{height:66svh}.home81-collections-hero>div{left:18px;right:18px;bottom:28px}.home81-collections-hero h2{font-size:40px}.home81-collection-rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px}.home81-collection-rail button{flex:0 0 42%;scroll-snap-align:start}.home81-solutions>div{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 10px}.home81-solutions a strong{font-size:16px}}
'''
    globals_path.write_text(css, encoding="utf-8")

print("Applied storefront V81: ready solutions, collections, Echo media and homepage")
