from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
root_layout_path = root / "app" / "layout.tsx"
ready_layout_path = root / "app" / "ready-solutions" / "layout.tsx"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"V66 anchor not found: {label}")
    return text.replace(old, new, 1)


# --- Collections: materialize one continuous editorial + commerce page. ---
page = page_path.read_text(encoding="utf-8")
if "COLLECTIONS_ZARA_KULTURA_V66" not in page:
    start = page.index("function CollectionsView(")
    end = page.index("\nfunction EditorialView(", start)
    collections_view = r'''// COLLECTIONS_ZARA_KULTURA_V66
function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle,initialEditorial }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void; initialEditorial?:Editorial }) {
  const [active,setActive]=useState<Editorial|null>(initialEditorial??null);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});

  useEffect(()=>{
    if(initialEditorial){
      setActive(initialEditorial);
      setSelectedIds([]);
      setSizes({});
      setVariants({});
    }
  },[initialEditorial?.id]);

  useEffect(()=>{
    if(!active)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[active]);

  const collectionPrice=(editorial:Editorial)=>{
    const values=editorial.productIds.map(id=>products.find(item=>item.id===id)?.price||0).filter(Boolean);
    return values.length?Math.min(...values):0;
  };
  const items=useMemo(()=>active?active.productIds.map(id=>products.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)):[],[active]);
  const open=(editorial:Editorial)=>{setActive(editorial);setSelectedIds([]);setSizes({});setVariants({})};
  const close=()=>{setActive(null);setSelectedIds([]);setSizes({});setVariants({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const currentProduct=(item:Product)=>variants[item.id]??item;
  const colorOf=(item:Product)=>{const current=currentProduct(item);return current.selectedColor??current.colorVariants?.[0]?.name??current.skus?.[0]?.color??""};
  const sizeOptions=(item:Product)=>getProductSizeOptions(currentProduct(item),colorOf(item));
  const pending=selectedIds.filter(id=>{
    const item=items.find(product=>product.id===id);
    if(!item)return false;
    return sizeOptions(item).length>1&&!sizes[id];
  });
  const selectedProducts=selectedIds.map(id=>items.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)).map(item=>{
    const current=currentProduct(item);
    const color=colorOf(item);
    const options=sizeOptions(item);
    const selectedSize=sizes[item.id]??(options.length===1?options[0][0]:"");
    const sku=selectedSize?findProductSku(current,color,selectedSize):findProductSku(current,color);
    return {...current,selectedColor:color,selectedSize:selectedSize||sku?.size||"",selectedSkuId:sku?.id,price:sku?.price??current.price};
  });
  const total=selectedProducts.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;
  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};
  const readySolutionCollection=active?({"Эхо":"Камея","Нити":"Нити времени","Феникс":"Жар-птица"} as Record<string,string>)[active.name]||active.name:"";
  const readySolutionHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/?collection=${encodeURIComponent(readySolutionCollection)}`;

  return <main className="collections-v52 collections-v66-zara">
    <header className="collections-v52-intro">
      <div><small>КУЛЬТУРА ДОМА · КОЛЛЕКЦИИ</small><h1>Коллекции</h1></div>
      <p>Дом складывается из историй. Каждая коллекция объединяет цвет, орнамент и предметы так, чтобы их можно было прожить вместе — или выбрать только один акцент.</p>
    </header>
    <section className="collections-v52-index" aria-label="Коллекции Культура Дома">
      {editorials.map(editorial=><article className="collections-v52-card" key={editorial.id}>
        <button className="collections-v52-card-media" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v52-card-copy"><small>КОЛЛЕКЦИЯ</small><button type="button" onClick={()=>open(editorial)}><h2>{editorial.name}</h2></button><p>{editorial.lead}</p><div><span>{productCountLabel(editorial.productIds.length)}</span><strong>{collectionPrice(editorial)?`от ${fmt(collectionPrice(editorial))}`:""}</strong></div></div>
      </article>)}
    </section>

    {active&&<div className="v52-story-backdrop" role="presentation"><button className="v52-story-dismiss" type="button" onClick={close} aria-label="Закрыть коллекцию"/>
      <section className="v52-story-modal" role="dialog" aria-modal="true" aria-label={`Коллекция ${active.name}`}>
        <header className="v52-story-topbar"><button type="button" onClick={close}>← Коллекции</button><strong>КУЛЬТУРА ДОМА</strong><button type="button" onClick={close} aria-label="Закрыть">×</button></header>
        <div className="v52-story-columns">
          <aside className="v52-story-editorial" aria-label="История коллекции">
            <div className="v52-story-title"><small>КОЛЛЕКЦИЯ</small><h1>{active.name}</h1><p>{active.lead}</p><span>{productCountLabel(items.length)}</span></div>
            {active.images.map((image,index)=><figure key={`${active.id}-${image}`}><img src={assetUrl(image)} alt={`${active.name}, кадр ${index+1}`}/>{index===0&&<figcaption>{active.detail}</figcaption>}</figure>)}
            <div className="v52-story-note"><small>ИСТОРИЯ КОЛЛЕКЦИИ</small><p>{active.description}</p><a className="v52-buy-story v58-ready-solution-link" href={readySolutionHref}>СОБРАТЬ ГОТОВОЕ РЕШЕНИЕ →</a></div>
          </aside>
          <section className="v52-story-commerce" aria-label="Товары коллекции">
            <header className="v52-commerce-head"><div><small>ТОВАРЫ КОЛЛЕКЦИИ</small><h2>Предметы коллекции</h2><p>Выберите нужные позиции. Если у предмета несколько размеров, размер появится после выбора.</p></div><div className="v65-commerce-actions"><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всё"}</button></div></header>
            <div className="product-grid v52-story-products is-selection-mode">{items.map(item=>{const current=currentProduct(item);const selected=selectedIds.includes(item.id);const options=sizeOptions(item);const needsSize=selected&&options.length>1&&!sizes[item.id];return <div className={`v52-story-product ${selected?"selected":""}`} key={item.id}><ProductCard product={current} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={true} selected={selected} pending={needsSize} onSelect={()=>toggle(item.id)} onVariantChange={product=>{setVariants(state=>({...state,[item.id]:product}));setSizes(state=>{const next={...state};delete next[item.id];return next})}}/>{selected&&options.length>1&&<label className="v52-inline-size"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(state=>({...state,[item.id]:event.target.value}))}><option value="">Выбрать</option>{options.map(([name])=><option key={name} value={name}>{name}</option>)}</select></label>}</div>})}</div>
            <footer className="v52-purchase-bar"><div><span>{pending.length?`Выберите размер · ${pending.length}`:selectedProducts.length?`Выбрано ${selectedProducts.length} из ${items.length}`:"Выберите товары"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>КУПИТЬ</button></footer>
          </section>
        </div>
      </section>
    </div>}
  </main>;
}
'''
    page = page[:start] + collections_view + page[end:]
    page_path.write_text(page, encoding="utf-8")
    print("Collections V66 markup applied")
else:
    print("Collections V66 already applied")


# --- Ready Solutions: keep the configurator logic, change its visible hierarchy. ---
ready = ready_path.read_text(encoding="utf-8")
if "EDITORIAL_COMMERCE_V66" not in ready:
    ready = replace_once(
        ready,
        "// READY_SOLUTIONS_PREMIUM_FILTERS_V62\n// READY_SOLUTIONS_LARGE_STEPS_V63\nexport function ReadySolutionsLanding()",
        "// READY_SOLUTIONS_PREMIUM_FILTERS_V62\n// READY_SOLUTIONS_LARGE_STEPS_V63\n// EDITORIAL_COMMERCE_V66\nexport function ReadySolutionsLanding()",
        "ready solutions marker",
    )
    ready = replace_once(
        ready,
        'return <div className="rs57-page">\n    <StoreHeader/>\n    <main className="rs57-landing">',
        'return <div className="rs57-page rs66-zara">\n    <StoreHeader/>\n    <main className="rs57-landing">',
        "landing root",
    )
    ready = replace_once(
        ready,
        '<div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h1>Готовые решения для дома</h1><p>Выберите пространство и адаптируйте готовую композицию под себя.</p></div>',
        '<div><small>КУЛЬТУРА ДОМА · ГОТОВЫЕ РЕШЕНИЯ</small><h1>Готовые решения</h1><p>Цельные композиции для спальни, стола и дома. Выберите близкий образ, затем измените только те предметы, которые нужны именно вам.</p></div>',
        "landing intro",
    )
    ready = replace_once(
        ready,
        '<header className="rs57-index-head"><div><small>ПОДБОР</small><h2 id="rs57-index-title">Найдите своё решение</h2></div><span>{visible.length} из {cards.length}</span></header>',
        '<header className="rs57-index-head"><div><small>ПРОСТРАНСТВА</small><h2 id="rs57-index-title">Композиции для дома</h2></div><span>{visible.length} из {cards.length}</span></header>',
        "landing index title",
    )
    ready = replace_once(ready, 'НАСТРОИТЬ РЕШЕНИЕ <Icon name="arrow"/>', 'СМОТРЕТЬ РЕШЕНИЕ <Icon name="arrow"/>', "landing card CTA")
    ready = replace_once(
        ready,
        'return <div className="rs57-page rs57-wizard-page">',
        'return <div className="rs57-page rs57-wizard-page rs66-zara">',
        "wizard root",
    )
    ready = replace_once(
        ready,
        '<div className="rs57-wizard-hero-copy"><small>{solution.space}</small><h1>{solution.name}</h1><p>Выберите основу и настройте её под своё пространство.</p>',
        '<div className="rs57-wizard-hero-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция Культура Дома. Сохраните её целиком или измените состав, цвет и количество под своё пространство.</p>',
        "wizard hero copy",
    )
    ready = replace_once(
        ready,
        '<em>{value === 1 ? "Параметры" : value === 2 ? "Состав" : "Результат"}</em>',
        '<em>{value === 1 ? "Параметры" : value === 2 ? "Состав" : "Образ"}</em>',
        "stepper labels",
    )
    ready = ready.replace('<small>ШАГ 1 ИЗ 3</small><h2>Параметры</h2>', '<small>НАСТРОЙКА РЕШЕНИЯ</small><h2>Параметры</h2>', 1)
    ready = ready.replace('<small>ШАГ 2 ИЗ 3</small><h2>{replaceOptionId ? "Выберите замену" : "Состав решения"}</h2>', '<small>СОСТАВ РЕШЕНИЯ</small><h2>{replaceOptionId ? "Выберите замену" : "Предметы решения"}</h2>', 1)
    ready = ready.replace('<div><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2>', '<div><small>ГОТОВЫЙ ОБРАЗ</small><h2>Ваше решение</h2>', 1)
    ready = replace_once(ready, 'ДОБАВИТЬ ВСЁ В КОРЗИНУ', 'КУПИТЬ РЕШЕНИЕ', "result CTA")
    ready = ready.replace('>В КОРЗИНУ</button>', '>КУПИТЬ</button>', 1)
    ready_path.write_text(ready, encoding="utf-8")
    print("Ready Solutions V66 markup applied")
else:
    print("Ready Solutions V66 already applied")


# Keep the V66 styles last in cascade even when this migration runs on an older source snapshot.
root_layout = root_layout_path.read_text(encoding="utf-8")
if 'import "./collections-zara-kultura-v66.css";' not in root_layout:
    root_layout = root_layout.replace('import "./collections-v65.css";\n', 'import "./collections-v65.css";\nimport "./collections-zara-kultura-v66.css";\n', 1)
    root_layout_path.write_text(root_layout, encoding="utf-8")

ready_layout = ready_layout_path.read_text(encoding="utf-8")
if 'import "./ready-solutions-zara-kultura-v66.css";' not in ready_layout:
    ready_layout = ready_layout.replace('import "./ready-solutions-v64.css";\n', 'import "./ready-solutions-v64.css";\nimport "./ready-solutions-zara-kultura-v66.css";\n', 1)
    ready_layout_path.write_text(ready_layout, encoding="utf-8")

print("Editorial commerce V66 complete")
