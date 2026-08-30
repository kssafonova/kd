"use client";

import { useEffect } from "react";

const GRID_KEY="kd-catalog-grid-v132";

export function CatalogTogasV132Enhancer(){
  useEffect(()=>{
    const getCatalog=()=>document.querySelector<HTMLElement>(".view-catalog .catalog-v123");

    const closeSort=()=>{
      document.querySelectorAll<HTMLElement>(".catalog-sort-popover-v132.is-open").forEach(popover=>popover.classList.remove("is-open"));
      document.querySelectorAll<HTMLButtonElement>(".catalog-sort-trigger-v132[aria-expanded='true']").forEach(button=>button.setAttribute("aria-expanded","false"));
    };

    const updateSortButton=(catalog:HTMLElement)=>{
      const select=catalog.querySelector<HTMLSelectElement>(".catalog-sort-v123 select");
      const button=catalog.querySelector<HTMLButtonElement>(".catalog-sort-trigger-v132");
      if(!select||!button)return;
      button.querySelector<HTMLElement>(".catalog-sort-current-v132")!.textContent=select.options[select.selectedIndex]?.textContent||"По популярности";
    };

    const buildSortMenu=(catalog:HTMLElement,popover:HTMLElement)=>{
      const select=catalog.querySelector<HTMLSelectElement>(".catalog-sort-v123 select");
      if(!select)return;
      popover.replaceChildren();
      Array.from(select.options).forEach(option=>{
        const row=document.createElement("button");
        row.type="button";
        row.className=`catalog-sort-option-v132${option.value===select.value?" is-selected":""}`;
        row.dataset.value=option.value;
        row.innerHTML=`<span class="catalog-sort-check-v132" aria-hidden="true">${option.value===select.value?"✓":""}</span><span>${option.textContent||""}</span>`;
        row.addEventListener("click",()=>{
          const currentSelect=catalog.querySelector<HTMLSelectElement>(".catalog-sort-v123 select");
          if(!currentSelect)return;
          currentSelect.value=option.value;
          currentSelect.dispatchEvent(new Event("change",{bubbles:true}));
          updateSortButton(catalog);
          closeSort();
        });
        popover.appendChild(row);
      });
    };

    const enhance=()=>{
      const catalog=getCatalog();
      if(!catalog)return;

      const filterLabel=catalog.querySelector<HTMLElement>(".catalog-filter-trigger-v123>span");
      if(filterLabel&&filterLabel.textContent!=="Фильтры")filterLabel.textContent="Фильтры";

      const tools=catalog.querySelector<HTMLElement>(".catalog-tools-v123");
      const nativeSort=catalog.querySelector<HTMLElement>(".catalog-sort-v123");
      const select=catalog.querySelector<HTMLSelectElement>(".catalog-sort-v123 select");
      if(!tools||!nativeSort||!select)return;
      nativeSort.classList.add("catalog-sort-native-v132");

      if(!tools.querySelector(".catalog-sort-trigger-v132")){
        const sortButton=document.createElement("button");
        sortButton.type="button";
        sortButton.className="catalog-sort-trigger-v132";
        sortButton.setAttribute("aria-haspopup","menu");
        sortButton.setAttribute("aria-expanded","false");
        sortButton.innerHTML='<span class="catalog-sort-icon-v132" aria-hidden="true">↕</span><span class="catalog-sort-copy-v132"><small>Сортировка</small><b class="catalog-sort-current-v132"></b></span><span class="catalog-sort-chevron-v132" aria-hidden="true">⌄</span>';
        nativeSort.insertAdjacentElement("afterend",sortButton);

        const popover=document.createElement("div");
        popover.className="catalog-sort-popover-v132";
        popover.setAttribute("role","menu");
        popover.setAttribute("aria-label","Сортировка товаров");
        tools.appendChild(popover);

        sortButton.addEventListener("click",event=>{
          event.preventDefault();
          event.stopPropagation();
          const opening=!popover.classList.contains("is-open");
          closeSort();
          if(opening){
            buildSortMenu(catalog,popover);
            popover.classList.add("is-open");
            sortButton.setAttribute("aria-expanded","true");
          }
        });
      }
      updateSortButton(catalog);

      if(!tools.querySelector(".catalog-view-switch-v132")){
        const group=document.createElement("div");
        group.className="catalog-view-switch-v132";
        group.setAttribute("role","group");
        group.setAttribute("aria-label","Вид каталога");
        group.innerHTML=`
          <button type="button" data-grid="2" aria-label="Две карточки в ряд"><span class="grid-icon-v132 grid-icon-compact-v132" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>
          <button type="button" data-grid="1" aria-label="Одна карточка в ряд"><span class="grid-icon-v132 grid-icon-large-v132" aria-hidden="true"><i></i></span></button>`;
        tools.appendChild(group);

        let stored="2";
        try{stored=window.localStorage.getItem(GRID_KEY)==="1"?"1":"2"}catch{}
        catalog.dataset.grid=stored;
        group.querySelectorAll<HTMLButtonElement>("button").forEach(button=>{
          const apply=()=>{
            const value=button.dataset.grid==="1"?"1":"2";
            catalog.dataset.grid=value;
            group.querySelectorAll<HTMLButtonElement>("button").forEach(item=>item.classList.toggle("is-active",item===button));
            try{window.localStorage.setItem(GRID_KEY,value)}catch{}
          };
          button.addEventListener("click",apply);
          button.classList.toggle("is-active",button.dataset.grid===stored);
        });
      }
    };

    const onDocumentClick=(event:MouseEvent)=>{
      const target=event.target as Element|null;
      if(!target?.closest(".catalog-sort-trigger-v132,.catalog-sort-popover-v132"))closeSort();
    };
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")closeSort()};
    const onPop=()=>window.setTimeout(enhance,0);

    const observer=new MutationObserver(enhance);
    observer.observe(document.body,{childList:true,subtree:true});
    document.addEventListener("click",onDocumentClick);
    document.addEventListener("keydown",onKey);
    window.addEventListener("popstate",onPop);
    enhance();

    return()=>{
      observer.disconnect();
      document.removeEventListener("click",onDocumentClick);
      document.removeEventListener("keydown",onKey);
      window.removeEventListener("popstate",onPop);
    };
  },[]);

  return null;
}
