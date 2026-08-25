from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "constructor" / "constructor-client.tsx"
client = client_path.read_text(encoding="utf-8")

old_hero = '''      <section className="kd-solutions-hero-v33">
        <div className="kd-solutions-hero-copy-v33">
          <small>ГОТОВЫЕ РЕШЕНИЯ</small>
          <h1>Соберите дом как цельную историю</h1>
          <p>Готовые сочетания для спальни, гостиной и столовой. Мы уже собрали предметы по настроению — вам остаётся выбрать сценарий и настроить детали под себя.</p>
          <a href="#ready-solutions-grid">ВЫБРАТЬ РЕШЕНИЕ <HeaderIcon name="arrow"/></a>
        </div>
        <div className="kd-solutions-hero-media-v33">
          {heroCard && <RemoteImage src={heroCard.previewFile ? `/images/constructor/${heroCard.previewFile}` : heroCard.fallbackImage} fallbackSrc={heroCard.fallbackImage} alt={heroCard.name} loading="eager"/>}
          {heroCard && <span><small>{heroCard.space}</small><b>{heroCard.name}</b></span>}
        </div>
      </section>'''

new_hero = '''      <section className="kd-solutions-hero-v39">
        <div className="kd-solutions-hero-stage-v39">
          <div className="kd-solutions-hero-copy-v39">
            <small>ГОТОВЫЕ РЕШЕНИЯ · КУЛЬТУРА ДОМА</small>
            <h1>Пространство, собранное за вас</h1>
            <p>Готовые сочетания предметов из разных коллекций. Выберите историю, настройте состав и добавьте всё нужное в корзину одним сценарием.</p>
            <a href="#ready-solutions-grid">СМОТРЕТЬ РЕШЕНИЯ <HeaderIcon name="arrow"/></a>
          </div>
          <div className="kd-solutions-hero-media-v39">
            {heroCard && <RemoteImage src={heroCard.previewFile ? `/images/constructor/${heroCard.previewFile}` : heroCard.fallbackImage} fallbackSrc={heroCard.fallbackImage} alt={heroCard.name} loading="eager"/>}
            {heroCard && <div className="kd-solutions-hero-caption-v39"><small>{heroCard.space}</small><span>{heroCard.name}</span></div>}
          </div>
        </div>
        <div className="kd-solutions-hero-steps-v39" aria-label="Как это работает">
          <article><b>01</b><div><h2>Выберите сценарий</h2><p>Начните с пространства и количества персон.</p></div></article>
          <article><b>02</b><div><h2>Настройте состав</h2><p>Оставьте нужные товары, цвета, размеры и количество.</p></div></article>
          <article><b>03</b><div><h2>Добавьте всё сразу</h2><p>Готовый состав переносится в корзину отдельными товарами.</p></div></article>
        </div>
      </section>'''

if "kd-solutions-hero-v39" not in client:
    if old_hero not in client:
        raise SystemExit("Ready solutions V39 hero anchor not found")
    client = client.replace(old_hero, new_hero, 1)

old_how = '''      <section className="kd-solutions-how-v33">
        <header><small>КАК ЭТО РАБОТАЕТ</small><h2>Три шага — и пространство собрано</h2></header>
        <div><article><b>01</b><h3>Выберите сценарий</h3><p>Начните с пространства и количества персон — мы покажем подходящие решения.</p></article><article><b>02</b><h3>Настройте состав</h3><p>Сравните товары по группам, выберите коллекции, цвета, размеры и количество.</p></article><article><b>03</b><h3>Добавьте всё сразу</h3><p>Готовый набор одной кнопкой переносится в корзину отдельными товарами.</p></article></div>
      </section>

'''
if old_how in client:
    client = client.replace(old_how, "", 1)
elif "kd-solutions-how-v33" in client and "kd-solutions-hero-v39" in client:
    raise SystemExit("Ready solutions V39 old how-to block still present")

client_path.write_text(client, encoding="utf-8")
print("Ready solutions V39 integrated hero and steps applied")
