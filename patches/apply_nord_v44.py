from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V44_RAID_CLEANUP' in s:
    raise SystemExit(0)
patch=r'''<style id="NORD_V44_RAID_CLEANUP">
/* V44: one resource block only, inside the hero card. Remove the misleading top copy. */
.v38-raid-page .v20-counter{display:none!important}
.v38-player-card .v20-hpbar.hero{display:none!important}
.v38-player-card .v38-player-stats span:nth-child(3){display:none!important}
.v38-player-card .v38-player-stats{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.v38-player-card .nord40-player-res{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important;margin-top:8px!important}
.nord44-res .r{min-height:40px!important;padding:6px!important;border:1px solid #29434a!important;border-radius:10px!important;background:linear-gradient(160deg,#0b1a20,#071217)!important;text-align:center!important;color:#a9b9b6!important}
.nord44-res .r b{display:block!important;color:#e5d6b6!important;font-size:9px!important}
.nord44-res .r i{display:block!important;height:4px!important;margin-top:4px!important;border-radius:99px!important;background:#18282d!important;overflow:hidden!important}
.nord44-res .r em{display:block!important;height:100%!important;border-radius:99px!important}
.nord44-res .h em{background:#d85c68}.nord44-res .m em{background:#5f9dde}.nord44-res .st em{background:#57bd83}
.nord44-xp{margin-top:8px;padding:7px 8px;border:1px solid #3a4b3f;border-radius:11px;background:linear-gradient(160deg,#111d19,#091411)}
.nord44-xp-head{display:flex;justify-content:space-between;gap:8px;color:#b9c3bc;font-size:8px;margin-bottom:5px}
.nord44-xp-head b{color:#ead8b4;font-size:9px}.nord44-xpbar{height:7px;border-radius:99px;background:#18251f;overflow:hidden}.nord44-xpbar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#8f7a42,#d8bb72);width:0%}
</style>
<script id="NORD_V44_RAID_CLEANUP">
(function(){
  function pct(v,m){v=Math.max(0,+v||0);m=Math.max(1,+m||1);return Math.max(0,Math.min(100,v/m*100))}
  function num(v,d){var n=Number(v);return isFinite(n)?n:d}
  function player(){try{return typeof hero==='function'?(hero()||{}):{}}catch(e){return {}}}
  function save(){try{return JSON.parse(localStorage.getItem('nord_rpg_save_v7')||'{}')}catch(e){return {}}}
  function refresh(){
    var card=document.querySelector('.v38-player-card');if(!card)return;
    var p=player(),a=p._v20Raid||{},d=save();
    var hp=num(a.hp,p.hp),mh=num(a.maxHp,p.maxHp||108);
    var mp=num(p.mp,d.mp||0),mm=num(p.maxMp,d.maxMp||50);
    var st=num(a.st,p.st),sm=num(a.maxSt,p.maxSt||d.maxSt||118);
    var res=card.querySelector('.nord40-player-res');
    if(!res){res=document.createElement('div');res.className='nord40-player-res nord44-res';card.appendChild(res)}
    res.classList.add('nord44-res');
    var html='<div class="r h"><b>❤️ '+hp+'/'+mh+'</b><i><em style="width:'+pct(hp,mh)+'%"></em></i></div>'+
      '<div class="r m"><b>🔷 '+mp+'/'+mm+'</b><i><em style="width:'+pct(mp,mm)+'%"></em></i></div>'+
      '<div class="r st"><b>🟢 '+st+'/'+sm+'</b><i><em style="width:'+pct(st,sm)+'%"></em></i></div>';
    if(res.innerHTML!==html)res.innerHTML=html;
    var xp=num(p.xp,num(p.exp,num(p.experience,num(d.xp,0))));
    var next=num(p.xpToNext,num(p.nextXp,num(p.xpMax,num(p.expToNext,num(p.expNext,num(d.xpToNext,100))))));
    if(next<=0)next=100;
    var level=num(p.level,1), shown=Math.max(0,xp), max=Math.max(1,next);
    var box=card.querySelector('.nord44-xp');
    if(!box){box=document.createElement('div');box.className='nord44-xp';card.appendChild(box)}
    box.innerHTML='<div class="nord44-xp-head"><span>⭐ ОПЫТ</span><b>'+shown+'/'+max+' XP</b></div><div class="nord44-xpbar"><i style="width:'+pct(shown,max)+'%"></i></div>';
    /* The original resource row is now the single authoritative HP/MP/stamina display. */
    var oldTop=document.querySelector('.v38-raid-page .v20-counter');if(oldTop)oldTop.remove();
  }
  setInterval(refresh,700);setTimeout(refresh,100);setTimeout(refresh,500);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')
