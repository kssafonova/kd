from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv, json

ROOT=Path(__file__).resolve().parents[1]
SOURCE_DIR=ROOT/"scripts"/"product-source"
PAGE=ROOT/"app"/"page.tsx"
OUT=ROOT/"public"/"data"/"catalog_xlsx_full.csv"
REPORT=ROOT/"public"/"data"/"catalog-import-report.json"
MARKER="// GROUPED_CATALOG_V92"
FIELDS=["Id","Артикул","Название товара","Цвет","Аромат","Размер","Цена","Старая цена","Высота","Ширина","Объем","Диаметр","Комплектация / Информация о размере","Материал","Состав","Детали","Коллекция","Капсула","Категория","Подкатегория","Товар входит в готовое решение","Опционально входит в готовое решение","Описание готового решения","Превью фотография товара","Вторая фотография товара в скролле","Третья фотография в стролле"]
CONFLICT_FIELDS=["Название товара","Материал","Состав","Детали","Коллекция","Капсула","Категория","Подкатегория","Товар входит в готовое решение","Опционально входит в готовое решение"]

def clean_value(value:object)->str:
    text=str(value or "").strip()
    if not text or text=="null": return ""
    text=text.replace("\r\n","\n").replace("\r","\n").replace("\u2028","\n").replace("\u2029","\n").replace("\\n","\n")
    return "\\n".join(part.strip() for part in text.split("\n") if part.strip())

def read_rows():
    files=sorted(SOURCE_DIR.glob("products_part_*.csv")); rows=[]; headers=None
    if not files: raise SystemExit("No product source CSV parts")
    for path in files:
        with path.open("r",encoding="utf-8-sig",newline="") as fh:
            reader=csv.DictReader(fh,delimiter=";"); current=list(reader.fieldnames or [])
            if headers is None: headers=current
            elif current!=headers: raise SystemExit(f"Header mismatch in {path.name}")
            for raw in reader:
                if any(clean_value(v) for v in raw.values()): rows.append({str(k):clean_value(v) for k,v in raw.items() if k is not None})
    missing=sorted({"ID","Артикул","Название товара","Цена","Категория","Подкатегория","Фото 1"}-set(headers or []))
    if missing: raise SystemExit("Missing columns: "+", ".join(missing))
    return rows,len(files)

def map_row(r):
    return {
        "Id":r.get("ID", ""),"Артикул":r.get("Артикул", ""),"Название товара":r.get("Название товара", ""),"Цвет":r.get("Цвет", ""),"Аромат":r.get("Аромат", ""),"Размер":r.get("Размер", ""),"Цена":r.get("Цена", ""),"Старая цена":r.get("Старая цена", ""),"Высота":r.get("Высота", ""),"Ширина":r.get("Ширина", ""),"Объем":r.get("Объем", ""),"Диаметр":r.get("Диаметр", ""),"Комплектация / Информация о размере":r.get("Комплектация / информация о размере", ""),"Материал":r.get("Материал", ""),"Состав":r.get("Состав", ""),"Детали":r.get("Детали", ""),"Коллекция":r.get("Коллекция", ""),"Капсула":r.get("Капсула", ""),"Категория":r.get("Категория", ""),"Подкатегория":r.get("Подкатегория", ""),"Товар входит в готовое решение":r.get("Товар входит в готовое решение", ""),"Опционально входит в готовое решение":r.get("Опционально входит в готовое решение", ""),"Описание готового решения":r.get("Капсула.1", ""),"Превью фотография товара":r.get("Фото 1", ""),"Вторая фотография товара в скролле":r.get("Фото 2", ""),"Третья фотография в стролле":r.get("Фото 3", "")
    }

def report_for(source,valid,invalid):
    by=defaultdict(list)
    for r in source:
        if r.get("Артикул"): by[r["Артикул"]].append(r)
    valid_by=defaultdict(list)
    for r in valid: valid_by[r["Артикул"]].append(r)
    invalid_rows=[]
    for article in sorted(invalid):
        first=by[article][0]; invalid_rows.append({"article":article,"name":first.get("Название товара"),"category":first.get("Категория") or None,"subcategory":first.get("Подкатегория") or None,"reason":"missing category/subcategory"})
    conflicts=[]
    for article,group in sorted(valid_by.items()):
        fields={}
        for field in CONFLICT_FIELDS:
            vals=list(dict.fromkeys(r.get(field,"") for r in group if r.get(field,"")))
            if len(vals)>1: fields[field]=vals
        if fields: conflicts.append({"article":article,"name":group[0]["Название товара"],"fields":fields})
    scents=[]
    for article,group in sorted(valid_by.items()):
        first=group[0]; values=list(dict.fromkeys(r["Аромат"] for r in group if r["Аромат"]))
        if first["Категория"]=="Декор для дома" and first["Подкатегория"]=="Свечи и диффузоры" and values: scents.append({"article":article,"name":first["Название товара"],"scents":values})
    return {"marker":MARKER,"source_rows":len(source),"source_articles":len(by),"valid_rows":len(valid),"valid_articles":len(valid_by),"invalid_articles":invalid_rows,"conflicts":conflicts,"scent_switch_articles":scents}

def replace(text,old,new,label):
    if new in text: return text
    if old not in text: raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old,new,1)

def patch_page():
    text=PAGE.read_text(encoding="utf-8")
    if '  switchBy?: "color" | "scent" | "none";\n' not in text:
        text=replace(text,"  optionalReadySolution?: string;\n};",'  optionalReadySolution?: string;\n  switchBy?: "color" | "scent" | "none";\n};',"switchBy type")
    if MARKER not in text:
        old='const priceKnown=(value:number)=>Number.isFinite(value)&&value>0;\n// CATALOG_PRODUCT_NORMALIZATION_V74\nconst isAromaProduct=(product:Product)=>product.id===1499||product.article==="KD-PD-2519"||String(product.name||"").trim().toLocaleLowerCase("ru-RU")==="свеча феникс";'
        new='const priceKnown=(value:number)=>Number.isFinite(value)&&value>0;\n// GROUPED_CATALOG_V92\nconst cleanNulls=(value:unknown)=>{const text=String(value??"").trim();return !text||text==="null"?undefined:text};\nconst splitMultiline=(value:unknown)=>{const text=cleanNulls(value);return text?text.split(/\\\\n|\\n|\\u2028|\\u2029/g).map(part=>part.trim()).filter(Boolean):[]};\nconst renderMultiline=(value:unknown)=>{const parts=splitMultiline(value);return parts.length?<>{parts.map((part,index)=><p key={`${part}-${index}`}>{part}</p>)}</>:null};\nconst parseCatalogPrice=(value:unknown)=>Number(String(cleanNulls(value)??"").replace(/[^\\d.,-]/g,"").replace(",","."))||0;\n// CATALOG_PRODUCT_NORMALIZATION_V74\nconst isAromaProduct=(product:Product)=>product.switchBy==="scent";'
        text=replace(text,old,new,"cleanNulls/renderMultiline helpers")
    text=replace(text,'  const rows=chunks.flat().filter(row=>row["Артикул"]&&row["Название товара"]);','  const rows=chunks.flat().map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as XlsxProductEntityRow).filter(row=>row["Артикул"]&&row["Название товара"]&&row["Категория"]&&row["Подкатегория"]);',"runtime null/category filter")
    start=text.find("  grouped.forEach((variants)=>{"); end=text.find("  products=incoming;",start)
    if start<0 or end<0: raise SystemExit("catalog grouping block not found")
    loader='''  grouped.forEach((variants)=>{\n    const first=variants[0],article=cleanNulls(first["Артикул"])??"",name=cleanNulls(first["Название товара"])??article;\n    const existing=products.find(product=>String(product.article||"").trim()===article),id=existing?.id??entityId(article,name);\n    const category=cleanNulls(first["Категория"]),subcategory=cleanNulls(first["Подкатегория"]);\n    const colors=Array.from(new Set(variants.map(row=>cleanNulls(row["Цвет"])).filter(Boolean))),scents=Array.from(new Set(variants.map(row=>cleanNulls(row["Аромат"])).filter(Boolean)));\n    const scentMode=category==="Декор для дома"&&subcategory==="Свечи и диффузоры"&&scents.length>1;\n    const switchBy:Product["switchBy"]=scentMode?"scent":colors.length>1?"color":"none";\n    const skus:CatalogSku[]=variants.map((row,index)=>{\n      const images=[row["Превью фотография товара"],row["Вторая фотография товара в скролле"],row["Третья фотография в стролле"]].map(cleanNulls).filter((value):value is string=>Boolean(value));\n      const sourceColor=cleanNulls(row["Цвет"]),scent=cleanNulls(row["Аромат"]),key=(switchBy==="scent"?scent:switchBy==="color"?sourceColor:undefined)??"Единый вариант";\n      const size=cleanNulls(row["Размер"])??cleanNulls(row["Объем"])??cleanNulls(row["Диаметр"])??"Единый размер",price=parseCatalogPrice(row["Цена"]),oldPrice=parseCatalogPrice(row["Старая цена"]);\n      return {id:`xlsx-${id}-${index}`,article,productId:id,color:key,colorHex:entityColorHex(sourceColor??key),size,height:cleanNulls(row["Высота"]),width:cleanNulls(row["Ширина"]),diameter:cleanNulls(row["Диаметр"]),packageInfo:cleanNulls(row["Комплектация / Информация о размере"]),material:cleanNulls(row["Материал"])??"",composition:cleanNulls(row["Состав"])??"",details:cleanNulls(row["Детали"]),collection:cleanNulls(row["Коллекция"]),capsule:cleanNulls(row["Капсула"]),price,image:images[0]??"/images/image-placeholder.svg",gallery:images.slice(1),available:true,...({volume:cleanNulls(row["Объем"]),oldPrice:oldPrice>price?oldPrice:undefined,sourceColor,scent} as any)};\n    });\n    const firstSku=skus[0],priced=skus.filter(item=>priceKnown(item.price)),minSku=priced.reduce<CatalogSku|undefined>((best,item)=>!best||item.price<best.price?item:best,undefined),price=minSku?.price??0;\n    const switchRows=Array.from(new Map(skus.map(item=>[item.color,item])).values());\n    incoming.push({id,name,article,note:[cleanNulls(firstSku.material),cleanNulls(firstSku.size)].filter(Boolean).join(", "),price,oldPrice:Number((minSku as any)?.oldPrice)||undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:switchRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery})),category,subcategory,collection:cleanNulls(first["Коллекция"]),capsule:cleanNulls(first["Капсула"]),readySolution:cleanNulls(first["Товар входит в готовое решение"]),optionalReadySolution:cleanNulls(first["Опционально входит в готовое решение"]),switchBy});\n  });\n'''
    text=text[:start]+loader+text[end:]
    text=replace(text,'  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??sizes[0]?.[1]??product.price;','  const unitPrice=sku?.price??(sizes.length?Math.min(...sizes.map(([,value])=>value)):product.price);',"min size price")
    text=replace(text,'  const specs=sku??mediaSku??product.skus?.[0];\n  const needsSize=Boolean(sizes.length&&!effectiveSelectedSize);','  const specs=sku??mediaSku??product.skus?.[0];\n  const specsExtra=specs as (CatalogSku&{volume?:string;oldPrice?:number})|undefined;\n  const currentOldPrice=Number(specsExtra?.oldPrice)||0;\n  const solutionTags=Array.from(new Set([...splitMultiline(product.readySolution),...splitMultiline(product.optionalReadySolution)]));\n  const needsSize=Boolean(sizes.length&&!effectiveSelectedSize);',"variant metadata")
    old='<div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{knownUnitPrice?(sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)):"Цена уточняется"}</strong>{knownUnitPrice&&product.oldPrice&&<><del>{sizes.length>1&&!selectedSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}</small><label className="pdp-color-label">{isAromaProduct(product)?"Аромат":"Цвет"}: {color.name}</label>{isAromaProduct(product)&&variants.length>1&&<div className="pdp-aroma-options">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}}>{variant.name}</button>)}</div>}{!isAromaProduct(product)&&variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}'
    new='<div className={`pdp-price ${currentOldPrice>unitPrice?"sale":""}`}><strong>{knownUnitPrice?(sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)):"Цена уточняется"}</strong>{knownUnitPrice&&currentOldPrice>unitPrice&&<><del>{fmt(currentOldPrice)}</del><mark>−{Math.round((1-unitPrice/currentOldPrice)*100)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}</small>{solutionTags.length>0&&<div className="pdp-aroma-options" aria-label="Готовые решения">{solutionTags.map(tag=><a key={tag} href={`${process.env.NEXT_PUBLIC_BASE_PATH??""}/ready-solutions`}>{tag}</a>)}</div>}{product.switchBy!=="none"&&<label className="pdp-color-label">{isAromaProduct(product)?"Аромат":"Цвет"}: {color.name}</label>}{isAromaProduct(product)&&variants.length>1&&<div className="pdp-aroma-options">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}}>{variant.name}</button>)}</div>}{product.switchBy==="color"&&variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}'
    text=replace(text,old,new,"PDP switch/price/tags")
    old='{title:"ХАРАКТЕРИСТИКИ",content:specs?<><p>{specs.collection?`${specs.material}. ${specs.size}. Коллекция «${specs.collection}».`:`${specs.material}. ${specs.size}.`}</p><dl><div><dt>Материал</dt><dd>{specs.material}</dd></div><div><dt>Состав</dt><dd>{specs.composition}</dd></div>{specs.height&&<div><dt>Высота</dt><dd>{specs.height}</dd></div>}{specs.width&&<div><dt>Ширина</dt><dd>{specs.width}</dd></div>}{specs.diameter&&<div><dt>Диаметр</dt><dd>{specs.diameter}</dd></div>}{specs.packageInfo&&<div><dt>Комплектация</dt><dd>{specs.packageInfo}</dd></div>}{specs.details&&<div><dt>Детали</dt><dd>{specs.details}</dd></div>}{specs.collection&&<div><dt>Коллекция</dt><dd>{specs.collection}</dd></div>}</dl></>:<p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p>},'
    new='{title:"ХАРАКТЕРИСТИКИ",content:specs?<dl>{cleanNulls(specs.material)&&<div><dt>Материал</dt><dd>{renderMultiline(specs.material)}</dd></div>}{cleanNulls(specs.composition)&&<div><dt>Состав</dt><dd>{renderMultiline(specs.composition)}</dd></div>}{cleanNulls(specs.height)&&<div><dt>Высота</dt><dd>{renderMultiline(specs.height)}</dd></div>}{cleanNulls(specs.width)&&<div><dt>Ширина</dt><dd>{renderMultiline(specs.width)}</dd></div>}{cleanNulls(specsExtra?.volume)&&<div><dt>Объём</dt><dd>{renderMultiline(specsExtra?.volume)}</dd></div>}{cleanNulls(specs.diameter)&&<div><dt>Диаметр</dt><dd>{renderMultiline(specs.diameter)}</dd></div>}{cleanNulls(specs.packageInfo)&&<div><dt>Комплектация</dt><dd>{renderMultiline(specs.packageInfo)}</dd></div>}{cleanNulls(specs.details)&&<div><dt>Детали</dt><dd>{renderMultiline(specs.details)}</dd></div>}{cleanNulls(specs.collection)&&<div><dt>Коллекция</dt><dd>{renderMultiline(specs.collection)}</dd></div>}{cleanNulls(specs.capsule)&&<div><dt>Капсула</dt><dd>{renderMultiline(specs.capsule)}</dd></div>}</dl>:null},'
    text=replace(text,old,new,"multiline/null characteristics")
    text=text.replace('<small>{chosen.name.toLowerCase()}, {product.note}</small>','<small>{product.switchBy==="none"?product.note:<>{chosen.name.toLowerCase()}, {product.note}</>}</small>')
    text=text.replace('<p className="quick-color">{isAromaProduct(product)?"Аромат":"Цвет"}: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>','{product.switchBy!=="none"&&<p className="quick-color">{isAromaProduct(product)?"Аромат":"Цвет"}: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>}')
    PAGE.write_text(text,encoding="utf-8")

def main():
    source,parts=read_rows(); mapped=[map_row(r) for r in source if r.get("Артикул") and r.get("Название товара")]
    invalid={r["Артикул"] for r in mapped if not r["Категория"] or not r["Подкатегория"]}; valid=[r for r in mapped if r["Артикул"] not in invalid]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(valid)
    report=report_for(source,valid,invalid); REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    patch_page()
    print(f"{MARKER}: {report['source_rows']} rows/{report['source_articles']} articles -> {report['valid_rows']} rows/{report['valid_articles']} cards; {len(report['invalid_articles'])} invalid; {len(report['conflicts'])} conflicts; {len(report['scent_switch_articles'])} scent switch; {parts} parts")
    for x in report["invalid_articles"]: print(f"INVALID {x['article']}: {x['category']!r} / {x['subcategory']!r}")
    for x in report["conflicts"]: print(f"CONFLICT {x['article']}: {', '.join(x['fields'])}")

if __name__=="__main__": main()
