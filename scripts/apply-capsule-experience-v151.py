from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STORY=ROOT/"app"/"story-index.tsx"
CAPSULE_PAGE=ROOT/"app"/"capsules"/"page.tsx"
COLLECTION_PAGE=ROOT/"app"/"collections"/"page.tsx"
MENU=ROOT/"app"/"shared-kultura-menu.tsx"
HOME=ROOT/"app"/"home-standalone.tsx"
EXPERIENCE=ROOT/"app"/"capsule-experience.tsx"
SMOKE=ROOT/"scripts"/"navigation-smoke-v144.cjs"

# The capsule landing is now one focused task: discover a capsule, configure
# variants, and optionally purchase the complete story. Collections are kept
# out of this routing page. /collections remains a compatibility alias only.
STORY.write_text('''import CapsuleExperience from "./capsule-experience";\nimport "./capsule-experience.css";\n\nexport default function StoryIndex(){return <CapsuleExperience/>}\n''',encoding="utf-8")
route='''import StoryIndex from "../story-index";\nexport default function CapsulesPage(){return <StoryIndex/>}\n'''
CAPSULE_PAGE.write_text(route,encoding="utf-8")
COLLECTION_PAGE.write_text(route.replace("CapsulesPage","CollectionsPage"),encoding="utf-8")

menu=MENU.read_text(encoding="utf-8")
menu=menu.replace('aria-label="Капсулы, коллекции и готовые решения"','aria-label="Капсулы и готовые решения"')
menu=menu.replace('onClick={()=>openRoute("/collections/")}><span>КАПСУЛЫ И КОЛЛЕКЦИИ</span>','onClick={()=>openRoute("/capsules/")}><span>КАПСУЛЫ</span>')
MENU.write_text(menu,encoding="utf-8")

home=HOME.read_text(encoding="utf-8")
home=home.replace('/collections/#capsules','/capsules/')
home=home.replace('Все капсулы и коллекции','Все капсулы')
home=home.replace('КАПСУЛЫ И КОЛЛЕКЦИИ','КАПСУЛЫ')
HOME.write_text(home,encoding="utf-8")

experience=EXPERIENCE.read_text(encoding="utf-8")
experience=experience.replace('function skuLabel(sku:CapsuleSku){','function skuLabel(sku:Partial<CapsuleSku>){')
EXPERIENCE.write_text(experience,encoding="utf-8")

# Keep the live-browser smoke aligned with the new product contract. The
# compatibility /collections URL must show the same capsule-only landing.
smoke=SMOKE.read_text(encoding="utf-8")
smoke=smoke.replace('/КАПСУЛЫ И КОЛЛЕКЦИИ/i','/КАПСУЛЫ/i')
smoke=smoke.replace('Unified Kultura menu: capsules and collections action missing','Unified Kultura menu: capsules action missing')
smoke=smoke.replace('Catalog unified menu story action missing','Catalog unified menu capsule action missing')
old='''  // Capsules and collections are one lightweight server-rendered landing. Both\n  // legacy URLs remain valid and expose both groups for backwards compatibility.\n  for(const path of ['/collections/','/capsules/']){\n    await goto(path,'.story-index-page');\n    assert((await page.locator('.section-head h1').innerText()).includes('Капсулы и коллекции'),`${path}: combined title missing`);\n    assert(await page.locator('#capsules').count()===1,`${path}: capsules section missing`);\n    assert(await page.locator('#collections').count()===1,`${path}: collections section missing`);\n    assert(await page.locator('#capsules a[href*="capsule="]').count()>=3,`${path}: capsule cards are not linked`);\n    assert(await page.locator('#collections a[href*="collection="]').count()>=3,`${path}: collection cards are not linked`);\n  }\n'''
new='''  // Capsule routing is now a focused landing. /collections remains a backwards-compatible\n  // alias but must not render a collections index. Clicking a capsule opens the shopping dialog.\n  for(const path of ['/capsules/','/collections/']){\n    await goto(path,'.capsules-v151-page');\n    assert((await page.locator('.capsules-v151-intro h1').innerText()).trim()==='Капсулы',`${path}: capsule-only title missing`);\n    assert(await page.locator('#collections').count()===0,`${path}: collections leaked back into capsule landing`);\n    assert(await page.locator('.capsule-card-v151').count()>=3,`${path}: capsule cards missing`);\n    await page.locator('.capsule-card-v151').first().click();\n    await page.waitForSelector('.capsule-dialog-v151',{state:'visible',timeout:5000});\n    assert(await page.locator('.capsule-gallery-v151 img').count()>=2,`${path}: capsule gallery missing`);\n    assert(await page.locator('.capsule-products-v151 article').count()>=1,`${path}: capsule products missing`);\n    assert(await page.getByRole('button',{name:/ВЫКУПИТЬ ВСЮ КАПСУЛУ|ВЫБЕРИТЕ ВАРИАНТЫ/i}).count()===1,`${path}: capsule purchase CTA missing`);\n    await page.getByRole('button',{name:'Закрыть'}).click();\n  }\n'''
if old in smoke:
    smoke=smoke.replace(old,new,1)
elif '.capsule-dialog-v151' not in smoke:
    raise SystemExit('CAPSULE_V151: expected legacy story smoke block not found')
smoke=smoke.replace("NAVIGATION_SMOKE_V148_OK","NAVIGATION_SMOKE_V151_OK")
SMOKE.write_text(smoke,encoding="utf-8")

if "КАПСУЛЫ И КОЛЛЕКЦИИ" in MENU.read_text(encoding="utf-8"):
    raise SystemExit("CAPSULE_V151: legacy combined menu label remains")
if '#collections' in STORY.read_text(encoding="utf-8"):
    raise SystemExit("CAPSULE_V151: collections section remains on story landing")
print("CAPSULE_EXPERIENCE_V151_OK")
