from pathlib import Path
import sys

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('project/app/src/main/assets/index.html')
s = p.read_text(encoding='utf-8')
if 'NORD_V46_AUDIO' in s:
    raise SystemExit(0)

patch = r'''<script id="NORD_V46_AUDIO">
(function(){
  'use strict';
  if(window.NORD_AUDIO_V46) return;
  window.NORD_AUDIO_V46 = true;

  var AC = window.AudioContext || window.webkitAudioContext;
  var ctx = null;
  var master = null;
  var lastAt = 0;
  var rnd = function(a,b){ return a + Math.random()*(b-a); };

  function ensure(){
    if(!AC) return null;
    try{
      if(!ctx){
        ctx = new AC();
        master = ctx.createGain();
        master.gain.value = 0.16;
        master.connect(ctx.destination);
      }
      if(ctx.state === 'suspended') ctx.resume();
      return ctx;
    }catch(e){ return null; }
  }

  function tone(freq, dur, type, gain, when, endFreq){
    var c=ensure(); if(!c) return;
    when=when||c.currentTime;
    var o=c.createOscillator(), g=c.createGain();
    o.type=type||'sine';
    o.frequency.setValueAtTime(Math.max(30,freq),when);
    if(endFreq) o.frequency.exponentialRampToValueAtTime(Math.max(30,endFreq),when+dur);
    g.gain.setValueAtTime(0.0001,when);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0001,gain),when+0.008);
    g.gain.exponentialRampToValueAtTime(0.0001,when+dur);
    o.connect(g); g.connect(master); o.start(when); o.stop(when+dur+0.02);
  }

  function noise(dur, gain, hp, when){
    var c=ensure(); if(!c) return;
    when=when||c.currentTime;
    var n=Math.max(1,Math.floor(c.sampleRate*dur));
    var b=c.createBuffer(1,n,c.sampleRate), data=b.getChannelData(0);
    for(var i=0;i<n;i++) data[i]=(Math.random()*2-1)*(1-i/n);
    var src=c.createBufferSource(), f=c.createBiquadFilter(), g=c.createGain();
    f.type='highpass'; f.frequency.value=hp||900;
    g.gain.setValueAtTime(0.0001,when);
    g.gain.exponentialRampToValueAtTime(gain,when+0.006);
    g.gain.exponentialRampToValueAtTime(0.0001,when+dur);
    src.buffer=b; src.connect(f); f.connect(g); g.connect(master); src.start(when); src.stop(when+dur+0.02);
  }

  function play(kind){
    var c=ensure(); if(!c) return;
    var now=c.currentTime;
    if(now-lastAt<0.045) return;
    lastAt=now;
    var v=Math.random()<0.5?0:1;
    if(kind==='attack'){
      if(v===0){ noise(.13,.34,1200,now); tone(180,.16,'sawtooth',.18,now,70); tone(720,.08,'triangle',.10,now+.018,240); }
      else { noise(.09,.38,1800,now); tone(260,.18,'square',.14,now,82); tone(980,.055,'triangle',.09,now+.01,310); }
    } else if(kind==='heavy'){
      if(v===0){ noise(.22,.42,500,now); tone(110,.28,'sine',.22,now,48); tone(360,.10,'sawtooth',.11,now,120); }
      else { tone(150,.30,'triangle',.25,now,45); noise(.16,.30,700,now+.025); tone(520,.08,'square',.08,now+.02,180); }
    } else if(kind==='defend'){
      if(v===0){ tone(680,.12,'triangle',.16,now,360); tone(1080,.08,'sine',.10,now+.018,520); noise(.055,.16,2300,now); }
      else { noise(.08,.20,2500,now); tone(510,.17,'square',.11,now,820); }
    } else if(kind==='potion'){
      if(v===0){ tone(420,.18,'sine',.12,now,760); tone(620,.24,'triangle',.08,now+.04,980); }
      else { tone(330,.14,'sine',.10,now,540); tone(540,.24,'sine',.10,now+.06,900); tone(900,.18,'triangle',.06,now+.12,1200); }
    } else if(kind==='open'){
      if(v===0){ tone(190,.08,'square',.12,now,280); tone(420,.16,'triangle',.10,now+.07,700); }
      else { tone(240,.07,'square',.12,now,360); tone(520,.20,'sine',.10,now+.06,880); }
    } else if(kind==='trap'){
      if(v===0){ tone(170,.12,'square',.13,now,80); noise(.09,.18,1700,now+.04); }
      else { noise(.06,.20,2200,now); tone(280,.15,'sawtooth',.12,now+.025,95); }
    } else if(kind==='inventory'){
      if(v===0){ tone(310,.07,'sine',.09,now,390); tone(460,.09,'triangle',.07,now+.045,520); }
      else { tone(260,.06,'sine',.09,now,330); tone(520,.10,'triangle',.07,now+.05,610); }
    } else if(kind==='map'){
      if(v===0){ noise(.07,.10,900,now); tone(360,.10,'triangle',.07,now+.025,470); }
      else { tone(300,.08,'sine',.08,now,420); noise(.055,.08,1200,now+.035); }
    } else if(kind==='journal'){
      if(v===0){ noise(.11,.09,1300,now); tone(440,.07,'sine',.05,now+.02,520); }
      else { noise(.08,.10,1600,now); tone(520,.06,'triangle',.05,now+.025,610); }
    } else if(kind==='ui'){
      if(v===0){ tone(520,.055,'sine',.10,now,680); }
      else { tone(420,.05,'triangle',.10,now,590); tone(780,.035,'sine',.035,now+.015,860); }
    } else if(kind==='next'){
      if(v===0){ tone(420,.10,'triangle',.10,now,620); tone(700,.16,'sine',.09,now+.07,980); }
      else { tone(500,.08,'sine',.10,now,760); tone(820,.18,'triangle',.08,now+.06,1100); }
    } else if(kind==='win'){
      var base=v?520:440; tone(base,.16,'triangle',.13,now,base*1.12); tone(base*1.25,.18,'sine',.11,now+.10,base*1.45); tone(base*1.5,.28,'triangle',.09,now+.21,base*1.9);
    } else if(kind==='lose'){
      var b=v?220:260; tone(b,.20,'sawtooth',.12,now,b*.78); tone(b*.72,.30,'triangle',.10,now+.14,b*.48);
    }
  }

  window.NORD_SFX_V46 = play;

  function classify(el){
    if(!el) return 'ui';
    var x=(el.getAttribute('data-sound')||'').toLowerCase();
    if(x) return x;
    var t=((el.innerText||el.textContent||'')+' '+(el.getAttribute('aria-label')||'')+' '+(el.id||'')+' '+(el.className||'')).toLowerCase();
    if(/атак|attack|удар/.test(t)) return /силь|heavy|мощ/.test(t)?'heavy':'attack';
    if(/защит|block|щит/.test(t)) return 'defend';
    if(/зель|potion|леч/.test(t)) return 'potion';
    if(/сундук|открыть|open|loot/.test(t)) return 'open';
    if(/ловуш|trap/.test(t)) return 'trap';
    if(/инвентар|inventory|сумк/.test(t)) return 'inventory';
    if(/карта|map/.test(t)) return 'map';
    if(/журнал|log|journal/.test(t)) return 'journal';
    if(/побед|win|victory/.test(t)) return 'win';
    if(/поражен|проиг|lose|defeat/.test(t)) return 'lose';
    if(/следующ|далее|next|продолж/.test(t)) return 'next';
    return 'ui';
  }

  document.addEventListener('pointerdown',function(e){
    var el=e.target && e.target.closest ? e.target.closest('button,[role="button"],a,.btn,.button,.action,.choice,[onclick]') : e.target;
    if(!el) return;
    play(classify(el));
  },true);
  document.addEventListener('touchstart',function(){ ensure(); },{passive:true,once:true});
  document.addEventListener('click',function(e){
    var el=e.target && e.target.closest ? e.target.closest('[data-sound]') : null;
    if(el && el.getAttribute('data-sound')) play(el.getAttribute('data-sound'));
  },true);
})();
</script>'''

s = s.replace('</head>', patch + '</head>', 1)
p.write_text(s, encoding='utf-8')
