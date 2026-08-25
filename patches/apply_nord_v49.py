from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V49_SINGLE_RESOURCE' in s: raise SystemExit(0)
patch=r'''<style id="NORD_V49_SINGLE_RESOURCE">
/* V49: one authoritative resource panel and one XP bar only. */
.v38-raid-page .v20-counter,.v38-raid-page .nord44-xp{display:none!important;visibility:hidden!important;height:0!important;overflow:hidden!important}
.v38-player-card .nord44-xp{display:none!important}
.v38-player-card .nord40-player-res.nord45-res.nord47-res{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important;width:100%!important;margin-top:7px!important;visibility:visible!important;opacity:1!important}
.nord49-res{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important;width:100%!important;margin-top:7px!important}
.nord49-res .r{min-height:38px!important;padding:5px!important;border:1px solid #29434a!important;border-radius:10px!important;background:#09161b!important;text-align:center!important}
.nord49-res b{display:block!important;color:#e5d6b6!important;font-size:9px!important;white-space:nowrap!important}.nord49-res i{display:block!important;height:4px!important;margin-top:4px!important;border-radius:99px!important;background:#18282d!important;overflow:hidden!important}.nord49-res em{display:block!important;height:100%!important;border-radius:99px!important}.nord49-res .h em{background:#d85c68}.nord49-res .m em{background:#5f9dde}.nord49-res .st em{background:#57bd83}
.nord49-xp{margin-top:7px!important;padding:6px 8px!important;border:1px solid #3a4b3f!important;border-radius:10px!important;background:#0b1714!important}.nord49-xp-head{display:flex!important;justify-content:space-between!important;color:#b9c3bc!important;font-size:8px!important;margin-bottom:4px!important}.nord49-xp-head b{color:#ead8b4!important;font-size:9px!important}.nord49-xpbar{height:6px!important;border-radius:99px!important;background:#18251f!important;overflow:hidden!important}.nord49-xpbar i{display:block!important;height:100%!important;border-radius:99px!important;background:linear-gradient(90deg,#8f7a42,#d8bb72)!important}
</style>
<script id="NORD_V49_SINGLE_RESOURCE">
(function(){
  'use strict';
  window.NORD_RES_LOCK=true;
  var last={hp:null,mh:null,mp:null,mm:null,st:null,sm:null,xp:null,next:null};
  function n(v){var x=Number(v);return isFinite(x)?x:null}
  function pick(o,ks,old){for(var i=0;i<ks.length;i++){if(o&&o[ks[i]]!=null){var x=n(o[ks[i]]);if(x!=null)return x}}return old}
  function p(){try{return typeof hero==='function'?(hero()||{}):{}}catch(e){return {}}}
  function render(){
    var page=document.querySelector('.v38-raid-page'),card=page&&page.querySelector('.v38-player-card');if(!card)return;
    var o=p(),r=o._v20Raid||{};
    var strong=card.querySelector('strong'),m=strong&&(strong.textContent||'').match(/(\d+)\s*\/\s*(\d+)/);
    if(m){last.hp=+m[1];last.mh=+m[2]}
    last.hp=pick(r,['hp','health','currentHp'],pick(o,['hp','health','currentHp'],last.hp));
    last.mh=pick(r,['maxHp','maxHealth'],pick(o,['maxHp','maxHealth'],last.mh));
    last.mp=pick(o,['mp','mana','currentMana','magic','currentMagic'],last.mp);
    last.mm=pick(o,['maxMp','maxMana','manaMax','maxMagic'],last.mm);
    last.st=pick(r,['st','stamina','currentStamina','endurance'],pick(o,['st','stamina','currentStamina','endurance','energy'],last.st));
    last.sm=pick(r,['maxSt','maxStamina','maxEndurance'],pick(o,['maxSt','maxStamina','maxEndurance'],last.sm));
    last.xp=pick(o,['xp','exp','experience'],last.xp);last.next=pick(o,['xpToNext','nextXp','xpMax','expToNext'],last.next);
    if(last.hp==null||last.mh==null)return;
    if(last.mp==null||last.mm==null)return;
    if(last.st==null||last.sm==null)return;
    last.hp=Math.max(0,Math.min(last.mh,last.hp));last.mp=Math.max(0,Math.min(last.mm,last.mp));last.st=Math.max(0,Math.min(last.sm,last.st));
    var old=card.querySelector('.nord40-player-res');
    var res=old;if(!res){res=document.createElement('div');res.className='nord40-player-res nord49-res';card.appendChild(res)}res.className='nord40-player-res nord49-res';
    function pc(v,m){return Math.max(0,Math.min(100,Math.round(v/m*100)))}
    var html='<div class="r h"><b>❤️ '+last.hp+'/'+last.mh+'</b><i><em style="width:'+pc(last.hp,last.mh)+'%"></em></i></div><div class="r m"><b>🔷 '+last.mp+'/'+last.mm+'</b><i><em style="width:'+pc(last.mp,last.mm)+'%"></em></i></div><div class="r st"><b>🟢 '+last.st+'/'+last.sm+'</b><i><em style="width:'+pc(last.st,last.sm)+'%"></em></i></div>';
    if(res.innerHTML!==html)res.innerHTML=html;
    var boxes=card.querySelectorAll('.nord45-xp,.nord44-xp,.nord49-xp');for(var i=0;i<boxes.length;i++)boxes[i].remove();
    if(last.xp!=null&&last.next!=null){var xp=document.createElement('div');xp.className='nord49-xp';xp.innerHTML='<div class="nord49-xp-head"><span>⭐ ОПЫТ</span><b>'+Math.max(0,last.xp)+'/'+Math.max(1,last.next)+' XP</b></div><div class="nord49-xpbar"><i style="width:'+pc(last.xp,last.next)+'%"></i></div>';card.appendChild(xp)}
    var tops=page.querySelectorAll('.v20-counter');for(var j=0;j<tops.length;j++)tops[j].remove();
  }
  setInterval(render,500);setTimeout(render,100);setTimeout(render,500);setTimeout(render,1200);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')