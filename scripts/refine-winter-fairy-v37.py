from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "constructor" / "table-solution-client.tsx"
client = client_path.read_text(encoding="utf-8")

# 1) Preserve exact merchandising order inside each Winter Fairy Tale group and
# guarantee that the scenario contains exactly the five groups from the approved screenshot.
old_categories = '  const categories = useMemo(() => solution ? buildSolutionCategories(rows, solution.space) : [], [rows, solution]);'
new_categories = '''  const categories = useMemo(() => {
    if (!solution) return [];
    const built = buildSolutionCategories(rows, solution.space);
    const order = (solution.productOrder || []).map(norm);
    const rank = (title: string) => {
      const value = norm(title);
      const index = order.findIndex((target) => value === target || value.includes(target) || target.includes(value));
      return index < 0 ? 9999 : index;
    };
    const reordered = built.map((category) => ({
      ...category,
      slots: category.slots.map((slot) => ({
        ...slot,
        options: [...slot.options].sort((a, b) => rank(a.title) - rank(b.title)),
      })),
    }));
    if (solution.id !== "table-7") return reordered;
    const winterOrder = ["bedding", "throwsCoverlets", "decorativePillows", "vases", "atmosphere"];
    return winterOrder.flatMap((id) => {
      const category = reordered.find((item) => item.id === id);
      return category ? [category] : [];
    });
  }, [rows, solution]);'''
if old_categories in client:
    client = client.replace(old_categories, new_categories, 1)
elif new_categories not in client:
    raise SystemExit("Winter Fairy Tale categories anchor not found")

# 2) Apply screenshot defaults for quantity, colour and size only on first load.
selection_end = '  }, [categories, solution]);\n\n  if (!solution)'
defaults_effect = '''  }, [categories, solution]);

  useEffect(() => {
    if (!solution || !options.length) return;
    const findDefault = <T,>(values: Record<string, T> | undefined, title: string): T | undefined => {
      if (!values) return undefined;
      const normalizedTitle = norm(title);
      const entry = Object.entries(values).find(([name]) => {
        const target = norm(name);
        return normalizedTitle === target || normalizedTitle.includes(target) || target.includes(normalizedTitle);
      });
      return entry?.[1];
    };

    setQty((state) => {
      if (Object.keys(state).length) return state;
      const next: Record<string, number> = {};
      options.forEach((option) => {
        const value = findDefault(solution.defaultQuantities, option.title);
        if (typeof value === "number" && value > 0) next[option.id] = value;
      });
      return next;
    });
    setColors((state) => {
      if (Object.keys(state).length) return state;
      const next: Record<string, string> = {};
      options.forEach((option) => {
        const value = findDefault(solution.defaultColors, option.title);
        if (value) next[option.id] = value;
      });
      return next;
    });
    setSizes((state) => {
      if (Object.keys(state).length) return state;
      const next: Record<string, string> = {};
      options.forEach((option) => {
        const value = findDefault(solution.defaultSizes, option.title);
        if (value) next[option.id] = value;
      });
      return next;
    });
  }, [options, solution]);

  if (!solution)'''
if "const findDefault = <T,>" not in client:
    if selection_end not in client:
        raise SystemExit("Winter Fairy Tale default state anchor not found")
    client = client.replace(selection_end, defaults_effect, 1)

# 3) Use the exact white embroidered Ice Patterns pillow from the GitHub storefront
# as the Winter Fairy Tale hero, while keeping existing preview logic for other scenarios.
old_hero = '  const hero = solution.previewFile ? `/assets/images/constructor/${solution.previewFile}` : fallback;'
new_hero = '  const hero = solution.heroImage || (solution.previewFile ? `/assets/images/constructor/${solution.previewFile}` : fallback);'
if old_hero in client:
    client = client.replace(old_hero, new_hero, 1)
elif new_hero not in client:
    raise SystemExit("Winter Fairy Tale hero image anchor not found")

client_path.write_text(client, encoding="utf-8")
print("Winter Fairy Tale V37 screenshot refinements applied")
