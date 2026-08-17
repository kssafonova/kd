from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

feature = r'''

    <section className="home-collection-duo" aria-label="Коллекции для спальни">
      <button className="home-collection-feature home-collection-feature-luna" type="button" onClick={()=>go("collections")}>
        <img src={assetUrl("/images/editorial/caps_luna_postel.png")} alt="Коллекция Лунная сказка"/>
        <span className="home-collection-feature-shade"/>
        <span className="home-collection-feature-copy">
          <small>КОЛЛЕКЦИЯ</small>
          <strong>Лунная сказка</strong>
          <em>СМОТРЕТЬ КОЛЛЕКЦИЮ →</em>
        </span>
      </button>

      <button className="home-collection-feature home-collection-feature-ice" type="button" onClick={()=>go("collections")}>
        <img src={assetUrl("/images/editorial/caps_led.png")} alt="Коллекция Ледяные узоры"/>
        <span className="home-collection-feature-shade"/>
        <span className="home-collection-feature-copy">
          <small>КОЛЛЕКЦИЯ</small>
          <strong>Ледяные узоры</strong>
          <em>СМОТРЕТЬ КОЛЛЕКЦИЮ →</em>
        </span>
      </button>
    </section>'''

# Remove previous single feature or duo when the script is re-run.
page = re.sub(r'\n\s*<section className="home-bedroom-feature">[\s\S]*?</section>', '', page, count=1)
page = re.sub(r'\n\s*<section className="home-collection-duo"[\s\S]*?</section>', '', page, count=1)
anchor = '    <section className="home-reference-products">'
if anchor not in page:
    raise SystemExit("Homepage products anchor not found")
page = page.replace(anchor, feature + "\n\n" + anchor, 1)
page_path.write_text(page, encoding="utf-8")

# Remove both historical and current styles to keep this patch idempotent.
css = re.sub(r'\n?/\* HOME_BEDROOM_FEATURE_V1 \*/[\s\S]*?/\* END_HOME_BEDROOM_FEATURE_V1 \*/', '', css)
css = re.sub(r'\n?/\* HOME_COLLECTION_DUO_V2 \*/[\s\S]*?/\* END_HOME_COLLECTION_DUO_V2 \*/', '', css)
css += r'''

/* HOME_COLLECTION_DUO_V2 */
.home-collection-duo{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:7px;
  width:100%;
  padding:0 26px 48px;
  background:#fff;
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
  background:linear-gradient(180deg,rgba(8,12,16,.03) 42%,rgba(8,12,16,.62) 100%);
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
  max-width:90%;
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
.home-collection-feature-ice>img{object-position:center}
@media(max-width:900px){
  .home-collection-duo{
    grid-template-columns:1fr;
    gap:7px;
    padding:0 16px 38px;
  }
  .home-collection-feature{
    min-height:72svh;
    max-height:760px;
  }
  .home-collection-feature-copy{
    left:22px;
    right:22px;
    bottom:28px;
  }
  .home-collection-feature-copy strong{font-size:48px}
}
@media(max-width:520px){
  .home-collection-duo{padding:0 0 32px;gap:4px}
  .home-collection-feature{min-height:620px}
  .home-collection-feature-copy{left:18px;right:18px;bottom:24px}
  .home-collection-feature-copy small{font-size:7px;margin-bottom:10px}
  .home-collection-feature-copy strong{font-size:39px}
  .home-collection-feature-copy em{font-size:7px;margin-top:20px}
}
/* END_HOME_COLLECTION_DUO_V2 */
'''
css_path.write_text(css, encoding="utf-8")
print("Added paired Luna and Ice Patterns homepage collection features")
