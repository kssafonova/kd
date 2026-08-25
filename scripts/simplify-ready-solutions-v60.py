from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
text = path.read_text(encoding="utf-8")

if "READY_SOLUTIONS_SIMPLIFIED_V60" in text:
    print("Ready Solutions V60 already applied")
    raise SystemExit(0)

# 1) Landing: one decision only — space. Collection context remains only when entered
# from an editorial collection.
text = text.replace(
'''  const [space, setSpace] = useState("all");
  const [guests, setGuests] = useState("all");
  const [category, setCategory] = useState("all");''',
'''  // READY_SOLUTIONS_SIMPLIFIED_V60
  const [space, setSpace] = useState("all");''',
1)
text = text.replace(
'''  const guestValues = Array.from(new Set(cards.flatMap((card) => card.guestOptions))).sort((a, b) => a - b);
  const categories = Array.from(new Set(cards.flatMap((card) => card.groups.map((group) => group.title))));
  const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(value) === norm(collectionContext))) && (space === "all" || card.solution.space === space) && (guests === "all" || card.guestOptions.includes(Number(guests))) && (category === "all" || card.groups.some((group) => group.title === category)));
  const reset = () => { setSpace("all"); setGuests("all"); setCategory("all"); };''',
'''  const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(value) === norm(collectionContext))) && (space === "all" || card.solution.space === space));
  const reset = () => { setSpace("all"); };''',
1)
text = text.replace(
'''      <section className="rs57-intro">
        <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Пространство, которое легко собрать</h1><p>Выберите зону и готовый сценарий. Мы уже совместили предметы по стилю и цвету — вам остаётся настроить количество персон, состав и варианты товаров.</p></div>
        <ol><li><b>01</b><span><strong>Выберите решение</strong><small>по пространству и задаче</small></span></li><li><b>02</b><span><strong>Настройте состав</strong><small>те же товары, что в каталоге</small></span></li><li><b>03</b><span><strong>Проверьте результат</strong><small>замените или удалите предметы</small></span></li></ol>
      </section>''',
'''      <section className="rs57-intro rs60-intro">
        <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Соберите пространство целиком</h1><p>Выберите пространство. Внутри можно настроить количество, состав, цвет и заменить любой предмет.</p></div>
      </section>''',
1)
text = text.replace(
'''        <div className="rs57-filterbar" aria-label="Фильтры готовых решений">
          <label><span>Пространство</span><select value={space} onChange={(event) => setSpace(event.target.value)}><option value="all">Все пространства</option>{spaces.map((value) => <option key={value}>{value}</option>)}</select></label>
          <label><span>Количество персон</span><select value={guests} onChange={(event) => setGuests(event.target.value)}><option value="all">Любое</option>{guestValues.map((value) => <option value={value} key={value}>{value} {value === 1 ? "персона" : value <= 4 ? "персоны" : "персон"}</option>)}</select></label>
          <label><span>Категория</span><select value={category} onChange={(event) => setCategory(event.target.value)}><option value="all">Все категории</option>{categories.map((value) => <option key={value}>{value}</option>)}</select></label>
          {(space !== "all" || guests !== "all" || category !== "all") && <button type="button" onClick={reset}>Сбросить</button>}
        </div>''',
'''        <div className="rs57-filterbar rs60-space-filter" aria-label="Фильтр по пространству">
          <label><span>Пространство</span><select value={space} onChange={(event) => setSpace(event.target.value)}><option value="all">Все пространства</option>{spaces.map((value) => <option key={value}>{value}</option>)}</select></label>
          {space !== "all" && <button type="button" onClick={reset}>Сбросить</button>}
        </div>''',
1)

# 2) Composition: collection is a filter beside product type, not a separate step.
text = text.replace(
'''  const [filters, setFilters] = useState<Record<string, string>>({});''',
'''  const [filters, setFilters] = useState<Record<string, string>>({});
  const [collectionFilters, setCollectionFilters] = useState<Record<string, string>>({});''',
1)
text = text.replace(
'''          <ProductGroup group={active} filter={filters[active.id] || "all"} onFilter={(value) => setFilters((current) => ({ ...current, [active.id]: value }))} selected={selected} colors={colors} sizes={sizes} qty={qty} guests={guests} replacingId={replaceOptionId} onSelected={handleSelect} onColor={(id, value) => { setColors((current) => ({ ...current, [id]: value })); const option = active.items.find((item) => item.option.id === id)?.option; if (option) setSizes((current) => ({ ...current, [id]: optionSizes(option, value)[0] || "" })); }} onSize={(id, value) => setSizes((current) => ({ ...current, [id]: value }))} onQty={(id, value) => setQty((current) => ({ ...current, [id]: Math.max(1, value) }))}/>''',
'''          <ProductGroup group={active} filter={filters[active.id] || "all"} onFilter={(value) => setFilters((current) => ({ ...current, [active.id]: value }))} collectionFilter={collectionFilters[active.id] || "all"} onCollectionFilter={(value) => setCollectionFilters((current) => ({ ...current, [active.id]: value }))} selected={selected} colors={colors} sizes={sizes} qty={qty} guests={guests} replacingId={replaceOptionId} onSelected={handleSelect} onColor={(id, value) => { setColors((current) => ({ ...current, [id]: value })); const option = active.items.find((item) => item.option.id === id)?.option; if (option) setSizes((current) => ({ ...current, [id]: optionSizes(option, value)[0] || "" })); }} onSize={(id, value) => setSizes((current) => ({ ...current, [id]: value }))} onQty={(id, value) => setQty((current) => ({ ...current, [id]: Math.max(1, value) }))}/>''',
1)

old_product_group = '''function ProductGroup({ group, filter, onFilter, selected, colors, sizes, qty, guests, replacingId, onSelected, onColor, onSize, onQty }: { group: FormGroup; filter: string; onFilter: (value: string) => void; selected: Record<string, boolean>; colors: Record<string, string>; sizes: Record<string, string>; qty: Record<string, number>; guests: number; replacingId: string | null; onSelected: (id: string, value: boolean) => void; onColor: (id: string, value: string) => void; onSize: (id: string, value: string) => void; onQty: (id: string, value: number) => void }) {
  const subcategories = Array.from(new Map(group.items.map((item) => [item.subcategoryId, item.subcategoryTitle])).entries());
  const visible = filter === "all" ? group.items : group.items.filter((item) => item.subcategoryId === filter);
  const allVisibleSelected = visible.length > 0 && visible.every(({ option }) => selected[option.id]);
  return <section className="rs57-product-group">
    <header><div><small>КАТЕГОРИЯ</small><h3>{group.title}</h3><p>{group.description}</p></div>{!replacingId && <button type="button" onClick={() => visible.forEach(({ option }) => onSelected(option.id, !allVisibleSelected))}>{allVisibleSelected ? "Снять всё" : "Выбрать всё"}</button>}</header>
    {subcategories.length > 1 && <div className="rs57-subfilters"><button type="button" className={filter === "all" ? "is-active" : ""} onClick={() => onFilter("all")}>Все</button>{subcategories.map(([id, title]) => <button type="button" key={id} className={filter === id ? "is-active" : ""} onClick={() => onFilter(id)}>{title}</button>)}</div>}
    <div className="product-grid rs57-product-grid">{visible.map((item) => <ReadyCatalogCard key={item.option.id} option={item.option} selected={Boolean(selected[item.option.id])} color={colors[item.option.id] || ""} size={sizes[item.option.id] || ""} quantity={qty[item.option.id] || recommendedOptionQuantity(item.option, guests)} guests={guests} replacing={Boolean(replacingId)} replacingSelf={replacingId === item.option.id} onToggle={() => onSelected(item.option.id, !selected[item.option.id])} onColor={(value) => onColor(item.option.id, value)} onSize={(value) => onSize(item.option.id, value)} onQty={(value) => onQty(item.option.id, value)}/>)}</div>
  </section>;
}'''
new_product_group = '''function ProductGroup({ group, filter, onFilter, collectionFilter, onCollectionFilter, selected, colors, sizes, qty, guests, replacingId, onSelected, onColor, onSize, onQty }: { group: FormGroup; filter: string; onFilter: (value: string) => void; collectionFilter: string; onCollectionFilter: (value: string) => void; selected: Record<string, boolean>; colors: Record<string, string>; sizes: Record<string, string>; qty: Record<string, number>; guests: number; replacingId: string | null; onSelected: (id: string, value: boolean) => void; onColor: (id: string, value: string) => void; onSize: (id: string, value: string) => void; onQty: (id: string, value: number) => void }) {
  const subcategories = Array.from(new Map(group.items.map((item) => [item.subcategoryId, item.subcategoryTitle])).entries());
  const collections = Array.from(new Set(group.items.map((item) => item.option.collection).filter(Boolean))).sort((a, b) => a.localeCompare(b, "ru"));
  const visible = group.items.filter((item) => (filter === "all" || item.subcategoryId === filter) && (collectionFilter === "all" || norm(item.option.collection) === norm(collectionFilter)));
  const allVisibleSelected = visible.length > 0 && visible.every(({ option }) => selected[option.id]);
  return <section className="rs57-product-group rs60-product-group">
    <header><div><small>КАТЕГОРИЯ</small><h3>{group.title}</h3></div>{!replacingId && <button type="button" onClick={() => visible.forEach(({ option }) => onSelected(option.id, !allVisibleSelected))}>{allVisibleSelected ? "Снять всё" : "Выбрать всё"}</button>}</header>
    <div className="rs60-product-filters">
      <label><span>Тип товара</span><select value={filter} onChange={(event) => onFilter(event.target.value)}><option value="all">Все</option>{subcategories.map(([id, title]) => <option key={id} value={id}>{title}</option>)}</select></label>
      <label><span>Коллекция</span><select value={collectionFilter} onChange={(event) => onCollectionFilter(event.target.value)}><option value="all">Все коллекции</option>{collections.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
    </div>
    <div className="product-grid rs57-product-grid">{visible.map((item) => <ReadyCatalogCard key={item.option.id} option={item.option} selected={Boolean(selected[item.option.id])} color={colors[item.option.id] || ""} size={sizes[item.option.id] || ""} quantity={qty[item.option.id] || recommendedOptionQuantity(item.option, guests)} guests={guests} replacing={Boolean(replacingId)} replacingSelf={replacingId === item.option.id} onToggle={() => onSelected(item.option.id, !selected[item.option.id])} onColor={(value) => onColor(item.option.id, value)} onSize={(value) => onSize(item.option.id, value)} onQty={(value) => onQty(item.option.id, value)}/>)}</div>
  </section>;
}'''
if old_product_group not in text:
    raise RuntimeError("ProductGroup anchor not found")
text = text.replace(old_product_group, new_product_group, 1)

# 3) Result: moodboard is the result. No duplicate list or summary card.
start = text.index('      {step === 3 && <div className="rs57-stage rs57-result-stage">')
end = text.index('\n    </main>', start)
result_block = '''      {step === 3 && <div className="rs57-stage rs57-result-stage rs60-result-stage">
        <section className="rs60-result-main"><header className="rs57-stage-head rs60-result-head"><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2><p>Ваше решение собрано в одном визуальном поле. Меняйте количество, заменяйте, удаляйте или добавляйте предметы прямо здесь.</p></header>
          {selectedRows.length ? <section className="rs60-moodboard" aria-label="Выбранные товары">
            <div className="rs60-moodboard-grid">
              {selectedRows.map(({ row, quantity, option, group }, index) => <article className={`rs60-moodboard-card rs60-mood-${index % 7}`} key={`mood-${option.id}-${row.offer_id}`}>
                <div className="rs60-moodboard-media"><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div>
                <div className="rs60-moodboard-copy"><small>{group.title}</small><strong>{option.title}</strong><span>{money(priceOf(row))}</span></div>
                <div className="rs60-moodboard-controls"><div className="rs60-qty"><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))} aria-label="Увеличить количество">+</button></div><div className="rs60-card-actions"><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></div>
              </article>)}
              <button type="button" className="rs60-add-card" onClick={goComposition}><span>+</span><strong>Добавить предмет</strong><small>из доступных категорий и коллекций</small></button>
            </div>
            <footer className="rs60-result-total"><div><span>{selectedRows.length} позиций</span><strong>{money(total)}</strong></div><button type="button" className="rs57-primary" onClick={addToCart}>ДОБАВИТЬ ВСЁ В КОРЗИНУ</button></footer>
          </section> : <div className="rs57-empty-result"><h3>В решении пока нет товаров</h3><button type="button" onClick={goComposition}>Добавить предмет</button></div>}
        </section>
      </div>}'''
text = text[:start] + result_block + text[end:]

path.write_text(text, encoding="utf-8")
print("Ready Solutions simplified V60 applied")
