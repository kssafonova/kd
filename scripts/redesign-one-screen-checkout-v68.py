from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "page.tsx"
text = path.read_text(encoding="utf-8")

if "ONE_SCREEN_CHECKOUT_V68" in text:
    print("One-screen checkout V68 already applied")
    raise SystemExit(0)

start = text.index("function Checkout({cart,total,profile,close,editCart,submit}")
end = text.index("\nfunction CheckoutMap(", start)

new_checkout = r'''// ONE_SCREEN_CHECKOUT_V68
function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type DeliveryMethod="courier"|"store"|"pvz";
  type PaymentMethod="online"|"upon";
  const shellRef=useRef<HTMLDivElement>(null);
  const [delivery,setDelivery]=useState<DeliveryMethod>("courier");
  const [payment,setPayment]=useState<PaymentMethod>("online");
  const [slot,setSlot]=useState("18:00–22:00");
  const [pickupPoint,setPickupPoint]=useState("");
  const [storePoint,setStorePoint]=useState("");
  const [pvzQuery,setPvzQuery]=useState("");
  const [access,setAccess]=useState("");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [recipientName,setRecipientName]=useState(profile?[profile.name,profile.surname].filter(Boolean).join(" "):"");
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [submitAttempted,setSubmitAttempted]=useState(false);
  const [notifications,setNotifications]=useState(true);
  const [agreed,setAgreed]=useState(false);
  const [accountNoticeOpen,setAccountNoticeOpen]=useState(Boolean(profile?.phone));
  const [checkoutAsGuest,setCheckoutAsGuest]=useState(false);

  const storePoints:Record<string,string[]>={
    "Москва":["Культура Дома · Петровка"],
    "Санкт-Петербург":["Культура Дома · Невский проспект"],
    "Казань":["Культура Дома · улица Баумана"],
  };
  const availableStores=storePoints[form.city]??[];
  const pvz=KD_PVZ_POINTS[form.city]??[];
  const filteredPvz=pvz.filter(point=>!pvzQuery.trim()||point.toLocaleLowerCase("ru-RU").includes(pvzQuery.trim().toLocaleLowerCase("ru-RU")));
  const phoneDigits=form.phone.replace(/\D/g,"");
  const profileDigits=(profile?.phone||"").replace(/\D/g,"");
  const registeredNumber=Boolean(profileDigits&&phoneDigits===profileDigits);
  const phoneOk=phoneDigits.length>=10&&phoneVerified;
  const emailOk=form.email.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const contactOk=recipientName.trim().length>1&&phoneOk&&emailOk;
  const deliveryOk=delivery==="courier"
    ? form.city.trim().length>0&&form.address.trim().length>3
    : delivery==="store"
      ? form.city.trim().length>0&&storePoint.length>0
      : form.city.trim().length>0&&pickupPoint.length>0;
  const paymentOk=Boolean(payment);
  const onlineDiscount=payment==="online"?Math.round(total*.03):0;
  const shipping=delivery==="courier"?(total>=15000?0:300):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const canSubmit=contactOk&&deliveryOk&&paymentOk&&agreed;
  const expensive=payable>=30000;
  const courierMapPoint=form.address.trim()?`${form.city}, ${form.address}`:form.city||"Москва";

  const setPhone=(value:string)=>{
    setForm({...form,phone:value});
    const digits=value.replace(/\D/g,"");
    setPhoneVerified(Boolean(profileDigits&&digits===profileDigits));
    setCodeSent(false);
    setPhoneCode("");
    setOtpError("");
    setAccountNoticeOpen(Boolean(profileDigits&&digits===profileDigits));
    setCheckoutAsGuest(false);
  };
  const requestPhoneCode=()=>{
    if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}
    setCodeSent(true);setPhoneCode("");setOtpError("");
  };
  const verifyPhone=()=>{
    if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}
    else setOtpError("Неверный код. В прототипе используйте 1234");
  };
  const submitOrder=()=>{
    setSubmitAttempted(true);
    if(!canSubmit)return;
    submit();
  };
  const chooseCity=(city:string)=>{
    setForm({...form,city,address:city===form.city?form.address:""});
    setPickupPoint("");setStorePoint("");setPvzQuery("");
  };
  const deliveryLabel=delivery==="courier"
    ? `${form.city}${form.address?`, ${form.address}`:""} · ${slot}`
    : delivery==="store"?storePoint:`ПВЗ · ${pickupPoint}`;

  return <div className="checkout checkout-v43 checkout-v68" ref={shellRef} data-analytics-step="checkout_view">
    <header className="checkout-v43-head checkout-v68-head"><button type="button" onClick={close}>← <span>Корзина</span></button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>

    <form className="checkout-v68-layout" onSubmit={event=>{event.preventDefault();submitOrder()}}>
      <main className="checkout-v68-main">
        <header className="checkout-v68-title"><small>ОФОРМЛЕНИЕ ЗАКАЗА</small><h1>Оформление</h1><p>Все данные на одной странице. До подтверждения можно изменить способ получения и оплаты.</p></header>

        <section className="checkout-v68-section" aria-labelledby="checkout-contact-title">
          <header><span>01</span><div><h2 id="checkout-contact-title">Контактные данные</h2><p>Получатель и номер для связи по заказу.</p></div></header>
          <div className="checkout-v68-fields">
            <label className="v43-field"><span>Имя получателя *</span><input value={recipientName} onChange={event=>setRecipientName(event.target.value)} autoComplete="name" name="recipientName" placeholder="Имя и фамилия"/></label>
            <label className={`v43-field checkout-v43-phone checkout-v68-phone ${phoneVerified?"is-verified":""}`}><span>Контактный телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} autoComplete="tel" inputMode="tel" name="phone" placeholder="+7 999 000-00-00"/>{phoneDigits.length>=10&&!phoneVerified&&<button type="button" onClick={requestPhoneCode}>{codeSent?"Отправить ещё":"Получить код"}</button>}{phoneVerified&&<b>✓ Подтверждён</b>}</div></label>
            {registeredNumber&&accountNoticeOpen&&<aside className="checkout-v68-account-note"><div><b>ⓘ</b><p>Этот номер привязан к вашему аккаунту. С аккаунтом заказ будет доступен в личном кабинете и сможет участвовать в бонусной программе.</p></div><button type="button" className="checkout-v68-account-primary" onClick={()=>{setCheckoutAsGuest(false);setAccountNoticeOpen(false)}}>ПРОДОЛЖИТЬ С АККАУНТОМ</button><button type="button" onClick={()=>{setCheckoutAsGuest(true);setAccountNoticeOpen(false)}}>ВСЁ РАВНО ПРОДОЛЖИТЬ КАК ГОСТЬ</button></aside>}
            {checkoutAsGuest&&registeredNumber&&<button type="button" className="checkout-v68-account-restore" onClick={()=>setAccountNoticeOpen(true)}>Номер связан с аккаунтом · изменить выбор</button>}
            {codeSent&&!phoneVerified&&<div className="checkout-v43-otp checkout-v68-otp"><div><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></div><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Для статического прототипа: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}
            <label className="v43-field"><span>Email для чека и статуса</span><input type="email" value={form.email} onChange={event=>setForm({...form,email:event.target.value})} autoComplete="email" name="email" placeholder="example@mail.ru"/></label>
            <label className="checkout-v68-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Получать уведомления об изменении статуса заказа</span></label>
          </div>
        </section>

        <section className="checkout-v68-section" aria-labelledby="checkout-delivery-title">
          <header><span>02</span><div><h2 id="checkout-delivery-title">Способ получения</h2><p>Выберите удобный вариант — стоимость сразу попадёт в итог.</p></div></header>
          <div className="checkout-v68-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>setDelivery("courier")}><Icon name="bag"/><b>Курьером</b><small>{shipping===0?"Бесплатно":"300 ₽"}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>setDelivery("store")}><span>⌂</span><b>Самовывоз</b><small>Бесплатно</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>setDelivery("pvz")}><Icon name="pin"/><b>ПВЗ</b><small>Бесплатно</small></button>
          </div>

          <div className="checkout-v68-address">
            <CitySuggestField value={form.city} required onChange={chooseCity}/>
            {delivery==="courier"&&<>
              <AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm({...form,address})}/>
              <div className="checkout-v68-address-parts"><label className="v43-field"><span>Подъезд</span><input value={access.split(" · ")[0]||""} onChange={event=>setAccess(`${event.target.value} · ${access.split(" · ")[1]||""} · ${access.split(" · ")[2]||""}`)} placeholder="2"/></label><label className="v43-field"><span>Этаж</span><input value={access.split(" · ")[1]||""} onChange={event=>setAccess(`${access.split(" · ")[0]||""} · ${event.target.value} · ${access.split(" · ")[2]||""}`)} placeholder="3"/></label><label className="v43-field"><span>Квартира</span><input value={access.split(" · ")[2]||""} onChange={event=>setAccess(`${access.split(" · ")[0]||""} · ${access.split(" · ")[1]||""} · ${event.target.value}`)} placeholder="8"/></label></div>
              <div className="checkout-v68-map-wrap checkout-v68-courier-map"><div className="checkout-v68-map-head"><b>Проверьте точку на карте</b><span>{courierMapPoint}</span></div><CheckoutMap points={[courierMapPoint]} selected={courierMapPoint} choose={()=>{}} mode="courier"/></div>
              <div className="checkout-v68-slots"><span>Время доставки</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div>
            </>}

            {delivery==="store"&&<div className="checkout-v68-pickup"><header><b>Выберите бутик</b><span>{form.city}</span></header>{availableStores.length?availableStores.map(point=><button type="button" key={point} className={storePoint===point?"active":""} onClick={()=>setStorePoint(point)}><i/><div><b>{point}</b><small>Ежедневно · уточним готовность после заказа</small></div></button>):<p>В этом городе пока нет бутика для самовывоза.</p>}{availableStores.length>0&&<div className="checkout-v68-map-wrap"><CheckoutMap points={availableStores} selected={storePoint} choose={setStorePoint} mode="pickup"/></div>}</div>}

            {delivery==="pvz"&&<div className="checkout-v68-pvz"><label className="checkout-v68-pvz-search"><Icon name="search"/><input value={pvzQuery} onChange={event=>setPvzQuery(event.target.value)} placeholder="Адрес или станция метро"/><Icon name="pin"/></label><div className="checkout-v68-map-wrap"><CheckoutMap points={filteredPvz} selected={pickupPoint} choose={setPickupPoint} mode="pickup"/></div></div>}
          </div>
        </section>

        <section className="checkout-v68-section" aria-labelledby="checkout-payment-title">
          <header><span>03</span><div><h2 id="checkout-payment-title">Способ оплаты</h2><p>Онлайн-оплата выгоднее — скидка применяется сразу.</p></div></header>
          <div className="checkout-v68-payment-options">
            <button type="button" className={payment==="online"?"active":""} onClick={()=>setPayment("online")}><i/><div><b>Онлайн — картой / СБП <mark>−3%</mark></b><span>Оплата после подтверждения заказа</span></div></button>
            <button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><div><b>При получении</b><span>Картой или наличными</span></div></button>
          </div>
          {expensive&&<aside className="checkout-v68-concierge"><small>ЗАКАЗ ОТ 30 000 ₽</small><b>Персональное сопровождение</b><p>Менеджер свяжется, чтобы подтвердить наличие, доставку и детали заказа.</p></aside>}
        </section>

        <section className="checkout-v68-section checkout-v68-final" aria-labelledby="checkout-final-title">
          <header><span>04</span><div><h2 id="checkout-final-title">Проверьте заказ</h2><p>{recipientName||"Получатель"} · {form.phone||"телефон"}</p></div></header>
          <div className="checkout-v68-review-line"><span>Получение</span><b>{deliveryLabel}</b></div>
          <div className="checkout-v68-review-line"><span>Оплата</span><b>{payment==="online"?"Онлайн — карта / СБП · скидка 3%":"При получении"}</b></div>
          <button type="button" className="checkout-v68-edit-cart" onClick={editCart}>Состав заказа · {productCountLabel(cart.reduce((sum,item)=>sum+item.quantity,0))} · Изменить</button>
          <label className="checkout-v68-check checkout-v68-agree"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Согласен(на) с условиями продажи и обработкой персональных данных.</span></label>
          {submitAttempted&&!canSubmit&&<div className="checkout-v43-inline-error" role="alert">{!recipientName.trim()?"Укажите имя получателя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите телефон. ":""}{!emailOk?"Проверьте email. ":""}{!deliveryOk?"Заполните данные получения. ":""}{!agreed?"Подтвердите согласие с условиями.":""}</div>}
          <div className="checkout-v68-desktop-submit"><div><span>Итого</span><b>{fmt(payable)}</b>{onlineDiscount>0&&<small>Скидка за онлайн-оплату −{fmt(onlineDiscount)}</small>}</div><button type="submit" className="primary" disabled={!canSubmit}>ОФОРМИТЬ ЗАКАЗ · {fmt(payable)}</button></div>
          <small className="checkout-v68-security">⌑ Безопасное оформление и защита данных</small>
        </section>
      </main>

      <aside className="checkout-v68-summary"><div className="checkout-v68-summary-inner"><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header><div className="checkout-v68-summary-items">{cart.slice(0,4).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><div><b>{item.name}</b><span>{item.selectedColor} · {item.selectedSize}</span><small>{item.quantity} × {fmt(item.price)}</small></div></article>)}</div>{cart.length>4&&<small>Ещё {cart.length-4} поз.</small>}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div>{onlineDiscount>0&&<div><dt>Онлайн-оплата −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}<div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div></dl><div className="checkout-v68-summary-total"><span>Итого</span><b>{fmt(payable)}</b></div></div></aside>
    </form>

    <div className="checkout-v68-mobile-submit"><div><small>ИТОГО</small><b>{fmt(payable)}</b></div><button type="button" className="primary" disabled={!canSubmit} onClick={submitOrder}>ОФОРМИТЬ ЗАКАЗ</button></div>
  </div>;
}
'''

text = text[:start] + new_checkout + text[end:]
path.write_text(text, encoding="utf-8")
print("One-screen checkout V68 applied")
