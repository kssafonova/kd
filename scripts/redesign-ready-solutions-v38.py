from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "constructor" / "constructor-client.tsx"
client = client_path.read_text(encoding="utf-8")

replacements = {
    '<small>ГОТОВЫЕ РЕШЕНИЯ · КУЛЬТУРА ДОМА</small>\n          <h1>Дом, собранный в единую историю</h1>\n          <p>Подборки для разных пространств, в которых предметы из нескольких коллекций уже сочетаются между собой. Выберите сценарий и настройте состав под себя.</p>\n          <a href="#ready-solutions-grid">СМОТРЕТЬ РЕШЕНИЯ <HeaderIcon name="arrow"/></a>':
    '<small>ГОТОВЫЕ РЕШЕНИЯ</small>\n          <h1>Соберите дом как цельную историю</h1>\n          <p>Готовые сочетания для спальни, гостиной и столовой. Мы уже собрали предметы по настроению — вам остаётся выбрать сценарий и настроить детали под себя.</p>\n          <a href="#ready-solutions-grid">ВЫБРАТЬ РЕШЕНИЕ <HeaderIcon name="arrow"/></a>',

    '<section className="kd-solutions-heading-v33" id="ready-solutions-grid"><div><small>ПОДБОРКИ ДЛЯ ДОМА</small><h2>Выберите свою историю</h2></div><p>Каждое решение можно изменить: убрать ненужное, выбрать другую коллекцию, цвет, размер и количество.</p></section>':
    '<section className="kd-solutions-heading-v33" id="ready-solutions-grid"><div><small>СЦЕНАРИИ</small><h2>Готовые сочетания для дома</h2></div><p>Выберите пространство, откройте решение и оставьте только те предметы, которые нужны именно вам.</p></section>',

    '<header><small>КАК ЭТО РАБОТАЕТ</small><h2>От идеи до готового пространства</h2></header>':
    '<header><small>КАК ЭТО РАБОТАЕТ</small><h2>Три шага — и пространство собрано</h2></header>',

    '<div><small>КУЛЬТУРА ДОМА</small><h2>Современный русский дом без буквального декора</h2><p>Мы соединяем фактуру, цвет, традицию и современную форму так, чтобы вещи легко жили вместе и не требовали сложного подбора.</p></div>':
    '<div><small>КУЛЬТУРА ДОМА</small><h2>Традиции, которые живут в современном доме</h2><p>Фактура, цвет и знакомые мотивы соединяются с лаконичной современной формой — спокойно, небуквально и без лишнего декора.</p></div>',
}

for old, new in replacements.items():
    if old in client:
        client = client.replace(old, new, 1)
    elif new not in client:
        raise SystemExit(f"Ready solutions V38 anchor not found: {old[:80]}")

client_path.write_text(client, encoding="utf-8")
print("Ready solutions V38 editorial copy applied")
