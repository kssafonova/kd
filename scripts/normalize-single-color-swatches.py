from pathlib import Path
import re

path=Path("app/page.tsx")
text=path.read_text(encoding="utf-8")
pattern=r'(?:\{variants\.length>1&&)+(<div className="plp-swatches"[\s\S]*?</div>)(?:\})+'
text,count=re.subn(pattern,r'{variants.length>1&&\1}',text,count=1)
path.write_text(text,encoding="utf-8")
print(f"Normalized product swatches: {count}")
