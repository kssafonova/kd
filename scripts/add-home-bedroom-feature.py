from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# Insert the bedroom editorial feature between the category shelf and bestsellers.
feature = r'''

    <section className="home-bedroom-feature">
      <img src={assetUrl("/images/blue-bedroom.png")} alt="Коллекции для спальни"/>
      <div className="home-bedroom-feature-shade"/>
      <div className="home-bedroom-feature-copy">
        <p>КОЛЛЕКЦИИ ДЛЯ СПАЛЬНИ</p>
        <h2>Пространство для тишины</h2>
        <span>Постельное бельё и текстиль, созданные для спокойных личных ритуалов.</span>
        <button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ КОЛЛЕКЦИИ →</button>
      </div>
    </section>'''

# Remove a previous copy if the script is re-run.
page = re.sub(r'\n\s*<section className="home-bedroom-feature">[\s\S]*?</section>', '', page, count=1)
anchor = '    <section className="home-reference-products">'
if anchor not in page:
    raise SystemExit("Homepage products anchor not found")
page = page.replace(anchor, feature + "\n\n" + anchor, 1)
page_path.write_text(page, encoding="utf-8")

css = re.sub(r'\n?/\* HOME_BEDROOM_FEATURE_V1 \*/[\s\S]*?/\* END_HOME_BEDROOM_FEATURE_V1 \*/', '', css)
css += r'''

/* HOME_BEDROOM_FEATURE_V1 */
.home-bedroom-feature{
  position:relative;
  width:100%;
  min-height:620px;
  overflow:hidden;
  background:#d9dde0;
}
.home-bedroom-feature>img{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center;
}
.home-bedroom-feature-shade{
  position:absolute;
  inset:0;
  background:linear-gradient(90deg,rgba(15,24,30,.55) 0%,rgba(15,24,30,.22) 42%,rgba(15,24,30,.04) 72%);
}
.home-bedroom-feature-copy{
  position:absolute;
  left:7.5%;
  top:50%;
  transform:translateY(-50%);
  z-index:2;
  max-width:610px;
  color:#fff;
}
.home-bedroom-feature-copy p{
  margin:0 0 20px;
  font-size:9px;
  letter-spacing:.19em;
}
.home-bedroom-feature-copy h2{
  margin:0;
  max-width:580px;
  font-size:clamp(48px,5vw,78px);
  line-height:.98;
  font-weight:400;
  letter-spacing:-.02em;
}
.home-bedroom-feature-copy span{
  display:block;
  max-width:430px;
  margin-top:22px;
  font-size:13px;
  line-height:1.6;
}
.home-bedroom-feature-copy button{
  margin-top:30px;
  padding:0 0 6px;
  border-bottom:1px solid rgba(255,255,255,.9);
  color:#fff;
  font-size:9px;
  letter-spacing:.11em;
}
@media(max-width:900px){
  .home-bedroom-feature{min-height:68svh;max-height:720px}
  .home-bedroom-feature>img{object-position:58% center}
  .home-bedroom-feature-shade{background:linear-gradient(180deg,rgba(12,20,26,.12),rgba(12,20,26,.48))}
  .home-bedroom-feature-copy{
    left:20px;
    right:20px;
    top:auto;
    bottom:40px;
    transform:none;
    max-width:none;
  }
  .home-bedroom-feature-copy h2{font-size:44px;max-width:520px}
  .home-bedroom-feature-copy span{font-size:11px;max-width:360px;margin-top:16px}
  .home-bedroom-feature-copy button{margin-top:22px}
}
@media(max-width:520px){
  .home-bedroom-feature{min-height:590px}
  .home-bedroom-feature-copy{left:16px;right:16px;bottom:30px}
  .home-bedroom-feature-copy p{font-size:8px;margin-bottom:14px}
  .home-bedroom-feature-copy h2{font-size:38px;line-height:1}
  .home-bedroom-feature-copy span{font-size:10px;line-height:1.55}
}
/* END_HOME_BEDROOM_FEATURE_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Added homepage bedroom editorial feature")
