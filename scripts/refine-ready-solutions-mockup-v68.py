from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
s = path.read_text(encoding="utf-8")
marker = "READY_SOLUTIONS_MOCKUP_V68"
if marker in s:
    print("V68 already applied")
    raise SystemExit(0)

# Give every wizard step a stable styling hook.
s = s.replace(
    '<div className="rs57-page rs57-wizard-page rs66-zara">',
    '<div className={`rs57-page rs57-wizard-page rs66-zara rs68-wizard rs68-step-${step}`}>',
    1,
)

# The third step is the actual result, not another editorial "look" step.
s = s.replace('value === 2 ? "Состав" : "Образ"', 'value === 2 ? "Состав" : "Результат"', 1)

# Collections on Parameters: visual product/editorial cards with black checkboxes.
pattern = r'<nav className="rs62-filter-rail rs62-collection-rail">\{availableCollections\.map\(\(collection\) => \{.*?\}\)\}</nav>'
replacement = '''<div className="rs68-collection-grid">{availableCollections.map((collection) => { const active=activeCollections.some((value)=>norm(sourceCollectionName(value))===norm(sourceCollectionName(collection))); const preview=catalog.catalog.find((row)=>belongsToCollection(row,collection)&&Boolean(row.primary_image_url))?.primary_image_url || solutionImage(solution,rows); return <button type="button" key={collection} className={`rs68-collection-card ${active?"is-active":""}`} disabled={active&&activeCollections.length===1} onClick={()=>setActiveCollections((current)=>active?current.filter((value)=>norm(sourceCollectionName(value))!==norm(sourceCollectionName(collection))):[...current,collection])}><span className="rs68-collection-media"><RemoteImage src={preview} fallbackSrc="/images/image-placeholder.svg" alt={displayCollectionName(collection)}/><i className="rs68-collection-check">{active?"✓":""}</i></span><strong>{displayCollectionName(collection)}</strong></button>; })}</div>'''
s, count = re.subn(pattern, replacement, s, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("V68 collection rail not found")

# Product size choice becomes a horizontal button rail instead of a select.
old_size = '''{sizes.length > 1 && <label className="v52-inline-size"><span>Размер</span><select value={size} onChange={(event) => onSize(event.target.value)}>{sizes.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>}'''
new_size = '''{sizes.length > 1 && <div className="rs68-size-picker"><span>Размер</span><div>{sizes.map((value) => <button type="button" key={value} className={size===value?"is-active":""} onClick={()=>onSize(value)}>{value}</button>)}</div></div>}'''
if old_size not in s:
    raise RuntimeError("V68 size select not found")
s = s.replace(old_size, new_size, 1)

# Result headline follows the reference mockup and uses the solution name.
s = s.replace(
    '<div><small>ГОТОВЫЙ ОБРАЗ</small><h2>Ваше решение</h2><p>Готовый образ. Цвета уже выбраны; при необходимости замените или удалите предмет.</p></div>',
    '<div><small>ВАШЕ РЕШЕНИЕ</small><h2>{solution.name}</h2><p>Цвет каждого предмета уже выбран. При необходимости измените количество, замените или удалите позицию.</p></div>',
    1,
)

# Add category summary rows under the visual moodboard, as in the reference.
needle = '''            </div>\n            <footer className="rs60-result-total rs61-result-total">'''
insert = '''            </div>\n            <div className="rs68-result-groups">{groups.map((group)=>{const count=selectedRows.filter((item)=>item.group.id===group.id).length;if(!count)return null;return <button type="button" key={group.id} onClick={()=>{setActiveGroup(group.id);setStep(2)}}><span>{group.title} · {count}</span><b>›</b></button>})}<button type="button" className="rs68-edit-composition" onClick={goComposition}>Изменить состав</button></div>\n            <footer className="rs60-result-total rs61-result-total">'''
if needle not in s:
    raise RuntimeError("V68 moodboard footer anchor not found")
s = s.replace(needle, insert, 1)

s = s.replace('>КУПИТЬ РЕШЕНИЕ</button>', '>ДОБАВИТЬ В КОРЗИНУ</button>', 1)

# Mobile dock follows the exact information hierarchy from the supplied mockup.
old_dock = '''<div className="rs57-mobile-dock"><span><small>{selectedRows.length} позиций</small><strong>{money(total)}</strong></span>{step === 1 ? <button type="button" onClick={() => setStep(2)}>К СОСТАВУ</button> : step === 2 ? <button type="button" onClick={() => setStep(3)} disabled={!selectedRows.length}>РЕЗУЛЬТАТ</button> : <button type="button" onClick={addToCart} disabled={!selectedRows.length}>КУПИТЬ</button>}</div>'''
new_dock = '''<div className="rs57-mobile-dock rs68-mobile-dock"><span><small>{step===1?`${activeCollections.length} коллекции · ${selectedRows.length} позиций`:step===2?`Выбрано: ${selectedRows.length}`:`${selectedRows.length} предметов`}</small><strong>{money(total)}</strong></span>{step === 1 ? <button type="button" onClick={() => setStep(2)}>К СОСТАВУ</button> : step === 2 ? <button type="button" onClick={() => setStep(3)} disabled={!selectedRows.length}>ПЕРЕЙТИ К РЕЗУЛЬТАТУ</button> : <button type="button" onClick={addToCart} disabled={!selectedRows.length}>ДОБАВИТЬ В КОРЗИНУ</button>}</div>'''
if old_dock not in s:
    raise RuntimeError("V68 mobile dock not found")
s = s.replace(old_dock, new_dock, 1)

s = s.replace('// READY_SOLUTIONS_COHESIVE_UX_V64', '// READY_SOLUTIONS_COHESIVE_UX_V64\n// READY_SOLUTIONS_MOCKUP_V68', 1)
path.write_text(s, encoding="utf-8")
print("Applied ready solutions mockup V68")
