from pathlib import Path
import shutil

root=Path(__file__).resolve().parents[1]
storefront=root/"app"/"storefront-app.tsx"
page=root/"app"/"page.tsx"

if storefront.exists():
    shutil.copyfile(storefront,page)
    print("Restored monolithic storefront for legacy migrations")
else:
    print("No storefront-app.tsx yet; keeping current page.tsx")
