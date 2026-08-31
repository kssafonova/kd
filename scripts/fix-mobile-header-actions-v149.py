from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSS=ROOT/"app"/"globals.css"
css=CSS.read_text(encoding="utf-8")
marker="/* KULTURA_MOBILE_HEADER_ACTIONS_V149 */"
block=r'''

/* KULTURA_MOBILE_HEADER_ACTIONS_V149
   Search, profile, favourites and bag remain equally available on mobile.
   Compact spacing keeps the existing Kultura header balanced at 390px. */
@media(max-width:900px){
  .header-actions{gap:5px;min-width:0}
  .header-actions button{display:grid!important;place-items:center;width:27px;height:38px;padding:2px;line-height:1}
  .header-actions button:nth-child(3){display:grid!important}
  .header-actions svg{width:23px;height:23px}
  .header-actions .bag svg{width:24px;height:24px}
  .header-actions .bag b,.header-actions .favorite-header b{right:-2px;top:0}
}
@media(max-width:520px){
  .header{padding-left:10px;padding-right:10px}
  .header-actions{gap:3px}
  .header-actions button{width:26px;height:38px}
  .header-actions svg{width:22px;height:22px}
  .header-actions .bag svg{width:23px;height:23px}
  .logo{font-size:16px}
}
'''
if marker not in css:
    css=css.rstrip()+block+"\n"
CSS.write_text(css,encoding="utf-8")
print("KULTURA_HEADER_V149: all four mobile header actions visible with compact non-overlapping sizing")
