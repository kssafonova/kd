from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
text = page_path.read_text(encoding="utf-8")

# ProductCard keeps its existing layout. In story purchase mode the quick-add slot
# becomes a 3-state selector: selected / excluded / pending-size.
sig_base = 'function ProductCard({ product, onClick, onQuick, favorite, liked }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean }) {'
sig_v9 = 'function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; onSelect?:()=>void }) {'
sig_v10 = 'function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void }) {'
if sig_base in text:
    text = text.replace(sig_base, sig_v10, 1)
elif sig_v9 in text:
    text = text.replace(sig_v9, sig_v10, 1)
elif sig_v10 not in text:
    raise SystemExit("ProductCard signature marker not found")

quick_base = '<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>'
quick_v9 = '{selectionMode?<button className={`quick selection-check ${selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{selected?"✓":""}</button>:<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>}'
quick_v10 = '{selectionMode?<button className={`quick selection-check ${pending?"pending":selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={pending?`Выберите размер для ${product.name}`:selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{pending?"?":selected?"✓":""}</button>:<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>}'
quick_nested = quick_v9.replace(quick_base, quick_v10)
if quick_nested in text:
    text = text.replace(quick_nested, quick_v10, 1)
elif quick_v9 in text:
    text = text.replace(quick_v9, quick_v10, 1)
elif quick_v10 in text:
    pass
elif quick_base in text:
    text = text.replace(quick_base, quick_v10, 1)
else:
    raise SystemExit("ProductCard quick control marker not found")

# Story purchase needs to distinguish "not selected by the user" from
# "intended, but cannot be selected yet because a size is missing".
state_old = '  const [storyBuying,setStoryBuying]=useState(false);\n  const [builderOpen,setBuilderOpen]=useState(false);'
state_new = '  const [storyBuying,setStoryBuying]=useState(false);\n  const [storyExcludedIds,setStoryExcludedIds]=useState<number[]>([]);\n  const [builderOpen,setBuilderOpen]=useState(false);'
if state_old in text:
    text = text.replace(state_old, state_new, 1)
elif state_new not in text:
    raise SystemExit("Story purchase state marker not found")

story_products = '  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];'
story_validation = story_products + '''\n  const storyPendingIds=storyProducts.filter(item=>!storyExcludedIds.includes(item.id)).filter(item=>{const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);return options.length>1&&!sizes[item.id]}).map(item=>item.id);\n  const storyReady=storyPendingIds.length===0&&selectedIds.length>0;\n  const pendingStoryProducts=storyProducts.filter(item=>storyPendingIds.includes(item.id));'''
text = re.sub(
    re.escape(story_products) + r'\n  const storyReady=storyProducts\.filter\(item=>selectedIds\.includes\(item\.id\)\)\.every\(item=>\{const color=colorById\[item\.id\]\?\?item\.selectedColor;const options=getProductSizeOptions\(item,color\);return options\.length<=1\|\|Boolean\(sizes\[item\.id\]\)\}\);',
    story_validation,
    text,
    count=1,
)
if story_validation not in text:
    if story_products not in text:
        raise SystemExit("storyProducts marker not found")
    text = text.replace(story_products, story_validation, 1)

# Start with fixed-size items selected. Multi-size products stay pending until the
# user chooses a size. Any stale story size choices are cleared on a fresh entry.
start_base = 'const startStoryPurchase=()=>{if(!active)return;setSelectedIds(active.productIds);setStoryBuying(true)};'
start_v9 = 'const startStoryPurchase=()=>{if(!active)return;setSelectedIds(active.productIds);setSizes(current=>{const next={...current};active.productIds.forEach(id=>delete next[id]);return next});setStoryBuying(true)};'
start_v10 = 'const startStoryPurchase=()=>{if(!active)return;const initialSelected=active.productIds.filter(id=>{const item=itemById(id);if(!item)return false;const color=colorById[item.id]??item.selectedColor;return getProductSizeOptions(item,color).length<=1});setSelectedIds(initialSelected);setStoryExcludedIds([]);setSizes(current=>{const next={...current};active.productIds.forEach(id=>delete next[id]);return next});setStoryBuying(true)};'
if start_base in text:
    text = text.replace(start_base, start_v10, 1)
elif start_v9 in text:
    text = text.replace(start_v9, start_v10, 1)
elif start_v10 not in text:
    raise SystemExit("startStoryPurchase marker not found")

close_base = 'const closeStory=()=>{setStoryBuying(false);setStory(null)};'
close_v10 = 'const closeStory=()=>{setStoryBuying(false);setStoryExcludedIds([]);setStory(null)};'
if close_base in text:
    text = text.replace(close_base, close_v10, 1)
elif close_v10 not in text:
    raise SystemExit("closeStory marker not found")

# Keep the generic toggle for the full-capsule builder, and add a story-specific
# tri-state toggle. Pending -> excluded lets a user intentionally omit that item.
toggle_marker = '  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(x=>x!==id):[...current,id]);'
toggle_helpers = toggle_marker + '''\n  const focusStorySize=(id:number)=>setTimeout(()=>document.getElementById(`story-size-${id}`)?.focus(),0);\n  const toggleStoryItem=(item:Product,requiresSize:boolean,hasSize:boolean)=>{const id=item.id;const selected=selectedIds.includes(id);const excluded=storyExcludedIds.includes(id);if(selected){setSelectedIds(current=>current.filter(x=>x!==id));setStoryExcludedIds(current=>current.includes(id)?current:[...current,id]);return}if(excluded){setStoryExcludedIds(current=>current.filter(x=>x!==id));if(requiresSize&&!hasSize){focusStorySize(id);return}setSelectedIds(current=>current.includes(id)?current:[...current,id]);return}if(requiresSize&&!hasSize){setStoryExcludedIds(current=>current.includes(id)?current:[...current,id]);return}setSelectedIds(current=>current.includes(id)?current:[...current,id])};'''
if toggle_helpers not in text:
    if toggle_marker not in text:
        raise SystemExit("toggle marker not found")
    text = text.replace(toggle_marker, toggle_helpers, 1)

add_base = 'const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};'
add_v9 = 'const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length||!storyReady)return;setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};'
add_v10 = 'const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length||!storyReady)return;setStoryBuying(false);setStoryExcludedIds([]);setStory(null);chosen.forEach(addToCart)};'
if add_base in text:
    text = text.replace(add_base, add_v10, 1)
elif add_v9 in text:
    text = text.replace(add_v9, add_v10, 1)
elif add_v10 not in text:
    raise SystemExit("addStory marker not found")

# Inline V8 creates a floating checkbox above ProductCard; remove it and reuse the
# existing quick-add slot so the grid and card geometry do not move.
controls_v8 = r'''{storyBuying&&<button className="luna-story-card-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected} aria-label={selected?`Убрать ${item.name}`:`Добавить ${item.name}`}>{selected?"✓":""}</button>}
          <ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>'''
controls_v9 = r'''<ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={storyBuying} selected={selected} onSelect={()=>toggle(item.id)}/>'''
controls_v10 = r'''{pending&&<span className="luna-story-size-badge">Нужен размер</span>}
          <ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={storyBuying} selected={selected} pending={pending} onSelect={()=>toggleStoryItem(item,requiresSize,Boolean(size))}/>'''
if controls_v8 in text:
    text = text.replace(controls_v8, controls_v10, 1)
elif controls_v9 in text:
    text = text.replace(controls_v9, controls_v10, 1)
elif controls_v10 not in text:
    raise SystemExit("Story ProductCard control marker not found")

# Story card state: multi-size item starts blank/pending and fixed-size items are
# immediately valid. Excluded is an explicit user choice and is not an error.
map_v8 = 'const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell ${storyBuying?(selected?"selected":"not-selected"):""}`} key={`${active.id}-${item.id}`}>'
map_v9 = 'const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??(options.length===1?(options[0]?.[0]??item.selectedSize??""):"");const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell ${storyBuying?(selected?"selected":"not-selected"):""}`} key={`${active.id}-${item.id}`}>'
map_v10 = 'const selected=selectedIds.includes(item.id);const excluded=storyExcludedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const requiresSize=options.length>1;const size=sizes[item.id]??(requiresSize?"":(options[0]?.[0]??item.selectedSize??""));const pending=storyBuying&&requiresSize&&!size&&!excluded;const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell ${storyBuying?(pending?"pending-size":selected?"selected":"excluded"):""}`} key={`${active.id}-${item.id}`}>'
if map_v8 in text:
    text = text.replace(map_v8, map_v10, 1)
elif map_v9 in text:
    text = text.replace(map_v9, map_v10, 1)
elif map_v10 not in text:
    raise SystemExit("Story card state marker not found")

config_v8 = r'''{storyBuying&&<div className="luna-story-card-config">{options.length>1?<label><span>Размер</span><select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select></label>:<span className="luna-story-fixed-size">{size}</span>}<div className="luna-story-card-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div></div>}'''
config_v9 = r'''{storyBuying&&<div className="luna-story-card-config">{options.length>1?<label><span>Размер</span><select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))} aria-label={`Выберите размер ${item.name}`}><option value="" disabled>Выберите размер</option>{options.map(([o])=><option key={o} value={o}>{o}</option>)}</select></label>:<span className="luna-story-fixed-size">{size}</span>}<div className="luna-story-card-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div></div>}'''
config_v10 = r'''{storyBuying&&<><div className={`luna-story-card-config ${pending?"has-error":""}`}>{requiresSize?<label><span>Размер</span><select id={`story-size-${item.id}`} value={size} aria-invalid={pending} onChange={e=>{const value=e.target.value;setSizes(current=>({...current,[item.id]:value}));setStoryExcludedIds(current=>current.filter(x=>x!==item.id));setSelectedIds(current=>current.includes(item.id)?current:[...current,item.id])}} aria-label={`Выберите размер ${item.name}`}><option value="" disabled>Выберите размер</option>{options.map(([o])=><option key={o} value={o}>{o}</option>)}</select></label>:<span className="luna-story-fixed-size">{size}</span>}{selected&&<div className="luna-story-card-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div>}</div>{pending&&<div className="luna-story-size-error">⚠ Выберите размер, чтобы добавить в набор</div>}</>}'''
if config_v8 in text:
    text = text.replace(config_v8, config_v10, 1)
elif config_v9 in text:
    text = text.replace(config_v9, config_v10, 1)
elif config_v10 not in text:
    raise SystemExit("Story card config marker not found")

footer_v8 = r'''{!storyBuying?<div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div>:<div className="luna-clean-story-buy luna-story-buy-active"><button className="luna-story-buy-cancel" type="button" onClick={()=>setStoryBuying(false)}>ОТМЕНА</button><div className="luna-story-buy-total"><span>{selectedIds.length} {selectedIds.length===1?"товар":"товара"}</span><strong>{fmt(total)}</strong></div><button className="luna-story-buy-add" type="button" disabled={!selectedIds.length} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button></div>}'''
footer_v9 = r'''{!storyBuying?<div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div>:<div className="luna-clean-story-buy luna-story-buy-active"><button className="luna-story-buy-cancel" type="button" onClick={()=>setStoryBuying(false)}>ОТМЕНА</button><div className="luna-story-buy-total"><span>{selectedIds.length} {selectedIds.length===1?"товар":"товара"}</span><strong>{fmt(total)}</strong></div><button className="luna-story-buy-add" type="button" disabled={!selectedIds.length||!storyReady} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button></div>}'''
footer_v10 = r'''{!storyBuying?<div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div>:<div className="luna-clean-story-buy luna-story-buy-active"><button className="luna-story-buy-cancel" type="button" onClick={()=>{setStoryBuying(false);setStoryExcludedIds([])}}>ОТМЕНА</button><div className="luna-story-buy-summary"><div className="luna-story-buy-total"><span><b>{selectedIds.length} из {storyProducts.length}</b> товаров готовы</span><strong>{fmt(total)}</strong></div>{storyPendingIds.length>0&&<div className="luna-story-buy-note">⚠ {pendingStoryProducts[0]?.name}: не выбран размер — не учтён в сумме</div>}{storyPendingIds.length>0&&<div className="luna-story-buy-hint">Выберите размер в карточке выше</div>}</div><button className="luna-story-buy-add" type="button" aria-disabled={!storyReady} onClick={()=>{if(!storyReady){const id=storyPendingIds[0];if(id)focusStorySize(id);return}addStory()}}>{storyPendingIds.length>0?"ВЫБРАТЬ РАЗМЕР, ЧТОБЫ ПРОДОЛЖИТЬ":"ДОБАВИТЬ В КОРЗИНУ"}</button></div>}'''
if footer_v8 in text:
    text = text.replace(footer_v8, footer_v10, 1)
elif footer_v9 in text:
    text = text.replace(footer_v9, footer_v10, 1)
elif footer_v10 not in text:
    raise SystemExit("Story footer marker not found")

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_STORY_CARD_CONTROLS_V9 \*/[\s\S]*?/\* END_LUNA_STORY_CARD_CONTROLS_V9 \*/', '', css)
css = re.sub(r'\n?/\* LUNA_STORY_VALIDATION_V10 \*/[\s\S]*?/\* END_LUNA_STORY_VALIDATION_V10 \*/', '', css)
css += r'''

/* LUNA_STORY_VALIDATION_V10 */
.luna-clean-products.is-buying .product-card>.quick.selection-check{display:grid;place-items:center;border:1px solid #d8d8d5;background:#fff;color:transparent;border-radius:0;font-size:12px;line-height:1;box-shadow:none}
.luna-clean-products.is-buying .product-card>.quick.selection-check.selected{background:#1d1d1f;border-color:#1d1d1f;color:#fff}
.luna-clean-products.is-buying .product-card>.quick.selection-check.pending{background:#fff;border:1px dashed #8a8f98;color:#8a8f98;font-size:10px;font-weight:400}
.luna-story-card-shell{position:relative;min-width:0}
.luna-story-card-shell.excluded>.product-card .product-image,.luna-story-card-shell.excluded>.product-card .product-copy,.luna-story-card-shell.excluded>.product-card>.heart{opacity:.42}
.luna-story-card-shell.pending-size{outline:1px solid #c0392b;outline-offset:0;background:#fff7f6}
.luna-story-size-badge{position:absolute;z-index:7;top:8px;left:8px;padding:3px 7px;background:#c0392b;color:#fff;font-size:9px;line-height:1.2;letter-spacing:.02em}
.luna-story-card-config.has-error select{border-color:#c0392b;color:#c0392b;font-weight:500}
.luna-story-card-config select option{color:#1d1d1f;font-weight:400}
.luna-story-size-error{padding:5px 2px 7px;color:#c0392b;font-size:9px;line-height:1.35}
.luna-story-buy-summary{min-width:0;display:grid;gap:4px}
.luna-story-buy-total{display:flex;align-items:baseline;justify-content:flex-end;gap:9px}.luna-story-buy-total span{font-size:9px;color:#777}.luna-story-buy-total span b{color:#1d1d1f;font-weight:500}.luna-story-buy-total strong{font-size:16px;font-weight:400;white-space:nowrap}
.luna-story-buy-note{color:#c0392b;font-size:9px;line-height:1.25;text-align:right}
.luna-story-buy-hint{color:#8a8f98;font-size:9px;line-height:1.25;text-align:right}
.luna-story-buy-add[aria-disabled="true"]{background:#c9ccd1!important;color:#fff!important;cursor:pointer}
@media(max-width:700px){
  .luna-clean-products.is-buying .product-card>.quick.selection-check{font-size:11px}
  .luna-clean-products.is-buying .product-card>.quick.selection-check.pending{font-size:9px}
  .luna-story-size-badge{top:7px;left:7px;font-size:8px;padding:3px 6px}
  .luna-story-size-error{font-size:8px;padding:4px 0 6px}
  .luna-clean-story-buy.luna-story-buy-active{grid-template-columns:auto 1fr;gap:8px 12px;padding:10px 16px calc(10px + env(safe-area-inset-bottom))}
  .luna-story-buy-summary{min-width:0}.luna-story-buy-total{justify-content:flex-end;gap:7px}.luna-story-buy-total strong{font-size:14px}.luna-story-buy-note,.luna-story-buy-hint{font-size:8px;text-align:right}
  .luna-story-buy-add{grid-column:1/3;height:46px!important;width:100%!important}
}
/* END_LUNA_STORY_VALIDATION_V10 */
'''
css_path.write_text(css, encoding="utf-8")
