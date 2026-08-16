from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text()
css = css_path.read_text()

state_old = '  const [open,setOpen]=useState("");\n'
state_new = '  const [open,setOpen]=useState("");\n  const [storesOpen,setStoresOpen]=useState(false);\n'
if state_old not in page:
    raise SystemExit("ProductView open state marker not found")
page = page.replace(state_old, state_new, 1)

replacement = '''<button className="pdp-stores-button" onClick={()=>setStoresOpen(true)} aria-label="Показать наличие в бутиках"><span><Icon name="pin"/>НАЛИЧИЕ В МАГАЗИНАХ</span><Icon name="chevron"/></button><div className="pdp-accordions">{[
  {title:"ИНФОРМАЦИЯ О ТОВАРЕ",content:<><p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p><dl><div><dt>Состав</dt><dd>Хлопок / лён</dd></div><div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>},
  {title:"ДОСТАВКА",content:<><p>Бесплатная доставка при заказе от 15 000 ₽. Доступны курьерская доставка и самовывоз из бутика.</p><small>Срок и доступные способы рассчитываются при оформлении заказа.</small></>},
  {title:"ВОЗВРАТ",content:<><p>Возврат товара надлежащего качества возможен в течение 14 дней при сохранении товарного вида и комплектации.</p><small>Для отдельных категорий могут действовать специальные условия возврата.</small></>}
].map(section=><section className={`pdp-accordion-item ${open===section.title?"open":""}`} key={section.title}><button className="pdp-accordion-trigger" onClick={()=>setOpen(open===section.title?"":section.title)} aria-expanded={open===section.title}><span>{section.title}</span><Icon name="chevron"/></button>{open===section.title&&<div className="pdp-accordion-panel">{section.content}</div>}</section>)}</div>'''

pattern = re.compile(r'(<button className="primary purchase-cta total-cta".*?</button>)<div className="pdp-service-links">.*?\{open&&<p className="service-copy">.*?</p>\}', re.S)
page, count = pattern.subn(r'\1' + replacement, page, count=1)
if count != 1:
    raise SystemExit(f"Service links replacement failed: {count}")

end_old = '<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite}/></div>;\n}\n\nfunction RichContent'
end_new = '''<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite}/>{storesOpen&&<BoutiqueMap close={()=>setStoresOpen(false)}/>}</div>;
}

function BoutiqueMap({close}:{close:()=>void}){
  const boutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124}
  ];
  const [selected,setSelected]=useState(0);
  const boutique=boutiques[selected];
  const delta=.035;
  const mapSrc=`https://www.openstreetmap.org/export/embed.html?bbox=${boutique.lon-delta}%2C${boutique.lat-delta}%2C${boutique.lon+delta}%2C${boutique.lat+delta}&layer=mapnik&marker=${boutique.lat}%2C${boutique.lon}`;
  return <div className="boutique-map-overlay" role="dialog" aria-modal="true" aria-label="Наличие в магазинах"><button className="boutique-map-backdrop" onClick={close} aria-label="Закрыть карту"/><section className="boutique-map-modal"><header><div><small>НАЛИЧИЕ В МАГАЗИНАХ</small><h2>Бутики Культура дома</h2></div><button className="boutique-map-close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header><div className="boutique-map-body"><aside>{boutiques.map((item,index)=><button key={item.city} className={index===selected?"active":""} onClick={()=>setSelected(index)}><span><Icon name="pin"/><b>{item.city}</b></span><strong>{item.address}</strong><small>{item.hours}</small><i>{index===selected?"На карте":"Показать на карте"}</i></button>)}</aside><div className="boutique-map-canvas"><iframe key={`${boutique.city}-${selected}`} src={mapSrc} title={`Карта бутика — ${boutique.city}`} loading="lazy"/><div className="boutique-map-caption"><div><b>{boutique.city}</b><span>{boutique.address}</span></div><small>{boutique.hours}</small></div></div></div></section></div>;
}

function RichContent'''
if end_old not in page:
    raise SystemExit("ProductView ending marker not found")
page = page.replace(end_old, end_new, 1)

marker = '/* PDP ACCORDIONS + BOUTIQUE MAP */'
styles = '''

/* PDP ACCORDIONS + BOUTIQUE MAP */
.pdp-stores-button{width:100%;min-height:48px;margin:10px 0 0;border:1px solid #252726;padding:0 14px;display:flex;align-items:center;justify-content:space-between;font-size:9px;letter-spacing:.09em;text-transform:uppercase;background:#fff;transition:background .2s,color .2s}
.pdp-stores-button:hover{background:#f4f2ed}.pdp-stores-button>span{display:flex;align-items:center;gap:9px}.pdp-stores-button svg{width:18px;height:18px}.pdp-stores-button>svg:last-child{width:15px;height:15px}
.pdp-accordions{margin-top:14px;border-top:1px solid var(--line)}.pdp-accordion-item{border-bottom:1px solid var(--line)}.pdp-accordion-trigger{width:100%;min-height:49px;padding:0 2px;display:flex;align-items:center;justify-content:space-between;text-align:left;font-size:9px;letter-spacing:.08em}.pdp-accordion-trigger svg{width:16px;height:16px;transition:transform .2s}.pdp-accordion-item.open .pdp-accordion-trigger svg{transform:rotate(90deg)}
.pdp-accordion-panel{padding:0 3px 18px;color:#545653;font-size:10px;line-height:1.65}.pdp-accordion-panel p{margin:0 0 12px}.pdp-accordion-panel small{display:block;color:#777;line-height:1.55}.pdp-accordion-panel dl{margin:0}.pdp-accordion-panel dl>div{display:flex;justify-content:space-between;gap:18px;padding:6px 0;border-top:1px solid #eee}.pdp-accordion-panel dt,.pdp-accordion-panel dd{margin:0}.pdp-accordion-panel dd{text-align:right;color:#242625}
.boutique-map-overlay{position:fixed;inset:0;z-index:240;display:flex;align-items:center;justify-content:center;padding:24px}.boutique-map-backdrop{position:absolute;inset:0;background:rgba(14,16,15,.58)}.boutique-map-modal{position:relative;z-index:1;width:min(1080px,calc(100vw - 48px));height:min(700px,calc(100vh - 48px));background:#fff;display:flex;flex-direction:column;box-shadow:0 24px 80px rgba(0,0,0,.28);overflow:hidden}.boutique-map-modal>header{height:86px;flex:0 0 86px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;border-bottom:1px solid var(--line)}.boutique-map-modal>header small{display:block;font-size:8px;letter-spacing:.16em;color:#777;margin-bottom:7px}.boutique-map-modal>header h2{margin:0;font:400 25px/1 var(--serif)}.boutique-map-close{width:38px;height:38px;display:grid;place-items:center}.boutique-map-close svg{width:22px;height:22px}
.boutique-map-body{min-height:0;flex:1;display:grid;grid-template-columns:310px 1fr}.boutique-map-body>aside{overflow:auto;border-right:1px solid var(--line);padding:8px 0}.boutique-map-body>aside>button{width:100%;text-align:left;padding:20px 22px;border-bottom:1px solid #eee;display:flex;flex-direction:column;gap:7px;position:relative}.boutique-map-body>aside>button.active{background:#f3f1ec}.boutique-map-body>aside>button>span{display:flex;align-items:center;gap:8px}.boutique-map-body>aside>button svg{width:17px;height:17px}.boutique-map-body>aside b{font-size:11px;letter-spacing:.04em}.boutique-map-body>aside strong{font:400 18px var(--serif)}.boutique-map-body>aside small{font-size:9px;color:#777}.boutique-map-body>aside i{font-style:normal;font-size:8px;letter-spacing:.08em;text-transform:uppercase;margin-top:6px;text-decoration:underline;text-underline-offset:4px}.boutique-map-canvas{position:relative;min-width:0;background:#e9ebe7}.boutique-map-canvas iframe{width:100%;height:100%;border:0;display:block}.boutique-map-caption{position:absolute;left:18px;right:18px;bottom:18px;background:rgba(255,255,255,.95);backdrop-filter:blur(8px);padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:18px;box-shadow:0 4px 25px rgba(0,0,0,.12)}.boutique-map-caption>div{display:flex;flex-direction:column;gap:3px}.boutique-map-caption b{font-size:10px;text-transform:uppercase}.boutique-map-caption span,.boutique-map-caption small{font-size:9px;color:#666}
@media(max-width:900px){.pdp-stores-button{min-height:46px;font-size:8px;margin-top:9px}.pdp-accordions{margin-top:12px}.pdp-accordion-trigger{min-height:46px;font-size:8px}.pdp-accordion-panel{font-size:9px;padding-bottom:16px}.boutique-map-overlay{padding:0;align-items:flex-end}.boutique-map-modal{width:100%;height:92vh;max-height:none;border-radius:14px 14px 0 0}.boutique-map-modal>header{height:68px;flex-basis:68px;padding:0 15px}.boutique-map-modal>header h2{font-size:19px}.boutique-map-body{display:flex;flex-direction:column}.boutique-map-body>aside{display:flex;flex:0 0 auto;border-right:0;border-bottom:1px solid var(--line);overflow-x:auto;padding:0}.boutique-map-body>aside>button{min-width:72vw;padding:14px 15px;border-bottom:0;border-right:1px solid #eee}.boutique-map-body>aside strong{font-size:15px}.boutique-map-canvas{flex:1;min-height:340px}.boutique-map-caption{left:10px;right:10px;bottom:10px;padding:11px 12px}}
'''
if marker not in css:
    css += styles

page_path.write_text(page)
css_path.write_text(css)
