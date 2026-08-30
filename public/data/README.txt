CATALOG MASTER

`catalog_master.csv` is the only product catalog source used by the storefront.

Format:
- UTF-8
- semicolon-delimited
- 198 SKU rows
- 136 unique articles
- one product card per `Артикул`; rows with the same article are SKU variants
- product photos reference only files under `/assets/images/`

Legacy grouped/XLSX product catalog exports were removed and must not be reintroduced.
