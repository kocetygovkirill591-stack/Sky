from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V40_UI_FIX' in s:
    raise SystemExit(0)
patch=r'''<style id="NORD_V40_UI_FIX">
/* Remove the oversized resource box added by V39. */
.v38-raid-page .nord39-top{display:none!important}
.v38-raid-page .v20-counter{width:auto!important;min-width:0!important;max-width:none!important;height:auto!important;min-height:0!important;margin:6px 0 7px!important;padding:6px 8px!important;display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important;border:0!important;background:transparent!important;box-shadow:none!important;border-radius:0!important;color:#d9e1df!important}
.v38-raid-page .v20-counter>span,.v38-raid-page .v20-counter>b,.v38-raid-page .v20-counter>small{display:none!important}
.nord40-res{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px;grid-column:1/-1;width:100%}
.nord40-res .r{padding:6px 7px;border:1px solid #29434a;border-radius:11px;background:linear-gradient(160deg,#0b1a20,#071217);font-size:8px;color:#b8c4c1;text-align:center}
.nord40-res .r b{display:block;color:#ead8b4;font-size:10px}
.nord40-res .r i{display:block;height:4px;margin-top:4px;border-radius:99px;background:#17252a;overflow:hidden}
.nord40-res .r em{display:block;height:100%;border-radius:99px}
.nord40-h em{background:#da5d69}.nord40-m em{background:#5d9bdd}.nord40-s em{background:#58bd83}
.v38-player-card .v20-hpbar.hero{display:none!important}
.nord40-player-res{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px;margin-top:7px}
.nord40-player-res .r{padding:5px;border:1px solid #243b40;border-radius:9px;background:#091419;text-align:center;color:#839996;font-size:7px}
.nord40-player-res b{display:block;color:#d9e1df;font-size:9px}
.nord40-player-res i{display:block;height:3px;margin-top:3px;border-radius:99px;background:#18272c;overflow:hidden}
.nord40-player-res em{display:block;height:100%;border-radius:99px}
.nord40-player-res .h em{background:#d85c68}.nord40-player-res .m em{background:#5f9dde}.nord40-player-res .s em{background:#57bd83}
</style>
<script id="NORD_V40_UI_FIX">
(function(){
function state(){try{return JSON.parse(localStorage.getItem('nord_rpg_save_v7')||'{}')}catch(e){return {}}}
function pct(v,m){v=Math.max(0,+v||0);m=Math.max(1,+m||1);return Math.max(0,Math.min(100,v/m*100))}
function resourceRow(){
  var d=state(),p={}; try{if(typeof hero==='function')p=hero()||{}}catch(e){}
  var hp=+((p._v20Raid||{}).hp||p.hp||0),mh=+((p._v20Raid||{}).maxHp||p.maxHp||108),mp=+(p.mp||d.mp||0),mm=+(p.maxMp||d.maxMp||50),st=+((p._v20Raid||{}).st||p.st||0),sm=+(p.maxSt||d.maxSt||118);
  var el=document.querySelector('.v38-raid-page .v20-counter');if(!el)return;
  var x=el.querySelector('.nord40-res');if(!x){x=document.createElement('div');x.className='nord40-res';el.appendChild(x)}
  x.innerHTML='<div class="r nord40-h"><b>❤️ '+hp+'/'+mh+'</b><i><em style="width:'+pct(hp,mh)+'%"></em></i></div><div class="r nord40-m"><b>🔷 '+mp+'/'+mm+'</b><i><em style="width:'+pct(mp,mm)+'%"></em></i></div><div class="r nord40-s"><b>🟢 '+st+'/'+sm+'</b><i><em style="width:'+pct(st,sm)+'%"></em></i></div>';
}
function playerRow(){
  var card=document.querySelector('.v38-player-card');if(!card)return;
  var d=state(),p={};try{if(typeof hero==='function')p=hero()||{}}catch(e){}
  var a=p._v20Raid||{},hp=+((a.hp!=null)?a.hp:(p.hp||0)),mh=+((a.maxHp!=null)?a.maxHp:(p.maxHp||108)),mp=+(p.mp||d.mp||0),mm=+(p.maxMp||d.maxMp||50),st=+(p.st||a.st||0),sm=+(p.maxSt||d.maxSt||118);
  var old=card.querySelector('.nord40-player-res');if(!old){old=document.createElement('div');old.className='nord40-player-res';card.appendChild(old)}
  old.innerHTML='<div class="r h"><b>❤️ '+hp+'/'+mh+'</b><i><em style="width:'+pct(hp,mh)+'%"></em></i></div><div class="r m"><b>🔷 '+mp+'/'+mm+'</b><i><em style="width:'+pct(mp,mm)+'%"></em></i></div><div class="r s"><b>🟢 '+st+'/'+sm+'</b><i><em style="width:'+pct(st,sm)+'%"></em></i></div>';
}
function refresh(){resourceRow();playerRow()}
new MutationObserver(function(){refresh()}).observe(document.documentElement,{childList:true,subtree:true});
setInterval(refresh,700);setTimeout(refresh,100);setTimeout(refresh,400);
})();
</script>
<script id="NORD_V40_COMBAT_SFX">
(function(){
var AC=null;
function ctx(){try{AC=AC||new(window.AudioContext||window.webkitAudioContext)();if(AC.state==='suspended')AC.resume();return AC}catch(e){return null}}
function hit(){var a=ctx();if(!a)return;var t=a.currentTime,o=a.createOscillator(),g=a.createGain();o.type='sawtooth';o.frequency.setValueAtTime(520,t);o.frequency.exponentialRampToValueAtTime(110,t+.09);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.08,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+.12);o.connect(g).connect(a.destination);o.start(t);o.stop(t+.13)}
function clang(){var a=ctx();if(!a)return;var t=a.currentTime;[720,1080].forEach(function(f,i){var o=a.createOscillator(),g=a.createGain();o.type='square';o.frequency.value=f;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.045,t+.005);g.gain.exponentialRampToValueAtTime(.0001,t+.16+i*.02);o.connect(g).connect(a.destination);o.start(t);o.stop(t+.18)})}
function potion(){var a=ctx();if(!a)return;var t=a.currentTime,o=a.createOscillator(),g=a.createGain();o.type='sine';o.frequency.setValueAtTime(180,t);o.frequency.linearRampToValueAtTime(430,t+.25);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.05,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+.28);o.connect(g).connect(a.destination);o.start(t);o.stop(t+.3)}
function magic(){var a=ctx();if(!a)return;var t=a.currentTime,o=a.createOscillator(),g=a.createGain();o.type='triangle';o.frequency.setValueAtTime(360,t);o.frequency.exponentialRampToValueAtTime(760,t+.2);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.04,t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+.24);o.connect(g).connect(a.destination);o.start(t);o.stop(t+.25)}
document.addEventListener('pointerdown',function(e){var b=e.target.closest('[data-v20-action]');if(!b)return;var a=b.getAttribute('data-v20-action'),id=b.getAttribute('data-id');if(a==='combat'){id==='potion'?potion():id==='defend'?clang():hit()}else if(a==='event'){magic()}},{capture:true,passive:true});
})();
</script>'''
s=s.replace('</body>',patch+'</body>',1)
p.write_text(s,encoding='utf-8')
