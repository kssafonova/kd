(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,76460,e=>{"use strict";var t=e.i(71645);e.s(["ProductCardGalleryEnhancer",0,function(){return(0,t.useEffect)(()=>{let e=e=>{if("true"===e.dataset.cardGalleryEnhanced)return;let t=e.closest(".product-image");if(!t)return;let a=()=>Array.from(e.querySelectorAll(":scope > img"));if(a().length<2)return;e.dataset.cardGalleryEnhanced="true",t.classList.add("product-image-gallery");let r=document.createElement("div");r.className="product-card-gallery-nav product-card-gallery-prev",r.setAttribute("aria-hidden","true");let i=document.createElement("div");i.className="product-card-gallery-nav product-card-gallery-next",i.setAttribute("aria-hidden","true");let s=document.createElement("div");s.className="product-card-gallery-dots",s.setAttribute("aria-hidden","true"),t.append(r,i,s);let n=0,l=0,o=!1,d=!1,c=0,m=0,u=0,p=e=>Math.max(0,Math.min(a().length-1,e)),h=()=>{let e=a().length;s.replaceChildren(...Array.from({length:e},(e,t)=>{let a=document.createElement("i");return a.className=`product-card-gallery-dot${t===n?" active":""}`,a})),r.classList.toggle("is-disabled",n<=0),i.classList.toggle("is-disabled",n>=e-1)},g=()=>{let t=e.clientWidth||1,a=p(Math.round(e.scrollLeft/t));a!==n&&(n=a,h())},f=()=>{l&&cancelAnimationFrame(l),l=requestAnimationFrame(g)},y=(t,r="smooth")=>{let i=a(),s=p(t),l=i[s];l&&(n=s,h(),e.scrollTo({left:l.offsetLeft,top:0,behavior:r}))},v=e=>{e.preventDefault(),e.stopPropagation()},x=a=>{if(o){o=!1,t.classList.remove("is-dragging");try{e.releasePointerCapture?.(a.pointerId)}catch{}if(d){u=Date.now()+350;let t=e.clientWidth||1;y(Math.round(e.scrollLeft/t))}}},b=new MutationObserver(()=>{n=p(n),h(),f()});r.addEventListener("pointerdown",v),i.addEventListener("pointerdown",v),r.addEventListener("click",e=>{v(e),y(n-1)}),i.addEventListener("click",e=>{v(e),y(n+1)}),t.addEventListener("keydown",e=>{"ArrowLeft"===e.key&&(e.preventDefault(),e.stopPropagation(),y(n-1)),"ArrowRight"===e.key&&(e.preventDefault(),e.stopPropagation(),y(n+1))}),e.addEventListener("scroll",f,{passive:!0}),e.addEventListener("pointerdown",a=>{"mouse"===a.pointerType&&0===a.button&&(o=!0,d=!1,c=a.clientX,m=e.scrollLeft,e.setPointerCapture?.(a.pointerId),t.classList.add("is-dragging"))}),e.addEventListener("pointermove",t=>{if(!o)return;let a=t.clientX-c;Math.abs(a)>4&&(d=!0),d&&(t.preventDefault(),e.scrollLeft=m-a)}),e.addEventListener("pointerup",x),e.addEventListener("pointercancel",x),e.addEventListener("click",e=>{Date.now()<u&&v(e)},!0),b.observe(e,{childList:!0});let j="u">typeof ResizeObserver?new ResizeObserver(f):null;j?.observe(e),h(),f()},t=()=>{document.querySelectorAll(".product-card .product-image .product-media-scroll.horizontal-media.is-scrollable").forEach(e)};t();let a=new MutationObserver(t);return a.observe(document.body,{childList:!0,subtree:!0}),()=>{a.disconnect()}},[]),null}])},5366,e=>{"use strict";var t=e.i(71645);e.s(["CollectionPurchaseEnhancer",0,function(){return(0,t.useEffect)(()=>{let e=e=>{if("1"===e.dataset.purchaseEnhanced)return;e.dataset.purchaseEnhanced="1";let t=e.querySelector(".editorial-products-head"),a=t?.querySelector(".primary.total-cta"),r=e.querySelector(".product-grid");if(!t||!a||!r)return;let i=document.createElement("div");i.className="collection-purchase-dock",i.innerHTML='<div class="collection-purchase-dock-copy"><small>ВАШ ВЫБОР</small><strong>Все предметы</strong></div><button type="button" class="collection-purchase-dock-cta"><span>ВЫБРАТЬ ТОВАРЫ</span><b></b></button>',e.appendChild(i);let s=i.querySelector(".collection-purchase-dock-copy strong"),n=i.querySelector(".collection-purchase-dock-cta"),l=n?.querySelector("span"),o=n?.querySelector("b"),d=()=>{let t=e.classList.contains("selection-mode"),r=Array.from(e.querySelectorAll(".selectable-product")),d=r.filter(e=>e.classList.contains("selected")),c=a.querySelector("span")?.textContent?.trim()||"",m=a.querySelector("b")?.textContent?.trim()||"",u=t?d.length:r.length;s&&(s.textContent=t?`${u} ${1===u?"предмет":u>=2&&u<=4?"предмета":"предметов"} выбрано`:`${r.length} ${1===r.length?"предмет":"предметов"} в образе`),l&&(l.textContent=t?c||"ДОБАВИТЬ В КОРЗИНУ":"НАСТРОИТЬ И КУПИТЬ"),o&&(o.textContent=m),n&&(n.disabled=a.disabled),i.classList.toggle("is-selection",t)};n?.addEventListener("click",()=>a.click()),a.addEventListener("click",()=>{window.setTimeout(()=>{d(),e.classList.contains("selection-mode")&&window.matchMedia("(max-width: 760px)").matches&&r.scrollIntoView({behavior:"smooth",block:"start"})},40)}),e.addEventListener("change",()=>window.setTimeout(d,0)),e.addEventListener("click",e=>{let t=e.target;(t.closest(".product-selector")||t.closest(".selection-help button"))&&window.setTimeout(d,0)}),new MutationObserver(d).observe(e,{subtree:!0,attributes:!0,attributeFilter:["class","disabled"],childList:!0,characterData:!0}),d()},t=()=>Array.from(document.querySelectorAll(".editorial-products")).forEach(e);t();let a=new MutationObserver(t);return a.observe(document.body,{subtree:!0,childList:!0}),()=>a.disconnect()},[]),null}])},92453,e=>{"use strict";var t=e.i(71645);let a="kultura-address-book-v1",r=e=>`${e}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`,i=e=>String(e??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"),s=e=>{let t=e&&"object"==typeof e?e:{},a=Array.isArray(t.recipients)?t.recipients.map(e=>{let t=Array.isArray(e.addresses)?e.addresses.map(e=>({id:e.id||r("address"),label:e.label||"Адрес доставки",city:e.city||"Москва",address:e.address||"",flat:e.flat||"",comment:e.comment||""})):[],a=t.some(t=>t.id===e.defaultAddressId)?e.defaultAddressId:t[0]?.id;return{id:e.id||r("recipient"),name:e.name||"",surname:e.surname||"",phone:e.phone||"",email:e.email||"",addresses:t,defaultAddressId:a}}):[],i=a.some(e=>e.id===t.defaultRecipientId)?t.defaultRecipientId:a[0]?.id;return{version:1,recipients:a,defaultRecipientId:i}},n=()=>{try{let e=localStorage.getItem(a);if(e)return s(JSON.parse(e))}catch{}let e=(()=>{let e=(()=>{try{let e=localStorage.getItem("kultura-profile");return e?JSON.parse(e):null}catch{return null}})();if(!e)return{version:1,recipients:[]};let t=r("recipient"),a=r("address"),i=!!(e.city?.trim()||e.address?.trim());return{version:1,recipients:[{id:t,name:e.name??"",surname:e.surname??"",phone:e.phone??"",email:e.email??"",addresses:i?[{id:a,label:"Основной адрес",city:e.city||"Москва",address:e.address??"",flat:"",comment:""}]:[],defaultAddressId:i?a:void 0}],defaultRecipientId:t}})();try{localStorage.setItem(a,JSON.stringify(e))}catch{}return e},l=e=>{let t=s(e);try{localStorage.setItem(a,JSON.stringify(t))}catch{}window.dispatchEvent(new CustomEvent("kultura-address-book-change",{detail:t}))},o=e=>[e.name,e.surname].filter(Boolean).join(" ")||"Получатель",d=e=>[e.city,e.address,e.flat?`кв. ${e.flat}`:""].filter(Boolean).join(", "),c=(e,t)=>{if(!e)return;let a=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value")?.set;a?.call(e,t),e.dispatchEvent(new Event("input",{bubbles:!0})),e.dispatchEvent(new Event("change",{bubbles:!0}))};function m(e){if(e.querySelector("[data-address-book-root]"))return;e.classList.add("profile-book-enhanced");let t=document.createElement("section");t.dataset.addressBookRoot="true",t.className="profile-address-book";let a=e.querySelector(".account-fields");a?.insertAdjacentElement("afterend",t);let s=null,c=null,m=null,u=()=>{let e=n();t.innerHTML=`<div class="profile-book-heading">
      <div><small>ДОСТАВКА</small><h3>Получатели и адреса</h3><p>Сохраните несколько получателей и адресов, чтобы выбирать их при оформлении заказа.</p></div>
      <button type="button" data-add-recipient>+ ПОЛУЧАТЕЛЬ</button>
    </div>
    <div class="profile-book-list">
      ${e.recipients.length?e.recipients.map(t=>{let a=t.id===e.defaultRecipientId;return`<article class="profile-recipient-card ${a?"is-default":""}" data-recipient-id="${t.id}">
          <header>
            <div><span class="profile-recipient-avatar">${i((t.name||"П").slice(0,1).toUpperCase())}</span><div><strong>${i(o(t))}</strong><small>${i(t.phone||t.email||"Контакты не указаны")}</small></div></div>
            <button type="button" data-edit-recipient="${t.id}">ИЗМЕНИТЬ</button>
          </header>
          <div class="profile-recipient-actions">
            ${a?'<span class="profile-default-badge">ПОЛУЧАТЕЛЬ ПО УМОЛЧАНИЮ</span>':`<button type="button" data-default-recipient="${t.id}">Сделать основным</button>`}
            ${e.recipients.length>1?`<button type="button" class="danger" data-remove-recipient="${t.id}">Удалить</button>`:""}
          </div>
          <div class="profile-addresses">
            ${t.addresses.length?t.addresses.map(e=>{let a=e.id===t.defaultAddressId;return`<div class="profile-address-card ${a?"is-default":""}">
                <button type="button" class="profile-address-main" data-default-address="${t.id}|${e.id}">
                  <span class="profile-address-radio">${a?"✓":""}</span>
                  <span><strong>${i(e.label||"Адрес доставки")}</strong><small>${i(d(e))}</small>${e.comment?`<em>${i(e.comment)}</em>`:""}</span>
                </button>
                <div><button type="button" data-edit-address="${t.id}|${e.id}">Изменить</button><button type="button" data-remove-address="${t.id}|${e.id}">Удалить</button></div>
              </div>`}).join(""):'<p class="profile-address-empty">Адресов пока нет.</p>'}
            <button type="button" class="profile-add-address" data-add-address="${t.id}">+ ДОБАВИТЬ АДРЕС</button>
          </div>
        </article>`}).join(""):'<div class="profile-book-empty"><strong>Добавьте первого получателя</strong><span>Его контакты и адрес можно будет выбрать в checkout.</span></div>'}
    </div>
    ${(e=>{if(!s)return"";let t="new"===s?{id:"",name:"",surname:"",phone:"",email:"",addresses:[]}:e.recipients.find(e=>e.id===s);return t?`<form class="profile-book-editor" data-recipient-form>
      <div class="profile-book-editor-head"><strong>${"new"===s?"Новый получатель":"Редактировать получателя"}</strong><button type="button" data-cancel-recipient aria-label="Закрыть">\xd7</button></div>
      <div class="profile-book-fields">
        <label><span>Имя</span><input name="name" value="${i(t.name)}" required></label>
        <label><span>Фамилия</span><input name="surname" value="${i(t.surname)}"></label>
        <label><span>Телефон</span><input name="phone" type="tel" value="${i(t.phone)}" required></label>
        <label><span>Email</span><input name="email" type="email" value="${i(t.email)}"></label>
      </div>
      <button class="profile-book-save" type="submit">СОХРАНИТЬ ПОЛУЧАТЕЛЯ</button>
    </form>`:""})(e)}
    ${(e=>{if(!c)return"";let t=e.recipients.find(e=>e.id===c);if(!t)return"";let a=m&&"new"!==m?t.addresses.find(e=>e.id===m):void 0;return`<form class="profile-book-editor address-editor" data-address-form data-recipient-id="${t.id}">
      <div class="profile-book-editor-head"><strong>${a?"Редактировать адрес":"Новый адрес"}</strong><button type="button" data-cancel-address aria-label="Закрыть">\xd7</button></div>
      <div class="profile-book-fields address-fields">
        <label><span>Название</span><input name="label" value="${i(a?.label||"Дом")}" placeholder="Дом, Работа, Дача"></label>
        <label><span>Город</span><input name="city" value="${i(a?.city||"Москва")}" required></label>
        <label class="wide"><span>Улица и дом</span><input name="address" value="${i(a?.address)}" required></label>
        <label><span>Квартира / офис</span><input name="flat" value="${i(a?.flat)}"></label>
        <label><span>Комментарий курьеру</span><input name="comment" value="${i(a?.comment)}"></label>
      </div>
      <button class="profile-book-save" type="submit">СОХРАНИТЬ АДРЕС</button>
    </form>`})(e)}`};t.addEventListener("click",e=>{let t=e.target.closest("button");if(!t)return;let a=n();if(t.hasAttribute("data-add-recipient")){s="new",c=null,m=null,u();return}if(t.dataset.editRecipient){s=t.dataset.editRecipient,c=null,m=null,u();return}if(t.hasAttribute("data-cancel-recipient")){s=null,u();return}if(t.dataset.defaultRecipient){a.defaultRecipientId=t.dataset.defaultRecipient,l(a),u();return}if(t.dataset.removeRecipient){let e=t.dataset.removeRecipient;if(!window.confirm("Удалить получателя и его сохранённые адреса?"))return;a.recipients=a.recipients.filter(t=>t.id!==e),a.defaultRecipientId===e&&(a.defaultRecipientId=a.recipients[0]?.id),l(a),u();return}if(t.dataset.addAddress){c=t.dataset.addAddress,m="new",s=null,u();return}if(t.dataset.editAddress){let[e,a]=t.dataset.editAddress.split("|");c=e,m=a,s=null,u();return}if(t.hasAttribute("data-cancel-address")){c=null,m=null,u();return}if(t.dataset.defaultAddress){let[e,r]=t.dataset.defaultAddress.split("|"),i=a.recipients.find(t=>t.id===e);i&&(i.defaultAddressId=r),l(a),u();return}if(t.dataset.removeAddress){let[e,r]=t.dataset.removeAddress.split("|"),i=a.recipients.find(t=>t.id===e);if(!i)return;i.addresses=i.addresses.filter(e=>e.id!==r),i.defaultAddressId===r&&(i.defaultAddressId=i.addresses[0]?.id),l(a),u()}}),t.addEventListener("submit",e=>{e.preventDefault();let t=e.target,a=new FormData(t),i=n();if(t.matches("[data-recipient-form]")){let e={name:String(a.get("name")||"").trim(),surname:String(a.get("surname")||"").trim(),phone:String(a.get("phone")||"").trim(),email:String(a.get("email")||"").trim()};if(!e.name||!e.phone)return;if("new"===s){let t=r("recipient");i.recipients.push({id:t,...e,addresses:[]}),i.defaultRecipientId||(i.defaultRecipientId=t)}else{let t=i.recipients.find(e=>e.id===s);t&&Object.assign(t,e)}s=null,l(i),u();return}if(t.matches("[data-address-form]")){let e=t.dataset.recipientId,s=i.recipients.find(t=>t.id===e);if(!s)return;let n={label:String(a.get("label")||"Адрес доставки").trim()||"Адрес доставки",city:String(a.get("city")||"").trim(),address:String(a.get("address")||"").trim(),flat:String(a.get("flat")||"").trim(),comment:String(a.get("comment")||"").trim()};if(!n.city||!n.address)return;if("new"===m){let e=r("address");s.addresses.push({id:e,...n}),s.defaultAddressId||(s.defaultAddressId=e)}else{let e=s.addresses.find(e=>e.id===m);e&&Object.assign(e,n)}c=null,m=null,l(i),u()}}),u()}function u(e){let t=e.querySelector(".checkout-section"),a=t?.querySelector(".checkout-fields");if(!t||!a||t.querySelector("[data-checkout-address-book]"))return;let r=n();if(!r.recipients.length)return;let s=document.createElement("div");s.dataset.checkoutAddressBook="true",s.className="checkout-address-book",a.insertAdjacentElement("beforebegin",s);let l=r.defaultRecipientId||r.recipients[0].id,m=r.recipients.find(e=>e.id===l)?.defaultAddressId,u=(t=!1)=>{let a=n(),r=a.recipients.find(e=>e.id===l)||a.recipients[0];if(!r)return;l=r.id;let u=r.addresses.find(e=>e.id===m)||r.addresses.find(e=>e.id===r.defaultAddressId)||r.addresses[0];m=u?.id,s.innerHTML=`<div class="checkout-saved-head"><div><small>СОХРАНЁННЫЕ ДАННЫЕ</small><strong>Кому доставить?</strong></div><span>${a.recipients.length} получ.</span></div>
      <div class="checkout-recipient-tabs">${a.recipients.map(e=>`<button type="button" class="${e.id===l?"active":""}" data-checkout-recipient="${e.id}"><strong>${i(o(e))}</strong><small>${i(e.phone)}</small></button>`).join("")}</div>
      ${r.addresses.length?`<div class="checkout-address-tabs"><p>Адрес доставки</p>${r.addresses.map(e=>`<button type="button" class="${e.id===m?"active":""}" data-checkout-address="${e.id}"><span>${e.id===m?"✓":""}</span><b>${i(e.label)}</b><small>${i(d(e))}</small></button>`).join("")}</div>`:'<div class="checkout-no-address">Для этого получателя адрес ещё не сохранён — заполните его ниже.</div>'}`,t&&(c(e.querySelector('input[name="name"]'),r.name),c(e.querySelector('input[name="surname"]'),r.surname),c(e.querySelector('input[name="email"]'),r.email),c(e.querySelector('input[name="phone"]'),r.phone),u&&(c(e.querySelector('input[name="city"]'),u.city),c(e.querySelector('input[name="address"]'),u.address),c(e.querySelector('input[name="flat"]'),u.flat),c(e.querySelector('input[name="comment"]'),u.comment)))};s.addEventListener("click",e=>{let t=e.target.closest("button");if(t){if(t.dataset.checkoutRecipient){l=t.dataset.checkoutRecipient;let e=n().recipients.find(e=>e.id===l);m=e?.defaultAddressId||e?.addresses[0]?.id,u(!0);return}t.dataset.checkoutAddress&&(m=t.dataset.checkoutAddress,u(!0))}}),u(!0)}e.s(["ProfileAddressBookEnhancer",0,function(){return(0,t.useEffect)(()=>{let e=()=>{document.querySelectorAll(".auth-profile").forEach(m),document.querySelectorAll(".checkout-overlay").forEach(u)};e();let t=new MutationObserver(e);t.observe(document.body,{childList:!0,subtree:!0});let a=()=>{document.querySelectorAll(".checkout-overlay [data-checkout-address-book]").forEach(e=>e.remove()),e()};return window.addEventListener("kultura-address-book-change",a),()=>{t.disconnect(),window.removeEventListener("kultura-address-book-change",a)}},[]),null}])},94253,e=>{"use strict";var t=e.i(71645);let a=[{eyebrow:"КУЛЬТУРА ДОМА",title:"Традиции в современном доме",text:"Текстиль, сервировка и декор, собранные в спокойную цельную композицию.",image:"/assets/images/caps_luna_postel2.png",mobile:"/assets/images/caps_luna_postel.png",cta:"Смотреть коллекции",action:"collections"},{eyebrow:"ГОТОВЫЕ РЕШЕНИЯ",title:"Дом, который уже собран",text:"Выберите настроение и настройте состав, количество и коллекции под своё пространство.",image:"/assets/images/green.jpeg",mobile:"/assets/images/green.jpeg",cta:"Выбрать решение",action:"solutions"},{eyebrow:"СЕРВИРОВКА",title:"Предметы для ежедневных ритуалов",text:"Фарфор, стекло и текстиль работают вместе — как интерьер, а не как отдельные товары.",image:"/assets/images/time-table.png",mobile:"/assets/images/russian-service-blue.png",cta:"Смотреть посуду",action:"tableware"}],r={"Ледяные узоры":["/assets/images/caps_led_podyshka.png","/assets/images/caps_led_podyshka2.png","/assets/images/caps_led_serviz.png","/assets/images/caps_led.png"],"Лунная сказка":["/assets/images/caps_luna_postel.png","/assets/images/caps_luna_postel2.png","/assets/images/caps_luna_postel3.png","/assets/images/caps_luna_serviz.png","/assets/images/caps_luna_serviz2.png","/assets/images/caps_luna_serviz3.png"],Тайна:["/assets/images/tayna0.jpg","/assets/images/tayna1.jpg","/assets/images/tayna2.jpg"],Нити:["/assets/images/niti0.jpg","/assets/images/niti1.jpg"],Феникс:["/assets/images/feniks0.jpg","/assets/images/feniks1.jpg","/assets/images/feniks2.jpg"]};function i(e){return`/kd${e}`}function s(){return document.querySelector(".home-v81")}function n(e){if("solutions"===e){window.location.href="/kd/ready-solutions/";return}let t=s();if(t){if("collections"===e){let e=Array.from(t.querySelectorAll(".home81-nav button")).find(e=>e.textContent?.trim()==="Коллекции");e?.click();return}if("tableware"===e){let e=Array.from(t.querySelectorAll(".home81-categories button")).find(e=>e.textContent?.includes("Посуда и сервировка"));e?.click()}}}function l(e,t){let a=e.firstElementChild,r=a?Math.max(a.getBoundingClientRect().width+16,.72*e.clientWidth):.8*e.clientWidth;e.scrollBy({left:r*t,behavior:"smooth"})}function o(e,t,a){if(e.querySelector(".home87-rail-controls"))return;let r=document.createElement("div");r.className="home87-rail-controls",r.innerHTML=`<button type="button" aria-label="Назад: ${a}">←</button><button type="button" aria-label="Вперёд: ${a}">→</button>`;let[i,s]=Array.from(r.querySelectorAll("button"));i?.addEventListener("click",()=>l(t,-1)),s?.addEventListener("click",()=>l(t,1)),e.appendChild(r)}function d(){let e=document.querySelector(".home-v113 .home117-capsules");e&&(!function(){if(document.getElementById("home125-capsule-images"))return;let e=document.createElement("style");e.id="home125-capsule-images",e.textContent=`
    .home-v113 .home117-capsule-media.home125-capsule-media{
      position:relative!important;
      display:block!important;
      width:100%!important;
      aspect-ratio:4/5!important;
      padding:0!important;
      overflow:hidden!important;
      background:#f0eee9!important;
    }
    .home-v113 .home125-capsule-image-grid{
      display:grid!important;
      width:100%!important;
      height:100%!important;
      min-height:100%!important;
      gap:2px!important;
      overflow:hidden!important;
      background:#fff!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="2"]{
      grid-template-columns:1fr 1fr!important;
      grid-template-rows:1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="3"]{
      grid-template-columns:1.35fr .65fr!important;
      grid-template-rows:1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="3"] img:first-child{
      grid-row:1 / 3!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="4"]{
      grid-template-columns:1fr 1fr!important;
      grid-template-rows:1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="6"]{
      grid-template-columns:1fr 1fr 1fr!important;
      grid-template-rows:1fr 1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="6"] img:first-child{
      grid-column:1 / 3!important;
      grid-row:1 / 3!important;
    }
    .home-v113 .home125-capsule-image-grid img{
      display:block!important;
      width:100%!important;
      height:100%!important;
      min-width:0!important;
      min-height:0!important;
      object-fit:cover!important;
      object-position:center!important;
      background:#ece9e2!important;
      transform:scale(1.001);
      transition:transform .55s ease,opacity .3s ease!important;
    }
    @media(hover:hover){
      .home-v113 .home117-capsule-card:hover .home125-capsule-image-grid img{
        transform:scale(1.018);
      }
    }
    @media(max-width:700px){
      .home-v113 .home117-capsule-media.home125-capsule-media{
        aspect-ratio:3/4!important;
      }
      .home-v113 .home125-capsule-image-grid{
        gap:1px!important;
      }
    }
  `,document.head.appendChild(e)}(),e.querySelectorAll(".home117-capsule-card").forEach(e=>{let t=e.querySelector("h3")?.textContent?.trim()||"",a=r[t],s=e.querySelector(".home117-capsule-media");if(!a?.length||!s)return;let n=a.join("|");if(s.dataset.home125Images===n)return;let l=document.createElement("span");l.className="home125-capsule-image-grid",l.dataset.count=String(a.length),l.setAttribute("aria-hidden","true"),a.forEach((e,a)=>{let r=document.createElement("img");r.src=i(e),r.alt="",r.loading="lazy",r.decoding="async",r.dataset.capsuleImage=`${t}-${a+1}`,l.appendChild(r)}),s.replaceChildren(l),s.classList.add("home125-capsule-media"),s.dataset.home125Images=n}))}function c(){let e=s();!e||"1"===e.dataset.home87&&e.querySelector(".home87-hero")&&e.querySelector(".home87-brand-story")||(e.dataset.home87="1",function(e){let t=e.querySelector(".home81-hero");if(!t||e.querySelector(".home87-hero"))return;e.querySelector(".home86-banner-section")?.remove();let r=document.createElement("section");r.className="home87-hero",r.setAttribute("aria-label","Главные истории Культура Дома");let s=document.createElement("div");s.className="home87-hero-rail",a.forEach((e,t)=>{let a=document.createElement("article");a.className="home87-hero-slide",a.innerHTML=`
      <picture>
        <source media="(max-width: 700px)" srcset="${i(e.mobile)}" />
        <img src="${i(e.image)}" alt="${e.title}" loading="${0===t?"eager":"lazy"}" />
      </picture>
      <div class="home87-hero-shade"></div>
      <div class="home87-hero-copy">
        <small>${e.eyebrow}</small>
        <h1>${e.title}</h1>
        <p>${e.text}</p>
        <button type="button" data-home87-action="${e.action}">${e.cta}</button>
      </div>`,s.appendChild(a)});let o=document.createElement("div");o.className="home87-hero-footer",o.innerHTML=`<div class="home87-hero-progress">${a.map((e,t)=>`<button type="button" aria-label="${e.title}" data-home87-slide="${t}" class="${0===t?"is-active":""}"></button>`).join("")}</div><div class="home87-hero-arrows"><button type="button" aria-label="Предыдущий баннер">←</button><button type="button" aria-label="Следующий баннер">→</button></div>`,r.appendChild(s),r.appendChild(o),t.before(r),t.hidden=!0,r.querySelectorAll("[data-home87-action]").forEach(e=>{e.addEventListener("click",()=>n(e.dataset.home87Action||""))});let d=Array.from(r.querySelectorAll("[data-home87-slide]"));s.addEventListener("scroll",()=>{let e=Math.max(0,Math.min(a.length-1,Math.round(s.scrollLeft/Math.max(1,s.clientWidth))));d.forEach((t,a)=>t.classList.toggle("is-active",a===e))},{passive:!0}),d.forEach(e=>e.addEventListener("click",()=>{let t=Number(e.dataset.home87Slide||0);s.scrollTo({left:s.clientWidth*t,behavior:"smooth"})}));let c=Array.from(r.querySelectorAll(".home87-hero-arrows button"));c[0]?.addEventListener("click",()=>l(s,-1)),c[1]?.addEventListener("click",()=>l(s,1))}(e),function(e){let t=e.querySelector(".home81-collections");if(!t||e.querySelector(".home87-brand-story"))return;let a=document.createElement("section");a.className="home87-brand-story",a.innerHTML=`
    <div class="home87-brand-media"><img src="${i("/assets/images/russian-bedroom.png")}" alt="Современная интерпретация русских традиций в интерьере" loading="lazy" /></div>
    <div class="home87-brand-copy">
      <small>О БРЕНДЕ</small>
      <h2>Традиции познаются в доме</h2>
      <p>Культура Дома переводит русские художественные традиции в современный интерьер — через материал, орнамент, цвет и домашние ритуалы.</p>
      <button type="button" data-home87-action="collections">Смотреть истории</button>
    </div>`,t.before(a),a.querySelector("[data-home87-action]")?.addEventListener("click",()=>n("collections"))}(e),function(e){let t=e.querySelector(".home81-categories");if(t){let e=t.querySelector("header small"),a=t.querySelector("header h2"),r=t.querySelector("header p");e&&(e.textContent="КАТАЛОГ"),a&&(a.textContent="Для каждой зоны дома"),r&&(r.textContent="Быстрый вход в основные категории — без перегруженной навигации.")}let a=e.querySelector(".home81-collections");if(a){let e=a.querySelector(".home81-collections-hero > div"),t=a.querySelector(".home81-collections-hero small"),r=a.querySelector(".home81-collections-hero h2"),i=a.querySelector(".home81-collections-hero p"),s=a.querySelector(".home81-collection-rail");t&&(t.textContent="КОЛЛЕКЦИИ"),r&&(r.textContent="Коллекции для дома"),i&&(i.textContent="Редакционные истории, где цвет, орнамент и материал продолжаются от одного предмета к другому."),e&&s&&o(e,s,"Коллекции")}let r=e.querySelector(".home81-solutions");if(r){let e=r.querySelector("header"),t=r.querySelector("header small"),a=r.querySelector("header h2"),i=r.querySelector("header p"),s=r.querySelector(":scope > div");t&&(t.textContent="ГОТОВЫЕ РЕШЕНИЯ"),a&&(a.textContent="Готовые решения для вашего дома"),i&&(i.textContent="Выберите готовую композицию как отправную точку, а затем адаптируйте её под своё пространство."),e&&s&&o(e,s,"Готовые решения")}}(e))}e.s(["HomeZaraTogasV86Enhancer",0,function(){return(0,t.useEffect)(()=>{c(),d();let e=new MutationObserver(()=>{c(),d()});return e.observe(document.body,{childList:!0,subtree:!0}),()=>e.disconnect()},[]),null}])},580,e=>{"use strict";var t=e.i(71645);let a=[{title:"Зелёный салон",meta:"ГОТОВОЕ РЕШЕНИЕ · ГОСТИНАЯ",copy:"Глубокие зелёные оттенки, натуральные ткани и благородные фактуры.",images:["/assets/images/g1.jpeg"]},{title:"Зимняя сказка",meta:"ГОТОВОЕ РЕШЕНИЕ · ЗИМНЯЯ ИСТОРИЯ",copy:"Ледяные оттенки, мягкий свет и атмосфера спокойной зимы.",images:["/assets/images/s1.png","/assets/images/s2.png","/assets/images/s3.jpg","/assets/images/s4.png","/assets/images/skazka5.jpg","/assets/images/skazka41.png"]},{title:"Красные линии",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Выразительные красные акценты в сдержанной и минималистичной гамме.",images:["/assets/images/r1.jpeg","/assets/images/r2.jpeg"]},{title:"Пламя морских глубин",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Глубокий синий, мерцающий свет и фактуры, вдохновлённые океаном.",images:["/assets/images/p1.png","/assets/images/p2.png","/assets/images/p3.png"]},{title:"Тёплый брутализм",meta:"ГОТОВОЕ РЕШЕНИЕ · ИНТЕРЬЕР",copy:"Сочетание дерева, камня и кожи в тёплой палитре и лаконичном дизайне.",images:["/assets/images/b1.png","/assets/images/b2.png","/assets/images/b3.png"]}];function r(e){return e.replace(/[&<>'"]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[e]||e)}function i(){let e=document.querySelector(".home-v113 .home113-solutions");if(!e||(!function(){if(document.getElementById("home126-ready-solutions-style"))return;let e=document.createElement("style");e.id="home126-ready-solutions-style",e.textContent=`
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
  `,document.head.appendChild(e)}(),"1"===e.dataset.home126Ready))return;let t=new Map;e.querySelectorAll(".home113-solution").forEach(e=>{let a=e.querySelector("h3")?.textContent?.trim(),r=e.querySelector("a[href]")?.getAttribute("href");a&&r&&t.set(a,r)});let i="/kd/ready-solutions/",s=a.map(e=>{let a=t.get(e.title)||i,s=e.images.map((t,a)=>`<img src="/kd${t}" alt="${r(e.title)}, фото ${a+1}" loading="lazy" decoding="async" />`).join("");return`
      <article class="home126-ready-card">
        <a class="home126-ready-media" data-count="${e.images.length}" href="${r(a)}" aria-label="Открыть готовое решение ${r(e.title)}">
          ${s}
        </a>
        <div class="home126-ready-copy">
          <small>${r(e.meta)}</small>
          <h3>${r(e.title)}</h3>
          <p>${r(e.copy)}</p>
          <a class="home126-ready-link" href="${r(a)}">Собрать решение <span aria-hidden="true">→</span></a>
        </div>
      </article>`}).join("");e.classList.add("home126-ready-solutions"),e.innerHTML=`
    <header class="home126-ready-head">
      <div class="home126-ready-head-copy">
        <small>ГОТОВЫЕ РЕШЕНИЯ</small>
        <h2>Готовые решения</h2>
        <p>Выберите готовую композицию как отправную точку и настройте предметы под своё пространство.</p>
      </div>
      <a class="home126-ready-all" href="${i}">Все готовые решения <span aria-hidden="true">→</span></a>
    </header>
    <div class="home126-ready-rail" aria-label="Готовые решения Культура дома">${s}</div>`,e.dataset.home126Ready="1"}e.s(["HomeReadySolutionsZaraV126Enhancer",0,function(){return(0,t.useEffect)(()=>{i();let e=new MutationObserver(()=>i());return e.observe(document.body,{childList:!0,subtree:!0}),()=>e.disconnect()},[]),null}])},24069,e=>{"use strict";var t=e.i(43476),a=e.i(74080),r=e.i(71645);let i=e=>e?`${new Intl.NumberFormat("ru-RU").format(e)} ₽`:"цена уточняется",s=e=>String(e||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е"),n=e=>{let t=String(e||"").trim();return t&&"null"!==t.toLowerCase()?/^https?:\/\//i.test(t)?t:t.startsWith("/kd/")?`/kd${t.slice(3)}`:t.startsWith("/")?`/kd${t}`:`/kd/images/imported-products/${t}`:"/kd/assets/images/image-placeholder.svg"};function l(e,t){if(!e)return null;let a=e.querySelector(`:scope > #${t}`);return a||((a=document.createElement("div")).id=t,a.className="truth-commerce-root",e.appendChild(a)),e.classList.add("truth-commerce-replaced"),a}function o({src:e,alt:a}){let[i,s]=(0,r.useState)(n(e));return(0,r.useEffect)(()=>s(n(e)),[e]),(0,t.jsx)("img",{src:i,alt:a,loading:"lazy",onError:()=>s("/kd/assets/images/image-placeholder.svg")})}function d(e,t,a=1){let r=[];try{r=JSON.parse(localStorage.getItem("kultura-cart")||"[]")}catch{}let i=t.aroma||t.color||"Без цвета",s=t.size||t.volume||"Единый размер",l=`truth-${t.offerId||t.id}`,o={id:e.id,name:e.name,note:[t.collection,t.capsule,t.material].filter(Boolean).join(" · "),price:t.price,image:n(t.photos[0]),gallery:t.photos.slice(1).map(n),article:e.article,selectedColor:i,selectedSize:s,selectedSkuId:l,quantity:a,skus:[{id:l,article:t.article,productId:e.id,color:i,colorHex:"#d8d5cf",size:s,material:t.material,composition:t.composition,collection:t.collection,details:t.details,price:t.price,image:n(t.photos[0]),gallery:t.photos.slice(1).map(n),available:!0}]},c=r.findIndex(e=>e.id===o.id&&e.selectedColor===i&&e.selectedSize===s);c>=0?r[c]={...r[c],quantity:(r[c].quantity||1)+a}:r.push(o);try{localStorage.setItem("kultura-cart",JSON.stringify(r)),window.dispatchEvent(new Event("storage"))}catch{}}function c({p:e,open:a}){let r=e.variants.map(e=>e.price).filter(Boolean),s=r.length?Math.min(...r):0;return(0,t.jsxs)("article",{className:"truth-product-card",children:[(0,t.jsx)("button",{className:"truth-product-media",onClick:()=>a(e),children:(0,t.jsx)(o,{src:e.variants.find(e=>e.photos.length)?.photos[0],alt:e.name})}),(0,t.jsxs)("div",{className:"truth-product-copy",children:[(0,t.jsx)("small",{children:e.collections[0]||e.capsules[0]||e.category}),(0,t.jsx)("button",{onClick:()=>a(e),children:(0,t.jsx)("h3",{children:e.name})}),(0,t.jsx)("p",{children:[e.subcategory,e.variants[0]?.material].filter(Boolean).join(" · ")}),(0,t.jsxs)("div",{className:"truth-product-price",children:[(0,t.jsx)("strong",{children:s?`${r.some(e=>e!==s)?"от ":""}${i(s)}`:"цена уточняется"}),(0,t.jsxs)("span",{children:[e.variants.length," вар."]})]})]})]})}function m({p:e,close:a}){let[s,n]=(0,r.useState)(e.variants[0]?.variantKey||""),l=e.variants.find(e=>e.variantKey===s)||e.variants[0];if(!l)return null;let c=[["Артикул",l.article],["Offer ID",l.offerId],["Коллекция",l.collection],["Капсула",l.capsule],["Категория",l.category],["Подкатегория",l.subcategory],["Цвет",l.color],["Аромат",l.aroma],["Размер",l.size],["Высота",l.height],["Ширина",l.width],["Объём",l.volume],["Диаметр",l.diameter],["Комплектация",l.packageInfo],["Материал",l.material],["Состав",l.composition],["Детали",l.details]].filter(([,e])=>e);return(0,t.jsxs)("div",{className:"truth-modal-backdrop",children:[(0,t.jsx)("button",{className:"truth-modal-dismiss",onClick:a}),(0,t.jsxs)("section",{className:"truth-product-modal",children:[(0,t.jsxs)("header",{children:[(0,t.jsx)("button",{onClick:a,children:"← Назад"}),(0,t.jsx)("strong",{children:"КУЛЬТУРА ДОМА"}),(0,t.jsx)("button",{onClick:a,children:"×"})]}),(0,t.jsxs)("div",{className:"truth-modal-grid",children:[(0,t.jsx)("div",{className:"truth-modal-gallery",children:(l.photos.length?l.photos:[""]).map((a,r)=>(0,t.jsx)(o,{src:a,alt:`${e.name} ${r+1}`},r))}),(0,t.jsxs)("aside",{className:"truth-modal-info",children:[(0,t.jsx)("small",{children:l.collection||l.capsule||l.category}),(0,t.jsx)("h1",{children:e.name}),(0,t.jsxs)("div",{className:"truth-modal-price",children:[(0,t.jsx)("strong",{children:i(l.price)}),l.oldPrice&&l.oldPrice>l.price?(0,t.jsx)("del",{children:i(l.oldPrice)}):null]}),e.variants.length>1?(0,t.jsxs)("label",{className:"truth-variant-select",children:[(0,t.jsx)("span",{children:"Вариант"}),(0,t.jsx)("select",{value:s,onChange:e=>n(e.target.value),children:e.variants.map(e=>(0,t.jsxs)("option",{value:e.variantKey,children:[[e.color,e.aroma,e.size||e.volume].filter(Boolean).join(" · ")," — ",i(e.price)]},e.variantKey))})]}):null,(0,t.jsx)("button",{className:"truth-add-cart",onClick:()=>{d(e,l),a()},children:"ДОБАВИТЬ В КОРЗИНУ"}),(0,t.jsx)("dl",{className:"truth-characteristics",children:c.map(([e,a])=>(0,t.jsxs)("div",{children:[(0,t.jsx)("dt",{children:e}),(0,t.jsx)("dd",{children:a})]},e))})]})]})]})]})}function u({d:e}){let[a,i]=(0,r.useState)("Все товары"),[n,l]=(0,r.useState)(""),[o,d]=(0,r.useState)(null),p=["Все товары",...Array.from(new Set(e.products.map(e=>e.category).filter(Boolean)))],h=e.products.filter(e=>("Все товары"===a||e.category===a)&&(!n||s(`${e.name} ${e.article} ${e.collections} ${e.capsules}`).includes(s(n))));return(0,t.jsxs)("div",{className:"truth-catalog-shell",children:[(0,t.jsx)("div",{className:"truth-crumbs",children:"Главная / Каталог"}),(0,t.jsxs)("section",{className:"truth-catalog-head",children:[(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:"КАТАЛОГ"}),(0,t.jsx)("h1",{children:a}),(0,t.jsx)("p",{children:"Товары, варианты, цены и связи — только из таблицы."})]}),(0,t.jsxs)("strong",{children:[h.length," из ",e.productCount]})]}),(0,t.jsxs)("div",{className:"truth-catalog-tools",children:[(0,t.jsx)("nav",{children:p.map(e=>(0,t.jsx)("button",{className:a===e?"is-active":"",onClick:()=>i(e),children:e},e))}),(0,t.jsx)("input",{value:n,onChange:e=>l(e.target.value),placeholder:"Поиск"})]}),(0,t.jsx)("div",{className:"truth-product-grid",children:h.map(e=>(0,t.jsx)(c,{p:e,open:d},e.key))}),o?(0,t.jsx)(m,{p:o,close:()=>d(null)}):null]})}function p({d:e}){let[a,i]=(0,r.useState)(null),[s,n]=(0,r.useState)(null),l=(0,r.useMemo)(()=>new Map(e.products.map(e=>[e.key,e])),[e]),d=a?a.productKeys.map(e=>l.get(e)).filter(e=>!!e):[];return(0,t.jsxs)("div",{className:"truth-collections-shell truth-capsules-shell",children:[(0,t.jsxs)("section",{className:"truth-collections-head",children:[(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:"КУЛЬТУРА ДОМА · EDITORIAL"}),(0,t.jsx)("h1",{children:"Капсулы"}),(0,t.jsx)("p",{children:"Редакционные истории для дома: каждая капсула объединяет предметы, материалы и настроение. Состав и связи синхронизированы с таблицей."})]}),(0,t.jsx)("strong",{children:e.capsules.length})]}),a?(0,t.jsxs)("section",{className:"truth-collection-detail",children:[(0,t.jsxs)("header",{children:[(0,t.jsx)("button",{onClick:()=>i(null),children:"← Все капсулы"}),(0,t.jsx)("small",{children:"КАПСУЛА"}),(0,t.jsx)("h1",{children:a.name})]}),(0,t.jsx)("div",{className:"truth-product-grid",children:d.map(e=>(0,t.jsx)(c,{p:e,open:n},e.key))})]}):(0,t.jsx)("div",{className:"truth-entity-grid",children:e.capsules.map(e=>(0,t.jsxs)("article",{children:[(0,t.jsx)("button",{className:"truth-entity-media",onClick:()=>i(e),children:(0,t.jsx)(o,{src:e.heroImage,alt:e.name})}),(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:"КАПСУЛА"}),(0,t.jsx)("button",{onClick:()=>i(e),children:(0,t.jsx)("h2",{children:e.name})}),(0,t.jsxs)("p",{children:[e.productKeys.length," товаров · ",e.variantCount," вариантов"]})]})]},e.name))}),s?(0,t.jsx)(m,{p:s,close:()=>n(null)}):null]})}function h(e,t){let a=new Map(e.products.map(e=>[e.key,e]));return{req:t.requiredProductKeys.map(e=>a.get(e)).filter(e=>!!e),opt:t.optionalProductKeys.map(e=>a.get(e)).filter(e=>!!e&&!t.requiredProductKeys.includes(e.key))}}function g({d:e}){let[a,i]=(0,r.useState)(null),s=e.products.slice(0,8),n=e.capsules.slice(0,5),l=e.readySolutions.slice(0,5);return(0,t.jsxs)("div",{className:"truth-home",children:[(0,t.jsxs)("section",{className:"truth-home-hero",children:[(0,t.jsx)(o,{src:n[0]?.heroImage||s[0]?.variants[0]?.photos[0],alt:"Культура Дома"}),(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:"КУЛЬТУРА ДОМА · EDITORIAL"}),(0,t.jsx)("h1",{children:"Традиции в каждом доме"}),(0,t.jsx)("p",{children:"Современный взгляд на русский дом: текстиль, сервировка и декор, собранные в капсулы и готовые решения."}),(0,t.jsxs)("div",{children:[(0,t.jsx)("a",{href:"?section=collections",children:"Смотреть капсулы"}),(0,t.jsx)("a",{href:"/kd/ready-solutions/",children:"Готовые решения"})]})]})]}),(0,t.jsxs)("section",{className:"truth-home-section",children:[(0,t.jsxs)("header",{children:[(0,t.jsx)("small",{children:"КАПСУЛЫ"}),(0,t.jsx)("h2",{children:"Истории для дома"}),(0,t.jsx)("a",{href:"?section=collections",children:"Все капсулы"})]}),(0,t.jsx)("div",{className:"truth-home-capsules",children:n.map(e=>(0,t.jsxs)("a",{href:"?section=collections",children:[(0,t.jsx)("span",{children:(0,t.jsx)(o,{src:e.heroImage,alt:e.name})}),(0,t.jsx)("small",{children:"КАПСУЛА"}),(0,t.jsx)("strong",{children:e.name}),(0,t.jsxs)("em",{children:[e.productKeys.length," товаров"]})]},e.name))})]}),(0,t.jsxs)("section",{className:"truth-home-section",children:[(0,t.jsxs)("header",{children:[(0,t.jsx)("small",{children:"КАТАЛОГ"}),(0,t.jsx)("h2",{children:"Новые предметы"}),(0,t.jsx)("a",{href:"?section=catalog",children:"Весь каталог"})]}),(0,t.jsx)("div",{className:"truth-product-grid",children:s.map(e=>(0,t.jsx)(c,{p:e,open:i},e.key))})]}),(0,t.jsxs)("section",{className:"truth-home-section",children:[(0,t.jsxs)("header",{children:[(0,t.jsx)("small",{children:"ГОТОВЫЕ РЕШЕНИЯ"}),(0,t.jsx)("h2",{children:"Соберите пространство целиком"}),(0,t.jsx)("a",{href:"/kd/ready-solutions/",children:"Все решения"})]}),(0,t.jsx)("div",{className:"truth-home-solutions",children:l.map(e=>(0,t.jsxs)("a",{href:`/kd/ready-solutions/${f(e.name)}/`,children:[(0,t.jsx)("span",{children:(0,t.jsx)(o,{src:e.heroImage,alt:e.name})}),(0,t.jsx)("small",{children:e.space||"ГОТОВОЕ РЕШЕНИЕ"}),(0,t.jsx)("strong",{children:e.name}),(0,t.jsxs)("em",{children:[e.requiredProductKeys.length," обязательных · ",e.optionalProductKeys.length," опциональных"]})]},e.name))})]}),a?(0,t.jsx)(m,{p:a,close:()=>i(null)}):null]})}let f=e=>{let t=s(e);return"зеленый салон"===t?"green-salon":"красные линии"===t?"red-lines":"зимняя сказка"===t?"winter-fairy-tale":"пламя морских глубин"===t?"flame-of-sea-depths":"теплый брутализм"===t?"warm-brutalism":t.replace(/[^a-zа-я0-9]+/g,"-").replace(/^-+|-+$/g,"")};function y({d:e}){return(0,t.jsxs)("div",{className:"truth-solutions-shell",children:[(0,t.jsx)("div",{className:"truth-crumbs",children:"Главная / Готовые решения"}),(0,t.jsxs)("section",{className:"truth-solutions-head",children:[(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:"ГОТОВЫЕ РЕШЕНИЯ"}),(0,t.jsx)("h1",{children:"Готовые решения"}),(0,t.jsx)("p",{children:"Обязательные и опциональные товары — только по таблице."})]}),(0,t.jsx)("strong",{children:e.readySolutions.length})]}),(0,t.jsx)("div",{className:"truth-solution-grid",children:e.readySolutions.map(a=>{let{req:r,opt:i}=h(e,a);return(0,t.jsxs)("article",{className:"truth-solution-card",children:[(0,t.jsx)("a",{className:"truth-solution-media",href:`/kd/ready-solutions/${f(a.name)}/`,children:(0,t.jsx)(o,{src:a.heroImage,alt:a.name})}),(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:a.space}),(0,t.jsx)("a",{href:`/kd/ready-solutions/${f(a.name)}/`,children:(0,t.jsx)("h2",{children:a.name})}),(0,t.jsx)("p",{children:[...a.collections,...a.capsules].join(" · ")}),(0,t.jsxs)("div",{className:"truth-solution-counts",children:[(0,t.jsxs)("span",{children:[r.length," обязательных"]}),(0,t.jsxs)("span",{children:[i.length," опциональных"]})]}),(0,t.jsx)("a",{className:"truth-solution-cta",href:`/kd/ready-solutions/${f(a.name)}/`,children:"НАСТРОИТЬ →"})]})]},a.id)})})]})}function v({d:e,s:a}){let{req:s,opt:n}=(0,r.useMemo)(()=>h(e,a),[e,a]),l=(0,r.useMemo)(()=>[...s,...n],[s,n]),[c,u]=(0,r.useState)({}),[p,g]=(0,r.useState)(null);(0,r.useEffect)(()=>u(Object.fromEntries(l.map(e=>[e.key,{selected:s.some(t=>t.key===e.key),variantKey:e.variants[0]?.variantKey||"",quantity:1}]))),[a.id]);let f=l.flatMap(e=>{let t=c[e.key];if(!t?.selected)return[];let a=e.variants.find(e=>e.variantKey===t.variantKey)||e.variants[0];return a?[{p:e,v:a,q:Math.max(1,t.quantity||1)}]:[]}),y=(e,a,r)=>(0,t.jsxs)("section",{className:"truth-solution-group",children:[(0,t.jsxs)("header",{children:[(0,t.jsxs)("div",{children:[(0,t.jsx)("small",{children:r?"ОСНОВА":"ОПЦИОНАЛЬНО"}),(0,t.jsx)("h2",{children:e})]}),(0,t.jsx)("span",{children:a.length})]}),(0,t.jsx)("div",{className:"truth-solution-items",children:a.map(e=>{let a=c[e.key]||{selected:r,variantKey:e.variants[0]?.variantKey||"",quantity:1},s=e.variants.find(e=>e.variantKey===a.variantKey)||e.variants[0];return(0,t.jsxs)("article",{className:`truth-solution-item ${a.selected?"is-selected":""}`,children:[(0,t.jsx)("button",{className:"truth-solution-item-media",onClick:()=>g(e),children:(0,t.jsx)(o,{src:s?.photos[0],alt:e.name})}),(0,t.jsxs)("div",{className:"truth-solution-item-copy",children:[(0,t.jsxs)("label",{className:"truth-check",children:[(0,t.jsx)("input",{type:"checkbox",checked:a.selected,onChange:t=>u(r=>({...r,[e.key]:{...a,selected:t.target.checked}}))}),(0,t.jsx)("span",{children:r?"В решении":"Добавить"})]}),(0,t.jsx)("button",{onClick:()=>g(e),children:(0,t.jsx)("h3",{children:e.name})}),(0,t.jsx)("strong",{children:i(s?.price||0)}),e.variants.length>1?(0,t.jsx)("select",{value:a.variantKey,onChange:t=>u(r=>({...r,[e.key]:{...a,variantKey:t.target.value}})),children:e.variants.map(e=>(0,t.jsxs)("option",{value:e.variantKey,children:[[e.color,e.aroma,e.size||e.volume].filter(Boolean).join(" · ")," — ",i(e.price)]},e.variantKey))}):null,(0,t.jsxs)("label",{className:"truth-qty",children:[(0,t.jsx)("span",{children:"Количество"}),(0,t.jsx)("input",{type:"number",min:1,value:a.quantity,onChange:t=>u(r=>({...r,[e.key]:{...a,quantity:Math.max(1,Number(t.target.value)||1)}}))})]})]})]},e.key)})})]}),x=f.reduce((e,t)=>e+t.v.price*t.q,0);return(0,t.jsxs)("div",{className:"truth-solution-wizard",children:[(0,t.jsxs)("div",{className:"truth-crumbs",children:[(0,t.jsx)("a",{href:"/kd/",children:"Главная"})," / ",(0,t.jsx)("a",{href:"/kd/ready-solutions/",children:"Готовые решения"})," / ",a.name]}),(0,t.jsxs)("section",{className:"truth-solution-hero",children:[(0,t.jsx)("div",{children:(0,t.jsx)(o,{src:a.heroImage,alt:a.name})}),(0,t.jsxs)("aside",{children:[(0,t.jsxs)("small",{children:["ГОТОВОЕ РЕШЕНИЕ · ",a.space]}),(0,t.jsx)("h1",{children:a.name}),(0,t.jsx)("p",{children:"Состав, варианты, цены и связи синхронизированы с базой данных."}),(0,t.jsx)("div",{children:[...a.collections,...a.capsules].map(e=>(0,t.jsx)("span",{children:e},e))})]})]}),y("Обязательные товары",s,!0),n.length?y("Опциональные товары",n,!1):null,(0,t.jsxs)("footer",{className:"truth-solution-total",children:[(0,t.jsxs)("div",{children:[(0,t.jsxs)("span",{children:[f.length," позиций"]}),(0,t.jsx)("strong",{children:i(x)})]}),(0,t.jsx)("button",{disabled:!f.length,onClick:()=>f.forEach(e=>d(e.p,e.v,e.q)),children:"ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ"})]}),p?(0,t.jsx)(m,{p:p,close:()=>g(null)}):null]})}e.s(["TruthCommerceEnhancer",0,function(){let e=function(){let[e,t]=(0,r.useState)(null);return(0,r.useEffect)(()=>{let e=!0;return fetch("/kd/data/database/site_runtime.json",{cache:"no-store"}).then(async e=>{if(!e.ok)throw 0;return e.json()}).then(a=>{e&&t(a)}).catch(()=>{}),()=>{e=!1}},[]),e}(),[i,s]=(0,r.useState)(null),[n,o]=(0,r.useState)(null),[d,c]=(0,r.useState)(null),[m,h]=(0,r.useState)(null),[x,b]=(0,r.useState)(null);if((0,r.useEffect)(()=>{let e=()=>{s(l(document.querySelector("main.home-v81"),"truth-home-host")),o(null),c(l(document.querySelector("main.collections-v52"),"truth-capsules-host")),h(l(document.querySelector("main.rs57-landing"),"truth-solutions-host")),b(l(document.querySelector("main.rs57-wizard-shell"),"truth-wizard-host"))};e();let t=new MutationObserver(e);return t.observe(document.body,{childList:!0,subtree:!0}),()=>t.disconnect()},[]),!e)return null;let j=window.location.pathname.match(/ready-solutions\/([^/]+)/)?.[1]||"",k=e.readySolutions.find(e=>e.id===j||f(e.name)===j);return(0,t.jsxs)(t.Fragment,{children:[i?(0,a.createPortal)((0,t.jsx)(g,{d:e}),i):null,n?(0,a.createPortal)((0,t.jsx)(u,{d:e}),n):null,d?(0,a.createPortal)((0,t.jsx)(p,{d:e}),d):null,m?(0,a.createPortal)((0,t.jsx)(y,{d:e}),m):null,x&&k?(0,a.createPortal)((0,t.jsx)(v,{d:e,s:k}),x):null]})}])},19942,e=>{"use strict";var t=e.i(71645);let a="/data/catalog_master.csv";e.s(["CatalogLoadingStateV127",0,function(){return(0,t.useEffect)(()=>{let e,t=document.querySelector(".view-catalog .catalog-v123");if(!t||t.querySelector(".product-grid .product-card")||(e=t.querySelector(".title-line > span")?.textContent?.trim()??"",!(t.querySelector(".catalog-empty-v123")&&/^0\s/.test(e))))return;t.classList.add("catalog-data-loading-v127");let r=!1,i=0,s=()=>{r||(r=!0,t.classList.remove("catalog-data-loading-v127"),l.disconnect(),d?.disconnect(),window.clearTimeout(i))},n=()=>{r||(window.clearTimeout(i),i=window.setTimeout(s,450))},l=new MutationObserver(()=>{(t.querySelector(".product-grid .product-card")||!t.querySelector(".catalog-empty-v123"))&&s()});l.observe(t,{childList:!0,subtree:!0,characterData:!0});let o=performance.getEntriesByType("resource").some(e=>e.name.includes(a)),d=null;if(o)n();else if("PerformanceObserver"in window){d=new PerformanceObserver(e=>{e.getEntries().some(e=>e.name.includes(a))&&n()});try{d.observe({type:"resource",buffered:!0})}catch{d=null}}let c=window.setTimeout(s,7e3);return()=>{r=!0,t.classList.remove("catalog-data-loading-v127"),l.disconnect(),d?.disconnect(),window.clearTimeout(i),window.clearTimeout(c)}},[]),null}])}]);