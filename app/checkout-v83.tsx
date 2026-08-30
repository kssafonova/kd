"use client";

import { useMemo, useState } from "react";
import { RemoteImage } from "./remote-image";

type CartLike = {
  id?: number | string;
  name?: string;
  note?: string;
  price?: number;
  image?: string;
  selectedColor?: string;
  selectedSize?: string;
  quantity?: number;
};
type ProfileLike = { name?: string; surname?: string; email?: string; phone?: string; city?: string; address?: string } | null;
type DeliveryMethod = "courier" | "store" | "pvz";
type PaymentMethod = "card" | "sbp" | "split" | "halva" | "upon";
type VerifyMethod = "phone" | "email";

const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(Math.max(0, value || 0))} ₽`;
const validPhone = (value: string) => value.replace(/\D/g, "").length >= 11;
const validEmail = (value: string) => /\S+@\S+\.\S+/.test(value);

const PICKUP_POINTS = [
  { id: "pvz-1", title: "ПВЗ · Большая Дмитровка", address: "Москва, ул. Большая Дмитровка, 22", meta: "Сегодня до 21:00", x: 34, y: 42 },
  { id: "pvz-2", title: "ПВЗ · Петровка", address: "Москва, ул. Петровка, 19", meta: "Завтра с 10:00", x: 58, y: 32 },
  { id: "pvz-3", title: "ПВЗ · Цветной бульвар", address: "Москва, Цветной бульвар, 15", meta: "Завтра с 11:00", x: 67, y: 58 },
];
const STORES = [
  { id: "store-1", title: "Бутик Культура Дома", address: "Москва, ул. Большая Дмитровка, 22", meta: "Ежедневно 10:00–22:00", x: 40, y: 45 },
  { id: "store-2", title: "Культура Дома · Петровка", address: "Москва, ул. Петровка, 19", meta: "Ежедневно 10:00–21:00", x: 62, y: 35 },
];

export function CheckoutV83({ cart, total, profile, close, editCart, submit }: { cart: CartLike[]; total: number; profile: ProfileLike; close: () => void; editCart: () => void; submit: () => void }) {
  const [delivery, setDelivery] = useState<DeliveryMethod>("courier");
  const [payment, setPayment] = useState<PaymentMethod>("card");
  const [verifyMethod, setVerifyMethod] = useState<VerifyMethod>(profile?.phone ? "phone" : "phone");
  const [recipientName, setRecipientName] = useState(profile?.name || "");
  const [surname, setSurname] = useState(profile?.surname || "");
  const [phone, setPhone] = useState(profile?.phone || "");
  const [email, setEmail] = useState(profile?.email || "");
  const [codeSent, setCodeSent] = useState(false);
  const [code, setCode] = useState("");
  const [verified, setVerified] = useState(Boolean(profile?.phone || profile?.email));
  const [city, setCity] = useState(profile?.city || "Москва");
  const [address, setAddress] = useState(profile?.address || "");
  const [apartment, setApartment] = useState("");
  const [comment, setComment] = useState("");
  const [pickupId, setPickupId] = useState("pvz-1");
  const [pickupQuery, setPickupQuery] = useState("");
  const [bonusExpanded, setBonusExpanded] = useState(true);
  const [bonusAmount, setBonusAmount] = useState("");
  const [consent, setConsent] = useState(true);
  const [errors, setErrors] = useState<string[]>([]);

  const itemCount = useMemo(() => cart.reduce((sum, item) => sum + Math.max(1, item.quantity || 1), 0), [cart]);
  const shipping = delivery === "courier" && total < 15000 ? 900 : 0;
  const onlineDiscount = payment === "card" || payment === "sbp" ? Math.round(total * 0.03) : 0;
  const bonusWriteoff = Math.min(Math.max(0, Number(bonusAmount.replace(/\D/g, "")) || 0), Math.max(0, total - onlineDiscount));
  const finalTotal = Math.max(0, total + shipping - onlineDiscount - bonusWriteoff);
  const pickupSource = delivery === "store" ? STORES : PICKUP_POINTS;
  const filteredPickup = pickupSource.filter((point) => `${point.title} ${point.address}`.toLowerCase().includes(pickupQuery.toLowerCase()));
  const selectedPickup = pickupSource.find((point) => point.id === pickupId) || pickupSource[0];

  const contactValue = verifyMethod === "phone" ? phone : email;
  const contactValid = verifyMethod === "phone" ? validPhone(phone) : validEmail(email);
  const sendCode = () => { if (!contactValid) return; setCodeSent(true); setCode(""); setVerified(false); };
  const confirmCode = () => { if (code.trim().length >= 4) setVerified(true); };
  const switchVerification = (method: VerifyMethod) => { setVerifyMethod(method); setCodeSent(false); setCode(""); setVerified(false); };

  const validate = () => {
    const next: string[] = [];
    if (!recipientName.trim()) next.push("Укажите имя получателя");
    if (!verified) next.push(`Подтвердите ${verifyMethod === "phone" ? "номер телефона" : "email"}`);
    if (delivery === "courier" && !address.trim()) next.push("Укажите адрес доставки");
    if ((delivery === "store" || delivery === "pvz") && !selectedPickup) next.push("Выберите пункт получения");
    if (payment === "upon" && delivery !== "store") next.push("Оплата при получении доступна для самовывоза");
    if (!consent) next.push("Подтвердите согласие с условиями заказа");
    setErrors(next);
    if (!next.length) submit();
  };

  const paymentItems: Array<{ id: PaymentMethod; title: string; note: string; tag?: string; disabled?: boolean }> = [
    { id: "card", title: "Банковская карта", note: "Visa, Mastercard, МИР", tag: "−3%" },
    { id: "sbp", title: "СБП", note: "Оплата через приложение банка", tag: "−3%" },
    { id: "split", title: "Яндекс Сплит", note: "Разделите платёж на части" },
    { id: "halva", title: "Халва", note: "Рассрочка картой Халва" },
    { id: "upon", title: "При получении", note: delivery === "store" ? "Картой или наличными в бутике" : "Доступно для самовывоза", disabled: delivery !== "store" },
  ];

  return <div className="checkout-v83" data-analytics-step="checkout_view_v83">
    <header className="checkout-v83-topbar">
      <button type="button" onClick={close} aria-label="Назад">←</button>
      <b>КУЛЬТУРА ДОМА</b>
      <button type="button" onClick={editCart}>Корзина · {itemCount}</button>
    </header>

    <form className="checkout-v83-layout" onSubmit={(event) => { event.preventDefault(); validate(); }}>
      <main className="checkout-v83-main">
        <header className="checkout-v83-heading"><small>ОФОРМЛЕНИЕ ЗАКАЗА</small><h1>Почти готово</h1><p>Контакты, доставка и оплата — на одном экране.</p></header>

        <section className="checkout-v83-section" aria-labelledby="v83-contacts">
          <div className="checkout-v83-section-head"><span>01</span><div><h2 id="v83-contacts">Получатель</h2><p>Укажите данные человека, который получит заказ.</p></div></div>
          <div className="checkout-v83-grid-2">
            <label className="checkout-v83-field"><span>Имя получателя *</span><input value={recipientName} onChange={(e) => setRecipientName(e.target.value)} placeholder="Имя" autoComplete="given-name" /></label>
            <label className="checkout-v83-field"><span>Фамилия</span><input value={surname} onChange={(e) => setSurname(e.target.value)} placeholder="Фамилия" autoComplete="family-name" /></label>
          </div>

          <div className="checkout-v83-verify">
            <div className="checkout-v83-verify-tabs"><button type="button" className={verifyMethod === "phone" ? "active" : ""} onClick={() => switchVerification("phone")}>По номеру телефона</button><button type="button" className={verifyMethod === "email" ? "active" : ""} onClick={() => switchVerification("email")}>По email</button></div>
            <div className={`checkout-v83-contact-line ${verified ? "verified" : ""}`}>
              <label className="checkout-v83-field"><span>{verifyMethod === "phone" ? "Телефон *" : "Email *"}</span><input value={contactValue} onChange={(e) => verifyMethod === "phone" ? setPhone(e.target.value) : setEmail(e.target.value)} placeholder={verifyMethod === "phone" ? "+7 999 000-00-00" : "name@example.com"} autoComplete={verifyMethod === "phone" ? "tel" : "email"}/></label>
              {verified ? <b className="checkout-v83-verified">✓ Подтверждено</b> : <button type="button" className="checkout-v83-text-action" disabled={!contactValid} onClick={sendCode}>{codeSent ? "Отправить повторно" : "Получить код"}</button>}
            </div>
            {codeSent && !verified && <div className="checkout-v83-code"><label className="checkout-v83-field"><span>Код подтверждения</span><input value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))} inputMode="numeric" placeholder="0000"/></label><button type="button" onClick={confirmCode} disabled={code.length < 4}>Подтвердить</button><small>В прототипе можно ввести любые 4 цифры. В production здесь подключается SMS/email-провайдер.</small></div>}
            <label className="checkout-v83-field checkout-v83-email-secondary"><span>Email для чека и состава заказа</span><input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="name@example.com" autoComplete="email" /></label>
          </div>
        </section>

        <section className="checkout-v83-section" aria-labelledby="v83-bonus">
          <div className="checkout-v83-section-head"><span>02</span><div><h2 id="v83-bonus">Бонусная программа</h2><p>Войдите по телефону или email, чтобы использовать бонусный счёт.</p></div></div>
          <div className="checkout-v83-bonus">
            <button type="button" className="checkout-v83-bonus-head" onClick={() => setBonusExpanded((v) => !v)}><span><b>{verified ? "Бонусный счёт подключён" : "Подтвердите контакт для бонусов"}</b><small>{verified ? "Можно списать бонусы на этот заказ" : "Баланс появится после подтверждения"}</small></span><em>{bonusExpanded ? "−" : "+"}</em></button>
            {bonusExpanded && <div className="checkout-v83-bonus-body"><label className="checkout-v83-field"><span>Списать бонусы</span><input disabled={!verified} value={bonusAmount} onChange={(e) => setBonusAmount(e.target.value.replace(/\D/g, ""))} placeholder={verified ? "0" : "Сначала подтвердите контакт"} inputMode="numeric" /></label><p>После покупки начисление отобразится в личном кабинете. Конкретные правила начисления задаются программой лояльности.</p></div>}
          </div>
        </section>

        <section className="checkout-v83-section" aria-labelledby="v83-delivery">
          <div className="checkout-v83-section-head"><span>03</span><div><h2 id="v83-delivery">Доставка</h2><p>Курьер, самовывоз из бутика или ПВЗ.</p></div></div>
          <div className="checkout-v83-delivery-tabs">
            <button type="button" className={delivery === "courier" ? "active" : ""} onClick={() => setDelivery("courier")}><b>Курьер</b><small>{total >= 15000 ? "Бесплатно" : money(900)}</small></button>
            <button type="button" className={delivery === "store" ? "active" : ""} onClick={() => { setDelivery("store"); setPickupId("store-1"); }}><b>Самовывоз</b><small>Из бутика</small></button>
            <button type="button" className={delivery === "pvz" ? "active" : ""} onClick={() => { setDelivery("pvz"); setPickupId("pvz-1"); }}><b>ПВЗ</b><small>Пункт выдачи</small></button>
          </div>

          {delivery === "courier" ? <div className="checkout-v83-address">
            <label className="checkout-v83-field"><span>Город</span><input value={city} onChange={(e) => setCity(e.target.value)} placeholder="Москва" /></label>
            <label className="checkout-v83-field"><span>Адрес *</span><input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="Начните вводить улицу и дом" /></label>
            <label className="checkout-v83-field"><span>Квартира / офис</span><input value={apartment} onChange={(e) => setApartment(e.target.value)} placeholder="Необязательно" /></label>
          </div> : <div className="checkout-v83-pickup">
            <label className="checkout-v83-search"><span>⌕</span><input value={pickupQuery} onChange={(e) => setPickupQuery(e.target.value)} placeholder="Адрес или название пункта" /></label>
            <div className="checkout-v83-map-layout">
              <div className="checkout-v83-map" aria-label="Карта пунктов получения">
                <div className="checkout-v83-map-road road-a"/><div className="checkout-v83-map-road road-b"/><div className="checkout-v83-map-road road-c"/>
                {pickupSource.map((point) => <button type="button" key={point.id} className={`checkout-v83-pin ${pickupId === point.id ? "active" : ""}`} style={{ left: `${point.x}%`, top: `${point.y}%` }} onClick={() => setPickupId(point.id)} aria-label={point.title}><span>●</span></button>)}
                <small className="checkout-v83-map-label label-1">Тверская</small><small className="checkout-v83-map-label label-2">Петровка</small><small className="checkout-v83-map-label label-3">Цветной бульвар</small>
              </div>
              <div className="checkout-v83-points">{filteredPickup.map((point) => <button type="button" key={point.id} className={pickupId === point.id ? "active" : ""} onClick={() => setPickupId(point.id)}><i/><span><b>{point.title}</b><small>{point.address}</small><em>{point.meta}</em></span></button>)}</div>
            </div>
            {selectedPickup && <div className="checkout-v83-selected-point"><span>Выбрано</span><b>{selectedPickup.title}</b><small>{selectedPickup.address}</small></div>}
          </div>}
          <label className="checkout-v83-field checkout-v83-comment"><span>Комментарий к заказу</span><textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Пожелания по доставке" rows={2}/></label>
        </section>

        <section className="checkout-v83-section" aria-labelledby="v83-payment">
          <div className="checkout-v83-section-head"><span>04</span><div><h2 id="v83-payment">Оплата</h2><p>Выберите удобный способ.</p></div></div>
          <div className="checkout-v83-payments">{paymentItems.map((item) => <button type="button" key={item.id} disabled={item.disabled} className={payment === item.id ? "active" : ""} onClick={() => !item.disabled && setPayment(item.id)}><i/><span><b>{item.title}{item.tag && <mark>{item.tag}</mark>}</b><small>{item.note}</small></span></button>)}</div>
        </section>

        <section className="checkout-v83-section checkout-v83-mobile-order">
          <div className="checkout-v83-section-head"><span>05</span><div><h2>Ваш заказ</h2><p>{itemCount} товаров</p></div></div>
          <OrderSummary cart={cart} total={total} shipping={shipping} onlineDiscount={onlineDiscount} bonusWriteoff={bonusWriteoff} finalTotal={finalTotal} editCart={editCart}/>
        </section>

        {errors.length > 0 && <div className="checkout-v83-errors">{errors.map((error) => <p key={error}>{error}</p>)}</div>}
        <label className="checkout-v83-consent"><input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)}/><i>✓</i><span>Я согласен с условиями оформления заказа и обработкой персональных данных.</span></label>
        <button className="checkout-v83-submit" type="submit">ОФОРМИТЬ ЗАКАЗ · {money(finalTotal)}</button>
        <p className="checkout-v83-security">Данные заказа передаются по защищённому соединению.</p>
      </main>

      <aside className="checkout-v83-summary"><OrderSummary cart={cart} total={total} shipping={shipping} onlineDiscount={onlineDiscount} bonusWriteoff={bonusWriteoff} finalTotal={finalTotal} editCart={editCart}/><button className="checkout-v83-submit" type="submit">ОФОРМИТЬ ЗАКАЗ · {money(finalTotal)}</button><small className="checkout-v83-aside-note">Нажимая кнопку, вы подтверждаете заказ.</small></aside>
    </form>
  </div>;
}

function OrderSummary({ cart, total, shipping, onlineDiscount, bonusWriteoff, finalTotal, editCart }: { cart: CartLike[]; total: number; shipping: number; onlineDiscount: number; bonusWriteoff: number; finalTotal: number; editCart: () => void }) {
  return <div className="checkout-v83-order-card">
    <header><h2>Ваш заказ</h2><button type="button" onClick={editCart}>Изменить</button></header>
    <div className="checkout-v83-order-items">{cart.slice(0, 4).map((item, index) => <article key={String(item.id ?? index)}><RemoteImage src={item.image || "/assets/images/image-placeholder.svg"} fallbackSrc="/assets/images/image-placeholder.svg" alt={item.name || "Товар"}/><div><b>{item.name}</b><small>{[item.selectedColor, item.selectedSize].filter(Boolean).join(" · ")}</small><em>{Math.max(1, item.quantity || 1)} × {money(item.price || 0)}</em></div></article>)}</div>
    <dl><div><dt>Товары</dt><dd>{money(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping ? money(shipping) : "Бесплатно"}</dd></div>{onlineDiscount > 0 && <div className="discount"><dt>Скидка за предоплату</dt><dd>−{money(onlineDiscount)}</dd></div>}{bonusWriteoff > 0 && <div className="discount"><dt>Бонусы</dt><dd>−{money(bonusWriteoff)}</dd></div>}</dl>
    <footer><span>Итого</span><strong>{money(finalTotal)}</strong></footer>
  </div>;
}
