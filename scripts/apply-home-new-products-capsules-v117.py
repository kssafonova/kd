from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
CSS = ROOT / "app" / "globals.css"

page = PAGE.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
marker = "HOME_NEW_PRODUCTS_CAPSULES_V117"
page_changed = False

if marker not in page:
    old_void = "  void onProduct; void favorite; void favorites; void onAdd; void openEditorial;"
    if old_void not in page:
        raise SystemExit("HOME_NEW_PRODUCTS_CAPSULES_V117: HomeView callback guard not found")
    page = page.replace(old_void, "  void openEditorial;", 1)

    capsule_data_pattern = re.compile(r"  const capsules=\[\n.*?\n  \];\n  const solutions=\[", re.S)
    capsule_data_replacement = '''  const newProducts=products.slice(0,12);\n  const capsules=[\n    {title:"Нити",meta:"КАПСУЛА · ТЕКСТИЛЬ",imageIndex:7},\n    {title:"Тайна",meta:"КАПСУЛА · ТЁМНАЯ ЭСТЕТИКА",imageIndex:22},\n    {title:"Ледяные узоры",meta:"КАПСУЛА · ЗИМНЯЯ ИСТОРИЯ",imageIndex:18},\n    {title:"Лунная сказка",meta:"КАПСУЛА · СПАЛЬНЯ И СЕРВИРОВКА",imageIndex:12},\n    {title:"Феникс",meta:"КАПСУЛА · ДЕКОР",imageIndex:9},\n  ];\n  const solutions=['''
    page, data_count = capsule_data_pattern.subn(capsule_data_replacement, page, count=1)
    if data_count != 1:
        raise SystemExit(f"HOME_NEW_PRODUCTS_CAPSULES_V117: capsule data patch count={data_count}")

    section_pattern = re.compile(
        r'(\n    <section className="home113-section home113-category-section">.*?</section>\n)'
        r'\n    <section className="home113-capsules">.*?</section>\n\n'
        r'    <section className="home113-solutions">',
        re.S,
    )

    def replace_sections(match: re.Match[str]) -> str:
        return match.group(1) + r'''
    {/* HOME_NEW_PRODUCTS_CAPSULES_V117 */}
    <section className="home117-new-products" aria-labelledby="home117-new-products-title">
      <header className="home117-section-head"><div><small>КАТАЛОГ</small><h2 id="home117-new-products-title">Новинки</h2></div><button type="button" onClick={()=>openCatalog()}>Смотреть все</button></header>
      <div className="home117-product-rail" aria-label="Новинки товаров">{newProducts.map(product=><div className="home117-product-item" key={`home-new-${product.id}`}><ProductCard product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/></div>)}</div>
    </section>

    <section className="home113-capsules home117-capsules" aria-labelledby="home117-capsules-title">
      <header className="home117-section-head home117-capsules-head"><div><small>КАПСУЛЫ</small><h2 id="home117-capsules-title">Капсулы</h2></div><button type="button" onClick={()=>go("collections")}>Смотреть все</button></header>
      <div className="home117-capsule-rail" aria-label="Капсулы Культура дома">{capsules.map(item=><article className="home117-capsule-card" key={item.title}>
        <button type="button" className="home117-capsule-media" onClick={()=>go("collections")} aria-label={`Открыть капсулу ${item.title}`}><span role="img" aria-label={item.title} style={atlasStyle(item.imageIndex)}/></button>
        <div className="home117-capsule-copy"><small>{item.meta}</small><button type="button" onClick={()=>go("collections")}><h3>{item.title}</h3></button><button type="button" className="home117-capsule-link" onClick={()=>go("collections")}>Смотреть капсулу</button></div>
      </article>)}</div>
    </section>

    <section className="home113-solutions">'''

    page, section_count = section_pattern.subn(replace_sections, page, count=1)
    if section_count != 1:
        raise SystemExit(f"HOME_NEW_PRODUCTS_CAPSULES_V117: homepage section patch count={section_count}")
    page_changed = True

css = re.sub(
    r"\n?/\* HOME_NEW_PRODUCTS_CAPSULES_V117 \*/.*?/\* END_HOME_NEW_PRODUCTS_CAPSULES_V117 \*/\n?",
    "\n",
    css,
    flags=re.S,
)

css_block = r'''
/* HOME_NEW_PRODUCTS_CAPSULES_V117 */
.home117-new-products{padding:clamp(58px,7vw,104px) 0 clamp(72px,8vw,120px);background:#f7f5ef;color:#171815}
.home117-section-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;padding:0 clamp(20px,4.2vw,64px) 30px}
.home117-section-head small{display:block;margin-bottom:10px;font:500 10px/1.2 Arial,sans-serif;letter-spacing:.17em;text-transform:uppercase;color:rgba(23,24,21,.62)}
.home117-section-head h2{margin:0;font-family:"Tenor Sans",Georgia,serif;font-size:clamp(32px,4.2vw,58px);font-weight:400;line-height:1;letter-spacing:-.02em}
.home117-section-head>button{border:0;border-bottom:1px solid currentColor;background:none;padding:0 0 5px;color:inherit;font:500 10px/1.2 Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
.home117-product-rail{display:flex;gap:clamp(12px,1.35vw,22px);overflow-x:auto;overscroll-behavior-inline:contain;scroll-snap-type:x proximity;scrollbar-width:none;padding:0 clamp(20px,4.2vw,64px) 12px}
.home117-product-rail::-webkit-scrollbar,.home117-capsule-rail::-webkit-scrollbar{display:none}
.home117-product-item{flex:0 0 clamp(260px,23.5vw,360px);min-width:0;scroll-snap-align:start}
.home117-product-item .product-card{width:100%;height:100%;margin:0}
.home117-product-item .product-image{width:100%}
.home113-capsules.home117-capsules{padding:clamp(70px,8vw,126px) 0 clamp(84px,9vw,138px);background:#efede7;color:#171815}
.home117-capsules-head{padding-bottom:34px}
.home117-capsule-rail{display:flex;gap:clamp(18px,2vw,32px);overflow-x:auto;overscroll-behavior-inline:contain;scroll-snap-type:x mandatory;scrollbar-width:none;padding:0 clamp(20px,4.2vw,64px) 14px}
.home117-capsule-card{flex:0 0 min(39vw,590px);min-width:340px;scroll-snap-align:start}
.home117-capsule-media{display:block;width:100%;padding:0;border:0;background:#ddd8ce;cursor:pointer;overflow:hidden}
.home117-capsule-media>span{display:block;width:100%;aspect-ratio:4/5;background-repeat:no-repeat;transition:transform .55s cubic-bezier(.2,.7,.2,1)}
.home117-capsule-card:hover .home117-capsule-media>span{transform:scale(1.012)}
.home117-capsule-copy{padding-top:18px}
.home117-capsule-copy>small{display:block;margin-bottom:8px;font:500 9px/1.25 Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:rgba(23,24,21,.58)}
.home117-capsule-copy>button{border:0;background:none;padding:0;color:inherit;text-align:left;cursor:pointer}
.home117-capsule-copy h3{margin:0;font-family:"Tenor Sans",Georgia,serif;font-size:clamp(25px,2.25vw,36px);font-weight:400;line-height:1.08}
.home117-capsule-link{margin-top:12px!important;padding-bottom:4px!important;border-bottom:1px solid currentColor!important;font:500 10px/1.2 Arial,sans-serif!important;letter-spacing:.12em!important;text-transform:uppercase}
@media(max-width:900px){
  .home117-new-products{padding:48px 0 64px}
  .home117-section-head{align-items:flex-end;padding:0 16px 22px}
  .home117-section-head h2{font-size:34px}
  .home117-product-rail{gap:10px;padding:0 16px 10px;scroll-snap-type:x mandatory}
  .home117-product-item{flex-basis:72vw;max-width:310px}
  .home113-capsules.home117-capsules{padding:58px 0 72px}
  .home117-capsules-head{padding-bottom:24px}
  .home117-capsule-rail{gap:12px;padding:0 16px 12px}
  .home117-capsule-card{flex-basis:84vw;min-width:0;max-width:430px}
  .home117-capsule-copy{padding-top:14px}
  .home117-capsule-copy h3{font-size:29px}
}
/* END_HOME_NEW_PRODUCTS_CAPSULES_V117 */
'''

css = css.rstrip() + "\n\n" + css_block.strip() + "\n"
PAGE.write_text(page, encoding="utf-8")
CSS.write_text(css, encoding="utf-8")

print(
    "HOME_NEW_PRODUCTS_CAPSULES_V117: homepage New Products rail inserted between categories and capsules; "
    "catalog ProductCard reused; capsules converted to one horizontal five-card rail; ready solutions unchanged; "
    f"page_changed={page_changed}; css_changed=True"
)
