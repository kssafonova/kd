from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / "app" / "page.tsx"
text = path.read_text(encoding="utf-8")

if "MOBILE_CART_CHECKOUT_V67" in text:
    print("Mobile cart/checkout V67 already applied")
    raise SystemExit(0)

checkout_anchor = text.index("function Checkout({cart,total,profile,close,editCart,submit}")
text = text[:checkout_anchor] + "// MOBILE_CART_CHECKOUT_V67\n" + text[checkout_anchor:]

state_anchor = '  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});\n'
if state_anchor not in text:
    raise RuntimeError("Checkout form state anchor not found")
text = text.replace(
    state_anchor,
    state_anchor + '  const [recipientName,setRecipientName]=useState(profile?[profile.name,profile.surname].filter(Boolean).join(" "):"");\n',
    1,
)

old_contact_ok = '  const contactOk=form.name.trim().length>0&&phoneOk&&emailOk;'
if old_contact_ok not in text:
    raise RuntimeError("contactOk anchor not found")
text = text.replace(old_contact_ok, '  const contactOk=recipientName.trim().length>1&&phoneOk&&emailOk;', 1)

old_contact_section = re.compile(
    r'\{step===1&&<section className="checkout-v43-step" data-analytics-step="checkout_contacts">.*?</section>\}\n\n        \{step===2&&',
    re.S,
)
match = old_contact_section.search(text)
if not match:
    raise RuntimeError("Checkout contact section not found")

new_contact = r'''{step===1&&<section className="checkout-v43-step checkout-v67-contacts" data-analytics-step="checkout_contacts"><header><small>ШАГ 1 ИЗ 3</small><h1>Контактные данные</h1><p>Укажите получателя и подтвердите номер телефона. Регистрация для оформления не нужна.</p></header><div className="checkout-v43-fields checkout-v67-fields"><label className="v43-field checkout-v67-recipient"><span>Имя получателя *</span><input value={recipientName} onChange={event=>setRecipientName(event.target.value)} autoComplete="name" name="recipientName" placeholder="Имя и фамилия"/></label><label className={`v43-field checkout-v43-phone checkout-v67-phone ${phoneVerified?"is-verified":""}`}><span>Телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} autoComplete="tel" inputMode="tel" name="phone" placeholder="+7 999 000-00-00"/>{phoneDigits.length>=10&&!phoneVerified&&<button type="button" onClick={requestPhoneCode}>{codeSent?"Отправить ещё":"Получить код"}</button>}{phoneVerified&&<b>✓ Подтверждён</b>}</div></label>{codeSent&&!phoneVerified&&<div className="checkout-v43-otp checkout-v67-otp"><div><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></div><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>В прототипе используйте код 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}<label className="v43-field checkout-v67-email"><span>Email</span><input type="email" value={form.email} onChange={field("email")} autoComplete="email" name="email" placeholder="Для чека и статуса заказа"/></label></div>{contactAttempted&&!contactOk&&<div className="checkout-v43-inline-error" role="alert">{!recipientName.trim()?"Укажите имя получателя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите номер телефона. ":""}{!emailOk?"Проверьте email.":""}</div>}<div className="checkout-v67-security">⌑ Безопасное оформление и защита данных</div><button type="button" className="primary checkout-v43-next" onClick={nextFromContacts}>ПРОДОЛЖИТЬ К ДОСТАВКЕ</button></section>}

        {step===2&&'''
text = text[:match.start()] + new_contact + text[match.end():]

old_review = '<p>{form.name} · {form.phone}{form.email?` · ${form.email}`:""}</p>'
if old_review not in text:
    raise RuntimeError("Checkout review contact line not found")
text = text.replace(old_review, '<p>{recipientName} · {form.phone}{form.email?` · ${form.email}`:""}</p>', 1)

path.write_text(text, encoding="utf-8")
print("Mobile cart/checkout V67 applied")
