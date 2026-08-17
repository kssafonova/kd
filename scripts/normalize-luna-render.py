from pathlib import Path

path=Path("app/page.tsx")
text=path.read_text(encoding="utf-8")
current='{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} addToCart={(product)=>add(product,product.selectedSize,product.quantity)} />}'
legacy='{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} />}'
if current in text:
    text=text.replace(current,legacy,1)
path.write_text(text,encoding="utf-8")
print("Normalized Luna editorial render")
