from pathlib import Path

page_path = Path("app/page.tsx")
page = page_path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global page
    if new in page:
        return
    if old not in page:
        raise SystemExit(f"{label} not found")
    page = page.replace(old, new, 1)


if 'import { RemoteImage } from "./remote-image";' not in page:
    replace_once(
        'import { assetUrl } from "./assets";\n',
        'import { assetUrl } from "./assets";\nimport { RemoteImage } from "./remote-image";\n',
        "RemoteImage import",
    )

replace_once(
    '<img key={`${src}-${index}`} src={assetUrl(src)} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>',
    '<RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>',
    "Scrollable product media",
)

page = page.replace(
    '<img src={assetUrl(src)} alt=""/>',
    '<RemoteImage src={src} alt=""/>',
)
page = page.replace(
    '<img src={assetUrl(item.image)} alt={item.name}/>',
    '<RemoteImage src={item.image} alt={item.name}/>',
)
page = page.replace(
    '<img src={assetUrl(productImage)} alt={`Предмет из ${editorial.name}`}/>',
    '<RemoteImage src={productImage} alt={`Предмет из ${editorial.name}`}/>',
)

page_path.write_text(page, encoding="utf-8")
print("Remote URL image loader wired into storefront media")
