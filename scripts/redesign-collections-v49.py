from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

new_editorials = '''type Editorial = { id:string; name:string; kind:"КАПСУЛА"|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string[]; productIds:number[] };
// COLLECTIONS_ONLY_V49
const editorials:Editorial[] = [
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле. Белый, ледяной голубой и деликатный орнамент создают ощущение тихого зимнего утра.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/images/editorial/caps_led.png","/images/editorial/caps_led_podyshka.png","/images/editorial/caps_led_podyshka2.png","/images/editorial/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КОЛЛЕКЦИЯ", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Коллекция о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png","/images/editorial/caps_luna_serviz2.png","/images/editorial/caps_luna_serviz3.png"], productIds:[4,10,5,6,3] },
  { id:"white-chapter", name:"Белая глава", kind:"КОЛЛЕКЦИЯ", lead:"Белый сатин, спокойный свет и мягкие фактуры для спальни, в которой ничего не отвлекает.", detail:"Белая глава строится на чистой палитре и тактильности. Постельный текстиль, подушки и мягкие предметы объединены так, чтобы интерьер оставался светлым, спокойным и цельным.", description:"Светлая коллекция текстиля для тихой современной спальни.", images:["/images/russian-bedroom.png","/images/classic-bedroom.png","/images/zip-product-bed.png","/images/beige-bedroom.png"], productIds:[2,8,11,12,3] },
  { id:"home-in-bloom", name:"Дом в цвету", kind:"КОЛЛЕКЦИЯ", lead:"Фарфор, вазы и сервировка для стола, который выглядит празднично даже в обычный день.", detail:"Коллекция соединяет посуду, вазы и предметы сервировки в лёгкую композицию. Цвет и прозрачные фактуры добавляют дому выразительности, но не превращают стол в парадную декорацию.", description:"Коллекция для сервировки и домашних встреч — выразительная, но повседневная.", images:["/images/editorial-vases.webp","/images/editorial-table.webp","/images/russian-service-blue.png","/images/time-table.png"], productIds:[5,10,2001,2004,2010] },
  { id:"velvet-rhythm", name:"Бархатный ритм", kind:"КОЛЛЕКЦИЯ", lead:"Молочные и холодные синие оттенки, стёганые поверхности и мягкий текстиль для многослойной спальни.", detail:"Бархатный ритм собран вокруг покрывал, пледов и декоративных подушек. Разные фактуры остаются в одной спокойной гамме и позволяют менять настроение спальни без полного обновления интерьера.", description:"Тактильная коллекция пледов, покрывал и декоративных подушек.", images:["/images/beige-bedroom.png","/images/classic-bedroom.png","/images/blue-bedroom.png","/images/products/KD-PD-1027-MOL01.png"], productIds:[7,6,3,2000,2003] },
];'''

pattern = re.compile(
    r'type Editorial = \{ id:string; name:string; kind:"КАПСУЛА"\|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string\[\]; productIds:number\[\] \};\n(?:\/\/ COLLECTIONS_ONLY_V49\n)?const editorials:Editorial\[\] = \[.*?\n\];',
    re.S,
)
page, count = pattern.subn(new_editorials, page, count=1)
if count != 1:
    raise SystemExit("V49: editorials block not found")

page = page.replace('const [filter,setFilter]=useState<"all"|"capsule"|"collection">("all");\n  ', '')
page = re.sub(
    r'const visible=editorials\.filter\(item=>filter==="all"\|\|\(filter==="capsule"\?item\.kind==="КАПСУЛА":item\.kind==="КОЛЛЕКЦИЯ"\)\);',
    'const visible=editorials;',
    page,
    count=1,
)
page = re.sub(r'\n\s*<nav className="collections-v34-tabs" aria-label="[^"]*">.*?</nav>\n', '\n', page, count=1, flags=re.S)
page = page.replace('<h1>Капсулы и коллекции</h1>', '<h1>Коллекции</h1>')
page = page.replace('Истории для дома, собранные из предметов Культура Дома.', 'Коллекции для разных пространств и домашних ритуалов — от спальни до сервировки.')
page = page.replace('aria-label="Список капсул и коллекций"', 'aria-label="Список коллекций"')
page = page.replace('Капсулы и коллекции', 'Коллекции')
page = page.replace('КАПСУЛЫ И КОЛЛЕКЦИИ', 'КОЛЛЕКЦИИ')
page = page.replace('label:"КАПСУЛА",title:"Лунная сказка"', 'label:"КОЛЛЕКЦИЯ",title:"Лунная сказка"')

page_path.write_text(page, encoding="utf-8")
print("V49 collections-only landing applied")
