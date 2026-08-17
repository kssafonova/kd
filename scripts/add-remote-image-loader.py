from pathlib import Path

page_path = Path("app/page.tsx")
page = page_path.read_text(encoding="utf-8")

if 'import { RemoteImage } from "./remote-image";' not in page:
    page = page.replace(
        'import { assetUrl } from "./assets";\n',
        'import { assetUrl } from "./assets";\nimport { RemoteImage } from "./remote-image";\n',
        1,
    )

legacy_scroll_image = '<img key={`${src}-${index}`} src={assetUrl(src)} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>'
remote_scroll_image = '<RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>'
if legacy_scroll_image in page:
    page = page.replace(legacy_scroll_image, remote_scroll_image, 1)

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
