from pathlib import Path

path = Path("app/page.tsx")
page = path.read_text(encoding="utf-8")

old = 'const openQuick=()=>{setMode("quick");track("story_quick_add_open")};'
new = '''const openQuick=()=>{
    // Quick-buy always opens the canonical ready-made preset, independent of builder edits.
    if(story==="bedroom"){
      setBedSize("");
      setBedOptional({blanket:true,pillow:true});
      setBedQty({blanket:1,pillow:1});
    }else if(story==="table"){
      setOccasion("Чай для двоих");
      setGuests(2);
      setTableOptional({napkin:true,plate:false,vase:false,gift:false});
    }
    setMode("quick");
    track("story_quick_add_open");
  };'''

if old in page:
    page = page.replace(old, new, 1)
elif 'Quick-buy always opens the canonical ready-made preset' in page:
    print("Story quick-buy preset already refined")
    raise SystemExit(0)
else:
    raise SystemExit("Story quick-buy handler not found")

path.write_text(page, encoding="utf-8")
print("Refined story quick-buy preset reset")
