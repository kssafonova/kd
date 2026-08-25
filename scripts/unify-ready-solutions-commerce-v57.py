from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "ready-solutions" / "ready-solutions-client.tsx"
layout_path = root / "app" / "ready-solutions" / "layout.tsx"
page_path = root / "app" / "page.tsx"

# V71 is the active responsive wizard. Keep the landing on the proven V57
# implementation, but route scenario pages to V71 so later migrations cannot
# silently restore the old wizard.
client_path.write_text(
    'export { ReadySolutionsLanding } from "./ready-solutions-v57-client";\nexport { ReadySolutionWizard } from "./ready-solutions-v71-client";\n',
    encoding="utf-8",
)

layout = layout_path.read_text(encoding="utf-8")
if 'ready-solutions-v57.css' not in layout:
    layout = layout.replace(
        'import "./ready-solutions.css";',
        'import "./ready-solutions.css";\nimport "./ready-solutions-v57.css";',
    )
if 'ready-solutions-v71.css' not in layout:
    layout = layout.replace(
        'import "./ready-solutions-v57.css";',
        'import "./ready-solutions-v57.css";\nimport "./ready-solutions-v71.css";',
    )
layout_path.write_text(layout, encoding="utf-8")

page = page_path.read_text(encoding="utf-8")

if 'if(open==="menu")' not in page:
    page = page.replace(
        '    if(open==="favorites")setFavoritesOpen(true);',
        '    if(open==="favorites")setFavoritesOpen(true);\n    if(open==="menu"){setMenuSection("");setMenu(true)}\n    if(open==="boutiques")setBoutiquesOpen(true);',
    )

if 'const requestedCollection=params.get("collection")' not in page:
    page = page.replace(
        '    const open=params.get("open");',
        '    const open=params.get("open");\n    const requestedCollection=params.get("collection");',
    )
    page = page.replace(
        '    if(section==="collections")setView("collections");',
        '''    if(section==="collections")setView("collections");
    if(requestedCollection){
      const key=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
      const aliases:Record<string,string>={"мокоши":"Символы","камея":"Эхо","жар-птица":"Феникс","жар птица":"Феникс"};
      const requested=aliases[key(requestedCollection)]||requestedCollection;
      const matched=editorials.find(item=>key(item.name)===key(requested));
      if(matched){setEditorial(matched);setView("editorial")}
    }''',
    )
    page = page.replace(
        '    if(section||open)window.history.replaceState({},"",window.location.pathname);',
        '    if(section||open||requestedCollection)window.history.replaceState({},"",window.location.pathname);',
    )

if 'title:"Тёплый брутализм"' not in page:
    page = page.replace(
        '    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/images/products/KD-PD-2000-WHITE01.png",href:`${constructorHref}table-7/`},',
        '    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/images/products/KD-PD-2000-WHITE01.png",href:`${constructorHref}table-7/`},\n    {room:"КАБИНЕТ",title:"Тёплый брутализм",image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a4375b9224e0_big.jpg",href:`${constructorHref}table-8/`},',
    )

page_path.write_text(page, encoding="utf-8")
print("Ready Solutions V71 route preserved during migration")
