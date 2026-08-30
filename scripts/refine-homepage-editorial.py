from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# Match the supplied homepage reference more closely: quieter headings, no descriptive
# copy in section headers, and a strict editorial rhythm.
page = page.replace('["Спальня","/assets/images/classic-bedroom.png"]', '["Ванная","/assets/images/classic-bedroom.png"]', 1)

page = re.sub(
    r'<header className="home-bedroom-collections-head">[\s\S]*?</header>',
    '''<header className="home-bedroom-collections-head">
        <div>
          <p>СПАЛЬНЯ</p>
          <h2 id="home-bedroom-collections-title">КОЛЛЕКЦИИ И КАПСУЛЫ</h2>
        </div>
        <button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ →</button>
      </header>''',
    page,
    count=1,
)

page = page.replace(
    '<div className="home-reference-products-head"><div><p>ВЫБОР РЕДАКЦИИ · СПАЛЬНЯ</p><h2>ХИТЫ ПРОДАЖ</h2></div><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>',
    '<div className="home-reference-products-head"><div><p>СПАЛЬНЯ</p><h2>ВЫБОР РЕДАКЦИИ</h2></div><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>',
    1,
)

# Keep collection card labels minimal like the reference.
page = page.replace('<small>КОЛЛЕКЦИЯ · СПАЛЬНЯ</small>', '<small>КОЛЛЕКЦИЯ</small>')
page = page.replace('<em>СМОТРЕТЬ ИСТОРИИ →</em>', '<em>СМОТРЕТЬ КОЛЛЕКЦИЮ →</em>')

page_path.write_text(page, encoding="utf-8")

css = re.sub(r'\n?/\* HOME_EDITORIAL_REFERENCE_V4 \*/[\s\S]*?/\* END_HOME_EDITORIAL_REFERENCE_V4 \*/', '', css)
css += r'''

/* HOME_EDITORIAL_REFERENCE_V4 */
.view-home{background:#fff}
.home-reference-hero{
  height:clamp(600px,47vw,760px)!important;
  min-height:600px!important;
}
.home-reference-hero .hero-media img{object-position:center 48%!important}
.home-reference-hero .hero-nav{height:42px!important;gap:46px!important}
.home-reference-hero .hero-nav button{height:42px!important;padding:14px 0 10px!important;font-size:8px!important;letter-spacing:.12em!important}
.home-reference-hero .hero-dots{bottom:48px!important}

.home-reference-shelf{
  padding:30px 26px 58px!important;
}
.home-reference-heading{
  margin-bottom:17px!important;
  align-items:center!important;
}
.home-reference-heading p{
  font-size:8px!important;
  letter-spacing:.19em!important;
}
.home-reference-heading button,
.home-bedroom-collections-head>button,
.home-reference-products-head>button{
  font-size:7px!important;
  letter-spacing:.11em!important;
  border-bottom:1px solid #777!important;
  padding-bottom:4px!important;
}
.home-reference-shelf .category-grid{gap:6px!important}
.home-reference-shelf .category-card{
  aspect-ratio:.9/1!important;
  padding:17px 14px!important;
}
.home-reference-shelf .category-card span{
  font-size:17px!important;
  line-height:1.05!important;
  font-weight:400!important;
}
.home-reference-shelf .category-card b{
  margin-top:7px!important;
  font-size:6.5px!important;
  letter-spacing:.08em!important;
}

.home-bedroom-collections{
  padding:12px 26px 64px!important;
}
.home-bedroom-collections-head{
  display:flex!important;
  align-items:flex-end!important;
  justify-content:space-between!important;
  gap:20px!important;
  padding:0 0 20px!important;
}
.home-bedroom-collections-head>div{
  display:grid!important;
  gap:8px!important;
}
.home-bedroom-collections-head p{
  margin:0!important;
  font-size:7px!important;
  line-height:1!important;
  letter-spacing:.19em!important;
  color:#5b5e5b!important;
}
.home-bedroom-collections-head h2{
  margin:0!important;
  font-size:17px!important;
  line-height:1!important;
  font-weight:400!important;
  letter-spacing:.035em!important;
}
.home-bedroom-collections-head>span{display:none!important}
.home-collection-duo{
  gap:7px!important;
}
.home-collection-feature{
  min-height:660px!important;
  aspect-ratio:1.03/1!important;
}
.home-collection-feature-copy{
  left:30px!important;
  right:30px!important;
  bottom:30px!important;
}
.home-collection-feature-copy small{
  margin-bottom:11px!important;
  font-size:7px!important;
  letter-spacing:.18em!important;
}
.home-collection-feature-copy strong{
  font-size:clamp(42px,4.25vw,68px)!important;
  line-height:.94!important;
}
.home-collection-feature-copy em{
  margin-top:22px!important;
  font-size:6.5px!important;
  letter-spacing:.11em!important;
}
.home-collection-feature-shade{
  background:linear-gradient(180deg,rgba(8,12,16,0) 45%,rgba(8,12,16,.58) 100%)!important;
}

.home-reference-products{
  padding:12px 26px 58px!important;
}
.home-reference-products-head{
  margin-bottom:20px!important;
  align-items:flex-end!important;
}
.home-reference-products-head>div{
  display:grid!important;
  gap:8px!important;
}
.home-reference-products-head p{
  font-size:7px!important;
  letter-spacing:.19em!important;
}
.home-reference-products-head h2{
  margin:0!important;
  font-size:17px!important;
  line-height:1!important;
  font-weight:400!important;
  letter-spacing:.035em!important;
}
.home-reference-products .product-rail{
  gap:12px!important;
}
.home-reference-products .product-image,
.home-reference-products .product-image .product-media-scroll,
.home-reference-products .product-image img{
  aspect-ratio:1/1.06!important;
}
.home-reference-products .product-copy{padding-top:9px!important}
.home-reference-products .product-copy strong{font-size:14px!important;line-height:1.1!important}
.home-reference-products .product-copy small{font-size:7px!important;line-height:1.35!important;color:#898989!important}
.home-reference-products .price{font-size:12px!important;margin-top:8px!important}
.home-reference-products .price del{font-size:8px!important}

.home-reference-manifest{
  padding:92px 20px 88px!important;
  background:#f3f0ea!important;
}
.home-reference-manifest p{font-size:7px!important;letter-spacing:.21em!important;margin-bottom:22px!important}
.home-reference-manifest h2{font-size:38px!important;line-height:1.06!important;margin-bottom:24px!important;font-weight:400!important}
.home-reference-manifest span{font-size:9px!important;line-height:1.75!important;color:#777!important}
.home-reference-manifest button{font-size:7px!important;margin-top:28px!important}

@media(max-width:900px){
  .home-reference-hero{height:72svh!important;min-height:520px!important}
  .home-reference-shelf{padding:24px 16px 42px!important}
  .home-reference-shelf .category-card{aspect-ratio:.9/1!important}
  .home-bedroom-collections{padding:8px 16px 46px!important}
  .home-bedroom-collections-head{padding-bottom:16px!important}
  .home-bedroom-collections-head h2{font-size:16px!important}
  .home-collection-duo{
    display:flex!important;
    overflow-x:auto!important;
    scroll-snap-type:x mandatory!important;
    scrollbar-width:none!important;
    margin-right:-16px!important;
    padding-right:16px!important;
  }
  .home-collection-duo::-webkit-scrollbar{display:none!important}
  .home-collection-feature{
    flex:0 0 82vw!important;
    min-height:66svh!important;
    max-height:700px!important;
    scroll-snap-align:start!important;
  }
  .home-collection-feature-copy strong{font-size:43px!important}
  .home-reference-products{padding:8px 16px 46px!important}
  .home-reference-products-head h2{font-size:16px!important}
  .home-reference-products .product-card{flex-basis:70vw!important}
  .home-reference-manifest{padding:72px 20px 68px!important}
  .home-reference-manifest h2{font-size:30px!important}
}
@media(max-width:520px){
  .home-reference-hero{height:68svh!important;min-height:480px!important}
  .home-bedroom-collections{padding-left:16px!important;padding-right:16px!important}
  .home-bedroom-collections-head p,.home-reference-products-head p{font-size:6.5px!important}
  .home-bedroom-collections-head h2,.home-reference-products-head h2{font-size:15px!important}
  .home-collection-feature{flex-basis:86vw!important;min-height:570px!important}
  .home-collection-feature-copy{left:18px!important;right:18px!important;bottom:22px!important}
  .home-collection-feature-copy strong{font-size:37px!important}
  .home-reference-products .product-card{flex-basis:76vw!important}
}
/* END_HOME_EDITORIAL_REFERENCE_V4 */
'''
css_path.write_text(css, encoding="utf-8")
print("Refined homepage to the supplied editorial reference")
