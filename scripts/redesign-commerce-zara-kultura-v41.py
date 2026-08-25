from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

marker = "COMMERCE_ZARA_KULTURA_V41"

account_start = page.find("function Account(")
account_fields_start = page.find("function AccountFields(", account_start)
favorites_start = page.find("function Favorites(", account_fields_start)
if account_start < 0 or account_fields_start < 0 or favorites_start < 0:
    raise SystemExit("V41 account anchors not found")

account_block = r'''function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  // AUTH_FLOW_V20
  // COMMERCE_ZARA_KULTURA_V41
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

  useEffect(()=>{
    if(profile){setDraft(profile);setMode("profile")}
  },[profile]);

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

  return <div className="overlay auth-overlay commerce-v41-account-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть личный кабинет"/><aside className="side-panel account auth-v20 account-v41" role="dialog" aria-modal="true" aria-label="Личный кабинет">
    <header className="account-v41-head"><div><small>КУЛЬТУРА ДОМА</small><h1>Личный кабинет</h1></div><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {mode==="profile"?<div className="account-v41-profile">
      <div className="account-v41-welcome"><small>ПРОФИЛЬ</small><h2>{draft.name?`Здравствуйте, ${draft.name}`:"Ваш профиль"}</h2><p>Контактные данные и адрес автоматически подставятся при оформлении заказа.</p></div>
      <section className="account-v41-section"><header><span>Личные данные</span><small>Можно изменить в любой момент</small></header><AccountFields draft={draft} setDraft={setDraft}/></section>
      <section className="account-v41-glance" aria-label="Данные профиля"><div><span>Адрес доставки</span><b>{draft.address?`${draft.city}, ${draft.address}`:draft.city||"Не указан"}</b></div><div><span>Связь</span><b>{draft.phone||draft.email||"Не указана"}</b></div></section>
      <div className="account-v41-actions"><button className="primary auth-primary" onClick={saveProfile}>СОХРАНИТЬ ИЗМЕНЕНИЯ</button><button className="link auth-logout" onClick={signOut}>Выйти из аккаунта</button></div>
    </div>:<div className="auth-flow account-v41-auth">
      {step==="identify"&&<><div className="account-v41-intro"><small>ВХОД И РЕГИСТРАЦИЯ</small><h2>Войти в аккаунт</h2><p>Сохраняйте данные для оформления заказа и быстрее возвращайтесь к покупкам.</p></div><div className="auth-methods" role="tablist" aria-label="Способ входа"><button type="button" role="tab" aria-selected={method==="phone"} className={method==="phone"?"active":""} onClick={()=>switchMethod("phone")}>Телефон</button><button type="button" role="tab" aria-selected={method==="email"} className={method==="email"?"active":""} onClick={()=>switchMethod("email")}>Email</button></div><label className="auth-field"><span>{method==="phone"?"Номер телефона":"Email"}</span><input type={method==="phone"?"tel":"email"} autoComplete={method==="phone"?"tel":"email"} inputMode={method==="phone"?"tel":"email"} value={identifier} onChange={event=>setIdentifier(event.target.value)} placeholder={method==="phone"?"+7 999 000-00-00":"name@example.com"} onKeyDown={event=>{if(event.key==="Enter")requestCode()}}/></label><button className="primary auth-primary" disabled={!identifier.trim()} onClick={requestCode}>ПОЛУЧИТЬ КОД</button><p className="auth-legal">Продолжая, вы соглашаетесь с условиями обработки персональных данных.</p></>}
      {step==="code"&&<><button className="auth-back" type="button" onClick={()=>{setStep("identify");setCode("")}}>← Назад</button><div className="account-v41-intro"><small>ПОДТВЕРЖДЕНИЕ</small><h2>Введите код</h2><p>Мы отправили код на {contactLabel} <b>{identifier}</b>.</p></div><label className="auth-field auth-code-field"><span>Код подтверждения</span><input autoFocus inputMode="numeric" autoComplete="one-time-code" maxLength={4} value={code} onChange={event=>setCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000" onKeyDown={event=>{if(event.key==="Enter")verifyCode()}}/></label><button className="primary auth-primary" disabled={code.length!==4} onClick={verifyCode}>ПРОДОЛЖИТЬ</button><button className="link auth-resend" type="button" onClick={requestCode}>Отправить код ещё раз</button><p className="auth-demo-note">Демо-код: 1234</p></>}
      {step==="register"&&<><button className="auth-back" type="button" onClick={()=>setStep("code")}>← Назад</button><div className="account-v41-intro"><small>НОВЫЙ АККАУНТ</small><h2>Остался один шаг</h2><p>{method==="phone"?"Телефон подтверждён.":"Email подтверждён."} Укажите имя — остальные данные можно заполнить позже.</p></div><div className="auth-register-fields"><label className="auth-field"><span>Имя</span><input autoFocus value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})} placeholder="Имя"/></label><label className="auth-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})} placeholder="Необязательно"/></label>{method==="phone"?<label className="auth-field"><span>Email</span><input type="email" value={draft.email} onChange={event=>setDraft({...draft,email:event.target.value})} placeholder="Необязательно"/></label>:<label className="auth-field"><span>Телефон</span><input type="tel" value={draft.phone} onChange={event=>setDraft({...draft,phone:event.target.value})} placeholder="Необязательно"/></label>}</div><button className="primary auth-primary" disabled={!draft.name.trim()} onClick={register}>СОЗДАТЬ АККАУНТ</button></>}
    </div>}
  </aside></div>;
}

function AccountFields({draft,setDraft}:{draft:Profile;setDraft:(profile:Profile)=>void}){
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setDraft({...draft,[key]:event.target.value});
  return <div className="account-fields account-fields-v41"><label><span>Имя</span><input value={draft.name} onChange={field("name")} placeholder="Имя"/></label><label><span>Фамилия</span><input value={draft.surname} onChange={field("surname")} placeholder="Фамилия"/></label><label><span>Email</span><input type="email" value={draft.email} onChange={field("email")} placeholder="name@example.com"/></label><label><span>Телефон</span><input type="tel" value={draft.phone} onChange={field("phone")} placeholder="+7 999 000-00-00"/></label><label><span>Город</span><input value={draft.city} onChange={field("city")} placeholder="Город"/></label><label><span>Адрес</span><input value={draft.address} onChange={field("address")} placeholder="Улица, дом, квартира"/></label></div>;
}

'''
page = page[:account_start] + account_block + page[favorites_start:]

cart_start = page.find("function Cart(")
checkout_start = page.find("function Checkout(", cart_start)
if cart_start < 0 or checkout_start < 0:
    raise SystemExit("V41 cart anchors not found")

cart_block = r'''function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const deliveryLeft=Math.max(0,15000-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/15000*100));
  return <div className="overlay cart-v41-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть корзину"/><aside className="side-panel cart cart-v41" role="dialog" aria-modal="true" aria-label="Корзина">
    <header className="cart-v41-head"><div><small>КУЛЬТУРА ДОМА</small><h1>Корзина {itemCount>0&&<span>({itemCount})</span>}</h1></div><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {cart.length===0?<div className="cart-v41-empty">{recentItems.length?<><div className="cart-v41-empty-copy"><h2>Корзина пока пуста</h2><p>Вернитесь к недавно просмотренным предметам или продолжите покупки.</p></div><section className="recent-cart cart-v41-recent"><header><span>Недавно просмотренные</span></header><div>{recentItems.map(product=><button key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><strong>{product.name}</strong><b>{fmt(product.price)}</b></button>)}</div></section><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></>:<><h2>Корзина пока пуста</h2><p>Добавьте предметы, которые хотите видеть дома.</p><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></>}</div>:<>
      <section className="cart-v41-delivery" aria-label="Бесплатная доставка"><div><span>{deliveryLeft===0?"Бесплатная доставка включена":`До бесплатной доставки ${fmt(deliveryLeft)}`}</span><small>Бесплатно от 15 000 ₽</small></div><i><b style={{width:`${deliveryProgress}%`}}/></i></section>
      <div className="cart-items cart-v41-items">{cart.map((p,i)=><article className="cart-v41-item" key={`${p.id}-${i}`}><button className="cart-v41-media" type="button" onClick={()=>choose(p)} aria-label={`Открыть ${p.name}`}><ScrollableProductMedia product={p} alt={`${p.name}, ${p.selectedColor}`} className="cart-item-media"/></button><div className="cart-item-copy cart-v41-copy"><small>КУЛЬТУРА ДОМА</small><button className="cart-v41-title" type="button" onClick={()=>choose(p)}>{p.name}</button><div className="cart-v41-variants"><span>Цвет: {p.selectedColor}</span><span data-cart-controls="CART_CONTROLS_V19">Размер: {p.selectedSize}</span></div>{isGiftPackagingAvailable(p)&&<label className="cart-gift-checkbox cart-v41-gift"><input type="checkbox" checked={Boolean(p.giftWrap)} onChange={event=>update(i,{giftWrap:event.target.checked})} aria-label={`Подарочная упаковка для ${p.name}`}/><span>Подарочная упаковка</span></label>}<div className="cart-item-bottom cart-v41-item-bottom"><QuantityControl quantity={p.quantity} setQuantity={quantity=>update(i,{quantity})}/><b>{fmt(p.price*p.quantity)}</b></div><button className="cart-v41-remove" type="button" onClick={()=>remove(i)}>Удалить</button></div></article>)}</div>
      <footer className="cart-v41-footer"><div className="cart-v41-total"><span>Итого</span><b>{fmt(total)}</b></div><p>Доставка рассчитывается на следующем шаге.</p><button className="primary checkout-cta" onClick={checkout}>ОФОРМИТЬ ЗАКАЗ</button><button className="cart-v41-continue" type="button" onClick={go}>Продолжить покупки</button></footer>
    </>}
  </aside></div>;
}

'''
page = page[:cart_start] + cart_block + page[checkout_start:]

checkout_start = page.find("function Checkout(")
checkout_map_start = page.find("function CheckoutMap(", checkout_start)
if checkout_start < 0 or checkout_map_start < 0:
    raise SystemExit("V41 checkout anchors not found")

checkout_block = r'''function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  const [delivery,setDelivery]=useState<"courier"|"pickup">("courier");
  const [payment,setPayment]=useState<"card"|"upon">("card");
  const [agreed,setAgreed]=useState(true);
  const [mapPoint,setMapPoint]=useState("Петровка, 12");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const deliveryPrice=delivery==="courier"&&total<15000?690:0;
  const finalTotal=total+deliveryPrice;
  const handleSubmit=(event:React.FormEvent)=>{event.preventDefault();if(!agreed){alert("Подтвердите согласие с условиями заказа");return}submit()};
  const setField=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:event.target.value});
  const points=delivery==="pickup"?["Петровка, 12","Кутузовский проспект, 48","Большая Конюшенная, 12"]:["Петровка, 12","Арбат, 20","Большая Ордынка, 31"];
  useEffect(()=>{setMapPoint(points[0])},[delivery]);
  return <div className="checkout-overlay checkout-v41" role="dialog" aria-modal="true" aria-label="Оформление заказа">
    <header className="checkout-v41-head"><button onClick={close} aria-label="Закрыть оформление"><Icon name="close"/></button><b>КУЛЬТУРА ДОМА</b><nav aria-label="Этапы оформления"><span className="active">01 Контакты</span><span>02 Доставка</span><span>03 Оплата</span></nav></header>
    <form className="checkout-v41-form" onSubmit={handleSubmit}>
      <div className="checkout-main checkout-v41-main"><div className="checkout-heading checkout-v41-heading"><small>ОФОРМЛЕНИЕ ЗАКАЗА</small><h1>Завершите заказ</h1><p>Заполните данные, выберите способ получения и оплаты.</p></div>
        <section className="checkout-section checkout-v41-section"><div className="checkout-step checkout-v41-step"><i>01</i><div><h2>Контактные данные</h2><p>Для подтверждения заказа и связи с вами.</p></div></div><div className="checkout-fields checkout-v41-fields"><label><span>Имя</span><input value={form.name} onChange={setField("name")} name="name" autoComplete="given-name" required/></label><label><span>Фамилия</span><input value={form.surname} onChange={setField("surname")} name="surname" autoComplete="family-name" required/></label><label><span>Email</span><input value={form.email} onChange={setField("email")} type="email" name="email" autoComplete="email" required/></label><label><span>Телефон</span><input value={form.phone} onChange={setField("phone")} type="tel" name="phone" autoComplete="tel" placeholder="+7 999 000-00-00" required/></label></div></section>
        <section className="checkout-section checkout-v41-section"><div className="checkout-step checkout-v41-step"><i>02</i><div><h2>Способ получения</h2><p>Выберите доставку или самовывоз из бутика.</p></div></div><div className="checkout-options checkout-v41-options"><label className={delivery==="courier"?"active":""}><input type="radio" name="delivery" checked={delivery==="courier"} onChange={()=>setDelivery("courier")}/><span><b>Курьерская доставка</b><small>{total>=15000?"Бесплатно":"690 ₽"} · 1–3 дня</small></span><em>→</em></label><label className={delivery==="pickup"?"active":""}><input type="radio" name="delivery" checked={delivery==="pickup"} onChange={()=>setDelivery("pickup")}/><span><b>Самовывоз из бутика</b><small>Бесплатно · сегодня</small></span><em>→</em></label></div>{delivery==="courier"&&<div className="checkout-address checkout-v41-address"><label><span>Город</span><input value={form.city} onChange={setField("city")} name="city" required/></label><label><span>Улица и дом</span><input value={form.address} onChange={setField("address")} name="address" required/></label><label><span>Квартира</span><input name="flat"/></label><label><span>Комментарий курьеру</span><input name="comment"/></label></div>}<CheckoutMap points={points} selected={mapPoint} choose={(point)=>{setMapPoint(point);if(delivery==="courier")setForm({...form,address:point})}} mode={delivery}/></section>
        <section className="checkout-section checkout-v41-section"><div className="checkout-step checkout-v41-step"><i>03</i><div><h2>Оплата</h2><p>Выберите удобный способ оплаты.</p></div></div><div className="checkout-options checkout-v41-options"><label className={payment==="card"?"active":""}><input type="radio" name="payment" checked={payment==="card"} onChange={()=>setPayment("card")}/><span><b>Банковской картой онлайн</b><small>МИР · Visa · Mastercard</small></span><em>→</em></label><label className={payment==="upon"?"active":""}><input type="radio" name="payment" checked={payment==="upon"} onChange={()=>setPayment("upon")}/><span><b>При получении</b><small>Картой или наличными</small></span><em>→</em></label></div></section>
      </div>
      <aside className="checkout-summary checkout-v41-summary"><div className="summary-title"><div><small>ВАШ ЗАКАЗ</small><h2>{cart.reduce((sum,item)=>sum+item.quantity,0)} {cart.reduce((sum,item)=>sum+item.quantity,0)===1?"товар":"товара"}</h2></div><button type="button" onClick={editCart}>Изменить</button></div><div className="summary-items checkout-v41-items">{cart.map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-item-media"/><div><strong>{item.name}</strong><span>{item.selectedColor}</span><span>Размер: {item.selectedSize}</span><span>Количество: {item.quantity}</span>{item.giftWrap&&<small>Подарочная упаковка</small>}<b>{fmt(item.price*item.quantity)}</b></div></article>)}</div><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Получение</dt><dd>{delivery==="pickup"?`Бутик: ${mapPoint}`:mapPoint}</dd></div><div><dt>Доставка</dt><dd>{deliveryPrice?fmt(deliveryPrice):"Бесплатно"}</dd></div><div className="summary-total"><dt>Итого</dt><dd>{fmt(finalTotal)}</dd></div></dl><label className="checkout-consent checkout-v41-consent"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен с условиями продажи и политикой конфиденциальности</span></label><button className="primary checkout-v41-submit" type="submit">ПОДТВЕРДИТЬ ЗАКАЗ · {fmt(finalTotal)}</button><small className="checkout-security">Данные заказа защищены. Оплата проходит на безопасной странице банка.</small></aside>
    </form>
  </div>;
}

'''
page = page[:checkout_start] + checkout_block + page[checkout_map_start:]

page_path.write_text(page, encoding="utf-8")
print("Commerce Zara Kultura V41 applied")
