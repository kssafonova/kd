# Культура дома — CSV database export

Нормализованный экспорт данных сайта. Разделитель во всех CSV: `;`, кодировка UTF-8 with BOM.

- Товарных карточек: 139
- SKU/вариантов: 213
- Категорий: 5
- Подкатегорий: 21
- Коллекций: 21
- Капсул: 5
- Готовых решений: 5
- Регионов checkout: 10

Начните с `00_database_manifest.csv` и `32_schema_relationships.csv`.

Источники: `public/data/catalog_master.csv`, текущие CSV конструктора в `public/data/`, и конфигурация checkout/бутиков из `app/page.tsx`.
