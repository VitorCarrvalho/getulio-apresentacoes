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

  const res = await next();
  const r = new Response(res.body, res);
  r.headers.set('cache-control', 'private, max-age=300, must-revalidate');
  return r;
}
