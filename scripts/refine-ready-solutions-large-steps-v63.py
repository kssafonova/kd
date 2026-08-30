from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
text = path.read_text(encoding="utf-8")

marker = "READY_SOLUTIONS_LARGE_STEPS_V63"
if marker in text:
    print("Ready Solutions V63 already applied")
    raise SystemExit(0)

text = text.replace("// READY_SOLUTIONS_PREMIUM_FILTERS_V62", "// READY_SOLUTIONS_PREMIUM_FILTERS_V62\n// READY_SOLUTIONS_LARGE_STEPS_V63", 1)
text = text.replace('className="rs57-stepper" aria-label="Этапы готового решения"', 'className="rs57-stepper rs63-stepper" aria-label="Этапы готового решения"', 1)
text = text.replace('className="rs57-stage rs57-parameters rs61-parameters rs62-parameters"', 'className="rs57-stage rs57-parameters rs61-parameters rs62-parameters rs63-parameters"', 1)

start = text.index('      {step === 3 && <div className="rs57-stage rs57-result-stage rs60-result-stage rs61-result-stage">')
end = text.index('\n    </main>', start)

result_block = '''      {step === 3 && <div className="rs57-stage rs57-result-stage rs60-result-stage rs61-result-stage rs63-result-stage">
        <section className="rs60-result-main rs61-result-main">
          <header className="rs57-stage-head rs60-result-head rs63-result-head">
            <div><small>ШАГ 3 ИЗ 3</small><h2>Результат</h2><p>Финальный moodboard решения. Цвет каждого товара уже зафиксирован на выборе из шага «Состав» — здесь остаётся только собранный образ.</p></div>
            <div className="rs63-result-head-summary"><span>{selectedRows.length} позиций · {activeCollections.length} коллекций</span><strong>{money(total)}</strong></div>
          </header>
          {selectedRows.length ? <section className="rs61-moodboard" aria-label="Финальный moodboard выбранных товаров">
            <div className="rs61-moodboard-grid">
              {selectedRows.map(({ row, quantity, option, group }, index) => { const finalColor = colors[option.id] || row.color || ""; return <article className={`product-card rs61-moodboard-card rs61-mood-${index % 7}`} key={`mood-${option.id}-${row.offer_id}`}>
                <div className="product-image rs61-moodboard-media"><RemoteImage src={rowImages(row)[0] || "/assets/images/image-placeholder.svg"} fallbackSrc="/assets/images/image-placeholder.svg" alt={`${option.title}${finalColor ? `, цвет ${finalColor}` : ""}`}/></div>
                <div className="product-copy rs61-moodboard-copy"><div className="product-link"><strong>{option.title}</strong><small>{[displayCollectionName(option.collection || row.collection || ""), row.size || row.volume].filter(Boolean).join(" · ")}</small></div>{finalColor && <div className="rs63-final-color" aria-label={`Выбранный цвет ${finalColor}`}><i style={{ background: swatchColor(finalColor) }}/><span>{finalColor}</span></div>}<span className="price">{money(priceOf(row))}</span></div>
                <div className="rs61-moodboard-controls"><div className="rs61-qty"><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: Math.max(1, quantity - 1) }))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={() => setQty((current) => ({ ...current, [option.id]: quantity + 1 }))} aria-label="Увеличить количество">+</button></div><div className="rs61-card-actions"><button type="button" onClick={() => startReplace(option, group)}>Заменить</button><button type="button" onClick={() => removeItem(option.id)}>Удалить</button></div></div>
              </article>})}
              <button type="button" className="product-card rs61-add-card" onClick={goComposition}><span>+</span><strong>Добавить предмет</strong><small>Вернуться к составу решения</small></button>
            </div>
            <footer className="rs60-result-total rs61-result-total"><div><span>{selectedRows.length} позиций · выбранные цвета сохранены</span><strong>{money(total)}</strong></div><button type="button" className="rs57-primary" onClick={addToCart}>ДОБАВИТЬ ВСЁ В КОРЗИНУ</button></footer>
          </section> : <div className="rs57-empty-result"><h3>В решении пока нет товаров</h3><button type="button" onClick={goComposition}>Добавить предмет</button></div>}
        </section>
      </div>}'''

text = text[:start] + result_block + text[end:]
path.write_text(text, encoding="utf-8")
print("Ready Solutions V63 applied")
