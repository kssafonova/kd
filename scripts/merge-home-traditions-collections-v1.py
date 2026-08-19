from pathlib import Path

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

old = r'''    <section className="hv4-traditions" aria-label="Традиции в каждом доме">
      <div className="hv4-traditions-media">
        <img src={assetUrl("/images/russian-bedroom.png")} alt="Современная русская спальня"/>
        <img src={assetUrl("/images/editorial-table.webp")} alt="Сервировка дома"/>
        <img src={assetUrl("/images/time-hero.png")} alt="Предметы Культура дома"/>
        <div className="hv4-traditions-copy"><div><small>15 СЕКУНД · BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
      </div>
    </section>

    <section className="hv4-collections hv4-shell">
      <header className="hv4-head"><div><small>EDITORIAL</small><h2>Капсулы и коллекции</h2></div><button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ</button></header>
      <div className="hv4-collection-rail">{capsuleCards.map(card=>{
        const editorial=editorials.find(item=>item.id===card.id);
        return <button type="button" className="hv4-collection-card" key={card.id} onClick={()=>editorial&&openEditorial(editorial)}><img src={assetUrl(card.image)} alt={card.title}/><span><small>{card.kind}</small><strong>{card.title}</strong><em>СМОТРЕТЬ ИСТОРИЮ</em></span></button>;
      })}</div>
    </section>'''

new = r'''    <section className="hv4-traditions-collections" aria-label="Традиции, капсулы и коллекции">
      <div className="hv4-traditions-collections-shell">
        <div className="hv4-traditions-media">
          <img src={assetUrl("/images/russian-bedroom.png")} alt="Современная русская спальня"/>
          <img src={assetUrl("/images/editorial-table.webp")} alt="Сервировка дома"/>
          <img src={assetUrl("/images/time-hero.png")} alt="Предметы Культура дома"/>
          <div className="hv4-traditions-copy"><div><small>15 СЕКУНД · BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
        </div>

        <div className="hv4-traditions-collections-content">
          <header className="hv4-traditions-collections-head">
            <div><small>EDITORIAL</small><h2>Капсулы и коллекции</h2></div>
            <button type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ</button>
          </header>
          <div className="hv4-collection-rail">{capsuleCards.map(card=>{
            const editorial=editorials.find(item=>item.id===card.id);
            return <button type="button" className="hv4-collection-card" key={card.id} onClick={()=>editorial&&openEditorial(editorial)}><img src={assetUrl(card.image)} alt={card.title}/><span><small>{card.kind}</small><strong>{card.title}</strong><em>СМОТРЕТЬ ИСТОРИЮ</em></span></button>;
          })}</div>
        </div>
      </div>
    </section>'''

if new in text:
    print("Traditions + collections homepage block already merged")
elif old not in text:
    raise SystemExit("Expected separate traditions/collections blocks not found")
else:
    text = text.replace(old, new, 1)
    PAGE.write_text(text, encoding="utf-8")
    print("Merged traditions and collections homepage blocks")
