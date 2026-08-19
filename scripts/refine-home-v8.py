from pathlib import Path

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Keep a local play/pause state for the 15-second brand story.
state_anchor = '  const hero=heroSlides[activeIndex];\n'
state_line = '  const [traditionsPlaying,setTraditionsPlaying]=useState(true);\n'
if state_line not in text:
    if state_anchor not in text:
        raise SystemExit("Home hero state anchor not found")
    text = text.replace(state_anchor, state_anchor + state_line, 1)

# Refine hero CTA with an inline arrow while preserving the existing action.
old_hero = '<div className="hv4-hero-copy"><h1>{hero.title}</h1><button type="button" onClick={hero.action}>СМОТРЕТЬ</button></div>'
new_hero = '<div className="hv4-hero-copy"><h1>{hero.title}</h1><button type="button" onClick={hero.action}><span>СМОТРЕТЬ</span><Icon name="arrow"/></button></div>'
if old_hero in text:
    text = text.replace(old_hero, new_hero, 1)

# Bind the current 15-second motion story to play/pause state.
plain_media = '<div className="hv4-traditions-media">'
stateful_media = '<div className={`hv4-traditions-media ${traditionsPlaying?"is-playing":"is-paused"}`}> '
if plain_media in text:
    text = text.replace(plain_media, stateful_media, 1)

copy_block = '<div className="hv4-traditions-copy"><div><small>BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>'
player_block = '''<div className="hv4-video-controls" aria-label="Управление историей">
            <button type="button" className="hv4-video-toggle" onClick={()=>setTraditionsPlaying(value=>!value)} aria-label={traditionsPlaying?"Поставить видео на паузу":"Продолжить видео"}>
              {traditionsPlaying?<span className="hv4-pause-icon" aria-hidden="true"><i/><i/></span>:<span className="hv4-play-icon" aria-hidden="true"/>}
            </button>
            <span className="hv4-video-track" aria-hidden="true"><i/></span>
            <small>0:15</small>
          </div>'''
if 'className="hv4-video-controls"' not in text:
    if copy_block not in text:
        raise SystemExit("Traditions copy block not found")
    text = text.replace(copy_block, copy_block + '\n          ' + player_block, 1)

PAGE.write_text(text, encoding="utf-8")
print("Refined homepage V8: smaller hero, catalog-style favorite and subtle 15s story player")
