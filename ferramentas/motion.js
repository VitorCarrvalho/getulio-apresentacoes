const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});const errs=[];p.on('pageerror',e=>errs.push(''+e));
await p.goto('file:///home/claude/build/dist/index.html?nogate');await p.waitForTimeout(800);
const total=await p.evaluate(()=>[...document.querySelectorAll('#deck .slide')].reduce((a,s)=>a+1+(+s.dataset.steps||0),0));
const res=[];let maxEnd=0;
for(let k=0;k<total;k++){ if(k) await p.keyboard.press('ArrowRight');
  if([15,20,58].includes(k)){} 
  const t0=Date.now();let running;
  for(;;){await p.waitForTimeout(250);running=await p.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').map(a=>(a.effect&&a.effect.getTiming().iterations)));
    if(!running.length||Date.now()-t0>6000)break;}
  const el=(Date.now()-t0)/1000;maxEnd=Math.max(maxEnd,el);
  const inf=running.filter(x=>x===Infinity).length;
  res.push(`${await p.evaluate('location.hash')}:${el.toFixed(1)}s${running.length?' RUNNING '+running.length+' inf '+inf:''}`);}
console.log(res.join('  '));console.log('max settle',maxEnd,'errors',errs);
// frames durante transições
await p.evaluate(()=>go(14,0));await p.waitForTimeout(2500);await p.keyboard.press('ArrowRight');await p.waitForTimeout(450);await p.screenshot({path:'/home/claude/build/mid_gold.png'});
await p.evaluate(()=>go(28,0));await p.waitForTimeout(3000);await p.keyboard.press('ArrowRight');await p.waitForTimeout(600);await p.screenshot({path:'/home/claude/build/mid_pil.png'});
await p.evaluate(()=>go(11,0));await p.waitForTimeout(1300);await p.screenshot({path:'/home/claude/build/mid_lab.png'});
await b.close()})();
