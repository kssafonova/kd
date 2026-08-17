from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# Make sure the Ice Patterns collection exists as its own editorial destination.
if 'id:"ice"' not in page:
    ice = r'''  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле. Белый, ледяной голубой и деликатный орнамент создают ощущение тихого зимнего утра.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/images/editorial/caps_led.png","/images/editorial/caps_led_podyshka.png","/images/editorial/caps_led_podyshka2.png","/images/editorial/caps_led_serviz.png"], productIds:[12,3,6,2] },
'''
    marker = 'const editorials:Editorial[] = [\n'
    if marker not in page:
        raise SystemExit("Editorial collection list not found")
    page = page.replace(marker, marker + ice, 1)

# HomeView needs a direct editorial opener so cards do not route through the collection index.
old_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}'
new_render = '{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
if old_render in page:
    page = page.replace(old_render, new_render, 1)
elif 'openEditorial={(item)=>{setEditorial(item);go("editorial")}}' not in page:
    raise SystemExit("HomeView render not found")

old_signature = 'function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void }) {'
new_signature = 'function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {'
if old_signature in page:
    page = page.replace(old_signature, new_signature, 1)
elif 'openEditorial:(editorial:Editorial)=>void' not in page:
    raise SystemExit("HomeView signature not found")

feature = r'''

    <section className="home-bedroom-collections" aria-labelledby="home-bedroom-collections-title">
      <header className="home-bedroom-collections-head">
        <div>
          <p>ДЛЯ СПАЛЬНИ</p>
          <h2 id="home-bedroom-collections-title">Коллекции и истории</h2>
        </div>
        <span>Текстиль, свет и детали для личного пространства.</span>
      </header>

      <div className="home-collection-duo">
        <button className="home-collection-feature home-collection-feature-luna" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="luna")!)}>
          <img src={assetUrl("/images/editorial/caps_luna_postel.png")} alt="Коллекция Лунная сказка"/>
          <span className="home-collection-feature-shade"/>
          <span className="home-collection-feature-copy">
            <small>КОЛЛЕКЦИЯ · СПАЛЬНЯ</small>
            <strong>Лунная сказка</strong>
            <em>СМОТРЕТЬ ИСТОРИИ →</em>
          </span>
        </button>

        <button className="home-collection-feature home-collection-feature-ice" type="button" onClick={()=>openEditorial(editorials.find(item=>item.id==="ice")!)}>
          <img src={assetUrl("/images/editorial/caps_led.png")} alt="Коллекция Ледяные узоры"/>
          <span className="home-collection-feature-shade"/>
          <span className="home-collection-feature-copy">
            <small>КОЛЛЕКЦИЯ · СПАЛЬНЯ</small>
            <strong>Ледяные узоры</strong>
            <em>СМОТРЕТЬ ИСТОРИИ →</em>
          </span>
        </button>
      </div>
    </section>'''

# Remove any earlier version of this homepage feature before inserting the current one.
page = re.sub(r'\n\s*<section className="home-bedroom-feature">[\s\S]*?</section>', '', page, count=1)
page = re.sub(r'\n\s*<section className="home-bedroom-collections"[\s\S]*?</section>', '', page, count=1)
page = re.sub(r'\n\s*<section className="home-collection-duo"[\s\S]*?</section>', '', page, count=1)
anchor = '    <section className="home-reference-products">'
if anchor not in page:
    raise SystemExit("Homepage products anchor not found")
page = page.replace(anchor, feature + "\n\n" + anchor, 1)

# Give Ice Patterns a bedroom/story editorial treatment instead of the folklore fallback.
page = page.replace(
    'const variant=editorial.id==="time"?"cinematic":editorial.id==="buyan"?"offset":editorial.id==="poetry"?"magazine":"gallery";',
    'const variant=editorial.id==="time"||editorial.id==="ice"?"cinematic":editorial.id==="buyan"?"offset":editorial.id==="poetry"?"magazine":"gallery";'
)
page = page.replace(
    'const chapter=editorial.id==="time"?"NIGHT STUDY":editorial.id==="buyan"?"SUMMER TABLE":editorial.id==="poetry"?"POETRY OF HOME":"FOLKLORE REFRAMED";',
    'const chapter=editorial.id==="ice"?"BEDROOM STORIES":editorial.id==="time"?"NIGHT STUDY":editorial.id==="buyan"?"SUMMER TABLE":editorial.id==="poetry"?"POETRY OF HOME":"FOLKLORE REFRAMED";'
)
page = page.replace(
    'const index=editorial.id==="time"?"01":editorial.id==="buyan"?"02":editorial.id==="poetry"?"03":"04";',
    'const index=editorial.id==="time"?"01":editorial.id==="ice"?"02":editorial.id==="buyan"?"03":editorial.id==="poetry"?"04":"05";'
)

page_path.write_text(page, encoding="utf-8")

# Replace previous feature CSS with the paired bedroom collection system.
css = re.sub(r'\n?/\* HOME_BEDROOM_FEATURE_V1 \*/[\s\S]*?/\* END_HOME_BEDROOM_FEATURE_V1 \*/', '', css)
css = re.sub(r'\n?/\* HOME_COLLECTION_DUO_V2 \*/[\s\S]*?/\* END_HOME_COLLECTION_DUO_V2 \*/', '', css)
css = re.sub(r'\n?/\* HOME_BEDROOM_COLLECTIONS_V3 \*/[\s\S]*?/\* END_HOME_BEDROOM_COLLECTIONS_V3 \*/', '', css)
css += r'''

/* HOME_BEDROOM_COLLECTIONS_V3 */
.home-bedroom-collections{
  padding:44px 26px 50px;
  background:#fff;
}
.home-bedroom-collections-head{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:36px;
  padding:0 0 20px;
}
.home-bedroom-collections-head>div{display:grid;gap:8px}
.home-bedroom-collections-head p{
  margin:0;
  font-size:9px;
  line-height:1;
  letter-spacing:.18em;
  color:#555b58;
}
.home-bedroom-collections-head h2{
  margin:0;
  font-size:31px;
  line-height:1;
  font-weight:400;
  letter-spacing:-.015em;
}
.home-bedroom-collections-head>span{
  max-width:350px;
  padding-bottom:2px;
  color:#7b7e7b;
  font-size:10px;
  line-height:1.55;
  text-align:right;
}
.home-collection-duo{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:7px;
  width:100%;
}
.home-collection-feature{
  position:relative;
  display:block;
  width:100%;
  min-height:680px;
  padding:0;
  overflow:hidden;
  background:#e9e9e6;
  color:#fff;
  text-align:left;
}
.home-collection-feature>img{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center;
  transition:transform .7s ease;
}
.home-collection-feature:hover>img{transform:scale(1.018)}
.home-collection-feature-shade{
  position:absolute;
  inset:0;
  background:linear-gradient(180deg,rgba(8,12,16,.01) 35%,rgba(8,12,16,.65) 100%);
}
.home-collection-feature-copy{
  position:absolute;
  z-index:2;
  left:34px;
  right:34px;
  bottom:34px;
  display:flex;
  flex-direction:column;
  align-items:flex-start;
}
.home-collection-feature-copy small{
  margin-bottom:12px;
  font-size:8px;
  line-height:1;
  letter-spacing:.18em;
  font-style:normal;
}
.home-collection-feature-copy strong{
  max-width:92%;
  font-size:clamp(38px,4.4vw,70px);
  line-height:.95;
  font-weight:400;
  letter-spacing:-.025em;
}
.home-collection-feature-copy em{
  margin-top:24px;
  padding-bottom:5px;
  border-bottom:1px solid rgba(255,255,255,.92);
  font-size:8px;
  line-height:1;
  letter-spacing:.1em;
  font-style:normal;
}
.home-collection-feature-luna>img{object-position:center 54%}
.home-collection-feature-ice>img{object-position:center 48%}
@media(max-width:900px){
  .home-bedroom-collections{padding:34px 16px 40px}
  .home-bedroom-collections-head{align-items:flex-start;padding-bottom:16px}
  .home-bedroom-collections-head h2{font-size:28px}
  .home-bedroom-collections-head>span{max-width:250px;font-size:9px}
  .home-collection-duo{grid-template-columns:1fr;gap:7px}
  .home-collection-feature{min-height:72svh;max-height:760px}
  .home-collection-feature-copy{left:22px;right:22px;bottom:28px}
  .home-collection-feature-copy strong{font-size:48px}
}
@media(max-width:520px){
  .home-bedroom-collections{padding:30px 0 32px}
  .home-bedroom-collections-head{display:block;padding:0 16px 16px}
  .home-bedroom-collections-head h2{font-size:25px;margin-top:7px}
  .home-bedroom-collections-head>span{display:block;max-width:310px;margin-top:10px;text-align:left;font-size:9px}
  .home-collection-duo{gap:4px}
  .home-collection-feature{min-height:620px}
  .home-collection-feature-copy{left:18px;right:18px;bottom:24px}
  .home-collection-feature-copy small{font-size:7px;margin-bottom:10px}
  .home-collection-feature-copy strong{font-size:39px}
  .home-collection-feature-copy em{font-size:7px;margin-top:20px}
}
/* END_HOME_BEDROOM_COLLECTIONS_V3 */
'''
css_path.write_text(css, encoding="utf-8")
print("Added direct bedroom collection story links for Luna and Ice Patterns")
