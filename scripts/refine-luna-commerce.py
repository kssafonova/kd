from pathlib import Path
import re

page_path=Path("app/page.tsx")
css_path=Path("app/globals.css")
text=page_path.read_text(encoding="utf-8")

text=text.replace(
'  const [builderOpen,setBuilderOpen]=useState(false);\n  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);',
'  const [builderOpen,setBuilderOpen]=useState(false);\n  const [builderIds,setBuilderIds]=useState<number[]>(editorial.productIds);\n  const [builderTitle,setBuilderTitle]=useState("Соберите капсулу");\n  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);',
1)

prepare=r'''  const prepare=(product:Product):Product=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const regularPrice=product.oldPrice??product.price;
    const preview=previewById[product.id];
    const variants=(product.colorVariants??[]).filter(variant=>variant.name===color);
    const skus=product.skus?.filter(s=>s.color===color).map(s=>({...s,price:regularPrice,...(preview?{image:preview,gallery:Array.from(new Set([preview,...s.gallery]))}:{} )}));
    const sku=skus?.find(s=>s.color===color)??skus?.[0];
    return {
      ...product,
      oldPrice:undefined,
      badge:undefined,
      image:preview??sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      colorVariants:variants.length?variants:product.colorVariants,
      skus,
      selectedColor:sku?.color??color,
      selectedSize:sku?.size??product.selectedSize,
      selectedSkuId:sku?.id,
      price:regularPrice,
    };
  };'''
text,count=re.subn(r'  const prepare=\(product:Product\):Product=>\{[\s\S]*?\n  \};(?=\n  const items=)',prepare,text,count=1)
if count!=1: raise SystemExit("Luna prepare() marker not found")

text=text.replace(
'  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];',
'  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];\n  const builderItems=builderIds.map(itemById).filter(Boolean) as Product[];',
1)

text=text.replace(
'    return {...item,price:sku?.price??item.price,image:sku?.image??item.image,gallery:sku?.gallery??item.gallery,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id,quantity};',
'    return {...item,price:item.price,image:sku?.image??item.image,gallery:sku?.gallery??item.gallery,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id,quantity};',
1)

text=text.replace(
'  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(x=>x!==id):[...current,id]);\n  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);chosen.forEach(addToCart)};',
'  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(x=>x!==id):[...current,id]);\n  const openBuilder=(ids:number[],title:string)=>{setBuilderIds(ids);setSelectedIds(ids);setBuilderTitle(title);setBuilderOpen(true)};\n  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);setStory(null);chosen.forEach(addToCart)};',
1)

text=text.replace(
'<section className="luna-clean-builder-entry"><h2>Соберите капсулу</h2><button type="button" onClick={()=>setBuilderOpen(true)}>СОБРАТЬ КАПСУЛУ</button></section>',
'<section className="luna-clean-builder-entry"><h2>Соберите капсулу</h2><button type="button" onClick={()=>openBuilder(editorial.productIds,"Соберите капсулу")}>СОБРАТЬ КАПСУЛУ</button></section>',
1)

story_products='<div className="luna-clean-products">{storyProducts.map(item=><ProductCard key={`${active.id}-${item.id}`} product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>'
story_products_new=story_products+'<div className="luna-clean-story-buy"><button type="button" onClick={()=>openBuilder(active.productIds,`Купить историю · ${active.title}`)}>КУПИТЬ ИСТОРИЮ</button></div>'
if story_products not in text: raise SystemExit("Story products marker not found")
text=text.replace(story_products,story_products_new,1)

text=text.replace(
'<header><strong>Соберите капсулу</strong><button type="button" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"><Icon name="close"/></button></header>',
'<header><strong>{builderTitle}</strong><button type="button" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"><Icon name="close"/></button></header>',
1)

text=text.replace(
'<div className="luna-clean-builder-tools"><span>{selectedIds.length} из {items.length}</span><button type="button" onClick={()=>setSelectedIds(selectedIds.length===items.length?[]:items.map(i=>i.id))}>{selectedIds.length===items.length?"СНЯТЬ ВСЕ":"ВЫБРАТЬ ВСЕ"}</button></div>',
'<div className="luna-clean-builder-tools"><span>{selectedIds.length} из {builderItems.length}</span><button type="button" onClick={()=>setSelectedIds(selectedIds.length===builderItems.length?[]:builderItems.map(i=>i.id))}>{selectedIds.length===builderItems.length?"СНЯТЬ ВСЕ":"ВЫБРАТЬ ВСЕ"}</button></div>',
1)

text=text.replace('<div className="luna-clean-builder-list">{items.map(item=>{','<div className="luna-clean-builder-list">{builderItems.map(item=>{',1)

text=text.replace(
'<footer><div><span>{selectedIds.length} позиций</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addAll}>ДОБАВИТЬ В КОРЗИНУ</button></footer>',
'<footer><div><span>{selectedIds.length} позиций</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addAll}>{builderIds.length===items.length?"ДОБАВИТЬ КАПСУЛУ В КОРЗИНУ":"ДОБАВИТЬ ИСТОРИЮ В КОРЗИНУ"}</button></footer>',
1)

page_path.write_text(text,encoding="utf-8")

css=css_path.read_text(encoding="utf-8")
css=re.sub(r'\n?/\* LUNA_STORY_COMMERCE_V7 \*/[\s\S]*?/(?=\* END_LUNA_STORY_COMMERCE_V7 \*/)|\n?/\* LUNA_STORY_COMMERCE_V7 \*/[\s\S]*\Z','',css)
css+=r'''

/* LUNA_STORY_COMMERCE_V7 */
.luna-clean-story-buy{display:flex;justify-content:center;padding:2px 16px 30px;background:#fff}
.luna-clean-story-buy button{width:min(360px,100%);height:46px;border:0;background:#1d1d1f;color:#fff;font:inherit;font-size:10px;letter-spacing:.09em;cursor:pointer}
.luna-clean-builder>header strong{max-width:calc(100% - 52px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.luna-clean-builder footer>button:disabled{opacity:.35;cursor:default}
@media(max-width:700px){
  .luna-clean-story-buy{padding:0 16px 22px}
  .luna-clean-story-buy button{width:100%;height:48px}
  .luna-clean-builder>header strong{font-size:13px}
  .luna-clean-builder footer>button{min-width:0;flex:1;padding:0 12px}
}
/* END_LUNA_STORY_COMMERCE_V7 */
'''
css_path.write_text(css,encoding="utf-8")
