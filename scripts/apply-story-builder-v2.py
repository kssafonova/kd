from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

replacement = r'''function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart, openCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void; openCart:()=>void }) {
  type StoryKind = "bedroom" | "table";
  type StoryMode = "quick" | "builder" | null;
  type StoryLine = { key:string; product:Product; quantity:number; required?:boolean; subtitle:string };
  type AddedState = { title:string; lines:StoryLine[]; total:number };

  const [story,setStory]=useState<StoryKind|null>(null);
  const [mode,setMode]=useState<StoryMode>(null);
  const [builderStep,setBuilderStep]=useState(1);
  const [bedSize,setBedSize]=useState("");
  const [bedOptional,setBedOptional]=useState({blanket:true,pillow:true});
  const [bedQty,setBedQty]=useState({blanket:1,pillow:1});
  const [occasion,setOccasion]=useState("Чай для двоих");
  const [guests,setGuests]=useState<2|4|6>(2);
  const [tableOptional,setTableOptional]=useState({napkin:true,plate:false,vase:false,gift:false});
  const [added,setAdded]=useState<AddedState|null>(null);

  const track=(event:string,detail:Record<string,unknown>={})=>{
    if(typeof window==="undefined")return;
    const payload={event,capsule:"Лунная сказка",story:story??undefined,...detail};
    window.dispatchEvent(new CustomEvent("kd:analytics",{detail:payload}));
    const layer=(window as unknown as {dataLayer?:Record<string,unknown>[]}).dataLayer;
    layer?.push(payload);
  };

  useEffect(()=>{
    if(story)track("story_view",{story});
  // analytics fires only when the user opens a story
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[story]);

  useEffect(()=>{
    if(!story&&!mode&&!added)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[story,mode,added]);

  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={4:"/assets/images/KD-PD-1024-DARK02.png",6:"/assets/images/KD-PD-1026-BLUE01.png",3:"/assets/images/KD-PD-1023-BLUE02.png"};
  const prepare=(product:Product):Product=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const regularPrice=product.oldPrice??product.price;
    const preview=previewById[product.id];
    const variants=(product.colorVariants??[]).filter(variant=>variant.name===color);
    const skus=product.skus?.filter(s=>s.color===color).map(s=>({...s,price:regularPrice,...(preview?{image:preview,gallery:Array.from(new Set([preview,...s.gallery]))}:{})}));
    const sku=skus?.find(s=>s.color===color)??skus?.[0];
    return {...product,oldPrice:undefined,badge:undefined,image:preview??sku?.image??product.image,gallery:sku?.gallery??product.gallery,colorVariants:variants.length?variants:product.colorVariants,skus,selectedColor:sku?.color??color,selectedSize:sku?.size??product.selectedSize,selectedSkuId:sku?.id,price:regularPrice};
  };

  const lunaItems=editorial.productIds.map(id=>products.find(p=>p.id===id)).filter(Boolean).map(p=>prepare(p!));
  const itemById=(id:number)=>lunaItems.find(item=>item.id===id);
  const bedding=itemById(4)!;
  const blanket=itemById(6)!;
  const pillow=itemById(3)!;
  const tea=itemById(10)!;

  const virtualProduct=(id:number,name:string,price:number,image:string,note:string,color:string,size:string,article:string):Product=>({
    id,name,price,image,note,article,selectedColor:color,selectedSize:size,selectedSkuId:article,quantity:1,
    colorVariants:[{name:color,hex:color.includes("син")?"#1b2c49":"#e7ded0",image}],gallery:[image]
  });
  const napkin=virtualProduct(110,"Льняная салфетка с вышивкой",1490,"/assets/images/KD-PD-1027-MOL01.png","лён, вышивка","Молочный","45×45 см","KD-STORY-NAPKIN");
  const dessert=virtualProduct(111,"Тарелка десертная «Лунная сказка»",2990,"/assets/images/moon-plate.png","фарфор","Ночной синий","18 см","KD-STORY-PLATE");
  const vase=virtualProduct(112,"Ваза «Ледяные узоры»",5990,"/assets/images/caps_led_serviz.png","стекло","Ледяной","Стандарт","KD-STORY-VASE");
  const gift=virtualProduct(113,"Подарочная упаковка",490,"/assets/images/caps_luna_serviz2.png","премиальная упаковка","Молочный","Стандарт","KD-STORY-GIFT");

  const bedSizes=[
    {label:"Полуторный 140×220",price:29990,available:true},
    {label:"Евро 200×220",price:29990,available:true},
    {label:"Кинг сайз 220×240",price:31990,available:true},
  ];
  const bedSizePrice=bedSizes.find(option=>option.label===bedSize)?.price??0;
  const configuredBedding=():Product=>({
    ...bedding,
    price:bedSizePrice||29990,
    selectedSize:bedSize,
    quantity:1,
    skus:bedding.skus?.map(s=>s.size===bedSize?{...s,price:bedSizePrice||s.price}:s),
  });
  const fixed=(product:Product,quantity=1):Product=>{
    const color=product.selectedColor??product.colorVariants?.[0]?.name??"Молочный";
    const options=getProductSizeOptions(product,color);
    const size=options.length===1?options[0][0]:(product.selectedSize??options[0]?.[0]??"Стандарт");
    const sku=findProductSku(product,color,size);
    return {...product,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id??product.selectedSkuId,price:sku?.price??product.price,quantity};
  };

  const bedroomLines=():StoryLine[]=>{
    const lines:StoryLine[]=[];
    if(bedSize)lines.push({key:"bedding",product:configuredBedding(),quantity:1,required:true,subtitle:`Ночной синий · ${bedSize}`});
    if(bedOptional.blanket)lines.push({key:"blanket",product:fixed(blanket,bedQty.blanket),quantity:bedQty.blanket,subtitle:`Синий · ${fixed(blanket).selectedSize}`});
    if(bedOptional.pillow)lines.push({key:"pillow",product:fixed(pillow,bedQty.pillow),quantity:bedQty.pillow,subtitle:`Синий · ${fixed(pillow).selectedSize}`});
    return lines;
  };
  const tableLines=():StoryLine[]=>{
    const lines:StoryLine[]=[{key:"tea",product:fixed({...tea,price:4490},guests),quantity:guests,required:true,subtitle:`Ночной синий · ${guests} персон`}];
    if(tableOptional.napkin)lines.push({key:"napkin",product:{...napkin,quantity:guests},quantity:guests,subtitle:`Молочный · ${guests} шт.`});
    if(tableOptional.plate)lines.push({key:"plate",product:{...dessert,quantity:guests},quantity:guests,subtitle:`Ночной синий · ${guests} шт.`});
    if(tableOptional.vase)lines.push({key:"vase",product:vase,quantity:1,subtitle:"Ледяной · 1 шт."});
    if(tableOptional.gift)lines.push({key:"gift",product:gift,quantity:1,subtitle:"1 упаковка"});
    return lines;
  };
  const currentLines=()=>story==="table"?tableLines():bedroomLines();
  const lineTotal=(line:StoryLine)=>line.product.price*line.quantity;
  const totalOf=(lines:StoryLine[])=>lines.reduce((sum,line)=>sum+lineTotal(line),0);
  const unitsOf=(lines:StoryLine[])=>lines.reduce((sum,line)=>sum+line.quantity,0);
  const deliveryText=(total:number)=>total>=15000?"Бесплатная доставка доступна":`До бесплатной доставки ${fmt(15000-total)}`;

  const storyDefs=[
    {id:"bedroom" as const,kicker:"СПАЛЬНЯ",title:"Спальня для долгих вечеров",intro:"Тёмный шёлк, прохладный синий и кружево — готовый образ, который можно купить целиком или настроить под себя.",images:editorial.images.slice(0,3),price:47970},
    {id:"table" as const,kicker:"СЕРВИРОВКА",title:"Чай для двоих",intro:"Вечерний чай и глубокий синий фарфор. Готовая сервировка для двух персон с возможностью изменить состав.",images:editorial.images.slice(3,6),price:11960},
  ];
  const activeStory=storyDefs.find(item=>item.id===story);

  const closeAll=()=>{setMode(null);setStory(null);setBuilderStep(1)};
  const openStory=(id:StoryKind)=>{
    setStory(id);setMode(null);setBuilderStep(1);setAdded(null);
    if(id==="bedroom"){
      setBedSize("");setBedOptional({blanket:true,pillow:true});setBedQty({blanket:1,pillow:1});
    }else{
      setOccasion("Чай для двоих");setGuests(2);setTableOptional({napkin:true,plate:false,vase:false,gift:false});
    }
  };
  const openQuick=()=>{setMode("quick");track("story_quick_add_open")};
  const openBuilder=()=>{setMode("builder");setBuilderStep(1);track("builder_open")};

  const commit=(title:string,lines:StoryLine[])=>{
    lines.forEach(line=>addToCart({...line.product,quantity:line.quantity}));
    const total=totalOf(lines);
    setAdded({title,lines,total});
    setMode(null);
    track(mode==="builder"?"builder_add_to_cart":"story_quick_add",{uniqueItems:lines.length,totalUnits:unitsOf(lines),totalPrice:total});
  };

  const quantity=(value:number,onChange:(next:number)=>void,label:string)=><div className="story-v2-qty" role="group" aria-label={`Количество: ${label}`}><button type="button" onClick={()=>onChange(Math.max(1,value-1))} aria-label={`Уменьшить количество ${label}`}>−</button><b>{value}</b><button type="button" onClick={()=>onChange(value+1)} aria-label={`Увеличить количество ${label}`}>+</button></div>;

  const productRow=(line:StoryLine,controls?:React.ReactNode)=><div className="story-v2-product-row" key={line.key}>
    <img src={assetUrl(line.product.image)} alt={line.product.name}/>
    <div className="story-v2-product-copy"><strong>{line.product.name}</strong><span>{line.subtitle}</span><small>{fmt(line.product.price)} за шт.</small></div>
    <div className="story-v2-product-side">{controls??<b>{line.quantity>1?`${line.quantity} × `:""}{fmt(lineTotal(line))}</b>}</div>
  </div>;

  const summary=(lines:StoryLine[],label?:string)=><aside className="story-v2-summary">
    {label&&<p>{label}</p>}
    <div><span>{lines.length} {lines.length===1?"товар":"товара"} / {unitsOf(lines)} шт.</span><strong>{fmt(totalOf(lines))}</strong></div>
    <small>{deliveryText(totalOf(lines))}</small>
  </aside>;

  const bedroomQuick=()=>{
    const lines=bedroomLines();
    const selectedTarget=1+(bedOptional.blanket?1:0)+(bedOptional.pillow?1:0);
    const ready=lines.length;
    const canAdd=Boolean(bedSize);
    return <>
      <header className="story-v2-sheet-head"><div><small>ГОТОВАЯ ИСТОРИЯ</small><h2>Спальня для долгих вечеров</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="story-v2-sheet-body">
        <div className={`story-v2-quick-required ${!bedSize?"needs-action":""}`}>
          <div className="story-v2-required-label"><span>Обязательно</span>{!bedSize&&<b>Нужен размер</b>}</div>
          <div className="story-v2-quick-title"><img src={assetUrl(bedding.image)} alt={bedding.name}/><div><strong>{bedding.name}</strong><span>Ночной синий</span></div></div>
          <div className="story-v2-size-list" role="radiogroup" aria-label="Выберите размер комплекта">
            {bedSizes.map(option=><button key={option.label} type="button" className={bedSize===option.label?"active":""} disabled={!option.available} onClick={()=>{setBedSize(option.label);track("variant_selected",{size:option.label,price:option.price})}} aria-pressed={bedSize===option.label}><span>{option.label}</span><b>{option.available?fmt(option.price):"Нет в наличии"}</b></button>)}
          </div>
          {!bedSize&&<p className="story-v2-validation">Выберите размер основы, чтобы добавить готовую историю.</p>}
        </div>
        <div className="story-v2-quick-options"><p>ДОПОЛНЕНИЯ</p>
          {[{key:"blanket" as const,item:blanket,selected:bedOptional.blanket,qty:bedQty.blanket},{key:"pillow" as const,item:pillow,selected:bedOptional.pillow,qty:bedQty.pillow}].map(row=>{
            const configured=fixed(row.item,row.qty);
            return <div className={`story-v2-toggle-row ${row.selected?"selected":""}`} key={row.key}>
              <img src={assetUrl(configured.image)} alt={configured.name}/>
              <div><strong>{configured.name}</strong><span>{configured.selectedSize}</span><small>{fmt(configured.price)}</small></div>
              <button className="story-v2-check" type="button" onClick={()=>{setBedOptional(current=>({...current,[row.key]:!current[row.key]}));track(row.selected?"builder_item_remove":"builder_item_add",{item:row.key})}} aria-pressed={row.selected} aria-label={row.selected?`Убрать ${configured.name}`:`Добавить ${configured.name}`}>{row.selected?"✓":""}</button>
            </div>
          })}
        </div>
      </div>
      <footer className="story-v2-sheet-footer">
        <div className="story-v2-ready"><span><b>{ready} из {selectedTarget}</b> товаров готовы</span><strong>{fmt(totalOf(lines))}</strong></div>
        <small>{deliveryText(totalOf(lines))}</small>
        <button className="story-v2-primary" disabled={!canAdd} onClick={()=>canAdd&&commit("Спальня для долгих вечеров",lines)}>{canAdd?`Добавить историю в корзину · ${fmt(totalOf(lines))}`:"Выберите размер"}</button>
        <button className="story-v2-link" type="button" onClick={openBuilder}>Не подходит состав? <u>Настроить историю</u></button>
      </footer>
    </>;
  };

  const tableQuick=()=>{
    const lines=tableLines();
    return <>
      <header className="story-v2-sheet-head"><div><small>ГОТОВАЯ ИСТОРИЯ</small><h2>Чай для двоих</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="story-v2-sheet-body">
        <div className="story-v2-quick-options"><p>ГОТОВЫЙ СОСТАВ</p>
          {productRow(lines[0])}
          {productRow(lines.find(line=>line.key==="napkin")!)}
        </div>
        <div className="story-v2-person-note"><span>2 персоны</span><p>Хотите сервировку на 4 или 6 персон? Настройте историю — количество предметов пересчитается автоматически.</p></div>
      </div>
      <footer className="story-v2-sheet-footer">
        <div className="story-v2-ready"><span><b>{lines.length}</b> товара / {unitsOf(lines)} шт.</span><strong>{fmt(totalOf(lines))}</strong></div>
        <small>{deliveryText(totalOf(lines))}</small>
        <button className="story-v2-primary" onClick={()=>commit("Чай для двоих",lines)}>Добавить историю в корзину · {fmt(totalOf(lines))}</button>
        <button className="story-v2-link" type="button" onClick={openBuilder}>Нужно больше персон? <u>Настроить сервировку</u></button>
      </footer>
    </>;
  };

  const builderLines=story==="table"?tableLines():bedroomLines();
  const bedroomBuilder=()=>{
    const next=()=>setBuilderStep(step=>Math.min(4,step+1));
    const back=()=>setBuilderStep(step=>Math.max(1,step-1));
    return <div className="story-v2-builder-layout">
      <section className="story-v2-builder-main">
        <header className="story-v2-builder-head"><div><small>НАСТРОИТЬ ИСТОРИЮ</small><h2>Спальня для долгих вечеров</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <nav className="story-v2-steps" aria-label="Шаги конструктора">{["Основа","Размер","Дополнения","Ваш образ"].map((label,index)=><button key={label} type="button" className={builderStep===index+1?"active":builderStep>index+1?"done":""} onClick={()=>index+1<=builderStep&&setBuilderStep(index+1)}><b>{index+1}</b><span>{label}</span></button>)}</nav>
        <div className="story-v2-step-content">
          {builderStep===1&&<><div className="story-v2-step-title"><small>ШАГ 1</small><h3>Основа</h3><p>Основа образа обязательна. Она уже добавлена — останется выбрать подходящий размер.</p></div><div className="story-v2-base-card"><img src={assetUrl(bedding.image)} alt={bedding.name}/><div><span>ОБЯЗАТЕЛЬНО</span><strong>{bedding.name}</strong><small>Ночной синий</small><b>от {fmt(29990)}</b></div><i>✓</i></div></>}
          {builderStep===2&&<><div className="story-v2-step-title"><small>ШАГ 2</small><h3>Выберите размер</h3><p>Размер комплекта — обязательный параметр. Цена образа обновится сразу после выбора.</p></div><div className="story-v2-builder-sizes">{bedSizes.map(option=><button key={option.label} type="button" className={bedSize===option.label?"active":""} disabled={!option.available} onClick={()=>{setBedSize(option.label);track("variant_selected",{size:option.label,price:option.price})}}><span>{option.label}</span><b>{option.available?fmt(option.price):"Нет в наличии"}</b></button>)}</div>{!bedSize&&<p className="story-v2-validation">Размер пока не выбран — основа не входит в итоговую стоимость.</p>}</>}
          {builderStep===3&&<><div className="story-v2-step-title"><small>ШАГ 3</small><h3>Дополните образ</h3><p>Плед и подушка уже входят в preset. Их можно убрать или изменить количество.</p></div><div className="story-v2-builder-addons">{[{key:"blanket" as const,item:blanket,selected:bedOptional.blanket,qty:bedQty.blanket},{key:"pillow" as const,item:pillow,selected:bedOptional.pillow,qty:bedQty.pillow}].map(row=>{const configured=fixed(row.item,row.qty);return <div className={`story-v2-addon-card ${row.selected?"selected":""}`} key={row.key}><button className="story-v2-addon-media" type="button" onClick={()=>setBedOptional(current=>({...current,[row.key]:!current[row.key]}))}><img src={assetUrl(configured.image)} alt={configured.name}/><span>{row.selected?"Добавлено":"Добавить"}</span></button><div><strong>{configured.name}</strong><small>Размер: {configured.selectedSize}</small><b>{fmt(configured.price)}</b>{row.selected&&quantity(row.qty,nextQty=>setBedQty(current=>({...current,[row.key]:nextQty})),configured.name)}</div></div>})}</div></>}
          {builderStep===4&&<><div className="story-v2-step-title"><small>ШАГ 4</small><h3>Ваш образ</h3><p>Проверьте состав. В корзину попадут отдельные товары с выбранными вариантами и количеством.</p></div><div className="story-v2-review">{builderLines.map(line=>productRow(line,line.key==="blanket"?quantity(bedQty.blanket,nextQty=>setBedQty(current=>({...current,blanket:nextQty})),line.product.name):line.key==="pillow"?quantity(bedQty.pillow,nextQty=>setBedQty(current=>({...current,pillow:nextQty})),line.product.name):undefined))}</div></>}
        </div>
        <div className="story-v2-builder-nav">{builderStep>1?<button className="story-v2-secondary" type="button" onClick={back}>Назад</button>:<span/>}{builderStep<4?<div>{builderStep===3&&<button className="story-v2-skip" type="button" onClick={()=>setBuilderStep(4)}>Пропустить</button>}<button className="story-v2-primary compact" type="button" disabled={builderStep===2&&!bedSize} onClick={next}>{builderStep===2&&!bedSize?"Выберите размер":"Продолжить"}</button></div>:<button className="story-v2-primary compact" type="button" disabled={!bedSize} onClick={()=>bedSize&&commit("Спальня для долгих вечеров",builderLines)}>Добавить образ в корзину · {fmt(totalOf(builderLines))}</button>}</div>
      </section>
      <div className="story-v2-builder-aside">{summary(builderLines,bedSize?"ВАШ ОБРАЗ":"ВЫБЕРИТЕ РАЗМЕР")}</div>
    </div>;
  };

  const tableBuilder=()=>{
    const next=()=>setBuilderStep(step=>Math.min(4,step+1));
    const back=()=>setBuilderStep(step=>Math.max(1,step-1));
    const toggle=(key:keyof typeof tableOptional)=>{setTableOptional(current=>({...current,[key]:!current[key]}));track(tableOptional[key]?"builder_item_remove":"builder_item_add",{item:key})};
    return <div className="story-v2-builder-layout">
      <section className="story-v2-builder-main">
        <header className="story-v2-builder-head"><div><small>НАСТРОИТЬ СЕРВИРОВКУ</small><h2>Лунная сказка</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <nav className="story-v2-steps" aria-label="Шаги конструктора">{["Повод","Персоны","Дополнения","Ваш набор"].map((label,index)=><button key={label} type="button" className={builderStep===index+1?"active":builderStep>index+1?"done":""} onClick={()=>index+1<=builderStep&&setBuilderStep(index+1)}><b>{index+1}</b><span>{label}</span></button>)}</nav>
        <div className="story-v2-step-content">
          {builderStep===1&&<><div className="story-v2-step-title"><small>ШАГ 1</small><h3>Выберите повод</h3><p>Состав можно изменить позже — выбор задаёт только стартовый сценарий.</p></div><div className="story-v2-occasion-grid">{["Чай для двоих","Ужин с близкими","Праздничный стол"].map(value=><button key={value} type="button" className={occasion===value?"active":""} onClick={()=>setOccasion(value)}><span>{value}</span><small>{value==="Чай для двоих"?"Камерная сервировка":value==="Ужин с близкими"?"Спокойный вечер":"Торжественный стол"}</small></button>)}</div></>}
          {builderStep===2&&<><div className="story-v2-step-title"><small>ШАГ 2</small><h3>Количество персон</h3><p>Количество чайных пар, салфеток и тарелок пересчитывается автоматически.</p></div><div className="story-v2-guests">{([2,4,6] as const).map(value=><button key={value} className={guests===value?"active":""} type="button" onClick={()=>{setGuests(value);track("variant_selected",{guests:value})}}><b>{value}</b><span>персоны</span></button>)}</div>{productRow(tableLines()[0])}</>}
          {builderStep===3&&<><div className="story-v2-step-title"><small>ШАГ 3</small><h3>Дополните сервировку</h3><p>Салфетки входят в preset. Остальные предметы можно добавить по желанию.</p></div><div className="story-v2-table-addons">{[{key:"napkin" as const,item:napkin,label:`${guests} шт.`},{key:"plate" as const,item:dessert,label:`${guests} шт.`},{key:"vase" as const,item:vase,label:"1 шт."},{key:"gift" as const,item:gift,label:"1 шт."}].map(row=>{const selected=tableOptional[row.key];return <button type="button" className={`story-v2-table-addon ${selected?"selected":""}`} key={row.key} onClick={()=>toggle(row.key)}><img src={assetUrl(row.item.image)} alt={row.item.name}/><span><strong>{row.item.name}</strong><small>{row.label}</small><b>{fmt(row.item.price)}</b></span><i>{selected?"✓":"+"}</i></button>})}</div></>}
          {builderStep===4&&<><div className="story-v2-step-title"><small>ШАГ 4</small><h3>Ваш набор</h3><p>{occasion} · {guests} персон. В корзину попадут отдельные позиции.</p></div><div className="story-v2-review">{builderLines.map(line=>productRow(line))}</div></>}
        </div>
        <div className="story-v2-builder-nav">{builderStep>1?<button className="story-v2-secondary" type="button" onClick={back}>Назад</button>:<span/>}{builderStep<4?<div>{builderStep===3&&<button className="story-v2-skip" type="button" onClick={()=>{setTableOptional({napkin:false,plate:false,vase:false,gift:false});setBuilderStep(4)}}>Пропустить</button>}<button className="story-v2-primary compact" type="button" onClick={next}>Продолжить</button></div>:<button className="story-v2-primary compact" type="button" onClick={()=>commit(occasion,builderLines)}>Добавить набор в корзину · {fmt(totalOf(builderLines))}</button>}</div>
      </section>
      <div className="story-v2-builder-aside">{summary(builderLines,`${occasion.toUpperCase()} · ${guests} ПЕРСОН`)}</div>
    </div>;
  };

  return <div className="luna-story-v2-page">
    <section className="luna-story-v2-head"><p>КАПСУЛА</p><h1>Лунная сказка</h1><span>{editorial.lead}</span></section>
    <div className="luna-story-v2-list">{storyDefs.map((entry,index)=><section className={`luna-story-v2-entry ${index%2?"reverse":""}`} key={entry.id}>
      <button className="luna-story-v2-media" type="button" onClick={()=>openStory(entry.id)} aria-label={`Открыть историю ${entry.title}`}>
        <span className="luna-story-v2-media-grid">{entry.images.map((image,imageIndex)=><img src={assetUrl(image)} alt={`${entry.title}, фото ${imageIndex+1}`} key={`${entry.id}-${image}`}/>)}</span>
      </button>
      <div className="luna-story-v2-copy"><small>{entry.kicker}</small><h2>{entry.title}</h2><p>{entry.intro}</p><span>{entry.id==="bedroom"?"3 предмета":"4 предмета"} · от {fmt(entry.price)}</span><button type="button" onClick={()=>openStory(entry.id)}>ОТКРЫТЬ ИСТОРИЮ <Icon name="arrow"/></button></div>
    </section>)}</div>

    {story&&activeStory&&<div className="story-v2-layer" role="dialog" aria-modal="true" aria-label={activeStory.title}>
      <div className="story-v2-landing">
        <header className="story-v2-landing-head"><div><small>ЛУННАЯ СКАЗКА · {activeStory.kicker}</small><h2>{activeStory.title}</h2></div><button type="button" onClick={closeAll} aria-label="Закрыть историю"><Icon name="close"/></button></header>
        <div className="story-v2-landing-grid"><div className="story-v2-landing-gallery">{activeStory.images.map((image,index)=><img src={assetUrl(image)} alt={`${activeStory.title}, фото ${index+1}`} key={image}/>)}</div><aside className="story-v2-landing-info"><p>{activeStory.intro}</p><div className="story-v2-composition"><small>ГОТОВЫЙ ОБРАЗ</small>{(story==="bedroom"?[{name:bedding.name,meta:"Обязательно · выберите размер"},{name:blanket.name,meta:"Добавлено · можно убрать"},{name:pillow.name,meta:"Добавлено · можно убрать"}]:[{name:tea.name,meta:"2 шт. · основа"},{name:napkin.name,meta:"2 шт. · добавлено"}]).map(item=><div key={item.name}><strong>{item.name}</strong><span>{item.meta}</span></div>)}</div><div className="story-v2-landing-price"><span>{story==="bedroom"?"3 предмета":"4 предмета"}</span><strong>от {fmt(activeStory.price)}</strong></div><button className="story-v2-primary" type="button" onClick={openQuick}>Купить историю · от {fmt(activeStory.price)}</button><button className="story-v2-secondary wide" type="button" onClick={openBuilder}>{story==="table"?"Настроить сервировку":"Настроить под себя"}</button><p className="story-v2-landing-note">Без перехода в карточку товара. Состав и варианты настраиваются здесь.</p></aside></div>
      </div>
    </div>}

    {mode==="quick"&&story&&<div className="story-v2-sub-layer" role="dialog" aria-modal="true" aria-label="Купить историю"><button className="story-v2-backdrop" type="button" onClick={()=>setMode(null)} aria-label="Закрыть"/><section className="story-v2-sheet">{story==="bedroom"?bedroomQuick():tableQuick()}</section></div>}

    {mode==="builder"&&story&&<div className="story-v2-builder-layer" role="dialog" aria-modal="true" aria-label="Конструктор истории"><button className="story-v2-backdrop" type="button" onClick={()=>setMode(null)} aria-label="Закрыть"/><div className="story-v2-builder">{story==="bedroom"?bedroomBuilder():tableBuilder()}</div></div>}

    {added&&<div className="story-v2-sub-layer story-v2-confirm-layer" role="dialog" aria-modal="true" aria-label="История добавлена в корзину"><button className="story-v2-backdrop" type="button" onClick={()=>setAdded(null)} aria-label="Закрыть"/><section className="story-v2-confirm"><span className="story-v2-confirm-mark">✓</span><small>ГОТОВО</small><h2>История добавлена в корзину</h2><p>{added.title}</p><div className="story-v2-confirm-list">{added.lines.map(line=>productRow(line))}</div>{summary(added.lines)}<button className="story-v2-primary" type="button" onClick={()=>{setAdded(null);setStory(null);openCart();track("view_cart")}}>Перейти в корзину</button><button className="story-v2-secondary wide" type="button" onClick={()=>{setAdded(null);setStory(null);setBuilderStep(1)}}>Продолжить покупки</button></section></div>}
  </div>;
}
'''

pattern = r'function LunaEditorialView\([\s\S]*?\n}\n\nfunction EditorialView'
if not re.search(pattern, page):
    raise SystemExit("LunaEditorialView block not found")
page = re.sub(pattern, replacement + "\n\nfunction EditorialView", page, count=1)

# Add openCart to the editorial bridge and keep current product/cart APIs intact.
page = re.sub(
    r'function EditorialView\(\{ editorial, selectProduct, favorite, favorites, quickAdd, addToCart \}: \{ editorial:Editorial; selectProduct:\(product:Product\)=>void; favorite:\(id:number\)=>void; favorites:number\[\]; quickAdd:\(product:Product\)=>void; addToCart:\(product:Product\)=>void \}\)',
    'function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart, openCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void; openCart:()=>void })',
    page,
    count=1,
)
page = page.replace(
    '<LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd} addToCart={addToCart}/>',
    '<LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd} addToCart={addToCart} openCart={openCart}/>',
    1,
)

# Allow story flows to put real SKU lines into the cart without forcing the cart drawer open.
page = re.sub(
    r'const add = \(product: Product, chosenSize = size, quantity = product\.quantity \?\? 1(?:, openDrawer = true)?\) => \{',
    'const add = (product: Product, chosenSize = size, quantity = product.quantity ?? 1, openDrawer = true) => {',
    page,
    count=1,
)
page = page.replace('setPlpSize(null); setSizeSheet(false); setCartOpen(true);', 'setPlpSize(null); setSizeSheet(false); if(openDrawer)setCartOpen(true);', 1)
page = re.sub(
    r'<EditorialView editorial=\{editorial\} selectProduct=\{openProduct\} favorite=\{favorite\} favorites=\{favorites\} quickAdd=\{setPlpSize\} addToCart=\{\(product\)=>add\(product,product\.selectedSize,product\.quantity\)\} ?/?>',
    '<EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} addToCart={(product)=>add(product,product.selectedSize,product.quantity,false)} openCart={()=>setCartOpen(true)} />',
    page,
    count=1,
)

page_path.write_text(page,encoding="utf-8")

css = re.sub(r'\n?/\* STORY_BUILDER_V2 \*/[\s\S]*?/\* END_STORY_BUILDER_V2 \*/', '', css)
css += r'''

/* STORY_BUILDER_V2 */
.luna-story-v2-page{background:#fff;color:#1d1d1f;min-height:70vh}
.luna-story-v2-head{padding:64px 4vw 52px;text-align:center;display:grid;justify-items:center;gap:12px}
.luna-story-v2-head p,.luna-story-v2-copy small,.story-v2-landing-head small,.story-v2-sheet-head small,.story-v2-builder-head small,.story-v2-step-title>small,.story-v2-composition>small,.story-v2-quick-options>p{font-size:9px;letter-spacing:.18em;margin:0;color:#777}
.luna-story-v2-head h1{font:400 clamp(38px,5vw,72px)/.96 Georgia,serif;margin:0}
.luna-story-v2-head span{max-width:620px;font-size:12px;line-height:1.7;color:#777}
.luna-story-v2-list{display:grid;gap:88px;padding:0 4vw 96px}
.luna-story-v2-entry{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(300px,.55fr);gap:clamp(36px,5vw,92px);align-items:center}
.luna-story-v2-entry.reverse{grid-template-columns:minmax(300px,.55fr) minmax(0,1.45fr)}
.luna-story-v2-entry.reverse .luna-story-v2-media{order:2}.luna-story-v2-entry.reverse .luna-story-v2-copy{order:1}
.luna-story-v2-media{border:0;background:none;padding:0;text-align:left;cursor:pointer;min-width:0}
.luna-story-v2-media-grid{display:grid;grid-template-columns:1.6fr 1fr;grid-template-rows:1fr 1fr;gap:6px;height:min(68vw,720px);overflow:hidden;background:#f4f4f1}
.luna-story-v2-media-grid img{width:100%;height:100%;object-fit:cover;display:block}.luna-story-v2-media-grid img:first-child{grid-row:1/3}
.luna-story-v2-copy{display:grid;align-content:center;gap:18px;max-width:430px}.luna-story-v2-copy h2{font:400 clamp(34px,4vw,58px)/1 Georgia,serif;margin:0}.luna-story-v2-copy p{font-size:12px;line-height:1.75;color:#666;margin:0}.luna-story-v2-copy>span{font-size:11px}.luna-story-v2-copy>button{width:max-content;display:flex;align-items:center;gap:8px;border:0;border-bottom:1px solid #1d1d1f;background:none;padding:0 0 5px;font:inherit;font-size:9px;letter-spacing:.1em;cursor:pointer}.luna-story-v2-copy>button svg{width:14px;height:14px}
.story-v2-layer,.story-v2-sub-layer,.story-v2-builder-layer{position:fixed;inset:0;z-index:140;background:rgba(17,23,24,.28);display:flex;align-items:center;justify-content:center;padding:28px;animation:storyFade .22s ease both}.story-v2-sub-layer,.story-v2-builder-layer{z-index:160}.story-v2-backdrop{position:absolute;inset:0;border:0;background:transparent;cursor:default}
.story-v2-landing{position:relative;width:min(1280px,96vw);height:min(860px,92vh);background:#fff;overflow:auto;box-shadow:0 28px 80px rgba(0,0,0,.16);animation:storyRise .28s ease both}
.story-v2-landing-head,.story-v2-sheet-head,.story-v2-builder-head{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;padding:26px 30px;border-bottom:1px solid #e8e8e5}.story-v2-landing-head>div,.story-v2-sheet-head>div,.story-v2-builder-head>div{display:grid;gap:7px}.story-v2-landing-head h2,.story-v2-sheet-head h2,.story-v2-builder-head h2{font:400 28px/1.08 Georgia,serif;margin:0}.story-v2-landing-head>button,.story-v2-sheet-head>button,.story-v2-builder-head>button{width:44px;height:44px;border:0;background:none;display:grid;place-items:center;cursor:pointer}.story-v2-landing-head svg,.story-v2-sheet-head svg,.story-v2-builder-head svg{width:21px;height:21px}
.story-v2-landing-grid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(360px,.6fr);min-height:calc(100% - 98px)}.story-v2-landing-gallery{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;background:#f2f2ef}.story-v2-landing-gallery img{width:100%;height:100%;min-height:280px;object-fit:cover;display:block}.story-v2-landing-gallery img:first-child{grid-column:1/3;min-height:420px}.story-v2-landing-info{padding:42px 36px;display:flex;flex-direction:column;align-self:stretch}.story-v2-landing-info>p{font-size:12px;line-height:1.75;color:#666;margin:0 0 30px}.story-v2-composition{border-top:1px solid #ddd;border-bottom:1px solid #ddd;padding:24px 0;display:grid;gap:0}.story-v2-composition>small{margin-bottom:12px}.story-v2-composition>div{display:grid;gap:3px;padding:13px 0;border-top:1px solid #eee}.story-v2-composition>div:first-of-type{border-top:0}.story-v2-composition strong{font-size:12px;font-weight:500}.story-v2-composition span{font-size:10px;color:#777}.story-v2-landing-price{display:flex;justify-content:space-between;align-items:baseline;padding:24px 0}.story-v2-landing-price span{font-size:10px;color:#777}.story-v2-landing-price strong{font-size:20px;font-weight:400}.story-v2-landing-note{font-size:9px!important;line-height:1.5!important;text-align:center;margin:12px 0 0!important;color:#8a8a88!important}
.story-v2-primary{min-height:50px;border:0;background:#2F4A4A;color:#fff;padding:0 22px;font:inherit;font-size:10px;letter-spacing:.08em;cursor:pointer;transition:background .2s,opacity .2s}.story-v2-primary:hover:not(:disabled){background:#223b3b}.story-v2-primary:disabled{background:#c9ccd1;cursor:not-allowed}.story-v2-primary.compact{min-width:260px}.story-v2-secondary{min-height:48px;border:1px solid #bfc2c0;background:#fff;color:#1d1d1f;padding:0 22px;font:inherit;font-size:10px;letter-spacing:.06em;cursor:pointer}.story-v2-secondary.wide{width:100%;margin-top:10px}.story-v2-link{border:0;background:none;min-height:44px;font:inherit;font-size:10px;color:#666;cursor:pointer;padding:10px}.story-v2-skip{min-height:44px;border:0;background:none;font:inherit;font-size:10px;text-decoration:underline;cursor:pointer;padding:0 14px}
.story-v2-sheet{position:absolute;z-index:2;right:0;top:0;width:min(620px,100vw);height:100%;background:#fff;display:flex;flex-direction:column;box-shadow:-24px 0 70px rgba(0,0,0,.12);animation:storyDrawer .28s ease both}.story-v2-sheet-body{flex:1;overflow:auto;padding:22px 28px 30px}.story-v2-quick-required{border:1px solid #dededb;padding:18px;transition:border-color .2s,background .2s}.story-v2-quick-required.needs-action{border-color:#a85b50;background:#fffaf9}.story-v2-required-label{display:flex;justify-content:space-between;gap:10px;margin-bottom:14px}.story-v2-required-label span,.story-v2-required-label b{font-size:8px;letter-spacing:.12em}.story-v2-required-label b{color:#a44337}.story-v2-quick-title{display:grid;grid-template-columns:84px 1fr;gap:14px;align-items:center;margin-bottom:18px}.story-v2-quick-title img{width:84px;height:84px;object-fit:cover}.story-v2-quick-title>div{display:grid;gap:5px}.story-v2-quick-title strong{font-size:13px;font-weight:500}.story-v2-quick-title span{font-size:10px;color:#777}.story-v2-size-list,.story-v2-builder-sizes{display:grid}.story-v2-size-list button,.story-v2-builder-sizes button{min-height:52px;border:0;border-top:1px solid #ddd;background:#fff;display:flex;align-items:center;justify-content:space-between;text-align:left;padding:0 10px;font:inherit;cursor:pointer}.story-v2-size-list button:last-child,.story-v2-builder-sizes button:last-child{border-bottom:1px solid #ddd}.story-v2-size-list button.active,.story-v2-builder-sizes button.active{background:#f1f5f4;box-shadow:inset 3px 0 #2F4A4A}.story-v2-size-list button:disabled,.story-v2-builder-sizes button:disabled{color:#aaa;text-decoration:line-through;cursor:not-allowed}.story-v2-size-list button span,.story-v2-builder-sizes button span{font-size:11px}.story-v2-size-list button b,.story-v2-builder-sizes button b{font-size:11px;font-weight:400}.story-v2-validation{margin:12px 0 0;color:#a44337;font-size:10px;line-height:1.45}.story-v2-quick-options{margin-top:28px}.story-v2-quick-options>p{margin-bottom:10px}.story-v2-toggle-row{display:grid;grid-template-columns:72px 1fr 44px;gap:13px;align-items:center;padding:13px 0;border-top:1px solid #e4e4e1}.story-v2-toggle-row img{width:72px;height:72px;object-fit:cover}.story-v2-toggle-row>div{display:grid;gap:4px}.story-v2-toggle-row strong{font-size:11px;font-weight:500}.story-v2-toggle-row span,.story-v2-toggle-row small{font-size:9px;color:#777}.story-v2-check{width:44px;height:44px;border:1px solid #bbb;background:#fff;cursor:pointer;font-size:14px}.story-v2-toggle-row.selected .story-v2-check{background:#2F4A4A;color:#fff;border-color:#2F4A4A}.story-v2-person-note{padding:22px 0;border-top:1px solid #ddd;margin-top:20px}.story-v2-person-note span{font:400 20px Georgia,serif}.story-v2-person-note p{font-size:10px;line-height:1.55;color:#777}
.story-v2-sheet-footer{border-top:1px solid #ddd;padding:17px 28px 22px;background:#fff}.story-v2-ready{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:5px}.story-v2-ready span{font-size:10px;color:#777}.story-v2-ready span b{color:#1d1d1f}.story-v2-ready strong{font-size:18px;font-weight:400}.story-v2-sheet-footer>small{display:block;font-size:9px;color:#62706d;margin-bottom:12px}.story-v2-sheet-footer>.story-v2-primary{width:100%}
.story-v2-builder{position:relative;z-index:2;width:min(1240px,96vw);max-height:94vh;background:#fff;overflow:auto;box-shadow:0 28px 80px rgba(0,0,0,.16);animation:storyRise .28s ease both}.story-v2-builder-layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;min-height:min(820px,94vh)}.story-v2-builder-main{min-width:0;display:flex;flex-direction:column;border-right:1px solid #e3e3df}.story-v2-builder-head{padding:24px 30px}.story-v2-steps{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #ddd}.story-v2-steps button{min-height:68px;border:0;border-right:1px solid #eee;background:#fff;display:flex;align-items:center;justify-content:center;gap:8px;font:inherit;color:#999;cursor:default}.story-v2-steps button b{width:23px;height:23px;border:1px solid #bbb;border-radius:50%;display:grid;place-items:center;font-size:9px;font-weight:400}.story-v2-steps button span{font-size:9px}.story-v2-steps button.active,.story-v2-steps button.done{color:#1d1d1f;cursor:pointer}.story-v2-steps button.active b,.story-v2-steps button.done b{background:#2F4A4A;color:#fff;border-color:#2F4A4A}.story-v2-step-content{flex:1;padding:34px 38px 24px;overflow:auto}.story-v2-step-title{max-width:620px;margin-bottom:28px}.story-v2-step-title h3{font:400 34px/1.05 Georgia,serif;margin:7px 0 10px}.story-v2-step-title p{font-size:11px;line-height:1.65;color:#777;margin:0}.story-v2-base-card{display:grid;grid-template-columns:180px 1fr 44px;gap:22px;align-items:center;border:1px solid #ddd;padding:14px;max-width:680px}.story-v2-base-card img{width:180px;aspect-ratio:1/1;object-fit:cover}.story-v2-base-card>div{display:grid;gap:7px}.story-v2-base-card span{font-size:8px;letter-spacing:.12em;color:#2F4A4A}.story-v2-base-card strong{font:400 20px Georgia,serif}.story-v2-base-card small{font-size:10px;color:#777}.story-v2-base-card b{font-size:12px;font-weight:500}.story-v2-base-card i{width:34px;height:34px;background:#2F4A4A;color:#fff;display:grid;place-items:center;font-style:normal}.story-v2-builder-sizes{max-width:720px}.story-v2-builder-sizes button{min-height:62px;padding:0 16px}.story-v2-builder-addons{display:grid;grid-template-columns:1fr 1fr;gap:18px}.story-v2-addon-card{border:1px solid #ddd}.story-v2-addon-card.selected{border-color:#2F4A4A}.story-v2-addon-media{position:relative;border:0;background:#f2f2ef;padding:0;width:100%;aspect-ratio:1.35/1;cursor:pointer}.story-v2-addon-media img{width:100%;height:100%;object-fit:cover}.story-v2-addon-media span{position:absolute;bottom:10px;right:10px;background:#fff;padding:7px 10px;font-size:8px;letter-spacing:.08em}.story-v2-addon-card.selected .story-v2-addon-media span{background:#2F4A4A;color:#fff}.story-v2-addon-card>div{display:grid;gap:5px;padding:14px}.story-v2-addon-card strong{font-size:12px;font-weight:500}.story-v2-addon-card small{font-size:9px;color:#777}.story-v2-addon-card b{font-size:11px;font-weight:400}.story-v2-qty{height:44px;display:flex;align-items:center;border:1px solid #ccc;width:max-content;margin-top:7px}.story-v2-qty button{width:44px;height:42px;border:0;background:#fff;font-size:15px;cursor:pointer}.story-v2-qty b{width:34px;text-align:center;font-size:10px;font-weight:400}.story-v2-builder-nav{display:flex;align-items:center;justify-content:space-between;gap:15px;padding:16px 30px;border-top:1px solid #ddd;background:#fff}.story-v2-builder-nav>div{display:flex;align-items:center;gap:6px;margin-left:auto}.story-v2-builder-aside{padding:34px 28px;background:#f4f2ed}.story-v2-summary{position:sticky;top:28px;display:grid;gap:13px}.story-v2-summary>p{font-size:8px;letter-spacing:.15em;margin:0;color:#777}.story-v2-summary>div{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-top:13px;border-top:1px solid #ccc}.story-v2-summary span{font-size:10px;color:#666}.story-v2-summary strong{font:400 24px Georgia,serif}.story-v2-summary small{font-size:9px;color:#5f706d}.story-v2-product-row{display:grid;grid-template-columns:76px minmax(0,1fr) auto;gap:14px;align-items:center;padding:13px 0;border-top:1px solid #e1e1de}.story-v2-product-row img{width:76px;height:76px;object-fit:cover}.story-v2-product-copy{display:grid;gap:4px}.story-v2-product-copy strong{font-size:11px;font-weight:500}.story-v2-product-copy span,.story-v2-product-copy small{font-size:9px;color:#777}.story-v2-product-side{display:flex;align-items:center;justify-content:flex-end}.story-v2-product-side>b{font-size:11px;font-weight:400}.story-v2-review{border-bottom:1px solid #e1e1de}.story-v2-occasion-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.story-v2-occasion-grid button{min-height:150px;border:1px solid #ddd;background:#f5f3ee;padding:20px;text-align:left;display:flex;flex-direction:column;justify-content:flex-end;gap:6px;font:inherit;cursor:pointer}.story-v2-occasion-grid button.active{border-color:#2F4A4A;box-shadow:inset 0 0 0 1px #2F4A4A}.story-v2-occasion-grid span{font:400 18px Georgia,serif}.story-v2-occasion-grid small{font-size:9px;color:#777}.story-v2-guests{display:flex;gap:10px;margin-bottom:26px}.story-v2-guests button{width:110px;aspect-ratio:1/1;border:1px solid #ccc;background:#fff;font:inherit;display:grid;place-items:center;align-content:center;gap:5px;cursor:pointer}.story-v2-guests button.active{background:#2F4A4A;color:#fff;border-color:#2F4A4A}.story-v2-guests b{font:400 30px Georgia,serif}.story-v2-guests span{font-size:9px}.story-v2-table-addons{display:grid;grid-template-columns:1fr 1fr;gap:12px}.story-v2-table-addon{min-height:118px;border:1px solid #ddd;background:#fff;padding:10px;display:grid;grid-template-columns:88px 1fr 44px;gap:12px;align-items:center;text-align:left;font:inherit;cursor:pointer}.story-v2-table-addon.selected{border-color:#2F4A4A}.story-v2-table-addon img{width:88px;height:88px;object-fit:cover}.story-v2-table-addon>span{display:grid;gap:5px}.story-v2-table-addon strong{font-size:10px;font-weight:500}.story-v2-table-addon small{font-size:9px;color:#777}.story-v2-table-addon b{font-size:10px;font-weight:400}.story-v2-table-addon i{width:38px;height:38px;border:1px solid #bbb;display:grid;place-items:center;font-style:normal}.story-v2-table-addon.selected i{background:#2F4A4A;color:#fff;border-color:#2F4A4A}
.story-v2-confirm-layer{z-index:180}.story-v2-confirm{position:relative;z-index:2;width:min(560px,94vw);max-height:90vh;overflow:auto;background:#fff;padding:34px;box-shadow:0 25px 80px rgba(0,0,0,.16);text-align:center;animation:storyRise .28s ease both}.story-v2-confirm-mark{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:#2F4A4A;color:#fff;margin:0 auto 18px}.story-v2-confirm>small{font-size:8px;letter-spacing:.16em;color:#777}.story-v2-confirm h2{font:400 32px/1.05 Georgia,serif;margin:8px 0}.story-v2-confirm>p{font-size:11px;color:#777;margin:0 0 24px}.story-v2-confirm-list{text-align:left;border-bottom:1px solid #ddd;margin-bottom:20px}.story-v2-confirm .story-v2-summary{position:static;text-align:left;margin-bottom:22px}.story-v2-confirm>.story-v2-primary{width:100%}
@keyframes storyFade{from{opacity:0}to{opacity:1}}@keyframes storyRise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}@keyframes storyDrawer{from{transform:translateX(100%)}to{transform:none}}
@media(max-width:900px){
  .luna-story-v2-head{padding:44px 20px 34px}.luna-story-v2-list{gap:58px;padding:0 16px 70px}.luna-story-v2-entry,.luna-story-v2-entry.reverse{grid-template-columns:1fr;gap:20px}.luna-story-v2-entry.reverse .luna-story-v2-media,.luna-story-v2-entry.reverse .luna-story-v2-copy{order:initial}.luna-story-v2-media-grid{height:auto;display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:6px;scrollbar-width:none}.luna-story-v2-media-grid::-webkit-scrollbar{display:none}.luna-story-v2-media-grid img,.luna-story-v2-media-grid img:first-child{flex:0 0 88%;height:68svh;max-height:660px;min-height:460px;object-fit:cover;scroll-snap-align:start}.luna-story-v2-copy{gap:12px;padding:0 4px}.luna-story-v2-copy h2{font-size:36px}
  .story-v2-layer{padding:0;background:#fff}.story-v2-landing{width:100%;height:100%;box-shadow:none}.story-v2-landing-head{position:sticky;top:0;z-index:5;background:#fff;padding:16px}.story-v2-landing-head h2{font-size:21px}.story-v2-landing-grid{grid-template-columns:1fr;display:block}.story-v2-landing-gallery{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;padding:0;gap:4px;scrollbar-width:none}.story-v2-landing-gallery::-webkit-scrollbar{display:none}.story-v2-landing-gallery img,.story-v2-landing-gallery img:first-child{flex:0 0 88%;height:54svh;min-height:390px;object-fit:cover;scroll-snap-align:start}.story-v2-landing-info{padding:28px 18px 44px}.story-v2-landing-info>p{font-size:11px;margin-bottom:22px}.story-v2-composition{padding:18px 0}.story-v2-landing-price{padding:20px 0}
  .story-v2-sub-layer,.story-v2-builder-layer{padding:0;align-items:flex-end}.story-v2-sheet{position:relative;width:100%;height:94svh;border-radius:18px 18px 0 0;animation:storySheet .28s ease both}.story-v2-sheet-head{padding:17px 16px}.story-v2-sheet-head h2{font-size:22px}.story-v2-sheet-body{padding:16px 16px 190px}.story-v2-sheet-footer{position:absolute;left:0;right:0;bottom:0;padding:13px 16px calc(14px + env(safe-area-inset-bottom));box-shadow:0 -7px 22px rgba(0,0,0,.05)}.story-v2-quick-title{grid-template-columns:68px 1fr}.story-v2-quick-title img{width:68px;height:68px}
  .story-v2-builder{width:100%;height:100svh;max-height:none;box-shadow:none}.story-v2-builder-layout{grid-template-columns:1fr;min-height:100%}.story-v2-builder-main{border:0;min-height:100svh}.story-v2-builder-head{position:sticky;top:0;z-index:5;background:#fff;padding:14px 16px}.story-v2-builder-head h2{font-size:21px}.story-v2-steps{position:sticky;top:73px;z-index:4;background:#fff}.story-v2-steps button{min-height:55px;gap:4px;flex-direction:column}.story-v2-steps button b{width:20px;height:20px}.story-v2-steps button span{font-size:7px}.story-v2-step-content{padding:24px 16px 180px;overflow:visible}.story-v2-step-title h3{font-size:30px}.story-v2-base-card{grid-template-columns:110px 1fr 34px;gap:14px;padding:9px}.story-v2-base-card img{width:110px}.story-v2-base-card strong{font-size:17px}.story-v2-builder-addons,.story-v2-table-addons{grid-template-columns:1fr}.story-v2-addon-media{aspect-ratio:1.45/1}.story-v2-builder-nav{position:fixed;left:0;right:0;bottom:0;z-index:7;padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:grid;grid-template-columns:auto 1fr;background:#fff;box-shadow:0 -8px 24px rgba(0,0,0,.06)}.story-v2-builder-nav>div{display:grid;grid-template-columns:auto 1fr;width:100%}.story-v2-builder-nav .story-v2-primary.compact{min-width:0;width:100%}.story-v2-builder-aside{position:fixed;left:0;right:0;bottom:70px;z-index:6;padding:9px 16px;background:#f4f2ed}.story-v2-builder-aside .story-v2-summary{position:static;display:grid;grid-template-columns:1fr auto;gap:5px}.story-v2-builder-aside .story-v2-summary>p{display:none}.story-v2-builder-aside .story-v2-summary>div{grid-column:1/3;padding:0;border:0}.story-v2-builder-aside .story-v2-summary small{grid-column:1/3}.story-v2-occasion-grid{grid-template-columns:1fr}.story-v2-occasion-grid button{min-height:110px}.story-v2-guests button{width:31%;max-width:120px}.story-v2-product-row{grid-template-columns:62px minmax(0,1fr) auto;gap:10px}.story-v2-product-row img{width:62px;height:62px}.story-v2-table-addon{grid-template-columns:74px 1fr 44px}.story-v2-table-addon img{width:74px;height:74px}.story-v2-confirm{width:100%;max-height:94svh;border-radius:18px 18px 0 0;padding:26px 16px calc(18px + env(safe-area-inset-bottom))}
}
@media(max-width:520px){.luna-story-v2-head h1{font-size:43px}.luna-story-v2-media-grid img,.luna-story-v2-media-grid img:first-child{height:58svh;min-height:430px}.story-v2-landing-gallery img,.story-v2-landing-gallery img:first-child{flex-basis:92%;height:48svh}.story-v2-sheet-body{padding-bottom:205px}.story-v2-builder-sizes button{min-height:58px}.story-v2-base-card{grid-template-columns:94px 1fr 30px}.story-v2-base-card img{width:94px}.story-v2-addon-card>div{padding:12px}.story-v2-ready strong{font-size:16px}}
@keyframes storySheet{from{transform:translateY(100%)}to{transform:none}}
/* END_STORY_BUILDER_V2 */
'''
css_path.write_text(css,encoding="utf-8")
print("Applied adaptive story quick-buy and builder v2")
