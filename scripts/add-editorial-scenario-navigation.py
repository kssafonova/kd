from pathlib import Path
import re

path = Path("app/page.tsx")
page = path.read_text(encoding="utf-8")

import_line = 'import { EditorialScenarioLanding } from "./editorial-scenario-landing";\n'
if import_line not in page:
    anchor = 'import { catalogProductOverrides, type CatalogSku } from "./catalog-data";\n'
    if anchor not in page:
        raise SystemExit("page import anchor not found")
    page = page.replace(anchor, anchor + import_line, 1)

replacement = r'''function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  return <EditorialScenarioLanding
    collections={editorials}
    openCollection={(item)=>{
      const selected=editorials.find(editorial=>editorial.id===item.id);
      if(selected)openEditorial(selected);
    }}
  />;
}'''

pattern = r'function CollectionsView\([\s\S]*?\n}\n\nfunction LunaEditorialView'
if not re.search(pattern, page):
    raise SystemExit("CollectionsView block not found")

page = re.sub(pattern, replacement + "\n\nfunction LunaEditorialView", page, count=1)
path.write_text(page, encoding="utf-8")
print("Applied Editorial tabs and scenario navigation")
