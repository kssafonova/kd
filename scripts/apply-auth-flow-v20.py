from pathlib import Path

page_path = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = "AUTH_FLOW_V20"
if marker in text:
    print("Auth flow V20 already applied")
    raise SystemExit(0)

start = text.find("function Account({ profile, close, notice, save, logout }")
end = text.find("function AccountFields(", start)
if start < 0 or end < 0:
    raise SystemExit("Account component boundaries were not found")

account = r'''function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  // AUTH_FLOW_V20
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
    if(profile){
      setDraft(profile);
      setMode("profile");
    }
  },[profile]);

  const cleanPhone=(value:string)=>value.replace(/[^\d+]/g,"");
  const validEmail=(value:string)=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
  const validPhone=(value:string)=>cleanPhone(value).replace(/\D/g,"").length>=10;
  const contactValid=method==="email"?validEmail(identifier):validPhone(identifier);
  const contactLabel=method==="email"?"email":"номер телефона";

  const switchMethod=(next:AuthMethod)=>{
    setMethod(next);
    setIdentifier(next==="email"?(profile?.email??""):(profile?.phone??""));
    setCode("");
    setStep("identify");
  };

  const requestCode=()=>{
    if(!contactValid){
      notice(method==="email"?"Введите корректный email":"Введите корректный номер телефона");
      return;
    }
    setStep("code");
    setCode("");
    notice(method==="phone"?"Демо: код из SMS — 1234":"Демо: код из письма — 1234");
  };

  const verifyCode=()=>{
    if(code.trim()!=="1234"){
      notice("Неверный код. Для демо используйте 1234");
      return;
    }
    const sameProfile=Boolean(profile&&(method==="email"?profile.email.trim().toLowerCase()===identifier.trim().toLowerCase():cleanPhone(profile.phone)===cleanPhone(identifier)));
    if(sameProfile&&profile){
      setDraft(profile);
      setMode("profile");
      setStep("identify");
      notice("Вход выполнен");
      return;
    }
    setDraft(current=>({...current,[method==="email"?"email":"phone"]:identifier.trim()}));
    setStep("register");
  };

  const register=()=>{
    const next={...draft,[method==="email"?"email":"phone"]:identifier.trim()};
    if(!next.name.trim()){
      notice("Введите имя");
      return;
    }
    save(next);
    setDraft(next);
    setMode("profile");
    setStep("identify");
    notice("Аккаунт создан");
  };

  const saveProfile=()=>{
    if(!draft.name.trim()){
      notice("Введите имя");
      return;
    }
    if(draft.email&&!validEmail(draft.email)){
      notice("Проверьте email");
      return;
    }
    if(draft.phone&&!validPhone(draft.phone)){
      notice("Проверьте номер телефона");
      return;
    }
    save(draft);
    notice("Данные профиля сохранены");
  };

  const signOut=()=>{
    logout();
    setDraft(blank);
    setIdentifier("");
    setCode("");
    setStep("identify");
    setMode("auth");
    notice("Вы вышли из аккаунта");
  };

  return <div className="overlay auth-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть личный кабинет"/><aside className="side-panel account auth-v20"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ЛИЧНЫЙ КАБИНЕТ</p>{mode==="profile"?<div className="auth-profile"><small>ПРОФИЛЬ</small><h2>{draft.name}, добро пожаловать</h2><span>Контакты и адрес подставятся при оформлении заказа.</span><AccountFields draft={draft} setDraft={setDraft}/><button className="primary auth-primary" onClick={saveProfile}>СОХРАНИТЬ ДАННЫЕ</button><button className="link auth-logout" onClick={signOut}>ВЫЙТИ</button></div>:<div className="auth-flow">{step==="identify"&&<><small>ВХОД И РЕГИСТРАЦИЯ</small><h2>Войти в аккаунт</h2><span>Выберите удобный способ. Пароль не нужен — пришлём одноразовый код.</span><div className="auth-methods" role="tablist" aria-label="Способ входа"><button type="button" role="tab" aria-selected={method==="phone"} className={method==="phone"?"active":""} onClick={()=>switchMethod("phone")}>По телефону</button><button type="button" role="tab" aria-selected={method==="email"} className={method==="email"?"active":""} onClick={()=>switchMethod("email")}>По email</button></div><label className="auth-field"><span>{method==="phone"?"Номер телефона":"Email"}</span><input type={method==="phone"?"tel":"email"} autoComplete={method==="phone"?"tel":"email"} inputMode={method==="phone"?"tel":"email"} value={identifier} onChange={event=>setIdentifier(event.target.value)} placeholder={method==="phone"?"+7 999 000-00-00":"name@example.com"} onKeyDown={event=>{if(event.key==="Enter")requestCode()}}/></label><button className="primary auth-primary" disabled={!identifier.trim()} onClick={requestCode}>ПОЛУЧИТЬ КОД</button><p className="auth-legal">Продолжая, вы соглашаетесь с условиями обработки персональных данных.</p></>}{step==="code"&&<><button className="auth-back" type="button" onClick={()=>{setStep("identify");setCode("")}}>← Назад</button><small>ПОДТВЕРЖДЕНИЕ</small><h2>Введите код</h2><span>Код отправлен на {contactLabel} <b>{identifier}</b>.</span><label className="auth-field auth-code-field"><span>Код подтверждения</span><input autoFocus inputMode="numeric" autoComplete="one-time-code" maxLength={4} value={code} onChange={event=>setCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000" onKeyDown={event=>{if(event.key==="Enter")verifyCode()}}/></label><button className="primary auth-primary" disabled={code.length!==4} onClick={verifyCode}>ПРОДОЛЖИТЬ</button><button className="link auth-resend" type="button" onClick={requestCode}>ОТПРАВИТЬ КОД ЕЩЁ РАЗ</button><p className="auth-demo-note">Демо-код: 1234</p></>}{step==="register"&&<><button className="auth-back" type="button" onClick={()=>setStep("code")}>← Назад</button><small>НОВЫЙ АККАУНТ</small><h2>Остался один шаг</h2><span>{method==="phone"?"Телефон подтверждён.":"Email подтверждён."} Укажите имя — остальные данные можно заполнить позже.</span><div className="auth-register-fields"><label className="auth-field"><span>Имя</span><input autoFocus value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})} placeholder="Имя"/></label><label className="auth-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})} placeholder="Необязательно"/></label>{method==="phone"?<label className="auth-field"><span>Email</span><input type="email" value={draft.email} onChange={event=>setDraft({...draft,email:event.target.value})} placeholder="Необязательно"/></label>:<label className="auth-field"><span>Телефон</span><input type="tel" value={draft.phone} onChange={event=>setDraft({...draft,phone:event.target.value})} placeholder="Необязательно"/></label>}</div><button className="primary auth-primary" disabled={!draft.name.trim()} onClick={register}>СОЗДАТЬ АККАУНТ</button></>}</div>}</aside></div>;
}

'''

page_path.write_text(text[:start] + account + text[end:], encoding="utf-8")
print("Auth flow V20 applied: phone/email passwordless login and registration")
