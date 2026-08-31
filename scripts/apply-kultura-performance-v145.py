from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
GLOBALS=ROOT/"app"/"globals.css"
ROOT_LAYOUT=ROOT/"app"/"layout.tsx"
HOME=ROOT/"app"/"home-standalone.tsx"
STORE=ROOT/"app"/"storefront-app.tsx"

# Keep Tenor Sans and the exact Kultura doma UI, but avoid render-blocking CSS @import.
globals_css=GLOBALS.read_text(encoding="utf-8")
globals_css=globals_css.replace("@import url('https://fonts.googleapis.com/css2?family=Tenor+Sans&display=swap');\n","")
perf_css='''\n/* KULTURA_PERFORMANCE_V145 — paint/layout optimization only; no visual changes. */
@supports (content-visibility:auto){
  .view-catalog .product-card{content-visibility:auto;contain-intrinsic-size:auto 520px}
  .view-home .home-fast-section{content-visibility:auto;contain-intrinsic-size:auto 720px}
  .view-product .rich-content>*,.pdp-rich-content>*{content-visibility:auto;contain-intrinsic-size:auto 720px}
}
'''
if "KULTURA_PERFORMANCE_V145" not in globals_css:
    globals_css+=perf_css
GLOBALS.write_text(globals_css,encoding="utf-8")

layout=ROOT_LAYOUT.read_text(encoding="utf-8")
if "fonts.googleapis.com/css2?family=Tenor+Sans" not in layout:
    layout=layout.replace(
        '<html lang="ru"><body>{children}</body></html>',
        '<html lang="ru"><head><link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tenor+Sans&display=swap"/></head><body>{children}</body></html>',
        1,
    )
ROOT_LAYOUT.write_text(layout,encoding="utf-8")

# Homepage: do not download the whole catalog/secondary routes on mount.
# Prefetch only after real user intent, while preserving the same links and design.
home=HOME.read_text(encoding="utf-8")
eager='''    router.prefetch("/catalog/");
    router.prefetch("/capsules/");
    router.prefetch("/collections/");
    router.prefetch("/ready-solutions/");
'''
home=home.replace(eager,'''    const prefetched=new Set<string>();
    const prefetchIntent=(event:Event)=>{
      const anchor=(event.target as Element|null)?.closest<HTMLAnchorElement>("a[href]");
      if(!anchor)return;
      const raw=anchor.getAttribute("href")||"";
      const relative=BASE&&raw.startsWith(BASE)?(raw.slice(BASE.length)||"/"):raw;
      if(!relative.startsWith("/")||prefetched.has(relative))return;
      prefetched.add(relative);
      router.prefetch(relative);
    };
''',1)
if 'root?.addEventListener("pointerover",prefetchIntent' not in home:
    home=home.replace(
        '    root?.addEventListener("click",route);\n    return()=>root?.removeEventListener("click",route);',
        '    root?.addEventListener("click",route);\n    root?.addEventListener("pointerover",prefetchIntent,{passive:true});\n    root?.addEventListener("touchstart",prefetchIntent,{passive:true});\n    return()=>{root?.removeEventListener("click",route);root?.removeEventListener("pointerover",prefetchIntent);root?.removeEventListener("touchstart",prefetchIntent)};',
        1,
    )

# If the brand MP4 files are not in assets, keep the same poster/ratio but make no failed network requests.
video_desktop=ROOT/"assets"/"video"/"kultura-brand-desktop.mp4"
video_mobile=ROOT/"assets"/"video"/"kultura-brand-mobile.mp4"
if not video_desktop.exists() and not video_mobile.exists():
    home=re.sub(r'\n\s*useEffect\(\(\)=>\{\n\s*const video=brandVideoRef\.current;.*?\n\s*\},\[\]\);',"",home,count=1,flags=re.S)
    home=home.replace('<source media="(max-width:700px)" src={url("/assets/video/kultura-brand-mobile.mp4")} type="video/mp4"/>','',1)
    home=home.replace('<source src={url("/assets/video/kultura-brand-desktop.mp4")} type="video/mp4"/>','',1)
HOME.write_text(home,encoding="utf-8")

# Catalog/PDP: all Foto 1–3 remain available. Give secondary gallery images low network priority;
# local /assets images themselves no longer create React state/effects (handled in remote-image.tsx).
store=STORE.read_text(encoding="utf-8")
store=store.replace(
    'loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>)',
    'loading="lazy" decoding="async" fetchPriority={index===0?"auto":"low"} draggable={false} style={{objectPosition:position||product.position||"center"}}/>)',
    1,
)
STORE.write_text(store,encoding="utf-8")

print("KULTURA_PERFORMANCE_V145: Tenor Sans preserved, blocking font import removed, intent-prefetch enabled, failed video requests suppressed, local image hydration reduced, offscreen paint deferred")
