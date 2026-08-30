"use client";

import { useEffect } from "react";

type ReadyCard={title:string;note:string;image:string};
type ReadyGroup={id:string;label:string;cards:ReadyCard[]};

const READY_GROUPS:ReadyGroup[]=[
  {
    id:"kitchen",
    label:"Кухня и столовая",
    cards:[
      {title:"Красные линии",note:"Акцентная сервировка и столовый текстиль",image:"/assets/images/3_stol_desktop.png"},
      {title:"Зелёный салон",note:"Спокойная композиция для ежедневного стола",image:"/assets/images/2stol.png"},
      {title:"Зимняя сказка",note:"Светлая сервировка с прохладными акцентами",image:"/assets/images/time-table.png"},
    ],
  },
  {
    id:"bed-living",
    label:"Спальня и гостиная",
    cards:[
      {title:"Зимняя сказка",note:"Постельное бельё, пледы и мягкие фактуры",image:"/assets/images/2_sleep_desktop.png"},
      {title:"Зелёный салон",note:"Текстиль и декор для спокойной гостиной",image:"/assets/images/green.jpeg"},
      {title:"Тёплый брутализм",note:"Глубокие оттенки и выразительные материалы",image:"/assets/images/1_new_desktop.png"},
    ],
  },
  {
    id:"office",
    label:"Кабинет",
    cards:[
      {title:"Тёплый брутализм",note:"Сдержанная композиция для рабочего пространства",image:"/assets/images/4dekor.png"},
      {title:"Зелёный салон",note:"Спокойный цвет и тактильные детали",image:"/assets/images/green.jpeg"},
      {title:"Красные линии",note:"Один выразительный акцент в нейтральном интерьере",image:"/assets/images/niti0.jpg"},
    ],
  },
];

const HERO_COPY=[
  {eyebrow:"НОВИНКИ",title:"Новое для дома"},
  {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой"},
  {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал"},
];

function base(){return process.env.NEXT_PUBLIC_BASE_PATH??""}
function asset(path:string){return `${base()}${path}`}

function simplifyHero(home:HTMLElement){
  if(home.dataset.home135Hero==="true")return;
  const slides=Array.from(home.querySelectorAll<HTMLElement>(".home134-hero-slide"));
  if(!slides.length)return;
  slides.forEach((slide,index)=>{
    const copy=HERO_COPY[index];
    if(!copy)return;
    const eyebrow=slide.querySelector<HTMLElement>(".home134-hero-copy small");
    const title=slide.querySelector<HTMLElement>(".home134-hero-copy h1");
    const button=slide.querySelector<HTMLButtonElement>("[data-hero-action]");
    if(eyebrow)eyebrow.textContent=copy.eyebrow;
    if(title)title.textContent=copy.title;
    slide.querySelector(".home134-hero-copy p")?.remove();
    if(button)button.innerHTML=`Смотреть <span aria-hidden="true">→</span>`;
  });
  home.querySelector(".home134-hero-count")?.remove();
  home.dataset.home135Hero="true";
}

function renderReadyCards(section:HTMLElement,group:ReadyGroup){
  const grid=section.querySelector<HTMLElement>(".home135-ready-grid");
  if(!grid)return;
  grid.innerHTML=group.cards.map(card=>`
    <a class="home135-ready-card" href="${base()}/ready-solutions/?space=${encodeURIComponent(group.id)}">
      <span class="home135-ready-media"><img src="${asset(card.image)}" alt="${card.title}" loading="lazy" decoding="async" /></span>
      <span class="home135-ready-copy"><strong>${card.title}</strong><small>${card.note}</small><em>Смотреть решение →</em></span>
    </a>`).join("");
  section.querySelectorAll<HTMLButtonElement>("[role=tab]").forEach(button=>{
    const selected=button.dataset.group===group.id;
    button.classList.toggle("is-active",selected);
    button.setAttribute("aria-selected",String(selected));
    button.tabIndex=selected?0:-1;
  });
}

function rebuildReadySolutions(section:HTMLElement){
  if(section.dataset.home135Ready==="true")return;
  section.dataset.home135Ready="true";
  section.innerHTML=`
    <header class="home134-section-head home135-ready-head">
      <div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2>Выберите пространство</h2></div>
      <p>Начните с комнаты — покажем готовые композиции, которые можно взять целиком или настроить под себя.</p>
    </header>
    <div class="home135-ready-tabs" role="tablist" aria-label="Пространства дома">
      ${READY_GROUPS.map((group,index)=>`<button type="button" role="tab" data-group="${group.id}" aria-selected="${index===0}" class="${index===0?"is-active":""}">${group.label}</button>`).join("")}
    </div>
    <div class="home135-ready-grid" aria-live="polite"></div>
    <a class="home135-ready-all" href="${base()}/ready-solutions/">Все готовые решения</a>`;

  const tabs=Array.from(section.querySelectorAll<HTMLButtonElement>("[role=tab]"));
  tabs.forEach((button,index)=>{
    button.addEventListener("click",()=>{
      const group=READY_GROUPS.find(item=>item.id===button.dataset.group);
      if(group)renderReadyCards(section,group);
    });
    button.addEventListener("keydown",event=>{
      if(event.key!=="ArrowLeft"&&event.key!=="ArrowRight")return;
      event.preventDefault();
      const direction=event.key==="ArrowRight"?1:-1;
      const next=(index+direction+tabs.length)%tabs.length;
      tabs[next]?.focus();
      tabs[next]?.click();
    });
  });
  renderReadyCards(section,READY_GROUPS[0]);
}

function createConstructor(){
  const section=document.createElement("section");
  section.className="home135-constructor";
  section.setAttribute("aria-labelledby","home135-constructor-title");
  section.innerHTML=`
    <div class="home135-constructor-media"><img src="${asset("/assets/images/green.jpeg")}" alt="Интерьер как основа для собственного готового решения" loading="lazy" decoding="async" /></div>
    <div class="home135-constructor-copy">
      <small>КОНСТРУКТОР</small>
      <h2 id="home135-constructor-title">Соберите решение под свой дом</h2>
      <p>Начните с готовой композиции и настройте её под себя: оставьте нужные предметы, замените детали и выберите количество.</p>
      <a href="${base()}/constructor/">Собрать своё решение <span aria-hidden="true">→</span></a>
    </div>`;
  return section;
}

function simplifyCapsules(home:HTMLElement){
  const section=home.querySelector<HTMLElement>(".home117-capsules");
  if(!section)return;
  section.classList.add("home135-capsules");
  const headerSmall=section.querySelector<HTMLElement>(".home117-section-head small");
  const title=section.querySelector<HTMLElement>(".home117-section-head h2");
  if(headerSmall)headerSmall.textContent="КАПСУЛЫ";
  if(title)title.textContent="Истории дома";
}

function enhance(){
  const home=document.querySelector<HTMLElement>(".view-home .home-v113");
  if(!home)return;
  simplifyHero(home);
  simplifyCapsules(home);

  const ready=home.querySelector<HTMLElement>(".home134-spaces");
  if(ready){
    rebuildReadySolutions(ready);
    if(!home.querySelector(".home135-constructor"))ready.insertAdjacentElement("afterend",createConstructor());
  }
}

export function HomePremiumV135Enhancer(){
  useEffect(()=>{
    enhance();
    const observer=new MutationObserver(enhance);
    observer.observe(document.body,{childList:true,subtree:true});
    return()=>observer.disconnect();
  },[]);
  return null;
}
