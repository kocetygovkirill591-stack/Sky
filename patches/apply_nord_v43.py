from pathlib import Path
import sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('project/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
if 'NORD_V43_RESOURCE_FIX' in s:
    raise SystemExit(0)
patch=r'''<style id="NORD_V43_RESOURCE_FIX">
/* Keep only one compact top resource strip; remove duplicate legacy children. */
.v38-raid-page .v20-counter{display:block!important;width:auto!important;height:auto!important;min-height:0!important;padding:7px 8px!important;margin:6px 0 8px!important;background:transparent!important;border:0!important;box-shadow:none!important}
.v38-raid-page .v20-counter>.nord40-res{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important;width:100%!important}
.v38-raid-page .v20-counter>.nord40-res~*{display:none!important}
.v38-raid-page .v20-counter>.nord40-res + div,.v38-raid-page .v20-counter>.nord40-res + span,.v38-raid-page .v20-counter>span:not(.nord40-res),.v38-raid-page .v20-counter>b,.v38-raid-page .v20-counter>small{display:none!important}
/* Hero card: stats only. Resources are shown once in the top strip. */
.v38-player-card .nord40-player-res{display:none!important}
.v38-player-card .v20-hpbar.hero{display:none!important}
.v38-player-card strong{font-size:11px!important}
.nord43-res .r{min-height:39px!important;padding:5px 6px!important;border-radius:10px!important}
.nord43-res .r b{font-size:9px!important}
.nord43-res .r i{height:4px!important}
</style>
<script id="NORD_V43_RESOURCE_FIX">
(function(){
  function pct(v,m){v=Math.max(0,+v||0);m=Math.max(1,+m||1);return Math.max(0,Math.min(100,v/m*100))}
  function getRaid(){try{var p=typeof hero==='function'?hero():{};return p&&p._v20Raid?p._v20Raid:null}catch(e){return null}}
  function readPlayerHP(){
    var el=document.querySelector('.v38-player-card strong');
    if(!el)return null;
    var m=(el.textContent||'').match(/([0-9]+)\s*\/\s*([0-9]+)/);
    return m?[+m[1],+m[2]]:null;
  }
  function refresh(){
    var page=document.querySelector('.v38-raid-page');if(!page)return;
    var p={};try{p=typeof hero==='function'?hero()||{}:{}}catch(e){}
    var a=getRaid()||{};
    var hpPair=readPlayerHP();
    var hp=hpPair?hpPair[0]:((a.hp!=null)?+a.hp:+(p.hp||0));
    var mh=hpPair?hpPair[1]:((a.maxHp!=null)?+a.maxHp:+(p.maxHp||108));
    var mp=+(p.mp||0),mm=+(p.maxMp||50),st=+(a.st!=null?a.st:(p.st||0)),sm=+(p.maxSt||118);
    var el=page.querySelector('.v20-counter');if(!el)return;
    var top=el.querySelector('.nord40-res');if(!top){top=document.createElement('div');top.className='nord40-res nord43-res';el.appendChild(top)}
    var html='<div class="r nord40-h"><b>❤️ '+hp+'/'+mh+'</b><i><em style="width:'+pct(hp,mh)+'%"></em></i></div>'+
             '<div class="r nord40-m"><b>🔷 '+mp+'/'+mm+'</b><i><em style="width:'+pct(mp,mm)+'%"></em></i></div>'+
             '<div class="r nord40-s"><b>🟢 '+st+'/'+sm+'</b><i><em style="width:'+pct(st,sm)+'%"></em></i></div>';
    if(top.innerHTML!==html)top.innerHTML=html;
    var dup=el.querySelectorAll(':scope > *');
    for(var i=0;i<dup.length;i++){if(dup[i]!==top)dup[i].style.display='none'}
  }
  setInterval(refresh,1000);setTimeout(refresh,100);setTimeout(refresh,500);
})();
</script>'''
s=s.replace('</head>',patch+'</head>',1)
p.write_text(s,encoding='utf-8')