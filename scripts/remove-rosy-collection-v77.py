from pathlib import Path

root = Path(__file__).resolve().parents[1]
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
marker = "// READY_SOLUTIONS_REMOVE_ROSY_V77"

ready = ready_path.read_text(encoding="utf-8")
if marker not in ready:
    old_base = '  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна", "Росы"],'
    new_base = '  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна"],'
    if old_base in ready:
        ready = ready.replace(old_base, new_base, 1)
    elif new_base not in ready:
        raise RuntimeError("Green Salon base collections anchor not found")

    ready = ready.replace(
        '  "Петербург", "Многоцвет", "Весна", "Росы", "Алая нить",',
        '  "Петербург", "Многоцвет", "Весна", "Алая нить",',
        1,
    )
    ready = ready.replace('  if (name.includes("росы")) return "Росы";\n', '', 1)

    ready = ready.replace(
        '// READY_SOLUTIONS_RED_LINES_ALAYA_NIT_V76',
        '// READY_SOLUTIONS_RED_LINES_ALAYA_NIT_V76\n' + marker,
        1,
    )
    ready_path.write_text(ready, encoding="utf-8")

print("Ready Solutions V77: Rosy collection removed")
