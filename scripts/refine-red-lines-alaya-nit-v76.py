from pathlib import Path

root = Path(__file__).resolve().parents[1]
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
marker = "// READY_SOLUTIONS_RED_LINES_ALAYA_NIT_V76"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"{label}: anchor not found")
    return text.replace(old, new, 1)


ready = ready_path.read_text(encoding="utf-8")
if marker not in ready:
    # Alaya Nit is a fifth default-selected source collection for Red Lines.
    ready = replace_once(
        ready,
        '  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры"],',
        '  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры", "Алая нить"],',
        'Red Lines base collections',
    )

    # The feed has no explicit collection value for the two Alaya Nit SKUs,
    # so infer it from their product names and make it available to collection matching.
    ready = replace_once(
        ready,
        '  "Петербург", "Многоцвет", "Весна", "Росы",\n] as const;',
        '  "Петербург", "Многоцвет", "Весна", "Росы", "Алая нить",\n] as const;',
        'Alaya Nit source hint',
    )
    ready = replace_once(
        ready,
        '  if (name.includes("росы")) return "Росы";\n  // The eligible feed names this SKU “Весенний сад”; merchandise the requested teapot inside the live “Весна” Green Salon collection.',
        '  if (name.includes("росы")) return "Росы";\n  if (name.includes("алая нить")) return "Алая нить";\n  // The eligible feed names this SKU “Весенний сад”; merchandise the requested teapot inside the live “Весна” Green Salon collection.',
        'Alaya Nit collection inference',
    )

    # Keep this migration idempotent and visible in the materialized source.
    ready = replace_once(
        ready,
        '// READY_SOLUTIONS_MERCH_V75\nconst CART_KEY = "kultura-cart";',
        '// READY_SOLUTIONS_MERCH_V75\n' + marker + '\nconst CART_KEY = "kultura-cart";',
        'V76 marker',
    )
    ready_path.write_text(ready, encoding="utf-8")

print("Ready Solutions V76 Alaya Nit merchandising applied")
