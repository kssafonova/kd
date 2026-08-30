from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

state_anchor = '  const [traditionsPlaying,setTraditionsPlaying]=useState(true);\n'
state_block = '''  const traditionsVideoRef=useRef<HTMLVideoElement>(null);
  const [traditionsProgress,setTraditionsProgress]=useState(0);
  const [traditionsDuration,setTraditionsDuration]=useState(12.7);
'''
if state_block not in text:
    if state_anchor not in text:
        raise SystemExit("Traditions state anchor not found")
    text = text.replace(state_anchor, state_anchor + state_block, 1)

helper_anchor = '  const scrollHomeRail=(id:string,direction:-1|1)=>{\n'
helper = '''  const toggleTraditionsVideo=()=>{
    const video=traditionsVideoRef.current;
    if(!video)return;
    if(video.paused){void video.play();setTraditionsPlaying(true)}
    else{video.pause();setTraditionsPlaying(false)}
  };

'''
if helper not in text:
    if helper_anchor not in text:
        raise SystemExit("Home rail helper anchor not found")
    text = text.replace(helper_anchor, helper + helper_anchor, 1)

images_pattern = re.compile(r'''          <img src=\{assetUrl\("/assets/images/russian-bedroom\.png"\)\} alt="Современная русская спальня"/>\n          <img src=\{assetUrl\("/assets/images/editorial-table\.webp"\)\} alt="Сервировка дома"/>\n          <img src=\{assetUrl\("/assets/images/time-hero\.png"\)\} alt="Предметы Культура дома"/>''')
video_markup = '''          <video ref={traditionsVideoRef} className="hv4-traditions-video" autoPlay loop muted playsInline preload="metadata" poster={assetUrl("/assets/images/russian-bedroom.png")}
            onPlay={()=>setTraditionsPlaying(true)} onPause={()=>setTraditionsPlaying(false)}
            onLoadedMetadata={event=>setTraditionsDuration(event.currentTarget.duration||12.7)}
            onTimeUpdate={event=>{const video=event.currentTarget;setTraditionsProgress(video.duration?video.currentTime/video.duration:0)}}>
            <source media="(max-width: 700px)" src={assetUrl("/videos/home-mobile.mp4")} type="video/mp4"/>
            <source src={assetUrl("/videos/home-desktop.mp4")} type="video/mp4"/>
          </video>'''
if 'className="hv4-traditions-video"' not in text:
    text, count = images_pattern.subn(video_markup, text, count=1)
    if count != 1:
        raise SystemExit("Traditions image sequence not found")

toggle_old = 'onClick={()=>setTraditionsPlaying(value=>!value)}'
if toggle_old in text:
    text = text.replace(toggle_old, 'onClick={toggleTraditionsVideo}', 1)

track_old = '<span className="hv4-video-track" aria-hidden="true"><i/></span>\n            <small>0:15</small>'
track_new = '<span className="hv4-video-track" aria-hidden="true"><i style={{transform:`scaleX(${traditionsProgress})`}}/></span>\n            <small>{`0:${String(Math.round(traditionsDuration)).padStart(2,"0")}`}</small>'
if track_old in text:
    text = text.replace(track_old, track_new, 1)
elif 'traditionsProgress' not in text.split('className="hv4-video-track"',1)[-1][:300]:
    raise SystemExit("Traditions progress controls not found")

PAGE.write_text(text, encoding="utf-8")
print("Homepage V11: responsive desktop/mobile video replaces CSS motion story")
