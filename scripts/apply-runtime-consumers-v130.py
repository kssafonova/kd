from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "app" / "truth-commerce-enhancer.tsx"

text = TRUTH.read_text(encoding="utf-8")
marker = "// SITE_DATABASE_RUNTIME_CONSUMER_V130"
if marker not in text:
    pattern = r'function useTruth\(\)\{const\[d,setD\]=useState<D\|null>\(null\);useEffect\(\(\)=>\{.*?;return d\}'
    replacement = 'function useTruth(){const[d,setD]=useState<D|null>(null);useEffect(()=>{let ok=true;fetch(`${BASE}/data/database/site_runtime.json`,{cache:"no-store"}).then(async r=>{if(!r.ok)throw 0;return r.json() as Promise<D>}).then(x=>{if(ok)setD(x)}).catch(()=>{});return()=>{ok=false}},[]);return d}'
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("SITE_DATABASE_RUNTIME_CONSUMER_V130: useTruth signature not found")
    text = text.replace('import { useEffect, useMemo, useState } from "react";', 'import { useEffect, useMemo, useState } from "react";\n' + marker, 1)
    text = text.replace("КАТАЛОГ · XLSX TRUTH", "КАТАЛОГ")
    text = text.replace("ГОТОВЫЕ РЕШЕНИЯ · XLSX TRUTH", "ГОТОВЫЕ РЕШЕНИЯ")
    text = text.replace("синхронизированы с XLSX", "синхронизированы с базой данных")
    # Keep the full modern catalog underneath: its sorting/filter UX already reads
    # the normalized 01/02/18/19 database tables through site-database.generated.ts.
    # The truth enhancer continues to own home, collections and ready solutions,
    # but must not hide the catalog controls.
    old_catalog_host = 'setC(host(document.querySelector<HTMLElement>("main.catalog.page"),"truth-catalog-host"));'
    if old_catalog_host in text:
        text = text.replace(old_catalog_host, 'setC(null);', 1)
TRUTH.write_text(text, encoding="utf-8")
print("// SITE_DATABASE_RUNTIME_CONSUMER_V130: home/collections/ready-solutions use database runtime; modern filtered catalog remains active")
