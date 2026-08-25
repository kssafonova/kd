"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS, findTableSolution, type TableSolution } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedOptionQuantity,
  type SolutionCategory,
  type SolutionProductOption,
} from "./table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "./types";

const CART_KEY = "kultura-cart";
const CART_OFFSET = 970000;
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const rowPrice = (value?: string) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const norm = (value: string) => String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/[«»"']/g, "").replace(/\s+/g, " ");
const rowImages = (row?: CatalogRow) => Array.from(new Set([row?.primary_image_url, ...(row?.all_image_urls || "").split("|")].filter((value): value is string => Boolean(value))));

const colorHex = (value: string) => {
  const v = norm(value);
  if (v.includes("бел") || v.includes("молоч") || v.includes("айвори")) return "#f2f0e9";
  if (v.includes("черн")) return "#1d1d1b";
  if (v.includes("ночн") || v.includes("темно-син")) return "#24364a";
  if (v.includes("голуб")) return "#9db8c7";
  if (v.includes("син")) return "#506b82";
  if (v.includes("зелен")) return "#62765f";
  if (v.includes("красн") || v.includes("бордо")) return "#8f403e";
  if (v.includes("пудр") || v.includes("роз")) return "#d6aaa7";
  if (v.includes("беж") || v.includes("льнян") || v.includes("песоч")) return "#cab89e";
  if (v.includes("сер")) return "#a3a29d";
  if (v.includes("золот")) return "#b99a5f";
  return "#d8d5cf";
};

type CartItem = {
  id: number;
  name: string;
  note: string;
  price: number;
  image: string;
  gallery: string[];
  selectedColor: string;
  selectedSize: string;
  selectedSkuId: string;
  quantity: number;
  skus: Array<{ id: string; article: string; productId: number; color: string; colorHex: string; size: string; material: string; composition: string; price: number; image: string; gallery: string[] }>;
};

function addToSharedCart(items: CartItem[]) {
  let current: CartItem[] = [];
  try { current = JSON.parse(localStorage.getItem(CART_KEY) || "[]") as CartItem[]; } catch {}
  const next = [...current];
  items.forEach((item) => {
    const index = next.findIndex((existing) => existing.id === item.id && existing.selectedColor === item.selectedColor && existing.selectedSize === item.selectedSize);
    if (index >= 0) next[index] = { ...next[index], quantity: next[index].quantity + item.quantity };
    else next.push(item);
  });
  try { localStorage.setItem(CART_KEY, JSON.stringify(next)); } catch {}
}

function Arrow() {
  return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h14M13 7l5 5-5 5"/></svg>;
}

function ReadyHeaderV47() {
  const [menu, setMenu] = useState(false);
  return <>
    <div className="rs47-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</div>
    <header className="rs47-header">
      <div className="rs47-header-left"><button type="button" className="rs47-menu-button" onClick={() => setMenu(true)} aria-label="Открыть меню"><span/><span/></button><Link href={`${basePath}/`}>Бутики</Link></div>
      <Link className="rs47-logo" href={`${basePath}/`}>КУЛЬТУРА ДОМА</Link>
      <nav className="rs47-header-actions" aria-label="Сервисы"><Link href={`${basePath}/`}>Поиск</Link><Link href={`${basePath}/`}>Профиль</Link><Link href={`${basePath}/?cart=open`}>Корзина</Link></nav>
    </header>
    {menu && <div className="rs47-menu" role="dialog" aria-modal="true"><button className="rs47-menu-bg" type="button" onClick={() => setMenu(false)} aria-label="Закрыть меню"/><aside><header><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={() => setMenu(false)}>×</button></header><nav><small>КАТАЛОГ</small><Link href={`${basePath}/`}>Новинки</Link><Link href={`${basePath}/`}>Спальня</Link><Link href={`${basePath}/`}>Кухня и столовая</Link><Link href={`${basePath}/`}>Декор</Link><small>ВДОХНОВЕНИЕ</small><Link href={`${basePath}/`}>Капсулы и коллекции</Link><Link className="active" href={`${basePath}/constructor/`}>Готовые решения</Link></nav></aside></div>}
  </>;
}

function ReadyFooterV47() {
  return <footer className="rs47-footer"><div><strong>КУЛЬТУРА ДОМА</strong><p>Предметы и истории для дома, в котором традиция звучит современно.</p></div><nav><Link href={`${basePath}/`}>Каталог</Link><Link href={`${basePath}/constructor/`}>Готовые решения</Link><Link href={`${basePath}/`}>Доставка и оплата</Link><Link href={`${basePath}/`}>Бутики</Link></nav><small>© 2026 Культура Дома</small></footer>;
}

function useConstructorData() {
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

export function ReadySolutionsLandingV47() {
  const { catalog, error } = useConstructorData();
  const [space, setSpace] = useState("Все");
  const cards = useMemo(() => !catalog ? [] : TABLE_SOLUTIONS.map((solution) => {
    const rows = resolveTableSolutionCatalogRows(catalog.catalog, solution);
    return { solution, rows, image: solutionImage(solution, rows), count: Array.from(new Set(rows.map((row) => norm(row.product_name)))).length };
  }), [catalog]);
  const spaces = ["Все", ...Array.from(new Set(TABLE_SOLUTIONS.map((solution) => solution.space)))];
  const visible = cards.filter(({ solution }) => space === "Все" || solution.space === space);
  const hero = visible[0] || cards[0];

  if (error) return <><ReadyHeaderV47/><main className="rs47-state"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></main></>;
  if (!catalog) return <><ReadyHeaderV47/><main className="rs47-state">Загружаем готовые решения…</main></>;

  return <div className="rs47-page"><ReadyHeaderV47/><main className="rs47-landing">
    <section className="rs47-landing-hero">
      <div className="rs47-landing-copy"><small>ГОТОВЫЕ РЕШЕНИЯ · КУЛЬТУРА ДОМА</small><h1>Дом, собранный в единую историю</h1><p>Не начинайте с пустой корзины. Выберите готовое пространство, а затем оставьте только нужные предметы, цвета и размеры.</p><a href="#rs47-solutions">Смотреть решения <Arrow/></a></div>
      <div className="rs47-landing-media">{hero && <RemoteImage src={hero.image} fallbackSrc={hero.rows[0]?.primary_image_url} alt={hero.solution.name} loading="eager"/>}<div>{hero && <><small>{hero.solution.space}</small><strong>{hero.solution.name}</strong></>}</div></div>
      <div className="rs47-steps"><article><b>01</b><div><strong>Выберите пространство</strong><p>Сервировка, спальня или гостиная — начните с готовой композиции.</p></div></article><article><b>02</b><div><strong>Настройте предметы</strong><p>Добавляйте и убирайте товары, меняйте оттенок, размер и количество.</p></div></article><article><b>03</b><div><strong>Добавьте всё сразу</strong><p>Итог пересчитывается автоматически, а товары попадут в обычную корзину сайта.</p></div></article></div>
    </section>

    <section className="rs47-filter" aria-label="Фильтр по пространству"><span>Пространство</span><div>{spaces.map((item) => <button type="button" key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}</div><small>{visible.length} {visible.length === 1 ? "решение" : "решения"}</small></section>

    <section className="rs47-solutions" id="rs47-solutions"><header><div><small>ПОДБОРКИ ДЛЯ ДОМА</small><h2>Готовые пространства</h2></div><p>Внутри каждого решения — обычные карточки товаров из каталога и только один дополнительный слой: выбор состава.</p></header><div className="rs47-solution-grid">{visible.map(({ solution, rows, image, count }) => <Link className="rs47-solution-card" href={`${basePath}/constructor/${solution.id}/`} key={solution.id}><span className="rs47-solution-image"><RemoteImage src={image} fallbackSrc={rows[0]?.primary_image_url} alt={solution.name}/></span><span className="rs47-solution-info"><small>{solution.space}</small><strong>{solution.name}</strong><p>{solution.collections.join(" · ")}</p><span><em>{count} позиций</em><b>Настроить <Arrow/></b></span></span></Link>)}</div></section>
  </main><ReadyFooterV47/></div>;
}

function orderedCategories(categories: SolutionCategory[], solution: TableSolution) {
  const order = solution.productOrder?.map(norm) ?? [];
  if (!order.length) return categories;
  return categories.map((category) => ({ ...category, slots: category.slots.map((slot) => ({ ...slot, options: [...slot.options].sort((a, b) => {
    const ai = order.indexOf(norm(a.title));
    const bi = order.indexOf(norm(b.title));
    return (ai < 0 ? 9999 : ai) - (bi < 0 ? 9999 : bi);
  }) })) }));
}

export function ReadySolutionDetailV47({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const { catalog, rules, error } = useConstructorData();
  const [guests, setGuests] = useState(2);
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [saved, setSaved] = useState(false);
  const [adding, setAdding] = useState(false);

  const rows = useMemo(() => catalog && solution ? resolveTableSolutionCatalogRows(catalog.catalog, solution) : [], [catalog, solution]);
  const categories = useMemo(() => solution ? orderedCategories(buildSolutionCategories(rows, solution.space), solution) : [], [rows, solution]);
  const options = useMemo(() => categories.flatMap((category) => category.slots.flatMap((slot) => slot.options)), [categories]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, rules) : [2], [solution, rules]);
  const isDining = Boolean(solution?.space.toLocaleLowerCase("ru-RU").includes("кухн"));

  useEffect(() => { if (guestOptions.length && !guestOptions.includes(guests)) setGuests(guestOptions[0]); }, [guestOptions, guests]);
  useEffect(() => { setSelected({}); setColors({}); setSizes({}); setQty({}); setSaved(false); }, [scenarioId]);
  useEffect(() => {
    if (!solution || !options.length || Object.keys(selected).length) return;
    const defaults = (solution.defaultProductNames ?? solution.productNames).map(norm);
    const nextSelected: Record<string, boolean> = {};
    const nextColors: Record<string, string> = {};
    const nextSizes: Record<string, string> = {};
    const nextQty: Record<string, number> = {};
    options.forEach((option) => {
      const title = norm(option.title);
      nextSelected[option.id] = defaults.some((target) => target === title || target.includes(title) || title.includes(target));
      const defaultColor = Object.entries(solution.defaultColors ?? {}).find(([name]) => norm(name) === title)?.[1];
      const defaultSize = Object.entries(solution.defaultSizes ?? {}).find(([name]) => norm(name) === title)?.[1];
      const defaultQty = Object.entries(solution.defaultQuantities ?? {}).find(([name]) => norm(name) === title)?.[1];
      if (defaultColor) nextColors[option.id] = defaultColor;
      if (defaultSize) nextSizes[option.id] = defaultSize;
      if (defaultQty) nextQty[option.id] = defaultQty;
    });
    setSelected(nextSelected); setColors(nextColors); setSizes(nextSizes); setQty(nextQty);
  }, [options, solution, selected]);

  if (!solution) return <><ReadyHeaderV47/><main className="rs47-state"><h1>Решение не найдено</h1><Link href={`${basePath}/constructor/`}>Вернуться</Link></main></>;
  if (error) return <><ReadyHeaderV47/><main className="rs47-state"><h1>Не удалось загрузить решение</h1><p>{error}</p></main></>;
  if (!catalog) return <><ReadyHeaderV47/><main className="rs47-state">Загружаем решение…</main></>;

  const isChecked = (option: SolutionProductOption) => Boolean(selected[option.id]);
  const rowFor = (option: SolutionProductOption) => {
    const availableColors = optionColors(option);
    const activeColor = colors[option.id] || availableColors[0] || "";
    const availableSizes = optionSizes(option, activeColor);
    const activeSize = sizes[option.id] || availableSizes[0] || "";
    return pickOptionVariant(option, activeColor, activeSize) || option.variants[0];
  };
  const countFor = (option: SolutionProductOption) => qty[option.id] ?? recommendedOptionQuantity(option, guests);
  const active = options.filter(isChecked).map((option) => ({ option, row: rowFor(option), quantity: countFor(option) })).filter((item): item is { option: SolutionProductOption; row: CatalogRow; quantity: number } => Boolean(item.row));
  const units = active.reduce((sum, item) => sum + item.quantity, 0);
  const total = active.reduce((sum, item) => sum + rowPrice(item.row.price) * item.quantity, 0);
  const hero = solutionImage(solution, rows);

  const toggleCategory = (list: SolutionProductOption[]) => {
    const all = list.length > 0 && list.every(isChecked);
    setSelected((current) => ({ ...current, ...Object.fromEntries(list.map((option) => [option.id, !all])) }));
  };
  const save = () => {
    try { localStorage.setItem(`kultura-ready-solution-${scenarioId}`, JSON.stringify({ guests, items: active.map(({ option, row, quantity }) => ({ optionId: option.id, offerId: row.offer_id, quantity })) })); setSaved(true); } catch {}
  };
  const add = () => {
    const items: CartItem[] = active.map(({ option, row, quantity }, index) => {
      const numeric = Number(String(row.offer_id).split("-")[0]) || index + 1;
      const productId = CART_OFFSET + numeric;
      const image = row.primary_image_url || "/images/image-placeholder.svg";
      const selectedSize = row.size || row.volume || "Стандартный";
      return { id: productId, name: option.title, note: `Из готового решения «${solution.name}» · ${option.collection || "Культура Дома"}`, price: rowPrice(row.price), image, gallery: rowImages(row), selectedColor: row.color || "", selectedSize, selectedSkuId: `ready-${solution.sourceId}-${row.offer_id}`, quantity, skus: option.variants.map((variant, variantIndex) => ({ id: `ready-${solution.sourceId}-${variant.offer_id}`, article: variant.vendor_code || String(variant.offer_id), productId: CART_OFFSET + (Number(String(variant.offer_id).split("-")[0]) || numeric + variantIndex), color: variant.color || "", colorHex: colorHex(variant.color || ""), size: variant.size || variant.volume || "Стандартный", material: variant.material || "", composition: "", price: rowPrice(variant.price), image: variant.primary_image_url || image, gallery: rowImages(variant) })) };
    });
    if (!items.length) return;
    addToSharedCart(items); setAdding(true);
    window.setTimeout(() => { window.location.href = `${basePath}/?cart=open`; }, 280);
  };

  return <div className="rs47-page"><ReadyHeaderV47/><main className="rs47-detail">
    <nav className="rs47-breadcrumb"><Link href={`${basePath}/constructor/`}>← Готовые решения</Link><span>{solution.space}</span></nav>
    <section className="rs47-detail-hero"><div className="rs47-detail-image"><RemoteImage src={hero} fallbackSrc={rows[0]?.primary_image_url} alt={solution.name} loading="eager"/></div><div className="rs47-detail-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно настроить как обычную корзину: оставить нужное, поменять цвет и размер, увеличить количество.</p><div className="rs47-collection-tags">{solution.collections.map((collection) => <span key={collection}>{collection}</span>)}</div><div className="rs47-hero-meta"><span><b>{active.length}</b> выбрано</span><span><b>{units}</b> предметов</span><span><b>{money(total)}</b> итог</span></div><button type="button" className={`rs47-save-link ${saved ? "saved" : ""}`} onClick={save}>{saved ? "✓ Решение сохранено" : "♡ Сохранить решение"}</button></div></section>

    {isDining && guestOptions.length > 1 && <section className="rs47-guests"><div><small>СЕРВИРОВКА</small><strong>На сколько человек собираем стол?</strong><p>Количество индивидуальных предметов пересчитается автоматически.</p></div><div>{guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQty({}); }}><b>{value}</b><span>{value === 1 ? "человек" : "человека"}</span></button>)}</div></section>}

    <nav className="rs47-category-nav" aria-label="Группы товаров">{categories.map((category) => { const list = category.slots.flatMap((slot) => slot.options); const count = list.filter(isChecked).length; return <a key={category.id} href={`#rs47-${category.id}`}><span>{category.title}</span><small>{count}/{list.length}</small></a>; })}</nav>

    <div className="rs47-commerce"><section className="rs47-groups">{categories.map((category) => {
      const list = category.slots.flatMap((slot) => slot.options);
      const selectedCount = list.filter(isChecked).length;
      const all = list.length > 0 && selectedCount === list.length;
      return <section className="rs47-group" id={`rs47-${category.id}`} key={category.id}><header><div><h2>{category.title}</h2><p>{category.description}</p></div><label><input type="checkbox" checked={all} onChange={() => toggleCategory(list)}/><span>{all ? "Выбрано всё" : "Выбрать всё"}</span></label></header><div className="rs47-product-grid">{list.map((option) => {
        const checked = isChecked(option);
        const row = rowFor(option);
        const colorsList = optionColors(option);
        const activeColor = colors[option.id] || colorsList[0] || "";
        const sizeList = optionSizes(option, activeColor);
        const activeSize = sizes[option.id] || sizeList[0] || "";
        const quantity = countFor(option);
        return <article className={`rs47-product ${checked ? "selected" : ""}`} key={option.id}><div className="rs47-product-media"><RemoteImage src={row?.primary_image_url || "/images/image-placeholder.svg"} alt={option.title}/><button type="button" className="rs47-product-select" aria-pressed={checked} onClick={() => setSelected((current) => ({ ...current, [option.id]: !checked }))}>{checked ? "✓ В решении" : "+ Добавить"}</button></div><div className="rs47-product-copy"><small>{option.collection || "Культура Дома"}</small><h3>{option.title}</h3><strong>{rowPrice(row?.price) ? money(rowPrice(row?.price)) : "Цена уточняется"}</strong></div>{checked && <div className="rs47-product-controls">{colorsList.length > 1 && <div className="rs47-swatches" aria-label="Цвет">{colorsList.map((color) => <button type="button" key={color} className={activeColor === color ? "active" : ""} title={color} onClick={() => { setColors((current) => ({ ...current, [option.id]: color })); setSizes((current) => { const next = { ...current }; delete next[option.id]; return next; }); }}><i style={{ background: colorHex(color) }}/></button>)}</div>}{sizeList.length > 1 && <label className="rs47-size"><span>Размер</span><select value={activeSize} onChange={(event) => setSizes((current) => ({ ...current, [option.id]: event.target.value }))}>{sizeList.map((size) => <option key={size}>{size}</option>)}</select></label>}<div className="rs47-qty"><span>Количество</span><div><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))}>−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))}>+</button></div></div></div>}</article>;
      })}</div></section>;
    })}</section>

    <aside className="rs47-summary"><header><small>ВАШЕ РЕШЕНИЕ</small><h2>{solution.name}</h2></header><div className="rs47-summary-stats"><span>{active.length} позиций</span><span>{units} шт.</span></div><div className="rs47-summary-items">{active.slice(0, 5).map(({ option, row, quantity }) => <div key={option.id}><span><RemoteImage src={row.primary_image_url || "/images/image-placeholder.svg"} alt={option.title}/></span><p><b>{option.title}</b><small>{quantity} шт. · {row.color || option.collection}</small></p><strong>{money(rowPrice(row.price) * quantity)}</strong></div>)}{active.length > 5 && <small>Ещё {active.length - 5} позиций в составе</small>}</div><div className="rs47-summary-total"><span>Итого</span><strong>{money(total)}</strong></div><button type="button" className="rs47-add" disabled={!active.length || adding} onClick={add}>{adding ? "ДОБАВЛЯЕМ…" : `ДОБАВИТЬ ${units || ""} В КОРЗИНУ`}</button><button type="button" className={`rs47-summary-save ${saved ? "saved" : ""}`} onClick={save}>{saved ? "✓ СОХРАНЕНО" : "♡ СОХРАНИТЬ"}</button><p className="rs47-benefit">Бесплатная доставка от 15 000 ₽ · возврат 30 дней</p></aside></div>
  </main>
  {active.length > 0 && <div className="rs47-mobile-bar"><div><small>{active.length} позиций · {units} шт.</small><strong>{money(total)}</strong></div><button type="button" disabled={adding} onClick={add}>{adding ? "Добавляем…" : "В корзину"}</button></div>}
  <ReadyFooterV47/></div>;
}
