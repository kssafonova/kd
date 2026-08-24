"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import { buildSolutionCategories, deriveGuestOptions, pickOptionVariant, recommendedSlotQuantity } from "./table-solution-builder";
import type { ConstructorData, FinalConstructorData } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const peopleLabel = (value: number) => `${value} ${value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}`;

type HeaderIconName = "menu" | "pin" | "search" | "user" | "heart" | "bag" | "close" | "arrow";
function HeaderIcon({ name }: { name: HeaderIconName }) {
  const common = { fill: "none", stroke: "currentColor", strokeWidth: 1.5, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "menu") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 7h16M4 12h16M4 17h16"/></svg>;
  if (name === "pin") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>;
  if (name === "search") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.2"/><path d="m15 15 5 5"/></svg>;
  if (name === "user") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7" r="3.6"/><path d="M4.5 21c.8-4.2 3.3-6.3 7.5-6.3s6.7 2.1 7.5 6.3"/></svg>;
  if (name === "heart") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20.5 6.2c-2.1-2.3-5.9-1.8-8.5 1.3-2.6-3.1-6.4-3.6-8.5-1.3-2.2 2.5-1.4 6.6 1 9 2 2.2 4.6 4.5 7.5 6.5 2.9-2 5.5-4.3 7.5-6.5 2.4-2.4 3.2-6.5 1-9Z"/></svg>;
  if (name === "bag") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.2 8h15.6l-1.3 13H5.5L4.2 8Z"/><path d="M8.6 8V5.8a3.4 3.4 0 0 1 6.8 0V8"/></svg>;
  if (name === "close") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
}

function SolutionsHeader() {
  const [open, setOpen] = useState(false);
  return <>
    <header className="kd-solutions-site-header-v33">
      <div className="kd-solutions-site-header-left-v33">
        <button type="button" className="kd-solutions-header-icon-v33" onClick={() => setOpen(true)} aria-label="Открыть меню"><HeaderIcon name="menu"/></button>
        <Link className="kd-solutions-boutiques-v33" href="/"><HeaderIcon name="pin"/><span>Бутики</span></Link>
      </div>
      <Link className="kd-solutions-site-logo-v33" href="/">КУЛЬТУРА ДОМА</Link>
      <div className="kd-solutions-site-actions-v33">
        <Link href="/" aria-label="Поиск"><HeaderIcon name="search"/></Link>
        <Link href="/" aria-label="Профиль"><HeaderIcon name="user"/></Link>
        <Link href="/" aria-label="Избранное"><HeaderIcon name="heart"/></Link>
        <Link href="/?cart=open" aria-label="Корзина"><HeaderIcon name="bag"/></Link>
      </div>
    </header>

    {open && <div className="kd-solutions-menu-v33" role="dialog" aria-modal="true" aria-label="Навигация">
      <button className="kd-solutions-menu-backdrop-v33" type="button" onClick={() => setOpen(false)} aria-label="Закрыть меню"/>
      <aside>
        <header><button type="button" onClick={() => setOpen(false)} aria-label="Закрыть"><HeaderIcon name="close"/></button><Link href="/" onClick={() => setOpen(false)}>КУЛЬТУРА ДОМА</Link></header>
        <nav>
          <small>КАТАЛОГ</small>
          {["Новинки","Спальня","Кухня и столовая","Декор","Ванная","Одежда для дома"].map((item) => <Link href="/" onClick={() => setOpen(false)} key={item}><span>{item}</span><HeaderIcon name="arrow"/></Link>)}
          <small>EDITORIAL</small>
          <Link href="/" onClick={() => setOpen(false)}><span>Капсулы и коллекции</span><HeaderIcon name="arrow"/></Link>
          <Link className="active" href="/constructor/" onClick={() => setOpen(false)}><span>Готовые решения</span><HeaderIcon name="arrow"/></Link>
          <small>СЕРВИС</small>
          {["Идеи подарков","Доставка и оплата","Возврат","Бутики"].map((item) => <Link href="/" onClick={() => setOpen(false)} key={item}><span>{item}</span><HeaderIcon name="arrow"/></Link>)}
        </nav>
      </aside>
    </div>}
  </>;
}

function SolutionsFooter() {
  const [email, setEmail] = useState("");
  const [done, setDone] = useState(false);
  return <footer className="kd-solutions-footer-v33">
    <div className="kd-solutions-footer-main-v33">
      <section className="kd-solutions-footer-news-v33">
        <Link href="/">КУЛЬТУРА ДОМА</Link>
        <h2>Новые коллекции и истории для дома</h2>
        <p>Подпишитесь на письма о новых коллекциях, капсулах и специальных предложениях.</p>
        <form onSubmit={(event) => { event.preventDefault(); if (email.trim()) setDone(true); }}>
          <input type="email" required value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Ваш email" aria-label="Email"/>
          <button type="submit" aria-label="Подписаться">{done ? "✓" : "→"}</button>
        </form>
        {done && <small>Спасибо. Вы подписаны.</small>}
      </section>
      <nav className="kd-solutions-footer-links-v33" aria-label="Ссылки в подвале">
        <div><p>ПОКУПАТЕЛЯМ</p><Link href="/">Каталог</Link><Link href="/constructor/">Готовые решения</Link><Link href="/">Доставка и оплата</Link><Link href="/">Возврат</Link></div>
        <div><p>О БРЕНДЕ</p><Link href="/">Капсулы и коллекции</Link><Link href="/">Наша история</Link><Link href="/">Бутики</Link></div>
        <div><p>СВЯЗАТЬСЯ</p><a href="tel:+78005553535">8 800 555-35-35</a><a href="mailto:hello@kultura-doma.ru">hello@kultura-doma.ru</a><span>Ежедневно · 10:00–22:00</span></div>
      </nav>
    </div>
    <div className="kd-solutions-footer-bottom-v33"><span>© 2026 Культура дома</span><span>Политика конфиденциальности</span><span>Россия</span></div>
  </footer>;
}

export function ConstructorLanding() {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [ruleData, setRuleData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [space, setSpace] = useState("Все");
  const [people, setPeople] = useState(0);

  useEffect(() => {
    let active = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([loaded, rules]) => {
        if (!active) return;
        setData(loaded);
        setRuleData(rules);
      })
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решения"));
    return () => { active = false; };
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    return TABLE_SOLUTIONS.map((solution) => {
      const catalogRows = resolveTableSolutionCatalogRows(data.catalog, solution);
      const guestOptions = deriveGuestOptions(solution, ruleData);
      const targetPeople = people && guestOptions.includes(people) ? people : guestOptions[0] || 1;
      const categories = buildSolutionCategories(catalogRows, solution.space);
      const slots = categories.flatMap((category) => category.slots);
      const defaultRows = slots
        .map((slot) => {
          const option = slot.options[0];
          const row = option ? pickOptionVariant(option) : undefined;
          return row ? { row, quantity: recommendedSlotQuantity(slot, targetPeople) } : null;
        })
        .filter((item): item is { row: NonNullable<typeof item> extends { row: infer R } ? R : never; quantity: number } => Boolean(item));
      const price = defaultRows.reduce((sum, item) => sum + toPrice(item.row.price) * item.quantity, 0);
      const productCount = Array.from(new Set(catalogRows.map((row) => row.product_name))).length;
      return {
        ...solution,
        catalogRows,
        categories,
        slots,
        guestOptions,
        targetPeople,
        fallbackImage: catalogRows[0]?.primary_image_url || "/images/image-placeholder.svg",
        price,
        productCount,
      };
    });
  }, [data, ruleData, people]);

  const spaces = useMemo(() => ["Все", ...Array.from(new Set(TABLE_SOLUTIONS.map((item) => item.space)))], []);
  const availablePeople = useMemo(() => Array.from(new Set(cards.flatMap((card) => card.guestOptions))).sort((a, b) => a - b), [cards]);
  const visible = cards.filter((card) => (space === "Все" || card.space === space) && (!people || card.guestOptions.includes(people)));
  const heroCard = visible[0] || cards[0];

  if (error) return <><SolutionsHeader/><main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></div></main><SolutionsFooter/></>;
  if (!data) return <><SolutionsHeader/><main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем готовые решения…</div></main></>;

  return <div className="kd-solutions-page-v33">
    <SolutionsHeader/>
    <main className="kd-solutions-v33">
      <section className="kd-solutions-hero-v33">
        <div className="kd-solutions-hero-copy-v33">
          <small>ГОТОВЫЕ РЕШЕНИЯ · КУЛЬТУРА ДОМА</small>
          <h1>Дом, собранный в единую историю</h1>
          <p>Подборки для разных пространств, в которых предметы из нескольких коллекций уже сочетаются между собой. Выберите сценарий и настройте состав под себя.</p>
          <a href="#ready-solutions-grid">СМОТРЕТЬ РЕШЕНИЯ <HeaderIcon name="arrow"/></a>
        </div>
        <div className="kd-solutions-hero-media-v33">
          {heroCard && <RemoteImage src={heroCard.previewFile ? `/images/constructor/${heroCard.previewFile}` : heroCard.fallbackImage} fallbackSrc={heroCard.fallbackImage} alt={heroCard.name} loading="eager"/>}
          {heroCard && <span><small>{heroCard.space}</small><b>{heroCard.name}</b></span>}
        </div>
      </section>

      <section className="kd-solutions-tools-v33" aria-label="Подбор готового решения">
        <div className="kd-solutions-tool-v33">
          <span>Пространство</span>
          <div>{spaces.map((item) => <button type="button" key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}</div>
        </div>
        <div className="kd-solutions-tool-v33">
          <span>Количество персон</span>
          <div><button type="button" className={people === 0 ? "active" : ""} onClick={() => setPeople(0)}>Любое</button>{availablePeople.map((value) => <button type="button" key={value} className={people === value ? "active" : ""} onClick={() => setPeople(value)}>{value}</button>)}</div>
        </div>
        <strong>{visible.length} {visible.length === 1 ? "решение" : visible.length > 1 && visible.length < 5 ? "решения" : "решений"}</strong>
      </section>

      <section className="kd-solutions-heading-v33" id="ready-solutions-grid"><div><small>ПОДБОРКИ ДЛЯ ДОМА</small><h2>Выберите свою историю</h2></div><p>Каждое решение можно изменить: убрать ненужное, выбрать другую коллекцию, цвет, размер и количество.</p></section>

      {visible.length > 0 ? <section className="kd-solutions-grid-v33" aria-label="Готовые решения">
        {visible.map((card, index) => <Link className={`kd-solutions-card-v33 ${index === 0 ? "featured" : ""}`} href={`/constructor/${card.id}/`} key={card.id}>
          <div className="kd-solutions-card-media-v33"><RemoteImage src={card.previewFile ? `/images/constructor/${card.previewFile}` : card.fallbackImage} fallbackSrc={card.fallbackImage} alt={card.name} loading={index < 4 ? "eager" : "lazy"}/></div>
          <div className="kd-solutions-card-copy-v33">
            <small>{card.space}</small>
            <h3>{card.name}</h3>
            <p>{card.collections.length ? card.collections.join(" · ") : "Готовое сочетание предметов для дома"}</p>
            <dl><div><dt>Персон</dt><dd>{card.guestOptions.map((value) => value).join(" / ")}</dd></div><div><dt>Товаров</dt><dd>{card.productCount}</dd></div></dl>
            <div className="kd-solutions-card-bottom-v33"><strong>{card.price ? `от ${formatRub(card.price)}` : "Соберите состав"}</strong><span>СОБРАТЬ <HeaderIcon name="arrow"/></span></div>
          </div>
        </Link>)}
      </section> : <section className="kd-solutions-empty-v33"><h2>Нет точного совпадения</h2><p>Измените пространство или количество персон — состав каждого решения всё равно можно настроить вручную.</p><button type="button" onClick={() => { setSpace("Все"); setPeople(0); }}>ПОКАЗАТЬ ВСЕ</button></section>}

      <section className="kd-solutions-how-v33">
        <header><small>КАК ЭТО РАБОТАЕТ</small><h2>От идеи до готового пространства</h2></header>
        <div><article><b>01</b><h3>Выберите сценарий</h3><p>Начните с пространства и количества персон — мы покажем подходящие решения.</p></article><article><b>02</b><h3>Настройте состав</h3><p>Сравните товары по группам, выберите коллекции, цвета, размеры и количество.</p></article><article><b>03</b><h3>Добавьте всё сразу</h3><p>Готовый набор одной кнопкой переносится в корзину отдельными товарами.</p></article></div>
      </section>

      <section className="kd-solutions-editorial-note-v33">
        <div><small>КУЛЬТУРА ДОМА</small><h2>Современный русский дом без буквального декора</h2><p>Мы соединяем фактуру, цвет, традицию и современную форму так, чтобы вещи легко жили вместе и не требовали сложного подбора.</p></div>
        {heroCard && <div><RemoteImage src={heroCard.fallbackImage} alt="Культура Дома"/></div>}
      </section>
    </main>
    <SolutionsFooter/>
  </div>;
}
