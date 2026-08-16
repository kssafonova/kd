from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

old_code = '<small className="pdp-code">АРТИКУЛ: {sku?.id??product.article??`KD-PD-${1020+product.id}`}</small>'
new_code = '<small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}{sku&&<> · SKU: {sku.id}</>}</small>'
if old_code in text:
    text = text.replace(old_code, new_code, 1)

old_specs = '''  {title:"ХАРАКТЕРИСТИКИ",content:<><p>{specs?`${specs.material}. ${specs.size}.`:"Натуральные материалы, деликатная отделка и производство с вниманием к деталям."}</p><dl>{specs&&<><div><dt>Материал</dt><dd>{specs.material}</dd></div><div><dt>Состав</dt><dd>{specs.composition}</dd></div><div><dt>Высота</dt><dd>{specs.height}</dd></div><div><dt>Ширина</dt><dd>{specs.width}</dd></div></>}<div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>},'''
new_specs = '''  {title:"ХАРАКТЕРИСТИКИ",content:specs?<><p>{specs.collection?`${specs.material}. ${specs.size}. Коллекция «${specs.collection}».`:`${specs.material}. ${specs.size}.`}</p><dl><div><dt>Материал</dt><dd>{specs.material}</dd></div><div><dt>Состав</dt><dd>{specs.composition}</dd></div>{specs.height&&<div><dt>Высота</dt><dd>{specs.height}</dd></div>}{specs.width&&<div><dt>Ширина</dt><dd>{specs.width}</dd></div>}{specs.diameter&&<div><dt>Диаметр</dt><dd>{specs.diameter}</dd></div>}{specs.packageInfo&&<div><dt>Комплектация</dt><dd>{specs.packageInfo}</dd></div>}{specs.details&&<div><dt>Детали</dt><dd>{specs.details}</dd></div>}{specs.collection&&<div><dt>Коллекция</dt><dd>{specs.collection}</dd></div>}</dl></>:<p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p>},'''
if old_specs in text:
    text = text.replace(old_specs, new_specs, 1)
elif new_specs not in text:
    raise SystemExit("Product characteristics block was not found")

path.write_text(text, encoding="utf-8")
print("Synced workbook product characteristics to PDP")
