from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
MARKER = "// CATALOG_SKU_MODEL_V1"


def must_replace(text:str, old:str, new:str, label:str)->str:
    if old not in text:
        raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old,new,1)


def main():
    text=PAGE.read_text(encoding="utf-8")
    if MARKER in text:
        print("Normalized SKU catalog model already applied")
        return

    text = must_replace(
        text,
        'import { assetUrl } from "./assets";',
        'import { assetUrl } from "./assets";\nimport { catalogProductOverrides, type CatalogSku } from "./catalog-data";\n\n'+MARKER,
        "catalog import"
    )

    text = must_replace(
        text,
        '''  gallery?: string[];
};

type ColorVariant = { name: string; hex: string; image: string; position?: string };''',
        '''  gallery?: string[];
  article?: string;
  skus?: CatalogSku[];
  selectedSkuId?: string;
};

type ColorVariant = { name: string; hex: string; image: string; gallery?: string[]; position?: string };''',
        "product type"
    )

    text = must_replace(
        text,
        '''function getProductImages(product:Product){
  const sources=[product.image,...(product.gallery??[]),...(product.colorVariants??[]).map(variant=>variant.image)];
  return Array.from(new Set(sources.filter(Boolean)));
}''',
        '''function findProductSku(product:Product,color?:string,size?:string){
  if(!product.skus?.length)return undefined;
  return product.skus.find(item=>item.id===product.selectedSkuId)
    ??product.skus.find(item=>(!color||item.color===color)&&(!size||item.size===size))
    ??product.skus.find(item=>!color||item.color===color)
    ??product.skus[0];
}

function getProductSizeOptions(product:Product,color?:string){
  if(product.skus?.length){
    const rows=product.skus.filter(item=>!color||item.color===color);
    return Array.from(new Map(rows.map(item=>[item.size,[item.size,item.price] as const])).values());
  }
  return [["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
}

function getProductImages(product:Product){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize);
  if(sku)return Array.from(new Set([sku.image,...sku.gallery].filter(Boolean)));
  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;
  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];
  return Array.from(new Set(sources.filter(Boolean)));
}''',
        "sku helpers"
    )

    text = must_replace(text, 'const products: Product[] = [', 'const baseProducts: Product[] = [', "base products")

    insertion = '''const products: Product[] = baseProducts.map(base=>{
  const override=catalogProductOverrides[base.id];
  if(!override)return base;
  const first=override.skus[0];
  const colors=Array.from(new Map(override.skus.map(item=>[item.color,item])).values());
  return {
    ...base,
    name:override.name,
    note:override.note,
    article:override.article,
    skus:override.skus,
    price:Math.min(...override.skus.map(item=>item.price)),
    image:first.image,
    gallery:first.gallery,
    colorVariants:colors.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery}))
  };
});

'''
    text = must_replace(text, 'const slides:Slide[] = [', insertion+'const slides:Slide[] = [', "catalog overlay")

    text = must_replace(
        text,
        '''  const chosen = variants[colorIndex];
  const chosenProduct = { ...product, image: chosen.image, position: chosen.position ?? product.position, selectedColor: chosen.name };''',
        '''  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const chosenProduct = { ...product, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };''',
        "product card sku"
    )

    text = must_replace(
        text,
        '''function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void}){
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=index===sizes.length-1;''',
        '''function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableLast=true}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableLast?:boolean}){
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=unavailableLast&&index===sizes.length-1;''',
        "size rows"
    )

    old_pdp = '''  const [selectedSize,setSelectedSize]=useState("Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const variants=product.colorVariants??[{name:"Молочный",hex:"#eee",image:product.image}];
  useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);setColorIndex(initial>=0?initial:0);setActiveImage(0);setSelectedSize("Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);
  const color=variants[colorIndex];
  const gallery=product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const image=gallery[activeImage]??color.image;
  const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
  const unitPrice=sizes.find(([name])=>name===selectedSize)?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image,selectedColor:color.name,selectedSize,quantity};
  const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize():add(selectedProduct);'''
    new_pdp = '''  const [selectedSize,setSelectedSize]=useState(product.skus?.[0]?.size??"Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const variants=product.colorVariants??[{name:"Молочный",hex:"#eee",image:product.image}];
  useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);const nextIndex=initial>=0?initial:0;const nextColor=variants[nextIndex]?.name;setColorIndex(nextIndex);setActiveImage(0);setSelectedSize(findProductSku(product,nextColor)?.size??"Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);
  const color=variants[colorIndex];
  const sizes=getProductSizeOptions(product,color.name);
  const sku=findProductSku(product,color.name,selectedSize);
  const gallery=sku?[sku.image,...sku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const image=gallery[activeImage]??sku?.image??color.image;
  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image,gallery:sku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};
  const specs=sku??product.skus?.[0];
  const handlePurchase=()=>product.skus?.length?add(selectedProduct):(window.matchMedia("(max-width: 900px)").matches?chooseSize():add(selectedProduct));'''
    text = must_replace(text, old_pdp, new_pdp, "pdp sku state")

    text = must_replace(
        text,
        '<small className="pdp-code">АРТИКУЛ: KD-PD-{1020+product.id}</small>',
        '<small className="pdp-code">АРТИКУЛ: {sku?.id??product.article??`KD-PD-${1020+product.id}`}</small>',
        "pdp article"
    )

    text = must_replace(
        text,
        'onClick={()=>{setColorIndex(index);setActiveImage(0)}}',
        'onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize(findProductSku(product,variant.name)?.size??selectedSize);setQuantity(1)}}',
        "color switch"
    )

    text = must_replace(
        text,
        '<label>Размер <button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button></label><ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        '<label>Размер <button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Размерная сетка</button></label><ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        "pdp sizes"
    )

    text = must_replace(
        text,
        '''  {title:"ХАРАКТЕРИСТИКИ",content:<><p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p><dl><div><dt>Состав</dt><dd>Хлопок / лён</dd></div><div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>},''',
        '''  {title:"ХАРАКТЕРИСТИКИ",content:<><p>{specs?`${specs.material}. ${specs.size}.`:"Натуральные материалы, деликатная отделка и производство с вниманием к деталям."}</p><dl>{specs&&<><div><dt>Материал</dt><dd>{specs.material}</dd></div><div><dt>Состав</dt><dd>{specs.composition}</dd></div><div><dt>Высота</dt><dd>{specs.height}</dd></div><div><dt>Ширина</dt><dd>{specs.width}</dd></div></>}<div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>},''',
        "pdp specs"
    )

    text = must_replace(
        text,
        '''  const [chosenSize,setChosenSize]=useState("Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
  const unitPrice=sizes.find(([item])=>item===chosenSize)?.[1]??product.price;''',
        '''  const selectedColor=product.selectedColor??product.colorVariants?.[0]?.name;
  const [chosenSize,setChosenSize]=useState(findProductSku(product,selectedColor)?.size??"Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  const sizes=getProductSizeOptions(product,selectedColor);
  const selectedSku=findProductSku(product,selectedColor,chosenSize);
  const unitPrice=selectedSku?.price??sizes.find(([item])=>item===chosenSize)?.[1]??product.price;''',
        "plp sku sizes"
    )

    text = must_replace(
        text,
        '<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        '<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>',
        "plp rows"
    )

    old_drawer='''function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Высота</dt><dd>0,5 см</dd></div><div><dt>Ширина</dt><dd>{product.id===7?"220":"160"} см</dd></div><div><dt>Длина</dt><dd>{product.id===7?"240":"200"} см</dd></div><div><dt>Вес</dt><dd>1,2 кг</dd></div></dl></section><section><h2>СОСТАВ</h2><h3>ВНЕШНЯЯ ЧАСТЬ</h3><p>100% натуральный хлопок</p><h3>НАПОЛНИТЕЛЬ</h3><p>100% переработанный полиэстер</p></section><section><h2>СЕРТИФИЦИРОВАННЫЕ МАТЕРИАЛЫ</h2><h3>ХЛОПОК, СЕРТИФИЦИРОВАННЫЙ ПО OEKO-TEX®</h3><p>Материал проверен на отсутствие вредных веществ и подходит для ежедневного домашнего использования.</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}'''
    new_drawer='''function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize)??product.skus?.[0];
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Размер</dt><dd>{sku?.size??product.note}</dd></div>{sku&&<><div><dt>Высота</dt><dd>{sku.height}</dd></div><div><dt>Ширина</dt><dd>{sku.width}</dd></div></>}</dl></section><section><h2>МАТЕРИАЛ И СОСТАВ</h2><h3>{sku?.material??"Материал"}</h3><p>{sku?.composition??"Информация указана в характеристиках товара."}</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}'''
    text = must_replace(text, old_drawer, new_drawer, "info drawer")

    text = text.replace('  const sizeOptions=["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];\n','',1)
    text = must_replace(
        text,
        '<label>Размер<select value={p.selectedSize} onChange={event=>update(i,{selectedSize:event.target.value})}>{sizeOptions.map(option=><option key={option}>{option}</option>)}</select></label>',
        '<label>Размер<select value={p.selectedSize} onChange={event=>{const nextSize=event.target.value;const nextSku=findProductSku(p,p.selectedColor,nextSize);update(i,{selectedSize:nextSize,selectedSkuId:nextSku?.id,price:nextSku?.price??p.price,image:nextSku?.image??p.image,gallery:nextSku?.gallery??p.gallery})}}>{getProductSizeOptions(p,p.selectedColor).map(([option])=><option key={option}>{option}</option>)}</select></label>',
        "cart sku selector"
    )

    text = must_replace(
        text,
        '''    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const item: CartItem = { ...product, image: selectedVariant?.image ?? product.image, position: selectedVariant?.position ?? product.position, selectedSize: chosenSize, selectedColor: selectedVariant?.name ?? "Молочный", quantity };''',
        '''    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const selectedSku=findProductSku(product,product.selectedColor,chosenSize);
    const item: CartItem = { ...product, price:selectedSku?.price??product.price, image:selectedSku?.image??selectedVariant?.image??product.image, gallery:selectedSku?.gallery??product.gallery, position:selectedVariant?.position??product.position, selectedSize:chosenSize, selectedColor:selectedSku?.color??selectedVariant?.name??"Молочный", selectedSkuId:selectedSku?.id, quantity };''',
        "cart add"
    )
    text = must_replace(
        text,
        '''    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const item: CartItem = { ...product, price: unitPrice, image: selectedVariant?.image ?? product.image, position: selectedVariant?.position ?? product.position, selectedSize: chosenSize, selectedColor: selectedVariant?.name ?? "Молочный", quantity };''',
        '''    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const selectedSku=findProductSku(product,product.selectedColor,chosenSize);
    const item: CartItem = { ...product, price:selectedSku?.price??unitPrice, image:selectedSku?.image??selectedVariant?.image??product.image, gallery:selectedSku?.gallery??product.gallery, position:selectedVariant?.position??product.position, selectedSize:chosenSize, selectedColor:selectedSku?.color??selectedVariant?.name??"Молочный", selectedSkuId:selectedSku?.id, quantity };''',
        "plp cart add"
    )

    PAGE.write_text(text,encoding="utf-8")
    print("Applied normalized product/SKU catalog model")


if __name__=="__main__":
    main()
