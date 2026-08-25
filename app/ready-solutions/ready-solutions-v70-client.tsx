"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "../constructor/data-client";
import { findTableSolution } from "../constructor/table-solutions";
import { resolveTableSolutionCatalogRows } from "../constructor/table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedOptionQuantity,
  type SolutionCategory,
  type SolutionProductOption,
} from "../constructor/table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "../constructor/types";

const CART_KEY = "kultura-cart";
const CART_OFFSET = 998000;
const browserBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const priceOf = (row?: CatalogRow) => Number(String(row?.price || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const norm = (value: string) => String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/[«»"']/g, "").replace(/\s+/g, " ");
const rowImages = (row?: CatalogRow) => Array.from(new Set([row?.primary_image_url, ...(row?.all_image_urls || "").split("|")].filter((value): value is string => Boolean(value))));
const rowId = (row: CatalogRow) => {
  const numeric = Number(String(row.offer_id || row.group_id || "").replace(/\D/g, ""));
  if (Number.isFinite(numeric) && numeric > 0) return CART_OFFSET + numeric;
  return CART_OFFSET + Array.from(row.product_name).reduce((sum, char) => sum + char.charCodeAt(0), 0);
};

const COLOR_HEX: Record<string, string> = {
  "белый": "#f6f5f1", "молочный": "#ece6da", "бежевый": "#d6c4aa", "песочный": "#c8aa84", "коричневый": "#7b523b",
  "черный": "#1d1d1b", "чёрный": "#1d1d1b", "синий": "#38506a", "темно-синий": "#12263e", "ночной синий": "#10233e",
  "голубой": "#9eb8ca", "зеленый": "#6f806b", "зелёный": "#6f806b", "красный": "#8e3d35", "бордовый": "#6d2f31",
  "розовый": "#d3aaa5", "желтый": "#cfb168", "жёлтый": "#cfb168", "золотой": "#b59862", "серый": "#969696",
};
const swatchColor = (value: string) => COLOR_HEX[norm(value)] || "#d8d5cf";

const COLLECTION_LABELS: Record<string, string> = { "Мокоши": "Символы", "Камея": "Эхо", "Жар-птица": "Феникс" };
const displayCollectionName = (value: string) => COLLECTION_LABELS[value] || value;

function useData() {
  const [catalog, setCatalog] = useState<FinalConstructorData | null>(null);
  const [rules, setRules] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let alive = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([nextCatalog, nextRules]) => { if (alive) { setCatalog(nextCatalog); setRules(nextRules); } })
      .catch((reason: unknown) => { if (alive) setError(reason instanceof Error ? reason.message : "Не удалось загрузить данные"); });
    return () => { alive = false; };
  }, []);
  return { catalog, rules, error };
}

function Header() {
  return <>
    <div className="rs70-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</div>
    <header className="rs70-header"><Link href="/" className="rs70-menu" aria-label="Главная">☰</Link><Link href="/" className="rs70-logo">КУЛЬТУРА ДОМА</Link><nav><Link href="/?open=search">Поиск</Link><Link href="/?open=account">Профиль</Link><Link href="/?open=cart">Корзина</Link></nav></header>
  </>;
}

function Footer() {
  return <footer className="rs70-footer"><strong>КУЛЬТУРА ДОМА</strong><span>Предметы и готовые решения для цельного пространства.</span></footer>;
}

type GroupId = "tableware" | "tableTextile" | "bedding" | "decor" | "atmosphere" | "bath";
type GroupItem = { option: SolutionProductOption; subcategoryId: string; subcategoryTitle: string };
type FormGroup = { id: GroupId; title: string; description: string; items: GroupItem[] };

const GROUP_META: Record<GroupId, { title: string; description: string; categories: string[] }> = {
  tableware: { title: "Посуда и сервировка", description: "Тарелки, чайные пары, блюда, стекло, приборы и предметы подачи.", categories: ["plates", "bowls", "cupsPairs", "greenSalonTeaService", "redLinesServing", "redLinesTeaService", "sugarBowls", "milkJugs", "teapots", "serving", "drinkware", "cutlery"] },
  tableTextile: { title: "Столовый текстиль", description: "Скатерти, дорожки, плейсматы, салфетки и текстильные аксессуары.", categories: ["tableTextile"] },
  bedding: { title: "Постельное бельё", description: "Комплекты и базовый текстиль для спальни.", categories: ["bedding"] },
  decor: { title: "Декор для дома", description: "Пледы, покрывала, декоративные подушки, вазы, хранение и акцентные предметы.", categories: ["throwsCoverlets", "decorativePillows", "vases", "baskets", "games", "storage", "other"] },
  atmosphere: { title: "Свечи и диффузоры", description: "Свечи, ароматы и атмосферные детали для финального слоя композиции.", categories: ["atmosphere"] },
  bath: { title: "Для ванной", description: "Полотенца, халаты и предметы для ванной комнаты.", categories: ["bath"] },
};
const GROUP_ORDER: GroupId[] = ["tableware", "tableTextile", "bedding", "decor", "atmosphere", "bath"];

function buildGroups(categories: SolutionCategory[]): FormGroup[] {
  return GROUP_ORDER.map((id) => {
    const meta = GROUP_META[id];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
    return { id, title: meta.title, description: meta.description, items };
  }).filter((group) => group.items.length > 0);
}

function cartItemFromRow(row: CatalogRow, quantity = 1) {
  const images = rowImages(row);
  const price = priceOf(row);
  const color = row.color || "Без цвета";
  const size = row.size || row.volume || "Единый размер";
  const id = rowId(row);
  return {
    id, name: row.product_name, note: [row.collection, row.material].filter(Boolean).join(" · "), price,
    image: images[0] || "/images/image-placeholder.svg", gallery: images.slice(1), selectedColor: color, selectedSize: size,
    selectedSkuId: `ready70-${row.offer_id || id}`, quantity,
    skus: [{ id: `ready70-${row.offer_id || id}`, article: row.vendor_code || String(row.offer_id), productId: id, color, colorHex: swatchColor(color), size, material: row.material || "", composition: row.material || "", price, image: images[0] || "/images/image-placeholder.svg", gallery: images.slice(1) }],
  };
}

function addRowsToSharedCart(rows: Array<{ row: CatalogRow; quantity: number }>) {
  let current: any[] = [];
  try { current = JSON.parse(localStorage.getItem(CART_KEY) || "[]"); } catch {}
  const next = [...current];
  rows.forEach(({ row, quantity }) => {
    const item = cartItemFromRow(row, quantity);
    const index = next.findIndex((existing) => existing.id === item.id && existing.selectedColor === item.selectedColor && existing.selectedSize === item.selectedSize);
    if (index >= 0) next[index] = { ...next[index], quantity: (next[index].quantity || 1) + quantity };
    else next.push(item);
  });
  try { localStorage.setItem(CART_KEY, JSON.stringify(next)); } catch {}
}

type SelectedRow = { row: CatalogRow; quantity: number; option: SolutionProductOption; group: FormGroup };

type ProductGroupProps = {
  group: FormGroup; selected: Record<string, boolean>; colors: Record<string, string>; sizes: Record<string, string>; qty: Record<string, number>; guests: number;
  filter: string; collectionFilter: string; onFilter: (value: string) => void; onCollectionFilter: (value: string) => void;
  onSelected: (id: string, value: boolean) => void; onColor: (id: string, value: string) => void; onSize: (id: string, value: string) => void; onQty: (id: string, value: number) => void;
};

function ProductGroup({ group, selected, colors, sizes, qty, guests, filter, collectionFilter, onFilter, onCollectionFilter, onSelected, onColor, onSize, onQty }: ProductGroupProps) {
  const subs = Array.from(new Map(group.items.map((item) => [item.subcategoryId, item.subcategoryTitle])).entries());
  const cols = Array.from(new Set(group.items.map((item) => item.option.collection).filter(Boolean))).sort((a, b) => displayCollectionName(a).localeCompare(displayCollectionName(b), "ru"));
  const visible = group.items.filter((item) => (filter === "all" || item.subcategoryId === filter) && (collectionFilter === "all" || norm(item.option.collection) === norm(collectionFilter)));
  const allSelected = visible.length > 0 && visible.every(({ option }) => selected[option.id]);
  const selectedCount = group.items.filter(({ option }) => selected[option.id]).length;

  return <section className="rs70-category" id={`rs70-${group.id}`}>
    <header className="rs70-category-head"><div><small>КАТЕГОРИЯ</small><h2>{group.title}</h2><p>{group.description}</p></div><div className="rs70-category-count"><strong>{selectedCount}</strong><span>выбрано</span></div></header>
    <div className="rs70-toolbar">
      {subs.length > 1 && <div className="rs70-filter"><span>Тип</span><nav><button className={filter === "all" ? "is-active" : ""} onClick={() => onFilter("all")}>Все</button>{subs.map(([id, title]) => <button key={id} className={filter === id ? "is-active" : ""} onClick={() => onFilter(id)}>{title}</button>)}</nav></div>}
      {cols.length > 1 && <div className="rs70-filter"><span>Коллекция</span><nav><button className={collectionFilter === "all" ? "is-active" : ""} onClick={() => onCollectionFilter("all")}>Все</button>{cols.map((value) => <button key={value} className={norm(collectionFilter) === norm(value) ? "is-active" : ""} onClick={() => onCollectionFilter(value)}>{displayCollectionName(value)}</button>)}</nav></div>}
      <label className="rs70-select-all"><input type="checkbox" checked={allSelected} onChange={() => visible.forEach(({ option }) => onSelected(option.id, !allSelected))}/><i/><span>{allSelected ? "Снять выбор" : "Выбрать все в категории"}</span></label>
    </div>
    <div className="rs70-product-grid">{visible.map(({ option }) => <ProductCard key={option.id} option={option} selected={Boolean(selected[option.id])} color={colors[option.id] || ""} size={sizes[option.id] || ""} quantity={qty[option.id] || recommendedOptionQuantity(option, guests)} guests={guests} onToggle={() => onSelected(option.id, !selected[option.id])} onColor={(value) => onColor(option.id, value)} onSize={(value) => onSize(option.id, value)} onQty={(value) => onQty(option.id, value)}/>)}</div>
  </section>;
}

function ProductCard({ option, selected, color, size, quantity, guests, onToggle, onColor, onSize, onQty }: { option: SolutionProductOption; selected: boolean; color: string; size: string; quantity: number; guests: number; onToggle: () => void; onColor: (value: string) => void; onSize: (value: string) => void; onQty: (value: number) => void }) {
  const colors = optionColors(option);
  const sizes = optionSizes(option, color);
  const row = pickOptionVariant(option, color, size);
  const image = rowImages(row)[0] || "/images/image-placeholder.svg";
  const collection = displayCollectionName(option.collection || row?.collection || "");
  return <article className={`rs70-product-card ${selected ? "is-selected" : ""}`}>
    <div className="rs70-card-media"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/><label className="rs70-card-check"><input type="checkbox" checked={selected} onChange={onToggle}/><i>✓</i></label></div>
    <div className="rs70-card-copy"><div><h3>{option.title}</h3><p>{[collection, row?.material].filter(Boolean).join(" · ")}</p></div><strong>{money(priceOf(row))}</strong></div>
    {colors.length > 1 && <div className="rs70-swatches" aria-label="Цвет"><span>Цвет</span><nav>{colors.map((value) => <button type="button" key={value} className={(color || row?.color) === value ? "is-active" : ""} style={{ background: swatchColor(value) }} onClick={() => onColor(value)} title={value}/>)}</nav></div>}
    {selected && <div className="rs70-card-options">
      {sizes.length > 1 && <div className="rs70-size"><span>Размер</span><nav>{sizes.map((value) => <button type="button" key={value} className={size === value ? "is-active" : ""} onClick={() => onSize(value)}>{value}</button>)}</nav></div>}
      <div className="rs70-qty"><span>Количество<small>{option.perPerson ? `для ${guests} персон` : "на решение"}</small></span><nav><button type="button" onClick={() => onQty(Math.max(1, quantity - 1))}>−</button><b>{quantity}</b><button type="button" onClick={() => onQty(quantity + 1)}>+</button></nav></div>
    </div>}
  </article>;
}

export function ReadySolutionWizard({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const { catalog, rules, error } = useData();
  const [guests, setGuests] = useState(2);
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [collectionFilters, setCollectionFilters] = useState<Record<string, string>>({});
  const [review, setReview] = useState(false);

  const rows = useMemo(() => solution && catalog ? resolveTableSolutionCatalogRows(catalog.catalog, solution) : [], [catalog, solution]);
  const legacyCategories = useMemo(() => solution ? buildSolutionCategories(rows, solution.space) : [], [rows, solution]);
  const groups = useMemo(() => buildGroups(legacyCategories), [legacyCategories]);
  const options = useMemo(() => groups.flatMap((group) => group.items.map((item) => item.option)), [groups]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, rules) : [2, 4, 6], [solution, rules]);

  useEffect(() => {
    if (!solution || !options.length) return;
    setGuests((current) => guestOptions.includes(current) ? current : (guestOptions[0] || 2));
    const defaultNames = new Set((solution.defaultProductNames || []).map(norm));
    setSelected((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, defaultNames.has(norm(option.title))])));
    setColors((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, solution.defaultColors?.[option.title] || optionColors(option)[0] || ""])));
    setSizes((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => { const c = solution.defaultColors?.[option.title] || optionColors(option)[0] || ""; return [option.id, solution.defaultSizes?.[option.title] || optionSizes(option, c)[0] || ""]; })));
    setQty((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, solution.defaultQuantities?.[option.title] || recommendedOptionQuantity(option, guestOptions[0] || 2)])));
  }, [solution, options, guestOptions]);

  useEffect(() => {
    if (!options.length) return;
    setQty((current) => { const next = { ...current }; options.forEach((option) => { if (option.perPerson) next[option.id] = recommendedOptionQuantity(option, guests); }); return next; });
  }, [guests, options]);

  const selectedRows = useMemo<SelectedRow[]>(() => groups.flatMap((group) => group.items.flatMap(({ option }) => {
    if (!selected[option.id]) return [];
    const row = pickOptionVariant(option, colors[option.id] || "", sizes[option.id] || "");
    return row ? [{ row, quantity: Math.max(1, qty[option.id] || recommendedOptionQuantity(option, guests)), option, group }] : [];
  })), [groups, selected, colors, sizes, qty, guests]);
  const total = selectedRows.reduce((sum, item) => sum + priceOf(item.row) * item.quantity, 0);

  if (!solution) return <div className="rs70-page"><Header/><main className="rs70-state">Решение не найдено.</main></div>;
  if (error) return <div className="rs70-page"><Header/><main className="rs70-state">{error}</main></div>;
  if (!catalog || !groups.length) return <div className="rs70-page"><Header/><main className="rs70-state">Собираем решение…</main></div>;

  const addToCart = () => {
    if (!selectedRows.length) return;
    addRowsToSharedCart(selectedRows.map(({ row, quantity }) => ({ row, quantity })));
    window.location.href = `${browserBasePath}/?open=cart`;
  };

  return <div className="rs70-page">
    <Header/>
    <main className="rs70-shell">
      <nav className="rs70-crumbs"><Link href="/">Главная</Link><span>/</span><Link href="/ready-solutions/">Готовые решения</Link><span>/</span><b>{solution.name}</b></nav>
      <section className="rs70-hero"><div className="rs70-hero-media"><RemoteImage src={solution.heroImage || rows[0]?.primary_image_url || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div><div className="rs70-hero-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Возьмите готовую композицию за основу и настройте её под свой дом. Количество персон автоматически меняет персональные предметы.</p><div>{solution.collections.map((value) => <span key={value}>{displayCollectionName(value)}</span>)}</div></div></section>

      {!review ? <>
        <section className="rs70-persons"><div><small>ШАГ 01</small><h2>Сколько персон?</h2><p>Выберите один раз — тарелки, чашки, салфетки и другие персональные предметы пересчитаются автоматически.</p></div><nav>{guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "is-active" : ""} onClick={() => setGuests(value)}><strong>{value}</strong><span>{value === 1 ? "персона" : value <= 4 ? "персоны" : "персон"}</span></button>)}</nav></section>

        <section className="rs70-category-index"><div><small>ШАГ 02</small><h2>Соберите решение по категориям</h2><p>Категории идут сверху вниз как чек-лист. Можно выбрать всё или только нужные позиции.</p></div><nav>{groups.map((group) => <a key={group.id} href={`#rs70-${group.id}`}><span>{group.title}</span><b>{group.items.filter(({ option }) => selected[option.id]).length}</b></a>)}</nav></section>

        <div className="rs70-categories">{groups.map((group) => <ProductGroup key={group.id} group={group} selected={selected} colors={colors} sizes={sizes} qty={qty} guests={guests} filter={filters[group.id] || "all"} collectionFilter={collectionFilters[group.id] || "all"} onFilter={(value) => setFilters((current) => ({ ...current, [group.id]: value }))} onCollectionFilter={(value) => setCollectionFilters((current) => ({ ...current, [group.id]: value }))} onSelected={(id, value) => setSelected((current) => ({ ...current, [id]: value }))} onColor={(id, value) => { setColors((current) => ({ ...current, [id]: value })); const option = group.items.find((item) => item.option.id === id)?.option; if (option) setSizes((current) => ({ ...current, [id]: optionSizes(option, value)[0] || "" })); }} onSize={(id, value) => setSizes((current) => ({ ...current, [id]: value }))} onQty={(id, value) => setQty((current) => ({ ...current, [id]: Math.max(1, value) }))}/>)}</div>

        <section className="rs70-configure"><div><span>Выбрано {selectedRows.length} позиций для {guests} персон</span><strong>{money(total)}</strong></div><button type="button" onClick={() => setReview(true)} disabled={!selectedRows.length}>НАСТРОИТЬ РЕШЕНИЕ</button></section>
      </> : <section className="rs70-review"><header><div><small>ГОТОВО К ПОКУПКЕ</small><h2>Ваше решение</h2><p>{guests} персон · {selectedRows.length} позиций</p></div><button type="button" onClick={() => setReview(false)}>← Вернуться к настройке</button></header><div className="rs70-review-grid">{selectedRows.map(({ row, quantity, option }) => <article key={`${option.id}-${row.offer_id}`}><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/><div><h3>{option.title}</h3><p>{[displayCollectionName(row.collection || option.collection || ""), row.color, row.size || row.volume].filter(Boolean).join(" · ")}</p><span>{quantity} × {money(priceOf(row))}</span></div></article>)}</div><footer><div><span>Итого</span><strong>{money(total)}</strong></div><button type="button" onClick={addToCart}>ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ</button></footer></section>}
    </main>
    {!review && <div className="rs70-mobile-dock"><span><small>{selectedRows.length} позиций</small><strong>{money(total)}</strong></span><button type="button" onClick={() => setReview(true)} disabled={!selectedRows.length}>НАСТРОИТЬ</button></div>}
    <Footer/>
  </div>;
}
