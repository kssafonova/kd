from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
RESOLVER = Path(__file__).resolve().parents[1] / "app" / "constructor" / "table-solution-resolver.ts"
MARKER = "// CANONICAL_TABLE_SYNC_V85"

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old, new, 1)

def patch_page() -> None:
    text = PAGE.read_text(encoding="utf-8")
    if MARKER not in text:
        text = replace_once(text, 'const XLSX_ENTITY_FILES = Array.from({length:5},(_,index)=>`kultura_doma_product_entities_xlsx_${index+1}.csv`);', 'const XLSX_ENTITY_FILES:string[] = []; // canonical data is loaded from the compressed table snapshot below', "canonical entity source")
        text = replace_once(
            text,
            'const grouped=new Map<string,XlsxProductEntityRow[]>();\n'
            '  rows.forEach(row=>{const key=`${row["Артикул"]}|${row["Название товара"]}`;const list=grouped.get(key)||[];list.push(row);grouped.set(key,list)});\n'
            '  const existingByArticle=new Map(products.map(product=>[String(product.article||"").trim(),product]));',
            'const grouped=new Map<string,XlsxProductEntityRow[]>();\n'
            '  rows.forEach(row=>{const key=`${row["Артикул"]}|${row["Название товара"]}`;const list=grouped.get(key)||[];list.push(row);grouped.set(key,list)});\n'
            '  // The canonical table may reuse one article for distinct named products, so article+name is the storefront entity key.\n'
            f'  {MARKER}',
            "canonical entity key",
        )
        text = replace_once(
            text,
            '    const existing=existingByArticle.get(article);\n'
            '    const id=existing?.id??entityId(article,name);\n'
            '    const price=existing?.price??0;',
            '    const existing=products.find(product=>String(product.article||"").trim()===article&&String(product.name||"").trim()===name);\n'
            '    const id=existing?.id??entityId(article,name);\n'
            '    const tablePrice=Number(String(first["Цена"]||"").replace(/[^\\d.,-]/g,"").replace(",","."))||0;\n'
            '    const price=tablePrice>0?tablePrice:(existing?.price??0);\n'
            '    const tableOldPrice=Number(String(first["Старая цена"]||"").replace(/[^\\d.,-]/g,"").replace(",","."))||0;',
            "table prices",
        )
        text = replace_once(
            text,
            'collection:String(row["Коллекция"]||"").trim()||undefined,price,image:images[0]||"/assets/images/image-placeholder.svg"',
            'collection:String(row["Коллекция"]||"").trim()||undefined,price:Number(String(row["Цена"]||price).replace(/[^\\d.,-]/g,"").replace(",","."))||price,image:images[0]||"/assets/images/image-placeholder.svg"',
            "sku price",
        )
        text = replace_once(
            text,
            'incoming.push({...existing,id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,image:firstSku.image',
            'incoming.push({...existing,id,name,article,note:[firstSku.material,firstSku.size].filter(Boolean).join(", "),price,oldPrice:tableOldPrice>price?tableOldPrice:undefined,image:firstSku.image',
            "product old price",
        )
        text = replace_once(
            text,
            '  const incomingById=new Map(incoming.map(item=>[item.id,item]));\n'
            '  products=[...products.map(item=>incomingById.get(item.id)??item),...incoming.filter(item=>!products.some(current=>current.id===item.id))];\n'
            '}',
            '''  products=incoming;
  const tableCollectionNames=Array.from(new Set(rows.map(row=>String(row["Коллекция"]||"").trim()).filter(Boolean)));
  const editorialKey=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
  const previousEditorials=new Map(editorials.map(item=>[editorialKey(item.name),item]));
  editorials=tableCollectionNames.map((collection,index)=>{
    const productIds=products.filter(product=>product.skus?.some(sku=>String(sku.collection||"").trim()===collection)).map(product=>product.id);
    const productImages=Array.from(new Set(products.filter(product=>productIds.includes(product.id)).flatMap(product=>[product.image,...(product.gallery??[])])).values()).filter(Boolean).slice(0,3);
    const previous=previousEditorials.get(editorialKey(collection));
    const next:Editorial=previous
      ? {...previous,name:collection,kind:"КОЛЛЕКЦИЯ",productIds,images:previous.images?.length?previous.images:productImages}
      : {id:`table-collection-${index+1}`,name:collection,kind:"КОЛЛЕКЦИЯ",lead:"Предметы коллекции, собранные в единую историю для дома.",detail:"Откройте коллекцию и выберите предметы, которые работают вместе.",description:`Коллекция «${collection}» по актуальной товарной таблице Культура Дома.`,images:productImages.length?productImages:["/assets/images/image-placeholder.svg"],productIds};
    return next;
  });
}''',
            "authoritative catalog and collections",
        )
        text = replace_once(text, 'const editorials:Editorial[] = [', 'let editorials:Editorial[] = [', "mutable editorials")
        PAGE.write_text(text, encoding="utf-8")

def patch_resolver() -> None:
    text = RESOLVER.read_text(encoding="utf-8")
    marker = "// TABLE_READY_RELATIONS_V85"
    if marker in text:
        return
    text = replace_once(
        text,
        '  const productType = normalizeSolutionValue(row.product_type || "");\n\n'
        '  const rawCollectionMatch = collectionTargets.some(',
        '  const productType = normalizeSolutionValue(row.product_type || "");\n'
        f'  {marker}\n'
        '  const relationTargets=[solution.name,solution.sourceName].map(normalizeSolutionValue).filter(Boolean);\n'
        '  const relationMatch=String(row.style_tags||"").split("|").some(tag=>{\n'
        '    const separator=tag.indexOf(":");\n'
        '    if(separator<0)return false;\n'
        '    const kind=tag.slice(0,separator);\n'
        '    if(kind!=="required"&&kind!=="optional")return false;\n'
        '    const value=normalizeSolutionValue(tag.slice(separator+1));\n'
        '    return relationTargets.some(target=>matchesLoose(value,target));\n'
        '  });\n\n'
        '  const rawCollectionMatch = collectionTargets.some(',
        "ready relation tags",
    )
    text = replace_once(
        text,
        '  return collectionMatch || explicitProductMatch;',
        '  return relationMatch || collectionMatch || explicitProductMatch;',
        "ready relation return",
    )
    RESOLVER.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    patch_page()
    patch_resolver()
    print("Canonical table storefront sync applied")
