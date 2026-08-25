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

const basePath = "";
const browserBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const CART_KEY = "kultura-cart";
const SAVED_KEY = "kultura-ready-solution-v55";
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

function Icon({ name }: { name: "search" | "user" | "bag" | "pin" | "arrow" | "check" }) {
  const common = { fill: "none", stroke: "currentColor", strokeWidth: 1.6, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "search") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if (name === "user") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if (name === "bag") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if (name === "pin") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if (name === "check") return <svg viewBox="0 0 20 20" aria-hidden="true" {...common}><path d="m4.5 10 3.2 3.2 7.8-8"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
}

function ReadyHeader() {
  return <>
    <div className="rs55-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</div>
    <header className="rs55-header">
      <div className="rs55-header-left"><Link href={`${basePath}/`}>МЕНЮ</Link><Link href={`${basePath}/?open=boutiques`} className="rs55-boutiques"><Icon name="pin"/> Бутики</Link></div>
      <Link className="rs55-logo" href={`${basePath}/`}>КУЛЬТУРА ДОМА</Link>
      <nav className="rs55-header-actions" aria-label="Сервис"><Link href={`${basePath}/?open=search`} aria-label="Поиск"><Icon name="search"/></Link><Link href={`${basePath}/?open=account`} aria-label="Профиль"><Icon name="user"/></Link><Link href={`${basePath}/?open=cart`} aria-label="Корзина"><Icon name="bag"/></Link></nav>
    </header>
  </>;
}

function ReadyFooter() {
  return <footer className="rs55-footer"><div><strong>КУЛЬТУРА ДОМА</strong><p>Предметы и сценарии для дома, собранные в цельные композиции.</p></div><nav><Link href={`${basePath}/`}>Каталог</Link><Link href={`${basePath}/?open=boutiques`}>Бутики</Link><Link href={`${basePath}/?open=account`}>Личный кабинет</Link></nav></footer>;
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
    id,
    name: row.product_name,
    note: [row.collection, row.material].filter(Boolean).join(" · "),
    price,
    image: images[0] || "/images/image-placeholder.svg",
    gallery: images.slice(1),
    selectedColor: color,
    selectedSize: size,
    selectedSkuId: `ready-${row.offer_id || id}`,
    quantity,
    skus: [{ id: `ready-${row.offer_id || id}`, article: row.vendor_code || String(row.offer_id), productId: id, color, colorHex: "#d8d5cf", size, material: row.material || "", composition: row.material || "", price, image: images[0] || "/images/image-placeholder.svg", gallery: images.slice(1) }],
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
  tableware: { title: "Посуда и сервировка", description: "Тарелки, чайные пары, блюда, стекло и приборы для общей композиции стола.", categories: ["plates", "bowls", "cupsPairs", "greenSalonTeaService", "sugarBowls", "milkJugs", "teapots", "serving", "drinkware", "cutlery"] },
  tableTextile: { title: "Столовый текстиль", description: "Скатерти, дорожки, плейсматы и салфетки — количество персональных предметов пересчитывается автоматически.", categories: ["tableTextile"] },
  bedding: { title: "Постельное бельё", description: "Комплекты, пододеяльники, простыни и наволочки для основной текстильной базы спальни.", categories: ["bedding"] },
  throws: { title: "Пледы и покрывала", description: "Фактурные слои, которые связывают кровать, диван и цветовую палитру пространства.", categories: ["throwsCoverlets"] },
  pillows: { title: "Декоративные подушки", description: "Акцентные подушки и варианты отделки для завершения текстильной композиции.", categories: ["decorativePillows"] },
  decor: { title: "Декор для дома", description: "Вазы, предметы интерьера, игры и функциональный декор — добавляйте только нужные акценты.", categories: ["vases", "baskets", "games", "storage", "other"] },
  atmosphere: { title: "Свечи и диффузоры", description: "Свечи, подсвечники и ароматы для финального атмосферного слоя.", categories: ["atmosphere"] },
  bath: { title: "Для ванной", description: "Полотенца, халаты и текстиль для ванной, если они входят в выбранный сценарий.", categories: ["bath"] },
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

export function ReadySolutionsLanding() {
  const { catalog, error } = useData();
  if (error) return <div className="rs55-page"><ReadyHeader/><main className="rs55-state">{error}</main></div>;
  if (!catalog) return <div className="rs55-page"><ReadyHeader/><main className="rs55-state">Загружаем готовые решения…</main></div>;
  const cards = TABLE_SOLUTIONS.map((solution) => {
    const rows = resolveTableSolutionCatalogRows(catalog.catalog, solution);
    const prices = rows.map(priceOf).filter(Boolean);
    return { solution, rows, image: solutionImage(solution, rows), from: prices.length ? Math.min(...prices) : 0 };
  });
  const featured = cards[0];
  return <div className="rs55-page">
    <ReadyHeader/>
    <main>
      <section className="rs55-landing-hero">
        <div className="rs55-landing-hero-media"><RemoteImage src={featured.image} fallbackSrc="/images/image-placeholder.svg" alt={featured.solution.name}/></div>
        <div className="rs55-landing-hero-copy"><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Дом, собранный<br/>за вас</h1><p>Выберите готовую композицию и настройте её под себя: количество персон, категории, конкретные товары, размеры и цвета.</p><Link href={`${basePath}/ready-solutions/${featured.solution.id}/`}>Собрать решение <Icon name="arrow"/></Link></div>
      </section>

      <section className="rs55-how"><header><small>КАК ЭТО РАБОТАЕТ</small><h2>От идеи до корзины — несколько понятных шагов</h2></header><div className="rs55-how-grid"><article><b>01</b><h3>Выберите пространство</h3><p>Начните с готового сценария, уже собранного стилистически.</p></article><article><b>02</b><h3>Настройте состав</h3><p>Укажите количество персон и оставьте только нужные категории и товары.</p></article><article><b>03</b><h3>Добавьте в корзину</h3><p>Проверьте размеры, цвета и итоговую стоимость перед покупкой.</p></article></div></section>

      <section className="rs55-solutions"><header><small>СЦЕНАРИИ</small><h2>Выберите готовое решение</h2></header><div className="rs55-solution-grid">{cards.map(({ solution, rows, image, from }) => <article className="rs55-solution-card" key={solution.id}><Link href={`${basePath}/ready-solutions/${solution.id}/`}><span className="rs55-solution-media"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></span><span className="rs55-solution-copy"><small>{solution.space}</small><strong>{solution.name}</strong><em>{rows.length} вариантов · {from ? `от ${money(from)}` : "собрать состав"}</em><span>Настроить решение <Icon name="arrow"/></span></span></Link></article>)}</div></section>
    </main>
    <ReadyFooter/>
  </div>;
}

type WizardStep = 1 | 2 | 3 | 4;

export function ReadySolutionWizard({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const { catalog, rules, error } = useData();
  const [step, setStep] = useState<WizardStep>(1);
  const [guests, setGuests] = useState(2);
  const [enabledGroups, setEnabledGroups] = useState<Record<string, boolean>>({});
  const [activeGroup, setActiveGroup] = useState<string>("");
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [saved, setSaved] = useState(false);

  const rows = useMemo(() => solution && catalog ? resolveTableSolutionCatalogRows(catalog.catalog, solution) : [], [catalog, solution]);
  const legacyCategories = useMemo(() => solution ? buildSolutionCategories(rows, solution.space) : [], [rows, solution]);
  const groups = useMemo(() => buildGroups(legacyCategories), [legacyCategories]);
  const options = useMemo(() => groups.flatMap((group) => group.items.map((item) => item.option)), [groups]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, rules) : [2, 4, 6], [solution, rules]);

  useEffect(() => {
    if (!solution || !groups.length || !options.length) return;
    setGuests((current) => guestOptions.includes(current) ? current : (guestOptions[0] || 2));
    setEnabledGroups((current) => Object.keys(current).length ? current : Object.fromEntries(groups.map((group) => [group.id, true])));
    setActiveGroup((current) => current || groups[0]?.id || "");
    const defaultNames = new Set((solution.defaultProductNames || []).map(norm));
    setSelected((current) => Object.keys(current).length ? current : Object.fromEntries(options.map((option) => [option.id, defaultNames.has(norm(option.title))])));
    setColors((current) => {
      if (Object.keys(current).length) return current;
      return Object.fromEntries(options.map((option) => [option.id, solution.defaultColors?.[option.title] || optionColors(option)[0] || ""]));
    });
    setSizes((current) => {
      if (Object.keys(current).length) return current;
      return Object.fromEntries(options.map((option) => { const color = solution.defaultColors?.[option.title] || optionColors(option)[0] || ""; return [option.id, solution.defaultSizes?.[option.title] || optionSizes(option, color)[0] || ""]; }));
    });
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

  const selectedRows = useMemo(() => groups.flatMap((group) => {
    if (!enabledGroups[group.id]) return [];
    return group.items.flatMap(({ option }) => {
      if (!selected[option.id]) return [];
      const row = pickOptionVariant(option, colors[option.id] || "", sizes[option.id] || "");
      return row ? [{ row, quantity: Math.max(1, qty[option.id] || recommendedOptionQuantity(option, guests)), option, group }] : [];
    });
  }), [groups, enabledGroups, selected, colors, sizes, qty, guests]);
  const total = selectedRows.reduce((sum, item) => sum + priceOf(item.row) * item.quantity, 0);
  const enabledCount = groups.filter((group) => enabledGroups[group.id]).length;
  const active = groups.find((group) => group.id === activeGroup) || groups[0];

  if (!solution) return <div className="rs55-page"><ReadyHeader/><main className="rs55-state">Решение не найдено.</main></div>;
  if (error) return <div className="rs55-page"><ReadyHeader/><main className="rs55-state">{error}</main></div>;
  if (!catalog || !groups.length) return <div className="rs55-page"><ReadyHeader/><main className="rs55-state">Собираем конструктор…</main></div>;

  const goNext = () => setStep((current) => Math.min(4, current + 1) as WizardStep);
  const goBack = () => setStep((current) => Math.max(1, current - 1) as WizardStep);
  const saveSolution = () => {
    try { localStorage.setItem(SAVED_KEY, JSON.stringify({ scenarioId, guests, enabledGroups, selected, colors, sizes, qty, total, savedAt: new Date().toISOString() })); setSaved(true); setTimeout(() => setSaved(false), 2200); } catch {}
  };
  const addToCart = () => {
    if (!selectedRows.length) return;
    addRowsToSharedCart(selectedRows.map(({ row, quantity }) => ({ row, quantity })));
    window.location.href = `${browserBasePath}/?open=cart`;
  };

  const stepTitle = step === 1 ? "Количество персон" : step === 2 ? "Что входит в решение" : step === 3 ? "Выберите товары" : "Проверьте решение";

  return <div className="rs55-page rs55-wizard-page">
    <ReadyHeader/>
    <main className="rs55-wizard-shell">
      <section className="rs55-wizard-hero"><div className="rs55-wizard-hero-media"><RemoteImage src={solutionImage(solution, rows)} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div><div><Link href={`${basePath}/ready-solutions/`}>← Все решения</Link><small>{solution.space}</small><h1>{solution.name}</h1><p>Настройте готовую композицию под своё пространство. Выбор сохраняется при переходе между шагами.</p></div></section>

      <nav className="rs55-stepper" aria-label="Шаги конструктора">{[1,2,3,4].map((value) => <button key={value} type="button" className={step === value ? "is-active" : step > value ? "is-complete" : ""} onClick={() => setStep(value as WizardStep)}><span>{step > value ? <Icon name="check"/> : value}</span><em>{value === 1 ? "Персоны" : value === 2 ? "Категории" : value === 3 ? "Товары" : "Проверка"}</em></button>)}</nav>

      <div className="rs55-form-layout">
        <section className="rs55-form-panel">
          <header className="rs55-form-head"><small>ШАГ {step} ИЗ 4</small><h2>{stepTitle}</h2>{step === 1 && <p>Персональные предметы — тарелки, пары, приборы, плейсматы и салфетки — будут пересчитаны автоматически. Декор и крупный текстиль останутся по одному.</p>}{step === 2 && <p>Оставьте только нужные части композиции. Отключённая категория не попадёт в итог, но ваш выбор внутри неё сохранится.</p>}{step === 3 && <p>Выберите конкретные позиции, затем при необходимости уточните цвет, размер и количество.</p>}{step === 4 && <p>Проверьте итоговый состав перед добавлением в корзину.</p>}</header>

          {step === 1 && <div className="rs55-person-form">{guestOptions.map((value) => <button key={value} type="button" className={guests === value ? "is-active" : ""} onClick={() => setGuests(value)}><strong>{value}</strong><span>{value === 1 ? "персона" : value >= 2 && value <= 4 ? "персоны" : "персон"}</span></button>)}</div>}

          {step === 2 && <div className="rs55-category-form">{groups.map((group) => { const representative = pickOptionVariant(group.items[0].option); const checked = enabledGroups[group.id] !== false; return <article className={`rs55-category-choice ${checked ? "is-selected" : ""}`} key={group.id}><button type="button" className="rs55-category-media" onClick={() => setEnabledGroups((current) => ({ ...current, [group.id]: !checked }))}><RemoteImage src={rowImages(representative)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={group.title}/><span className={`rs55-black-check ${checked ? "is-selected" : ""}`}>{checked && <Icon name="check"/>}</span></button><button type="button" className="rs55-category-copy" onClick={() => setEnabledGroups((current) => ({ ...current, [group.id]: !checked }))}><span><small>{group.items.length} позиций</small><strong>{group.title}</strong><p>{group.description}</p></span></button></article>; })}</div>}

          {step === 3 && active && <div className="rs55-products-step"><nav className="rs55-group-tabs" aria-label="Категории товаров">{groups.filter((group) => enabledGroups[group.id] !== false).map((group) => <button type="button" key={group.id} className={active.id === group.id ? "is-active" : ""} onClick={() => setActiveGroup(group.id)}><span>{group.title}</span><em>{group.items.filter(({ option }) => selected[option.id]).length}/{group.items.length}</em></button>)}</nav><ProductGroup group={active} filter={filters[active.id] || "all"} onFilter={(value) => setFilters((current) => ({ ...current, [active.id]: value }))} selected={selected} colors={colors} sizes={sizes} qty={qty} guests={guests} onSelected={(id, value) => setSelected((current) => ({ ...current, [id]: value }))} onColor={(id, value) => { setColors((current) => ({ ...current, [id]: value })); const option = active.items.find((item) => item.option.id === id)?.option; if (option) setSizes((current) => ({ ...current, [id]: optionSizes(option, value)[0] || "" })); }} onSize={(id, value) => setSizes((current) => ({ ...current, [id]: value }))} onQty={(id, value) => setQty((current) => ({ ...current, [id]: Math.max(1, value) }))}/></div>}

          {step === 4 && <div className="rs55-review">{selectedRows.length ? selectedRows.map(({ row, quantity, option, group }) => <article key={`${option.id}-${row.offer_id}`}><span className="rs55-review-image"><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></span><div><small>{group.title}</small><strong>{option.title}</strong><p>{[row.color, row.size || row.volume].filter(Boolean).join(" · ") || "Единый вариант"}</p><span>{quantity} × {money(priceOf(row))}</span></div><b>{money(priceOf(row) * quantity)}</b></article>) : <div className="rs55-empty"><h3>Вы пока ничего не выбрали</h3><p>Вернитесь к товарам и отметьте нужные позиции.</p><button type="button" onClick={() => setStep(3)}>Перейти к товарам</button></div>}</div>}

          <div className="rs55-form-actions">{step > 1 ? <button type="button" className="rs55-secondary" onClick={goBack}>Назад</button> : <Link className="rs55-secondary" href={`${basePath}/ready-solutions/`}>Все решения</Link>}{step < 4 ? <button type="button" className="rs55-primary" onClick={goNext} disabled={step === 2 && enabledCount === 0}>Продолжить</button> : <><button type="button" className="rs55-save" onClick={saveSolution}>{saved ? "Сохранено ✓" : "Сохранить решение"}</button><button type="button" className="rs55-primary" onClick={addToCart} disabled={!selectedRows.length}>Добавить в корзину</button></>}</div>
        </section>

        <aside className="rs55-summary-card"><small>ВАШЕ РЕШЕНИЕ</small><h3>{solution.name}</h3><dl><div><dt>Персон</dt><dd>{guests}</dd></div><div><dt>Категорий</dt><dd>{enabledCount}</dd></div><div><dt>Выбрано</dt><dd>{selectedRows.length}</dd></div></dl><div className="rs55-summary-lines">{selectedRows.slice(0,5).map(({ option, quantity }) => <p key={option.id}><span>{option.title}</span><em>× {quantity}</em></p>)}{selectedRows.length > 5 && <p><span>И ещё</span><em>+{selectedRows.length - 5}</em></p>}</div><footer><span>Итого</span><strong>{money(total)}</strong></footer></aside>
      </div>
    </main>

    <div className="rs55-mobile-summary"><span><small>{selectedRows.length} товаров</small><strong>{money(total)}</strong></span>{step < 4 ? <button type="button" onClick={goNext} disabled={step === 2 && enabledCount === 0}>Продолжить</button> : <button type="button" onClick={addToCart} disabled={!selectedRows.length}>В корзину</button>}</div>
    <ReadyFooter/>
  </div>;
}

function ProductGroup({ group, filter, onFilter, selected, colors, sizes, qty, guests, onSelected, onColor, onSize, onQty }: { group: FormGroup; filter: string; onFilter: (value: string) => void; selected: Record<string, boolean>; colors: Record<string, string>; sizes: Record<string, string>; qty: Record<string, number>; guests: number; onSelected: (id: string, value: boolean) => void; onColor: (id: string, value: string) => void; onSize: (id: string, value: string) => void; onQty: (id: string, value: number) => void }) {
  const subcategories = Array.from(new Map(group.items.map((item) => [item.subcategoryId, item.subcategoryTitle])).entries());
  const visible = filter === "all" ? group.items : group.items.filter((item) => item.subcategoryId === filter);
  const allVisibleSelected = visible.length > 0 && visible.every(({ option }) => selected[option.id]);
  return <section className="rs55-product-group"><header><div><small>КАТЕГОРИЯ</small><h3>{group.title}</h3><p>{group.description}</p></div><button type="button" onClick={() => visible.forEach(({ option }) => onSelected(option.id, !allVisibleSelected))}>{allVisibleSelected ? "Снять всё" : "Выбрать всё"}</button></header>{subcategories.length > 1 && <div className="rs55-filters"><button type="button" className={filter === "all" ? "is-active" : ""} onClick={() => onFilter("all")}>Все</button>{subcategories.map(([id, title]) => <button type="button" key={id} className={filter === id ? "is-active" : ""} onClick={() => onFilter(id)}>{title}</button>)}</div>}<div className="rs55-product-grid">{visible.map((item) => <ReadyProductCard key={item.option.id} option={item.option} selected={Boolean(selected[item.option.id])} color={colors[item.option.id] || ""} size={sizes[item.option.id] || ""} quantity={qty[item.option.id] || recommendedOptionQuantity(item.option, guests)} guests={guests} onToggle={() => onSelected(item.option.id, !selected[item.option.id])} onColor={(value) => onColor(item.option.id, value)} onSize={(value) => onSize(item.option.id, value)} onQty={(value) => onQty(item.option.id, value)}/>)}</div></section>;
}

function ReadyProductCard({ option, selected, color, size, quantity, guests, onToggle, onColor, onSize, onQty }: { option: SolutionProductOption; selected: boolean; color: string; size: string; quantity: number; guests: number; onToggle: () => void; onColor: (value: string) => void; onSize: (value: string) => void; onQty: (value: number) => void }) {
  const colors = optionColors(option);
  const sizes = optionSizes(option, color);
  const row = pickOptionVariant(option, color, size);
  const image = rowImages(row)[0] || "/images/image-placeholder.svg";
  return <article className={`rs55-product-card ${selected ? "is-selected" : ""}`}><div className="rs55-product-media"><button type="button" onClick={onToggle} className="rs55-product-image"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></button><button type="button" className={`rs55-black-check ${selected ? "is-selected" : ""}`} onClick={onToggle} aria-pressed={selected} aria-label={selected ? `Убрать ${option.title}` : `Добавить ${option.title}`}>{selected && <Icon name="check"/>}</button></div><div className="rs55-product-copy"><div><small>{row?.collection || "Культура Дома"}</small><strong>{option.title}</strong></div><span>{money(priceOf(row))}</span></div>{selected && <div className="rs55-product-controls">{colors.length > 1 && <fieldset><legend>Цвет</legend><div className="rs55-option-row">{colors.map((value) => <button type="button" key={value} className={color === value ? "is-active" : ""} onClick={() => onColor(value)}>{value}</button>)}</div></fieldset>}{sizes.length > 1 && <label><span>Размер</span><select value={size} onChange={(event) => onSize(event.target.value)}>{sizes.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>}<div className="rs55-qty"><span>Количество<small>{option.perPerson ? `по числу персон: ${guests}` : "на всё решение"}</small></span><div><button type="button" onClick={() => onQty(Math.max(1, quantity - 1))}>−</button><b>{quantity}</b><button type="button" onClick={() => onQty(quantity + 1)}>+</button></div></div></div>}</article>;
}
