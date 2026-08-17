from pathlib import Path
import runpy

script = Path("scripts/restore-editorial-buy-all.py")
if not script.exists():
    raise SystemExit("restore-editorial-buy-all.py is missing")

runpy.run_path(str(script), run_name="__main__")
