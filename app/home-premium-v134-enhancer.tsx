"use client";

import { useEffect } from "react";

type SpaceCard={title:string;note:string;image:string;space:string};
type FilmScene={label:string;desktop:string;mobile:string};

const SPACES:SpaceCard[]=[
  {title:"Кухня и столовая",note:"Сервировка, фарфор и столовый текстиль",image:"/assets/images/2stol.png",space:"kitchen"},
  {title:"Гостиная",note:"Декор, текстиль и предметы для отдыха",image:"/assets/images/1_new_desktop.png",space:"living"},
  {title:"Спальня",note:"Постельное бельё, пледы и подушки",image:"/assets/images/1spal.png",space:"bedroom"},
  {title:"Ванная",note:"Текстиль для ежедневных ритуалов",image:"/assets/images/6van.png",space:"bathroom"},
  {title:"Декор",note:"Акцентные предметы для всего дома",image:"/assets/images/4dekor.png",space:"decor"},
];

const FILM_SCENES:FilmScene[]=[
  {label:"Традиция",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png"},
  {label:"Дом",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png"},
  {label:"Ритуалы",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png"},
  {label:"Культура дома",desktop:"/assets/images/4dekor.png",mobile:"/assets/images/4dekor.png"},
];

function base(){return process.env.NEXT_PUBLIC_BASE_PATH??""}
function asset(path:string){return `${base()}${path}`}

function createFilm(){
  const section=document.createElement("section");
  section.className="home134-brand-film";
  section.setAttribute("aria-labelledby","home134-film-title");
  section.innerHTML=`
    <header class="home134-film-head">
      <small>О БРЕНДЕ</small>
      <h2 id="home134-film-title">Традиции в каждом доме</h2>
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
  const cards=SPACES.map(item=>`
    <a class="home134-space-card" href="${base()}/ready-solutions/?space=${encodeURIComponent(item.space)}">
      <span class="home134-space-media"><img src="${asset(item.image)}" alt="${item.title}" loading="lazy" decoding="async" /></span>
      <span class="home134-space-copy"><strong>${item.title}</strong><small>${item.note}</small><em>Смотреть решения →</em></span>
    </a>`).join("");
  section.innerHTML=`
    <header class="home134-section-head">
      <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2 id="home134-spaces-title">Соберите пространство целиком</h2></div>
      <a href="${base()}/ready-solutions/">Все решения</a>
    </header>
    <div class="home134-space-rail">${cards}</div>`;
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
      <small>БУТИКИ КУЛЬТУРА ДОМА</small>
      <h2 id="home134-boutiques-title">Увидеть дом вживую</h2>
      <p>Сравните оттенки, фактуры и сервировку в пространстве бутика. Консультант поможет собрать предметы в цельный интерьер.</p>
      <button type="button" class="home134-boutiques-cta">Выбрать бутик <span aria-hidden="true">→</span></button>
      <span class="home134-boutiques-meta">Адреса · часы работы · наличие</span>
    </div>`;
  section.querySelector<HTMLButtonElement>(".home134-boutiques-cta")?.addEventListener("click",()=>{
    document.querySelector<HTMLButtonElement>(".view-home>.header .boutiques")?.click();
  });
  return section;
}

function enhance(){
  const home=document.querySelector<HTMLElement>(".view-home .home-v113");
  if(!home)return;

  home.querySelector(".home113-nav")?.classList.add("home134-hidden");
  home.querySelector(".home117-new-products")?.classList.add("home134-hidden");
  home.querySelector(".home113-solutions")?.classList.add("home134-hidden");
  home.querySelector(".home-boutiques-map")?.classList.add("home134-hidden");

  const categories=home.querySelector<HTMLElement>(".home113-category-section");
  if(categories&&!home.querySelector(".home134-brand-film"))categories.insertAdjacentElement("afterend",createFilm());

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
