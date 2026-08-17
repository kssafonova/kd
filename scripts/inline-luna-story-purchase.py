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
new = r'''{!storyBuying?<><div className="luna-clean-products">{storyProducts.map(item=><ProductCard key={`${active.id}-${item.id}`} product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div><div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div></>:<section className="luna-story-inline-config">
          <div className="luna-story-inline-head"><div><strong>Выберите товары</strong><span>Можно изменить размер и количество</span></div><button type="button" onClick={()=>setStoryBuying(false)}>ОТМЕНА</button></div>
          <div className="luna-story-inline-list">{storyProducts.map(item=>{const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const quantity=qty[item.id]??1;return <article className={selected?"selected":""} key={`story-config-${item.id}`}>
            <button className="luna-story-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected} aria-label={selected?`Убрать ${item.name}`:`Добавить ${item.name}`}>{selected?"✓":""}</button>
            <RemoteImage src={previewById[item.id]??item.image} alt={item.name}/>
            <div className="luna-story-item-copy"><h3>{item.name}</h3>{options.length>1?<label><span>Размер</span><select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select></label>:<small>{size}</small>}<div className="luna-story-item-bottom"><strong>{fmt(item.price*quantity)}</strong><div className="luna-story-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div></div></div>
          </article>})}</div>
          <footer className="luna-story-inline-footer"><div><span>{selectedIds.length} {selectedIds.length===1?"товар":"товара"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button></footer>
        </section>}'''
if old not in text:
    raise SystemExit("Inline story purchase marker not found")
text = text.replace(old, new, 1)

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_INLINE_STORY_PURCHASE_V8 \*/[\s\S]*?/\* END_LUNA_INLINE_STORY_PURCHASE_V8 \*/', '', css)
css += r'''

/* LUNA_INLINE_STORY_PURCHASE_V8 */
.luna-story-inline-config{background:#fff;border-top:1px solid #e8e8e5}
.luna-story-inline-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;padding:20px 18px 12px}
.luna-story-inline-head>div{display:grid;gap:4px}.luna-story-inline-head strong{font-size:15px;font-weight:400}.luna-story-inline-head span{font-size:11px;color:#777}
.luna-story-inline-head>button{border:0;background:transparent;padding:2px 0;border-bottom:1px solid #777;font:inherit;font-size:9px;letter-spacing:.08em;cursor:pointer}
.luna-story-inline-list{padding:0 18px 10px}
.luna-story-inline-list article{display:grid;grid-template-columns:28px 90px minmax(0,1fr);gap:13px;align-items:center;padding:15px 0;border-bottom:1px solid #ecece9;opacity:.42;transition:opacity .15s ease}
.luna-story-inline-list article.selected{opacity:1}.luna-story-inline-list article>img{width:90px;height:108px;object-fit:cover;background:#f4f4f2}
.luna-story-check{width:22px;height:22px;border:1px solid #aaa;background:#fff;color:#fff;padding:0;cursor:pointer}.selected .luna-story-check{background:#1d1d1f;border-color:#1d1d1f}
.luna-story-item-copy{min-width:0}.luna-story-item-copy h3{font-size:13px;font-weight:400;margin:0 0 9px}.luna-story-item-copy label{display:grid;grid-template-columns:auto minmax(140px,260px);align-items:center;gap:10px}.luna-story-item-copy label>span,.luna-story-item-copy small{font-size:10px;color:#777}.luna-story-item-copy select{height:34px;border:1px solid #d8d8d5;background:#fff;padding:0 8px;font:inherit;font-size:10px;min-width:0}
.luna-story-item-bottom{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:10px}.luna-story-item-bottom>strong{font-size:13px;font-weight:400}.luna-story-qty{display:flex;align-items:center;border:1px solid #ddd}.luna-story-qty button{width:30px;height:30px;border:0;background:#fff;font-size:15px;cursor:pointer}.luna-story-qty b{width:24px;text-align:center;font-size:10px;font-weight:400}
.luna-story-inline-footer{position:sticky;bottom:0;z-index:3;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:12px 18px;background:#fff;border-top:1px solid #dcdcd8;box-shadow:0 -5px 15px rgba(0,0,0,.025)}
.luna-story-inline-footer>div{display:grid;gap:2px}.luna-story-inline-footer span{font-size:9px;color:#777}.luna-story-inline-footer strong{font-size:16px;font-weight:400}.luna-story-inline-footer>button{height:44px;min-width:230px;border:0;background:#1d1d1f;color:#fff;padding:0 18px;font:inherit;font-size:9px;letter-spacing:.08em;cursor:pointer}.luna-story-inline-footer>button:disabled{opacity:.35;cursor:default}
@media(max-width:700px){
  .luna-story-inline-head{padding:17px 16px 10px}.luna-story-inline-head strong{font-size:14px}.luna-story-inline-head span{font-size:10px}
  .luna-story-inline-list{padding:0 16px}.luna-story-inline-list article{grid-template-columns:24px 76px minmax(0,1fr);gap:10px;padding:13px 0}.luna-story-inline-list article>img{width:76px;height:94px}.luna-story-item-copy h3{font-size:12px;line-height:1.25;margin-bottom:7px}.luna-story-item-copy label{display:grid;grid-template-columns:1fr;gap:4px}.luna-story-item-copy select{width:100%;height:32px}.luna-story-item-bottom{margin-top:7px}.luna-story-qty button{width:28px;height:28px}.luna-story-inline-footer{padding:10px 16px calc(10px + env(safe-area-inset-bottom));gap:10px}.luna-story-inline-footer>button{min-width:0;flex:1;height:44px;padding:0 10px}.luna-story-inline-footer strong{font-size:14px}
}
/* END_LUNA_INLINE_STORY_PURCHASE_V8 */
'''
css_path.write_text(css, encoding="utf-8")
