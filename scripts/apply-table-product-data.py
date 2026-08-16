from __future__ import annotations

from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
MEDIA_DIR = ROOT / "public" / "images" / "table-products"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

MEDIA = {
    "kd-pd-1023-white-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000dcb081f78263e374de7b6c4e&ts=496365&p=fs&cid=1&sig=6578dc64f0b53f1732153f68ee757b46979668d4313ce38d97de8a51d266071e&v=0",
    "kd-pd-1023-white-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000005344822f8042779ff6d3f96a&ts=496365&p=fs&cid=1&sig=73cf2755209b7b3a47854a151c12f102ede9516074c7c8e7cdc8eeeda8b1aa96&v=0",
    "kd-pd-1023-milk-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000c078822f90b12fee221ddc89&ts=496365&p=fs&cid=1&sig=dc241ae6d68adbd034fe4e666f23c697435cec3e9d7669167044015b74f6547c&v=0",
    "kd-pd-1023-milk-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000009e88822f8fd120274c5dba60&ts=496365&p=fs&cid=1&sig=512bf3d6c408c19af8c393afc1bb61741922dd4c7ebebef5d94129babecdd73b&v=0",
    "kd-pd-1023-blue-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000007038822f97a7d1db2709bbd0&ts=496365&p=fs&cid=1&sig=46b7b595c9c585d2c8a22a053bf244fd312426e6f471060e846f8bedc111abc2&v=0",
    "kd-pd-1023-blue-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_0000000029b0822f90fcd9855aa6af2a&ts=496365&p=fs&cid=1&sig=0cc2fada5e957a070af96e96f66cd666eb17c972e1b13c6d3a02f6b507307a72&v=0",
    "kd-pd-1026-white-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000d9bc820a84447e7575174cb8&ts=496365&p=fs&cid=1&sig=976f6f59703b90f6fccca3ba4defa6e3b1a1dc5f1b978de7bcc01f090eebda57&v=0",
    "kd-pd-1026-white-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000a33881f493e13ee993826095&ts=496365&p=fs&cid=1&sig=588a9a9c742506231b6f6cc2ca79a1acdced65f27c3d7e756e274fc761ec9c17&v=0",
    "kd-pd-1026-milk-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000001c6081f495c62eed4fb5e8ef&ts=496365&p=fs&cid=1&sig=4b3e920e75783cb348d056c8cee6e0294398e1698d8bc733d1cbf5a4538b1ff5&v=0",
    "kd-pd-1026-milk-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000006b3481f4a0213cecee3990a9&ts=496365&p=fs&cid=1&sig=53c9b13ef6054b706d62fb733b41fccc9ed5da995eb43f075d3409613b6ecdb3&v=0",
    "kd-pd-1026-blue-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000001ca881f49fee9cbdb71cccf5&ts=496365&p=fs&cid=1&sig=297ad3c9482d3a051f3c4f12997b743010d909eb2f64eeb309a8c420ac50bb1c&v=0",
    "kd-pd-1026-blue-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000d80081f4b377cbc8658defae&ts=496365&p=fs&cid=1&sig=9ccd572e5a946ff63dafa9b87df8988e4bb8ac13b4c51d4839b8ce4fdcf27c92&v=0",
    "kd-pd-1027-milk-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_000000007db481f487c330f8e25d5da8&ts=496365&p=fs&cid=1&sig=842bfd64633f741eeb80d595beeaf9f4fe9335a31c23a4dbaf8d560b5ed972ff&v=0",
    "kd-pd-1027-milk-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000d89c81f4980fc919b036ce49&ts=496365&p=fs&cid=1&sig=a64711e38f73fabff9acbed4c18caf0f00fa472f9d30ad3d0532f4487d13dfeb&v=0",
    "kd-pd-1027-sand-1.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000396881f4abc3cf0a7ea2e5c3&ts=496365&p=fs&cid=1&sig=234033a1986c7409936db6c3a15464de82354714580a87536db1429d33dca0f0&v=0",
    "kd-pd-1027-sand-2.jpg": "https://chatgpt.com/backend-api/estuary/content?id=file_00000000d1cc81f4b4b21ea4b809fd8a&ts=496365&p=fs&cid=1&sig=fcc2cc2b6aeed3c4f763b6bf881e00dc771664cc791f65ff71f01903d9d7488f&v=0",
}


def download_media() -> None:
    for filename, url in MEDIA.items():
        target = MEDIA_DIR / filename
        if target.exists() and target.stat().st_size > 10_000:
            continue
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            content_type = response.headers.get("Content-Type", "")
            payload = response.read()
        if len(payload) < 10_000 or ("image" not in content_type and not payload.startswith((b"\x89PNG", b"\xff\xd8\xff"))):
            raise RuntimeError(f"Unexpected media response for {filename}: {content_type}, {len(payload)} bytes")
        target.write_bytes(payload)
        print(f"Downloaded {filename}: {len(payload)} bytes")


def replace_product(text: str, product_id: int, next_id: int, replacement: str) -> str:
    start = text.index(f"  {{ id: {product_id},")
    end = text.index(f"  {{ id: {next_id},", start)
    return text[:start] + replacement.rstrip() + "\n" + text[end:]


def patch_page() -> None:
    text = PAGE.read_text(encoding="utf-8")

    text = text.replace(
        "  gallery?: string[];\n};\n\ntype ColorVariant = { name: string; hex: string; image: string; position?: string };",
        "  gallery?: string[];\n  sku?: string;\n  material?: string;\n  composition?: string;\n  sizes?: string[];\n  sizeDetails?: Record<string,{height:string;width:string}>;\n};\n\ntype ColorVariant = { name: string; hex: string; image: string; gallery?: string[]; position?: string };"
    )

    old_images = '''function getProductImages(product:Product){
  const sources=[product.image,...(product.gallery??[]),...(product.colorVariants??[]).map(variant=>variant.image)];
  return Array.from(new Set(sources.filter(Boolean)));
}'''
    new_images = '''function getProductImages(product:Product){
  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;
  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];
  return Array.from(new Set(sources.filter(Boolean)));
}

function getProductSizeOptions(product:Product){
  const names=product.sizes?.length?product.sizes:["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];
  return names.map((name,index)=>[name,product.price+(index===0?0:2000)] as const);
}'''
    if old_images in text:
        text = text.replace(old_images, new_images)

    text = text.replace(
        'const chosenProduct = { ...product, image: chosen.image, position: chosen.position ?? product.position, selectedColor: chosen.name };',
        'const chosenProduct = { ...product, image: chosen.image, gallery: chosen.gallery ?? product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name };'
    )

    p3 = '''  { id: 3, name: "Подушка с кружевом", note: "хлопок, 60×60 см", price: 2990, oldPrice: 3990, sku: "KD-PD-1023", material: "Хлопок", composition: "Внешняя часть: 100% хлопок; Наполнитель: 100% пух", sizes: ["60×60 см"], sizeDetails: {"60×60 см":{height:"60 см",width:"60 см"}}, image: "/images/table-products/kd-pd-1023-white-1.jpg", colorVariants: [
    { name: "Белый", hex: "#f7f7f4", image: "/images/table-products/kd-pd-1023-white-1.jpg", gallery:["/images/table-products/kd-pd-1023-white-2.jpg"] },
    { name: "Молочный", hex: "#e9e1d2", image: "/images/table-products/kd-pd-1023-milk-1.jpg", gallery:["/images/table-products/kd-pd-1023-milk-2.jpg"] },
    { name: "Синий", hex: "#8ba7c0", image: "/images/table-products/kd-pd-1023-blue-1.jpg", gallery:["/images/table-products/kd-pd-1023-blue-2.jpg"] },
  ] },'''
    p6 = '''  { id: 6, name: "Плед из кружева", note: "хлопок, 200×220 см", price: 9990, oldPrice: 13990, sku: "KD-PD-1026", material: "Хлопок", composition: "70% хлопок, 30% лён", sizes: ["200×220 см"], sizeDetails: {"200×220 см":{height:"200 см",width:"220 см"}}, image: "/images/table-products/kd-pd-1026-white-1.jpg", colorVariants: [
    { name: "Белый", hex: "#f6f5f0", image: "/images/table-products/kd-pd-1026-white-1.jpg", gallery:["/images/table-products/kd-pd-1026-white-2.jpg"] },
    { name: "Молочный", hex: "#ece5d8", image: "/images/table-products/kd-pd-1026-milk-1.jpg", gallery:["/images/table-products/kd-pd-1026-milk-2.jpg"] },
    { name: "Синий", hex: "#91a9bd", image: "/images/table-products/kd-pd-1026-blue-1.jpg", gallery:["/images/table-products/kd-pd-1026-blue-2.jpg"] },
  ] },'''
    p7 = '''  { id: 7, name: "Стёганое покрывало «Бархатный ритм»", note: "микровелюр, 200×220 / 220×240 см", price: 12990, sku: "KD-PD-1027", material: "Микровелюр", composition: "Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно", sizes: ["Евро 200×220 см","Кинг сайз 220×240 см"], sizeDetails: {"Евро 200×220 см":{height:"200 см",width:"220 см"},"Кинг сайз 220×240 см":{height:"220 см",width:"240 см"}}, image: "/images/table-products/kd-pd-1027-milk-1.jpg", colorVariants: [
    { name: "Молочный", hex: "#e8dfcf", image: "/images/table-products/kd-pd-1027-milk-1.jpg", gallery:["/images/table-products/kd-pd-1027-milk-2.jpg"] },
    { name: "Песочный", hex: "#c9ad88", image: "/images/table-products/kd-pd-1027-sand-1.jpg", gallery:["/images/table-products/kd-pd-1027-sand-2.jpg"] },
  ] },'''
    text = replace_product(text, 3, 4, p3)
    text = replace_product(text, 6, 7, p6)
    text = replace_product(text, 7, 8, p7)

    text = text.replace(
        'function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void}){\n  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=index===sizes.length-1;',
        'function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableLast=true}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableLast?:boolean}){\n  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=unavailableLast&&index===sizes.length-1;'
    )

    text = text.replace(
        'const [selectedSize,setSelectedSize]=useState("Евро 200×220");',
        'const [selectedSize,setSelectedSize]=useState(product.sizes?.[0]??"Евро 200×220");'
    )
    text = text.replace(
        'setSelectedSize("Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);',
        'setSelectedSize(product.sizes?.[0]??"Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);'
    )
    text = text.replace(
        'const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;',
        'const sizes=getProductSizeOptions(product);'
    )
    text = text.replace(
        'const selectedProduct={...product,price:unitPrice,image,selectedColor:color.name,selectedSize,quantity};',
        'const selectedProduct={...product,price:unitPrice,image,gallery:color.gallery??product.gallery,selectedColor:color.name,selectedSize,quantity};\n  const selectedDimensions=product.sizeDetails?.[selectedSize];'
    )
    text = text.replace(
        '<small className="pdp-code">АРТИКУЛ: KD-PD-{1020+product.id}</small>',
        '<small className="pdp-code">АРТИКУЛ: {product.sku??`KD-PD-${1020+product.id}`}</small>'
    )
    text = text.replace(
        '<label>Размер <button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button></label>',
        '<label>Размер <button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Размерная сетка</button></label>'
    )
    text = text.replace(
        '<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        '<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.sizes?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        1
    )

    generic_characteristics = '''{title:"ХАРАКТЕРИСТИКИ",content:<><p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p><dl><div><dt>Состав</dt><dd>Хлопок / лён</dd></div><div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>}'''
    dynamic_characteristics = '''{title:"ХАРАКТЕРИСТИКИ",content:<><p>{product.material?`Материал и параметры соответствуют выбранному варианту товара.`:"Натуральные материалы, деликатная отделка и производство с вниманием к деталям."}</p><dl>{product.material&&<div><dt>Материал</dt><dd>{product.material}</dd></div>}{product.composition&&<div><dt>Состав</dt><dd>{product.composition}</dd></div>}<div><dt>Размер</dt><dd>{selectedSize}</dd></div>{selectedDimensions&&<><div><dt>Высота</dt><dd>{selectedDimensions.height}</dd></div><div><dt>Ширина</dt><dd>{selectedDimensions.width}</dd></>}<div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>}'''
    text = text.replace(generic_characteristics, dynamic_characteristics)

    text = text.replace(
        'const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;',
        'const sizes=getProductSizeOptions(product);'
    )
    text = text.replace(
        '<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        '<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.sizes?.length} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>'
    )
    text = text.replace(
        'const [chosenSize,setChosenSize]=useState("Евро 200×220");',
        'const [chosenSize,setChosenSize]=useState(product.sizes?.[0]??"Евро 200×220");'
    )

    old_info = '''function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Высота</dt><dd>0,5 см</dd></div><div><dt>Ширина</dt><dd>{product.id===7?"220":"160"} см</dd></div><div><dt>Длина</dt><dd>{product.id===7?"240":"200"} см</dd></div><div><dt>Вес</dt><dd>1,2 кг</dd></div></dl></section><section><h2>СОСТАВ</h2><h3>ВНЕШНЯЯ ЧАСТЬ</h3><p>100% натуральный хлопок</p><h3>НАПОЛНИТЕЛЬ</h3><p>100% переработанный полиэстер</p></section><section><h2>СЕРТИФИЦИРОВАННЫЕ МАТЕРИАЛЫ</h2><h3>ХЛОПОК, СЕРТИФИЦИРОВАННЫЙ ПО OEKO-TEX®</h3><p>Материал проверен на отсутствие вредных веществ и подходит для ежедневного домашнего использования.</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}'''
    new_info = '''function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sizeNames=product.sizes?.length?product.sizes:["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl>{sizeNames.map(name=><div key={name}><dt>{name}</dt><dd>{product.sizeDetails?.[name]?`${product.sizeDetails[name].height} × ${product.sizeDetails[name].width}`:"Доступен"}</dd></div>)}</dl></section><section><h2>МАТЕРИАЛ И СОСТАВ</h2><h3>{product.material??"НАТУРАЛЬНЫЕ МАТЕРИАЛЫ"}</h3><p>{product.composition??"Натуральный хлопок и деликатная отделка."}</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}'''
    if old_info in text:
        text = text.replace(old_info, new_info)

    text = text.replace(
        '{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)}',
        '{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => {setSize(selected.sizes?.[0]??"Евро 200×220");setSizeSheet(true)}}'
    )
    text = text.replace(
        '{sizeSheet && <SizeSheet size={size} setSize={setSize} close={() => setSizeSheet(false)} add={(quantity,unitPrice) => add({...selected,price:unitPrice},size,quantity)} price={selected.price} />}',
        '{sizeSheet && <SizeSheet product={selected} size={size} setSize={setSize} close={() => setSizeSheet(false)} add={(quantity,unitPrice) => add({...selected,price:unitPrice},size,quantity)} />}'
    )
    text = text.replace(
        'function SizeSheet({ size, setSize, close, add, price }: { size:string; setSize:(s:string)=>void; close:()=>void; add:(quantity:number,unitPrice:number)=>void; price:number }) {\n  const [quantity,setQuantity]=useState(1);\n  const sizes=[["Евро 200×220",price],["Семейный 150×200",price+2000],["Кинг Сайз 220×240",price+2000]] as const;',
        'function SizeSheet({ product, size, setSize, close, add }: { product:Product; size:string; setSize:(s:string)=>void; close:()=>void; add:(quantity:number,unitPrice:number)=>void }) {\n  const [quantity,setQuantity]=useState(1);\n  const sizes=getProductSizeOptions(product);'
    )
    text = text.replace(
        '<ProductSizeRows sizes={sizes} selectedSize={size} setSelectedSize={setSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        '<ProductSizeRows sizes={sizes} selectedSize={size} setSelectedSize={setSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.sizes?.length} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>'
    )
    text = text.replace(
        '<button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button>',
        '<button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Размерная сетка</button>'
    )

    PAGE.write_text(text, encoding="utf-8")
    print("Applied product data from товары.csv to KD-PD-1023, KD-PD-1026, KD-PD-1027")


def main() -> None:
    download_media()
    patch_page()


if __name__ == "__main__":
    main()
