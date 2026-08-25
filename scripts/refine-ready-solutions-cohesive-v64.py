from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
text = path.read_text(encoding="utf-8")

if "READY_SOLUTIONS_COHESIVE_UX_V64" in text:
    print("Ready Solutions V64 already applied")
    raise SystemExit(0)

text = text.replace(
    'type WizardStep = 1 | 2 | 3;',
    '// READY_SOLUTIONS_COHESIVE_UX_V64\ntype WizardStep = 1 | 2 | 3;',
    1,
)

replacements = {
    '<div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Соберите пространство целиком</h1><p>Выберите пространство. Внутри можно настроить количество, состав, цвет и заменить любой предмет.</p></div>':
    '<div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Готовые решения для дома</h1><p>Выберите пространство и адаптируйте готовую композицию под себя.</p></div>',

    '<p>Готовая композиция, которую можно адаптировать под своё пространство. Меняйте количество, коллекции и отдельные предметы.</p>':
    '<p>Выберите основу и настройте её под своё пространство.</p>',

    '<p>Выберите количество персон и коллекции, которые хотите использовать в решении.</p>':
    '<p>Количество персон и коллекции определяют основу будущего состава.</p>',

    '"Категории и товары находятся в одном месте. Переключайтесь между категориями, отмечайте нужные предметы и сразу выбирайте цвет, размер и количество."':
    '"Выберите товары и настройте цвет, размер и количество."',

    '<p>Финальный moodboard решения. Цвет каждого товара уже зафиксирован на выборе из шага «Состав» — здесь остаётся только собранный образ.</p>':
    '<p>Готовый образ. Цвета уже выбраны; при необходимости замените или удалите предмет.</p>',
}

for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"V64 copy anchor not found: {old[:80]}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Ready Solutions V64 applied")
