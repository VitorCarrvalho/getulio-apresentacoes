// node shots.js file.html outdir WxH [WxH...]  -> estados finais via ?mirror (sem animação) + folhas
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [f,out,...sizes]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();const errs=[];
for(const sz of sizes){const [W,H]=sz.split('x').map(Number);const p=await b.newPage({viewport:{width:W,height:H}});
p.on('pageerror',e=>errs.push(sz+' '+e));p.on('console',m=>{if(m.type()==='error')errs.push(sz+' '+m.text())});
await p.goto('file://'+f+'?mirror');await p.waitForTimeout(600);
const steps=await p.evaluate(()=>[...document.querySelectorAll('#deck .slide')].map(s=>+s.dataset.steps||0));
for(let i=0;i<steps.length;i++)for(let s=0;s<=steps[i];s++){
 await p.evaluate(([i,s])=>go(i,s,0),[i,s]);await p.waitForTimeout(120);
 await p.screenshot({path:`${out}/${sz}_${String(i+1).padStart(2,'0')}.${s}.png`});}
await p.close();}
await b.close();console.log('errors:',errs.length?errs:'none');})();
