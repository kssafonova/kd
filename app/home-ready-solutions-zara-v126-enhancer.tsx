"use client";

import { useEffect } from "react";

type Solution = {
  title: string;
  meta: string;
  copy: string;
  images: string[];
};

const SOLUTIONS: Solution[] = [
  {
    title: "Зелёный салон",
    meta: "ГОТОВОЕ РЕШЕНИЕ · ГОСТИНАЯ",
    copy: "Глубокие зелёные оттенки, натуральные ткани и благородные фактуры.",
    images: ["/assets/images/g1.jpeg"],
  },
  {
    title: "Зимняя сказка",
    meta: "ГОТОВОЕ РЕШЕНИЕ · ЗИМНЯЯ ИСТОРИЯ",
    copy: "Ледяные оттенки, мягкий свет и атмосфера спокойной зимы.",
    images: [
      "/assets/images/s1.png",
      "/assets/images/s2.png",
      "/assets/images/s3.jpg",
      "/assets/images/s4.png",
      "/assets/images/skazka5.jpg",
      "/assets/images/skazka41.png",
    ],
  },
  {
    title: "Красные линии",
    meta: "ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",
    copy: "Выразительные красные акценты в сдержанной и минималистичной гамме.",
    images: ["/assets/images/r1.jpeg", "/assets/images/r2.jpeg"],
  },
  {
    title: "Пламя морских глубин",
    meta: "ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",
    copy: "Глубокий синий, мерцающий свет и фактуры, вдохновлённые океаном.",
    images: ["/assets/images/p1.png", "/assets/images/p2.png", "/assets/images/p3.png"],
  },
  {
    title: "Тёплый брутализм",
    meta: "ГОТОВОЕ РЕШЕНИЕ · ИНТЕРЬЕР",
    copy: "Сочетание дерева, камня и кожи в тёплой палитре и лаконичном дизайне.",
    images: ["/assets/images/b1.png", "/assets/images/b2.png", "/assets/images/b3.png"],
  },
];

function asset(path: string) {
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  return `${base}${path}`;
}

function installStyles() {
  if (document.getElementById("home126-ready-solutions-style")) return;
  const style = document.createElement("style");
  style.id = "home126-ready-solutions-style";
  style.textContent = `
    .home-v113 .home113-solutions.home126-ready-solutions{
      width:100%!important;
      max-width:none!important;
      margin:0!important;
      padding:clamp(88px,9vw,148px) clamp(20px,4vw,64px) clamp(104px,11vw,168px)!important;
      background:#f7f5f0!important;
      color:#1d1d1b!important;
    }
    .home126-ready-head{
      display:grid!important;
      grid-template-columns:minmax(0,1fr) auto!important;
      gap:28px 48px!important;
      align-items:end!important;
      max-width:1540px!important;
      margin:0 auto clamp(38px,4vw,62px)!important;
    }
    .home126-ready-head-copy{max-width:760px!important}
    .home126-ready-head small{
      display:block!important;
      margin:0 0 18px!important;
      color:#6d6a64!important;
      font-size:9px!important;
      line-height:1.2!important;
      letter-spacing:.19em!important;
      text-transform:uppercase!important;
    }
    .home126-ready-head h2{
      margin:0!important;
      font-family:"Tenor Sans",Georgia,serif!important;
      font-size:clamp(44px,5.2vw,78px)!important;
      font-weight:400!important;
      line-height:.98!important;
      letter-spacing:-.035em!important;
    }
    .home126-ready-head p{
      max-width:610px!important;
      margin:22px 0 0!important;
      color:#69655f!important;
      font-size:clamp(12px,.95vw,14px)!important;
      line-height:1.7!important;
    }
    .home126-ready-all{
      position:relative!important;
      display:inline-flex!important;
      align-items:center!important;
      gap:28px!important;
      min-height:44px!important;
      padding:0 0 8px!important;
      color:#1d1d1b!important;
      font-size:11px!important;
      letter-spacing:.02em!important;
      text-decoration:none!important;
      white-space:nowrap!important;
      border-bottom:1px solid rgba(29,29,27,.48)!important;
    }
    .home126-ready-all span{font-size:17px!important;line-height:1!important}
    .home126-ready-rail{
      display:grid!important;
      grid-template-columns:repeat(5,minmax(250px,1fr))!important;
      gap:clamp(12px,1.4vw,24px)!important;
      max-width:1540px!important;
      margin:0 auto!important;
      overflow-x:auto!important;
      overflow-y:hidden!important;
      scroll-snap-type:x mandatory!important;
      scrollbar-width:none!important;
      overscroll-behavior-x:contain!important;
    }
    .home126-ready-rail::-webkit-scrollbar{display:none!important}
    .home126-ready-card{
      display:flex!important;
      flex-direction:column!important;
      min-width:0!important;
      background:#f7f5f0!important;
      scroll-snap-align:start!important;
    }
    .home126-ready-media{
      position:relative!important;
      display:grid!important;
      width:100%!important;
      aspect-ratio:4/5!important;
      gap:2px!important;
      overflow:hidden!important;
      background:#e7e2da!important;
    }
    .home126-ready-media[data-count="1"]{grid-template-columns:1fr!important;grid-template-rows:1fr!important}
    .home126-ready-media[data-count="2"]{grid-template-columns:1fr 1fr!important;grid-template-rows:1fr!important}
    .home126-ready-media[data-count="3"]{grid-template-columns:1.08fr .92fr!important;grid-template-rows:1fr 1fr!important}
    .home126-ready-media[data-count="3"] img:first-child{grid-row:1 / 3!important}
    .home126-ready-media[data-count="6"]{grid-template-columns:1fr 1fr!important;grid-template-rows:repeat(3,1fr)!important}
    .home126-ready-media img{
      display:block!important;
      width:100%!important;
      height:100%!important;
      min-width:0!important;
      min-height:0!important;
      object-fit:cover!important;
      object-position:center!important;
      background:#e7e2da!important;
      transform:scale(1.001)!important;
      transition:transform .7s cubic-bezier(.2,.65,.3,1)!important;
    }
    .home126-ready-card:hover .home126-ready-media img{transform:scale(1.018)!important}
    .home126-ready-copy{
      display:flex!important;
      flex-direction:column!important;
      min-height:230px!important;
      padding:18px 4px 0!important;
    }
    .home126-ready-copy small{
      color:#77736c!important;
      font-size:8px!important;
      letter-spacing:.14em!important;
      text-transform:uppercase!important;
    }
    .home126-ready-copy h3{
      margin:10px 0 10px!important;
      font-family:"Tenor Sans",Georgia,serif!important;
      font-size:clamp(23px,1.8vw,30px)!important;
      font-weight:400!important;
      line-height:1.08!important;
      letter-spacing:-.025em!important;
    }
    .home126-ready-copy p{
      margin:0!important;
      color:#6a665f!important;
      font-size:11px!important;
      line-height:1.65!important;
    }
    .home126-ready-link{
      display:inline-flex!important;
      align-items:center!important;
      gap:24px!important;
      align-self:flex-start!important;
      margin-top:auto!important;
      padding:22px 0 8px!important;
      color:#1d1d1b!important;
      font-size:10px!important;
      text-decoration:none!important;
      border-bottom:1px solid rgba(29,29,27,.45)!important;
    }
    .home126-ready-link span{font-size:15px!important;line-height:1!important}
    @media(max-width:1100px){
      .home126-ready-rail{
        display:flex!important;
        gap:16px!important;
      }
      .home126-ready-card{flex:0 0 min(58vw,420px)!important}
    }
    @media(max-width:700px){
      .home-v113 .home113-solutions.home126-ready-solutions{
        padding:72px 18px 90px!important;
      }
      .home126-ready-head{
        display:block!important;
        margin-bottom:30px!important;
      }
      .home126-ready-head h2{font-size:46px!important}
      .home126-ready-head p{margin-top:16px!important;font-size:12px!important}
      .home126-ready-all{margin-top:24px!important}
      .home126-ready-rail{
        margin-right:-18px!important;
        padding-right:18px!important;
      }
      .home126-ready-card{flex:0 0 min(82vw,360px)!important}
      .home126-ready-media{aspect-ratio:4/5!important}
      .home126-ready-copy{min-height:218px!important}
    }
  `;
  document.head.appendChild(style);
}

function escapeHtml(value: string) {
  return value.replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;",
  }[char] || char));
}

function installReadySolutions() {
  const section = document.querySelector<HTMLElement>(".home-v113 .home113-solutions");
  if (!section) return;
  installStyles();

  if (section.dataset.home126Ready === "1") return;

  const existingLinks = new Map<string, string>();
  section.querySelectorAll<HTMLElement>(".home113-solution").forEach((article) => {
    const title = article.querySelector("h3")?.textContent?.trim();
    const href = article.querySelector<HTMLAnchorElement>("a[href]")?.getAttribute("href");
    if (title && href) existingLinks.set(title, href);
  });

  const fallbackHref = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;
  const cards = SOLUTIONS.map((item) => {
    const href = existingLinks.get(item.title) || fallbackHref;
    const images = item.images.map((src, index) => `<img src="${asset(src)}" alt="${escapeHtml(item.title)}, фото ${index + 1}" loading="lazy" decoding="async" />`).join("");
    return `
      <article class="home126-ready-card">
        <a class="home126-ready-media" data-count="${item.images.length}" href="${escapeHtml(href)}" aria-label="Открыть готовое решение ${escapeHtml(item.title)}">
          ${images}
        </a>
        <div class="home126-ready-copy">
          <small>${escapeHtml(item.meta)}</small>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.copy)}</p>
          <a class="home126-ready-link" href="${escapeHtml(href)}">Собрать решение <span aria-hidden="true">→</span></a>
        </div>
      </article>`;
  }).join("");

  section.classList.add("home126-ready-solutions");
  section.innerHTML = `
    <header class="home126-ready-head">
      <div class="home126-ready-head-copy">
        <small>ГОТОВЫЕ РЕШЕНИЯ</small>
        <h2>Готовые решения</h2>
        <p>Выберите готовую композицию как отправную точку и настройте предметы под своё пространство.</p>
      </div>
      <a class="home126-ready-all" href="${fallbackHref}">Все готовые решения <span aria-hidden="true">→</span></a>
    </header>
    <div class="home126-ready-rail" aria-label="Готовые решения Культура дома">${cards}</div>`;
  section.dataset.home126Ready = "1";
}

export function HomeReadySolutionsZaraV126Enhancer() {
  useEffect(() => {
    installReadySolutions();
    const observer = new MutationObserver(() => installReadySolutions());
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);
  return null;
}
