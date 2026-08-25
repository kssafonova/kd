from pathlib import Path

root = Path(__file__).resolve().parents[1]
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
ready_css_path = root / "app" / "ready-solutions" / "ready-solutions-v57.css"
page_path = root / "app" / "page.tsx"
collections_css_path = root / "app" / "unified-stories-v52.css"

ready = ready_path.read_text(encoding="utf-8")
ready_css = ready_css_path.read_text(encoding="utf-8")
page = page_path.read_text(encoding="utf-8")
collections_css = collections_css_path.read_text(encoding="utf-8")

# Collection -> Ready Solutions context. This is intentionally not a fourth
# permanent filter: it appears only when the customer enters from a collection.
if "COLLECTION_CONTEXT_V58" not in ready:
    ready = ready.replace(
        '  const [category, setCategory] = useState("all");',
        '''  const [category, setCategory] = useState("all");
  // COLLECTION_CONTEXT_V58
  const [collectionContext, setCollectionContext] = useState("");
  useEffect(() => {
    const requested = new URLSearchParams(window.location.search).get("collection") || "";
    setCollectionContext(requested);
  }, []);''',
        1,
    )
    ready = ready.replace(
        '  const visible = cards.filter((card) => (space === "all" || card.solution.space === space) && (guests === "all" || card.guestOptions.includes(Number(guests))) && (category === "all" || card.groups.some((group) => group.title === category)));',
        '  const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(value) === norm(collectionContext))) && (space === "all" || card.solution.space === space) && (guests === "all" || card.guestOptions.includes(Number(guests))) && (category === "all" || card.groups.some((group) => group.title === category)));',
        1,
    )
    ready = ready.replace(
        '        {visible.length ? <div className="rs57-solution-grid">',
        '''        {collectionContext && <div className="rs57-context-filter"><span>Коллекция</span><b>{collectionContext}</b><button type="button" onClick={() => setCollectionContext("")}>Снять фильтр</button></div>}
        {visible.length ? <div className="rs57-solution-grid">''',
        1,
    )

if "COLLECTION_CONTEXT_STYLE_V58" not in ready_css:
    ready_css += r'''

/* COLLECTION_CONTEXT_STYLE_V58 — contextual bridge from collection stories. */
.rs57-context-filter{display:flex;align-items:center;gap:10px;margin:-12px 0 26px;padding:11px 0;border-bottom:1px solid var(--rs-line);font-size:9px}
.rs57-context-filter>span{color:#858680;text-transform:uppercase;letter-spacing:.1em}
.rs57-context-filter>b{font-weight:400;font-size:11px}
.rs57-context-filter>button{margin-left:auto;padding-bottom:3px;border-bottom:1px solid #777873;color:#666761;font-size:9px}
@media(max-width:760px){.rs57-context-filter{margin:-8px 0 22px}.rs57-context-filter>b{font-size:10px}}
'''

# Current editorial titles are customer-facing names while solution data keeps the
# source collection names. Map only the renamed collections; all other names pass through.
if "READY_SOLUTION_COLLECTION_BRIDGE_V58" not in page:
    page = page.replace(
        '  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};',
        '''  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};
  // READY_SOLUTION_COLLECTION_BRIDGE_V58
  const readySolutionCollection=active?({"Символы":"Мокоши","Эхо":"Камея","Феникс":"Жар-птица"} as Record<string,string>)[active.name]||active.name:"";
  const readySolutionHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/?collection=${encodeURIComponent(readySolutionCollection)}`;''',
        1,
    )
    page = page.replace(
        '<div className="v52-story-note"><small>О КОЛЛЕКЦИИ</small><p>{active.description}</p></div>',
        '<div className="v52-story-note"><small>О КОЛЛЕКЦИИ</small><p>{active.description}</p><a className="v52-buy-story v58-ready-solution-link" href={readySolutionHref}>СОБРАТЬ ГОТОВОЕ РЕШЕНИЕ →</a></div>',
        1,
    )

if "READY_SOLUTION_COLLECTION_LINK_STYLE_V58" not in collections_css:
    collections_css += r'''

/* READY_SOLUTION_COLLECTION_LINK_STYLE_V58 */
.v58-ready-solution-link{display:inline-flex!important;align-items:center;justify-content:center;width:max-content;min-width:230px;margin-top:30px;text-decoration:none}
@media(max-width:820px){.v58-ready-solution-link{width:100%;min-width:0;margin-top:24px}}
'''

ready_path.write_text(ready, encoding="utf-8")
ready_css_path.write_text(ready_css, encoding="utf-8")
page_path.write_text(page, encoding="utf-8")
collections_css_path.write_text(collections_css, encoding="utf-8")
print("Collections ↔ Ready Solutions V58 bridge applied")
