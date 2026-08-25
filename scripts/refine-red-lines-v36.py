from pathlib import Path

root = Path(__file__).resolve().parents[1]
builder_path = root / "app" / "constructor" / "table-solution-builder.ts"
builder = builder_path.read_text(encoding="utf-8")

# 1) Add screenshot-specific category labels.
anchor_meta = '''  greenSalonTeaService: {
    title: "Чайники, сахарницы и молочники",
    description: "Чайники, сахарницы, молочники и сливочники собраны в одном блоке, как в сценарии «Зеленый салон».",
  },
'''
insert_meta = anchor_meta + '''  redLinesServing: {
    title: "БЛЮДА, САЛАТНИКИ И ПОДАЧА",
    description: "Салатники, глубокие тарелки, блюда и супницы Камея собраны в одном блоке, как на утвержденном макете «Красные линии».",
  },
  redLinesTeaService: {
    title: "Чайники, сахарницы и молочники",
    description: "Чайник, сахарница и молочник Камея собраны в одном блоке, как на утвержденном макете «Красные линии».",
  },
'''
if "redLinesServing:" not in builder:
    if anchor_meta not in builder:
        raise SystemExit("Red Lines category meta anchor not found")
    builder = builder.replace(anchor_meta, insert_meta, 1)

# 2) Detect Red Lines without affecting other table solutions.
anchor_detector = '''const isGreenSalonRows = (rows: CatalogRow[]) => {
  const names = rows.map((row) => normalize(row.product_name));
  return names.some((name) => name.includes("пасхальная весна")) &&
    names.some((name) => name.includes("петербург")) &&
    names.some((name) => name.includes("овация"));
};

'''
insert_detector = anchor_detector + '''const isRedLinesRows = (rows: CatalogRow[]) => {
  const names = rows.map((row) => normalize(row.product_name));
  return names.some((name) => name.includes("тарелка десертная мокоши")) &&
    names.some((name) => name.includes("кофейная пара камея")) &&
    names.some((name) => name.includes("супница камея"));
};

'''
if "const isRedLinesRows" not in builder:
    if anchor_detector not in builder:
        raise SystemExit("Red Lines detector anchor not found")
    builder = builder.replace(anchor_detector, insert_detector, 1)

# 3) Pass the scenario flag into the category classifier.
old_signature = 'const categoryForRow = (row: CatalogRow, space: string, greenSalon = false) => {'
new_signature = 'const categoryForRow = (row: CatalogRow, space: string, greenSalon = false, redLines = false) => {'
if old_signature in builder:
    builder = builder.replace(old_signature, new_signature, 1)
elif new_signature not in builder:
    raise SystemExit("Red Lines category signature anchor not found")

# 4) Apply screenshot grouping before the generic category rules.
anchor_rules = '''  // Green Salon follows the approved merchandising screenshot: tea pots,
  // sugar bowls and milk/cream jugs are one comparison group.
'''
red_rules = '''  // Red Lines follows the approved screenshot: bowls/deep plates and serving
  // pieces are one block; tea service pieces are another block.
  if (redLines && (
    hasAny(name, ["тарелка глубок", "салатник", "супниц", "блюдо"]) ||
    hasAny(type, ["deep_plate", "salad_bowl", "serving_dish", "soup_tureen", "tureen"])
  )) {
    const perPerson = name.includes("тарелка глубок") || type.includes("deep_plate");
    return { id: "redLinesServing", perPerson };
  }

  if (redLines && (
    name.includes("сахарниц") || type.includes("sugar_bowl") ||
    hasAny(name, ["молочник", "сливочник"]) || type.includes("milk_jug") ||
    name.includes("чайник") || type.includes("teapot")
  )) return { id: "redLinesTeaService", perPerson: false };

'''
if "Red Lines follows the approved screenshot" not in builder:
    if anchor_rules not in builder:
        raise SystemExit("Red Lines rules anchor not found")
    builder = builder.replace(anchor_rules, red_rules + anchor_rules, 1)

# 5) Preserve the screenshot order: plates -> serving -> cups -> tea -> textile.
old_order = '''const categoryOrder = [
  "plates",
  "bowls",
  "cupsPairs",
  "greenSalonTeaService",
'''
new_order = '''const categoryOrder = [
  "plates",
  "redLinesServing",
  "bowls",
  "cupsPairs",
  "greenSalonTeaService",
  "redLinesTeaService",
'''
if old_order in builder:
    builder = builder.replace(old_order, new_order, 1)
elif '  "redLinesServing",' not in builder or '  "redLinesTeaService",' not in builder:
    raise SystemExit("Red Lines category order anchor not found")

# 6) Detect and pass Red Lines during category construction.
old_build = '''  const categoryMap = new Map<string, Map<string, { perPerson: boolean; variants: CatalogRow[] }>>();
  const greenSalon = isGreenSalonRows(rows);

  rows.forEach((row) => {
    const category = categoryForRow(row, space, greenSalon);
'''
new_build = '''  const categoryMap = new Map<string, Map<string, { perPerson: boolean; variants: CatalogRow[] }>>();
  const greenSalon = isGreenSalonRows(rows);
  const redLines = isRedLinesRows(rows);

  rows.forEach((row) => {
    const category = categoryForRow(row, space, greenSalon, redLines);
'''
if old_build in builder:
    builder = builder.replace(old_build, new_build, 1)
elif "const redLines = isRedLinesRows(rows);" not in builder:
    raise SystemExit("Red Lines build anchor not found")

builder_path.write_text(builder, encoding="utf-8")
print("Red Lines V36 screenshot refinements applied")
