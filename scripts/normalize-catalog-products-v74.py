from pathlib import Path
import csv

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
builder_path = root / "app" / "constructor" / "table-solution-builder.ts"
ready_client_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
globals_path = root / "app" / "globals.css"
ready_css_path = root / "app" / "ready-solutions" / "ready-solutions-v71.css"
catalog_path = root / "public" / "data" / "kultura_doma_full_constructor_eligible_catalog.csv"

MARKER = "// CATALOG_PRODUCT_NORMALIZATION_V74"
REMOVED_IDS = {
    1257, 1259, 1260, 1261, 1262, 1263, 1266, 1267,
    1268, 1270, 1271, 1273, 1276, 1287, 1565, 1566, 1669,
}


def patch_page() -> None:
    page = page_path.read_text(encoding="utf-8")
    if MARKER in page:
        return

    helper_anchor = "const priceKnown=(value:number)=>Number.isFinite(value)&&value>0;\n"
    helper = helper_anchor + MARKER + "\nconst isAromaProduct=(product:Product)=>product.id===1499||product.article===\"KD-PD-2519\"||String(product.name||\"\").trim().toLocaleLowerCase(\"ru-RU\")===\"свеча феникс\";\n"
    if helper_anchor not in page:
        raise RuntimeError("V74 price helper anchor not found")
    page = page.replace(helper_anchor, helper, 1)

    # Remove the requested catalogue products from the actual shared product source.
    lines = page.splitlines(keepends=True)
    next_lines = []
    merged_written = False
    for line in lines:
        stripped = line.lstrip()
        removed = False
        for product_id in REMOVED_IDS:
            if stripped.startswith(f"{{id:{product_id},"):
                removed = True
                break
        if removed:
            continue
        if stripped.startswith("{id:1499,"):
            if not merged_written:
                next_lines.append(
                    '  {id:1499,article:"KD-PD-2519",name:"Свеча Феникс",note:"кокосовый воск, 10 см",price:4990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg",selectedColor:"Дерево жизни",selectedSize:"10 см",colorVariants:[{name:"Дерево жизни",hex:"#5f5143",image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg",gallery:["https://kultura-doma.ru/public/src/images/gallery/catalog/69ca6e5c7afbf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6978bca98d11e_big.jpg"]},{name:"Сандал и Шалфей",hex:"#8a806c",image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg",gallery:["https://kultura-doma.ru/public/src/images/gallery/catalog/69ca6e73dc686_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc91dddf6_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa3a6f1_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa56bea_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa6c634_big.jpg"]}],skus:[{...makeCollectionEditorialSku(1499,"KD-PD-2519","Феникс","Дерево жизни","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69ca6e5c7afbf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6978bca98d11e_big.jpg"]),id:"COL-1499-DEREVO",details:"Аромат: Дерево жизни"},{...makeCollectionEditorialSku(1499,"KD-PD-2520","Феникс","Сандал и Шалфей","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69ca6e73dc686_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc91dddf6_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa3a6f1_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa56bea_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a58dffa6c634_big.jpg"]),id:"COL-1499-SANDAL",details:"Аромат: Сандал и Шалфей"}]},\n'
                )
                merged_written = True
            continue
        if stripped.startswith("{id:1500,"):
            continue
        next_lines.append(line)
    page = "".join(next_lines)

    old_removed = "const REMOVED_PRODUCT_IDS = new Set([1,9]);"
    removed_values = ",".join(str(value) for value in sorted(REMOVED_IDS | {1500}))
    new_removed = f"const REMOVED_PRODUCT_IDS = new Set([1,9,{removed_values}]);"
    if old_removed not in page:
        raise RuntimeError("V74 removed products set anchor not found")
    page = page.replace(old_removed, new_removed, 1)

    old_push = "products.push(...collectionEditorialProducts.filter(item=>!isRetiredCatalogProduct(item.name)&&!products.some(existing=>existing.id===item.id)));"
    new_push = "products.push(...collectionEditorialProducts.filter(item=>!REMOVED_PRODUCT_IDS.has(item.id)&&!isRetiredCatalogProduct(item.name)&&!products.some(existing=>existing.id===item.id)));"
    if old_push not in page:
        raise RuntimeError("V74 collection push anchor not found")
    page = page.replace(old_push, new_push, 1)

    old_collection_ids = 'const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);'
    new_collection_ids = 'const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>!REMOVED_PRODUCT_IDS.has(item.id)&&item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);'
    if old_collection_ids not in page:
        raise RuntimeError("V74 collection product ids anchor not found")
    page = page.replace(old_collection_ids, new_collection_ids, 1)

    category_anchor = '    "Столовый текстиль":[],\n'
    if category_anchor not in page:
        raise RuntimeError("V74 catalog category anchor not found")
    page = page.replace(category_anchor, category_anchor + '    "Декор для дома":[1499],\n', 1)

    tabs_old = '["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Домашняя одежда","Столовый текстиль"]'
    tabs_new = '["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Декор для дома","Домашняя одежда","Столовый текстиль"]'
    if tabs_old not in page:
        raise RuntimeError("V74 catalog tabs anchor not found")
    page = page.replace(tabs_old, tabs_new, 1)

    # Product cards: aroma is a product variant, not a colour swatch.
    plp_anchor = '{variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>chooseVariant(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}'
    plp_new = '{isAromaProduct(product)&&variants.length>1&&<div className="plp-aroma-options" role="group" aria-label={`Аромат товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} onClick={()=>chooseVariant(i)} aria-label={`Выбрать аромат ${variant.name}`}>{variant.name}</button>)}</div>}{!isAromaProduct(product)&&variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>chooseVariant(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}'
    if plp_anchor not in page:
        raise RuntimeError("V74 PLP aroma anchor not found")
    page = page.replace(plp_anchor, plp_new, 1)

    pdp_anchor = '<label className="pdp-color-label">Цвет: {color.name}</label>{variants.length>1&&<div className="swatches product-swatches">'
    pdp_new = '<label className="pdp-color-label">{isAromaProduct(product)?"Аромат":"Цвет"}: {color.name}</label>{isAromaProduct(product)&&variants.length>1&&<div className="pdp-aroma-options">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}}>{variant.name}</button>)}</div>}{!isAromaProduct(product)&&variants.length>1&&<div className="swatches product-swatches">'
    if pdp_anchor not in page:
        raise RuntimeError("V74 PDP aroma anchor not found")
    page = page.replace(pdp_anchor, pdp_new, 1)

    page = page.replace(
        '<p className="quick-color">Цвет: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>',
        '<p className="quick-color">{isAromaProduct(product)?"Аромат":"Цвет"}: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>',
        1,
    )
    page = page.replace(
        '<span>Цвет: {item.selectedColor}</span><span>Размер: {item.selectedSize}</span>',
        '<span>{isAromaProduct(item)?"Аромат":"Цвет"}: {item.selectedColor}</span><span>Размер: {item.selectedSize}</span>',
        1,
    )
    page = page.replace(
        '<small className="pdp-code">АРТИКУЛ: {product.article??`KD-PD-${1020+product.id}`}</small>',
        '<small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}</small>',
        1,
    )

    page_path.write_text(page, encoding="utf-8")


def patch_ready_solution_builder() -> None:
    text = builder_path.read_text(encoding="utf-8")
    marker = "// PHOENIX_CANDLE_DECOR_V74"
    if marker in text:
        return
    anchor = '  if (hasAny(name, ["свеч", "диффузор", "аромат для дома", "аромадиффузор", "подсвечник"]) || hasAny(type, ["candle", "candle_holder", "diffuser"])) {\n'
    insert = '  // PHOENIX_CANDLE_DECOR_V74\n  if (name === normalize("Свеча Феникс")) return { id: "other", perPerson: false };\n\n' + anchor
    if anchor not in text:
        raise RuntimeError("V74 builder candle anchor not found")
    text = text.replace(anchor, insert, 1)
    builder_path.write_text(text, encoding="utf-8")


def patch_ready_solution_ui() -> None:
    text = ready_client_path.read_text(encoding="utf-8")
    marker = "// READY_AROMA_VARIANT_V74"
    if marker in text:
        return
    row_anchor = '  const colors=optionColors(option), sizes=optionSizes(option,color), row=pickOptionVariant(option,color,size), image=rowImages(row)[0]||"/images/image-placeholder.svg";\n'
    row_new = row_anchor + '  // READY_AROMA_VARIANT_V74\n  const aromaVariant=norm(displayProductName(option.title))===norm("Свеча Феникс");\n'
    if row_anchor not in text:
        raise RuntimeError("V74 ready ProductCard anchor not found")
    text = text.replace(row_anchor, row_new, 1)

    swatch_anchor = '{colors.length>1&&<div className="rs71-swatches">{colors.map((value)=><button type="button" key={value} title={value} className={(color||row?.color)===value?"is-active":""} style={{background:swatchColor(value)}} onClick={()=>onColor(value)}/>)}</div>}'
    swatch_new = '{colors.length>1&&(aromaVariant?<div className="rs71-aroma-options"><small>Аромат</small>{colors.map((value)=><button type="button" key={value} className={(color||row?.color)===value?"is-active":""} onClick={()=>onColor(value)}>{value}</button>)}</div>:<div className="rs71-swatches">{colors.map((value)=><button type="button" key={value} title={value} className={(color||row?.color)===value?"is-active":""} style={{background:swatchColor(value)}} onClick={()=>onColor(value)}/>)}</div>)}'
    if swatch_anchor not in text:
        raise RuntimeError("V74 ready aroma swatch anchor not found")
    text = text.replace(swatch_anchor, swatch_new, 1)
    ready_client_path.write_text(text, encoding="utf-8")


def patch_css() -> None:
    css = globals_path.read_text(encoding="utf-8")
    if "/* AROMA_OPTIONS_V74 */" not in css:
        css += '\n/* AROMA_OPTIONS_V74 */\n.plp-aroma-options,.pdp-aroma-options{display:flex;flex-wrap:wrap;gap:16px;margin:8px 0 14px}.plp-aroma-options button,.pdp-aroma-options button{border:0;border-bottom:1px solid #bdbdb8;background:transparent;padding:4px 0 6px;font-size:10px;line-height:1.25;text-align:left}.plp-aroma-options button.active,.pdp-aroma-options button.active{border-bottom-color:#111;color:#111}.pdp-aroma-options{margin-bottom:18px}\n'
        globals_path.write_text(css, encoding="utf-8")

    ready_css = ready_css_path.read_text(encoding="utf-8")
    if "/* READY_AROMA_OPTIONS_V74 */" not in ready_css:
        ready_css += '\n/* READY_AROMA_OPTIONS_V74 */\n.rs71-aroma-options{display:flex;flex-wrap:wrap;gap:10px 14px;margin:5px 0 12px}.rs71-aroma-options small{flex:0 0 100%;font-size:8px;letter-spacing:.08em;text-transform:uppercase;color:#777}.rs71-aroma-options button{border:0;border-bottom:1px solid #c8c8c3;background:#fff;padding:0 0 5px;font-size:10px;white-space:nowrap}.rs71-aroma-options button.is-active{border-bottom-color:#111;color:#111}@media(max-width:700px){.rs71-aroma-options{gap:8px 10px}.rs71-aroma-options button{font-size:8px}}\n'
        ready_css_path.write_text(ready_css, encoding="utf-8")


def normalize_constructor_catalog() -> None:
    if not catalog_path.exists():
        raise RuntimeError("V74 constructor catalogue CSV not found")
    with catalog_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise RuntimeError("V74 constructor catalogue header missing")
        rows = list(reader)

    output = []
    for row in rows:
        offer_id = str(row.get("offer_id") or "").strip()
        base_id = offer_id.split("-", 1)[0]
        if base_id.isdigit() and int(base_id) in REMOVED_IDS:
            continue
        if base_id in {"1499", "1500"}:
            aroma = "Дерево жизни" if base_id == "1499" else "Сандал и Шалфей"
            row["group_id"] = "1499"
            row["collection"] = "Жар-птица"
            row["product_name"] = "Свеча Феникс"
            row["product_type"] = "other"
            row["constructor_role"] = "decor"
            row["mix_role"] = "statement_accent"
            row["builder_domain"] = "decor"
            row["color"] = aroma
            row["size"] = "10 см"
            row["material"] = "воск кокосовый"
        output.append(row)

    with catalog_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output)


patch_page()
patch_ready_solution_builder()
patch_ready_solution_ui()
patch_css()
normalize_constructor_catalog()
print("Catalog V74 removals and Phoenix candle aroma merge applied")
