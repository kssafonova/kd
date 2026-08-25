from pathlib import Path

root = Path(__file__).resolve().parents[1]
landing_path = root / "app" / "constructor" / "constructor-client.tsx"
detail_path = root / "app" / "constructor" / "table-solution-client.tsx"
landing = landing_path.read_text(encoding="utf-8")
detail = detail_path.read_text(encoding="utf-8")

# Landing refinements run after V38/V39, keeping their integrated hero/steps structure.
landing = landing.replace('className="kd-solutions-page-v33"', 'className="kd-solutions-page-v33 kd-solutions-v46"', 1)
landing = landing.replace('<span>Количество персон</span>', '<span>Количество человек</span>', 1)
landing = landing.replace('<h2>Выберите свою историю</h2>', '<h2>Готовые пространства</h2>', 1)
landing = landing.replace('Каждое решение можно изменить: убрать ненужное, выбрать другую коллекцию, цвет, размер и количество.', 'Выберите готовую основу и настройте только то, что важно: состав, оттенок, размер и количество.', 1)

# Detail: give the scenario its own identity rather than repeating the landing title.
detail = detail.replace('className="solution-simple-shell kd-ready-v29"', 'className="solution-simple-shell kd-ready-v29 kd-ready-v46"', 1)
old_hero = '''      <section className="kd-ready-hero-v29">
        <div className="kd-ready-hero-copy-v29"><small>{solution.name} · {solution.space}</small><h1>ГОТОВЫЕ РЕШЕНИЯ</h1><p>Соберите идеальное пространство за несколько кликов — выберите нужные предметы, цвет и количество.</p>{solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((x) => <span key={x}>{x}</span>)}</div>}</div>
        <div className="kd-ready-hero-media-v29"><RemoteImage src={hero} fallbackSrc={fallback} alt={solution.name} loading="eager"/></div>
      </section>'''
new_hero = '''      <section className="kd-ready-hero-v29 kd-ready-hero-v46">
        <div className="kd-ready-hero-copy-v29"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция для дома. Оставьте нужные предметы, выберите цвет и размер — итог пересчитается автоматически.</p>{solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((x) => <span key={x}>{x}</span>)}</div>}<button type="button" className={`kd-ready-hero-save-v46 ${saved ? "saved" : ""}`} onClick={save}>{saved ? "✓ Решение сохранено" : "♡ Сохранить решение"}</button></div>
        <div className="kd-ready-hero-media-v29"><RemoteImage src={hero} fallbackSrc={fallback} alt={solution.name} loading="eager"/></div>
      </section>'''
if old_hero in detail:
    detail = detail.replace(old_hero, new_hero, 1)
elif 'kd-ready-hero-v46' not in detail:
    raise SystemExit('V46 detail hero anchor not found')

old_guests = '''      <section className="kd-ready-guests-v29"><span>Сколько персон будет за столом?</span><div role="group">{guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQty({}); }}><b>{value}</b><em>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</em></button>)}</div></section>'''
new_guests = '''      <section className="kd-ready-guests-v29 kd-ready-guests-v46"><div><small>СОСТАВ РЕШЕНИЯ</small><span>{solution.space.includes("Кухня") ? "На сколько человек сервируем?" : "Для скольких человек собираем решение?"}</span></div><div role="group">{guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQty({}); }}><b>{value}</b><em>{value === 1 ? "человек" : "человека"}</em></button>)}</div></section>'''
if old_guests in detail:
    detail = detail.replace(old_guests, new_guests, 1)
elif 'kd-ready-guests-v46' not in detail:
    raise SystemExit('V46 guest selector anchor not found')

commerce_anchor = '''      {!rows.length ? <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены</h2></div></section> : <div className="kd-ready-commerce-v29">'''
commerce_replacement = '''      {!rows.length ? <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены</h2></div></section> : <><nav className="kd-ready-category-nav-v46" aria-label="Группы товаров">{categories.map((category) => { const list = category.slots.flatMap((slot) => slot.options); const selectedCount = list.filter(checked).length; return <a key={category.id} href={`#solution-category-${category.id}`}><span>{category.title}</span><small>{selectedCount}/{list.length}</small></a>; })}</nav><div className="kd-ready-commerce-v29 kd-ready-commerce-v46">'''
if commerce_anchor in detail:
    detail = detail.replace(commerce_anchor, commerce_replacement, 1)
elif 'kd-ready-category-nav-v46' not in detail:
    raise SystemExit('V46 category nav anchor not found')

# Close the fragment introduced around category nav + commerce grid.
old_close = '''        </aside>
      </div>}'''
new_close = '''        </aside>
      </div></>}'''
if old_close in detail:
    detail = detail.replace(old_close, new_close, 1)
elif '</div></>}' not in detail:
    raise SystemExit('V46 commerce fragment close anchor not found')

detail = detail.replace('<dt>Персон</dt><dd>{guests}</dd>', '<dt>Человек</dt><dd>{guests}</dd>', 1)
detail = detail.replace('"ДОБАВИТЬ В КОРЗИНУ"', '"ДОБАВИТЬ ВЕСЬ СОСТАВ"', 1)
detail = detail.replace('"♡ СОХРАНИТЬ РЕШЕНИЕ"', '"♡ СОХРАНИТЬ"', 1)

landing_path.write_text(landing, encoding="utf-8")
detail_path.write_text(detail, encoding="utf-8")
print("Applied V46 ready solutions and constructor UX redesign")
