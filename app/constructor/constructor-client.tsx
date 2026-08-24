"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS, type TableSolution } from "./table-solutions";
import type { CatalogRow, FinalConstructorData } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const normalize = (value: string) => value.trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/\s+/g, " ");

const findProduct = (catalog: CatalogRow[], name: string) => {
  const target = normalize(name);
  return catalog.find((row) => normalize(row.product_name) === target);
};

const representativeRows = (catalog: CatalogRow[], solution: TableSolution) => {
  const exact = solution.productNames
    .map((name) => findProduct(catalog, name))
    .filter((row): row is CatalogRow => Boolean(row));
  if (exact.length) return exact;

  const collectionNames = solution.collections.map(normalize);
  return catalog.filter((row) => {
    const collection = normalize(row.collection || "");
    const product = normalize(row.product_name || "");
    return collectionNames.some((name) => collection === name || product.includes(name));
  });
};

export function ConstructorLanding() {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [error, setError] = useState("");
  const [space, setSpace] = useState("Все");

  useEffect(() => {
    let active = true;
    loadFinalConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решения"));
    return () => { active = false; };
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    return TABLE_SOLUTIONS.map((solution) => {
      const rows = solution.productNames
        .map((name) => findProduct(data.catalog, name))
        .filter((row): row is CatalogRow => Boolean(row));
      const mediaRows = representativeRows(data.catalog, solution);
      return {
        ...solution,
        rows,
        fallbackImage: mediaRows[0]?.primary_image_url || "/images/image-placeholder.svg",
        price: rows.reduce((sum, row) => sum + toPrice(row.price), 0),
      };
    });
  }, [data]);

  const spaces = useMemo(() => ["Все", ...Array.from(new Set(TABLE_SOLUTIONS.map((item) => item.space)))], []);
  const visible = cards.filter((card) => space === "Все" || card.space === space);

  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем готовые решения…</div></main>;

  return (
    <main className="solution-simple-shell table-solutions-shell">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/">КУЛЬТУРА ДОМА</Link>
          <span>ГОТОВЫЕ РЕШЕНИЯ</span>
        </nav>

        <header className="solution-simple-heading table-solutions-heading">
          <small>ГОТОВЫЕ РЕШЕНИЯ</small>
          <h1>Решения для пространства</h1>
          <p>Сценарии собраны по таблице: пространство, коллекции и заданный состав товаров. Там, где состав в источнике не указан, мы не подменяем его случайными товарами.</p>
        </header>

        {spaces.length > 2 && <div className="solution-simple-filters" role="tablist" aria-label="Пространство">
          {spaces.map((item) => <button key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}
        </div>}

        <section className="solution-simple-grid table-solution-grid" aria-label="Готовые решения">
          {visible.map((card, index) => (
            <Link className="solution-simple-card table-solution-card" href={`/constructor/${card.id}/`} key={card.id}>
              <div className="solution-simple-card-media table-solution-card-media">
                <RemoteImage
                  src={`/images/ready-solutions/${card.previewFile}`}
                  fallbackSrc={card.fallbackImage}
                  alt={card.name}
                  loading={index < 4 ? "eager" : "lazy"}
                />
                <span className="table-solution-number">{String(card.sourceId).padStart(2, "0")}</span>
              </div>
              <div className="solution-simple-card-copy table-solution-card-copy">
                <small>{card.space}</small>
                <h2>{card.name}</h2>
                <div className="table-solution-collections" aria-label="Коллекции">
                  {card.collections.map((collection) => <span key={collection}>{collection}</span>)}
                </div>
                <div className="solution-simple-card-meta">
                  <span>{card.productNames.length ? `${card.productNames.length} товаров` : "Состав уточняется"}</span>
                  <strong>{card.price ? formatRub(card.price) : "—"}</strong>
                </div>
                <span className="solution-simple-card-cta">СМОТРЕТЬ РЕШЕНИЕ <b>→</b></span>
              </div>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}
