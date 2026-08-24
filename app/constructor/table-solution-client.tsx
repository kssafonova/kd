"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadFinalConstructorData } from "./data-client";
import { findTableSolution } from "./table-solutions";
import { resolveTableSolutionProducts } from "./table-solution-resolver";
import type { CatalogRow, FinalConstructorData } from "./types";

const CART_STORAGE_KEY = "kultura-cart";
const CART_ID_OFFSET = 920000;
const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;

const splitImages = (row?: CatalogRow) => Array.from(new Set([
  row?.primary_image_url,
  ...(row?.all_image_urls || "").split("|"),
].filter((value): value is string => Boolean(value))));

type SharedCartItem = {
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
  skus: Array<{
    id: string;
    article: string;
    productId: number;
    color: string;
    colorHex: string;
    size: string;
    material: string;
    composition: string;
    price: number;
    image: string;
    gallery: string[];
  }>;
};

const mergeIntoSharedCart = (items: SharedCartItem[]) => {
  let existing: SharedCartItem[] = [];
  try {
    const raw = localStorage.getItem(CART_STORAGE_KEY);
    if (raw) existing = JSON.parse(raw) as SharedCartItem[];
  } catch { existing = []; }

  const merged = [...existing];
  items.forEach((item) => {
    const index = merged.findIndex((entry) => entry.id === item.id && entry.selectedSize === item.selectedSize && entry.selectedColor === item.selectedColor);
    if (index >= 0) merged[index] = { ...merged[index], quantity: merged[index].quantity + item.quantity };
    else merged.push(item);
  });

  try { localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(merged)); } catch {}
};

export function TableSolutionDetail({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [redirecting, setRedirecting] = useState(false);

  useEffect(() => {
    let active = true;
    loadFinalConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решение"));
    return () => { active = false; };
  }, []);

  const productRows = useMemo(() => {
    if (!data || !solution) return [];
    return resolveTableSolutionProducts(data.catalog, solution);
  }, [data, solution]);

  if (!solution) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;
  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;

  const activeRows = productRows.filter((row) => selected[row.offer_id] !== false);
  const total = activeRows.reduce((sum, row) => sum + toPrice(row.price) * (quantity[row.offer_id] || 1), 0);
  const previewFallback = productRows[0]?.primary_image_url || "/images/image-placeholder.svg";
  const scrollFallback = productRows[1]?.primary_image_url || productRows[0]?.all_image_urls?.split("|")[1] || previewFallback;
  const previewSrc = solution.previewFile ? `/images/constructor/${solution.previewFile}` : previewFallback;
  const scrollSrc = solution.scrollFile ? `/images/constructor/${solution.scrollFile}` : scrollFallback;

  const addSolution = () => {
    const items: SharedCartItem[] = activeRows.map((row, index) => {
      const numericOffer = Number(String(row.offer_id).split("-")[0]) || index + 1;
      const productId = CART_ID_OFFSET + numericOffer;
      const skuId = `table-solution-${solution.sourceId}-${row.offer_id}`;
      const image = row.primary_image_url || "/images/image-placeholder.svg";
      const gallery = splitImages(row);
      const size = row.size || row.volume || "Стандартный";
      const price = toPrice(row.price);
      return {
        id: productId,
        name: row.product_name,
        note: `Из готового решения «${solution.name}»`,
        price,
        image,
        gallery,
        selectedColor: row.color || "",
        selectedSize: size,
        selectedSkuId: skuId,
        quantity: quantity[row.offer_id] || 1,
        skus: [{
          id: skuId,
          article: row.vendor_code || String(row.offer_id),
          productId,
          color: row.color || "",
          colorHex: "#d8d5cf",
          size,
          material: row.material || "",
          composition: "",
          price,
          image,
          gallery,
        }],
      };
    });

    if (!items.length) return;
    mergeIntoSharedCart(items);
    setRedirecting(true);
    window.setTimeout(() => {
      const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
      window.location.href = `${base}/?cart=open`;
    }, 450);
  };

  return (
    <main className="solution-simple-shell table-solution-detail-shell">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/constructor/">← ГОТОВЫЕ РЕШЕНИЯ</Link>
          <span>{solution.space}</span>
        </nav>

        <section className="table-solution-detail-hero">
          <div className="table-solution-hero-media">
            <RemoteImage src={previewSrc} fallbackSrc={previewFallback} alt={`${solution.name}: превью`} loading="eager"/>
            <RemoteImage src={scrollSrc} fallbackSrc={scrollFallback} alt={`${solution.name}: второй кадр`} loading="eager"/>
          </div>
          <div className="table-solution-hero-copy">
            <small>ГОТОВОЕ РЕШЕНИЕ · {solution.space.toUpperCase()}</small>
            <h1>{solution.name}</h1>
            {solution.collections.length > 0 && <div className="table-solution-collection-list">
              {solution.collections.map((collection) => <span key={collection}>{collection}</span>)}
            </div>}
            <p>Состав автоматически собран из CSV-каталога: включены все найденные товары указанных коллекций и позиции, явно перечисленные в таблице. Для каждого товара используется его реальное изображение из CSV.</p>
            <div className="table-solution-hero-total"><span>{activeRows.length} из {productRows.length} товаров выбрано</span><strong>{formatRub(total)}</strong></div>
          </div>
        </section>

        {productRows.length === 0 ? (
          <section className="table-solution-pending-composition">
            <div><small>СОСТАВ</small><h2>Товары не найдены в CSV</h2><p>Для этого решения в текущем каталоге не удалось найти позиции по указанным коллекциям или названиям.</p></div>
          </section>
        ) : (
          <div className="table-solution-buy-layout">
            <section className="table-solution-product-list">
              <header><div><small>СОСТАВ ИЗ CSV</small><h2>Все найденные товары</h2></div><p>Все позиции выбраны по умолчанию. Можно убрать лишние и изменить количество.</p></header>
              <div>
                {productRows.map((row) => {
                  const checked = selected[row.offer_id] !== false;
                  const q = quantity[row.offer_id] || 1;
                  return <article className={`table-solution-product ${checked ? "selected" : "disabled"}`} key={row.offer_id}>
                    <label className="table-solution-product-check"><input type="checkbox" checked={checked} onChange={(event) => setSelected((state) => ({ ...state, [row.offer_id]: event.target.checked }))}/><span/></label>
                    <div className="table-solution-product-media"><RemoteImage src={row.primary_image_url || "/images/image-placeholder.svg"} alt={row.product_name}/></div>
                    <div className="table-solution-product-copy">
                      <small>{row.collection || "Культура Дома"}</small>
                      <h3>{row.product_name}</h3>
                      <p>{[row.color && `Цвет: ${row.color}`, row.size && `Размер: ${row.size}`, row.volume && row.volume, row.material].filter(Boolean).join(" · ")}</p>
                      <div><strong>{toPrice(row.price) ? formatRub(toPrice(row.price)) : "Цена уточняется"}</strong>{checked && <div className="table-solution-qty"><button type="button" onClick={() => setQuantity((state) => ({ ...state, [row.offer_id]: Math.max(1, q - 1) }))}>−</button><span>{q}</span><button type="button" onClick={() => setQuantity((state) => ({ ...state, [row.offer_id]: q + 1 }))}>+</button></div>}</div>
                    </div>
                  </article>;
                })}
              </div>
            </section>

            <aside className="table-solution-purchase-card">
              <small>ВАШЕ РЕШЕНИЕ</small>
              <h2>{solution.name}</h2>
              <div><span>Выбрано</span><b>{activeRows.length} из {productRows.length}</b></div>
              <div className="table-solution-purchase-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong></div>
              <button type="button" disabled={!activeRows.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ"}</button>
              <p>Каждый товар добавится в обычную корзину отдельной позицией.</p>
            </aside>
          </div>
        )}
      </div>
    </main>
  );
}
