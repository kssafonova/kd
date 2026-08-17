КОНСТРУКТОР И EDITORIAL «КУЛЬТУРА ДОМА» — CSV-ДАННЫЕ

Основные CSV конструктора:

1. kultura-doma-constructor-presets-final.csv
2. kultura_doma_scenario_candidates.csv
3. kultura_doma_constructor_scenarios.csv
4. kultura_doma_full_constructor_eligible_catalog.csv

Расширение Editorial до 23 сценариев:

5. kultura_doma_scenario_expansion_rules.csv
6. kultura_doma_scenario_expansion_patch.csv

Итоговые пути:

public/data/kultura-doma-constructor-presets-final.csv
public/data/kultura_doma_scenario_candidates.csv
public/data/kultura_doma_constructor_scenarios.csv
public/data/kultura_doma_full_constructor_eligible_catalog.csv
public/data/kultura_doma_scenario_expansion_rules.csv
public/data/kultura_doma_scenario_expansion_patch.csv

Правила:
- CSV остаются обычными raw text файлами;
- не конвертировать CSV в JSON;
- не создавать Base64-файлы;
- не импортировать CSV в TypeScript/JavaScript bundle;
- клиент загружает CSV через fetch().

Первые 9 сценариев берутся из kultura_doma_constructor_scenarios.csv.
Ещё 14 сценариев берутся из kultura_doma_scenario_expansion_rules.csv.
Патч исправляет allowed_product_types для первой роли palace-dinner.

Для новых 14 сценариев нельзя выдумывать preset SKU. Конструктор фильтрует реальные товары master catalog по allowed_collections × allowed_product_types и предлагает пользователю выбрать конкретный offer_id самостоятельно.

На GitHub Pages путь автоматически учитывает basePath /kd через NEXT_PUBLIC_BASE_PATH.
Если один из четырёх основных CSV отсутствует, интерфейс показывает сообщение:
«Добавьте CSV-файлы в public/data».
