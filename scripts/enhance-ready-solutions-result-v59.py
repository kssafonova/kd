from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
css_path = root / "app" / "ready-solutions" / "ready-solutions-v57.css"

client = client_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

marker = "RESULT_MOODBOARD_V59"
if marker not in client:
    old = '''      {step === 3 && <div className="rs57-stage rs57-result-stage">
        <section><header className="rs57-stage-head"><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2><p>Финальный состав остаётся редактируемым. Можно удалить предмет, заменить его другим из той же категории или вернуться к составу и добавить ещё.</p></header>
          {selectedRows.length ? <div className="rs57-result-list">{selectedRows.map(({ row, quantity, option, group }) => <article key={`${option.id}-${row.offer_id}`} className="rs57-result-item"><div className="rs57-result-media"><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div><div className="rs57-result-copy"><small>{group.title}</small><strong>{option.title}</strong><p>{[row.color, row.size || row.volume].filter(Boolean).join(" · ") || "Единый вариант"}</p><span>{money(priceOf(row))}</span></div><div className="rs57-result-qty"><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))}>−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))}>+</button></div><b className="rs57-result-total">{money(priceOf(row) * quantity)}</b><div className="rs57-result-actions"><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></article>)}</div> : <div className="rs57-empty-result"><h3>В решении пока нет товаров</h3><p>Вернитесь к составу и выберите предметы.</p><button type="button" onClick={goComposition}>Выбрать товары</button></div>}
          <button type="button" className="rs57-add-more" onClick={goComposition}>+ Добавить или изменить предметы</button>
        </section>
        <aside className="rs57-summary-card rs57-result-summary"><small>ГОТОВОЕ РЕШЕНИЕ</small><h3>{solution.name}</h3><dl><div><dt>Персон</dt><dd>{guests}</dd></div><div><dt>Позиций</dt><dd>{selectedRows.length}</dd></div><div><dt>Коллекций</dt><dd>{solution.collections.length}</dd></div></dl><footer><span>Итого</span><strong>{money(total)}</strong></footer><button type="button" className="rs57-primary" onClick={addToCart} disabled={!selectedRows.length}>ДОБАВИТЬ В КОРЗИНУ</button><button type="button" className="rs57-save" onClick={saveSolution}>{saved ? "Сохранено ✓" : "Сохранить решение"}</button><p className="rs57-summary-note">Все выбранные товары попадут в общую корзину сайта с выбранными цветами, размерами и количеством.</p></aside>
      </div>}'''

    new = '''      {step === 3 && <div className="rs57-stage rs57-result-stage">
        <section><header className="rs57-stage-head"><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2><p>Сначала оцените решение как цельный образ, затем проверьте точный состав. Любой предмет можно заменить или удалить прямо из результата.</p></header>
          {selectedRows.length ? <>
            {/* RESULT_MOODBOARD_V59 */}
            <section className="rs59-moodboard" aria-labelledby="rs59-moodboard-title">
              <header className="rs59-moodboard-head"><div><small>ВАШЕ ПРОСТРАНСТВО</small><h3 id="rs59-moodboard-title">Собранный образ</h3><p>{selectedRows.length} {selectedRows.length === 1 ? "позиция" : selectedRows.length < 5 ? "позиции" : "позиций"} · {guests} {guests === 1 ? "персона" : guests <= 4 ? "персоны" : "персон"}</p></div><button type="button" onClick={goComposition}>Изменить состав</button></header>
              <div className="rs59-moodboard-grid">
                {selectedRows.slice(0, 4).map(({ row, option, group }, index) => <article className={`rs59-moodboard-tile rs59-tile-${index}`} key={`mood-${option.id}`}><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/><div className="rs59-tile-overlay"><span><small>{group.title}</small><strong>{option.title}</strong></span><div><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></div></article>)}
                <figure className="rs59-moodboard-tile rs59-moodboard-scene"><RemoteImage src={solutionImage(solution, rows)} fallbackSrc="/images/image-placeholder.svg" alt={`${solution.name} — интерьер`}/><figcaption><small>{solution.space}</small><strong>{solution.name}</strong></figcaption></figure>
                {selectedRows.slice(4, 8).map(({ row, option, group }, index) => <article className={`rs59-moodboard-tile rs59-tile-${index + 5}`} key={`mood-${option.id}`}><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/><div className="rs59-tile-overlay"><span><small>{group.title}</small><strong>{option.title}</strong></span><div><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></div></article>)}
                {selectedRows.length > 8 && <button type="button" className="rs59-moodboard-more" onClick={() => document.getElementById("rs59-result-products")?.scrollIntoView({ behavior: "smooth", block: "start" })}><small>ЕЩЁ В РЕШЕНИИ</small><strong>+{selectedRows.length - 8}</strong><span>Смотреть состав</span></button>}
              </div>
              <footer className="rs59-moodboard-footer"><span>Коллекции</span><p>{solution.collections.join(" · ")}</p><strong>{money(total)}</strong></footer>
            </section>

            <section className="rs59-result-products" id="rs59-result-products">
              <header><div><small>СОСТАВ РЕШЕНИЯ</small><h3>Выбранные товары</h3></div><span>{selectedRows.length} позиций</span></header>
              <div className="rs57-result-list">{selectedRows.map(({ row, quantity, option, group }) => <article key={`${option.id}-${row.offer_id}`} className="rs57-result-item"><div className="rs57-result-media"><RemoteImage src={rowImages(row)[0] || "/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div><div className="rs57-result-copy"><small>{group.title}</small><strong>{option.title}</strong><p>{[row.color, row.size || row.volume].filter(Boolean).join(" · ") || "Единый вариант"}</p><span>{money(priceOf(row))}</span></div><div className="rs57-result-qty"><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))}>−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))}>+</button></div><b className="rs57-result-total">{money(priceOf(row) * quantity)}</b><div className="rs57-result-actions"><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></article>)}</div>
            </section>
          </> : <div className="rs57-empty-result"><h3>В решении пока нет товаров</h3><p>Вернитесь к составу и выберите предметы.</p><button type="button" onClick={goComposition}>Выбрать товары</button></div>}
          <button type="button" className="rs57-add-more" onClick={goComposition}>+ Добавить или изменить предметы</button>
        </section>
        <aside className="rs57-summary-card rs57-result-summary"><small>ГОТОВОЕ РЕШЕНИЕ</small><h3>{solution.name}</h3><dl><div><dt>Персон</dt><dd>{guests}</dd></div><div><dt>Позиций</dt><dd>{selectedRows.length}</dd></div><div><dt>Коллекций</dt><dd>{solution.collections.length}</dd></div></dl><footer><span>Итого</span><strong>{money(total)}</strong></footer><button type="button" className="rs57-primary" onClick={addToCart} disabled={!selectedRows.length}>ДОБАВИТЬ В КОРЗИНУ</button><button type="button" className="rs57-save" onClick={saveSolution}>{saved ? "Сохранено ✓" : "Сохранить решение"}</button><p className="rs57-summary-note">Все выбранные товары попадут в общую корзину сайта с выбранными цветами, размерами и количеством.</p></aside>
      </div>}'''

    if old not in client:
        raise SystemExit("V59: result block anchor not found")
    client = client.replace(old, new, 1)

css_marker = "/* RESULT_MOODBOARD_STYLE_V59 */"
if css_marker not in css:
    css += r'''

/* RESULT_MOODBOARD_STYLE_V59 */
.rs59-moodboard{margin:0 0 54px;padding:20px 0 0;border-top:1px solid #1d1d1f}
.rs59-moodboard-head{display:flex;align-items:end;justify-content:space-between;gap:28px;margin-bottom:18px}
.rs59-moodboard-head small,.rs59-result-products>header small{display:block;color:#777873;font-size:8px;letter-spacing:.14em;text-transform:uppercase}
.rs59-moodboard-head h3,.rs59-result-products>header h3{margin:6px 0 4px;font-size:25px;line-height:1.2;font-weight:400}
.rs59-moodboard-head p{margin:0;color:#858680;font-size:9px}
.rs59-moodboard-head>button{padding:0 0 4px;border-bottom:1px solid #1d1d1f;font-size:9px;white-space:nowrap}
.rs59-moodboard-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:stretch}
.rs59-moodboard-tile{position:relative;min-width:0;aspect-ratio:1/1;margin:0;overflow:hidden;background:#f4f3ef}
.rs59-moodboard-tile>img{width:100%;height:100%;display:block;object-fit:cover;transition:transform .45s ease}
.rs59-moodboard-tile:hover>img{transform:scale(1.015)}
.rs59-tile-overlay{position:absolute;inset:auto 0 0;display:flex;align-items:flex-end;justify-content:space-between;gap:14px;padding:36px 12px 11px;background:linear-gradient(transparent,rgba(15,15,14,.58));color:#fff;opacity:0;transition:opacity .22s ease}
.rs59-moodboard-tile:hover .rs59-tile-overlay,.rs59-moodboard-tile:focus-within .rs59-tile-overlay{opacity:1}
.rs59-tile-overlay>span{min-width:0}.rs59-tile-overlay small{display:block;font-size:7px;letter-spacing:.08em;text-transform:uppercase;opacity:.78}.rs59-tile-overlay strong{display:block;margin-top:3px;font-size:11px;line-height:1.25;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rs59-tile-overlay>div{display:flex;gap:9px;flex:0 0 auto}.rs59-tile-overlay button{padding:0 0 2px;border-bottom:1px solid rgba(255,255,255,.8);color:#fff;font-size:8px}.rs59-tile-overlay button:last-child{opacity:.78}
.rs59-moodboard-scene figcaption{position:absolute;left:0;right:0;bottom:0;padding:38px 12px 11px;background:linear-gradient(transparent,rgba(15,15,14,.58));color:#fff}.rs59-moodboard-scene figcaption small{display:block;font-size:7px;letter-spacing:.1em;text-transform:uppercase}.rs59-moodboard-scene figcaption strong{display:block;margin-top:3px;font-size:13px;font-weight:400}
.rs59-moodboard-more{aspect-ratio:1/1;padding:18px;border:1px solid #dddcd7;display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-start;text-align:left;background:#fff}.rs59-moodboard-more small{font-size:7px;letter-spacing:.12em;color:#858680}.rs59-moodboard-more strong{margin:10px 0 18px;font-size:34px;font-weight:400}.rs59-moodboard-more span{font-size:9px;border-bottom:1px solid;padding-bottom:3px}
.rs59-moodboard-footer{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:baseline;padding:13px 0;border-bottom:1px solid var(--rs-line);font-size:9px}.rs59-moodboard-footer>span{color:#858680}.rs59-moodboard-footer p{margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rs59-moodboard-footer strong{font-size:15px;font-weight:400}
.rs59-result-products{scroll-margin-top:150px}
.rs59-result-products>header{display:flex;align-items:end;justify-content:space-between;gap:24px;padding:0 0 14px}.rs59-result-products>header>span{color:#858680;font-size:9px}

@media(max-width:760px){
  .rs59-moodboard{margin-bottom:38px;padding-top:16px}
  .rs59-moodboard-head{display:block;margin-bottom:14px}.rs59-moodboard-head h3{font-size:23px}.rs59-moodboard-head>button{margin-top:12px}
  .rs59-moodboard-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}
  .rs59-moodboard-scene{grid-column:span 2;aspect-ratio:2/1.25}
  .rs59-tile-overlay{opacity:1;padding:34px 8px 8px}.rs59-tile-overlay strong{font-size:9px}.rs59-tile-overlay small{font-size:6px}.rs59-tile-overlay>div{gap:7px}.rs59-tile-overlay button{font-size:7px}
  .rs59-moodboard-scene figcaption{padding:36px 10px 9px}.rs59-moodboard-scene figcaption strong{font-size:11px}
  .rs59-moodboard-more{padding:12px}.rs59-moodboard-more strong{font-size:28px;margin:8px 0 13px}.rs59-moodboard-more span{font-size:8px}
  .rs59-moodboard-footer{grid-template-columns:1fr auto;gap:5px 10px}.rs59-moodboard-footer>span{grid-column:1}.rs59-moodboard-footer p{grid-column:1;grid-row:2}.rs59-moodboard-footer strong{grid-column:2;grid-row:1/3;align-self:center}
  .rs59-result-products>header h3{font-size:22px}.rs59-result-products>header>span{font-size:8px}
}
'''

client_path.write_text(client, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")
print("V59 visual result moodboard applied")
