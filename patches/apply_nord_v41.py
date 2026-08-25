from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V41_RAID_START_FIX' in s:
    raise SystemExit(0)
# Expose the existing startRaid function without changing its local name/signature.
s=s.replace('const startRaid=', 'const startRaid=window.__nordStartRaid=', 1)
patch=r'''<style id="NORD_V41_RAID_START_FIX">.v20-choice[data-v20-action="startRaid"],button[data-v20-action="startRaid"],button[data-action="startRaid"]{touch-action:manipulation!important;pointer-events:auto!important;position:relative!important;z-index:30!important}</style><script id="NORD_V41_RAID_START_FIX">(function(){
function getId(b){return b.getAttribute('data-id')||b.getAttribute('data-cave')||b.getAttribute('data-cave-id')||((b.closest('[data-id]')||{}).getAttribute&&b.closest('[data-id]').getAttribute('data-id'))||null}
function isStart(b){var t=(b.innerText||b.textContent||'').replace(/\s+/g,' ').trim().toUpperCase();return t.indexOf('НАЧАТЬ РЕЙД')>=0}
document.addEventListener('click',function(e){var b=e.target.closest('button');if(!b||!isStart(b))return;var id=getId(b);try{if(typeof window.__nordStartRaid==='function'){e.preventDefault();e.stopImmediatePropagation();window.__nordStartRaid(id);return}}catch(err){console.error('NORD raid start failed',err)}},true);
})();</script>'''
s=s.replace('</body>',patch+'</body>',1)
p.write_text(s,encoding='utf-8')
