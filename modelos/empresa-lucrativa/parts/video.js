/* ---------- Vídeos locais ----------
   Cada slide de vídeo espera um arquivo na pasta videos/ (data-video-file). Só a janela do painel toca
   (os espelhos do apresentador não carregam o vídeo, para não duplicar o som). Toca sozinho ao entrar no slide e para ao sair.
   Se o arquivo não existir, o slide mostra um botão para escolher o vídeo ou arrastar o arquivo para a tela. */
const Video = (() => {
  let vid = null, slide = null, timer = null;
  const chosen = {}; /* id do slide -> URL do arquivo escolhido nesta sessão */
  function stop() { clearTimeout(timer); if (vid) { try { vid.pause(); } catch (e) {} vid.remove(); vid = null; } if (slide) slide.classList.remove('playing', 'ended'); slide = null; document.body.classList.remove('vidon'); }
  function play(s, src) {
    const box = s.querySelector('.lv'); vid = document.createElement('video');
    vid.src = src; vid.autoplay = true; vid.playsInline = true; vid.preload = 'auto'; vid.setAttribute('tabindex', '-1');
    vid.addEventListener('playing', () => { s.classList.remove('missing', 'ended'); s.classList.add('playing'); document.body.classList.add('vidon'); });
    vid.addEventListener('ended', () => { s.classList.add('ended'); document.body.classList.remove('vidon'); });
    vid.addEventListener('error', () => { s.classList.add('missing'); s.classList.remove('playing'); document.body.classList.remove('vidon'); if (vid) { vid.remove(); vid = null; } });
    box.appendChild(vid); const p = vid.play(); if (p && p.catch) p.catch(() => {});
  }
  function enter(s) {
    stop(); const f = s.dataset.videoFile; if (!f || window.__ROLE !== 'audience') return;
    slide = s; timer = setTimeout(() => play(s, chosen[s.id] || f), 700);
  }
  function toggle() {
    if (!slide) return; if (!vid) { enter(slide); return; }
    slide.classList.remove('ended'); if (vid.paused) { vid.play(); document.body.classList.add('vidon'); } else { vid.pause(); }
  }
  function use(s, file) { if (!file) return; chosen[s.id] = URL.createObjectURL(file); s.classList.remove('missing'); if (slide === s) { stop(); slide = s; play(s, chosen[s.id]); } }
  document.querySelectorAll('[data-video-file]').forEach(s => {
    const inp = s.querySelector('.pick input'); if (inp) inp.addEventListener('change', () => use(s, inp.files[0]));
    s.addEventListener('dragover', e => { e.preventDefault(); s.classList.add('drop'); });
    s.addEventListener('dragleave', () => s.classList.remove('drop'));
    s.addEventListener('drop', e => { e.preventDefault(); s.classList.remove('drop'); use(s, e.dataTransfer.files[0]); });
  });
  return { enter, stop, toggle };
})();
