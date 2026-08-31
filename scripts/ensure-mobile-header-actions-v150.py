from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSS=ROOT/"app"/"globals.css"
css=CSS.read_text(encoding="utf-8")
marker="/* KULTURA_MOBILE_HEADER_ACTIONS_V150 */"
block=r'''

/* KULTURA_MOBILE_HEADER_ACTIONS_V150
   Final, high-specificity mobile header contract. All four commerce actions
   remain visible on home/catalog while preserving the compact Kultura layout. */
@media(max-width:900px){
  .view-home .header .header-actions .favorite-header,
  .view-catalog .header .header-actions .favorite-header{
    display:grid!important;
    visibility:visible!important;
    opacity:1!important;
    pointer-events:auto!important;
  }
}
@media(max-width:520px){
  .view-home .header .header-actions,
  .view-catalog .header .header-actions{
    gap:3px!important;
    min-width:0!important;
  }
  .view-home .header .header-actions button,
  .view-catalog .header .header-actions button{
    display:grid!important;
    place-items:center!important;
    width:25px!important;
    height:36px!important;
    padding:1px!important;
  }
  .view-home .header .header-actions .favorite-header,
  .view-catalog .header .header-actions .favorite-header{
    display:grid!important;
  }
  .view-home .header .header-actions svg,
  .view-catalog .header .header-actions svg{
    width:20px!important;
    height:20px!important;
  }
  .view-home .header .header-actions .bag svg,
  .view-catalog .header .header-actions .bag svg{
    width:21px!important;
    height:21px!important;
  }
  .view-home .header .logo,
  .view-catalog .header .logo{
    font-size:16px!important;
  }
}
'''
if marker not in css:
    css=css.rstrip()+block+"\n"
CSS.write_text(css,encoding="utf-8")
print("KULTURA_HEADER_V150: high-specificity mobile home/catalog header keeps search, profile, favorites and bag visible without overlap")
