from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V42_FREEZE_FIX' in s:
    raise SystemExit(0)
marker='<!-- NORD_V42_FREEZE_FIX -->'
# V40 used a MutationObserver on the whole document while its refresh() function
# mutates that same document. That creates a mutation -> refresh -> mutation loop,
# which can starve the main thread exactly when the raid hub/run is rendered.
old="new MutationObserver(function(){refresh()}).observe(document.documentElement,{childList:true,subtree:true});"
if old in s:
    s=s.replace(old, "/* NORD_V42_FREEZE_FIX: disable document-wide observer; polling remains. */", 1)
# Also make the remaining 700ms polling cheaper: only update when the resource HTML changed.
old1="x.innerHTML='<div class=\"r nord40-h\"><b>❤️ '+hp+'/'+mh+'</b><i><em style=\"width:'+pct(hp,mh)+'%\"></em></i></div><div class=\"r nord40-m\"><b>🔷 '+mp+'/'+mm+'</b><i><em style=\"width:'+pct(mp,mm)+'%\"></em></i></div><div class=\"r nord40-s\"><b>🟢 '+st+'/'+sm+'</b><i><em style=\"width:'+pct(st,sm)+'%\"></em></i></div>';"
new1="var h='<div class=\"r nord40-h\"><b>❤️ '+hp+'/'+mh+'</b><i><em style=\"width:'+pct(hp,mh)+'%\"></em></i></div><div class=\"r nord40-m\"><b>🔷 '+mp+'/'+mm+'</b><i><em style=\"width:'+pct(mp,mm)+'%\"></em></i></div><div class=\"r nord40-s\"><b>🟢 '+st+'/'+sm+'</b><i><em style=\"width:'+pct(st,sm)+'%\"></em></i></div>';if(x.innerHTML!==h)x.innerHTML=h;"
if old1 in s:
    s=s.replace(old1,new1,1)
old2="old.innerHTML='<div class=\"r h\"><b>❤️ '+hp+'/'+mh+'</b><i><em style=\"width:'+pct(hp,mh)+'%\"></em></i></div><div class=\"r m\"><b>🔷 '+mp+'/'+mm+'</b><i><em style=\"width:'+pct(mp,mm)+'%\"></em></i></div><div class=\"r s\"><b>🟢 '+st+'/'+sm+'</b><i><em style=\"width:'+pct(st,sm)+'%\"></em></i></div>';"
new2="var ph='<div class=\"r h\"><b>❤️ '+hp+'/'+mh+'</b><i><em style=\"width:'+pct(hp,mh)+'%\"></em></i></div><div class=\"r m\"><b>🔷 '+mp+'/'+mm+'</b><i><em style=\"width:'+pct(mp,mm)+'%\"></em></i></div><div class=\"r s\"><b>🟢 '+st+'/'+sm+'</b><i><em style=\"width:'+pct(st,sm)+'%\"></em></i></div>';if(old.innerHTML!==ph)old.innerHTML=ph;"
if old2 in s:
    s=s.replace(old2,new2,1)
# Record that the fix was applied so the workflow is idempotent.
s=s.replace('</head>', marker+'<style id=\"NORD_V42_FREEZE_FIX\">.v38-raid-page button{touch-action:manipulation!important}</style></head>',1)
p.write_text(s,encoding='utf-8')
