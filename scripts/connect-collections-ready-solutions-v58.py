from pathlib import Path

root = Path(__file__).resolve().parents[1]
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
page_path = root / "app" / "page.tsx"

ready = ready_path.read_text(encoding="utf-8")
page = page_path.read_text(encoding="utf-8")

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

ready_path.write_text(ready, encoding="utf-8")
page_path.write_text(page, encoding="utf-8")
print("Collections ↔ Ready Solutions V58 bridge applied")
