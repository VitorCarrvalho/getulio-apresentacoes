// Confere o texto de cada edição contra o PowerPoint original.
//   node ferramentas/textcheck.js            todas as edições
//   node ferramentas/textcheck.js premium    só uma
// Regra: todo texto do PPT das telas incluídas tem que estar no HTML (bad 0) e nenhum texto pode sobrar (nenhuma linha EXTRA).
// Telas tiradas de propósito na edição aparecem como "fora", não como erro. Na edição com "telas": "todas", faltar tela é erro.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const R = path.join(__dirname, '..');
const ppt = JSON.parse(fs.readFileSync(path.join(R, 'original', 'ppt_text.json')));
const special = { 1: 's-capa', 3: 's-livro', 55: 's-fim' };
const all = Object.values(ppt).flat().map(t => t.replace(/\s+/g, ' ').trim()).filter(Boolean).sort((a, b) => b.length - a.length);
const alvo = process.argv.slice(2);
const slugs = (alvo.length ? alvo : fs.readdirSync(path.join(R, 'edicoes'))).filter(s => fs.existsSync(path.join(R, 'edicoes', s, 'edicao.json')));

(async () => {
  const b = await chromium.launch(); let total = 0;
  for (const slug of slugs) {
    const cfg = JSON.parse(fs.readFileSync(path.join(R, 'edicoes', slug, 'edicao.json')));
    const todas = (cfg.telas || 'todas') === 'todas';
    const p = await b.newPage();
    await p.goto('file://' + path.join(R, 'publicar', 'apresentacoes', slug, 'index.html') + '?mirror'); await p.waitForTimeout(500);
    const secs = await p.evaluate(() => [...document.querySelectorAll('#deck .slide')].map(s => ({ id: s.id, num: s.dataset.num, nums: s.dataset.nums || '', txt: s.textContent.replace(/\s+/g, ' ') })));
    let bad = 0, ok = 0, fora = 0; const log = [];
    for (const [n, boxes] of Object.entries(ppt)) {
      const sec = secs.find(s => special[n] ? s.id === special[n] : (s.num === n || s.nums.split(',').includes(n)));
      if (!sec) { if (todas) { bad++; log.push('NO SECTION ' + n); } else fora++; continue; }
      for (const t of boxes) { const tt = t.replace(/\s+/g, ' ').trim(); if (!tt) continue; if (sec.txt.includes(tt)) ok++; else { bad++; log.push('MISSING S' + n + ': ' + tt); } }
    }
    for (const s of secs) { let t = s.txt; for (const x of all) t = t.split(x).join(' '); t = t.replace(/\s+/g, ' ').trim(); if (t) { bad++; log.push('EXTRA ' + s.id + ' ' + JSON.stringify(t)); } }
    console.log(`${slug}: ok ${ok} bad ${bad}` + (fora ? ` (fora desta edição: ${fora} slides do PPT)` : ''));
    log.forEach(l => console.log('  ' + l)); total += bad; await p.close();
  }
  await b.close(); process.exit(total ? 1 : 0);
})();
