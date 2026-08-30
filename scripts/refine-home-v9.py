from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Commercial hero copy: every slide has an explicit destination-oriented CTA.
hero_pattern = r'''  const heroSlides=\[\n[\s\S]*?\n  \];\n  const activeIndex='''
hero_replacement = '''  const heroSlides=[
    {label:"НОВИНКИ",title:"Новинки",cta:"Смотреть новинки",desktopImage:"/assets/images/time-hero.png",mobileImage:"/assets/images/blue-bedding-vertical.png",action:()=>openCatalog("Все товары")},
    {label:"СПАЛЬНЯ",title:"Спальня",cta:"Перейти в спальню",desktopImage:"/assets/images/blue-bedroom.png",mobileImage:"/assets/images/caps_luna_postel.png",action:()=>openCatalog("Постельное бельё")},
    {label:"ДЕКОР ДЛЯ ДОМА",title:"Декор для дома",cta:"Смотреть декор",desktopImage:"/assets/images/beige-bedroom.png",mobileImage:"/assets/images/russian-bedroom.png",action:()=>openCatalog("Пледы и подушки")},
  ];
  const activeIndex='''
if re.search(hero_pattern, text):
    text = re.sub(hero_pattern, hero_replacement, text, count=1)
else:
    raise SystemExit("Home hero slides block not found")

# State used to pause autoplay while the user interacts, plus touch swipe on mobile.
state_anchor = '  const [traditionsPlaying,setTraditionsPlaying]=useState(true);\n'
state_insert = '''  const [heroPaused,setHeroPaused]=useState(false);
  const heroTouchStart=useRef<number|null>(null);
'''
if state_insert not in text:
    if state_anchor not in text:
        raise SystemExit("Traditions state anchor not found")
    text = text.replace(state_anchor, state_anchor + state_insert, 1)

# Replace the autoplay effect with an interaction-aware and reduced-motion-aware version.
effect_pattern = r'''  useEffect\(\(\)=>\{\n    const timer=window\.setInterval\(\(\)=>setSlide\(\(activeIndex\+1\)%heroSlides\.length\),6500\);\n    return\(\)=>window\.clearInterval\(timer\);\n  \},\[activeIndex,setSlide,heroSlides\.length\]\);'''
effect_replacement = '''  useEffect(()=>{
    if(heroPaused||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),6500);
    return()=>window.clearInterval(timer);
  },[activeIndex,setSlide,heroSlides.length,heroPaused]);

  const shiftHero=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);'''
if re.search(effect_pattern, text):
    text = re.sub(effect_pattern, effect_replacement, text, count=1)
elif 'const shiftHero=' not in text:
    raise SystemExit("Home hero autoplay effect not found")

# Full hero is still a section; behavior adds pause on hover/focus and swipe on touch.
plain_hero = '<section className="hv4-hero" aria-label="Главные разделы">'
interactive_hero = '''<section className="hv4-hero" aria-label="Главные разделы"
      onPointerEnter={()=>setHeroPaused(true)} onPointerLeave={()=>setHeroPaused(false)}
      onFocusCapture={()=>setHeroPaused(true)} onBlurCapture={()=>setHeroPaused(false)}
      onTouchStart={event=>{heroTouchStart.current=event.touches[0]?.clientX??null;setHeroPaused(true)}}
      onTouchEnd={event=>{const start=heroTouchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shiftHero(end<start?1:-1);heroTouchStart.current=null;setHeroPaused(false)}}>'''
if plain_hero in text:
    text = text.replace(plain_hero, interactive_hero, 1)

# Explicit CTA text and polite slide announcement.
old_copy = '<div className="hv4-hero-copy"><h1>{hero.title}</h1><button type="button" onClick={hero.action}><span>СМОТРЕТЬ</span><Icon name="arrow"/></button></div>'
new_copy = '<div className="hv4-hero-copy" aria-live="polite"><h1>{hero.title}</h1><button type="button" onClick={hero.action}><span>{hero.cta}</span><Icon name="arrow"/></button></div>'
if old_copy in text:
    text = text.replace(old_copy, new_copy, 1)

# Hero arrows are useful on desktop; mobile still has direct tabs and swipe.
old_controls = '<div className="hv4-hero-controls">\n        <nav className="hv4-hero-tabs" aria-label="Слайды главной">{heroSlides.map((item,index)=><button type="button" key={item.label} className={index===activeIndex?"active":""} onClick={()=>setSlide(index)}>{item.label}</button>)}</nav>\n      </div>'
new_controls = '''<div className="hv4-hero-controls">
        <nav className="hv4-hero-tabs" aria-label="Слайды главной">{heroSlides.map((item,index)=><button type="button" key={item.label} className={index===activeIndex?"active":""} aria-current={index===activeIndex?"true":undefined} onClick={()=>setSlide(index)}>{item.label}</button>)}</nav>
        <div className="hv4-hero-arrows" aria-label="Переключить баннер"><button type="button" aria-label="Предыдущий баннер" onClick={()=>shiftHero(-1)}><Icon name="arrow"/></button><button type="button" aria-label="Следующий баннер" onClick={()=>shiftHero(1)}><Icon name="arrow"/></button></div>
      </div>'''
if old_controls in text:
    text = text.replace(old_controls, new_controls, 1)

# Favorites must describe their current state for screen readers everywhere ProductCard is reused.
old_fav = 'aria-label="Добавить в избранное"'
new_fav = 'aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}'
if old_fav in text:
    text = text.replace(old_fav, new_fav, 1)

PAGE.write_text(text, encoding="utf-8")
print("Refined homepage V9: full-screen commercial hero, interaction-aware slider and responsive ecommerce behavior")
