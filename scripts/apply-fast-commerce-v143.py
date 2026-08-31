from pathlib import Path

root=Path(__file__).resolve().parents[1]
app=root/"app"

(app/"page.tsx").write_text('''import {FastHome} from "./fast-commerce";\n\nexport default function HomePage(){return <FastHome/>}\n''',encoding="utf-8")

catalog=app/"catalog"
catalog.mkdir(exist_ok=True)
(catalog/"page.tsx").write_text('''import {FastCatalog} from "../fast-commerce";\n\nexport default function CatalogPage(){return <FastCatalog/>}\n''',encoding="utf-8")
(catalog/"layout.tsx").write_text('''export default function CatalogLayout({children}:{children:React.ReactNode}){return <>{children}</>}\n''',encoding="utf-8")

capsules=app/"capsules"
capsules.mkdir(exist_ok=True)
(capsules/"page.tsx").write_text('''import {FastCapsules} from "../fast-commerce";\n\nexport default function CapsulesPage(){return <FastCapsules/>}\n''',encoding="utf-8")

collections=app/"collections"
collections.mkdir(exist_ok=True)
(collections/"page.tsx").write_text('''import {FastCollections} from "../fast-commerce";\n\nexport default function CollectionsPage(){return <FastCollections/>}\n''',encoding="utf-8")

(app/"layout.tsx").write_text('''import type {Metadata} from "next";\nimport "./globals.css";\nimport "./fast-commerce.css";\n\nexport const metadata:Metadata={title:"Культура дома — премиальные товары для дома",description:"Текстиль, посуда и предметы для дома с русским характером."};\nexport default function RootLayout({children}:{children:React.ReactNode}){return <html lang="ru"><body>{children}</body></html>}\n''',encoding="utf-8")

# Remove the obsolete client entry if the route-split migration recreated it.
legacy_client=catalog/"catalog-client.tsx"
if legacy_client.exists():
    legacy_client.unlink()

print("FAST_COMMERCE_V143: lightweight shared runtime enabled for home/catalog/capsules/collections; heavy catalog enhancers removed")
