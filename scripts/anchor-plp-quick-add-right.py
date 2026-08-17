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
    width:min(560px,43vw)!important;
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
    top:17px!important;
    right:18px!important;
    z-index:8!important;
  }
  .plp-compact-media{
    min-height:0!important;
    height:48vh!important;
    flex:0 0 48vh!important;
  }
  .plp-compact-media img{
    min-height:0!important;
    width:100%!important;
    height:100%!important;
    object-fit:cover!important;
  }
  .plp-compact-controls{
    flex:1 0 auto!important;
    justify-content:flex-start!important;
    gap:22px!important;
    padding:30px 42px 34px!important;
  }
  .plp-compact-add{
    margin-top:auto!important;
  }
}
/* END_PLP_DESKTOP_RIGHT_DRAWER_V1 */
'''

css_path.write_text(css, encoding="utf-8")
print("Anchored desktop PLP quick-add drawer to the right edge")
