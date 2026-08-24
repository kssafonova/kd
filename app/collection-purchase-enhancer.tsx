"use client";

import { useEffect } from "react";

export function CollectionPurchaseEnhancer(){
  useEffect(()=>{
    const roots=()=>Array.from(document.querySelectorAll<HTMLElement>(".editorial-products"));

    const enhance=(root:HTMLElement)=>{
      if(root.dataset.purchaseEnhanced==="1")return;
      root.dataset.purchaseEnhanced="1";

      const head=root.querySelector<HTMLElement>(".editorial-products-head");
      const primary=head?.querySelector<HTMLButtonElement>(".primary.total-cta");
      const grid=root.querySelector<HTMLElement>(".product-grid");
      if(!head||!primary||!grid)return;

      const dock=document.createElement("div");
      dock.className="collection-purchase-dock";
      dock.innerHTML='<div class="collection-purchase-dock-copy"><small>ВАШ ВЫБОР</small><strong>Все предметы</strong></div><button type="button" class="collection-purchase-dock-cta"><span>ВЫБРАТЬ ТОВАРЫ</span><b></b></button>';
      root.appendChild(dock);

      const dockCopy=dock.querySelector<HTMLElement>(".collection-purchase-dock-copy strong");
      const dockButton=dock.querySelector<HTMLButtonElement>(".collection-purchase-dock-cta");
      const dockLabel=dockButton?.querySelector<HTMLElement>("span");
      const dockPrice=dockButton?.querySelector<HTMLElement>("b");

      const sync=()=>{
        const selection=root.classList.contains("selection-mode");
        const cards=Array.from(root.querySelectorAll<HTMLElement>(".selectable-product"));
        const selected=cards.filter(card=>card.classList.contains("selected"));
        const originalLabel=primary.querySelector<HTMLElement>("span")?.textContent?.trim()||"";
        const originalPrice=primary.querySelector<HTMLElement>("b")?.textContent?.trim()||"";
        const count=selection?selected.length:cards.length;
        const noun=count===1?"предмет":count>=2&&count<=4?"предмета":"предметов";
        if(dockCopy)dockCopy.textContent=selection?`${count} ${noun} выбрано`:`${cards.length} ${cards.length===1?"предмет":"предметов"} в образе`;
        if(dockLabel)dockLabel.textContent=selection?(originalLabel||"ДОБАВИТЬ В КОРЗИНУ"):"НАСТРОИТЬ И КУПИТЬ";
        if(dockPrice)dockPrice.textContent=originalPrice;
        if(dockButton)dockButton.disabled=primary.disabled;
        dock.classList.toggle("is-selection",selection);
      };

      dockButton?.addEventListener("click",()=>primary.click());

      primary.addEventListener("click",()=>{
        window.setTimeout(()=>{
          sync();
          if(root.classList.contains("selection-mode")&&window.matchMedia("(max-width: 760px)").matches){
            grid.scrollIntoView({behavior:"smooth",block:"start"});
          }
        },40);
      });

      root.addEventListener("change",()=>window.setTimeout(sync,0));
      root.addEventListener("click",event=>{
        const target=event.target as HTMLElement;
        if(target.closest(".product-selector")||target.closest(".selection-help button"))window.setTimeout(sync,0);
      });

      const observer=new MutationObserver(sync);
      observer.observe(root,{subtree:true,attributes:true,attributeFilter:["class","disabled"],childList:true,characterData:true});
      sync();
    };

    const scan=()=>roots().forEach(enhance);
    scan();
    const pageObserver=new MutationObserver(scan);
    pageObserver.observe(document.body,{subtree:true,childList:true});
    return()=>pageObserver.disconnect();
  },[]);
  return null;
}
