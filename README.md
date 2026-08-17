# Культура Дома

Существующий Next.js App Router storefront с static export для GitHub Pages.

## Требования

- Node.js `>=22.13.0`
- npm

## Локальный запуск

```bash
npm install
npm run dev
```

Главная сайта открывается на локальном адресе, который выводит dev server.

Раздел конструктора:

```text
/constructor/
```

## Сборка

Проверка существующего проекта:

```bash
npm run build
```

GitHub Pages workflow дополнительно выполняет статический Next.js export:

```bash
NEXT_PUBLIC_BASE_PATH=/kd npx next build
```

`next.config.ts` сохраняет:

- `output: "export"`;
- `trailingSlash: true`;
- `basePath: "/kd"` в GitHub Actions;
- `assetPrefix: "/kd/"` в GitHub Actions;
- `images.unoptimized: true`.

## Конструктор сценариев

Новый раздел встроен в текущий Next.js-проект и не использует Vite/React Router как отдельное приложение.

Маршруты App Router:

```text
/constructor/
/constructor/red-thread-tea/
/constructor/quiet-obereg/
/constructor/sky-celebration/
/constructor/green-salon/
/constructor/blue-hour-bedroom/
```

`app/constructor/[scenarioId]/page.tsx` содержит `generateStaticParams()` для всех пяти `scenario_id`, поэтому страницы формируются во время static export и не требуют сервера.

### CSV

Конструктор загружает данные на клиенте через `fetch()`. CSV не импортируются в TypeScript/JavaScript bundle и не конвертируются в Base64/JSON.

В `public/data/` должны лежать исходные файлы без изменения содержимого:

```text
public/data/kultura-doma-constructor-presets-final.csv
public/data/kultura_doma_scenario_candidates.csv
public/data/kultura_doma_constructor_scenarios.csv
public/data/kultura_doma_full_constructor_eligible_catalog.csv
```

На GitHub Pages путь строится как `/kd/data/<filename>` через `NEXT_PUBLIC_BASE_PATH=/kd`. Локально используется `/data/<filename>`.

Если CSV отсутствуют, интерфейс не падает и показывает сообщение:

```text
Добавьте CSV-файлы в public/data
```

### Источники данных

- preset и порядок: `kultura-doma-constructor-presets-final.csv`;
- разрешённые замены: `kultura_doma_scenario_candidates.csv`;
- названия/описания: `kultura_doma_constructor_scenarios.csv`;
- изображения, варианты, материалы, цены и `availability_status`: `kultura_doma_full_constructor_eligible_catalog.csv`.

Изображения используются только из `primary_image_url` и `all_image_urls`.

### Замены

По умолчанию замена разрешена только при полном совпадении `product_type`.

Единственное исключение:

```text
tea_pair <-> coffee_pair
```

Поэтому `napkin` нельзя заменить на `placemat`, `table_runner` или `tablecloth`, а типы тарелок не смешиваются.

### MVP-корзина

Кнопка «Добавить всё в корзину» формирует массив отдельных SKU:

```json
[
  { "offer_id": "1330", "quantity": 2 }
]
```

Payload выводится в интерфейс и `console.log` с меткой `ADD_ALL_TO_CART`.

Позиции без валидной цены, недоступные SKU и товар с обязательным невыбранным вариантом блокируют добавление. Для `blue-hour-bedroom` конкретный размер белья выбирается вручную; автоматический выбор запрещён.

## GitHub Pages

Workflow: `.github/workflows/deploy-pages.yml`.

При push в `main` он:

1. применяет существующие storefront patches;
2. добавляет CTA «Собрать сценарий» на главную;
3. устанавливает зависимости;
4. выполняет `npx next build` с `NEXT_PUBLIC_BASE_PATH=/kd`;
5. публикует static export в текущую legacy Pages-схему репозитория.

После публикации итоговые URL:

```text
https://kssafonova.github.io/kd/constructor/
https://kssafonova.github.io/kd/constructor/red-thread-tea/
https://kssafonova.github.io/kd/constructor/quiet-obereg/
https://kssafonova.github.io/kd/constructor/sky-celebration/
https://kssafonova.github.io/kd/constructor/green-salon/
https://kssafonova.github.io/kd/constructor/blue-hour-bedroom/
```

## Существующий storefront

Существующие `app/page.tsx`, `app/layout.tsx`, карточки, PDP, галереи, editorial flow и CSS сохраняются. Конструктор добавлен отдельным App Router-разделом под `app/constructor/` и переиспользует `app/remote-image.tsx` для безопасной загрузки изображений.
