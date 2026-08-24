from pathlib import Path

root = Path(__file__).resolve().parents[1]

client_path = root / "app" / "constructor" / "table-solution-client.tsx"
client = client_path.read_text(encoding="utf-8")

old_selection = '      const explicit = solution.productNames.map(norm).filter(Boolean);'
new_selection = '      const explicit = (solution.defaultProductNames ?? solution.productNames).map(norm).filter(Boolean);'
if old_selection in client:
    client = client.replace(old_selection, new_selection, 1)
elif new_selection not in client:
    raise SystemExit("Green Salon selection anchor not found")

old_hero = '<div className="kd-ready-hero-copy-v29"><small>{solution.name} · {solution.space}</small><h1>ГОТОВЫЕ РЕШЕНИЯ</h1><p>Соберите идеальное пространство за несколько кликов — выберите нужные предметы, цвет и количество.</p>{solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((x) => <span key={x}>{x}</span>)}</div>}</div>'
new_hero = '<div className="kd-ready-hero-copy-v29"><small>{solution.id === "table-1" ? solution.space : `${solution.name} · ${solution.space}`}</small><h1>{solution.id === "table-1" ? solution.name.toUpperCase() : "ГОТОВЫЕ РЕШЕНИЯ"}</h1><p>Соберите идеальное пространство за несколько кликов — выберите нужные предметы, цвет и количество.</p>{solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((x) => <span key={x}>{x}</span>)}</div>}</div>'
if old_hero in client:
    client = client.replace(old_hero, new_hero, 1)
elif new_hero not in client:
    raise SystemExit("Green Salon hero anchor not found")

client_path.write_text(client, encoding="utf-8")

builder_path = root / "app" / "constructor" / "table-solution-builder.ts"
builder = builder_path.read_text(encoding="utf-8")
old_serving = '  if (greenSalon && hasAny(name, ["подставка для яйца", "подставка для яиц"])) {'
new_serving = '  if (greenSalon && (hasAny(name, ["подставка для яйца", "подставка для яиц"]) || name.includes("ваза для фруктов"))) {'
if old_serving in builder:
    builder = builder.replace(old_serving, new_serving, 1)
elif new_serving not in builder:
    raise SystemExit("Green Salon serving anchor not found")
builder_path.write_text(builder, encoding="utf-8")

print("Green Salon V35 detail refinements applied")
