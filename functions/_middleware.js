// Acesso por token para todo o site (Cloudflare Pages Functions). Roda antes de qualquer arquivo de publicar/.
// A senha fica na variável secreta ACCESS_TOKEN do projeto no Cloudflare (Pages → projeto → Settings → Variables and Secrets).
// Quem acerta o token recebe um cookie assinado que vale 7 dias. Trocar a senha derruba todos os acessos.

const COOKIE = 'lds_acesso';
const DIAS = 7;
const PUBLICO = new Set(['/entrar', '/entrar/', '/entrar/index.html', '/favicon.ico', '/robots.txt']);
const enc = new TextEncoder();

async function assinar(segredo, texto) {
  const k = await crypto.subtle.importKey('raw', enc.encode(segredo), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, enc.encode(texto));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function igual(a, b) { // comparação em tempo constante
  if (a.length !== b.length) return false;
  let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

function lerCookie(req, nome) {
  const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|;\\s*)' + nome + '=([^;]+)'));
  return m ? m[1] : '';
}

async function valido(req, segredo) {
  const [exp, sig] = lerCookie(req, COOKIE).split('.');
  if (!exp || !sig || !/^\d+$/.test(exp) || +exp < Date.now()) return false;
  return igual(sig, await assinar(segredo, 'acesso:' + exp));
}

const json = (obj, status = 200, headers = {}) =>
  new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers } });


/* ---------- Ativar rascunho (aba Rascunhos do catálogo) ----------
   Faz um commit no GitHub mudando só arquivos de edicoes/. O GitHub Actions (.github/workflows/build.yml) roda o build
   e publica; o Cloudflare Pages atualiza sozinho. Precisa da variável secreta GITHUB_TOKEN no Cloudflare
   (token "fine-grained" do GitHub com permissão Contents: Read and write só no repositório getulio-apresentacoes). */
const REPO = 'VitorCarrvalho/getulio-apresentacoes', BR = 'main';
async function gh(env, path, opt = {}) {
  const r = await fetch('https://api.github.com/repos/' + REPO + path, { ...opt, headers: { authorization: 'Bearer ' + env.GITHUB_TOKEN, accept: 'application/vnd.github+json', 'user-agent': 'lds-apresentacoes', 'x-github-api-version': '2022-11-28', ...(opt.body ? { 'content-type': 'application/json' } : {}) } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) {
    const dica = r.status === 401 ? 'o token do GitHub está inválido ou expirou (gere outro e cole de novo no Cloudflare)'
      : (r.status === 403 || r.status === 404) ? 'o token do GitHub não tem acesso de escrita ao repositório getulio-apresentacoes (precisa de "Contents: Read and write" e o repositório marcado)'
      : 'o GitHub recusou o pedido';
    throw new Error(dica + ' [GitHub ' + r.status + ': ' + (j.message || 'erro') + ' · ' + (opt.method || 'GET') + ' ' + path.split('?')[0] + ']');
  }
  return j;
}
const b64d = s => new TextDecoder().decode(Uint8Array.from(atob(s.replace(/\n/g, '')), c => c.charCodeAt(0)));
async function lerJson(env, path) { const j = await gh(env, '/contents/' + path + '?ref=' + BR); return { dados: JSON.parse(b64d(j.content)) }; }
async function ativar(env, slug) {
  if (!/^[a-z0-9-]+$/.test(slug)) throw new Error('Rascunho inválido.');
  const { dados: cfg } = await lerJson(env, 'edicoes/' + slug + '/edicao.json');
  if (!cfg.rascunho) throw new Error('Essa apresentação já está ativa.');
  const ref = await gh(env, '/git/ref/heads/' + BR);
  const base = await gh(env, '/git/commits/' + ref.object.sha);
  const arquivos = [];
  const txt = o => JSON.stringify(o, null, 2) + '\n';
  const novo = { ...cfg }; delete novo.rascunho; delete novo.numerado;
  let msg = 'Ativa rascunho ' + slug;
  if (cfg.substitui) {
    const alvo = cfg.substitui;
    const { dados: atual } = await lerJson(env, 'edicoes/' + alvo + '/edicao.json');
    const sufixo = (atual.raiz || '2025');
    const arq = { ...atual, slug: alvo + '-' + sufixo, evento: (atual.evento || atual.titulo) + ' (versão ' + sufixo + ')', arquivada: true };
    arquivos.push({ path: 'edicoes/' + arq.slug + '/edicao.json', content: txt(arq) });
    novo.slug = alvo; delete novo.substitui;
    if (alvo === 'original') novo.evento = 'Palestra original';
    arquivos.push({ path: 'edicoes/' + alvo + '/edicao.json', content: txt(novo) });
    arquivos.push({ path: 'edicoes/' + slug + '/edicao.json', sha: null });
    msg = 'Ativa rascunho ' + slug + ': vira "' + alvo + '"; versão anterior arquivada como ' + arq.slug;
  } else {
    arquivos.push({ path: 'edicoes/' + slug + '/edicao.json', content: txt(novo) });
  }
  const tree = await gh(env, '/git/trees', { method: 'POST', body: JSON.stringify({ base_tree: base.tree.sha, tree: arquivos.map(a => a.sha === null ? { path: a.path, mode: '100644', type: 'blob', sha: null } : { path: a.path, mode: '100644', type: 'blob', content: a.content }) }) });
  const commit = await gh(env, '/git/commits', { method: 'POST', body: JSON.stringify({ message: msg + ' (botão Ativar do catálogo)', tree: tree.sha, parents: [ref.object.sha] }) });
  await gh(env, '/git/refs/heads/' + BR, { method: 'PATCH', body: JSON.stringify({ sha: commit.sha }) });
  return commit.sha;
}

export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);
  const p = url.pathname;
  const segredo = env.ACCESS_TOKEN;

  if (p === '/') return Response.redirect(new URL('/apresentacoes/', url), 302);
  if (PUBLICO.has(p)) return next();

  if (p === '/api/entrar') {
    if (request.method !== 'POST') return json({ erro: 'Método não permitido.' }, 405);
    if (!segredo) return json({ erro: 'Acesso ainda não configurado no Cloudflare (falta ACCESS_TOKEN).' }, 503);
    let token = '';
    try { token = String((await request.json()).token || ''); } catch (e) {}
    // compara as assinaturas, não os textos, para não vazar tempo
    const ok = token && igual(await assinar(segredo, 'cmp:' + token), await assinar(segredo, 'cmp:' + segredo));
    if (!ok) { await new Promise(r => setTimeout(r, 600)); return json({ erro: 'Token inválido.' }, 401); }
    const exp = Date.now() + DIAS * 864e5;
    const val = exp + '.' + (await assinar(segredo, 'acesso:' + exp));
    return json({ ok: true }, 200, { 'set-cookie': `${COOKIE}=${val}; Path=/; Max-Age=${DIAS * 86400}; HttpOnly; Secure; SameSite=Lax` });
  }

  if (p === '/api/sair') {
    return new Response(null, { status: 302, headers: { location: '/entrar/', 'set-cookie': `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`, 'cache-control': 'no-store' } });
  }

  if (!segredo || !(await valido(request, segredo))) {
    const volta = encodeURIComponent(p + url.search);
    return new Response(null, { status: 302, headers: { location: '/entrar/?volta=' + volta, 'cache-control': 'no-store' } });
  }

  if (p === '/api/ativar') {
    if (request.method !== 'POST') return json({ erro: 'Método não permitido.' }, 405);
    if (!env.GITHUB_TOKEN) return json({ erro: 'O botão Ativar ainda não foi ligado: falta a chave GITHUB_TOKEN no Cloudflare. Enquanto isso, peça ao Claude: "ativa o rascunho".' }, 424);
    let slug = ''; try { slug = String((await request.json()).slug || ''); } catch (e) {}
    try { const sha = await ativar(env, slug); return json({ ok: true, commit: sha }); }
    catch (e) { return json({ erro: 'Não consegui ativar: ' + e.message }, 422); }
  }

  const res = await next();
  const r = new Response(res.body, res);
  r.headers.set('cache-control', 'private, max-age=300, must-revalidate');
  return r;
}
