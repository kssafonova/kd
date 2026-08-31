from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
HOME=ROOT/"app"/"home-standalone.tsx"
STORE=ROOT/"app"/"storefront-app.tsx"

home=HOME.read_text(encoding="utf-8")
# Keep homepage as a lightweight independent route, but every commerce action
# opens the canonical Kultura doma form inside the catalog route.
home=home.replace('onClick={()=>setMenu(true)}','onClick={()=>navigate("/catalog/?open=menu")}',1)
home=home.replace('onClick={()=>document.getElementById("home-boutiques")?.scrollIntoView({behavior:"smooth"})}','onClick={()=>navigate("/catalog/?open=boutiques")}',1)
# Remove the simplified standalone menu from the rendered tree. The canonical
# Menu component lives in StorefrontApp and is opened via ?open=menu.
home=re.sub(r'\n\s*\{menu&&<div className="home-fast-menu".*?</div>\}\n',"\n",home,count=1,flags=re.S)
# Same card interaction contract as PLP: media/title => PDP, quick icon => PLP quick-add.
home=home.replace('const productHref=url(`/catalog/?product=${encodeURIComponent(product.article??String(product.id))}`);return <article', 'const article=encodeURIComponent(product.article??String(product.id));const productHref=url(`/catalog/?product=${article}`);const quickHref=url(`/catalog/?quick=${article}`);return <article',1)
home=home.replace('<a className="quick home-fast-quick" href={productHref} aria-label={`Выбрать ${product.name}`}>','<a className="quick home-fast-quick" href={quickHref} aria-label={`Выбрать ${product.name}`}>',1)
HOME.write_text(home,encoding="utf-8")

store=STORE.read_text(encoding="utf-8")
# Deep-link bridge for homepage product cards. This opens existing Kultura PDP
# or PLPSizeFlow, never a duplicate lightweight modal.
if 'const requestedProduct=params.get("product");' not in store:
    store=store.replace('const requestedCollection=params.get("collection");','const requestedCollection=params.get("collection");\n    const requestedProduct=params.get("product");\n    const requestedQuick=params.get("quick");',1)
bridge='''    const requestedCommerceProduct=requestedProduct||requestedQuick;
    if(requestedCommerceProduct){
      const productKey=String(requestedCommerceProduct).trim().toLocaleLowerCase("ru-RU");
      const matched=products.find(item=>String(item.id)===requestedCommerceProduct||String(item.article||"").trim().toLocaleLowerCase("ru-RU")===productKey);
      if(matched){
        if(requestedQuick)setPlpSize(matched);
        else {setSelected(matched);setRecentlyViewed(current=>[matched.id,...current.filter(id=>id!==matched.id)].slice(0,6));setView("product")}
      }
    }
'''
if 'const requestedCommerceProduct=requestedProduct||requestedQuick;' not in store:
    needle='    if(open==="cart")setCartOpen(true);'
    if needle not in store: raise SystemExit("KULTURA_NAV_V146: query open bridge not found")
    store=store.replace(needle,bridge+needle,1)
store=store.replace('if(section||open||requestedCollection)window.history.replaceState({},"",window.location.pathname);','if(section||open||requestedCollection||requestedProduct||requestedQuick)window.history.replaceState({},"",window.location.pathname);',1)
STORE.write_text(store,encoding="utf-8")

print("KULTURA_NAV_V146: homepage actions now open canonical Kultura menu/search/account/favorites/cart/boutiques; product cards bridge to canonical PDP/PLP quick-add")
