from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
CSS=ROOT/"app"/"home-standalone.css"
css=CSS.read_text(encoding="utf-8")

block=r'''/* KULTURA_HOME_PLP_CARD_V148 — exact final PLP card system on home New Products. */
.home-fast-new .home-fast-product-rail{align-items:stretch}
.home-fast-new .home-fast-product{flex:0 0 clamp(220px,23vw,330px);color:inherit;scroll-snap-align:start}
.home-fast-new .product-card{
  display:grid;
  grid-template-columns:minmax(0,1fr) 40px;
  grid-template-areas:"media media" "copy action";
  column-gap:8px;
  row-gap:0;
  min-width:0;
}
.home-fast-new .product-image{grid-area:media;width:100%;padding:0;display:block;position:relative;overflow:hidden;background:#f3f1ed}
.home-fast-new .product-image img{width:100%;aspect-ratio:1/1.08;object-fit:cover}
.home-fast-new .product-copy{grid-area:copy;width:auto;padding:13px 0 0;display:flex;flex-direction:column;text-align:left;min-width:0}
.home-fast-new .product-link{display:flex;flex-direction:column;align-items:flex-start;text-align:left;width:100%;padding:0}
.home-fast-new .product-copy strong{font:400 18px/1.25 var(--serif)}
.home-fast-new .product-copy small{color:#999;font-size:11px;line-height:1.45;margin-top:4px}
.home-fast-new .price{font-size:17px;line-height:1.2;margin-top:8px}
.home-fast-new .price del{font-size:12px;color:#999;margin-left:7px}
.home-fast-new .price mark{margin-left:6px;background:transparent;color:#9b523c;font-size:10px}
.home-fast-new .quick{grid-area:action;position:static;align-self:start;justify-self:end;margin:10px 0 0;width:40px;height:40px;padding:0;display:grid;place-items:center}
.home-fast-new .quick>svg{width:31px;height:31px}
.home-fast-new .heart{position:absolute;right:10px;top:10px;z-index:2;color:#fff;filter:drop-shadow(0 1px 2px #0008);padding:0}
.home-fast-new .heart svg{width:31px;height:31px;stroke-width:1.2}
.home-fast-new .heart.liked{color:#9d654b}
.home-fast-new .plp-swatches{display:flex;gap:7px;flex-wrap:wrap;margin-top:9px;min-height:20px}
.home-fast-new .plp-swatches button{width:17px;height:17px;padding:0;border:1px solid #d7d7d3;border-radius:50%;box-shadow:inset 0 0 0 2px #fff}
.home-fast-new .plp-swatches button.active{outline:1px solid #222;outline-offset:1px}
.home-fast-new .plp-aroma-options{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.home-fast-new .plp-aroma-options button{padding:5px 7px;border:1px solid #ddd;background:#fff;font-size:9px;line-height:1}
.home-fast-new .plp-aroma-options button.active{border-color:#1d1d1d}

@media(max-width:760px){
  .home-fast-new .home-fast-product{flex-basis:64vw;max-width:280px}
  .home-fast-new .product-card{grid-template-columns:minmax(0,1fr) 42px;column-gap:6px}
  .home-fast-new .product-copy{padding-top:10px}
  .home-fast-new .product-copy strong{font-size:14px;line-height:1.28}
  .home-fast-new .product-copy small{font-size:10px;line-height:1.35}
  .home-fast-new .price{font-size:14px;margin-top:6px}
  .home-fast-new .quick{width:42px;height:42px;margin-top:5px}
  .home-fast-new .quick>svg{width:29px;height:29px}
  .home-fast-new .heart{right:7px;top:7px}
  .home-fast-new .heart svg{width:29px;height:29px}
}

@media(max-width:520px){
  .home-fast-new .product-card{grid-template-columns:minmax(0,1fr) 34px;column-gap:5px}
  .home-fast-new .product-copy{padding-top:8px}
  .home-fast-new .product-copy strong{font-size:13px}
  .home-fast-new .product-copy small{font-size:9px}
  .home-fast-new .price{font-size:13px}
  .home-fast-new .quick{width:34px;height:36px;margin-top:5px}
  .home-fast-new .quick>svg{width:26px;height:26px}
}
'''

# Replace either the previous v147 compatibility block or an earlier v148
# block. Keep all homepage styles above it untouched.
match=re.search(r'/\* KULTURA_HOME_PLP_CARD_V14[78].*\Z',css,flags=re.S)
if match:
    css=css[:match.start()].rstrip()+"\n\n"+block
else:
    css=css.rstrip()+"\n\n"+block

CSS.write_text(css,encoding="utf-8")
print("KULTURA_HOME_PLP_V148: homepage New Products now uses the final catalog PLP layout, typography, heart, swatches and cart-add sizing")
