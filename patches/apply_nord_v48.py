from pathlib import Path
import sys

p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V48_RESOURCE_SINGLETON' in s:
    raise SystemExit(0)

patch=r'''<style id="NORD_V48_RESOURCE_SINGLETON">
/* V48: hide every legacy resource renderer. Only .nord48-res is visible. */
.v38-raid-page .v20-counter,
.v38-raid-page .nord40-player-res,
.v38-raid-page .nord44-res,
.v38-raid-page .nord45-res,
.v38-raid-page .nord47-res{display:none!important;visibility:hidden!important;opacity:0!important;height:0!important;max-height:0!important;overflow:hidden!important;pointer-events:none!important}
.v38-raid-page .nord48-res{display:grid!important;visibility:visible!important;opacity:1!important}
.nord48-res{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important;margin-top:8px!important;width:100%!important}
.nord48-res .r{min-height:38px!important;padding:5px!important;border:1px solid #29434a!important;border-radius:10px!important;background:#09161b!important;text-align:center!important}
.nord48-res .r b{display:block!important;color:#e5d6b6!important;font-size:9px!important;white-space:nowrap!important}
.nord48-res .r i{display:block!important;height:4px!important;margin-top:4px!important;border-radius:99px!important;background:#18282d!important;overflow:hidden!important}
.nord48-res .r em{display:block!important;height:100%!important;border-radius:99px!important}
.nord48-res .h em{background:#d85c68}.nord48-res .m em{background:#5f9dde}.nord48-res .st em{background:#57bd83}
</style>
<script id="NORD_V48_RESOURCE_SINGLETON">
(function(){
  'use strict';
  var last={hp:null,mh:null,mp:null,mm:null,st:null,sm:null};
  var started=false;
  function n(v){var x=Number(v);return Number.isFinite(x)?x:null}
  function heroObj(){try{return typeof hero==='function'?(hero()||{}):{}}catch(e){return {}}}
  function raidObj(p){return p&&p._v20Raid&&typeof p._v20Raid==='object'?p._v20Raid:{}}
  function numText(el){var m=(el&&el.textContent||'').match(/(\d+)\s*\/\s*(\d+)/);return m?[+m[1],+m[2]]:null}
  function take(obj,keys,fallback){for(var i=0;i<keys.length;i++){if(obj&&obj[keys[i]]!==undefined&&obj[keys[i]]!==null){var x=n(obj[keys[i]]);if(x!==null)return x}}return fallback}
  function read(){
    var page=document.querySelector('.v38-raid-page');if(!page)return null;
    var p=heroObj(),a=raidObj(p);
    var player=page.querySelector('.v38-player-card');
    var pair=player?numText(player.querySelector('strong')):null;
    var hp=take(a,['hp','health'],null); if(hp===null)hp=take(p,['hp','health'],null); if(pair)hp=pair[0];
    var mh=take(a,['maxHp','maxHealth'],null); if(mh===null)mh=take(p,['maxHp','maxHealth'],null); if(pair)mh=pair[1];
    var mp=take(p,['mp','mana','magic'],null),mm=take(p,['maxMp','maxMana','maxMagic'],null);
    var st=take(a,['st','stamina','energy'],null); if(st===null)st=take(p,['st','stamina','energy'],null);
    var sm=take(a,['maxSt','maxStamina','maxEnergy'],null); if(sm===null)sm=take(p,['maxSt','maxStamina','maxEnergy'],null);
    /* Reject transient invalid states. Do not accept 0/maximum while a real value is already known. */
    if(hp!==null){ if(last.hp===null || hp>0 || last.hp===0) last.hp=Math.max(0,hp) }
    if(mh!==null && mh>0)last.mh=mh;
    if(mp!==null){ if(last.mp===null || mp>0 || last.mp===0) last.mp=Math.max(0,mp) }
    if(mm!==null && mm>0)last.mm=mm;
    if(st!==null){ if(last.st===null || st>0 || last.st===0) last.st=Math.max(0,st) }
    if(sm!==null && sm>0)last.sm=sm;
    if(last.hp!==null&&last.mh!==null&&last.hp>last.mh)last.hp=last.mh;
    if(last.mp!==null&&last.mm!==null&&last.mp>last.mm)last.mp=last.mm;
    if(last.st!==null&&last.sm!==null&&last.st>last.sm)last.st=last.sm;
    return {page:page,player:player}
  }
  function pct(v,m){return m?Math.max(0,Math.min(100,Math.round(v/m*100))):0}
  function render(){
    var x=read();if(!x||!x.player)return;
    var old=x.player.querySelectorAll('.nord40-player-res,.nord44-res,.nord45-res,.nord47-res');
    for(var i=0;i<old.length;i++){old[i].style.display='none';old[i].setAttribute('aria-hidden','true')}
    var res=x.player.querySelector('.nord48-res');
    if(!res){res=document.createElement('div');res.className='nord48-res';x.player.appendChild(res)}
    /* Do not render incomplete values. This avoids visual transitions through 0/undefined. */
    if(last.hp===null||last.mh===null||last.mp===null||last.mm===null||last.st===null||last.sm===null)return;
    var html='<div class="r h"><b>❤️ '+last.hp+'/'+last.mh+'</b><i><em style="width:'+pct(last.hp,last.mh)+'%"></em></i></div>'+\
      '<div class="r m"><b>🔷 '+last.mp+'/'+last.mm+'</b><i><em style="width:'+pct(last.mp,last.mm)+'%"></em></i></div>'+\
      '<div class="r st"><b>🟢 '+last.st+'/'+last.sm+'</b><i><em style="width:'+pct(last.st,last.sm)+'%"></em></i></div>';
    if(res.innerHTML!==html)res.innerHTML=html;
  }
  setInterval(render,100);
  setTimeout(render,0);setTimeout(render,80);setTimeout(render,250);setTimeout(render,500);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')
