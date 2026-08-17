from pathlib import Path
import re

css_path = Path("app/globals.css")
css = css_path.read_text(encoding="utf-8")

css = re.sub(
    r'\n?/\* PLP_DESKTOP_RIGHT_DRAWER_V1 \*/[\s\S]*?/\* END_PLP_DESKTOP_RIGHT_DRAWER_V1 \*/',
    '',
    css,
)

css += r'''

/* PLP_DESKTOP_RIGHT_DRAWER_V1 */
@media(min-width:901px){
  .plp-flow.plp-compact-flow{
    align-items:stretch!important;
    justify-content:flex-end!important;
    padding:0!important;
  }
  .plp-flow .plp-compact-modal{
    margin:0 0 0 auto!important;
    width:min(646px,46vw)!important;
    height:100%!important;
    max-height:100vh!important;
    display:flex!important;
    flex-direction:column!important;
    overflow-y:auto!important;
    border-top:0!important;
    border-right:0!important;
    border-bottom:0!important;
    border-left:1px solid #e6e0d8!important;
    box-shadow:-12px 0 45px rgba(0,0,0,.12)!important;
    animation:slideLeft .25s ease!important;
  }
  .plp-flow .plp-compact-modal>.close{
    position:fixed!important;
    top:18px!important;
    right:20px!important;
    z-index:10!important;
  }
  .plp-reference-gallery{
    flex:0 0 auto!important;
    width:100%!important;
  }
  .plp-reference-media>img{
    aspect-ratio:1.68/1!important;
  }
  .plp-reference-body{
    flex:1 0 auto!important;
    padding:38px 46px 38px!important;
  }
}
/* END_PLP_DESKTOP_RIGHT_DRAWER_V1 */
'''

css_path.write_text(css, encoding="utf-8")
print("Kept reference PLP quick-add layout inside a right-edge desktop drawer")
