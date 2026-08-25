"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "../constructor/data-client";
import { TABLE_SOLUTIONS, findTableSolution, type TableSolution } from "../constructor/table-solutions";
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

const browserBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const CART_KEY = "kultura-cart";
const SAVED_KEY = "kultura-ready-solution-v57";
const CART_OFFSET = 997000;

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
  "белый": "#f6f5f1", "молочный": "#ece6da", "бежевый": "#d6c4aa", "песочный": "#c8aa84",
  "коричневый": "#7b523b", "черный": "#1d1d1b", "чёрный": "#1d1d1b", "синий": "#38506a",
  "темно-синий": "#12263e", "ночной синий": "#10233e", "голубой": "#9eb8ca", "зеленый": "#6f806b",
  "зелёный": "#6f806b", "красный": "#8e3d35", "бордовый": "#6d2f31", "розовый": "#d3aaa5",
  "желтый": "#cfb168", "жёлтый": "#cfb168", "золотой": "#b59862", "серый": "#969696",
};
const swatchColor = (value: string) => COLOR_HEX[norm(value)] || "#d8d5cf";

function Icon({ name, filled = false }: { name: "search" | "user" | "bag" | "pin" | "arrow" | "check" | "heart" | "close"; filled?: boolean }) {
  const common = { fill: filled ? "currentColor" : "none", stroke: "currentColor", strokeWidth: 1.7, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "search") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if (name === "user") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if (name === "bag") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if (name === "pin") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if (name === "heart") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if (name === "close") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if (name === "check") return <svg viewBox="0 0 20 20" aria-hidden="true" {...common}><path d="m4.5 10 3.2 3.2 7.8-8"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
}

function StoreHeader() {
  return <>
    <div className="promo rs57-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href="/">ПОДРОБНЕЕ</Link></div>
    <header className="header rs57-header">
      <div className="header-left"><Link className="icon-btn hamburger" href="/?open=menu" aria-label="Открыть меню"><i/><i/><i/></Link><Link className="boutiques" href="/?open=boutiques"><Icon name="pin"/> Бутики</Link></div>
      <Link className="logo" href="/">КУЛЬТУРА ДОМА</Link>
      <div className="header-actions"><Link href="/?open=search" aria-label="Поиск"><Icon name="search"/></Link><Link href="/?open=account" aria-label="Профиль"><Icon name="user"/></Link><Link href="/?open=favorites" aria-label="Избранное"><Icon name="heart"/></Link><Link className="bag" href="/?open=cart" aria-label="Корзина"><Icon name="bag"/></Link></div>
    </header>
  </>;
}

function StoreFooter() {
  return <footer className="rs57-footer"><div><strong>КУЛЬТУРА ДОМА</strong><p>Коллекции, предметы и готовые решения для цельного пространства.</p></div><nav><Link href="/">Каталог</Link><Link href="/?section=collections">Коллекции</Link><Link href="/ready-solutions/">Готовые решения</Link><Link href="/?open=boutiques">Бутики</Link></nav></footer>;
}

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

function solutionImage(solution: TableSolution, rows: CatalogRow[]) {
  return solution.heroImage || (solution.previewFile ? `/images/constructor/${solution.previewFile}` : rows[0]?.primary_image_url) || "/images/image-placeholder.svg";
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
    selectedSkuId: `ready-${row.offer_id || id}`, quantity,
    skus: [{ id: `ready-${row.offer_id || id}`, article: row.vendor_code || String(row.offer_id), productId: id, color, colorHex: swatchColor(color), size, material: row.material || "", composition: row.material || "", price, image: images[0] || "/images/image-placeholder.svg", gallery: images.slice(1) }],
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

type GroupId = "tableware" | "tableTextile" | "bedding" | "throws" | "pillows" | "decor" | "atmosphere" | "bath";
type GroupItem = { option: SolutionProductOption; subcategoryId: string; subcategoryTitle: string };
type FormGroup = { id: GroupId; title: string; description: string; items: GroupItem[] };

const GROUP_META: Record<GroupId, { title: string; description: string; categories: string[] }> = {
  tableware: { title: "Посуда и сервировка", description: "Тарелки, пары, блюда, стекло и предметы подачи.", categories: ["plates", "bowls", "cupsPairs", "greenSalonTeaService", "redLinesServing", "redLinesTeaService", "sugarBowls", "milkJugs", "teapots", "serving", "drinkware", "cutlery"] },
  tableTextile: { title: "Столовый текстиль", description: "Скатерти, дорожки, плейсматы, салфетки и аксессуары.", categories: ["tableTextile"] },
  bedding: { title: "Постельное бельё", description: "Комплекты и базовый текстиль для спальни.", categories: ["bedding"] },
  throws: { title: "Пледы и покрывала", description: "Фактурные слои и покрывала для композиции.", categories: ["throwsCoverlets"] },
  pillows: { title: "Декоративные подушки", description: "Подушки, цветовые и фактурные акценты.", categories: ["decorativePillows"] },
  decor: { title: "Декор для дома", description: "Вазы, хранение, игры и функциональные предметы.", categories: ["vases", "baskets", "games", "storage", "other"] },
  atmosphere: { title: "Свечи и диффузоры", description: "Ароматы и свечи для финального атмосферного слоя.", categories: ["atmosphere"] },
  bath: { title: "Для ванной", description: "Полотенца, халаты и аксессуары для ванной.", categories: ["bath"] },
};
const GROUP_ORDER: GroupId[] = ["tableware", "tableTextile", "bedding", "throws", "pillows", "decor", "atmosphere", "bath"];

function buildGroups(categories: SolutionCategory[]): FormGroup[] {
  return GROUP_ORDER.map((id) => {
    const meta = GROUP_META[id];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
    return { id, title: meta.title, description: meta.description, items };
  }).filter((group) => group.items.length > 0);
}

const collectionHref = (collection: string) => `/?section=collections&collection=${encodeURIComponent(collection)}`;

// READY_SOLUTIONS_CATALOG_MOODBOARD_V61
const COLLECTION_LABELS: Record<string, string> = {
  "Мокоши": "Символы",
  "Камея": "Эхо",
  "Жар-птица": "Феникс",
};
const COLLECTION_SOURCES: Record<string, string> = Object.fromEntries(Object.entries(COLLECTION_LABELS).map(([source, label]) => [label, source]));
const displayCollectionName = (value: string) => COLLECTION_LABELS[value] || value;
const sourceCollectionName = (value: string) => COLLECTION_SOURCES[value] || value;
const belongsToCollection = (row: CatalogRow, collection: string) => {
  const target = norm(sourceCollectionName(collection));
  if (!target) return false;
  return norm(row.collection || "") === target || norm(row.product_name || "").includes(target);
};

// READY_SOLUTIONS_PREMIUM_FILTERS_V62
export function ReadySolutionsLanding() {
  const { catalog, rules, error } = useData();
  // READY_SOLUTIONS_SIMPLIFIED_V60
  const [space, setSpace] = useState("all");
  // COLLECTION_CONTEXT_V58
  const [collectionContext, setCollectionContext] = useState("");
  useEffect(() => {
    const requested = new URLSearchParams(window.location.search).get("collection") || "";
    setCollectionContext(requested);
  }, []);
  if (error) return <div className="rs57-page"><StoreHeader/><main className="rs57-state">{error}</main></div>;
  if (!catalog) return <div className="rs57-page"><StoreHeader/><main className="rs57-state">Загружаем готовые решения…</main></div>;

  const cards = TABLE_SOLUTIONS.map((solution) => {
    const rows = resolveTableSolutionCatalogRows(catalog.catalog, solution);
    const groups = buildGroups(buildSolutionCategories(rows, solution.space));
    const guestOptions = deriveGuestOptions(solution, rules);
    const prices = rows.map(priceOf).filter(Boolean);
    return { solution, rows, groups, guestOptions, image: solutionImage(solution, rows), from: prices.length ? Math.min(...prices) : 0 };
  });
  const spaces = Array.from(new Set(cards.map((card) => card.solution.space)));
  const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(displayCollectionName(value)) === norm(collectionContext) || norm(sourceCollectionName(value)) === norm(sourceCollectionName(collectionContext)))) && (space === "all" || card.solution.space === space)); // READY_SOLUTIONS_COLLECTION_LABELS_V61
  const reset = () => { setSpace("all"); };

  return <div className="rs57-page">
    <StoreHeader/>
    <main className="rs57-landing">
      <section className="rs57-intro rs60-intro">
        <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Соберите пространство целиком</h1><p>Выберите пространство. Внутри можно настроить количество, состав, цвет и заменить любой предмет.</p></div>
      </section>

      <section className="rs57-index" aria-labelledby="rs57-index-title">
        <header className="rs57-index-head"><div><small>ПОДБОР</small><h2 id="rs57-index-title">Найдите своё решение</h2></div><span>{visible.length} из {cards.length}</span></header>
        <div className="rs62-space-filter" aria-label="Фильтр по пространству"><span>Пространство</span><nav className="rs62-filter-rail"><button type="button" className={space === "all" ? "is-active" : ""} onClick={() => setSpace("all")}>Все</button>{spaces.map((value) => <button type="button" key={value} className={space === value ? "is-active" : ""} onClick={() => setSpace(value)}>{value}</button>)}</nav></div>

        {collectionContext && <div className="rs57-context-filter"><span>Коллекция</span><b>{displayCollectionName(collectionContext)}</b><button type="button" onClick={() => setCollectionContext("")}>Снять фильтр</button></div>}
        {visible.length ? <div className="rs57-solution-grid">{visible.map(({ solution, rows, groups, guestOptions, image, from }) => <article className="rs57-solution-card" key={solution.id}>
          <Link className="rs57-solution-media" href={`/ready-solutions/${solution.id}/`}><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></Link>
          <div className="rs57-solution-copy"><small>{solution.space}</small><Link href={`/ready-solutions/${solution.id}/`}><h3>{solution.name}</h3></Link><p>{solution.collections.map(displayCollectionName).join(" · ")}</p><div><span>{groups.length} категорий · {rows.length} вариантов</span><strong>{from ? `от ${money(from)}` : "Настроить состав"}</strong></div><div className="rs57-person-badges">{guestOptions.map((value) => <span key={value}>{value} {value === 1 ? "персона" : value <= 4 ? "персоны" : "персон"}</span>)}</div><Link className="rs57-card-cta" href={`/ready-solutions/${solution.id}/`}>НАСТРОИТЬ РЕШЕНИЕ <Icon name="arrow"/></Link></div>
        </article>)}</div> : <div className="rs57-empty-filter"><h3>Нет решений с такими параметрами</h3><p>Сбросьте один из фильтров — остальные параметры сохранятся.</p><button type="button" onClick={reset}>Показать все решения</button></div>}
      </section>
    </main>
    <StoreFooter/>
  </div>;
}

type WizardStep = 1 | 2 | 3;

type SelectedRow = { row: CatalogRow; quantity: number; option: SolutionProductOption; group: FormGroup };

export function ReadySolutionWizard({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const { catalog, rules, error } = useData();
  const [step, setStep] = useState<WizardStep>(1);
  const [guests, setGuests] = useState(2);
  const [activeGroup, setActiveGroup] = useState<string>("");
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [collectionFilters, setCollectionFilters] = useState<Record<string, string>>({});
  const [activeCollections, setActiveCollections] = useState<string[]>(() => solution ? [...solution.collections] : []);
  const [saved, setSaved] = useState(false);
  const [replaceOptionId, setReplaceOptionId] = useState<string | null>(null);
  const [replaceGroupId, setReplaceGroupId] = useState<string | null>(null);

  const availableCollections = useMemo(() => {
    if (!solution || !catalog) return solution ? [...solution.collections] : [];
    const pool = [...TABLE_SOLUTIONS.flatMap((item) => item.collections), ...catalog.catalog.map((row) => row.collection).filter(Boolean)];
    const byLabel = new Map<string, string>();
    pool.forEach((value) => {
      const source = String(value || "").trim();
      if (!source) return;
      const label = displayCollectionName(source);
      const key = norm(label);
      if (!byLabel.has(key)) byLabel.set(key, source);
    });
    solution.collections.forEach((source) => byLabel.set(norm(displayCollectionName(source)), source));
    return Array.from(byLabel.values()).sort((a, b) => displayCollectionName(a).localeCompare(displayCollectionName(b), "ru"));
  }, [catalog, solution]);

  const rows = useMemo(() => {
    if (!solution || !catalog) return [];
    const baseRows = resolveTableSolutionCatalogRows(catalog.catalog, solution);
    const baseCollections = solution.collections;
    const isEnabled = (value: string) => activeCollections.some((activeCollection) => norm(sourceCollectionName(activeCollection)) === norm(sourceCollectionName(value)));
    const keptBase = baseRows.filter((row) => {
      const matched = baseCollections.filter((collection) => belongsToCollection(row, collection));
      return matched.length === 0 || matched.some(isEnabled);
    });
    const extras = activeCollections.filter((collection) => !baseCollections.some((baseCollection) => norm(sourceCollectionName(baseCollection)) === norm(sourceCollectionName(collection))));
    const extraRows = catalog.catalog.filter((row) => extras.some((collection) => belongsToCollection(row, collection)));
    const merged = new Map<string, CatalogRow>();
    [...keptBase, ...extraRows].forEach((row) => {
      const key = String(row.offer_id || row.vendor_code || `${norm(row.product_name)}|${norm(row.color)}|${norm(row.size || row.volume)}`);
      if (!merged.has(key)) merged.set(key, row);
    });
    return Array.from(merged.values());
  }, [catalog, solution, activeCollections]);
  const legacyCategories = useMemo(() => solution ? buildSolutionCategories(rows, solution.space) : [], [rows, solution]);
  const groups = useMemo(() => buildGroups(legacyCategories), [legacyCategories]);
  const options = useMemo(() => groups.flatMap((group) => group.items.map((item) => item.option)), [groups]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, rules) : [2, 4, 6], [solution, rules]);

  useEffect(() => {
    if (!solution || !groups.length || !options.length) return;
    setGuests((current) => guestOptions.includes(current) ? current : (guestOptions[0] || 2));
    setActiveGroup((current) => current || groups[0]?.id || "");
    const defaultNames = new Set((solution.defaultProductNames || []).map(norm));
    setSelected((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, defaultNames.has(norm(option.title))])));
    setColors((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, solution.defaultColors?.[option.title] || optionColors(option)[0] || ""])));
    setSizes((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => { const color = solution.defaultColors?.[option.title] || optionColors(option)[0] || ""; return [option.id, solution.defaultSizes?.[option.title] || optionSizes(option, color)[0] || ""]; })));
    setQty((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, solution.defaultQuantities?.[option.title] || recommendedOptionQuantity(option, guestOptions[0] || 2)])));
  }, [solution, groups, options, guestOptions]);

  useEffect(() => {
    if (!options.length) return;
    setQty((current) => {
      const next = { ...current };
      options.forEach((option) => { if (option.perPerson) next[option.id] = recommendedOptionQuantity(option, guests); });
      return next;
    });
  }, [guests, options]);

  useEffect(() => {
    if (!options.length) return;
    setSelected((current) => { const next = { ...current }; options.forEach((option) => { if (!(option.id in next)) next[option.id] = false; }); return next; });
    setColors((current) => { const next = { ...current }; options.forEach((option) => { if (!(option.id in next)) next[option.id] = optionColors(option)[0] || ""; }); return next; });
    setSizes((current) => { const next = { ...current }; options.forEach((option) => { if (!(option.id in next)) { const color = optionColors(option)[0] || ""; next[option.id] = optionSizes(option, color)[0] || ""; } }); return next; });
    setQty((current) => { const next = { ...current }; options.forEach((option) => { if (!(option.id in next)) next[option.id] = recommendedOptionQuantity(option, guests); }); return next; });
  }, [options, guests]);

  const selectedRows = useMemo<SelectedRow[]>(() => groups.flatMap((group) => group.items.flatMap(({ option }) => {
    if (!selected[option.id]) return [];
    const row = pickOptionVariant(option, colors[option.id] || "", sizes[option.id] || "");
    return row ? [{ row, quantity: Math.max(1, qty[option.id] || recommendedOptionQuantity(option, guests)), option, group }] : [];
  })), [groups, selected, colors, sizes, qty, guests]);
  const total = selectedRows.reduce((sum, item) => sum + priceOf(item.row) * item.quantity, 0);
  const active = groups.find((group) => group.id === activeGroup) || groups[0];

  if (!solution) return <div className="rs57-page"><StoreHeader/><main className="rs57-state">Решение не найдено.</main></div>;
  if (error) return <div className="rs57-page"><StoreHeader/><main className="rs57-state">{error}</main></div>;
  if (!catalog || !groups.length) return <div className="rs57-page"><StoreHeader/><main className="rs57-state">Собираем решение…</main></div>;

  const saveSolution = () => {
    try { localStorage.setItem(SAVED_KEY, JSON.stringify({ scenarioId, guests, selected, colors, sizes, qty, total, savedAt: new Date().toISOString() })); setSaved(true); setTimeout(() => setSaved(false), 2200); } catch {}
  };
  const addToCart = () => {
    if (!selectedRows.length) return;
    addRowsToSharedCart(selectedRows.map(({ row, quantity }) => ({ row, quantity })));
    window.location.href = `${browserBasePath}/?open=cart`;
  };
  const handleSelect = (id: string, value: boolean) => {
    if (replaceOptionId && id !== replaceOptionId) {
      const oldQuantity = qty[replaceOptionId] || 1;
      setSelected((current) => ({ ...current, [replaceOptionId]: false, [id]: true }));
      setQty((current) => ({ ...current, [id]: oldQuantity }));
      setReplaceOptionId(null); setReplaceGroupId(null); setStep(3);
      return;
    }
    setSelected((current) => ({ ...current, [id]: value }));
  };
  const startReplace = (option: SolutionProductOption, group: FormGroup) => { setReplaceOptionId(option.id); setReplaceGroupId(group.id); setActiveGroup(group.id); setStep(2); };
  const cancelReplace = () => { setReplaceOptionId(null); setReplaceGroupId(null); setStep(3); };
  const removeItem = (id: string) => { setSelected((current) => ({ ...current, [id]: false })); if (replaceOptionId === id) { setReplaceOptionId(null); setReplaceGroupId(null); } };
  const goComposition = () => { setReplaceOptionId(null); setReplaceGroupId(null); setStep(2); };
  const currentReplacing = replaceOptionId ? options.find((option) => option.id === replaceOptionId) : null;

  return <div className="rs57-page rs57-wizard-page">
    <StoreHeader/>
    <main className="rs57-wizard-shell">
      <nav className="rs57-crumbs"><Link href="/">Главная</Link><span>/</span><Link href="/ready-solutions/">Готовые решения</Link><span>/</span><b>{solution.name}</b></nav>
      <section className="rs57-wizard-hero">
        <div className="rs57-wizard-hero-media"><RemoteImage src={solutionImage(solution, rows)} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div>
        <div className="rs57-wizard-hero-copy"><small>{solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно адаптировать под своё пространство. Меняйте количество, коллекции и отдельные предметы.</p><div className="rs57-collection-links"><span>Коллекции:</span>{activeCollections.map((collection) => <Link key={collection} href={collectionHref(collection)}>{displayCollectionName(collection)}</Link>)}</div></div>
      </section>

      <nav className="rs57-stepper" aria-label="Этапы готового решения">{([1, 2, 3] as WizardStep[]).map((value) => <button key={value} type="button" className={step === value ? "is-active" : step > value ? "is-complete" : ""} onClick={() => { if (value !== 2 || !replaceOptionId) setStep(value); }}><span>{step > value ? <Icon name="check"/> : value}</span><em>{value === 1 ? "Параметры" : value === 2 ? "Состав" : "Результат"}</em></button>)}</nav>

      {step === 1 && <div className="rs57-stage rs57-parameters rs61-parameters rs62-parameters"><section className="rs62-parameters-main"><header className="rs57-stage-head"><small>ШАГ 1 ИЗ 3</small><h2>Параметры</h2><p>Выберите количество персон и коллекции, которые хотите использовать в решении.</p></header><section className="rs62-parameter-block"><header><strong>Количество персон</strong><small>Персональные предметы пересчитаются автоматически</small></header><nav className="rs62-filter-rail rs62-person-rail">{guestOptions.map((value) => <button key={value} type="button" className={guests === value ? "is-active" : ""} onClick={() => setGuests(value)}><strong>{value}</strong><span>{value === 1 ? "персона" : value <= 4 ? "персоны" : "персон"}</span></button>)}</nav></section><section className="rs62-parameter-block"><header><strong>Коллекции</strong><small>Нажмите, чтобы добавить или убрать коллекцию</small></header><nav className="rs62-filter-rail rs62-collection-rail">{availableCollections.map((collection) => { const active=activeCollections.some((value)=>norm(sourceCollectionName(value))===norm(sourceCollectionName(collection))); return <button type="button" key={collection} className={active?"is-active":""} disabled={active&&activeCollections.length===1} onClick={()=>setActiveCollections((current)=>active?current.filter((value)=>norm(sourceCollectionName(value))!==norm(sourceCollectionName(collection))):[...current,collection])}><span>{displayCollectionName(collection)}</span>{active&&<em>✓</em>}</button>; })}</nav></section><footer className="rs62-parameter-action"><div><span>{activeCollections.length} коллекций · {selectedRows.length} позиций</span><strong>{money(total)}</strong></div><button type="button" className="rs57-primary" onClick={() => setStep(2)}>К СОСТАВУ</button></footer></section></div>}

      {step === 2 && active && <div className="rs57-stage rs57-composition">
        <section className="rs57-composition-main">
          <header className="rs57-stage-head"><small>ШАГ 2 ИЗ 3</small><h2>{replaceOptionId ? "Выберите замену" : "Состав решения"}</h2><p>{replaceOptionId && currentReplacing ? `Заменяем «${currentReplacing.title}». Выберите другой предмет в этой категории — после выбора вернём вас к результату.` : "Категории и товары находятся в одном месте. Переключайтесь между категориями, отмечайте нужные предметы и сразу выбирайте цвет, размер и количество."}</p></header>
          {replaceOptionId && <div className="rs57-replace-banner"><span><b>Режим замены</b><small>{currentReplacing?.title}</small></span><button type="button" onClick={cancelReplace}>Отменить</button></div>}
          <nav className="rs57-group-tabs rs62-category-rail" aria-label="Категории решения">{groups.filter((group) => !replaceGroupId || group.id === replaceGroupId).map((group) => <button type="button" key={group.id} className={active.id === group.id ? "is-active" : ""} onClick={() => setActiveGroup(group.id)}><span>{group.title}</span><em>{group.items.filter(({ option }) => selected[option.id]).length}/{group.items.length}</em></button>)}</nav>
          <ProductGroup group={active} filter={filters[active.id] || "all"} onFilter={(value) => setFilters((current) => ({ ...current, [active.id]: value }))} collectionFilter={collectionFilters[active.id] || "all"} onCollectionFilter={(value) => setCollectionFilters((current) => ({ ...current, [active.id]: value }))} selected={selected} colors={colors} sizes={sizes} qty={qty} guests={guests} replacingId={replaceOptionId} onSelected={handleSelect} onColor={(id, value) => { setColors((current) => ({ ...current, [id]: value })); const option = active.items.find((item) => item.option.id === id)?.option; if (option) setSizes((current) => ({ ...current, [id]: optionSizes(option, value)[0] || "" })); }} onSize={(id, value) => setSizes((current) => ({ ...current, [id]: value }))} onQty={(id, value) => setQty((current) => ({ ...current, [id]: Math.max(1, value) }))}/>
        </section>
        <aside className="rs57-summary-card rs57-sticky-summary"><small>ВАШ ВЫБОР</small><h3>{selectedRows.length ? `${selectedRows.length} позиций` : "Начните с товаров"}</h3><div className="rs57-summary-lines">{selectedRows.slice(0, 5).map(({ option, quantity }) => <p key={option.id}><span>{option.title}</span><em>× {quantity}</em></p>)}{selectedRows.length > 5 && <p><span>И ещё</span><em>+{selectedRows.length - 5}</em></p>}</div><footer><span>Итого</span><strong>{money(total)}</strong></footer><button type="button" className="rs57-primary" onClick={() => setStep(3)} disabled={!selectedRows.length}>ПЕРЕЙТИ К РЕЗУЛЬТАТУ</button></aside>
      </div>}

      {step === 3 && <div className="rs57-stage rs57-result-stage rs60-result-stage rs61-result-stage">
        <section className="rs60-result-main rs61-result-main"><header className="rs57-stage-head rs60-result-head"><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2><p>Собранный образ из тех же товарных карточек, что в каталоге. Количество, цвет, замену и удаление можно менять прямо здесь.</p></header>
          {selectedRows.length ? <section className="rs61-moodboard" aria-label="Выбранные товары">
            <div className="rs61-moodboard-grid">
              {selectedRows.map(({ row, quantity, option, group }, index) => <article className={`product-card rs61-moodboard-card rs61-mood-${index % 7}`} key={`mood-${option.id}-${row.offer_id}`}>
                <div className="product-image rs61-moodboard-media"><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div>
                <div className="product-copy rs61-moodboard-copy"><div className="product-link"><strong>{option.title}</strong><small>{[displayCollectionName(option.collection || row.collection || ""), row.color, row.size || row.volume].filter(Boolean).join(" · ")}</small></div>{optionColors(option).length > 1 && <div className="plp-swatches" role="group" aria-label={`Цвет товара ${option.title}`}>{optionColors(option).map((value) => <button type="button" key={value} className={(colors[option.id] || row.color) === value ? "active" : ""} style={{ background: swatchColor(value) }} onClick={() => { setColors((current) => ({ ...current, [option.id]: value })); setSizes((current) => ({ ...current, [option.id]: optionSizes(option, value)[0] || "" })); }} aria-label={`Выбрать цвет ${value}`} title={value}/>)}</div>}<span className="price">{money(priceOf(row))}</span></div>
                <div className="rs61-moodboard-controls"><div className="rs61-qty"><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))} aria-label="Увеличить количество">+</button></div><div className="rs61-card-actions"><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></div>
              </article>)}
              <button type="button" className="product-card rs61-add-card" onClick={goComposition}><span>+</span><strong>Добавить предмет</strong><small>Выбрать категорию или коллекцию</small></button>
            </div>
            <footer className="rs60-result-total rs61-result-total"><div><span>{selectedRows.length} позиций · {activeCollections.length} коллекций</span><strong>{money(total)}</strong></div><button type="button" className="rs57-primary" onClick={addToCart}>ДОБАВИТЬ ВСЁ В КОРЗИНУ</button></footer>
          </section> : <div className="rs57-empty-result"><h3>В решении пока нет товаров</h3><button type="button" onClick={goComposition}>Добавить предмет</button></div>}
        </section>
      </div>}
    </main>

    <div className="rs57-mobile-dock"><span><small>{selectedRows.length} позиций</small><strong>{money(total)}</strong></span>{step === 1 ? <button type="button" onClick={() => setStep(2)}>К СОСТАВУ</button> : step === 2 ? <button type="button" onClick={() => setStep(3)} disabled={!selectedRows.length}>РЕЗУЛЬТАТ</button> : <button type="button" onClick={addToCart} disabled={!selectedRows.length}>В КОРЗИНУ</button>}</div>
    <StoreFooter/>
  </div>;
}

function ProductGroup({ group, filter, onFilter, collectionFilter, onCollectionFilter, selected, colors, sizes, qty, guests, replacingId, onSelected, onColor, onSize, onQty }: { group: FormGroup; filter: string; onFilter: (value: string) => void; collectionFilter: string; onCollectionFilter: (value: string) => void; selected: Record<string, boolean>; colors: Record<string, string>; sizes: Record<string, string>; qty: Record<string, number>; guests: number; replacingId: string | null; onSelected: (id: string, value: boolean) => void; onColor: (id: string, value: string) => void; onSize: (id: string, value: string) => void; onQty: (id: string, value: number) => void }) { const subs=Array.from(new Map(group.items.map((item)=>[item.subcategoryId,item.subcategoryTitle])).entries()); const cols=Array.from(new Set(group.items.map((item)=>item.option.collection).filter(Boolean))).sort((a,b)=>displayCollectionName(a).localeCompare(displayCollectionName(b),"ru")); const visible=group.items.filter((item)=>(filter==="all"||item.subcategoryId===filter)&&(collectionFilter==="all"||norm(item.option.collection)===norm(collectionFilter))); const all=visible.length>0&&visible.every(({option})=>selected[option.id]); return <section className="rs57-product-group rs60-product-group rs62-product-group"><header><div><small>СОСТАВ</small><h3>{group.title}</h3></div>{!replacingId&&<button type="button" onClick={()=>visible.forEach(({option})=>onSelected(option.id,!all))}>{all?"Снять выбор":"Выбрать всё"}</button>}</header>{(subs.length>1||cols.length>1)&&<div className="rs62-product-filters">{subs.length>1&&<section><span>Тип</span><nav className="rs62-filter-rail"><button type="button" className={filter==="all"?"is-active":""} onClick={()=>onFilter("all")}>Все</button>{subs.map(([id,title])=><button type="button" key={id} className={filter===id?"is-active":""} onClick={()=>onFilter(id)}>{title}</button>)}</nav></section>}{cols.length>1&&<section><span>Коллекция</span><nav className="rs62-filter-rail"><button type="button" className={collectionFilter==="all"?"is-active":""} onClick={()=>onCollectionFilter("all")}>Все</button>{cols.map((value)=><button type="button" key={value} className={norm(collectionFilter)===norm(value)?"is-active":""} onClick={()=>onCollectionFilter(value)}>{displayCollectionName(value)}</button>)}</nav></section>}</div>}<div className="product-grid rs57-product-grid rs62-product-grid">{visible.map((item)=><ReadyCatalogCard key={item.option.id} option={item.option} selected={Boolean(selected[item.option.id])} color={colors[item.option.id]||""} size={sizes[item.option.id]||""} quantity={qty[item.option.id]||recommendedOptionQuantity(item.option,guests)} guests={guests} replacing={Boolean(replacingId)} replacingSelf={replacingId===item.option.id} onToggle={()=>onSelected(item.option.id,!selected[item.option.id])} onColor={(value)=>onColor(item.option.id,value)} onSize={(value)=>onSize(item.option.id,value)} onQty={(value)=>onQty(item.option.id,value)}/>)}</div></section>; }

function ReadyCatalogCard({ option, selected, color, size, quantity, guests, replacing, replacingSelf, onToggle, onColor, onSize, onQty }: { option: SolutionProductOption; selected: boolean; color: string; size: string; quantity: number; guests: number; replacing: boolean; replacingSelf: boolean; onToggle: () => void; onColor: (value: string) => void; onSize: (value: string) => void; onQty: (value: number) => void }) {
  const [liked, setLiked] = useState(false);
  const colors = optionColors(option);
  const sizes = optionSizes(option, color);
  const row = pickOptionVariant(option, color, size);
  const image = rowImages(row)[0] || "/images/image-placeholder.svg";
  const note = [row?.material, row?.size || row?.volume].filter(Boolean).join(", ");
  const productHref = row?.product_url || "";
  return <div className={`rs57-product-wrap ${selected ? "is-selected" : ""} ${replacingSelf ? "is-replacing" : ""}`}>
    <article className="product-card rs57-product-card">
      <button className={`heart ${liked ? "liked" : ""}`} type="button" onClick={() => setLiked((value) => !value)} aria-label={liked ? `Удалить ${option.title} из избранного` : `Добавить ${option.title} в избранное`}><Icon name="heart" filled={liked}/></button>
      {productHref ? <a className="product-image" href={productHref} target="_blank" rel="noreferrer"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></a> : <div className="product-image"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div>}
      <div className="product-copy"><div className="product-link"><strong>{option.title}</strong><small>{[color || row?.color, note].filter(Boolean).join(", ")}</small></div>{colors.length > 1 && <div className="plp-swatches" role="group" aria-label={`Цвет товара ${option.title}`}>{colors.map((value) => <button type="button" key={value} className={(color || row?.color) === value ? "active" : ""} style={{ background: swatchColor(value) }} onClick={() => onColor(value)} aria-label={`Выбрать цвет ${value}`} title={value}/>)}</div>}<span className="price">{money(priceOf(row))}</span></div>
      <button className={`quick selection-check rs62-selection-check ${selected ? "selected" : ""}`} type="button" onClick={onToggle} disabled={replacingSelf} aria-pressed={selected}>{selected ? "✓" : replacing ? "+" : ""}</button>
    </article>
    {selected && !replacing && <div className="rs57-card-controls">{sizes.length > 1 && <label className="v52-inline-size"><span>Размер</span><select value={size} onChange={(event) => onSize(event.target.value)}>{sizes.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>}<div className="rs57-inline-qty"><span>Количество<small>{option.perPerson ? `по числу персон: ${guests}` : "на всё решение"}</small></span><div><button type="button" onClick={() => onQty(Math.max(1, quantity - 1))}>−</button><b>{quantity}</b><button type="button" onClick={() => onQty(quantity + 1)}>+</button></div></div></div>}
  </div>;
}
