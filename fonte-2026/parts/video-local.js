/* ---------- Vídeo de arquivo (slides com data-video-file) ----------
   Para vídeos que não estão no YouTube. Na primeira vez, o Getúlio escolhe o arquivo no computador do painel
   (botão no slide ou arrastando o arquivo para a tela). O navegador guarda o vídeo (IndexedDB) e nas próximas vezes
   ele toca sozinho, com som, ao entrar no slide. Também aceita o arquivo na pasta videos/ ao lado do index.html.
   Só a janela do painel toca: os espelhos do apresentador não carregam o vídeo. */
const LocalVideo = (() => {
  let vid = null, slide = null, timer = null;
  const urls = {};
  const DB = 'getulio-videos', ST = 'v';
  function db() { return new Promise((ok, no) => { try { const r = indexedDB.open(DB, 1); r.onupgradeneeded = () => r.result.createObjectStore(ST); r.onsuccess = () => ok(r.result); r.onerror = () => no(r.error); } catch (e) { no(e); } }); }
  async function save(key, file) { try { const d = await db(); d.transaction(ST, 'readwrite').objectStore(ST).put(file, key); } catch (e) {} }
  async function load(key) { try { const d = await db(); return await new Promise(ok => { const r = d.transaction(ST).objectStore(ST).get(key); r.onsuccess = () => ok(r.result || null); r.onerror = () => ok(null); }); } catch (e) { return null; } }
  function stop() { clearTimeout(timer); if (vid) { try { vid.pause(); } catch (e) {} vid.remove(); vid = null; } if (slide) slide.classList.remove('playing', 'ended'); slide = null; document.body.classList.remove('vidon'); }
  function play(s, src, fallback) {
    if (slide !== s) return;
    vid = document.createElement('video');
    vid.src = src; vid.autoplay = true; vid.playsInline = true; vid.preload = 'auto'; vid.setAttribute('tabindex', '-1');
    vid.addEventListener('playing', () => { s.classList.remove('missing', 'ended'); s.classList.add('playing'); document.body.classList.add('vidon'); });
    vid.addEventListener('ended', () => { s.classList.add('ended'); document.body.classList.remove('vidon'); });
    vid.addEventListener('error', () => { if (vid) { vid.remove(); vid = null; } if (fallback) { play(s, fallback, null); return; } s.classList.add('missing'); s.classList.remove('playing'); document.body.classList.remove('vidon'); });
    $('.yt', s).appendChild(vid); const p = vid.play(); if (p && p.catch) p.catch(() => {});
  }
  function enter(s) {
    stop(); const f = s.dataset.videoFile; if (!f || window.__ROLE !== 'audience') return;
    slide = s;
    timer = setTimeout(async () => {
      if (!urls[s.id]) { const b = await load(s.id); if (b) urls[s.id] = URL.createObjectURL(b); }
      if (urls[s.id]) play(s, urls[s.id], f); else play(s, f, null);
    }, 700);
  }
  function toggle() {
    if (!slide) return; if (!vid) { enter(slide); return; }
    slide.classList.remove('ended'); if (vid.paused) { vid.play(); document.body.classList.add('vidon'); } else vid.pause();
  }
  function use(s, file) {
    if (!file) return; urls[s.id] = URL.createObjectURL(file); save(s.id, file); s.classList.remove('missing');
    if (slide === s) { stop(); slide = s; play(s, urls[s.id], null); }
  }
  $$('[data-video-file]').forEach(s => {
    const inp = s.querySelector('.pick input'); if (inp) inp.addEventListener('change', () => use(s, inp.files[0]));
    s.addEventListener('dragover', e => { e.preventDefault(); s.classList.add('drop'); });
    s.addEventListener('dragleave', () => s.classList.remove('drop'));
    s.addEventListener('drop', e => { e.preventDefault(); s.classList.remove('drop'); use(s, e.dataTransfer.files[0]); });
  });
  return { enter, stop, toggle };
})();
const Video = {
  enter(s) { YTVideo.enter(s); LocalVideo.enter(s); },
  stop() { YTVideo.stop(); LocalVideo.stop(); },
  toggle() { (slides[cur] && slides[cur].dataset.videoFile ? LocalVideo : YTVideo).toggle(); }
};
