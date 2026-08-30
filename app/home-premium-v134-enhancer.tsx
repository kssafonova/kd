"use client";

import { useEffect } from "react";

type HeroSlide={eyebrow:string;title:string;text:string;desktop:string;mobile:string;cta:string};
type SpaceCard={title:string;note:string;image:string;space:string};
type FilmScene={label:string;desktop:string;mobile:string};

const HERO:HeroSlide[]=[
  {eyebrow:"НОВИНКИ",title:"Новые истории дома",text:"Предметы, которые собирают пространство в цельный образ — от спальни до сервировки.",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png",cta:"Смотреть новинки"},
  {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой",text:"Сатин, мягкий свет и спокойные оттенки для пространства, в котором хочется остаться.",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png",cta:"Перейти в спальню"},
  {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал",text:"Фарфор, текстиль и детали стола в современной культуре русского дома.",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png",cta:"Смотреть сервировку"},
];

const SPACES:SpaceCard[]=[
  {title:"Кухня и столовая",note:"Сервировка и текстиль",image:"/assets/images/2stol.png",space:"kitchen"},
  {title:"Гостиная",note:"Декор и мягкий текстиль",image:"/assets/images/1_new_desktop.png",space:"living"},
  {title:"Спальня",note:"Постельное бельё и детали",image:"/assets/images/1spal.png",space:"bedroom"},
  {title:"Ванная",note:"Текстиль для ежедневных ритуалов",image:"/assets/images/6van.png",space:"bathroom"},
];

const FILM_SCENES:FilmScene[]=[
  {label:"Традиция",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png"},
  {label:"Дом",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png"},
  {label:"Ритуалы",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png"},
  {label:"Культура дома",desktop:"/assets/images/4dekor.png",mobile:"/assets/images/4dekor.png"},
];

function base(){return process.env.NEXT_PUBLIC_BASE_PATH??""}
function asset(path:string){return `${base()}${path}`}

function createHero(source:HTMLElement){
  const section=document.createElement("section");
  section.className="home134-hero";
  section.setAttribute("aria-label","Главные истории");
  section.innerHTML=`
    <div class="home134-hero-rail">
      ${HERO.map((item,index)=>`
        <article class="home134-hero-slide" data-index="${index}">
          <picture>
            <source media="(max-width:700px)" srcset="${asset(item.mobile)}" />
            <img src="${asset(item.desktop)}" alt="${item.title}" loading="${index===0?"eager":"lazy"}" decoding="async" />
          </picture>
          <div class="home134-hero-shade"></div>
          <div class="home134-hero-copy">
            <small>${item.eyebrow}</small>
            <h1>${item.title}</h1>
            <p>${item.text}</p>
            <button type="button" data-hero-action="${index}">${item.cta}<span aria-hidden="true">→</span></button>
          </div>
        </article>`).join("")}
    </div>
    <div class="home134-hero-footer" aria-label="Навигация по баннерам">
      <div class="home134-hero-progress">${HERO.map((_,index)=>`<button type="button" data-hero-dot="${index}" class="${index===0?"is-active":""}" aria-label="Баннер ${index+1}"></button>`).join("")}</div>
      <span class="home134-hero-count"><b>01</b> / 03</span>
    </div>`;

  const rail=section.querySelector<HTMLElement>(".home134-hero-rail");
  const dots=Array.from(section.querySelectorAll<HTMLButtonElement>("[data-hero-dot]"));
  const count=section.querySelector<HTMLElement>(".home134-hero-count b");
  const sync=()=>{
    if(!rail)return;
    const index=Math.max(0,Math.min(HERO.length-1,Math.round(rail.scrollLeft/Math.max(1,rail.clientWidth))));
    dots.forEach((dot,dotIndex)=>dot.classList.toggle("is-active",dotIndex===index));
    if(count)count.textContent=String(index+1).padStart(2,"0");
  };
  rail?.addEventListener("scroll",sync,{passive:true});
  dots.forEach(dot=>dot.addEventListener("click",()=>{
    const index=Number(dot.dataset.heroDot??0);
    rail?.scrollTo({left:(rail?.clientWidth??0)*index,behavior:"smooth"});
  }));
  section.querySelectorAll<HTMLButtonElement>("[data-hero-action]").forEach(button=>button.addEventListener("click",()=>{
    const index=Number(button.dataset.heroAction??0);
    const sourceControls=source.querySelectorAll<HTMLButtonElement>(".home113-hero-controls button");
    sourceControls[index]?.click();
    window.setTimeout(()=>source.querySelector<HTMLButtonElement>(".home113-hero-copy button")?.click(),0);
  }));
  return section;
}

function createFilm(){
  const section=document.createElement("section");
  section.className="home134-brand-film";
  section.setAttribute("aria-labelledby","home134-film-title");
  section.innerHTML=`
    <header class="home134-section-head home134-film-head">
      <div><small>О БРЕНДЕ</small><h2 id="home134-film-title">Традиции в каждом доме</h2></div>
      <p>Короткая история о том, как орнамент, материал и домашние ритуалы становятся частью современного интерьера.</p>
    </header>
    <div class="home134-film-frame">
      <div class="home134-film-fallback" aria-hidden="true"></div>
      <video class="home134-brand-video home134-brand-video-desktop" muted autoplay loop playsinline preload="metadata" aria-label="История бренда Культура дома">
        <source src="${asset("/assets/video/kultura-brand-desktop.mp4")}" type="video/mp4" />
      </video>
      <video class="home134-brand-video home134-brand-video-mobile" muted autoplay loop playsinline preload="metadata" aria-label="История бренда Культура дома">
        <source src="${asset("/assets/video/kultura-brand-mobile.mp4")}" type="video/mp4" />
      </video>
      <div class="home134-film-mark"><span>КУЛЬТУРА ДОМА</span><b>00:24</b></div>
    </div>`;
  const fallback=section.querySelector<HTMLElement>(".home134-film-fallback");
  FILM_SCENES.forEach((scene,index)=>{
    const node=document.createElement("div");
    node.className="home134-film-scene";
    node.style.setProperty("--film-desktop",`url(\"${asset(scene.desktop)}\")`);
    node.style.setProperty("--film-mobile",`url(\"${asset(scene.mobile)}\")`);
    node.style.setProperty("--film-delay",`${index*6}s`);
    node.innerHTML=`<span>${scene.label}</span>`;
    fallback?.appendChild(node);
  });
  const frame=section.querySelector<HTMLElement>(".home134-film-frame");
  section.querySelectorAll<HTMLVideoElement>("video").forEach(video=>{
    const ready=()=>frame?.classList.add(video.classList.contains("home134-brand-video-mobile")?"has-mobile-video":"has-desktop-video");
    video.addEventListener("canplay",ready,{once:true});
    video.addEventListener("loadeddata",ready,{once:true});
  });
  return section;
}

function createSpaces(){
  const section=document.createElement("section");
  section.className="home134-spaces";
  section.setAttribute("aria-labelledby","home134-spaces-title");
  section.innerHTML=`
    <header class="home134-section-head">
      <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2 id="home134-spaces-title">Комната, которую не нужно собирать по частям</h2></div>
      <p>Выберите пространство — мы уже подобрали предметы, которые работают вместе.</p>
    </header>
    <div class="home134-space-grid">
      ${SPACES.map(item=>`
        <a class="home134-space-card" href="${base()}/ready-solutions/?space=${encodeURIComponent(item.space)}">
          <span class="home134-space-media"><img src="${asset(item.image)}" alt="${item.title}" loading="lazy" decoding="async" /></span>
          <span class="home134-space-copy"><strong>${item.title}</strong><small>${item.note}</small><em>Собрать комнату →</em></span>
        </a>`).join("")}
    </div>
    <a class="home134-spaces-all" href="${base()}/ready-solutions/">Все готовые решения</a>`;
  return section;
}

function createBoutiques(){
  const section=document.createElement("section");
  section.className="home134-boutiques";
  section.setAttribute("aria-labelledby","home134-boutiques-title");
  section.innerHTML=`
    <picture class="home134-boutiques-media">
      <source media="(max-width:700px)" srcset="${asset("/assets/images/1_new_mobile.png")}" />
      <img src="${asset("/assets/images/1_new_desktop.png")}" alt="Интерьер Культура дома" loading="lazy" decoding="async" />
    </picture>
    <div class="home134-boutiques-copy">
      <small>БУТИКИ</small><h2 id="home134-boutiques-title">Увидеть материалы вживую</h2>
      <p>Сравните оттенки и фактуры и соберите интерьер вместе с консультантом.</p>
      <button type="button" class="home134-boutiques-cta">Выбрать бутик →</button>
    </div>`;
  section.querySelector<HTMLButtonElement>(".home134-boutiques-cta")?.addEventListener("click",()=>document.querySelector<HTMLButtonElement>(".view-home>.header .boutiques")?.click());
  return section;
}

function enhance(){
  const home=document.querySelector<HTMLElement>(".view-home .home-v113");
  if(!home)return;

  home.querySelector(".home113-nav")?.classList.add("home134-hidden");
  home.querySelector(".home113-solutions")?.classList.add("home134-hidden");
  home.querySelector(".home-boutiques-map")?.classList.add("home134-hidden");

  const sourceHero=home.querySelector<HTMLElement>(".home113-hero");
  if(sourceHero){
    sourceHero.classList.add("home134-source-hero");
    if(!home.querySelector(".home134-hero"))sourceHero.insertAdjacentElement("beforebegin",createHero(sourceHero));
  }

  const products=home.querySelector<HTMLElement>(".home117-new-products");
  products?.classList.remove("home134-hidden");
  if(products&&!home.querySelector(".home134-brand-film"))products.insertAdjacentElement("afterend",createFilm());

  const capsules=home.querySelector<HTMLElement>(".home117-capsules");
  if(capsules&&!home.querySelector(".home134-spaces"))capsules.insertAdjacentElement("afterend",createSpaces());

  const spaces=home.querySelector<HTMLElement>(".home134-spaces");
  if(spaces&&!home.querySelector(".home134-boutiques"))spaces.insertAdjacentElement("afterend",createBoutiques());
}

export function HomePremiumV134Enhancer(){
  useEffect(()=>{
    enhance();
    const observer=new MutationObserver(enhance);
    observer.observe(document.body,{childList:true,subtree:true});
    return()=>observer.disconnect();
  },[]);
  return null;
}
