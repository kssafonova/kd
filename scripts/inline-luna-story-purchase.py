from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
text = page_path.read_text(encoding="utf-8")

text = text.replace(
'  const [story,setStory]=useState<"bedroom"|"table"|null>(null);\n  const [builderOpen,setBuilderOpen]=useState(false);',
'  const [story,setStory]=useState<"bedroom"|"table"|null>(null);\n  const [storyBuying,setStoryBuying]=useState(false);\n  const [builderOpen,setBuilderOpen]=useState(false);',
1,
)

text = text.replace(
'  const openBuilder=(ids:number[],title:string)=>{setBuilderIds(ids);setSelectedIds(ids);setBuilderTitle(title);setBuilderOpen(true)};\n  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);setStory(null);chosen.forEach(addToCart)};',
'  const openBuilder=(ids:number[],title:string)=>{setBuilderIds(ids);setSelectedIds(ids);setBuilderTitle(title);setBuilderOpen(true)};\n  const startStoryPurchase=()=>{if(!active)return;setSelectedIds(active.productIds);setStoryBuying(true)};\n  const closeStory=()=>{setStoryBuying(false);setStory(null)};\n  const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};\n  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};',
1,
)

text = text.replace('onClick={()=>setStory(group.id)}><RemoteImage', 'onClick={()=>{setStoryBuying(false);setStory(group.id)}}><RemoteImage')
text = text.replace('onClick={()=>setStory(group.id)}>СМОТРЕТЬ ИСТОРИЮ</button>', 'onClick={()=>{setStoryBuying(false);setStory(group.id)}}>СМОТРЕТЬ ИСТОРИЮ</button>')

text = text.replace(
'<button className="luna-clean-backdrop" onClick={()=>setStory(null)} aria-label="Закрыть"/>',
'<button className="luna-clean-backdrop" onClick={closeStory} aria-label="Закрыть"/>',
1,
)
text = text.replace(
'<header><strong>{active.title}</strong><button type="button" onClick={()=>setStory(null)} aria-label="Закрыть"><Icon name="close"/></button></header>',
'<header><strong>{active.title}</strong><button type="button" onClick={closeStory} aria-label="Закрыть"><Icon name="close"/></button></header>',
1,
)

old = '<div className="luna-clean-products">{storyProducts.map(item=><ProductCard key={`${active.id}-${item.id}`} product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div><div className="luna-clean-story-buy"><button type="button" onClick={()=>openBuilder(active.productIds,`Купить историю · ${active.title}`)}>КУПИТЬ ИСТОРИЮ</button></div>'
new = r'''<div className={`luna-clean-products ${storyBuying?"is-buying":""}`}>{storyProducts.map(item=>{const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell ${storyBuying?(selected?"selected":"not-selected"):""}`} key={`${active.id}-${item.id}`}>
          {storyBuying&&<button className="luna-story-card-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected} aria-label={selected?`Убрать ${item.name}`:`Добавить ${item.name}`}>{selected?"✓":""}</button>}
          <ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>
          {storyBuying&&<div className="luna-story-card-config">{options.length>1?<label><span>Размер</span><select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select></label>:<span className="luna-story-fixed-size">{size}</span>}<div className="luna-story-card-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div></div>}
        </div>})}</div>
        {!storyBuying?<div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div>:<div className="luna-clean-story-buy luna-story-buy-active"><button className="luna-story-buy-cancel" type="button" onClick={()=>setStoryBuying(false)}>ОТМЕНА</button><div className="luna-story-buy-total"><span>{selectedIds.length} {selectedIds.length===1?"товар":"товара"}</span><strong>{fmt(total)}</strong></div><button className="luna-story-buy-add" type="button" disabled={!selectedIds.length} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button></div>}'''
if old not in text:
    raise SystemExit("Inline story purchase marker not found")
text = text.replace(old, new, 1)

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_INLINE_STORY_PURCHASE_V8 \*/[\s\S]*?/\* END_LUNA_INLINE_STORY_PURCHASE_V8 \*/', '', css)
css += r'''

/* LUNA_INLINE_STORY_PURCHASE_V8 */
.luna-story-card-shell{position:relative;min-width:0}
.luna-story-card-shell.not-selected>.product-card{opacity:.42}
.luna-story-card-check{position:absolute;z-index:8;top:10px;left:10px;width:24px;height:24px;border:1px solid rgba(29,29,31,.55);background:#fff;color:#fff;padding:0;display:grid;place-items:center;font:inherit;font-size:12px;cursor:pointer}
.luna-story-card-shell.selected .luna-story-card-check{background:#1d1d1f;border-color:#1d1d1f}
.luna-story-card-config{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;padding:9px 2px 2px;border-top:1px solid #ecece9;background:#fff}
.luna-story-card-config label{display:grid;gap:4px;min-width:0;flex:1}.luna-story-card-config label>span,.luna-story-fixed-size{font-size:9px;color:#777}.luna-story-card-config select{width:100%;height:32px;border:1px solid #d8d8d5;background:#fff;padding:0 7px;font:inherit;font-size:9px;min-width:0}
.luna-story-card-qty{display:flex;align-items:center;height:32px;border:1px solid #ddd;background:#fff;flex:0 0 auto}.luna-story-card-qty button{width:28px;height:30px;border:0;background:#fff;padding:0;font-size:14px;cursor:pointer}.luna-story-card-qty b{width:22px;text-align:center;font-size:9px;font-weight:400}
.luna-clean-story-buy.luna-story-buy-active{position:sticky;bottom:0;z-index:5;display:grid;grid-template-columns:auto 1fr minmax(220px,340px);align-items:center;gap:16px;padding:12px 16px;background:#fff;border-top:1px solid #ddd;box-shadow:0 -5px 15px rgba(0,0,0,.025)}
.luna-clean-story-buy.luna-story-buy-active>button{width:auto;margin:0}.luna-story-buy-cancel{height:auto!important;background:transparent!important;color:#1d1d1f!important;border:0!important;border-bottom:1px solid #777!important;padding:0 0 3px!important;font-size:9px!important}
.luna-story-buy-total{display:flex;align-items:baseline;justify-content:flex-end;gap:9px}.luna-story-buy-total span{font-size:9px;color:#777}.luna-story-buy-total strong{font-size:16px;font-weight:400}.luna-story-buy-add{height:44px!important;width:100%!important;background:#1d1d1f!important;color:#fff!important;border:0!important;padding:0 16px!important;font-size:9px!important;letter-spacing:.08em}.luna-story-buy-add:disabled{opacity:.35;cursor:default}
@media(max-width:700px){
  .luna-story-card-check{top:8px;left:8px;width:23px;height:23px}
  .luna-story-card-config{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:7px;padding:7px 0 0}.luna-story-card-config select{height:30px;font-size:9px}.luna-story-fixed-size{align-self:center}.luna-story-card-qty{height:30px}.luna-story-card-qty button{width:26px;height:28px}.luna-story-card-qty b{width:20px}
  .luna-clean-story-buy.luna-story-buy-active{grid-template-columns:auto 1fr;gap:8px 12px;padding:10px 16px calc(10px + env(safe-area-inset-bottom))}.luna-story-buy-total{justify-content:flex-end}.luna-story-buy-add{grid-column:1/3;height:44px!important}.luna-story-buy-cancel{justify-self:start}.luna-story-buy-total strong{font-size:14px}
}
/* END_LUNA_INLINE_STORY_PURCHASE_V8 */
'''
css_path.write_text(css, encoding="utf-8")
