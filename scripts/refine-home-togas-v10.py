from pathlib import Path

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Scope the latest homepage visual system without touching catalog/PDP behavior.
text = text.replace('return <main className="home-v4 home-reference-v5">', 'return <main className="home-v4 home-reference-v5 home-togas-v10">', 1)

# TOGAS-like homepage language: short, commercial, image-first.
text = text.replace('cta:"Смотреть новинки"', 'cta:"Смотреть"')
text = text.replace('cta:"Перейти в спальню"', 'cta:"Смотреть"')
text = text.replace('cta:"Смотреть декор"', 'cta:"Смотреть"')
text = text.replace('<small>НОВОЕ ПОСТУПЛЕНИЕ</small><h2>Новинки</h2>', '<small>НОВИНКИ</small><h2>Новое поступление</h2>', 1)
text = text.replace('<small>EDITORIAL</small><h2>Капсулы и коллекции</h2>', '<small>КОЛЛЕКЦИИ</small><h2>Капсулы и коллекции</h2>', 1)
text = text.replace('<small>ИНТЕРЬЕРНЫЕ СЦЕНАРИИ</small><h2>Готовые решения</h2>', '<small>ВДОХНОВЕНИЕ</small><h2>Готовые решения для дома</h2>', 1)
text = text.replace('<em>СОБРАТЬ РЕШЕНИЕ</em>', '<em>СМОТРЕТЬ</em>')
text = text.replace('>СМОТРЕТЬ EDITORIAL</button>', '>СМОТРЕТЬ ВСЕ</button>', 1)
text = text.replace('>НАШИ БУТИКИ</button>', '>СМОТРЕТЬ БУТИКИ</button>', 1)

PAGE.write_text(text, encoding="utf-8")
print("Applied TOGAS-inspired homepage V10 structure and copy")
