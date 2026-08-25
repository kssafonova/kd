from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "page.tsx"
text = path.read_text(encoding="utf-8")

if "CART_CHECKOUT_MOCKUP_V69" in text:
    print("Cart / checkout V69 already applied")
    raise SystemExit(0)

# Keep the existing cart business logic, but align copy and give the surface a
# dedicated final design hook for the supplied mobile reference.
text = text.replace('className="cart-v43" role="dialog"', 'className="cart-v43 cart-v69" role="dialog"', 1)
text = text.replace('<h1>Ваш выбор <span>{itemCount}</span></h1>', '<h1>Корзина <span>{itemCount} товаров</span></h1>', 1)
text = text.replace('<small>ДОПОЛНИТЕ КОМПЛЕКТ</small><h2>Может подойти к вашему выбору</h2>', '<small>ДОПОЛНИТЕ ИНТЕРЬЕР</small><h2>До полного образа</h2>', 1)

start = text.index("function Checkout({cart,total,profile,close,editCart,submit}")
end = text.index("\nfunction CheckoutMap(", start)

new_checkout = r'''// CART_CHECKOUT_MOCKUP_V69
function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type DeliveryMethod="courier"|"store"|"pvz";
  type PaymentMethod="online"|"upon";
  const [delivery,setDelivery]=useState<DeliveryMethod>("courier");
  const [payment,setPayment]=useState<PaymentMethod>("online");
  const [recipientName,setRecipientName]=useState(profile?.name??"");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [registeredChoice,setRegisteredChoice]=useState<""|"account"|"guest">("");
  const [submitAttempted,setSubmitAttempted]=useState(false);
  const [notifications,setNotifications]=useState(true);
  const [agreed,setAgreed]=useState(false);
  const [slot,setSlot]=useState("18:00–22:00");
  const [entrance,setEntrance]=useState("");
  const [floor,setFloor]=useState("");
  const [flat,setFlat]=useState("");
  const [pickupPoint,setPickupPoint]=useState("");
  const [storePoint,setStorePoint]=useState("");
  const [pvzQuery,setPvzQuery]=useState("");

  const storePoints:Record<string,string[]>={
    "Москва":["Культура Дома · Петровка"],
    "Санкт-Петербург":["Культура Дома · Невский проспект"],
    "Казань":["Культура Дома · улица Баумана"],
  };
  const pvz=KD_PVZ_POINTS[form.city]??[];
  const stores=storePoints[form.city]??[];
  const filteredPvz=pvz.filter(point=>!pvzQuery.trim()||point.toLocaleLowerCase("ru-RU").includes(pvzQuery.trim().toLocaleLowerCase("ru-RU")));
  const phoneDigits=form.phone.replace(/\D/g,"");
  const profileDigits=(profile?.phone||"").replace(/\D/g,"");
  const demoRegisteredDigits="79261234567";
  const registeredNumber=phoneDigits.length>=10&&(phoneDigits===profileDigits||phoneDigits===demoRegisteredDigits);
  const registeredName=profile?.name?`${profile.name}${profile.surname?` ${profile.surname.slice(0,1)}.`:""}`:"Анна И.";
  const emailOk=!form.email.trim()||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const phoneOk=phoneDigits.length>=10&&phoneVerified;
  const contactOk=recipientName.trim().length>1&&phoneOk&&emailOk;
  const deliveryOk=delivery==="courier"
    ? Boolean(form.city.trim()&&form.address.trim().length>3)
    : delivery==="store"?Boolean(form.city.trim()&&storePoint):Boolean(form.city.trim()&&pickupPoint);
  const onlineDiscount=payment==="online"?Math.round(total*.03):0;
  const shipping=delivery==="courier"?(total>=15000?0:300):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const canSubmit=contactOk&&deliveryOk&&agreed;
  const selectedPoint=delivery==="store"?storePoint:pickupPoint;
  const recipientFull=[recipientName.trim(),form.surname.trim()].filter(Boolean).join(" ");
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);

  const setPhone=(value:string)=>{
    const digits=value.replace(/\D/g,"");
    setForm(current=>({...current,phone:value}));
    setPhoneVerified(Boolean(profileDigits&&digits===profileDigits));
    setCodeSent(false);setPhoneCode("");setOtpError("");setRegisteredChoice("");
  };
  const requestPhoneCode=()=>{
    if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}
    setCodeSent(true);setPhoneCode("");setOtpError("");
  };
  const verifyPhone=()=>{
    if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}
    else setOtpError("Неверный код. В прототипе используйте 1234");
  };
  const continueWithAccount=()=>{setRegisteredChoice("account");setPhoneVerified(true);setCodeSent(false);setOtpError("")};
  const continueAsGuest=()=>{setRegisteredChoice("guest");if(!phoneVerified){setCodeSent(true);setPhoneCode("");setOtpError("")}};
  const chooseCity=(city:string)=>{setForm(current=>({...current,city,address:city===current.city?current.address:""}));setPickupPoint("");setStorePoint("");setPvzQuery("")};
  const chooseDelivery=(method:DeliveryMethod)=>{
    setDelivery(method);
    if(method==="pvz"&&!pickupPoint&&pvz[0])setPickupPoint(pvz[0]);
    if(method==="store"&&!storePoint&&stores[0])setStorePoint(stores[0]);
  };
  const submitOrder=()=>{setSubmitAttempted(true);if(canSubmit)submit()};

  return <div className="checkout checkout-v69" data-analytics-step="checkout_view">
    <header className="checkout-v69-head"><button type="button" onClick={close} aria-label="Вернуться в корзину">←</button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={editCart} aria-label="Открыть корзину"><Icon name="bag"/></button></header>

    <form className="checkout-v69-layout" onSubmit={event=>{event.preventDefault();submitOrder()}}>
      <main className="checkout-v69-main">
        <header className="checkout-v69-title"><h1>Оформление заказа</h1></header>

        <section className="checkout-v69-section checkout-v69-contacts" aria-labelledby="v69-contact-title">
          <h2 id="v69-contact-title">Контактные данные</h2>
          <div className="checkout-v69-fields checkout-v69-name-row">
            <label><span>Имя получателя *</span><input value={recipientName} onChange={event=>setRecipientName(event.target.value)} autoComplete="given-name" placeholder="Имя"/></label>
            <label><span>Фамилия</span><input value={form.surname} onChange={event=>setForm(current=>({...current,surname:event.target.value}))} autoComplete="family-name" placeholder="Необязательно"/></label>
          </div>
          <label className={`checkout-v69-field checkout-v69-phone ${phoneVerified?"is-verified":""}`}><span>Контактный телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} inputMode="tel" autoComplete="tel" placeholder="+7 999 000-00-00"/>{phoneVerified?<b>✓</b>:phoneDigits.length>=10?<button type="button" onClick={requestPhoneCode}>Получить код</button>:null}</div></label>

          {registeredNumber&&!registeredChoice&&<aside className="checkout-v69-account-note"><div><span>ⓘ</span><p>Этот номер привязан к аккаунту <b>{registeredName}</b>. Если продолжить как гость, заказ не появится в личном кабинете, а бонусы не начислятся автоматически.</p></div><button type="button" className="primary" onClick={continueWithAccount}>ВОЙТИ В АККАУНТ <em>(рекомендуем)</em></button><button type="button" onClick={continueAsGuest}>ВСЁ РАВНО ПРОДОЛЖИТЬ КАК ГОСТЬ</button></aside>}
          {registeredNumber&&registeredChoice&&<button type="button" className="checkout-v69-account-change" onClick={()=>setRegisteredChoice("")}>{registeredChoice==="account"?"Оформление с аккаунтом":"Продолжаем как гость"} · изменить</button>}

          {codeSent&&!phoneVerified&&<div className="checkout-v69-otp"><label><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></label><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}

          <label className="checkout-v69-field"><span>Email для уведомлений</span><input type="email" value={form.email} onChange={event=>setForm(current=>({...current,email:event.target.value}))} autoComplete="email" placeholder="example@mail.ru"/></label>
          <label className="checkout-v69-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Хочу получать статус заказа и уведомления</span></label>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v69-delivery-title">
          <h2 id="v69-delivery-title">Способ получения</h2>
          <div className="checkout-v69-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>chooseDelivery("courier")}><span>▱</span><b>Курьером</b><small>2–3 дня · {shipping===0?"0 ₽":"300 ₽"}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>chooseDelivery("store")}><span>⌂</span><b>Самовывоз</b><small>2–3 дня · 0 ₽</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>chooseDelivery("pvz")}><span>▦</span><b>ПВЗ</b><small>2–3 дня · 0 ₽</small></button>
          </div>

          <div className="checkout-v69-delivery-body">
            <CitySuggestField value={form.city} required onChange={chooseCity}/>

            {delivery==="courier"&&<>
              <AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm(current=>({...current,address}))}/>
              <div className="checkout-v69-address-parts"><label><span>Подъезд</span><input value={entrance} onChange={event=>setEntrance(event.target.value)} placeholder="2"/></label><label><span>Этаж</span><input value={floor} onChange={event=>setFloor(event.target.value)} placeholder="3"/></label><label><span>Квартира</span><input value={flat} onChange={event=>setFlat(event.target.value)} placeholder="8"/></label></div>
              <div className="checkout-v69-map-block"><div className="checkout-v69-map-caption"><b>Адрес на карте</b><span>{form.address?`${form.city}, ${form.address}`:form.city}</span></div><CheckoutMap points={[form.address?`${form.city}, ${form.address}`:form.city]} selected={form.address?`${form.city}, ${form.address}`:form.city} choose={()=>{}} mode="courier"/></div>
              <div className="checkout-v69-slots"><span>Время доставки</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div>
            </>}

            {delivery==="store"&&<div className="checkout-v69-pickup"><h3>Выберите бутик</h3>{stores.length?stores.map(point=><button type="button" key={point} className={storePoint===point?"active":""} onClick={()=>setStorePoint(point)}><i/><span><b>{point}</b><small>{form.city} · ежедневно</small></span></button>):<p>В этом городе пока нет доступного самовывоза.</p>}{stores.length>0&&<div className="checkout-v69-map-block"><CheckoutMap points={stores} selected={storePoint} choose={setStorePoint} mode="pickup"/></div>}</div>}

            {delivery==="pvz"&&<div className="checkout-v69-pvz"><label className="checkout-v69-pvz-search"><Icon name="search"/><input value={pvzQuery} onChange={event=>setPvzQuery(event.target.value)} placeholder="Введите адрес или станцию метро"/><Icon name="pin"/></label><div className="checkout-v69-map-block"><CheckoutMap points={filteredPvz.slice(0,5)} selected={pickupPoint} choose={setPickupPoint} mode="pickup"/></div>{selectedPoint&&<div className="checkout-v69-selected-point"><i/><span><b>{selectedPoint}</b><small>Готовность к выдаче: завтра, 09:00–20:00</small></span></div>}</div>}
          </div>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v69-payment-title">
          <h2 id="v69-payment-title">Способ оплаты</h2>
          <div className="checkout-v69-payments"><button type="button" className={payment==="online"?"active":""} onClick={()=>setPayment("online")}><i/><span><b>Онлайн — картой / СБП <mark>−3%</mark></b><small>−3% при оплате сейчас</small></span></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><span><b>При получении</b><small>Картой или наличными</small></span></button></div>
        </section>

        <section className="checkout-v69-section checkout-v69-order" aria-labelledby="v69-order-title">
          <div className="checkout-v69-order-head"><h2 id="v69-order-title">Состав заказа</h2><button type="button" onClick={editCart}>Изменить</button></div>
          <dl><div><dt>{itemCount} товаров</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div className="discount"><dt>Скидка при онлайн-оплате</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl>
          <div className="checkout-v69-total"><span>Итого</span><b>{fmt(payable)}</b></div>
          <label className="checkout-v69-check checkout-v69-agree"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен(на) с условиями обработки персональных данных и правилами продажи</span></label>
          {submitAttempted&&!canSubmit&&<div className="checkout-v69-errors" role="alert">{!recipientName.trim()?"Укажите имя получателя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите номер телефона. ":""}{!emailOk?"Проверьте email. ":""}{!deliveryOk?"Заполните данные доставки. ":""}{!agreed?"Подтвердите согласие с условиями.":""}</div>}
          <button type="submit" className="primary checkout-v69-submit" disabled={submitAttempted&&!canSubmit}>ОФОРМИТЬ ЗАКАЗ — {fmt(payable)}</button>
          <small className="checkout-v69-security">♙ Безопасное оформление и защита данных</small>
        </section>
      </main>

      <aside className="checkout-v69-summary"><div><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header>{cart.slice(0,3).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><span><b>{item.name}</b><small>{item.selectedColor} · {item.selectedSize}</small><em>{item.quantity} × {fmt(item.price)}</em></span></article>)}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div><dt>Скидка −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl><div className="checkout-v69-summary-total"><span>Итого</span><b>{fmt(payable)}</b></div></div></aside>
    </form>
  </div>;
}
'''

text = text[:start] + new_checkout + text[end:]
path.write_text(text, encoding="utf-8")
print("Cart / checkout V69 applied")
