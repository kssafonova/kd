from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
CSS = ROOT / "app" / "globals.css"
ASSETS = ROOT / "assets" / "images"

hero_assets = [
    "1_new_desktop.png",
    "1_new_mobile.png",
    "2_sleep_desktop.png",
    "2_sleep_mobile.png",
    "3_stol_desktop.png",
    "3_stol_mobile.png",
]
for filename in hero_assets:
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"HOME_HERO_DIRECT_IMAGES_V115: missing asset {filename}")

page_text = PAGE.read_text(encoding="utf-8")
page_original = page_text

hero_block = '''  const heroSlides=[
    {eyebrow:"НОВИНКИ",title:"Новые истории дома",text:"Предметы, которые собирают пространство в цельный образ — от спальни до сервировки.",cta:"Смотреть новинки",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png",action:()=>openCatalog()},
    {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой",text:"Сатин, мягкий свет и спокойные оттенки для пространства, в котором хочется остаться.",cta:"Перейти в спальню",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png",action:()=>openCatalog("Постельное белье")},
    {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал",text:"Фарфор, текстиль и детали стола в современной культуре русского дома.",cta:"Смотреть сервировку",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png",action:()=>openCatalog("Посуда и сервировка")},
  ];
'''

pattern = re.compile(r'  const heroSlides=\[.*?\n  \];\n', re.S)
if not pattern.search(page_text):
    raise SystemExit("HOME_HERO_DIRECT_IMAGES_V115: heroSlides block not found")
page_text = pattern.sub(hero_block, page_text, count=1)
page_text = re.sub(r'  const heroPosition=`\$\{active\*50\}% 50%`;\n', '', page_text, count=1)

old_desktop = '<div className="home113-hero-art home113-hero-art-desktop" aria-hidden="true" style={{backgroundImage:`url("${assetUrl("/assets/images/home113-hero-desktop.svg")}")`,backgroundPosition:heroPosition}}/>'
new_desktop = '<div className="home113-hero-art home113-hero-art-desktop" aria-hidden="true" style={{backgroundImage:`url("${assetUrl(hero.desktop)}")`}}/>'
old_mobile = '<div className="home113-hero-art home113-hero-art-mobile" aria-hidden="true" style={{backgroundImage:`url("${assetUrl("/assets/images/home113-hero-mobile.svg")}")`,backgroundPosition:heroPosition}}/>'
new_mobile = '<div className="home113-hero-art home113-hero-art-mobile" aria-hidden="true" style={{backgroundImage:`url("${assetUrl(hero.mobile)}")`}}/>'

if old_desktop not in page_text or old_mobile not in page_text:
    raise SystemExit("HOME_HERO_DIRECT_IMAGES_V115: atlas hero markup not found")
page_text = page_text.replace(old_desktop, new_desktop, 1).replace(old_mobile, new_mobile, 1)

for marker in hero_assets:
    if marker not in page_text:
        raise SystemExit(f"HOME_HERO_DIRECT_IMAGES_V115: page missing {marker}")
if "heroPosition" in page_text:
    raise SystemExit("HOME_HERO_DIRECT_IMAGES_V115: stale heroPosition remains")
PAGE.write_text(page_text, encoding="utf-8")

css_text = CSS.read_text(encoding="utf-8")
css_original = css_text
css_block = '''/* HOME_HERO_DIRECT_IMAGES_V115 */
.home113-hero-art{background-size:cover!important;background-position:center center!important;background-repeat:no-repeat!important}
.home113-hero-art-desktop{display:block!important}
.home113-hero-art-mobile{display:none!important}
@media(max-width:760px){
  .home113-hero-art-desktop{display:none!important}
  .home113-hero-art-mobile{display:block!important;background-size:cover!important;background-position:center center!important}
}
/* END_HOME_HERO_DIRECT_IMAGES_V115 */'''
css_pattern = re.compile(r'/\* HOME_HERO_DIRECT_IMAGES_V115 \*/.*?/\* END_HOME_HERO_DIRECT_IMAGES_V115 \*/', re.S)
if css_pattern.search(css_text):
    css_text = css_pattern.sub(css_block, css_text, count=1)
else:
    css_text = css_text.rstrip() + "\n\n" + css_block + "\n"
CSS.write_text(css_text, encoding="utf-8")

print(
    "// HOME_HERO_DIRECT_IMAGES_V115: direct PNG hero pairs enabled; "
    "1_new desktop/mobile + 2_sleep desktop/mobile + 3_stol desktop/mobile; "
    f"page_changed={page_text != page_original}; css_changed={css_text != css_original}"
)
