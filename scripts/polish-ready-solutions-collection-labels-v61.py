from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-v57-client.tsx"
text = path.read_text(encoding="utf-8")

if "READY_SOLUTIONS_COLLECTION_LABELS_V61" in text:
    print("Ready Solutions collection labels already polished")
    raise SystemExit(0)

if "READY_SOLUTIONS_CATALOG_MOODBOARD_V61" not in text:
    raise RuntimeError("V61 must be applied before label polish")

text = text.replace(
    'const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(value) === norm(collectionContext))) && (space === "all" || card.solution.space === space));',
    'const visible = cards.filter((card) => (!collectionContext || card.solution.collections.some((value) => norm(displayCollectionName(value)) === norm(collectionContext) || norm(sourceCollectionName(value)) === norm(sourceCollectionName(collectionContext)))) && (space === "all" || card.solution.space === space)); // READY_SOLUTIONS_COLLECTION_LABELS_V61',
    1,
)
text = text.replace(
    '<div className="rs57-solution-copy"><small>{solution.space}</small><Link href={`/ready-solutions/${solution.id}/`}><h3>{solution.name}</h3></Link><p>{solution.collections.join(" · ")}</p>',
    '<div className="rs57-solution-copy"><small>{solution.space}</small><Link href={`/ready-solutions/${solution.id}/`}><h3>{solution.name}</h3></Link><p>{solution.collections.map(displayCollectionName).join(" · ")}</p>',
    1,
)
text = text.replace(
    '{collectionContext && <div className="rs57-context-filter"><span>Коллекция</span><b>{collectionContext}</b>',
    '{collectionContext && <div className="rs57-context-filter"><span>Коллекция</span><b>{displayCollectionName(collectionContext)}</b>',
    1,
)
text = text.replace(
    '{collections.map((value) => <option key={value} value={value}>{value}</option>)}',
    '{collections.map((value) => <option key={value} value={value}>{displayCollectionName(value)}</option>)}',
    1,
)

path.write_text(text, encoding="utf-8")
print("Ready Solutions collection labels polished")
