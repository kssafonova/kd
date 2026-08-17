from pathlib import Path
import re

path = Path("app/page.tsx")
page = path.read_text(encoding="utf-8")

replacement = r'''function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  return <div className="collections page">
    <div className="section-head"><p>EDITORIAL</p><h1>Коллекции и капсулы</h1></div>
    <div className="collection-grid">
      {editorials.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ {item.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ"} <Icon name="arrow"/></span></div></button></article>)}
    </div>
  </div>;
}'''

pattern = r'function CollectionsView\([\s\S]*?\n}\n\nfunction LunaEditorialView'
if not re.search(pattern, page):
    raise SystemExit("CollectionsView block not found")

page = re.sub(pattern, replacement + "\n\nfunction LunaEditorialView", page, count=1)
path.write_text(page, encoding="utf-8")
print("Removed All / Capsules / Collections tabs from editorial landing")
