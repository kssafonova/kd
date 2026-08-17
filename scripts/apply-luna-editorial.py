from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

# Add the Luna capsule to the shared editorial catalogue. The six referenced
# images live under public/images/editorial; RemoteImage fallbacks keep the
# page usable while assets are being uploaded/replaced.
luna_entry = '''  { id:"luna", name:"Лунная сказка", kind:"КАПСУЛА", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Интерактивный editorial о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png","/images/editorial/caps_luna_serviz2.png","/images/editorial/caps_luna_serviz3.png"], productIds:[4,10,5,6,3] },\n'''
editorial_marker = 'const editorials:Editorial[] = [\n'
if 'id:"luna"' not in text:
    if editorial_marker not in text:
        raise SystemExit("Editorial catalogue marker not found")
    text = text.replace(editorial_marker, editorial_marker + luna_entry, 1)

# Give the editorial view access to the real cart action so Luna can be shopped
# directly from imagery instead of forcing a PDP hop.
old_render = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}'
new_render = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} add={(product)=>add(product,product.selectedSize,product.quantity)} />}'
if old_render in text:
    text = text.replace(old_render, new_render, 1)
elif new_render not in text:
    raise SystemExit("EditorialView render marker not found")

luna_component = r'''function LunaEditorialView({ editorial, selectProduct, favorite, favorites, add }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; add:(product:Product)=>void }) {
  const [activeScene,setActiveScene]=useState<string|null>(null);
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [selectedSizes,setSelectedSizes]=useState<Record<number,string>>({});

  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={
    4:"/images/products/KD-PD-1024-DARK02.png",
    6:"/images/products/KD-PD-1026-BLUE01.png",
    3:"/images/products/KD-PD-1023-BLUE02.png",
  };
  const sceneFallbacks=["/images/time-hero.png","/images/blue-bedroom.png","/images/night-editorial.png","/images/time-table.png","/images/time-tea-pair.png","/images/moon-plate.png"];
  const lunaItems=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);

  const prepareProduct=(product:Product)=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const sizeOptions=getProductSizeOptions(product,color);
    const chosenSize=selectedSizes[product.id]??sizeOptions[0]?.[0]??product.selectedSize??"";
    const sku=findProductSku(product,color,chosenSize);
    return {
      ...product,
      image:previewById[product.id]??sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      selectedColor:sku?.color??color,
      selectedSize:sku?.size??chosenSize,
      selectedSkuId:sku?.id,
      price:sku?.price??product.price,
      quantity:1,
    };
  };

  const preparedItems=lunaItems.map(prepareProduct);
  const itemById=(id:number)=>preparedItems.find(item=>item.id===id);
  const scenes=[
    {id:"bed-1",image:editorial.images[0],fallback:sceneFallbacks[0],kicker:"01 / BEDROOM",title:"Ночь начинается с тактильности",copy:"Сатин, глубокий синий и мягкое кружево собирают спальню в единый спокойный образ.",productIds:[4,6,3]},
    {id:"bed-2",image:editorial.images[1],fallback:sceneFallbacks[1],kicker:"02 / TEXTURE",title:"Слои света и ткани",copy:"Постельное бельё становится фоном, а плед и подушка — акцентами, которые можно менять независимо.",productIds:[4,3]},
    {id:"bed-3",image:editorial.images[2],fallback:sceneFallbacks[2],kicker:"03 / QUIET DETAIL",title:"Тихая архитектура спальни",copy:"Один цвет, разные фактуры: сатин отражает свет, хлопок и кружево делают композицию мягче.",productIds:[4,6,3]},
    {id:"table-1",image:editorial.images[3],fallback:sceneFallbacks[3],kicker:"04 / TABLE",title:"Поздний чай как маленький ритуал",copy:"Кобальтовая сервировка продолжает палитру спальни и связывает предметы капсулы между собой.",productIds:[10,5]},
    {id:"table-2",image:editorial.images[4],fallback:sceneFallbacks[4],kicker:"05 / PORCELAIN",title:"Фарфор цвета ночного неба",copy:"Чайная пара и тарелка работают вместе, но каждый предмет можно купить отдельно.",productIds:[10,5]},
    {id:"table-3",image:editorial.images[5],fallback:sceneFallbacks[5],kicker:"06 / AFTER DARK",title:"Дом после заката",copy:"Финальный кадр соединяет спальню и стол: один визуальный язык, несколько самостоятельных сценариев покупки.",productIds:[10,5,3]},
  ];
  const currentScene=scenes.find(scene=>scene.id===activeScene);
  const currentProducts=currentScene?.productIds.map(itemById).filter((item):item is Product=>Boolean(item))??[];

  const toggleSelected=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const addSelectedSet=()=>selectedIds.forEach(id=>{const item=itemById(id);if(item)add(item)});
  const setSize=(id:number,size:string)=>setSelectedSizes(current=>({...current,[id]:size}));

  return <div className="luna-editorial-page">
    <section className="luna-hero" onClick={()=>setActiveScene("bed-1")} role="button" tabIndex={0} onKeyDown={event=>{if(event.key==="Enter"||event.key===" ")setActiveScene("bed-1")}} aria-label="Открыть товары из первого образа">
      <RemoteImage src={editorial.images[0]} fallbackSrc={sceneFallbacks[0]} alt="Капсула Лунная сказка — спальня"/>
      <div className="luna-hero-shade"/>
      <div className="luna-hero-index">CAPSULE / 2026</div>
      <div className="luna-hero-copy"><p>EDITORIAL · ЛУННАЯ СКАЗКА</p><h1>Лунная<br/>сказка</h1><span>{editorial.lead}</span><button type="button" onClick={event=>{event.stopPropagation();document.getElementById("luna-story")?.scrollIntoView({behavior:"smooth"})}}>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></button></div>
      <button className="luna-shop-look" type="button" onClick={event=>{event.stopPropagation();setActiveScene("bed-1")}}><i>+</i><span>SHOP THE LOOK</span></button>
    </section>

    <section className="luna-intro" id="luna-story">
      <span>КУЛЬТУРА ДОМА / CAPSULE 05</span>
      <h2>Ночная история<br/>для современного дома</h2>
      <p>{editorial.detail}</p>
    </section>

    <section className="luna-scenes luna-bedroom-scenes">
      {scenes.slice(0,3).map((scene,index)=><button type="button" key={scene.id} className={`luna-scene-card luna-scene-${index+1}`} onClick={()=>setActiveScene(scene.id)}>
        <RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/>
        <span className="luna-scene-overlay"><small>{scene.kicker}</small><strong>{scene.title}</strong><i>СМОТРЕТЬ ТОВАРЫ +</i></span>
      </button>)}
    </section>

    <section className="luna-text-banner">
      <span>MOONLIGHT / TEXTURE / SILENCE</span>
      <h2>В этой капсуле нет одного «правильного» комплекта.</h2>
      <p>Соберите свою комбинацию: постельное бельё, плед и подушка могут жить вместе или по отдельности.</p>
    </section>

    <section className="luna-generated-banner luna-generated-banner-bed">
      <div className="luna-generated-main"><RemoteImage src={editorial.images[1]} fallbackSrc={sceneFallbacks[1]} alt="Лунная сказка — спальня"/></div>
      <div className="luna-generated-detail"><RemoteImage src={previewById[3]} alt="Подушка с кружевом синяя"/><span>DETAIL / LACE</span></div>
      <div className="luna-generated-copy"><small>03 / MATERIAL STUDY</small><h3>Глубокий синий<br/>без лишней декоративности</h3><p>Главный визуальный приём — один тон и контраст фактур.</p></div>
    </section>

    <section className="luna-scenes luna-table-scenes">
      {scenes.slice(3).map((scene,index)=><button type="button" key={scene.id} className={`luna-scene-card luna-table-${index+1}`} onClick={()=>setActiveScene(scene.id)}>
        <RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/>
        <span className="luna-scene-overlay"><small>{scene.kicker}</small><strong>{scene.title}</strong><i>SHOP THE TABLE +</i></span>
      </button>)}
    </section>

    <section className="luna-generated-banner luna-generated-banner-table">
      <div className="luna-generated-copy"><small>05 / THE TABLE</small><h3>Сервировка<br/>как продолжение интерьера</h3><p>Фарфор повторяет палитру текстиля и превращает разные категории в одну визуальную систему.</p></div>
      <div className="luna-generated-main"><RemoteImage src={editorial.images[4]} fallbackSrc={sceneFallbacks[4]} alt="Лунная сказка — сервировка"/></div>
      <div className="luna-generated-detail luna-plate-detail"><RemoteImage src="/images/moon-plate.png" alt="Тарелка Лунная сказка"/><span>PORCELAIN / NIGHT BLUE</span></div>
    </section>

    <section className="luna-set-builder">
      <header><div><span>BUILD YOUR CAPSULE</span><h2>Соберите свой комплект</h2></div><p>Выберите только те части, которые нужны вам. Размер текстиля можно изменить до добавления в корзину.</p></header>
      <div className="luna-builder-grid">{preparedItems.map(item=>{
        const checked=selectedIds.includes(item.id);
        const color=colorById[item.id]??item.selectedColor;
        const sizes=getProductSizeOptions(item,color);
        const selectedSize=selectedSizes[item.id]??sizes[0]?.[0]??item.selectedSize??"";
        const selectedSku=findProductSku(item,color,selectedSize);
        const price=selectedSku?.price??item.price;
        return <article className={`luna-builder-card ${checked?"selected":""}`} key={item.id}>
          <button className="luna-builder-image" type="button" onClick={()=>selectProduct(prepareProduct(item))}><RemoteImage src={previewById[item.id]??item.image} alt={item.name}/></button>
          <button className="luna-builder-check" type="button" onClick={()=>toggleSelected(item.id)} aria-pressed={checked}><i>{checked?"✓":""}</i><span>{checked?"В КОМПЛЕКТЕ":"ДОБАВИТЬ В КОМПЛЕКТ"}</span></button>
          <div className="luna-builder-copy"><small>{item.article??`KD-PD-${1020+item.id}`}</small><h3>{item.name}</h3><p>{color}</p>{sizes.length>1&&<label>Размер<select value={selectedSize} onChange={event=>setSize(item.id,event.target.value)}>{sizes.map(([size])=><option key={size} value={size}>{size}</option>)}</select></label>}<strong>{fmt(price)}</strong><div><button type="button" onClick={()=>selectProduct(prepareProduct(item))}>ПОДРОБНЕЕ</button><button type="button" className="luna-card-add" onClick={()=>add(prepareProduct(item))}>В КОРЗИНУ</button></div></div>
          <button className={`luna-builder-heart ${favorites.includes(item.id)?"active":""}`} type="button" onClick={()=>favorite(item.id)} aria-label="Добавить в избранное"><Icon name="heart" filled={favorites.includes(item.id)}/></button>
        </article>})}</div>
      <div className="luna-builder-total"><div><span>ВЫБРАНО · {selectedIds.length}</span><strong>{fmt(selectedIds.reduce((sum,id)=>{const item=itemById(id);if(!item)return sum;const color=colorById[id]??item.selectedColor;const size=selectedSizes[id]??getProductSizeOptions(item,color)[0]?.[0]??item.selectedSize;return sum+(findProductSku(item,color,size)?.price??item.price)},0))}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addSelectedSet}>ДОБАВИТЬ ВЕСЬ КОМПЛЕКТ В КОРЗИНУ <Icon name="arrow"/></button></div>
    </section>

    <section className="luna-finale" onClick={()=>setActiveScene("table-3")} role="button" tabIndex={0} onKeyDown={event=>{if(event.key==="Enter"||event.key===" ")setActiveScene("table-3")}}>
      <RemoteImage src={editorial.images[5]} fallbackSrc={sceneFallbacks[5]} alt="Лунная сказка — финальный editorial кадр"/>
      <div><span>06 / FINALE</span><h2>Дом, который<br/>просыпается ночью</h2><button type="button" onClick={event=>{event.stopPropagation();setActiveScene("table-3")}}>SHOP THE STORY +</button></div>
    </section>

    {currentScene&&<div className="luna-shop-overlay" role="dialog" aria-modal="true" aria-label={`Товары из образа ${currentScene.title}`}>
      <button className="luna-shop-backdrop" type="button" onClick={()=>setActiveScene(null)} aria-label="Закрыть товары"/>
      <aside className="luna-shop-drawer"><header><div><small>{currentScene.kicker}</small><h2>{currentScene.title}</h2><p>{currentScene.copy}</p></div><button type="button" onClick={()=>setActiveScene(null)} aria-label="Закрыть"><Icon name="close"/></button></header><div className="luna-shop-products">{currentProducts.map(item=>{
        const color=colorById[item.id]??item.selectedColor;
        const sizes=getProductSizeOptions(item,color);
        const selectedSize=selectedSizes[item.id]??sizes[0]?.[0]??item.selectedSize??"";
        const sku=findProductSku(item,color,selectedSize);
        return <article key={item.id}><button type="button" className="luna-shop-product-image" onClick={()=>{setActiveScene(null);selectProduct(prepareProduct(item))}}><RemoteImage src={previewById[item.id]??item.image} alt={item.name}/></button><div><small>{item.article}</small><h3>{item.name}</h3><span>{color}</span>{sizes.length>1&&<select value={selectedSize} onChange={event=>setSize(item.id,event.target.value)}>{sizes.map(([size])=><option key={size} value={size}>{size}</option>)}</select>}<strong>{fmt(sku?.price??item.price)}</strong><button type="button" onClick={()=>add(prepareProduct(item))}>ДОБАВИТЬ В КОРЗИНУ</button></div></article>})}</div></aside>
    </div>}
  </div>;
}
'''

if 'function LunaEditorialView(' not in text:
    marker = 'function EditorialView('
    if marker not in text:
        raise SystemExit("EditorialView function marker not found")
    text = text.replace(marker, luna_component + '\n\n' + marker, 1)

old_signature = 'function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {\n  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);'
new_signature = 'function EditorialView({ editorial, selectProduct, favorite, favorites, add }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; add:(product:Product)=>void }) {\n  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} add={add}/>;\n  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);'
if old_signature in text:
    text = text.replace(old_signature, new_signature, 1)
elif new_signature not in text:
    raise SystemExit("EditorialView signature marker not found")

path.write_text(text, encoding="utf-8")
print("Applied Luna interactive editorial capsule")
