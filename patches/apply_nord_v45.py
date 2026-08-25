from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V45_RESOURCE_FINAL' in s:
    raise SystemExit(0)
patch=r'''<style id="NORD_V45_RESOURCE_FINAL">
/* V45: no resource block above events; one authoritative compact block in combat card. */
.v38-raid-page .v20-counter{display:none!important;height:0!important;min-height:0!important;margin:0!important;padding:0!important;overflow:hidden!important}
.v38-raid-page .v20-counter:before,.v38-raid-page .v20-counter:after{display:none!important;content:none!important}
.v38-player-card .v20-hpbar.hero{display:none!important}
.v38-player-card .nord40-player-res{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important;margin-top:7px!important}
.v38-player-card .v38-player-stats span:nth-child(3){display:none!important}
.v38-player-card .v38-player-stats{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.nord45-res .r{min-height:38px!important;padding:5px!important;border:1px solid #29434a!important;border-radius:10px!important;background:#09161b!important;text-align:center!important}
.nord45-res .r b{display:block!important;color:#e5d6b6!important;font-size:9px!important;white-space:nowrap!important}
.nord45-res .r i{display:block!important;height:4px!important;margin-top:4px!important;border-radius:99px!important;background:#18282d!important;overflow:hidden!important}
.nord45-res .r em{display:block!important;height:100%!important;border-radius:99px!important}
.nord45-res .h em{background:#d85c68}.nord45-res .m em{background:#5f9dde}.nord45-res .st em{background:#57bd83}
.nord45-xp{margin-top:7px!important;padding:6px 8px!important;border:1px solid #3a4b3f!important;border-radius:10px!important;background:#0b1714!important}
.nord45-xp-head{display:flex!important;justify-content:space-between!important;color:#b9c3bc!important;font-size:8px!important;margin-bottom:4px!important}
.nord45-xp-head b{color:#ead8b4!important;font-size:9px!important}.nord45-xpbar{height:6px!important;border-radius:99px!important;background:#18251f!important;overflow:hidden!important}.nord45-xpbar i{display:block!important;height:100%!important;border-radius:99px!important;background:linear-gradient(90deg,#8f7a42,#d8bb72)!important}
/* In event state the resources are intentionally absent; the event itself stays compact. */
.v38-raid-page .v38-event ~ .v38-log{margin-top:7px!important}
</style>
<script id="NORD_V45_RESOURCE_FINAL">
(function(){
  function finite(v){var n=Number(v);return isFinite(n)?n:null}
  function pick(o,keys,fallback){for(var i=0;i<keys.length;i++){if(o&&o[keys[i]]!==undefined&&o[keys[i]]!==null){var n=finite(o[keys[i]]);if(n!==null)return n}}return fallback}
  function player(){try{return typeof hero==='function'?(hero()||{}):{}}catch(e){return {}}}
  function raid(){var p=player();return p&&p._v20Raid?p._v20Raid:null}
  function save(){try{return JSON.parse(localStorage.getItem('nord_rpg_save_v7')||'{}')}catch(e){return {}}}
  function pairFromText(el){if(!el)return null;var m=(el.textContent||'').match(/(\d+)\s*\/\s*(\d+)/);return m?[+m[1],+m[2]]:null}
  function refresh(){
    var page=document.querySelector('.v38-raid-page');if(!page)return;
    /* Kill the obsolete top counter completely so no stale zero/heart/vertical line can survive. */
    var tops=page.querySelectorAll('.v20-counter');for(var i=0;i<tops.length;i++)tops[i].remove();
    var card=page.querySelector('.v38-player-card');if(!card)return;
    var p=player(),a=raid()||{},d=save();
    var hpPair=pairFromText(card.querySelector('strong'));
    var hp=hpPair?hpPair[0]:pick(a,['hp','health','currentHp'],pick(p,['hp','health','currentHp'],100));
    var mh=hpPair?hpPair[1]:pick(a,['maxHp','maxHealth'],pick(p,['maxHp','maxHealth'],108));
    var oldRes=card.querySelector('.nord40-player-res');
    var oldTxt=oldRes?oldRes.textContent:'';
    var oldMana=(oldTxt.match(/🔷\s*(\d+)\s*\/(\d+)/)||[]);var oldSt=(oldTxt.match(/🟢\s*(\d+)\s*\/(\d+)/)||[]);
    var mm=pick(p,['maxMp','maxMana','manaMax','maxMagic','magicMax'],pick(d,['maxMp','maxMana'],50));
    var mp=pick(p,['mp','mana','currentMana','magic','currentMagic'],oldMana[1]!==undefined?+oldMana[1]:50);
    var sm=pick(a,['maxSt','maxStamina','maxEndurance'],pick(p,['maxSt','maxStamina','maxEndurance','staminaMax','enduranceMax'],pick(d,['maxSt','maxStamina'],118)));
    var st=pick(a,['st','stamina','currentStamina','endurance','currentEndurance'],pick(p,['st','stamina','currentStamina','endurance','currentEndurance','energy'],oldSt[1]!==undefined?+oldSt[1]:118));
    mp=Math.max(0,Math.min(mm,mp));st=Math.max(0,Math.min(sm,st));hp=Math.max(0,Math.min(mh,hp));
    var res=oldRes;if(!res){res=document.createElement('div');res.className='nord40-player-res nord45-res';card.appendChild(res)}res.classList.add('nord45-res');
    var pct=function(v,m){return Math.max(0,Math.min(100,m?Math.round(v/m*100):0))};
    var html='<div class="r h"><b>❤️ '+hp+'/'+mh+'</b><i><em style="width:'+pct(hp,mh)+'%"></em></i></div><div class="r m"><b>🔷 '+mp+'/'+mm+'</b><i><em style="width:'+pct(mp,mm)+'%"></em></i></div><div class="r st"><b>🟢 '+st+'/'+sm+'</b><i><em style="width:'+pct(st,sm)+'%"></em></i></div>';
    if(res.innerHTML!==html)res.innerHTML=html;
    var xp=pick(p,['xp','exp','experience'],pick(d,['xp','exp'],0));
    var next=pick(p,['xpToNext','nextXp','xpMax','expToNext','expNext'],pick(d,['xpToNext','nextXp'],100)); if(next<=0)next=100;
    var box=card.querySelector('.nord45-xp');if(!box){box=document.createElement('div');box.className='nord45-xp';card.appendChild(box)}
    box.innerHTML='<div class="nord45-xp-head"><span>⭐ ОПЫТ</span><b>'+Math.max(0,xp)+'/'+next+' XP</b></div><div class="nord45-xpbar"><i style="width:'+pct(xp,next)+'%"></i></div>';
  }
  setInterval(refresh,700);setTimeout(refresh,80);setTimeout(refresh,350);setTimeout(refresh,900);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')