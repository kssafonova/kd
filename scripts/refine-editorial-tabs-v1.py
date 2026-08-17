from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

replacement = '''function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  const [kind,setKind]=useState<"Истории"|"Готовые решения">("Истории");
  const visible=editorials.filter(item=>kind==="Истории"?item.kind==="КОЛЛЕКЦИЯ":item.kind==="КАПСУЛА");
  return <div className="collections page">
    <div className="section-head"><p>EDITORIAL</p><h1>Истории и готовые решения</h1></div>
    <div className="center-tabs">{(["Истории","Готовые решения"] as const).map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div>
    <div className="collection-grid">{visible.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>{kind==="Истории"?"СМОТРЕТЬ ИСТОРИЮ":"СМОТРЕТЬ РЕШЕНИЕ"} <Icon name="arrow"/></span></div></button></article>)}</div>
  </div>;
}

function LunaEditorialView'''

pattern = r'function CollectionsView\(\{ openEditorial \}: \{ openEditorial:\(editorial:Editorial\)=>void \}\) \{[\s\S]*?\n\}\n\nfunction LunaEditorialView'
text, count = re.subn(pattern, replacement, text, count=1)
if count != 1:
    raise SystemExit("Could not patch CollectionsView")

PAGE.write_text(text, encoding="utf-8")
print("Refined Editorial tabs to Stories / Ready solutions")
