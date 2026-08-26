from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = "// CHECKOUT_REDESIGN_V83"
if marker not in text:
    start = text.index("// MOBILE_CART_CHECKOUT_V67")
    end = text.index("\nfunction CheckoutMap(", start)
    new_checkout = r'''// CHECKOUT_REDESIGN_V83
function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type DeliveryMethod="courier"|"store"|"pvz";
  type PaymentMethod="card"|"sbp"|"split"|"halva"|"upon";
  type VerificationMethod="phone"|"email";
  const [delivery,setDelivery]=useState<DeliveryMethod>("courier");
  const [payment,setPayment]=useState<PaymentMethod>("card");
  const [verificationMethod,setVerificationMethod]=useState<VerificationMethod>(profile?.phone?"phone":profile?.email?"email":"phone");
  const [recipientName,setRecipientName]=useState(profile?.name??"");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [emailVerified,setEmailVerified]=useState(Boolean(profile?.email));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [emailCodeSent,setEmailCodeSent]=useState(false);
  const [emailCode,setEmailCode]=useState("");
  const [emailOtpError,setEmailOtpError]=useState("");
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
  const [comment,setComment]=useState("");

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
  const profileEmail=(profile?.email||"").trim().toLocaleLowerCase("ru-RU");
  const demoRegisteredDigits="79261234567";
  const registeredNumber=phoneDigits.length>=10&&(phoneDigits===profileDigits||phoneDigits===demoRegisteredDigits);
  const registeredName=profile?.name?`${profile.name}${profile.surname?` ${profile.surname.slice(0,1)}.`:""}`:"Анна И.";
  const emailValid=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const emailFormatOk=!form.email.trim()||emailValid;
  const phoneOk=phoneDigits.length>=10&&phoneVerified;
  const emailOk=emailValid&&emailVerified;
  const verificationOk=verificationMethod==="phone"?phoneOk:emailOk;
  const contactOk=recipientName.trim().length>1&&verificationOk&&emailFormatOk;
  const deliveryOk=delivery==="courier"
    ? Boolean(form.city.trim()&&form.address.trim().length>3)
    : delivery==="store"?Boolean(form.city.trim()&&storePoint):Boolean(form.city.trim()&&pickupPoint);
  const prepayDiscount=payment==="card"||payment==="sbp";
  const onlineDiscount=prepayDiscount?Math.round(total*.03):0;
  const shipping=delivery==="courier"?(total>=15000?0:300):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const canSubmit=contactOk&&deliveryOk&&agreed;
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);

  const setPhone=(value:string)=>{
    const digits=value.replace(/\D/g,"");
    setForm(current=>({...current,phone:value}));
    setPhoneVerified(Boolean(profileDigits&&digits===profileDigits));
    setCodeSent(false);setPhoneCode("");setOtpError("");setRegisteredChoice("");
  };
  const setEmail=(value:string)=>{
    setForm(current=>({...current,email:value}));
    setEmailVerified(Boolean(profileEmail&&value.trim().toLocaleLowerCase("ru-RU")===profileEmail));
    setEmailCodeSent(false);setEmailCode("");setEmailOtpError("");
  };
  const requestPhoneCode=()=>{
    if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}
    setCodeSent(true);setPhoneCode("");setOtpError("");
  };
  const verifyPhone=()=>{
    if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}
    else setOtpError("Неверный код. В прототипе используйте 1234");
  };
  const requestEmailCode=()=>{
    if(!emailValid){setEmailOtpError("Введите корректный email");return}
    setEmailCodeSent(true);setEmailCode("");setEmailOtpError("");
  };
  const verifyEmail=()=>{
    if(emailCode==="1234"){setEmailVerified(true);setEmailCodeSent(false);setEmailOtpError("")}
    else setEmailOtpError("Неверный код. В прототипе используйте 1234");
  };
  const continueWithAccount=()=>{setRegisteredChoice("account");setPhoneVerified(true);setCodeSent(false);setOtpError("")};
  const continueAsGuest=()=>{setRegisteredChoice("guest");if(!phoneVerified){setCodeSent(true);setPhoneCode("");setOtpError("")}};
  const chooseCity=(city:string)=>{setForm(current=>({...current,city,address:city===current.city?current.address:""}));setPickupPoint("");setStorePoint("");setPvzQuery("")};
  const chooseDelivery=(method:DeliveryMethod)=>{
    setDelivery(method);
    if(method!=="store"&&payment==="upon")setPayment("card");
    if(method==="pvz"&&!pickupPoint&&pvz[0])setPickupPoint(pvz[0]);
    if(method==="store"&&!storePoint&&stores[0])setStorePoint(stores[0]);
  };
  const submitOrder=()=>{setSubmitAttempted(true);if(canSubmit)submit()};

  return <div className="checkout checkout-v69 checkout-v83" data-analytics-step="checkout_view">
    <header className="checkout-v69-head"><button type="button" onClick={close} aria-label="Вернуться в корзину">←</button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={editCart} aria-label="Открыть корзину"><Icon name="bag"/></button></header>
    <form className="checkout-v69-layout" onSubmit={event=>{event.preventDefault();submitOrder()}}>
      <main className="checkout-v69-main">
        <header className="checkout-v69-title"><h1>Оформление заказа</h1></header>

        <section className="checkout-v69-section checkout-v69-contacts" aria-labelledby="v83-contact-title">
          <h2 id="v83-contact-title">Контактные данные</h2>
          <div className="checkout-v69-fields checkout-v69-name-row">
            <label><span>Имя получателя *</span><input value={recipientName} onChange={event=>setRecipientName(event.target.value)} autoComplete="given-name" placeholder="Имя"/></label>
            <label><span>Фамилия</span><input value={form.surname} onChange={event=>setForm(current=>({...current,surname:event.target.value}))} autoComplete="family-name" placeholder="Необязательно"/></label>
          </div>

          <div className="checkout-v83-verify">
            <header><div><h3>Подтверждение контакта</h3><p>Подтвердите телефон или email — достаточно одного способа.</p></div></header>
            <nav className="checkout-v83-verify-tabs" aria-label="Способ подтверждения"><button type="button" className={verificationMethod==="phone"?"active":""} onClick={()=>setVerificationMethod("phone")}>По телефону</button><button type="button" className={verificationMethod==="email"?"active":""} onClick={()=>setVerificationMethod("email")}>По email</button></nav>
          </div>

          <label className={`checkout-v69-field checkout-v69-phone ${phoneVerified?"is-verified":""}`}><span>Контактный телефон {verificationMethod==="phone"?"*":""}</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} inputMode="tel" autoComplete="tel" placeholder="+7 999 000-00-00"/>{phoneVerified?<b>✓</b>:verificationMethod==="phone"&&phoneDigits.length>=10?<button type="button" onClick={requestPhoneCode}>Получить код</button>:null}</div></label>
          {verificationMethod==="phone"&&registeredNumber&&!registeredChoice&&<aside className="checkout-v69-account-note"><div><span>ⓘ</span><p>Этот номер привязан к аккаунту <b>{registeredName}</b>. Можно войти и получить заказ в истории покупок или продолжить как гость.</p></div><button type="button" className="primary" onClick={continueWithAccount}>ВОЙТИ В АККАУНТ</button><button type="button" onClick={continueAsGuest}>ПРОДОЛЖИТЬ КАК ГОСТЬ</button></aside>}
          {verificationMethod==="phone"&&registeredNumber&&registeredChoice&&<button type="button" className="checkout-v69-account-change" onClick={()=>setRegisteredChoice("")}>{registeredChoice==="account"?"Оформление с аккаунтом":"Продолжаем как гость"} · изменить</button>}
          {verificationMethod==="phone"&&codeSent&&!phoneVerified&&<div className="checkout-v83-code"><label><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></label><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}
          {phoneVerified&&<div className="checkout-v83-verified-note">✓ Телефон подтверждён</div>}

          <label className={`checkout-v69-field checkout-v83-email-field ${emailVerified?"is-verified":""}`}><span>Email {verificationMethod==="email"?"*":"для уведомлений"}</span><div><input type="email" value={form.email} onChange={event=>setEmail(event.target.value)} autoComplete="email" placeholder="example@mail.ru"/>{emailVerified?<b>✓</b>:verificationMethod==="email"&&emailValid?<button type="button" onClick={requestEmailCode}>Получить код</button>:null}</div></label>
          {verificationMethod==="email"&&emailCodeSent&&!emailVerified&&<div className="checkout-v83-code"><label><span>Код из письма</span><input inputMode="numeric" maxLength={4} value={emailCode} onChange={event=>{setEmailCode(event.target.value.replace(/\D/g,"").slice(0,4));setEmailOtpError("")}} placeholder="0000"/></label><button type="button" onClick={verifyEmail}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{emailOtpError&&<em role="alert">{emailOtpError}</em>}</div>}
          {emailVerified&&<div className="checkout-v83-verified-note">✓ Email подтверждён</div>}
          <label className="checkout-v69-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Получать статус заказа и уведомления</span></label>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v83-delivery-title">
          <h2 id="v83-delivery-title">Способ получения</h2>
          <div className="checkout-v69-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>chooseDelivery("courier")}><span>▱</span><b>Курьером</b><small>2–3 дня · {shipping===0?"0 ₽":"300 ₽"}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>chooseDelivery("store")}><span>⌂</span><b>Самовывоз</b><small>Из бутика · 0 ₽</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>chooseDelivery("pvz")}><span>▦</span><b>ПВЗ</b><small>Пункт выдачи · 0 ₽</small></button>
          </div>
          <div className="checkout-v69-delivery-body">
            <CitySuggestField value={form.city} required onChange={chooseCity}/>
            {delivery==="courier"&&<>
              <AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm(current=>({...current,address}))}/>
              <div className="checkout-v69-address-parts"><label><span>Подъезд</span><input value={entrance} onChange={event=>setEntrance(event.target.value)} placeholder="2"/></label><label><span>Этаж</span><input value={floor} onChange={event=>setFloor(event.target.value)} placeholder="3"/></label><label><span>Квартира</span><input value={flat} onChange={event=>setFlat(event.target.value)} placeholder="8"/></label></div>
              <div className="checkout-v69-map-block"><div className="checkout-v69-map-caption"><b>Адрес на карте</b><span>{form.address?`${form.city}, ${form.address}`:form.city}</span></div><CheckoutMap points={[form.address?`${form.city}, ${form.address}`:form.city]} selected={form.address?`${form.city}, ${form.address}`:form.city} choose={()=>{}} mode="courier"/></div>
              <div className="checkout-v69-slots"><span>Время доставки</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div>
            </>}
            {delivery==="store"&&<div className="checkout-v69-pickup"><h3>Выберите бутик</h3>{stores.length?stores.map(point=><button type="button" key={point} className={storePoint===point?"active":""} onClick={()=>setStorePoint(point)}><i/><span><b>{point}</b><small>{form.city} · ежедневно</small></span></button>):<p>В этом городе пока нет доступного самовывоза.</p>}{stores.length>0&&<div className="checkout-v69-map-block"><CheckoutMap points={stores} selected={storePoint} choose={setStorePoint} mode="store"/></div>}</div>}
            {delivery==="pvz"&&<div className="checkout-v69-pvz"><label className="checkout-v69-pvz-search"><Icon name="search"/><input value={pvzQuery} onChange={event=>setPvzQuery(event.target.value)} placeholder="Адрес, улица или метро"/><Icon name="pin"/></label><div className="checkout-v69-map-block"><div className="checkout-v69-map-caption"><b>Пункты выдачи на карте</b><span>Выберите удобный ПВЗ</span></div><CheckoutMap points={filteredPvz.slice(0,6)} selected={pickupPoint} choose={setPickupPoint} mode="pvz"/></div>{pickupPoint&&<div className="checkout-v69-selected-point"><i/><span><b>{pickupPoint}</b><small>Готовность к выдаче: завтра · 09:00–20:00</small></span></div>}</div>}
          </div>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v83-payment-title">
          <h2 id="v83-payment-title">Способ оплаты</h2>
          <div className="checkout-v83-payments">
            <button type="button" className={`checkout-v83-payment ${payment==="card"?"active":""}`} onClick={()=>setPayment("card")}><i/><span><b>Банковская карта <mark>−3%</mark></b><small>Visa, Mastercard, Мир · скидка при предоплате</small></span></button>
            <button type="button" className={`checkout-v83-payment ${payment==="sbp"?"active":""}`} onClick={()=>setPayment("sbp")}><i/><span><b>СБП <mark>−3%</mark></b><small>Оплата через приложение банка</small></span></button>
            <button type="button" className={`checkout-v83-payment ${payment==="split"?"active":""}`} onClick={()=>setPayment("split")}><i/><span><b>Яндекс Сплит</b><small>Разделите сумму на несколько платежей</small></span></button>
            <button type="button" className={`checkout-v83-payment ${payment==="halva"?"active":""}`} onClick={()=>setPayment("halva")}><i/><span><b>Халва</b><small>Рассрочка по карте Халва</small></span></button>
            <button type="button" disabled={delivery!=="store"} className={`checkout-v83-payment checkout-v83-payment-wide ${payment==="upon"?"active":""}`} onClick={()=>setPayment("upon")}><i/><span><b>Оплата при получении</b><small>{delivery==="store"?"Картой или наличными в бутике":"Доступно при выборе самовывоза"}</small></span></button>
          </div>
          <label className="checkout-v83-comment"><span>Комментарий к заказу</span><textarea value={comment} onChange={event=>setComment(event.target.value)} placeholder="Например, удобное время для звонка"/></label>
        </section>

        <section className="checkout-v69-section checkout-v69-order" aria-labelledby="v83-order-title">
          <div className="checkout-v69-order-head"><h2 id="v83-order-title">Состав заказа</h2><button type="button" onClick={editCart}>Изменить</button></div>
          <dl><div><dt>{itemCount} товаров</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div className="discount"><dt>Скидка за предоплату</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl>
          <div className="checkout-v69-total"><span>Итого</span><b>{fmt(payable)}</b></div>
          <label className="checkout-v69-check checkout-v69-agree"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен(на) с условиями обработки персональных данных и правилами продажи</span></label>
          {submitAttempted&&!canSubmit&&<div className="checkout-v69-errors" role="alert">{!recipientName.trim()?"Укажите имя получателя. ":""}{verificationMethod==="phone"&&!phoneOk?"Подтвердите номер телефона. ":""}{verificationMethod==="email"&&!emailOk?"Подтвердите email. ":""}{!emailFormatOk?"Проверьте email. ":""}{!deliveryOk?"Заполните данные доставки. ":""}{!agreed?"Подтвердите согласие с условиями.":""}</div>}
          <button type="submit" className="primary checkout-v69-submit" disabled={submitAttempted&&!canSubmit}>ОФОРМИТЬ ЗАКАЗ — {fmt(payable)}</button>
          <small className="checkout-v69-security">Безопасное оформление и защита данных</small>
        </section>
      </main>

      <aside className="checkout-v69-summary"><div><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header>{cart.slice(0,4).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><span><b>{item.name}</b><small>{item.selectedColor} · {item.selectedSize}</small><em>{item.quantity} × {fmt(item.price)}</em></span></article>)}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div><dt>Скидка −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl><div className="checkout-v69-summary-total"><span>Итого</span><b>{fmt(payable)}</b></div></div></aside>
    </form>
  </div>;
}'''
    text = text[:start] + new_checkout + text[end:]

map_marker = "// CHECKOUT_MAP_V83"
if map_marker not in text:
    map_start = text.index("function CheckoutMap(")
    map_end = text.index("\nfunction Footer(", map_start)
    new_map = r'''// CHECKOUT_MAP_V83
function CheckoutMap({points,selected,choose,mode}:{points:string[];selected:string;choose:(point:string)=>void;mode:"courier"|"store"|"pvz"}){
  const title=mode==="pvz"?"ВЫБЕРИТЕ ПВЗ":mode==="store"?"ВЫБЕРИТЕ БУТИК":"УТОЧНИТЕ ТОЧКУ";
  const subtitle=mode==="pvz"?"Пункт выдачи":mode==="store"?"Самовывоз":"Курьерская доставка";
  return <div className="checkout-map"><div className="map-canvas" aria-label="Карта выбора точки">{points.map((point,index)=><button type="button" key={point} className={`map-pin pin-${index} ${selected===point?"active":""}`} onClick={()=>choose(point)} aria-label={`Выбрать ${point}`}><Icon name="pin"/><span>{index+1}</span></button>)}<i className="river"/><span className="map-label moscow">МОСКВА</span><span className="map-label center">САДОВОЕ КОЛЬЦО</span></div><div className="map-points"><p>{title}</p>{points.map((point,index)=><button type="button" key={point} className={selected===point?"active":""} onClick={()=>choose(point)}><b>{index+1}</b><span>{point}<small>{subtitle}</small></span></button>)}</div></div>;
}'''
    text = text[:map_start] + new_map + text[map_end:]

page_path.write_text(text, encoding="utf-8")
print("Checkout V83 applied")
