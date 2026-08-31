"use client";

import { useEffect, useState } from "react";

type MenuProps={
  onClose:()=>void;
  onCatalog:(category?:string)=>void;
  onNavigate:(path:string)=>void;
};

type MenuIconName="close"|"pin"|"arrow"|"chevron";

const CATALOG_SECTIONS=["Спальня","Кухня и столовая","Декор","Ванная","Одежда для дома","Идеи подарков","Аутлет"];
const SUBS:Record<string,string[]>={
  "РАСПРОДАЖА":["Смотреть все","Летнее предложение","До −35% на текстиль","До −30% на сервировку"],
  "Спальня":["Смотреть все","Комплекты постельного белья","Одеяла и подушки","Пледы и покрывала","Наволочки","Пододеяльники","Простыни","Наматрасники"],
  "Кухня и столовая":["Смотреть все","Блюда и тарелки","Салатники","Стаканы и бокалы","Графины","Чашки","Столовые приборы","Вазы и этажерки","Прочие предметы сервировки"],
  "Декор":["Смотреть все","Вазы","Свечи и ароматы","Декоративные подушки","Предметы интерьера"],
  "Ванная":["Смотреть все","Полотенца","Халаты","Коврики","Аксессуары для ванной"],
  "Одежда для дома":["Смотреть все","Сорочки","Пижамы","Халаты","Домашние костюмы"],
  "Идеи подарков":["Смотреть все","Для неё","Для него","Новоселье","Подарочный сертификат"],
  "Аутлет":["Смотреть все","Последний размер","Архив коллекций","До −50%"],
};
const CATALOG_MAP:Record<string,string>={
  "Спальня":"Постельное белье",
  "Кухня и столовая":"Посуда и сервировка",
  "Декор":"Декор для дома",
  "Ванная":"Все товары",
  "Одежда для дома":"Все товары",
  "РАСПРОДАЖА":"Все товары",
  "Идеи подарков":"Все товары",
  "Аутлет":"Все товары",
};
const SUBCATEGORY_MAP:Record<string,string>={
  "Комплекты постельного белья":"Постельное белье",
  "Пододеяльники":"Постельное белье",
  "Простыни":"Постельное белье",
  "Наматрасники":"Постельное белье",
  "Одеяла и подушки":"Пледы и подушки",
  "Пледы и покрывала":"Пледы и подушки",
  "Наволочки":"Пледы и подушки",
  "Блюда и тарелки":"Посуда и сервировка",
  "Салатники":"Посуда и сервировка",
  "Стаканы и бокалы":"Посуда и сервировка",
  "Графины":"Посуда и сервировка",
  "Чашки":"Посуда и сервировка",
  "Столовые приборы":"Посуда и сервировка",
};

function MenuIcon({name}:{name:MenuIconName}){
  const common={fill:"none",stroke:"currentColor",strokeWidth:1.45,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="close")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if(name==="pin")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if(name==="arrow")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m8 4 8 8-8 8"/></svg>;
}

export function SharedKulturaMenu({onClose,onCatalog,onNavigate}:MenuProps){
  const [current,setCurrent]=useState("");
  const list=SUBS[current]??[];

  useEffect(()=>{
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const keydown=(event:KeyboardEvent)=>{if(event.key==="Escape")onClose()};
    window.addEventListener("keydown",keydown);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",keydown)};
  },[onClose]);

  const openCatalog=(category?:string)=>{onClose();onCatalog(category)};
  const openRoute=(path:string)=>{onClose();onNavigate(path)};

  return <div className="overlay navigation-overlay" role="presentation">
    <button className="overlay-bg" onClick={onClose} aria-label="Закрыть меню"/>
    <aside className="menu-panel zara-menu premium-menu" role="dialog" aria-modal="true" aria-label="Меню Культура дома">
      <div className="menu-top">
        <button onClick={onClose} aria-label="Закрыть меню"><MenuIcon name="close"/></button>
        <span><MenuIcon name="pin"/> Бутики</span>
        <b>КУЛЬТУРА ДОМА</b>
      </div>
      <div className="menu-body">
        {!current?<div className="menu-first level-one premium-menu-root">
          <nav className="premium-menu-catalog" aria-label="Основные категории">
            <button className="premium-menu-new" onClick={()=>openCatalog("Все товары")}><span>НОВИНКИ</span><MenuIcon name="chevron"/></button>
            {CATALOG_SECTIONS.map(section=><button key={section} onClick={()=>setCurrent(section)}><span>{section}</span><MenuIcon name="chevron"/></button>)}
          </nav>

          <section className="premium-menu-editorial premium-menu-editorial-lower" aria-label="Капсулы и готовые решения">
            <small>ВДОХНОВЕНИЕ</small>
            <button onClick={()=>openRoute("/capsules/")}><span>КАПСУЛЫ</span></button>
            <button onClick={()=>openRoute("/ready-solutions/")}><span>ГОТОВЫЕ РЕШЕНИЯ</span></button>
          </section>
        </div>:<div className="menu-second level-two premium-menu-level-two" key={current}>
          <button className="menu-back" onClick={()=>setCurrent("")}><MenuIcon name="chevron"/><span>{current}</span></button>
          {list.map((item,index)=><button key={item} className={index===0?"view-all":""} onClick={()=>openCatalog(index===0?(CATALOG_MAP[current]??"Все товары"):(SUBCATEGORY_MAP[item]??CATALOG_MAP[current]??"Все товары"))}><span>{item}</span>{index===0&&<MenuIcon name="arrow"/>}</button>)}
          <div className="premium-menu-level-footer"><button onClick={()=>openCatalog(CATALOG_MAP[current]??"Все товары")}>ЛИДЕРЫ ПРОДАЖ</button></div>
        </div>}
      </div>
    </aside>
  </div>;
}
