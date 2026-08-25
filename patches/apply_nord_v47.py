from pathlib import Path
import sys,re

p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V47_RESOURCE_STABLE' in s:
    raise SystemExit(0)

# Disable the V45 polling renderer. V47 becomes the single authoritative renderer.
s=s.replace("function refresh(){\n    var page=document.querySelector('.v38-raid-page');if(!page)return;", "function refresh(){\n    if(window.NORD_RES_LOCK)return;\n    var page=document.querySelector('.v38-raid-page');if(!page)return;", 1)

patch=r'''<style id="NORD_V47_RESOURCE_STABLE">
/* V47: the raid page has exactly one resource display, inside the player card. */
.v38-raid-page .v20-counter{display:none!important;visibility:hidden!important;height:0!important;max-height:0!important;min-height:0!important;width:0!important;max-width:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important;opacity:0!important;pointer-events:none!important}
.v38-raid-page .v20-counter *{display:none!important;visibility:hidden!important}
.v38-player-card .nord45-res{display:grid!important;visibility:visible!important;opacity:1!important;width:100%!important}
.nord47-res .r{min-height:38px!important;padding:5px!important;border:1px solid #29434a!important;border-radius:10px!important;background:#09161b!important;text-align:center!important}
.nord47-res .r b{display:block!important;color:#e5d6b6!important;font-size:9px!important;white-space:nowrap!important}
.nord47-res .r i{display:block!important;height:4px!important;margin-top:4px!important;border-radius:99px!important;background:#18282d!important;overflow:hidden!important}
.nord47-res .r em{display:block!important;height:100%!important;border-radius:99px!important}
.nord47-res .h em{background:#d85c68}.nord47-res .m em{background:#5f9dde}.nord47-res .st em{background:#57bd83}
</style>
<script id="NORD_V47_RESOURCE_STABLE">
(function(){
  'use strict';
  window.NORD_RES_LOCK=true;
  var last={hp:100,mh:108,mp:50,mm:50,st:100,sm:118};
  var active=false;
  function num(v){var n=Number(v);return isFinite(n)?n:null}
  function pct(v,m){return Math.max(0,Math.min(100,m?Math.round(v/m*100):0))}
  function heroObj(){try{return typeof hero==='function'?(hero()||{}):{}}catch(e){return {}}}
  function raidObj(p){return p&&p._v20Raid?p._v20Raid:{}}
  function pair(text){var m=(text||'').match(/(\d+)\s*\/\s*(\d+)/);return m?[+m[1],+m[2]]:null}
  function accept(v,key){var n=num(v);if(n!==null)return n;return last[key]}
  function read(){
    var p=heroObj(),a=raidObj(p), page=document.querySelector('.v38-raid-page');
    if(!page)return null;
    active=true;
    /* Only accept numeric state. Missing/undefined fields never become zero. */
    if(a.hp!==undefined&&a.hp!==null) last.hp=Math.max(0,num(a.hp));
    else if(p.hp!==undefined&&p.hp!==null) last.hp=Math.max(0,num(p.hp));
    if(a.maxHp!==undefined&&a.maxHp!==null) last.mh=Math.max(1,num(a.maxHp));
    else if(p.maxHp!==undefined&&p.maxHp!==null) last.mh=Math.max(1,num(p.maxHp));
    if(a.st!==undefined&&a.st!==null) last.st=Math.max(0,num(a.st));
    else if(a.stamina!==undefined&&a.stamina!==null) last.st=Math.max(0,num(a.stamina));
    else if(p.st!==undefined&&p.st!==null) last.st=Math.max(0,num(p.st));
    if(a.maxSt!==undefined&&a.maxSt!==null) last.sm=Math.max(1,num(a.maxSt));
    else if(p.maxSt!==undefined&&p.maxSt!==null) last.sm=Math.max(1,num(p.maxSt));
    if(p.mp!==undefined&&p.mp!==null) last.mp=Math.max(0,num(p.mp));
    else if(p.mana!==undefined&&p.mana!==null) last.mp=Math.max(0,num(p.mana));
    if(p.maxMp!==undefined&&p.maxMp!==null) last.mm=Math.max(1,num(p.maxMp));
    else if(p.maxMana!==undefined&&p.maxMana!==null) last.mm=Math.max(1,num(p.maxMana));
    /* If the underlying state is temporarily unavailable, preserve the last real value. */
    if(last.hp>last.mh)last.hp=last.mh;
    if(last.mp>last.mm)last.mp=last.mm;
    if(last.st>last.sm)last.st=last.sm;
    return page;
  }
  function render(){
    var page=read();if(!page)return;
    /* Remove the legacy top panel synchronously and via observer below. */
    var top=page.querySelector('.v20-counter');if(top)top.remove();
    var card=page.querySelector('.v38-player-card');if(!card)return;
    var res=card.querySelector('.nord45-res');
    if(!res){res=document.createElement('div');res.className='nord40-player-res nord45-res nord47-res';card.appendChild(res)}
    res.classList.add('nord47-res');
    var html='<div class="r h"><b>❤️ '+last.hp+'/'+last.mh+'</b><i><em style="width:'+pct(last.hp,last.mh)+'%"></em></i></div>'+
      '<div class="r m"><b>🔷 '+last.mp+'/'+last.mm+'</b><i><em style="width:'+pct(last.mp,last.mm)+'%"></em></i></div>'+
      '<div class="r st"><b>🟢 '+last.st+'/'+last.sm+'</b><i><em style="width:'+pct(last.st,last.sm)+'%"></em></i></div>';
    if(res.innerHTML!==html)res.innerHTML=html;
  }
  function hideTop(){
    var els=document.querySelectorAll('.v38-raid-page .v20-counter');
    for(var i=0;i<els.length;i++)els[i].remove();
  }
  var obs=new MutationObserver(function(){hideTop()});
  try{obs.observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
  setInterval(render,250);
  setTimeout(render,0);setTimeout(render,50);setTimeout(render,150);setTimeout(render,400);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')
