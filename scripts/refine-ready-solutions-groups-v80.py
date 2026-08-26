from pathlib import Path

root = Path(__file__).resolve().parents[1]
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
marker = "// READY_SOLUTIONS_GROUPS_V80"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"{label}: anchor not found")
    return text.replace(old, new, 1)


ready = ready_path.read_text(encoding="utf-8")

if marker not in ready:
    # Keep the requested Red Lines merchandising sources available by default.
    # V76 normally adds Alaya Nit before this patch; this fallback also makes the
    # rule resilient if the materialized client is rebuilt from an older source.
    ready = ready.replace(
        '  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры"],',
        '  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры", "Алая нить"],',
        1,
    )

    # Winter Fairy Tale has its own simplified taxonomy. It must never expose
    # tableware or the generic "Декор для дома" bucket. Throws and pillows are
    # one group; vases and atmosphere each receive their own group.
    old_groups = '''const GROUP_ORDER: GroupId[] = ["tableware","tableTextile","bedding","decor","bath"];
function buildGroups(categories: SolutionCategory[]): FormGroup[] {
  return GROUP_ORDER.map((id) => {
    const meta = GROUP_META[id];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
    return { id, title: meta.title, items };
  }).filter((group) => group.items.length > 0);
}'''
    new_groups = '''const GROUP_ORDER: GroupId[] = ["tableware","tableTextile","bedding","decor","bath"];
function buildGroups(solutionName: string, categories: SolutionCategory[]): FormGroup[] {
  if (norm(solutionName) === norm("Зимняя сказка")) {
    const winterGroups: Array<{ id: GroupId; title: string; categories: string[] }> = [
      { id: "bedding", title: "Постельное бельё", categories: ["bedding"] },
      { id: "decor", title: "Пледы и подушки", categories: ["throwsCoverlets", "decorativePillows"] },
      { id: "tableTextile", title: "Вазы", categories: ["vases"] },
      { id: "atmosphere", title: "Свечи и диффузоры", categories: ["atmosphere"] },
    ];
    return winterGroups.map((group) => {
      const source = categories.filter((category) => group.categories.includes(category.id));
      const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
      return { id: group.id, title: group.title, items };
    }).filter((group) => group.items.length > 0);
  }
  return GROUP_ORDER.map((id) => {
    const meta = GROUP_META[id];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
    return { id, title: meta.title, items };
  }).filter((group) => group.items.length > 0);
}'''
    ready = replace_once(ready, old_groups, new_groups, "solution-specific groups")

    ready = replace_once(
        ready,
        'const categories=useMemo(()=>solution?buildSolutionCategories(extendedRows,solution.space):[],[extendedRows,solution]); const groups=useMemo(()=>buildGroups(categories),[categories]);',
        'const categories=useMemo(()=>solution?buildSolutionCategories(extendedRows,solution.space):[],[extendedRows,solution]); const groups=useMemo(()=>solution?buildGroups(solution.name,categories):[],[solution,categories]);',
        "buildGroups call",
    )

    # Keep the new merchandising source visible in the materialized file.
    ready = ready.replace(
        '// READY_SOLUTIONS_REMOVE_ROSY_V77\nconst CART_KEY = "kultura-cart";',
        '// READY_SOLUTIONS_REMOVE_ROSY_V77\n' + marker + '\nconst CART_KEY = "kultura-cart";',
        1,
    )

    ready_path.write_text(ready, encoding="utf-8")

print("Ready Solutions V80 grouping and assortment applied")
