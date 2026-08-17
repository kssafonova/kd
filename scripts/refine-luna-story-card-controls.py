from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
text = page_path.read_text(encoding="utf-8")

# Reuse the existing quick-add slot in ProductCard as a checkbox while a story is in selection mode.
old_sig = 'function ProductCard({ product, onClick, onQuick, favorite, liked }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean }) {'
new_sig = 'function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; onSelect?:()=>void }) {'
if old_sig in text:
    text = text.replace(old_sig, new_sig, 1)
elif new_sig not in text:
    raise SystemExit("ProductCard signature marker not found")

old_quick = '<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>'
new_quick = '{selectionMode?<button className={`quick selection-check ${selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{selected?"✓":""}</button>:<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>}'
if old_quick in text:
    text = text.replace(old_quick, new_quick, 1)
elif new_quick not in text:
    raise SystemExit("ProductCard quick control marker not found")

# Reset story size choices on every fresh entry into purchase mode so the selector starts neutral.
old_start = 'const startStoryPurchase=()=>{if(!active)return;setSelectedIds(active.productIds);setStoryBuying(true)};'
new_start = 'const startStoryPurchase=()=>{if(!active)return;setSelectedIds(active.productIds);setSizes(current=>{const next={...current};active.productIds.forEach(id=>delete next[id]);return next});setStoryBuying(true)};'
if old_start in text:
    text = text.replace(old_start, new_start, 1)
elif new_start not in text:
    raise SystemExit("startStoryPurchase marker not found")

# Require an explicit size for selected products that have multiple sizes.
story_products_marker = '  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];'
story_ready = story_products_marker + '\n  const storyReady=storyProducts.filter(item=>selectedIds.includes(item.id)).every(item=>{const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);return options.length<=1||Boolean(sizes[item.id])});'
if story_ready not in text:
    if story_products_marker not in text:
        raise SystemExit("storyProducts marker not found")
    text = text.replace(story_products_marker, story_ready, 1)

old_add_story = 'const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};'
new_add_story = 'const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length||!storyReady)return;setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};'
if old_add_story in text:
    text = text.replace(old_add_story, new_add_story, 1)
elif new_add_story not in text:
    raise SystemExit("addStory marker not found")

# Keep exactly the same product grid/card layout. The ProductCard itself swaps cart button -> checkbox.
old_controls = r'''{storyBuying&&<button className="luna-story-card-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected} aria-label={selected?`Убрать ${item.name}`:`Добавить ${item.name}`}>{selected?"✓":""}</button>}
          <ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>'''
new_controls = r'''<ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={storyBuying} selected={selected} onSelect={()=>toggle(item.id)}/>'''
if old_controls in text:
    text = text.replace(old_controls, new_controls, 1)
elif new_controls not in text:
    raise SystemExit("Story ProductCard control marker not found")

# In the story purchase grid, do not preselect the first size when multiple sizes exist.
old_size = 'const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell'
new_size = 'const size=sizes[item.id]??(options.length===1?(options[0]?.[0]??item.selectedSize??""):"");const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell'
if old_size in text:
    text = text.replace(old_size, new_size, 1)
elif new_size not in text:
    raise SystemExit("Story size state marker not found")

old_select = '<select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select>'
new_select = '<select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))} aria-label={`Выберите размер ${item.name}`}><option value="" disabled>Выберите размер</option>{options.map(([o])=><option key={o} value={o}>{o}</option>)}</select>'
# Replace only the first occurrence inside the story card controls; builder selectors stay unchanged.
if old_select in text:
    text = text.replace(old_select, new_select, 1)
elif new_select not in text:
    raise SystemExit("Story size select marker not found")

old_disabled = 'disabled={!selectedIds.length} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button>'
new_disabled = 'disabled={!selectedIds.length||!storyReady} onClick={addStory}>ДОБАВИТЬ В КОРЗИНУ</button>'
if old_disabled in text:
    text = text.replace(old_disabled, new_disabled, 1)
elif new_disabled not in text:
    raise SystemExit("Story footer button marker not found")

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_STORY_CARD_CONTROLS_V9 \*/[\s\S]*?/\* END_LUNA_STORY_CARD_CONTROLS_V9 \*/', '', css)
css += r'''

/* LUNA_STORY_CARD_CONTROLS_V9 */
.luna-clean-products.is-buying .product-card>.quick.selection-check{display:grid;place-items:center;border:1px solid #1d1d1f;background:#fff;color:#fff;border-radius:0;font-size:12px;line-height:1;box-shadow:none}
.luna-clean-products.is-buying .product-card>.quick.selection-check.selected{background:#1d1d1f;color:#fff}
.luna-story-card-shell.not-selected>.product-card{opacity:1}
.luna-story-card-shell.not-selected>.product-card .product-image,.luna-story-card-shell.not-selected>.product-card .product-copy,.luna-story-card-shell.not-selected>.product-card>.heart{opacity:.42}
.luna-story-card-config select:invalid{color:#777}
.luna-story-card-config select option{color:#1d1d1f}
@media(max-width:700px){.luna-clean-products.is-buying .product-card>.quick.selection-check{font-size:11px}}
/* END_LUNA_STORY_CARD_CONTROLS_V9 */
'''
css_path.write_text(css, encoding="utf-8")
