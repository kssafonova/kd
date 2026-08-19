from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

# Make the final homepage layer explicit and idempotent.
text = text.replace(
    'className="home-v4 home-reference-v5 home-togas-v10"',
    'className="home-v4 home-reference-v5 home-togas-v10 home-ux-v11"',
)

# Add the reusable homepage boutique map before HomeView.
marker = "// HOME_BOUTIQUES_MAP_V11"
if marker not in text:
    component = r'''
// HOME_BOUTIQUES_MAP_V11
function HomeBoutiques(){
  const boutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124},
  ];
  const [selected,setSelected]=useState(0);
  const boutique=boutiques[selected];
  const delta=.04;
  const mapSrc=`https://www.openstreetmap.org/export/embed.html?bbox=${boutique.lon-delta}%2C${boutique.lat-delta}%2C${boutique.lon+delta}%2C${boutique.lat+delta}&layer=mapnik&marker=${boutique.lat}%2C${boutique.lon}`;
  return <section id="home-boutiques" className="home-boutiques-map" aria-labelledby="home-boutiques-title">
    <div className="home-boutiques-copy">
      <small>БУТИКИ</small>
      <h2 id="home-boutiques-title">Посетите Культура дома</h2>
      <p>Посмотрите материалы, оттенки и коллекции вживую. Выберите город — карта покажет расположение бутика.</p>
      <div className="home-boutique-list" aria-label="Выбрать бутик">
        {boutiques.map((item,index)=><button type="button" key={item.city} className={index===selected?"active":""} onClick={()=>setSelected(index)} aria-pressed={index===selected}>
          <span><Icon name="pin"/><b>{item.city}</b></span>
          <strong>{item.address}</strong>
          <small>{item.hours}</small>
        </button>)}
      </div>
    </div>
    <div className="home-boutiques-map-canvas">
      <iframe key={`${boutique.city}-${selected}`} src={mapSrc} title={`Карта бутика Культура дома — ${boutique.city}`} loading="lazy" referrerPolicy="no-referrer-when-downgrade"/>
      <div className="home-boutiques-map-caption"><div><b>{boutique.city}</b><span>{boutique.address}</span></div><small>{boutique.hours}</small></div>
    </div>
  </section>;
}

'''
    anchor = "function HomeView("
    if anchor not in text:
        raise SystemExit("HomeView anchor not found")
    text = text.replace(anchor, component + anchor, 1)

# Replace the old static brand/boutiques promo with the real store finder.
start_token = '    <section className="hv4-brand-boutiques">'
start = text.find(start_token)
if start != -1:
    end = text.find("    </section>", start)
    if end == -1:
        raise SystemExit("Boutiques section closing tag not found")
    end += len("    </section>")
    text = text[:start] + "    <HomeBoutiques/>" + text[end:]

# Header boutiques should open the same map from every storefront view.
old_header_sig = 'function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {'
new_header_sig = 'function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, onBoutiques, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; onBoutiques:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {'
text = text.replace(old_header_sig, new_header_sig)
text = text.replace(
    '<button className="boutiques" onClick={() => alert("Бутики: Москва · Санкт-Петербург · Казань")}><Icon name="pin"/> Бутики</button>',
    '<button className="boutiques" onClick={onBoutiques}><Icon name="pin"/> Бутики</button>',
)

# Add global boutiques-map dialog state, also available away from the homepage.
state_anchor = '  const [checkoutOpen, setCheckoutOpen] = useState(false);'
if 'const [boutiquesOpen,setBoutiquesOpen]' not in text:
    if state_anchor not in text:
        raise SystemExit("checkoutOpen state anchor not found")
    text = text.replace(state_anchor, state_anchor + '\n  const [boutiquesOpen,setBoutiquesOpen]=useState(false);', 1)

text = text.replace(
    'menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen ? "hidden" : ""',
    'menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen || boutiquesOpen ? "hidden" : ""',
)
text = text.replace(
    '[menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen]);',
    '[menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen, boutiquesOpen]);',
)

# Wire Header to the map dialog.
header_call = '<Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />'
header_call_v11 = '<Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} onBoutiques={() => setBoutiquesOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />'
text = text.replace(header_call, header_call_v11)

# Render the shared BoutiqueMap modal before toast.
if '{boutiquesOpen&&<BoutiqueMap close={()=>setBoutiquesOpen(false)}/>}' not in text:
    toast_anchor = '      {toast && <div className="toast">{toast}</div>}'
    if toast_anchor not in text:
        raise SystemExit("Toast anchor not found")
    text = text.replace(toast_anchor, '      {boutiquesOpen&&<BoutiqueMap close={()=>setBoutiquesOpen(false)}/>}\n' + toast_anchor, 1)

page_path.write_text(text, encoding="utf-8")
print("Homepage UX V11 patch applied")
