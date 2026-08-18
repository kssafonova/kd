from pathlib import Path

PAGE = Path("app/page.tsx")
page = PAGE.read_text(encoding="utf-8")

start_token = "function Menu("
end_token = "\n\nfunction Search("

replacement = r'''function Menu({ current, setCurrent, close, go, openCatalog }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void }) {
  const catalogSections=["Спальня","Кухня и столовая","Декор","Ванная","Одежда для дома"];
  const subs:Record<string,string[]>={
    "РАСПРОДАЖА":["Смотреть все","Летнее предложение","До −35% на текстиль","До −30% на сервировку"],
    "Спальня":["Смотреть все","Комплекты постельного белья","Одеяла и подушки","Пледы и покрывала","Наволочки","Пододеяльники","Простыни","Наматрасники"],
    "Кухня и столовая":["Смотреть все","Блюда и тарелки","Салатники","Стаканы и бокалы","Графины","Чашки","Столовые приборы","Вазы и этажерки","Прочие предметы сервировки"],
    "Декор":["Смотреть все","Вазы","Свечи и ароматы","Декоративные подушки","Предметы интерьера"],
    "Ванная":["Смотреть все","Полотенца","Халаты","Коврики","Аксессуары для ванной"],
    "Одежда для дома":["Смотреть все","Сорочки","Пижамы","Халаты","Домашние костюмы"],
    "Идеи подарков":["Смотреть все","Для неё","Для него","Новоселье","Подарочный сертификат"],
    "Аутлет":["Смотреть все","Последний размер","Архив коллекций","До −50%"],
  };
  const list=subs[current]||[];
  const catalogMap:Record<string,string>={"Спальня":"Постельное бельё","Кухня и столовая":"Посуда и сервировка","Декор":"Пледы и подушки","Ванная":"Все товары","Одежда для дома":"Домашняя одежда","РАСПРОДАЖА":"Все товары","Идеи подарков":"Все товары","Аутлет":"Все товары"};
  const subcategoryMap:Record<string,string>={"Комплекты постельного белья":"Постельное бельё","Пододеяльники":"Постельное бельё","Простыни":"Постельное бельё","Наматрасники":"Постельное бельё","Одеяла и подушки":"Пледы и подушки","Пледы и покрывала":"Пледы и подушки","Наволочки":"Пледы и подушки","Блюда и тарелки":"Посуда и сервировка","Салатники":"Посуда и сервировка","Стаканы и бокалы":"Посуда и сервировка","Графины":"Посуда и сервировка","Чашки":"Посуда и сервировка","Столовые приборы":"Посуда и сервировка","Пижамы":"Домашняя одежда","Халаты":"Домашняя одежда","Домашние костюмы":"Домашняя одежда"};
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;

  return <div className="overlay navigation-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><aside className="menu-panel zara-menu premium-menu"><div className="menu-top"><button onClick={close} aria-label="Закрыть меню"><Icon name="close"/></button><span><Icon name="pin"/> Бутики</span><b>КУЛЬТУРА ДОМА</b></div><div className="menu-body">{!current?<div className="menu-first level-one premium-menu-root">
    <button className="premium-menu-new" onClick={()=>openCatalog("Все товары")}><span>НОВИНКИ</span><Icon name="arrow"/></button>

    <section className="premium-menu-editorial" aria-label="Editorial и готовые решения">
      <small>EDITORIAL</small>
      <button type="button" onClick={()=>go("collections")}><span>КАПСУЛЫ И КОЛЛЕКЦИИ</span><Icon name="arrow"/></button>
      <a href={constructorHref} onClick={close}><span>ГОТОВЫЕ РЕШЕНИЯ</span><Icon name="arrow"/></a>
    </section>

    <nav className="premium-menu-catalog" aria-label="Каталог">{catalogSections.map(x=><button key={x} onClick={()=>setCurrent(x)}><span>{x}</span><Icon name="chevron"/></button>)}</nav>

    <div className="premium-menu-service">
      <button onClick={()=>setCurrent("Идеи подарков")}><span>ИДЕИ ПОДАРКОВ</span><Icon name="chevron"/></button>
      <button className="premium-menu-certificate" onClick={()=>alert("Электронный сертификат доступен от 3 000 ₽")}><span>ПОДАРОЧНЫЙ СЕРТИФИКАТ</span></button>
    </div>

    <div className="premium-menu-commercial">
      <button className="sale" onClick={()=>setCurrent("РАСПРОДАЖА")}><span>РАСПРОДАЖА</span><Icon name="chevron"/></button>
      <button onClick={()=>setCurrent("Аутлет")}><span>АУТЛЕТ</span><Icon name="chevron"/></button>
    </div>
  </div>:<div className="menu-second level-two premium-menu-level-two" key={current}><button className="menu-back" onClick={()=>setCurrent("")}><Icon name="chevron"/><span>{current}</span></button>{list.map((x,i)=><button key={x} className={i===0?"view-all":""} onClick={()=>openCatalog(i===0?(catalogMap[current]??"Все товары"):(subcategoryMap[x]??catalogMap[current]??"Все товары"))}><span>{x}</span>{i===0&&<Icon name="arrow"/>}</button>)}<div className="premium-menu-level-footer"><button onClick={()=>openCatalog(catalogMap[current]??"Все товары")}>ЛИДЕРЫ ПРОДАЖ</button></div></div>}</div></aside></div>;
}'''

start = page.find(start_token)
end = page.find(end_token, start)
if start < 0 or end < 0:
    raise SystemExit("Menu component block not found")

page = page[:start] + replacement + page[end:]
PAGE.write_text(page, encoding="utf-8")
print("Applied Zara Home premium navigation menu")
