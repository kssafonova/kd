from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = "// CHECKOUT_BONUS_V84"
if marker in text:
    print("Checkout bonus V84 already applied")
    raise SystemExit(0)
if "// CHECKOUT_REDESIGN_V83" not in text:
    raise SystemExit("checkout-bonus-v84: V83 checkout must be applied first")

state_anchor = '  const [comment,setComment]=useState("");\n'
state_patch = state_anchor + '''  // CHECKOUT_BONUS_V84\n  const [loyaltyJoined,setLoyaltyJoined]=useState(Boolean(profile));\n  const [bonusAmount,setBonusAmount]=useState("");\n'''
if state_anchor not in text:
    raise SystemExit("checkout-bonus-v84: state anchor not found")
text = text.replace(state_anchor, state_patch, 1)

discount_anchor = '  const onlineDiscount=prepayDiscount?Math.round(total*.03):0;\n  const shipping=delivery==="courier"?(total>=15000?0:300):0;\n  const payable=Math.max(0,total-onlineDiscount+shipping);'
discount_patch = '''  const onlineDiscount=prepayDiscount?Math.round(total*.03):0;\n  const shipping=delivery==="courier"?(total>=15000?0:300):0;\n  const rawBonusAmount=Math.max(0,Number(bonusAmount.replace(/\\D/g,""))||0);\n  const bonusWriteoff=verificationOk&&loyaltyJoined?Math.min(rawBonusAmount,Math.max(0,total-onlineDiscount)):0;\n  const payable=Math.max(0,total-onlineDiscount-bonusWriteoff+shipping);'''
if discount_anchor not in text:
    raise SystemExit("checkout-bonus-v84: payable anchor not found")
text = text.replace(discount_anchor, discount_patch, 1)

payment_anchor = '''        <section className="checkout-v69-section" aria-labelledby="v83-payment-title">\n          <h2 id="v83-payment-title">Способ оплаты</h2>'''
bonus_section = '''        <section className="checkout-v69-section checkout-v84-loyalty" aria-labelledby="v84-loyalty-title">\n          <h2 id="v84-loyalty-title">Бонусная программа</h2>\n          <div className="checkout-v84-loyalty-head"><div><b>{verificationOk?"Контакт подтверждён":"Подтвердите телефон или email"}</b><small>{verificationOk?"Можно подключить бонусную программу и списать доступные бонусы":"После подтверждения контакт будет связан с бонусным счётом"}</small></div><span>{verificationOk?"✓":""}</span></div>\n          <label className="checkout-v84-loyalty-toggle"><input type="checkbox" checked={loyaltyJoined} disabled={!verificationOk} onChange={event=>{setLoyaltyJoined(event.target.checked);if(!event.target.checked)setBonusAmount("")}}/><i>✓</i><span>Участвовать в бонусной программе</span></label>\n          {verificationOk&&loyaltyJoined&&<div className="checkout-v84-loyalty-body"><label><span>Списать бонусы</span><input inputMode="numeric" value={bonusAmount} onChange={event=>setBonusAmount(event.target.value.replace(/\\D/g,"").slice(0,8))} placeholder="0"/></label><p>Доступный баланс и лимит списания в production загружаются из программы лояльности после входа или подтверждения контакта.</p></div>}\n        </section>\n\n''' + payment_anchor
if payment_anchor not in text:
    raise SystemExit("checkout-bonus-v84: payment section anchor not found")
text = text.replace(payment_anchor, bonus_section, 1)

order_anchor = '{onlineDiscount>0&&<div className="discount"><dt>Скидка за предоплату</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl>'
order_patch = '{onlineDiscount>0&&<div className="discount"><dt>Скидка за предоплату</dt><dd>−{fmt(onlineDiscount)}</dd></div>}{bonusWriteoff>0&&<div className="discount"><dt>Бонусы</dt><dd>−{fmt(bonusWriteoff)}</dd></div>}</dl>'
text = text.replace(order_anchor, order_patch)

summary_anchor = '{onlineDiscount>0&&<div><dt>Скидка −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl>'
summary_patch = '{onlineDiscount>0&&<div><dt>Скидка −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}{bonusWriteoff>0&&<div><dt>Бонусы</dt><dd>−{fmt(bonusWriteoff)}</dd></div>}</dl>'
text = text.replace(summary_anchor, summary_patch)

page_path.write_text(text, encoding="utf-8")
print("Checkout bonus V84 applied")
