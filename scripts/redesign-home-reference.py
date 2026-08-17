from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

new_home = r'''function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void }) {
  const homeSlides=[
    {category:"СПАЛЬНЯ",image:"/images/blue-bedroom.png",destination:"catalog" as View},
    {category:"РАСПРОДАЖА",image:"/images/russian-bedroom.png",destination:"catalog" as View},
    {category:"КУХНЯ И СТОЛОВАЯ",image:"/images/buyan-editorial.png",destination:"catalog" as View},
    {category:"ДЕКОР ДЛЯ ДОМА",image:"/images/beige-bedroom.png",destination:"catalog" as View},
  ];
  const activeIndex=((slide%homeSlides.length)+homeSlides.length)%homeSlides.length;
  const current=homeSlides[activeIndex];
  const homeCategories=[
    ["Кухня и столовая","/images/moon-plate.png"],
    ["Домашний текстиль","/images/russian-bedroom.png"],
    ["Спальня","/images/classic-bedroom.png"],
    ["Декор для дома","/images/zip-product-bed.png"],
    ["Аутлет","/images/beige-bedroom.png"],
  ] as const;
  const bestsellers=[1,2,7,12].map(id=>products.find(product=>product.id===id)!).filter(Boolean);

  return <>
    <section className="hero home-reference-hero">
      <div className="hero-media"><img src={assetUrl(current.image)} alt={current.category}/></div>
      <div className="hero-shade"/>
      <button className="hero-arrow prev" onClick={() => setSlide((activeIndex + homeSlides.length - 1) % homeSlides.length)} aria-label="Предыдущий баннер"><Icon name="chevron"/></button>
      <button className="hero-arrow next" onClick={() => setSlide((activeIndex + 1) % homeSlides.length)} aria-label="Следующий баннер"><Icon name="chevron"/></button>
      <div className="hero-dots">{homeSlides.map((_,i)=><button key={i} className={i===activeIndex?"active":""} onClick={()=>setSlide(i)} aria-label={`Баннер ${i+1}`}/>)}</div>
      <nav className="hero-nav">{homeSlides.map((item,i)=><button key={item.category} className={i===activeIndex?"active":""} onClick={()=>setSlide(i)}>{item.category}</button>)}</nav>
    </section>

    <section className="home-reference-shelf">
      <div className="home-reference-heading"><p>ДЛЯ ВАШЕГО ДОМА</p><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>
      <div className="category-grid">{homeCategories.map(([name,image],i)=><button className="category-card" key={name} onClick={()=>i===2?go("catalog"):go("catalog")}><img src={assetUrl(image)} alt={name}/><span>{name}</span><b>Смотреть категорию →</b></button>)}</div>
    </section>

    <section className="home-reference-products">
      <div className="home-reference-products-head"><div><p>ВЫБОР РЕДАКЦИИ · СПАЛЬНЯ</p><h2>ХИТЫ ПРОДАЖ</h2></div><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>
      <ProductRail className="home-product-rail" items={bestsellers} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="manifest home-reference-manifest"><p>КУЛЬТУРА ДОМА</p><h2>Предметы, с которыми остаётся вечное</h2><span>Натуральные материалы, ручная работа и образы русской культуры —<br/>для современного дома и личных семейных историй.</span><button onClick={()=>go("collections")}>УЗНАТЬ О БРЕНДЕ →</button></section>
  </>;
}'''

pattern = r'function HomeView\([\s\S]*?\n}\n\nfunction CatalogView'
if not re.search(pattern, page):
    raise SystemExit("HomeView block not found")
page = re.sub(pattern, new_home + '\n\nfunction CatalogView', page, count=1)
page_path.write_text(page, encoding="utf-8")

css = re.sub(r'\n?/\* HOME_REFERENCE_REDESIGN_V1 \*/[\s\S]*?/\* END_HOME_REFERENCE_REDESIGN_V1 \*/', '', css)
css += r'''

/* HOME_REFERENCE_REDESIGN_V1 */
.view-home{background:#fff}
.view-home .header{
  position:absolute!important;
  top:31px!important;
  left:0!important;
  right:0!important;
  width:100%!important;
  height:72px!important;
  z-index:30!important;
  background:transparent!important;
  border:0!important;
  color:#fff!important;
  backdrop-filter:none!important;
}
.view-home .header .logo,.view-home .header button{color:#fff!important}
.view-home .header .hamburger i{background:#fff!important}
.view-home .header svg{stroke:currentColor}
.view-home .header .bag b,.view-home .header .favorite-header b{box-shadow:0 0 0 2px rgba(255,255,255,.18)}
.view-home .promo{position:relative;z-index:31;height:31px;background:#31494b}
.home-reference-hero{
  height:min(720px,calc(100svh - 31px))!important;
  min-height:600px!important;
  margin:0!important;
  position:relative!important;
  overflow:hidden!important;
  background:#ddd!important;
}
.home-reference-hero .hero-media{position:absolute;inset:0}
.home-reference-hero .hero-media img{width:100%;height:100%;object-fit:cover;object-position:center;transition:opacity .25s ease,transform .6s ease}
.home-reference-hero .hero-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,15,18,.22) 0%,transparent 25%,transparent 72%,rgba(9,13,15,.24) 100%)}
.home-reference-hero .hero-arrow{top:51%;z-index:4;color:#fff;opacity:.9;padding:12px}
.home-reference-hero .hero-arrow svg{width:33px;height:33px;stroke-width:1.2}
.home-reference-hero .hero-arrow.prev{left:22px}
.home-reference-hero .hero-arrow.next{right:22px}
.home-reference-hero .hero-dots{z-index:5;bottom:54px;gap:8px}
.home-reference-hero .hero-dots button{width:4px;height:4px;background:rgba(255,255,255,.58)}
.home-reference-hero .hero-dots button.active{background:#fff;transform:scale(1.45)}
.home-reference-hero .hero-nav{
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  z-index:5;
  height:48px;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:42px;
  border:0;
  color:#fff;
  background:linear-gradient(180deg,transparent,rgba(8,11,12,.18));
}
.home-reference-hero .hero-nav button{height:48px;padding:17px 0 12px;color:#fff;font-size:9px;letter-spacing:.08em;border-bottom:1px solid transparent;opacity:.88}
.home-reference-hero .hero-nav button.active{border-color:#fff;opacity:1}
.home-reference-shelf{padding:30px 26px 42px;background:#fff}
.home-reference-heading,.home-reference-products-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:18px}
.home-reference-heading p,.home-reference-products-head p{margin:0;font-size:9px;letter-spacing:.17em;color:#4e5350}
.home-reference-heading button,.home-reference-products-head>button{font-size:8px;letter-spacing:.09em;border-bottom:1px solid #6e706c;padding:0 0 5px;white-space:nowrap}
.home-reference-shelf .category-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));grid-template-rows:none;gap:6px}
.home-reference-shelf .category-card{grid-column:auto!important;grid-row:auto!important;aspect-ratio:.88/1;padding:16px 14px;justify-content:flex-end}
.home-reference-shelf .category-card:after{background:linear-gradient(180deg,transparent 54%,rgba(0,0,0,.55))}
.home-reference-shelf .category-card span{font-size:18px;line-height:1.05}
.home-reference-shelf .category-card b{font-size:7px;letter-spacing:.08em;margin-top:6px;font-weight:400}
.home-reference-products{padding:30px 26px 48px;background:#fff}
.home-reference-products-head{margin-bottom:22px}
.home-reference-products-head h2{margin:8px 0 0;font-size:31px;line-height:1;font-weight:400;letter-spacing:.01em}
.home-reference-products .product-rail-shell{overflow:visible!important}
.home-reference-products .product-rail{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:16px!important;overflow:visible!important;padding:0!important}
.home-reference-products .product-card{min-width:0!important}
.home-reference-products .product-image img{aspect-ratio:1/1.08!important;object-fit:cover!important}
.home-reference-products .product-copy{padding-top:9px}
.home-reference-products .product-copy strong{font-size:16px;line-height:1.08}
.home-reference-products .product-copy small{font-size:8px;line-height:1.35}
.home-reference-products .price{font-size:14px;margin-top:8px}
.home-reference-products .price del{font-size:9px}
.home-reference-products .quick{bottom:7px}
.home-reference-products .heart svg{width:30px;height:30px}
.home-reference-manifest{padding:90px 20px 84px!important;background:#f2efe9!important}
.home-reference-manifest p{font-size:8px!important;letter-spacing:.2em!important;margin-bottom:19px!important}
.home-reference-manifest h2{font-size:39px!important;line-height:1.08!important;margin-bottom:24px!important}
.home-reference-manifest span{font-size:11px!important;line-height:1.8!important;color:#777!important}
.home-reference-manifest button{font-size:8px!important;margin-top:31px!important}
@media(max-width:900px){
  .view-home .header{height:62px!important;padding:0 16px!important}
  .view-home .header .boutiques{display:none!important}
  .view-home .header .logo{font-size:20px!important}
  .view-home .header-actions{gap:10px!important}
  .view-home .header-actions svg{width:23px!important;height:23px!important}
  .view-home .header-left{gap:10px!important}
  .home-reference-hero{height:72svh!important;min-height:520px!important}
  .home-reference-hero .hero-arrow{display:none!important}
  .home-reference-hero .hero-dots{bottom:50px!important}
  .home-reference-hero .hero-nav{justify-content:flex-start!important;gap:24px!important;overflow-x:auto!important;padding:0 16px!important;scrollbar-width:none!important}
  .home-reference-hero .hero-nav::-webkit-scrollbar{display:none!important}
  .home-reference-hero .hero-nav button{flex:0 0 auto!important;font-size:8px!important}
  .home-reference-shelf{padding:24px 16px 36px!important;overflow:hidden}
  .home-reference-shelf .category-grid{display:flex!important;gap:7px!important;overflow-x:auto!important;scroll-snap-type:x mandatory!important;scrollbar-width:none!important;margin-right:-16px;padding-right:16px}
  .home-reference-shelf .category-grid::-webkit-scrollbar{display:none!important}
  .home-reference-shelf .category-card{flex:0 0 54vw!important;aspect-ratio:.88/1!important;scroll-snap-align:start!important}
  .home-reference-products{padding:24px 16px 40px!important;overflow:hidden}
  .home-reference-products-head h2{font-size:27px!important}
  .home-reference-products .product-rail{display:flex!important;gap:10px!important;overflow-x:auto!important;scroll-snap-type:x mandatory!important;margin-right:-16px!important;padding-right:16px!important;scrollbar-width:none!important}
  .home-reference-products .product-rail::-webkit-scrollbar{display:none!important}
  .home-reference-products .product-card{flex:0 0 72vw!important;scroll-snap-align:start!important}
  .home-reference-manifest{padding:72px 22px 68px!important}
  .home-reference-manifest h2{font-size:30px!important}
  .home-reference-manifest span br{display:none}
}
@media(max-width:520px){
  .view-home .header .favorite-header{display:none!important}
  .view-home .header .logo{font-size:18px!important}
  .home-reference-hero{height:68svh!important;min-height:480px!important}
  .home-reference-heading,.home-reference-products-head{align-items:center!important}
  .home-reference-products-head h2{font-size:25px!important}
  .home-reference-shelf .category-card{flex-basis:62vw!important}
  .home-reference-products .product-card{flex-basis:78vw!important}
}
/* END_HOME_REFERENCE_REDESIGN_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Applied screenshot-inspired homepage redesign")
