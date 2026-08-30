from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "app" / "globals.css"
PAGE = ROOT / "app" / "page.tsx"

page_text = PAGE.read_text(encoding="utf-8")
if "HOME_REDESIGN_V113" not in page_text:
    raise SystemExit("HOME_ZARAHOME_V114: homepage V113 is not applied")

css_text = CSS.read_text(encoding="utf-8")
css_original = css_text

css_block = r'''/* HOME_ZARAHOME_V114 */
.view-home .promo{background:#111!important;color:#fff!important}
.home-v113{--zara-ink:#111;--zara-paper:#fff;--zara-warm:#f4f2ed;position:relative;background:var(--zara-paper)!important;color:var(--zara-ink)!important;overflow:hidden}

/* Navigation becomes part of the hero, as on editorial home pages. */
.home113-nav{position:absolute!important;top:72px!important;left:0!important;right:0!important;z-index:12!important;height:46px!important;justify-content:center!important;gap:clamp(18px,2.6vw,42px)!important;padding:0 clamp(18px,3.5vw,56px)!important;background:linear-gradient(180deg,rgba(0,0,0,.10),transparent)!important;border:0!important;color:#fff!important}
.home113-nav button,.home113-nav a{padding:15px 0!important;color:#fff!important;font:400 9px/1 Arial,sans-serif!important;letter-spacing:.14em!important;text-transform:uppercase!important;opacity:.94!important}
.home113-nav button:hover,.home113-nav a:hover{opacity:.62!important}

/* Hero: photography first, copy second. */
.home113-hero{height:calc(100svh - 31px)!important;min-height:650px!important;max-height:none!important;background:#aaa!important}
.home113-hero-shade{background:linear-gradient(180deg,rgba(0,0,0,.18) 0%,transparent 28%,transparent 62%,rgba(0,0,0,.35) 100%)!important}
.home113-hero-copy{left:clamp(22px,4vw,64px)!important;bottom:76px!important;width:min(560px,70vw)!important}
.home113-hero-copy small{font:400 9px/1.2 Arial,sans-serif!important;letter-spacing:.16em!important}
.home113-hero-copy h1{font-family:"Tenor Sans",Georgia,serif!important;font-size:clamp(42px,5vw,76px)!important;line-height:.98!important;letter-spacing:-.018em!important;margin:10px 0 20px!important;max-width:640px!important}
.home113-hero-copy p{display:none!important}
.home113-hero-copy button{padding-bottom:5px!important;font:400 9px/1 Arial,sans-serif!important;letter-spacing:.12em!important;gap:12px!important}
.home113-hero-copy button span{font-size:13px!important}
.home113-hero-controls{left:50%!important;right:auto!important;bottom:27px!important;width:132px!important;transform:translateX(-50%)!important;display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:8px!important;border:0!important}
.home113-hero-controls button{height:2px!important;min-height:2px!important;padding:0!important;background:rgba(255,255,255,.42)!important;font-size:0!important;display:block!important}
.home113-hero-controls button::before{display:none!important}.home113-hero-controls button.is-active{background:#fff!important}.home113-hero-controls button span,.home113-hero-controls button b{display:none!important}

/* Categories: quiet horizontal image rail. */
.home113-section{padding:clamp(58px,6.5vw,92px) 0 clamp(78px,8vw,118px)!important;background:#fff!important}
.home113-section-head{display:flex!important;align-items:flex-end!important;justify-content:space-between!important;padding:0 clamp(18px,3.4vw,52px)!important;margin-bottom:26px!important;gap:28px!important}
.home113-section-head>div small{display:none!important}
.home113-section-head h2{font-family:"Tenor Sans",Georgia,serif!important;font-size:clamp(28px,3vw,44px)!important;line-height:1!important;letter-spacing:-.01em!important;margin:0!important;text-transform:none!important}
.home113-section-head p{display:none!important}
.home113-category-rail{gap:8px!important;padding:0 clamp(18px,3.4vw,52px) 8px!important;scroll-snap-type:x mandatory!important}
.home113-category-card{flex:0 0 clamp(230px,22vw,350px)!important;scroll-snap-align:start!important}
.home113-atlas-card{aspect-ratio:1/1!important;background-color:#eee!important;transition:transform .7s cubic-bezier(.2,.6,.2,1)!important}
.home113-category-card:hover .home113-atlas-card{transform:scale(1.012)!important}
.home113-category-card strong{font-family:"Tenor Sans",Georgia,serif!important;font-size:clamp(15px,1.2vw,19px)!important;line-height:1.1!important;margin-top:11px!important}
.home113-category-card small{display:none!important}

/* Editorial sections: large asymmetric image layouts, minimal copy. */
.home113-capsules{padding:clamp(72px,8vw,118px) 0 clamp(100px,10vw,150px)!important;background:#fff!important;color:#111!important}
.home113-solutions{padding:clamp(88px,9vw,132px) 0 clamp(100px,10vw,150px)!important;background:var(--zara-warm)!important;color:#111!important}
.home113-editorial-head{display:flex!important;align-items:flex-end!important;justify-content:space-between!important;padding:0 clamp(18px,3.4vw,52px)!important;margin-bottom:clamp(46px,6vw,86px)!important;gap:30px!important}
.home113-editorial-head>small{display:none!important}
.home113-editorial-head h2{font-family:"Tenor Sans",Georgia,serif!important;font-size:clamp(30px,3.4vw,50px)!important;line-height:1!important;letter-spacing:-.012em!important;margin:0!important}
.home113-editorial-head p{display:none!important}
.home113-editorial-head>button,.home113-editorial-head>a{grid-column:auto!important;justify-self:auto!important;margin:0!important;color:#111!important;padding-bottom:4px!important;font:400 9px/1 Arial,sans-serif!important;letter-spacing:.11em!important}
.home113-editorial-head-light p,.home113-solutions .home113-solution-copy p{color:#777!important}
.home113-story-list,.home113-solution-list{gap:clamp(82px,10vw,148px)!important}
.home113-story,.home113-solution{display:block!important;max-width:1600px!important;margin:0 auto!important;padding:0 clamp(18px,3.4vw,52px)!important}
.home113-story-copy,.home113-solution-copy{position:static!important;padding:0 0 15px!important;display:flex!important;align-items:flex-end!important;justify-content:space-between!important;gap:24px!important}
.home113-story-copy small,.home113-solution-copy small,.home113-story-copy p,.home113-solution-copy p{display:none!important}
.home113-story-copy h3,.home113-solution-copy h3{font-family:"Tenor Sans",Georgia,serif!important;font-size:clamp(23px,2.35vw,36px)!important;line-height:1!important;letter-spacing:-.01em!important;margin:0!important;font-weight:400!important}
.home113-story-copy button,.home113-solution-copy a{flex:0 0 auto!important;color:#111!important;padding-bottom:4px!important;font:400 9px/1 Arial,sans-serif!important;letter-spacing:.11em!important;gap:10px!important}
.home113-story-copy button span,.home113-solution-copy a span{font-size:12px!important}
.home113-photo-rail{display:grid!important;grid-template-columns:repeat(12,minmax(0,1fr))!important;gap:8px!important;overflow:visible!important;padding:0!important;scroll-snap-type:none!important}
.home113-photo-card{position:relative!important;display:block!important;grid-column:span 6!important;flex:none!important;width:auto!important;aspect-ratio:4/5!important;background:#eee!important;overflow:hidden!important;scroll-snap-align:none!important}
.home113-photo-card:first-child{grid-column:span 7!important}
.home113-photo-card:nth-child(2){grid-column:span 5!important;margin-top:clamp(28px,6vw,92px)!important}
.home113-photo-card:nth-child(n+3){margin-top:0!important}
.home113-photo-card>span{transition:transform .7s cubic-bezier(.2,.6,.2,1)!important}
.home113-photo-card:hover>span{transform:scale(1.012)!important}
.home113-solutions .home113-photo-card{background:#e7e4dd!important}
.home113-solution:nth-child(even) .home113-photo-card:first-child,.home113-story:nth-child(even) .home113-photo-card:first-child{grid-column:span 6!important}
.home113-solution:nth-child(even) .home113-photo-card:nth-child(2),.home113-story:nth-child(even) .home113-photo-card:nth-child(2){grid-column:span 6!important;margin-top:clamp(22px,4vw,64px)!important}

/* Keep the store finder understated. */
.home-v113 .home-boutiques-map{margin:0!important;background:#fff!important;border-top:1px solid #e6e4df!important}
.home-v113 .home-boutiques-copy>small{font-size:8px!important;letter-spacing:.14em!important}
.home-v113 .home-boutiques-copy h2{font-family:"Tenor Sans",Georgia,serif!important;font-weight:400!important;letter-spacing:-.01em!important}

@media(max-width:760px){
  .home113-nav{top:62px!important;height:42px!important;justify-content:flex-start!important;gap:22px!important;padding:0 16px!important;background:linear-gradient(180deg,rgba(0,0,0,.12),transparent)!important}
  .home113-nav button,.home113-nav a{font-size:8px!important;padding:14px 0!important}
  .home113-hero{height:calc(100svh - 31px)!important;min-height:590px!important;max-height:none!important}
  .home113-hero-copy{left:18px!important;right:18px!important;bottom:66px!important;width:auto!important}
  .home113-hero-copy small{font-size:8px!important}.home113-hero-copy h1{font-size:clamp(37px,11.5vw,52px)!important;max-width:92%!important;margin:8px 0 16px!important}
  .home113-hero-copy button{font-size:8px!important}
  .home113-hero-controls{bottom:21px!important;width:112px!important;gap:6px!important}

  .home113-section{padding:46px 0 66px!important}.home113-section-head{padding:0 16px!important;margin-bottom:18px!important}.home113-section-head h2{font-size:25px!important}
  .home113-category-rail{padding:0 16px 7px!important;gap:7px!important}.home113-category-card{flex-basis:68vw!important}.home113-category-card strong{font-size:15px!important;margin-top:10px!important}

  .home113-capsules,.home113-solutions{padding:58px 0 78px!important}.home113-editorial-head{padding:0 16px!important;margin-bottom:36px!important;align-items:center!important}.home113-editorial-head h2{font-size:27px!important}.home113-editorial-head>button,.home113-editorial-head>a{font-size:8px!important;white-space:nowrap!important}
  .home113-story-list,.home113-solution-list{gap:62px!important}.home113-story,.home113-solution{padding:0!important}
  .home113-story-copy,.home113-solution-copy{padding:0 16px 13px!important;align-items:center!important}.home113-story-copy h3,.home113-solution-copy h3{font-size:25px!important}.home113-story-copy button,.home113-solution-copy a{font-size:8px!important}
  .home113-photo-rail{display:flex!important;gap:7px!important;overflow-x:auto!important;padding:0 16px 7px!important;scroll-snap-type:x mandatory!important;scrollbar-width:none!important}
  .home113-photo-rail::-webkit-scrollbar{display:none!important}.home113-photo-card,.home113-photo-card:first-child,.home113-photo-card:nth-child(2),.home113-photo-card:nth-child(n+3){flex:0 0 82vw!important;width:82vw!important;grid-column:auto!important;margin-top:0!important;scroll-snap-align:start!important;aspect-ratio:4/5!important}
  .home-v113 .home-boutiques-map{border-top:0!important}
}
/* END_HOME_ZARAHOME_V114 */'''

pattern = re.compile(r"/\* HOME_ZARAHOME_V114 \*/.*?/\* END_HOME_ZARAHOME_V114 \*/", re.S)
if pattern.search(css_text):
    css_text = pattern.sub(css_block, css_text, count=1)
else:
    css_text = css_text.rstrip() + "\n\n" + css_block + "\n"

CSS.write_text(css_text, encoding="utf-8")

checks = [
    "HOME_ZARAHOME_V114",
    ".home113-hero{height:calc(100svh - 31px)!important",
    ".home113-photo-rail{display:grid!important",
    ".home113-solutions{padding:clamp(88px,9vw,132px)",
    ".home113-category-card{flex:0 0 clamp(230px,22vw,350px)!important",
]
for marker in checks:
    if marker not in css_text:
        raise SystemExit(f"HOME_ZARAHOME_V114: missing marker {marker}")

print(
    "// HOME_ZARAHOME_V114: Zara Home-style homepage refinement applied; "
    "hero-first composition, overlay navigation, quiet category rail, asymmetric editorial galleries, light ready-solutions section; "
    f"css_changed={css_text != css_original}"
)
