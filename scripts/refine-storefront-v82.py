from pathlib import Path

root=Path(__file__).resolve().parents[1]
page_path=root/'app'/'page.tsx'
ready_path=root/'app'/'ready-solutions'/'ready-solutions-v71-client.tsx'

ready=ready_path.read_text(encoding='utf-8')
# Collection cards in Ready Solutions must never render an empty placeholder when
# a collection has no standalone feed image. Scope the replacement to the two
# collection-card RemoteImage nodes so product cards keep their own local data.
old_card='<RemoteImage src={rowImages(row)[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={name}/>'
new_card='<RemoteImage src={rowImages(row)[0]||solution.heroImage||baseRows[0]?.primary_image_url||"/images/editorial/caps_led.png"} fallbackSrc={solution.heroImage||baseRows[0]?.primary_image_url||"/images/editorial/caps_led.png"} alt={name}/>'
ready=ready.replace(old_card,new_card)
ready_path.write_text(ready,encoding='utf-8')

page=page_path.read_text(encoding='utf-8')
page=page.replace('image:"/images/constructor/warm-brutalism.jpeg"','image:"/images/constructor/bluegold2.jpeg"')
# Make the expanded home category list useful rather than linking to empty category pages.
old='''    "Пледы и подушки":[3,6,7,2000,2003],\n    "Домашняя одежда":[],\n    "Столовый текстиль":[],'''
new='''    "Пледы и подушки":[3,6,7,2000,2003],\n    "Декор для дома":products.filter(product=>/ваза|свеч|диффуз|декор|подуш|плед/i.test(product.name)).map(product=>product.id),\n    "Свечи и диффузоры":products.filter(product=>/свеч|диффуз/i.test(product.name)).map(product=>product.id),\n    "Для ванной":products.filter(product=>/ванн|полотен|халат/i.test(`${product.name} ${product.note}`)).map(product=>product.id),\n    "Домашняя одежда":products.filter(product=>/халат|пижам|одежд/i.test(`${product.name} ${product.note}`)).map(product=>product.id),\n    "Столовый текстиль":products.filter(product=>/скатерт|салфет|плейсмат|дорожк/i.test(product.name)).map(product=>product.id),'''
if old in page: page=page.replace(old,new,1)
# Keep the visible catalog rail aligned with the new home navigation.
page=page.replace('["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Декор для дома","Домашняя одежда","Столовый текстиль"]','["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Декор для дома","Свечи и диффузоры","Для ванной","Столовый текстиль"]')
page_path.write_text(page,encoding='utf-8')
print('Applied storefront V82 media and category polish')