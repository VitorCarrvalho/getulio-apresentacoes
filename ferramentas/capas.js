// Gera a miniatura do card do catálogo (capa de cada edição, 16:9) em edicoes/<slug>/capa.webp.
//   node ferramentas/capas.js            todas
//   node ferramentas/capas.js premium    só uma
// Rode depois do build.py e rode o build.py de novo para copiar as capas para publicar/.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const R = path.join(__dirname, '..');
const alvo = process.argv.slice(2);
const slugs = (alvo.length ? alvo : fs.readdirSync(path.join(R, 'edicoes'))).filter(s => fs.existsSync(path.join(R, 'publicar', 'apresentacoes', s, 'index.html')));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  for (const slug of slugs) {
    await p.goto('file://' + path.join(R, 'publicar', 'apresentacoes', slug, 'index.html') + '?mirror'); await p.waitForTimeout(700);
    const png = path.join(require('os').tmpdir(), `capa-${slug}.png`);
    await p.screenshot({ path: png });
    const out = path.join(R, 'edicoes', slug, 'capa.webp');
    execFileSync('python3', ['-c', 'import sys;from PIL import Image;Image.open(sys.argv[1]).convert("RGB").resize((960,540),Image.LANCZOS).save(sys.argv[2],"WEBP",quality=82)', png, out]);
    console.log(out);
  }
  await b.close();
})();
