КОНСТРУКТОР «КУЛЬТУРА ДОМА» — CSV-ДАННЫЕ

Поместите в эту папку четыре исходных CSV-файла БЕЗ ИЗМЕНЕНИЯ СОДЕРЖИМОГО:

1. kultura-doma-constructor-presets-final.csv
2. kultura_doma_scenario_candidates.csv
3. kultura_doma_constructor_scenarios.csv
4. kultura_doma_full_constructor_eligible_catalog.csv

Итоговые пути:

public/data/kultura-doma-constructor-presets-final.csv
public/data/kultura_doma_scenario_candidates.csv
public/data/kultura_doma_constructor_scenarios.csv
public/data/kultura_doma_full_constructor_eligible_catalog.csv

Требования:
- сохранить исходный UTF-8 с BOM;
- не конвертировать CSV в JSON;
- не кодировать файлы в Base64;
- не импортировать CSV в TypeScript/JavaScript bundle.

Клиентский конструктор загружает эти файлы через fetch().
На GitHub Pages путь автоматически учитывает basePath /kd через NEXT_PUBLIC_BASE_PATH.

Если файлов нет, интерфейс показывает сообщение:
«Добавьте CSV-файлы в public/data».
