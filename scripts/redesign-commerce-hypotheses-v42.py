from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

marker = "COMMERCE_HYPOTHESES_V42"

# V41 is intentionally applied first by the migration runner. V42 replaces only
# account/cart/checkout and leaves the rest of the storefront untouched.
account_start = page.find("function Account(")
favorites_start = page.find("function Favorites(", account_start)
if account_start < 0 or favorites_start < 0:
    raise SystemExit("V42 account anchors not found")

account_block = r'''const KD_CITY_SUGGESTIONS=["Москва","Санкт-Петербург","Казань","Екатеринбург","Новосибирск","Омск","Нижний Новгород","Самара","Ростов-на-Дону","Краснодар"];
const KD_ADDRESS_SUGGESTIONS:Record<string,string[]>={
  "Москва":["ул. Петровка, 12","Тверская ул., 18","Большая Дмитровка ул., 9","Ленинградский проспект, 36","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Большая Конюшенная ул., 15","Литейный проспект, 24","Московский проспект, 73"],
  "Казань":["ул. Баумана, 44","ул. Пушкина, 17","проспект Ямашева, 46"],
  "Екатеринбург":["проспект Ленина, 25","ул. Малышева, 51","ул. Вайнера, 10"],
  "Новосибирск":["Красный проспект, 50","ул. Ленина, 12","ул. Советская, 35"],
  "Омск":["ул. Ленина, 20","проспект Карла Маркса, 24","ул. Гагарина, 8"],
};
const KD_PVZ_POINTS:Record<string,string[]>={
  "Москва":["Петровка, 12","Тверская, 18","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Московский проспект, 73"],
  "Казань":["Баумана, 44","Ямашева, 46"],
  "Екатеринбург":["Ленина, 25","Малышева, 51"],
  "Новосибирск":["Красный проспект, 50","Ленина, 12"],
  "Омск":["Ленина, 20","Карла Маркса, 24"],
};

function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const query=value.trim().toLowerCase();
  const items=KD_CITY_SUGGESTIONS.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);
  return <label className="v42-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="address-level2" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить город"/>{open&&items.length>0&&<div className="v42-suggestions" role="listbox">{items.map(city=><button type="button" key={city} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(city);setOpen(false)}}>{city}</button>)}</div>}</label>;
}

function AddressSuggestField({city,value,onChange,label="Адрес",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const source=KD_ADDRESS_SUGGESTIONS[city]??[];
  const query=value.trim().toLowerCase();
  const items=source.filter(address=>!query||address.toLowerCase().includes(query)).slice(0,6);
  return <label className="v42-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="street-address" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Улица, дом"/>{open&&items.length>0&&<div className="v42-suggestions" role="listbox">{items.map(address=><button type="button" key={address} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(address);setOpen(false)}}><b>{address}</b><small>{city}</small></button>)}</div>}<small className="v42-hint">Подсказки работают в прототипе локально; поле готово к подключению адресного API.</small></label>;
}

function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  // AUTH_FLOW_V20
  // COMMERCE_HYPOTHESES_V42
  type AuthMethod = "phone" | "email";
  type AuthStep = "identify" | "code" | "register";
  const blank:Profile={name:"",surname:"",email:"",phone:"",city:"Москва",address:""};
  const initialMethod:AuthMethod=profile?.phone?"phone":"email";
  const [mode,setMode]=useState<"auth"|"profile">(profile?"profile":"auth");
  const [method,setMethod]=useState<AuthMethod>(initialMethod);
  const [step,setStep]=useState<AuthStep>("identify");
  const [identifier,setIdentifier]=useState(profile?(initialMethod==="phone"?profile.phone:profile.email):"");
  const [code,setCode]=useState("");
  const [draft,setDraft]=useState<Profile>(profile??blank);
  const [updates,setUpdates]=useState(true);
  const [activeSection,setActiveSection]=useState<"overview"|"profile">("overview");

  useEffect(()=>{if(profile){setDraft(profile);setMode("profile")}},[profile]);

  const cleanPhone=(value:string)=>value.replace(/[^\d+]/g,"");
  const validEmail=(value:string)=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
  const validPhone=(value:string)=>cleanPhone(value).replace(/\D/g,"").length>=10;
  const contactValid=method==="email"?validEmail(identifier):validPhone(identifier);
  const contactLabel=method==="email"?"email":"номер телефона";
  const switchMethod=(next:AuthMethod)=>{setMethod(next);setIdentifier(next==="email"?(profile?.email??""):(profile?.phone??""));setCode("");setStep("identify")};
  const requestCode=()=>{if(!contactValid){notice(method==="email"?"Введите корректный email":"Введите корректный номер телефона");return}setStep("code");setCode("");notice(method==="phone"?"Демо: код из SMS — 1234":"Демо: код из письма — 1234")};
  const verifyCode=()=>{if(code.trim()!=="1234"){notice("Неверный код. Для демо используйте 1234");return}const sameProfile=Boolean(profile&&(method==="email"?profile.email.trim().toLowerCase()===identifier.trim().toLowerCase():cleanPhone(profile.phone)===cleanPhone(identifier)));if(sameProfile&&profile){setDraft(profile);setMode("profile");setStep("identify");notice("Вход выполнен");return}setDraft(current=>({...current,[method==="email"?"email":"phone"]:identifier.trim()}));setStep("register")};
  const register=()=>{const next={...draft,[method==="email"?"email":"phone"]:identifier.trim()};if(!next.name.trim()){notice("Введите имя");return}save(next);setDraft(next);setMode("profile");setStep("identify");notice("Аккаунт создан")};
  const saveProfile=()=>{if(!draft.name.trim()){notice("Введите имя");return}if(draft.email&&!validEmail(draft.email)){notice("Проверьте email");return}if(draft.phone&&!validPhone(draft.phone)){notice("Проверьте номер телефона");return}save(draft);notice("Данные профиля сохранены")};
  const signOut=()=>{logout();setDraft(blank);setIdentifier("");setCode("");setStep("identify");setMode("auth");notice("Вы вышли из аккаунта")};

  return <div className="overlay auth-overlay commerce-v42-account-overlay" data-analytics-step="account_open"><button className="overlay-bg" onClick={close} aria-label="Закрыть личный кабинет"/><aside className="side-panel account auth-v20 account-v41 account-v42" role="dialog" aria-modal="true" aria-label="Личный кабинет">
    <header className="account-v41-head account-v42-head"><div><small>КУЛЬТУРА ДОМА</small><h1>Личный кабинет</h1></div><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {mode==="profile"?<div className="account-v42-profile">
      <section className="account-v42-welcome"><div><small>ПРОФИЛЬ</small><h2>{draft.name?`Здравствуйте, ${draft.name}`:"Ваш профиль"}</h2><p>Здесь собраны данные, которые сокращают оформление заказа и помогают вернуться к покупкам.</p></div><button type="button" onClick={()=>setActiveSection(activeSection==="profile"?"overview":"profile")}>{activeSection==="profile"?"К обзору":"Изменить данные"}</button></section>
      {activeSection==="overview"?<>
        <section className="account-v42-stats" aria-label="Преимущества аккаунта"><article><small>БОНУСЫ</small><strong>0</strong><span>бонусов доступно</span><p>Баланс всегда виден перед покупкой.</p></article><article><small>ЗАКАЗЫ</small><strong>0</strong><span>активных заказов</span><p>Статусы появятся здесь после оформления.</p></article></section>
        <section className="account-v42-card"><header><div><small>ДОСТАВКА</small><h3>Сохранённый адрес</h3></div><button type="button" onClick={()=>setActiveSection("profile")}>Изменить</button></header><p>{draft.address?`${draft.city}, ${draft.address}`:"Добавьте адрес — он автоматически подставится в checkout."}</p></section>
        <section className="account-v42-card account-v42-orders"><header><div><small>МОИ ЗАКАЗЫ</small><h3>Статус без лишних звонков</h3></div></header><div className="account-v42-order-empty"><i>○</i><p>После покупки здесь будет цепочка статусов: <b>принят → собран → передан курьеру → доставлен</b>.</p></div><label><input type="checkbox" checked={updates} onChange={event=>setUpdates(event.target.checked)}/><span>Получать уведомления о статусе заказа</span></label></section>
        <section className="account-v42-card"><header><div><small>ПОВТОРНАЯ ПОКУПКА</small><h3>Подборки к вашим покупкам</h3></div></header><p>После доставки здесь появятся рекомендации к купленным товарам и напоминание о бонусах.</p></section>
        <button className="link auth-logout account-v42-logout" onClick={signOut}>Выйти из аккаунта</button>
      </>:<>
        <section className="account-v41-section account-v42-edit"><header><span>Личные данные</span><small>Используются для оформления</small></header><AccountFields draft={draft} setDraft={setDraft}/></section>
        <div className="account-v41-actions"><button className="primary auth-primary" onClick={()=>{saveProfile();setActiveSection("overview")}}>СОХРАНИТЬ ИЗМЕНЕНИЯ</button></div>
      </>}
    </div>:<div className="auth-flow account-v41-auth account-v42-auth">
      {step==="identify"&&<><div className="account-v41-intro"><small>ВХОД И РЕГИСТРАЦИЯ</small><h2>Войти в аккаунт</h2><p>Адрес подставится автоматически, бонусы будут видны до оплаты, а статусы заказа — после покупки.</p></div><div className="auth-methods" role="tablist" aria-label="Способ входа"><button type="button" role="tab" aria-selected={method==="phone"} className={method==="phone"?"active":""} onClick={()=>switchMethod("phone")}>Телефон</button><button type="button" role="tab" aria-selected={method==="email"} className={method==="email"?"active":""} onClick={()=>switchMethod("email")}>Email</button></div><label className="auth-field"><span>{method==="phone"?"Номер телефона":"Email"}</span><input type={method==="phone"?"tel":"email"} autoComplete={method==="phone"?"tel":"email"} value={identifier} onChange={event=>setIdentifier(event.target.value)} placeholder={method==="phone"?"+7 999 000-00-00":"name@example.com"}/></label><button className="primary auth-primary" disabled={!identifier.trim()} onClick={requestCode}>ПОЛУЧИТЬ КОД</button><p className="auth-legal">Без пароля. Подтверждение контакта защищает от случайных заказов.</p></>}
      {step==="code"&&<><button className="auth-back" type="button" onClick={()=>{setStep("identify");setCode("")}}>← Назад</button><div className="account-v41-intro"><small>ПОДТВЕРЖДЕНИЕ</small><h2>Введите код</h2><p>Код отправлен на {contactLabel} <b>{identifier}</b>.</p></div><label className="auth-field auth-code-field"><span>Код подтверждения</span><input autoFocus inputMode="numeric" autoComplete="one-time-code" maxLength={4} value={code} onChange={event=>setCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000"/></label><button className="primary auth-primary" disabled={code.length!==4} onClick={verifyCode}>ПРОДОЛЖИТЬ</button><button className="link auth-resend" type="button" onClick={requestCode}>Отправить код ещё раз</button><p className="auth-demo-note">Демо-код: 1234</p></>}
      {step==="register"&&<><button className="auth-back" type="button" onClick={()=>setStep("code")}>← Назад</button><div className="account-v41-intro"><small>НОВЫЙ АККАУНТ</small><h2>Остался один шаг</h2><p>{method==="phone"?"Телефон подтверждён.":"Email подтверждён."} Для старта достаточно имени.</p></div><div className="auth-register-fields"><label className="auth-field"><span>Имя</span><input autoFocus value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})} placeholder="Имя"/></label><label className="auth-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})} placeholder="Необязательно"/></label></div><button className="primary auth-primary" disabled={!draft.name.trim()} onClick={register}>СОЗДАТЬ АККАУНТ</button></>}
    </div>}
  </aside></div>;
}

function AccountFields({draft,setDraft}:{draft:Profile;setDraft:(profile:Profile)=>void}){
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setDraft({...draft,[key]:event.target.value});
  return <div className="account-fields account-fields-v41 account-fields-v42"><label><span>Имя</span><input value={draft.name} onChange={field("name")} placeholder="Имя"/></label><label><span>Фамилия</span><input value={draft.surname} onChange={field("surname")} placeholder="Фамилия"/></label><label><span>Email</span><input type="email" value={draft.email} onChange={field("email")} placeholder="name@example.com"/></label><label><span>Телефон</span><input type="tel" value={draft.phone} onChange={field("phone")} placeholder="+7 999 000-00-00"/></label><CitySuggestField value={draft.city} onChange={city=>setDraft({...draft,city,address:city===draft.city?draft.address:""})}/><AddressSuggestField city={draft.city} value={draft.address} onChange={address=>setDraft({...draft,address})}/></div>;
}

'''
page = page[:account_start] + account_block + page[favorites_start:]

cart_start = page.find("function Cart(")
checkout_start = page.find("function Checkout(", cart_start)
if cart_start < 0 or checkout_start < 0:
    raise SystemExit("V42 cart anchors not found")

cart_block = r'''function Cart({ cart, profile, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; profile:Profile|null; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const deliveryLeft=Math.max(0,15000-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/15000*100));
  const shipping=total>=15000?0:300;
  const seedWords=(cart[0]?.name??"").toLowerCase().split(/[^а-яёa-z0-9]+/i).filter(word=>word.length>4&&!/[^(]/.test(word)).filter(word=>!["комплект","декоративная","постельного","культура","товара"].includes(word));
  const scored=products.filter(product=>!cart.some(item=>item.id===product.id)).map(product=>({product,score:seedWords.reduce((score,word)=>score+(product.name.toLowerCase().includes(word)?2:0),0)})).sort((a,b)=>b.score-a.score);
  const relatedItems=Array.from(new Map(scored.filter(row=>row.score>0).map(row=>[row.product.name,row.product])).values()).slice(0,4);
  const suggestions=relatedItems.length?relatedItems:recentItems.slice(0,4);
  return <div className="overlay cart-v41-overlay cart-v42-overlay" data-analytics-step="cart_open"><button className="overlay-bg" onClick={close} aria-label="Закрыть корзину"/><aside className="side-panel cart cart-v41 cart-v42" role="dialog" aria-modal="true" aria-label="Корзина">
    <header className="cart-v41-head cart-v42-head"><div><small>КУЛЬТУРА ДОМА</small><h1>Корзина {itemCount>0&&<span>({itemCount})</span>}</h1></div><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {cart.length===0?<div className="cart-v41-empty cart-v42-empty">{recentItems.length?<><div className="cart-v41-empty-copy"><h2>Корзина пока пуста</h2><p>Вернитесь к недавно просмотренным предметам или продолжите покупки.</p></div><section className="recent-cart cart-v41-recent"><header><span>Недавно просмотренные</span></header><div>{recentItems.map(product=><button key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><strong>{product.name}</strong><b>{fmt(product.price)}</b></button>)}</div></section><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></>:<><h2>Корзина пока пуста</h2><p>Добавьте предметы, которые хотите видеть дома.</p><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></>}</div>:<>
      <section className="cart-v42-confidence"><div><small>ДОСТАВКА БЕЗ СЮРПРИЗОВ</small><strong>{shipping===0?"Бесплатная доставка":`Доставка от ${fmt(shipping)}`}</strong><span>{shipping===0?"Порог бесплатной доставки достигнут":"Курьер по Москве — ориентировочно послезавтра"}</span></div><div className="cart-v42-progress"><span>{deliveryLeft===0?"Бесплатная доставка включена":`До бесплатной доставки ${fmt(deliveryLeft)}`}</span><i><b style={{width:`${deliveryProgress}%`}}/></i></div></section>
      <div className="cart-v41-items cart-v42-items">{cart.map((p,i)=><article className="cart-v41-item cart-v42-item" key={`${p.id}-${i}`}><button className="cart-v41-media" type="button" onClick={()=>choose(p)} aria-label={`Открыть ${p.name}`}><ScrollableProductMedia product={p} alt={`${p.name}, ${p.selectedColor}`} className="cart-item-media"/></button><div className="cart-item-copy cart-v41-copy"><small>КУЛЬТУРА ДОМА</small><button className="cart-v41-title" type="button" onClick={()=>choose(p)}>{p.name}</button><div className="cart-v41-variants"><span>Цвет: {p.selectedColor}</span><span data-cart-controls="CART_CONTROLS_V19">Размер: {p.selectedSize}</span></div>{isGiftPackagingAvailable(p)&&<label className="cart-gift-checkbox cart-v41-gift"><input type="checkbox" checked={Boolean(p.giftWrap)} onChange={event=>update(i,{giftWrap:event.target.checked})}/><span>Подарочная упаковка</span></label>}<div className="cart-item-bottom cart-v41-item-bottom"><QuantityControl quantity={p.quantity} setQuantity={quantity=>update(i,{quantity})}/><b>{fmt(p.price*p.quantity)}</b></div><button className="cart-v41-remove" onClick={()=>remove(i)}>Удалить</button></div></article>)}</div>
      {suggestions.length>0&&<section className="cart-v42-crosssell" data-analytics-step="cart_cross_sell"><header><div><small>ДОПОЛНИТЕ КОМПЛЕКТ</small><h2>Подойдёт к вашему выбору</h2></div><span>Средний заказ сейчас — 1,77 товара</span></header><div>{suggestions.map(product=><article key={product.id}><button className="cart-v42-cross-media" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/></button><div><button onClick={()=>choose(product)}>{product.name}</button><b>{fmt(product.price)}</b><button className="cart-v42-add" onClick={()=>quickAdd(product)}>Добавить</button></div></article>)}</div></section>}
      <footer className="cart-v41-footer cart-v42-footer"><div className="cart-v42-loyalty"><span>{profile?"Ваш баланс":"Бонусная программа"}</span><b>{profile?"0 бонусов":"Войдите, чтобы видеть бонусы"}</b></div><div className="cart-v41-total"><span>Товары</span><b>{fmt(total)}</b></div><div className="cart-v42-delivery-total"><span>Доставка</span><b>{shipping===0?"Бесплатно":`от ${fmt(shipping)}`}</b></div><p>Точная стоимость и дата подтверждаются до оплаты — без неожиданных доплат.</p><button className="primary checkout-cta" data-analytics-step="checkout_start" onClick={checkout}>ОФОРМИТЬ ЗАКАЗ</button><button className="cart-v41-continue" onClick={go}>Продолжить покупки</button></footer>
    </>}
  </aside></div>;
}

'''
page = page[:cart_start] + cart_block + page[checkout_start:]

checkout_start = page.find("function Checkout(")
checkout_map_start = page.find("function CheckoutMap(", checkout_start)
if checkout_start < 0 or checkout_map_start < 0:
    raise SystemExit("V42 checkout anchors not found")

checkout_block = r'''function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  const [delivery,setDelivery]=useState<"courier"|"pickup">("courier");
  const [payment,setPayment]=useState<"card"|"sbp"|"upon">("card");
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

  const shipping=delivery==="pickup"||total>=15000?0:300;
  const online=payment==="card"||payment==="sbp";
  const onlineDiscount=online?Math.round(total*.03):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const expensive=payable>=30000;
  const pvz=KD_PVZ_POINTS[form.city]??[];
  const phoneDigits=form.phone.replace(/\D/g,"");
  const phoneOk=profile?phoneDigits.length>=10:phoneDigits.length>=10&&phoneVerified;
  const contactOk=form.name.trim().length>0&&phoneOk&&(form.email.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim()));
  const deliveryOk=delivery==="courier"?(form.city.trim().length>0&&form.address.trim().length>3):(form.city.trim().length>0&&pickupPoint.length>0);
  const canSubmit=contactOk&&deliveryOk&&agreed;
  const requestPhoneCode=()=>{if(phoneDigits.length<10)return;setCodeSent(true);setPhoneCode("")};
  const verifyPhone=()=>{if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false)}};
  const applyPromo=()=>{setPromoStatus(promo.trim()?"Промокод принят для проверки при подтверждении заказа":"Введите промокод")};
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:event.target.value});

  return <div className="checkout checkout-v41 checkout-v42" data-analytics-step="checkout_view">
    <header className="checkout-v41-head checkout-v42-head"><button onClick={close} aria-label="Закрыть оформление"><Icon name="close"/></button><b>КУЛЬТУРА ДОМА</b><span>Без регистрации · один экран</span></header>
    <form className="checkout-v41-form checkout-v42-form" onSubmit={event=>{event.preventDefault();if(canSubmit)submit()}}>
      <main className="checkout-v41-main checkout-v42-main">
        <div className="checkout-v41-heading checkout-v42-heading"><small>ОФОРМЛЕНИЕ ЗАКАЗА</small><h1>Один экран — только необходимое</h1><p>Контакты, доставка и оплата остаются перед глазами. Стоимость доставки и итог известны до подтверждения.</p></div>

        <section className="checkout-v41-section checkout-v42-section" data-analytics-step="checkout_contacts"><div className="checkout-v41-step"><i>01</i><div><h2>Контакты</h2><p>{profile?"Данные подставлены из личного кабинета.":"Гостевой заказ без обязательной регистрации."}</p></div></div><div className="checkout-v42-fields"><label><span>Имя *</span><input value={form.name} onChange={field("name")} autoComplete="given-name" placeholder="Имя"/></label><label><span>Фамилия</span><input value={form.surname} onChange={field("surname")} autoComplete="family-name" placeholder="Необязательно"/></label><label className="checkout-v42-phone"><span>Телефон *</span><div><input value={form.phone} onChange={event=>{setForm({...form,phone:event.target.value});if(!profile)setPhoneVerified(false)}} autoComplete="tel" inputMode="tel" placeholder="+7 999 000-00-00"/>{!profile&&phoneDigits.length>=10&&!phoneVerified&&<button type="button" onClick={requestPhoneCode}>Подтвердить</button>}{phoneVerified&&<b>✓ Подтверждён</b>}</div></label><label><span>Email</span><input type="email" value={form.email} onChange={field("email")} autoComplete="email" placeholder="Для чека и статусов"/></label>{!profile&&codeSent&&!phoneVerified&&<div className="checkout-v42-otp"><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000"/><button type="button" onClick={verifyPhone}>Подтвердить номер</button><small>Демо-код: 1234</small></div>}</div></section>

        <section className="checkout-v41-section checkout-v42-section" data-analytics-step="checkout_delivery"><div className="checkout-v41-step"><i>02</i><div><h2>Доставка</h2><p>{shipping===0?"Бесплатная доставка для этого заказа.":"Курьерская доставка от 300 ₽ — стоимость известна заранее."}</p></div></div><div className="checkout-v42-choice"><button type="button" className={delivery==="courier"?"active":""} onClick={()=>setDelivery("courier")}><b>Курьер</b><span>{total>=15000?"Бесплатно":"от 300 ₽"}</span></button><button type="button" className={delivery==="pickup"?"active":""} onClick={()=>setDelivery("pickup")}><b>Пункт выдачи</b><span>Выбрать рядом</span></button></div><div className="checkout-v42-address"><CitySuggestField value={form.city} required onChange={city=>{setForm({...form,city,address:city===form.city?form.address:""});setPickupPoint("")}}/>{delivery==="courier"?<><AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm({...form,address})}/><label className="checkout-v42-access"><span>Квартира, подъезд, домофон</span><input value={access} onChange={event=>setAccess(event.target.value)} placeholder="Необязательно"/></label><div className="checkout-v42-slots"><small>Удобное время</small><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}>{value}{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div></>:<div className="checkout-v42-pvz"><header><span>Пункты выдачи</span><small>Доступность уточняется при подтверждении</small></header>{pvz.length?pvz.map(point=><button type="button" key={point} className={pickupPoint===point?"active":""} onClick={()=>setPickupPoint(point)}><i/><div><b>{point}</b><span>{form.city}</span></div></button>):<p>Введите город — покажем доступные варианты.</p>}</div>}</div></section>

        <section className="checkout-v41-section checkout-v42-section" data-analytics-step="checkout_payment"><div className="checkout-v41-step"><i>03</i><div><h2>Оплата</h2><p>Онлайн-оплата в прототипе получает −3% — гипотеза на снижение отмен.</p></div></div><div className="checkout-v42-payments"><button type="button" className={payment==="card"?"active":""} onClick={()=>setPayment("card")}><span>Банковская карта</span><b>−3%</b></button><button type="button" className={payment==="sbp"?"active":""} onClick={()=>setPayment("sbp")}><span>СБП</span><b>−3%</b></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><span>При получении</span><small>Без скидки</small></button></div>{expensive&&<aside className="checkout-v42-concierge"><small>ЗАКАЗ ОТ 30 000 ₽</small><b>Персональное сопровождение</b><p>Менеджер свяжется в течение часа, подтвердит наличие, сроки и детали доставки.</p></aside>}<button type="button" className="checkout-v42-promo-toggle" onClick={()=>setPromoOpen(!promoOpen)}>Промокод или подарочный сертификат <span>{promoOpen?"−":"+"}</span></button>{promoOpen&&<div className="checkout-v42-promo"><input value={promo} onChange={event=>{setPromo(event.target.value);setPromoStatus("")}} placeholder="Введите код"/><button type="button" onClick={applyPromo}>Применить</button>{promoStatus&&<small>{promoStatus}</small>}</div>}<label className="checkout-v42-notifications"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Сообщать: заказ принят → собран → передан курьеру → доставлен</span></label></section>

        <label className="checkout-v42-agree"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Согласен(на) с условиями продажи и обработкой персональных данных.</span></label>
      </main>
      <aside className="checkout-v41-summary checkout-v42-summary"><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header><div className="checkout-v42-summary-items">{cart.slice(0,4).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v42-summary-media"/><div><b>{item.name}</b><span>{item.selectedColor} · {item.selectedSize}</span><small>{item.quantity} × {fmt(item.price)}</small></div></article>)}</div>{cart.length>4&&<p className="checkout-v42-more">Ещё {cart.length-4} поз.</p>}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div>{onlineDiscount>0&&<div className="checkout-v42-discount"><dt>Онлайн-оплата −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}<div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div></dl><div className="checkout-v42-final"><span>Итого</span><b>{fmt(payable)}</b></div>{profile?<div className="checkout-v42-bonus"><span>Бонусный баланс</span><b>0 бонусов</b></div>:<p className="checkout-v42-login-note">После входа бонусный баланс будет виден здесь и в корзине.</p>}<button type="submit" className="primary checkout-v42-submit" disabled={!canSubmit}>ПОДТВЕРДИТЬ ЗАКАЗ · {fmt(payable)}</button>{!phoneOk&&!profile&&<small className="checkout-v42-error">Подтвердите номер телефона коротким кодом.</small>}{!deliveryOk&&<small className="checkout-v42-error">Заполните доставку: город и {delivery==="courier"?"адрес":"пункт выдачи"}.</small>}<p className="checkout-v42-safe">Ничего не списывается в этом демонстрационном прототипе.</p></aside>
    </form>
  </div>;
}

'''
page = page[:checkout_start] + checkout_block + page[checkout_map_start:]

old_cart_call = '''{cartOpen && <Cart cart={cart} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} />}'''
new_cart_call = '''{cartOpen && <Cart cart={cart} profile={profile} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} quickAdd={(product)=>{setCartOpen(false);setPlpSize(product)}} />}'''
if old_cart_call in page:
    page = page.replace(old_cart_call,new_cart_call,1)
elif "<Cart cart={cart} profile={profile}" not in page:
    raise SystemExit("V42 cart call anchor not found")

page_path.write_text(page,encoding="utf-8")
print("Applied hypothesis-driven commerce V42")
