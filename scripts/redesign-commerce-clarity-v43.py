from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

# V43 intentionally runs after V41/V42. It keeps the hypotheses implemented in
# V42, but presents them through a calmer multi-screen UX for desktop and mobile.
helper_start = page.find("const KD_CITY_SUGGESTIONS=")
favorites_start = page.find("function Favorites(", helper_start)
if helper_start < 0 or favorites_start < 0:
    raise SystemExit("V43 account/helper anchors not found")

account_block = r'''const KD_CITY_SUGGESTIONS=["Москва","Санкт-Петербург","Казань","Екатеринбург","Новосибирск","Омск","Нижний Новгород","Самара","Ростов-на-Дону","Краснодар"];
const KD_ADDRESS_SUGGESTIONS:Record<string,string[]>={
  "Москва":["ул. Петровка, 12","Тверская ул., 18","Большая Дмитровка ул., 9","Ленинградский проспект, 36","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Большая Конюшенная ул., 15","Литейный проспект, 24","Московский проспект, 73"],
  "Казань":["ул. Баумана, 44","ул. Пушкина, 17","проспект Ямашева, 46"],
  "Екатеринбург":["проспект Ленина, 25","ул. Малышева, 51","ул. Вайнера, 10"],
  "Новосибирск":["Красный проспект, 50","ул. Ленина, 12","ул. Советская, 35"],
  "Омск":["ул. Ленина, 20","проспект Карла Маркса, 24","ул. Гагарина, 8"],
  "Нижний Новгород":["Большая Покровская ул., 28","ул. Белинского, 61"],
  "Самара":["Ленинградская ул., 38","Московское шоссе, 17"],
  "Ростов-на-Дону":["Большая Садовая ул., 65","проспект Будённовский, 32"],
  "Краснодар":["Красная ул., 74","Северная ул., 324"],
};
const KD_PVZ_POINTS:Record<string,string[]>={
  "Москва":["Петровка, 12","Тверская, 18","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Московский проспект, 73"],
  "Казань":["Баумана, 44","Ямашева, 46"],
  "Екатеринбург":["Ленина, 25","Малышева, 51"],
  "Новосибирск":["Красный проспект, 50","Ленина, 12"],
  "Омск":["Ленина, 20","Карла Маркса, 24"],
  "Нижний Новгород":["Большая Покровская, 28","Белинского, 61"],
  "Самара":["Ленинградская, 38","Московское шоссе, 17"],
  "Ростов-на-Дону":["Большая Садовая, 65","Будённовский, 32"],
  "Краснодар":["Красная, 74","Северная, 324"],
};

function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const query=value.trim().toLowerCase();
  const items=KD_CITY_SUGGESTIONS.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);
  return <label className="v43-field v43-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="address-level2" aria-autocomplete="list" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить город"/>{open&&items.length>0&&<div className="v43-suggestions" role="listbox">{items.map(city=><button type="button" key={city} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(city);setOpen(false)}}>{city}</button>)}</div>}</label>;
}

function AddressSuggestField({city,value,onChange,label="Улица и дом",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const source=KD_ADDRESS_SUGGESTIONS[city]??[];
  const query=value.trim().toLowerCase();
  const items=source.filter(address=>!query||address.toLowerCase().includes(query)).slice(0,6);
  return <label className="v43-field v43-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="street-address" aria-autocomplete="list" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить адрес"/>{open&&items.length>0&&<div className="v43-suggestions" role="listbox">{items.map(address=><button type="button" key={address} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(address);setOpen(false)}}><b>{address}</b><small>{city}</small></button>)}</div>}</label>;
}

type AccountV43Section="overview"|"orders"|"addresses"|"personal"|"bonuses";

function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  // AUTH_FLOW_V20
  // COMMERCE_CLARITY_V43
  type AuthMethod="phone"|"email";
  type AuthStep="identify"|"code"|"register";
  const blank:Profile={name:"",surname:"",email:"",phone:"",city:"Москва",address:""};
  const initialMethod:AuthMethod=profile?.phone?"phone":"email";
  const [mode,setMode]=useState<"auth"|"profile">(profile?"profile":"auth");
  const [method,setMethod]=useState<AuthMethod>(initialMethod);
  const [step,setStep]=useState<AuthStep>("identify");
  const [identifier,setIdentifier]=useState(profile?(initialMethod==="phone"?profile.phone:profile.email):"");
  const [code,setCode]=useState("");
  const [draft,setDraft]=useState<Profile>(profile??blank);
  const [section,setSection]=useState<AccountV43Section>("overview");
  const [updates,setUpdates]=useState(true);

  useEffect(()=>{if(profile){setDraft(profile);setMode("profile")}},[profile]);

  const cleanPhone=(value:string)=>value.replace(/\D/g,"");
  const validEmail=(value:string)=>value.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
  const validPhone=(value:string)=>cleanPhone(value).length>=10;
  const contactValid=method==="email"?/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identifier.trim()):validPhone(identifier);
  const switchMethod=(next:AuthMethod)=>{setMethod(next);setIdentifier(next==="email"?(profile?.email??""):(profile?.phone??""));setCode("");setStep("identify")};
  const requestCode=()=>{if(!contactValid){notice(method==="email"?"Введите корректный email":"Введите корректный номер телефона");return}setCode("");setStep("code");notice(method==="phone"?"Демо-код из SMS — 1234":"Демо-код из письма — 1234")};
  const verifyCode=()=>{if(code.trim()!=="1234"){notice("Неверный код. Для демо используйте 1234");return}const sameProfile=Boolean(profile&&(method==="email"?profile.email.trim().toLowerCase()===identifier.trim().toLowerCase():cleanPhone(profile.phone)===cleanPhone(identifier)));if(sameProfile&&profile){setDraft(profile);setMode("profile");setSection("overview");setStep("identify");notice("Вход выполнен");return}setDraft(current=>({...current,[method==="email"?"email":"phone"]:identifier.trim()}));setStep("register")};
  const register=()=>{const next={...draft,[method==="email"?"email":"phone"]:identifier.trim()};if(!next.name.trim()){notice("Введите имя");return}save(next);setDraft(next);setMode("profile");setSection("overview");setStep("identify");notice("Аккаунт создан")};
  const savePersonal=()=>{if(!draft.name.trim()){notice("Введите имя");return}if(!validEmail(draft.email)){notice("Проверьте email");return}if(draft.phone&&!validPhone(draft.phone)){notice("Проверьте номер телефона");return}save(draft);notice("Личные данные сохранены")};
  const saveAddress=()=>{if(!draft.city.trim()||!draft.address.trim()){notice("Укажите город и адрес");return}save(draft);notice("Адрес сохранён")};
  const signOut=()=>{logout();setDraft(blank);setIdentifier("");setCode("");setStep("identify");setMode("auth");setSection("overview");notice("Вы вышли из аккаунта")};
  const nav:[AccountV43Section,string][]=[["overview","Обзор"],["orders","Заказы"],["addresses","Адреса"],["personal","Личные данные"],["bonuses","Бонусы"]];

  return <div className="overlay auth-overlay account-v43-overlay" data-analytics-step="account_open"><button className="overlay-bg" onClick={close} aria-label="Закрыть личный кабинет"/><aside className={`side-panel account auth-v20 account-v43 ${mode==="profile"?"is-profile":"is-auth"}`} role="dialog" aria-modal="true" aria-label="Личный кабинет">
    <header className="account-v43-head"><button className="account-v43-back" type="button" onClick={close}>← <span>Вернуться</span></button><b>КУЛЬТУРА ДОМА</b><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {mode==="profile"?<div className="account-v43-shell">
      <aside className="account-v43-nav"><div className="account-v43-person"><span>{(draft.name||"К").slice(0,1).toUpperCase()}</span><div><small>ЛИЧНЫЙ КАБИНЕТ</small><strong>{[draft.name,draft.surname].filter(Boolean).join(" ")||"Профиль"}</strong></div></div><nav>{nav.map(([key,label])=><button type="button" key={key} className={section===key?"active":""} onClick={()=>setSection(key)}>{label}<span>→</span></button>)}</nav><button type="button" className="account-v43-signout" onClick={signOut}>Выйти</button></aside>
      <main className="account-v43-main">
        <nav className="account-v43-mobile-nav" aria-label="Разделы личного кабинета">{nav.map(([key,label])=><button type="button" key={key} className={section===key?"active":""} onClick={()=>setSection(key)}>{label}</button>)}</nav>
        {section==="overview"&&<section className="account-v43-view"><header className="account-v43-title"><small>ОБЗОР</small><h1>{draft.name?`Здравствуйте, ${draft.name}`:"Личный кабинет"}</h1><p>Самое важное — заказы, адрес и бонусы — на одном экране.</p></header><div className="account-v43-overview-grid"><button type="button" onClick={()=>setSection("orders")}><small>ЗАКАЗЫ</small><strong>Нет активных</strong><span>Следить за статусом →</span></button><button type="button" onClick={()=>setSection("bonuses")}><small>БОНУСЫ</small><strong>0 бонусов</strong><span>Подробнее →</span></button><button type="button" className="wide" onClick={()=>setSection("addresses")}><small>ОСНОВНОЙ АДРЕС</small><strong>{draft.address?`${draft.city}, ${draft.address}`:"Адрес не добавлен"}</strong><span>{draft.address?"Изменить":"Добавить адрес"} →</span></button></div><section className="account-v43-note"><div><small>БЫСТРОЕ ОФОРМЛЕНИЕ</small><h2>Данные подставятся автоматически</h2></div><p>Имя, телефон и основной адрес будут заполнены в checkout. Их можно изменить перед подтверждением заказа.</p></section></section>}
        {section==="orders"&&<section className="account-v43-view"><header className="account-v43-title"><small>МОИ ЗАКАЗЫ</small><h1>Заказы</h1><p>Здесь будут история покупок и актуальный статус доставки.</p></header><div className="account-v43-empty"><span>○</span><h2>Заказов пока нет</h2><p>После оформления появится понятная цепочка: заказ принят → собран → передан курьеру → доставлен.</p><button type="button" className="primary" onClick={close}>ПРОДОЛЖИТЬ ПОКУПКИ</button></div><label className="account-v43-check"><input type="checkbox" checked={updates} onChange={event=>setUpdates(event.target.checked)}/><span>Получать уведомления об изменении статуса заказа</span></label></section>}
        {section==="addresses"&&<section className="account-v43-view"><header className="account-v43-title"><small>ДОСТАВКА</small><h1>Основной адрес</h1><p>Сохранённый адрес автоматически появится при оформлении заказа.</p></header><div className="account-v43-form account-v43-address-form"><CitySuggestField value={draft.city} required onChange={city=>setDraft({...draft,city,address:city===draft.city?draft.address:""})}/><AddressSuggestField city={draft.city} value={draft.address} required onChange={address=>setDraft({...draft,address})}/></div><div className="account-v43-form-actions"><button type="button" className="primary" onClick={saveAddress}>СОХРАНИТЬ АДРЕС</button><button type="button" onClick={()=>setSection("overview")}>Отмена</button></div></section>}
        {section==="personal"&&<section className="account-v43-view"><header className="account-v43-title"><small>ПРОФИЛЬ</small><h1>Личные данные</h1><p>Только данные, необходимые для связи и оформления заказа.</p></header><div className="account-v43-form"><label className="v43-field"><span>Имя *</span><input value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})} autoComplete="given-name"/></label><label className="v43-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})} autoComplete="family-name"/></label><label className="v43-field"><span>Телефон</span><input type="tel" value={draft.phone} onChange={event=>setDraft({...draft,phone:event.target.value})} autoComplete="tel"/></label><label className="v43-field"><span>Email</span><input type="email" value={draft.email} onChange={event=>setDraft({...draft,email:event.target.value})} autoComplete="email"/></label></div><div className="account-v43-form-actions"><button type="button" className="primary" onClick={savePersonal}>СОХРАНИТЬ</button><button type="button" onClick={()=>setSection("overview")}>Отмена</button></div></section>}
        {section==="bonuses"&&<section className="account-v43-view"><header className="account-v43-title"><small>ПРОГРАММА ЛОЯЛЬНОСТИ</small><h1>Бонусы</h1><p>Баланс показывается до оплаты, чтобы им было проще воспользоваться.</p></header><div className="account-v43-balance"><small>ДОСТУПНО</small><strong>0</strong><span>бонусов</span></div><div className="account-v43-info-rows"><div><b>Как начисляются</b><p>Правила начисления будут отображаться здесь после подключения программы лояльности.</p></div><div><b>Как использовать</b><p>Доступные бонусы будут показаны в корзине и на шаге оплаты.</p></div></div></section>}
      </main>
    </div>:<div className="account-v43-auth">
      {step==="identify"&&<><div className="account-v43-auth-title"><small>ЛИЧНЫЙ КАБИНЕТ</small><h1>Войти или создать аккаунт</h1><p>Без пароля — по короткому коду.</p></div><div className="auth-methods" role="tablist"><button type="button" className={method==="phone"?"active":""} onClick={()=>switchMethod("phone")}>Телефон</button><button type="button" className={method==="email"?"active":""} onClick={()=>switchMethod("email")}>Email</button></div><label className="v43-field"><span>{method==="phone"?"Номер телефона":"Email"}</span><input type={method==="phone"?"tel":"email"} value={identifier} onChange={event=>setIdentifier(event.target.value)} autoComplete={method==="phone"?"tel":"email"} placeholder={method==="phone"?"+7 999 000-00-00":"name@example.com"}/></label><button type="button" className="primary account-v43-auth-cta" disabled={!identifier.trim()} onClick={requestCode}>ПОЛУЧИТЬ КОД</button><p className="auth-legal">Продолжая, вы соглашаетесь с обработкой персональных данных.</p></>}
      {step==="code"&&<><button className="account-v43-auth-back" type="button" onClick={()=>setStep("identify")}>← Назад</button><div className="account-v43-auth-title"><small>ПОДТВЕРЖДЕНИЕ</small><h1>Введите код</h1><p>Код отправлен на {method==="phone"?"номер":"email"} <b>{identifier}</b>.</p></div><label className="v43-field"><span>Код</span><input autoFocus inputMode="numeric" maxLength={4} value={code} onChange={event=>setCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000"/></label><button type="button" className="primary account-v43-auth-cta" disabled={code.length!==4} onClick={verifyCode}>ПРОДОЛЖИТЬ</button><button type="button" className="account-v43-resend" onClick={requestCode}>Отправить код ещё раз</button><small className="account-v43-demo">Демо-код: 1234</small></>}
      {step==="register"&&<><button className="account-v43-auth-back" type="button" onClick={()=>setStep("code")}>← Назад</button><div className="account-v43-auth-title"><small>НОВЫЙ АККАУНТ</small><h1>Как к вам обращаться?</h1><p>Остальные данные можно заполнить позже.</p></div><label className="v43-field"><span>Имя *</span><input autoFocus value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})}/></label><label className="v43-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})}/></label><button type="button" className="primary account-v43-auth-cta" disabled={!draft.name.trim()} onClick={register}>СОЗДАТЬ АККАУНТ</button></>}
    </div>}
  </aside></div>;
}

'''
page = page[:helper_start] + account_block + page[favorites_start:]

cart_start = page.find("function Cart(")
checkout_start = page.find("function Checkout(", cart_start)
if cart_start < 0 or checkout_start < 0:
    raise SystemExit("V43 cart anchors not found")

cart_block = r'''function Cart({ cart, profile, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; profile:Profile|null; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const courierShipping=total>=15000?0:300;
  const courierTotal=total+courierShipping;
  const deliveryLeft=Math.max(0,15000-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/15000*100));
  const seedWords=(cart[0]?.name??"").toLowerCase().split(/[^а-яёa-z0-9]+/i).filter(word=>word.length>4).filter(word=>!["комплект","декоративная","постельного","культура","товара"].includes(word));
  const scored=products.filter(product=>!cart.some(item=>item.id===product.id)).map(product=>({product,score:seedWords.reduce((score,word)=>score+(product.name.toLowerCase().includes(word)?2:0),0)})).sort((a,b)=>b.score-a.score);
  const relatedItems=Array.from(new Map(scored.filter(row=>row.score>0).map(row=>[row.product.name,row.product])).values()).slice(0,4);
  const suggestions=relatedItems.length?relatedItems:recentItems.filter(product=>!cart.some(item=>item.id===product.id)).slice(0,4);

  return <div className="overlay cart-v43-overlay" data-analytics-step="cart_open"><aside className="cart-v43" role="dialog" aria-modal="true" aria-label="Корзина">
    <header className="cart-v43-head"><button type="button" onClick={go}>← <span>Продолжить покупки</span></button><b>КУЛЬТУРА ДОМА</b><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {cart.length===0?<main className="cart-v43-empty"><small>КОРЗИНА</small><h1>Здесь пока пусто</h1><p>Добавьте предметы из каталога или вернитесь к недавно просмотренным.</p>{recentItems.length>0&&<section><h2>Недавно просмотренные</h2><div>{recentItems.map(product=><button type="button" key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><span>{product.name}</span><b>{fmt(product.price)}</b></button>)}</div></section>}<button type="button" className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></main>:<main className="cart-v43-layout">
      <section className="cart-v43-content"><header className="cart-v43-title"><small>КОРЗИНА</small><h1>Ваш выбор <span>{itemCount}</span></h1><p>Проверьте количество и упаковку. Размер и цвет остаются такими, как вы выбрали.</p></header>
        <div className="cart-v43-delivery"><div><b>{courierShipping===0?"Бесплатная доставка":"До бесплатной доставки — "+fmt(deliveryLeft)}</b><span>{courierShipping===0?"Для курьера и ПВЗ":"Курьер — 300 ₽ · ПВЗ — бесплатно"}</span></div><i><b style={{width:`${deliveryProgress}%`}}/></i></div>
        <div className="cart-v43-items">{cart.map((item,index)=><article className="cart-v43-item" key={`${item.id}-${index}`}><button className="cart-v43-media" type="button" onClick={()=>choose(item)}><ScrollableProductMedia product={item} alt={item.name} className="cart-item-media"/></button><div className="cart-v43-copy"><div className="cart-v43-item-head"><button type="button" onClick={()=>choose(item)}>{item.name}</button><b>{fmt(item.price*item.quantity)}</b></div><div className="cart-v43-meta"><span>Цвет: {item.selectedColor}</span><span>Размер: {item.selectedSize}</span></div>{isGiftPackagingAvailable(item)&&<label className="cart-v43-gift"><input type="checkbox" checked={Boolean(item.giftWrap)} onChange={event=>update(index,{giftWrap:event.target.checked})}/><span>Подарочная упаковка</span></label>}<div className="cart-v43-actions"><QuantityControl quantity={item.quantity} setQuantity={quantity=>update(index,{quantity})}/><button type="button" onClick={()=>remove(index)}>Удалить</button></div></div></article>)}</div>
        {suggestions.length>0&&<section className="cart-v43-crosssell"><header><small>ДОПОЛНИТЕ КОМПЛЕКТ</small><h2>Может подойти к вашему выбору</h2></header><div>{suggestions.map(product=><article key={product.id}><button className="cart-v43-cross-media" type="button" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/></button><button className="cart-v43-cross-name" type="button" onClick={()=>choose(product)}>{product.name}</button><b>{fmt(product.price)}</b><button className="cart-v43-cross-add" type="button" onClick={()=>quickAdd(product)}>Добавить</button></article>)}</div></section>}
      </section>
      <aside className="cart-v43-summary"><div className="cart-v43-summary-inner"><small>ИТОГ ЗАКАЗА</small><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Курьер</dt><dd>{courierShipping===0?"Бесплатно":fmt(courierShipping)}</dd></div><div><dt>Пункт выдачи</dt><dd>Бесплатно</dd></div></dl><div className="cart-v43-total"><span>Итого при курьере</span><b>{fmt(courierTotal)}</b></div><p>На следующем шаге можно выбрать бесплатный ПВЗ. Итог обновится до подтверждения заказа.</p>{profile?<div className="cart-v43-bonus"><span>Ваш баланс</span><b>0 бонусов</b></div>:<div className="cart-v43-bonus"><span>Бонусы</span><b>Войдите, чтобы увидеть баланс</b></div>}<button type="button" className="primary cart-v43-checkout" data-analytics-step="checkout_start" onClick={checkout}>ПЕРЕЙТИ К ОФОРМЛЕНИЮ</button><div className="cart-v43-trust"><span>✓ Безопасная оплата</span><span>✓ Итог до подтверждения</span></div></div></aside>
    </main>}
  </aside></div>;
}

'''
page = page[:cart_start] + cart_block + page[checkout_start:]

checkout_start = page.find("function Checkout(")
checkout_map_start = page.find("function CheckoutMap(", checkout_start)
if checkout_start < 0 or checkout_map_start < 0:
    raise SystemExit("V43 checkout anchors not found")

checkout_block = r'''function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type CheckoutStep=1|2|3;
  type PaymentMethod="card"|"sbp"|"upon";
  const [step,setStep]=useState<CheckoutStep>(1);
  const [delivery,setDelivery]=useState<"courier"|"pickup">("courier");
  const [payment,setPayment]=useState<PaymentMethod|null>(null);
  const [slot,setSlot]=useState("18:00–22:00");
  const [agreed,setAgreed]=useState(true);
  const [notifications,setNotifications]=useState(true);
  const [promoOpen,setPromoOpen]=useState(false);
  const [promo,setPromo]=useState("");
  const [promoStatus,setPromoStatus]=useState("");
  const [pickupPoint,setPickupPoint]=useState("");
  const [access,setAccess]=useState("");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [contactAttempted,setContactAttempted]=useState(false);
  const [deliveryAttempted,setDeliveryAttempted]=useState(false);
  const shellRef=useRef<HTMLDivElement>(null);

  useEffect(()=>{shellRef.current?.scrollTo({top:0,behavior:"smooth"})},[step]);

  const shipping=delivery==="pickup"||total>=15000?0:300;
  const online=payment==="card"||payment==="sbp";
  const onlineDiscount=online?Math.round(total*.03):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const expensive=payable>=30000;
  const pvz=KD_PVZ_POINTS[form.city]??[];
  const phoneDigits=form.phone.replace(/\D/g,"");
  const phoneOk=phoneDigits.length>=10&&(profile?phoneVerified:Boolean(phoneVerified));
  const emailOk=form.email.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const contactOk=form.name.trim().length>0&&phoneOk&&emailOk;
  const deliveryOk=delivery==="courier"?(form.city.trim().length>0&&form.address.trim().length>3):(form.city.trim().length>0&&pickupPoint.length>0);
  const paymentOk=payment!==null;
  const canSubmit=contactOk&&deliveryOk&&paymentOk&&agreed;
  const requestPhoneCode=()=>{if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}setCodeSent(true);setPhoneCode("");setOtpError("")};
  const verifyPhone=()=>{if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}else setOtpError("Неверный код. Для демо используйте 1234")};
  const applyPromo=()=>setPromoStatus(promo.trim()?"Код принят для проверки":"Введите промокод");
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:event.target.value});
  const nextFromContacts=()=>{setContactAttempted(true);if(contactOk)setStep(2)};
  const nextFromDelivery=()=>{setDeliveryAttempted(true);if(deliveryOk)setStep(3)};
  const setPhone=(value:string)=>{setForm({...form,phone:value});setPhoneVerified(Boolean(profile?.phone&&value===profile.phone));setCodeSent(false);setOtpError("")};
  const stepLabel=(value:CheckoutStep)=>value===1?"Контакты":value===2?"Доставка":"Оплата";

  return <div className="checkout checkout-v43" ref={shellRef} data-analytics-step="checkout_view">
    <header className="checkout-v43-head"><button type="button" onClick={step===1?close:()=>setStep((step-1) as CheckoutStep)}>← <span>{step===1?"Вернуться":"Назад"}</span></button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    <nav className="checkout-v43-progress" aria-label="Шаги оформления">{([1,2,3] as CheckoutStep[]).map(value=><button type="button" key={value} className={`${step===value?"active":""} ${step>value?"done":""}`} onClick={()=>{if(value<step)setStep(value)}}><i>{step>value?"✓":value}</i><span>{stepLabel(value)}</span></button>)}</nav>
    <form className="checkout-v43-layout" onSubmit={event=>{event.preventDefault();if(canSubmit)submit()}}>
      <main className="checkout-v43-content">
        {step===1&&<section className="checkout-v43-step" data-analytics-step="checkout_contacts"><header><small>ШАГ 1 ИЗ 3</small><h1>Контактные данные</h1><p>{profile?"Мы подставили данные из профиля. Проверьте их перед продолжением.":"Оформить можно без регистрации. Номер подтверждаем коротким кодом, чтобы избежать ошибочных заказов."}</p></header><div className="checkout-v43-fields"><label className="v43-field"><span>Имя *</span><input value={form.name} onChange={field("name")} autoComplete="given-name" name="name" placeholder="Имя"/></label><label className="v43-field"><span>Фамилия</span><input value={form.surname} onChange={field("surname")} autoComplete="family-name" name="surname" placeholder="Необязательно"/></label><label className="v43-field checkout-v43-phone"><span>Телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} autoComplete="tel" inputMode="tel" name="phone" placeholder="+7 999 000-00-00"/>{phoneDigits.length>=10&&!phoneVerified&&<button type="button" onClick={requestPhoneCode}>Подтвердить</button>}{phoneVerified&&<b>✓ Подтверждён</b>}</div></label><label className="v43-field"><span>Email</span><input type="email" value={form.email} onChange={field("email")} autoComplete="email" name="email" placeholder="Для чека и статусов"/></label>{codeSent&&!phoneVerified&&<div className="checkout-v43-otp"><div><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></div><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}</div>{contactAttempted&&!contactOk&&<div className="checkout-v43-inline-error" role="alert">{!form.name.trim()?"Укажите имя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите телефон. ":""}{!emailOk?"Проверьте email.":""}</div>}<button type="button" className="primary checkout-v43-next" onClick={nextFromContacts}>ПРОДОЛЖИТЬ К ДОСТАВКЕ</button></section>}

        {step===2&&<section className="checkout-v43-step" data-analytics-step="checkout_delivery"><header><small>ШАГ 2 ИЗ 3</small><h1>Как доставить заказ?</h1><p>Стоимость и способ доставки выбираются до оплаты.</p></header><div className="checkout-v43-delivery-methods"><button type="button" className={delivery==="courier"?"active":""} onClick={()=>setDelivery("courier")}><i/><div><b>Курьер</b><span>{total>=15000?"Бесплатно":"300 ₽"}</span><small>До двери</small></div></button><button type="button" className={delivery==="pickup"?"active":""} onClick={()=>setDelivery("pickup")}><i/><div><b>Пункт выдачи</b><span>Бесплатно</span><small>Выберите удобный адрес</small></div></button></div><div className="checkout-v43-address"><CitySuggestField value={form.city} required onChange={city=>{setForm({...form,city,address:city===form.city?form.address:""});setPickupPoint("")}}/>{delivery==="courier"?<><AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm({...form,address})}/><label className="v43-field"><span>Квартира, подъезд, домофон</span><input value={access} onChange={event=>setAccess(event.target.value)} name="flat" placeholder="Необязательно"/></label><div className="checkout-v43-slots"><span>Удобное время</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div></>:<div className="checkout-v43-pvz"><span>Выберите пункт выдачи</span>{pvz.length?pvz.map(point=><button type="button" key={point} className={pickupPoint===point?"active":""} onClick={()=>setPickupPoint(point)}><i/><div><b>{point}</b><small>{form.city}</small></div></button>):<p>Выберите город — покажем доступные пункты.</p>}</div>}</div>{deliveryAttempted&&!deliveryOk&&<div className="checkout-v43-inline-error" role="alert">{delivery==="courier"?"Укажите город и адрес доставки.":"Выберите город и пункт выдачи."}</div>}<button type="button" className="primary checkout-v43-next" onClick={nextFromDelivery}>ПРОДОЛЖИТЬ К ОПЛАТЕ</button></section>}

        {step===3&&<section className="checkout-v43-step" data-analytics-step="checkout_payment"><header><small>ШАГ 3 ИЗ 3</small><h1>Оплата и подтверждение</h1><p>Проверьте способ оплаты и итоговую сумму. После нажатия заказ будет создан.</p></header><div className="checkout-v43-payments"><button type="button" className={payment==="card"?"active":""} onClick={()=>setPayment("card")}><i/><div><b>Банковская карта</b><span>−3% при онлайн-оплате</span></div></button><button type="button" className={payment==="sbp"?"active":""} onClick={()=>setPayment("sbp")}><i/><div><b>СБП</b><span>−3% при онлайн-оплате</span></div></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><div><b>При получении</b><span>Без скидки</span></div></button></div>{expensive&&<aside className="checkout-v43-concierge"><small>ЗАКАЗ ОТ 30 000 ₽</small><b>Персональное сопровождение</b><p>Менеджер свяжется в течение часа, чтобы подтвердить наличие, доставку и детали заказа.</p></aside>}<section className="checkout-v43-review"><div><span>Контакты</span><p>{form.name} · {form.phone}{form.email?` · ${form.email}`:""}</p><button type="button" onClick={()=>setStep(1)}>Изменить</button></div><div><span>Доставка</span><p>{delivery==="courier"?`${form.city}, ${form.address}${access?`, ${access}`:""} · ${slot}`:`ПВЗ: ${form.city}, ${pickupPoint}`}</p><button type="button" onClick={()=>setStep(2)}>Изменить</button></div></section><button type="button" className="checkout-v43-promo-toggle" onClick={()=>setPromoOpen(!promoOpen)}>Промокод или сертификат <span>{promoOpen?"−":"+"}</span></button>{promoOpen&&<div className="checkout-v43-promo"><input value={promo} onChange={event=>{setPromo(event.target.value);setPromoStatus("")}} placeholder="Введите код"/><button type="button" onClick={applyPromo}>Применить</button>{promoStatus&&<small>{promoStatus}</small>}</div>}<label className="checkout-v43-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Сообщать об изменении статуса заказа</span></label><label className="checkout-v43-check"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Согласен(на) с условиями продажи и обработкой персональных данных.</span></label>{!paymentOk&&<div className="checkout-v43-inline-error">Выберите способ оплаты.</div>}<button type="submit" className="primary checkout-v43-next" disabled={!canSubmit}>ОФОРМИТЬ ЗАКАЗ · {fmt(payable)}</button></section>}
      </main>
      <aside className="checkout-v43-summary"><div className="checkout-v43-summary-inner"><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header><div className="checkout-v43-summary-items">{cart.slice(0,3).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><div><b>{item.name}</b><span>{item.selectedColor} · {item.selectedSize}</span><small>{item.quantity} × {fmt(item.price)}</small></div></article>)}</div>{cart.length>3&&<small className="checkout-v43-more">Ещё {cart.length-3} поз.</small>}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div>{onlineDiscount>0&&<div className="discount"><dt>Онлайн-оплата −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}<div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div></dl><div className="checkout-v43-total"><span>Итого</span><b>{fmt(payable)}</b></div><p>{delivery==="pickup"?"Пункт выдачи выбран без доплаты.":shipping===0?"Курьерская доставка бесплатна.":"Курьерская доставка включена в итог."}</p>{profile?<div className="checkout-v43-bonus"><span>Бонусы</span><b>0 доступно</b></div>:<div className="checkout-v43-bonus"><span>Бонусы</span><b>Войдите, чтобы увидеть баланс</b></div>}</div></aside>
    </form>
    <div className="checkout-v43-mobile-bar"><div><small>ИТОГО</small><b>{fmt(payable)}</b></div>{step===1?<button type="button" className="primary" onClick={nextFromContacts}>ПРОДОЛЖИТЬ</button>:step===2?<button type="button" className="primary" onClick={nextFromDelivery}>ПРОДОЛЖИТЬ</button>:<button type="button" className="primary" disabled={!canSubmit} onClick={()=>{if(canSubmit)submit()}}>ОФОРМИТЬ</button>}</div>
  </div>;
}

'''
page = page[:checkout_start] + checkout_block + page[checkout_map_start:]

if "<Cart cart={cart} profile={profile}" not in page:
    raise SystemExit("V43 expects the V42 Cart call with profile and quickAdd")

page_path.write_text(page,encoding="utf-8")
print("Applied clear adaptive commerce flow V43")
