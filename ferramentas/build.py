#!/usr/bin/env python3
"""Monta o site inteiro em publicar/.

  publicar/apresentacoes/index.html          catálogo (protegido pelo token)
  publicar/apresentacoes/<slug>/index.html   cada edição: um HTML único, offline
  publicar/apresentacoes/<slug>/capa.webp    miniatura do card (gerada por ferramentas/capas.js)
  publicar/entrar/index.html                 tela do token (pública)

Cada edição vive em edicoes/<slug>/edicao.json (+ logo opcional). A base é fonte/.
Uso: python3 ferramentas/build.py            (tudo)
     python3 ferramentas/build.py premium    (só uma edição + catálogo)
"""
import json, re, sys, os, base64, shutil, html as H

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
F = os.path.join(R, 'fonte')
PUB = os.path.join(R, 'publicar')
ED = os.path.join(R, 'edicoes')
CAT = os.path.join(R, 'catalogo')

U = re.compile(r'(?<![\w#.\-])(-?\d+(?:\.\d+)?)u\b')
def conv_units(html):
    return re.sub(r'(<style>)(.*?)(</style>)',
                  lambda m: m.group(1) + U.sub(lambda x: f'calc(var(--u)*{x.group(1)})', m.group(2)) + m.group(3),
                  html, flags=re.S)

def read(p): return open(p, encoding='utf-8').read()

FONTS = read(os.path.join(F, 'assets/fonts.css'))
ICONS = json.load(open(os.path.join(F, 'assets/icons.json')))
SEC = re.compile(r'(?:<!--[^\n]*-->\n)?<section\b[^>]*\bid="([^"]+)"[\s\S]*?</section>\n*')

def dup_ids(css, pares):
    """Copia as regras de um id para outro (ex.: #s-capa -> #s-capa2), para telas repetidas."""
    def fix(m):
        sel = m.group(1)
        if sel.lstrip().startswith('@'): return m.group(0)
        partes = sel.split(',')
        extra = [re.sub('#' + re.escape(a) + r'(?![\w-])', '#' + b, x) for x in partes for a, bs in pares.items() for b in ([bs] if isinstance(bs, str) else bs) if re.search('#' + re.escape(a) + r'(?![\w-])', x)]
        return (','.join(partes + extra) if extra else sel) + '{'
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return re.sub(r'([^{}]+)\{', fix, css)

def carrega_raiz(nome):
    """Raiz = conteúdo-base de onde as edições escolhem telas.
       2025: fonte/ (a palestra antiga, 55 slides).  2026: fonte-2026/ (conteúdo do PPTX novo sobre o mesmo design)."""
    head = read(os.path.join(F, 'parts/head.html'))
    script = read(os.path.join(F, 'parts/script.html'))
    imgs = json.load(open(os.path.join(F, 'assets/imgs.json')))
    if nome == '2025':
        body = read(os.path.join(F, 'parts/body.html'))
        cfg = {'fixas': ['s-capa', 's-fim'], 'texto': 'original/ppt_text.json', 'especiais': {'1': 's-capa', '3': 's-livro', '55': 's-fim'}}
    else:
        d = os.path.join(R, 'fonte-' + nome)
        cfg = json.load(open(os.path.join(d, 'raiz.json'), encoding='utf-8'))
        body = read(os.path.join(d, 'parts/body.html'))
        head = head.replace('</head>', read(os.path.join(d, 'parts/extra.css')) + '</head>')
        head = re.sub(r'(<style>)(.*?)(</style>)', lambda m: m.group(1) + dup_ids(m.group(2), cfg.get('repetidas', {})) + m.group(3), head, flags=re.S)
        for fn in sorted(os.listdir(os.path.join(d, 'assets'))):
            k, ext = os.path.splitext(fn)
            if ext in MIME: imgs[k] = data_uri(os.path.join(d, 'assets', fn))
        # notas do apresentador: uma por slide do PPTX, agrupadas por tela
        notas = json.load(open(os.path.join(d, 'notas.json'), encoding='utf-8'))
        nb = {}
        for m in SEC.finditer(body):
            tag = re.match(r'[^>]*>', m.group(0)[m.group(0).index('<section'):]).group(0)
            nums = re.search(r'data-nums="([^"]+)"', tag) or re.search(r'data-num="([^"]+)"', tag)
            nb[m.group(1)] = [notas.get(n, '') for n in nums.group(1).split(',')] if nums else ['']
        js = 'const NOTES_BY_ID = ' + json.dumps(nb, ensure_ascii=False, indent=1) + ';\n'
        script = re.sub(r'const NOTES_BY_ID = \{.*?\n\};\n', lambda m: js, script, count=1, flags=re.S)
        # vídeos: YouTube (produção) + vídeo de arquivo (slides com data-video-file)
        script = script.replace('const Video = (() => {', 'const YTVideo = (() => {', 1)
        i = script.index('const YTVideo = (() => {'); j = script.index('\n})();\n', i) + len('\n})();\n')
        script = script[:j] + read(os.path.join(d, 'parts/video-local.js')) + script[j:]
        script = script.replace('if (slides[cur].dataset.video) {', 'if (slides[cur].dataset.video || slides[cur].dataset.videoFile) {')
        script = script.replace("slides[S.i] && slides[S.i].dataset.video ?", "slides[S.i] && (slides[S.i].dataset.video || slides[S.i].dataset.videoFile) ?")
        # data-in="2,3": elemento visível só nesses passos
        script = script.replace("  $$('[data-active]', s).forEach(", "  $$('[data-in]', s).forEach(e => e.classList.toggle('vis', e.dataset.in.split(',').includes(String(st))));\n  $$('[data-active]', s).forEach(", 1)
        script = script.replace("  foot.classList.toggle('dk', s.dataset.foot === 'dk');", "  foot.classList.toggle('dk', s.dataset.foot === 'dk' || (s.dataset.goldStep !== undefined && +s.dataset.goldStep === st));", 1)
        assert 'goldStep' in script
        script = script.replace('`Tela ${S.i + 1} de 46 · slide ${S.pn} do roteiro`', '`Tela ${S.i + 1} de ${S.steps.length} · slide ${S.pn}`')
        for a in ['const YTVideo', 'const LocalVideo', "[data-in]", 'const NOTES_BY_ID = {\n "s-capa"']:
            assert a in script, f'raiz {nome}: falhou o ajuste do script ({a})'
    secs = list(SEC.finditer(body))
    cfg.update(nome=nome, head=head, script=script, imgs=imgs,
               pre=body[:secs[0].start()], post=body[secs[-1].end():],
               sections={m.group(1): m.group(0) for m in secs}, ordem=[m.group(1) for m in secs])
    return cfg

RAIZES = {}
def raiz(nome):
    if nome not in RAIZES: RAIZES[nome] = carrega_raiz(nome)
    return RAIZES[nome]
MIME = {'.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
IMGS = json.load(open(os.path.join(F, 'assets/imgs.json')))
CATEGORIAS = {'original', 'empresa', 'igreja', 'evento'}
def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    return f'data:{MIME[ext]};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def logo_path(slug, cfg):
    return os.path.join(ED, slug, cfg['logo']) if cfg.get('logo') else None

def load(slug):
    cfg = json.load(open(os.path.join(ED, slug, 'edicao.json'), encoding='utf-8'))
    assert cfg['slug'] == slug, f'{slug}: slug diferente da pasta'
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug), f'{slug}: use só minúsculas, números e hífen'
    assert cfg.get('categoria') in CATEGORIAS, f'{slug}: categoria deve ser uma de {sorted(CATEGORIAS)}'
    rz = raiz(cfg.get('raiz', '2025'))
    telas = rz['ordem'] if cfg.get('telas', 'todas') == 'todas' else cfg['telas']
    desconhecidas = [t for t in telas if t not in rz['sections']]
    assert not desconhecidas, f'{slug}: telas inexistentes {desconhecidas}'
    assert len(set(telas)) == len(telas), f'{slug}: tela repetida'
    for t in rz['fixas']: assert t in telas, f'{slug}: {t} é obrigatória'
    if cfg.get('logo'): assert os.path.exists(logo_path(slug, cfg)), f'{slug}: logo não encontrado'
    cfg['_telas'] = telas
    return cfg

def build_deck(cfg):
    slug = cfg['slug']
    rz = raiz(cfg.get('raiz', '2025'))
    body = rz['pre'] + ''.join(rz['sections'][t] for t in cfg['_telas']) + rz['post']
    head, script = rz['head'], rz['script']
    if cfg.get('numerado'):
        # rascunho de trabalho: cada tela mostra o número do slide do roteiro (some na versão aprovada)
        body = body.replace('<body>', '<body class="numerado">\n<div id="pnum" aria-hidden="true"></div>', 1)
        head = head.replace('</head>', '<style>#pnum{position:fixed;left:50%;transform:translateX(-50%);top:18px;z-index:60;min-width:54px;text-align:center;font:700 26px/1 Montserrat,sans-serif;color:#D4AF37;background:#141416;border:1px solid #D4AF37;padding:9px 14px;border-radius:12px;font-variant-numeric:tabular-nums;pointer-events:none}html[data-role="presenter"] #pnum{display:none}body.vidon #pnum{opacity:.35}</style></head>')
        script = script.replace("  footNum.textContent = nums ?", "  const pnEl = document.getElementById('pnum'); if (pnEl) pnEl.textContent = String(nums ? nums[Math.min(st, nums.length - 1)] : (s.dataset.num || '')).padStart(2, '0');\n  footNum.textContent = nums ?", 1)
        assert 'pnEl' in script
    lp = logo_path(slug, cfg)
    logo = ''
    if lp:
        alt = H.escape(cfg.get('logo_alt') or cfg.get('cliente') or '')
        h = cfg.get('logo_altura')  # em unidades de desenho; padrão 110
        style = f' style="--lh:calc(var(--u)*{float(h):g})"' if h else ''
        logo = f'\n    <div class="clogo in" style="--d:1.7"><i></i><img src="{data_uri(lp)}" alt="{alt}"{style}></div>'
    body = body.replace('{{CLIENT_LOGO}}', logo)
    if cfg.get('qr', True) is False:
        body = body.replace('\n      <div class="qr in" style="--d:2.8">{{QR}}</div>', '')
    script = script.replace('{{SYNC_SUFFIX}}', '' if slug == 'original' else '-' + slug)
    html = conv_units(head + body + script)
    html = html.replace('{{FONTS}}', FONTS)
    html = re.sub(r'\{\{IMG:(\w+)\}\}', lambda m: rz['imgs'][m.group(1)], html)
    html = re.sub(r'\{\{IC:(\w+)\}\}', lambda m: ICONS[m.group(1)], html)
    html = re.sub(r'\{\{LOGO:(\d+)\}\}', lambda m: read(os.path.join(F, f'assets/image-13-{m.group(1)}.svg')).replace('<svg ', '<svg role="img" preserveAspectRatio="xMidYMid meet" '), html)
    html = html.replace('{{QR}}', read(os.path.join(F, 'assets/qr.svg')))
    left = re.findall(r'\{\{[^}]+\}\}', html)
    if left: sys.exit(f'{slug}: placeholders sobrando {left[:5]}')
    out = os.path.join(PUB, 'apresentacoes', slug, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    capa = os.path.join(ED, slug, 'capa.webp')
    if os.path.exists(capa): shutil.copyfile(capa, os.path.join(os.path.dirname(out), 'capa.webp'))
    print(f'  {slug:<24} {len(cfg["_telas"]):>2} telas  {len(html.encode())/1e6:.2f} MB' + ('  (rascunho: fora do catálogo)' if cfg.get('rascunho') else ''))

def card(cfg):
    slug = cfg['slug']
    lp = logo_path(slug, cfg)
    passos = sum(1 for _ in cfg['_telas'])
    return {
        'slug': slug,
        'titulo': cfg.get('titulo', 'Como Encantar Seu Time'),
        'evento': cfg.get('evento', ''),
        'cliente': cfg.get('cliente', ''),
        'cidade': cfg.get('cidade', ''),
        'data': cfg.get('data', ''),
        'duracao': cfg.get('duracao_min'),
        'categoria': cfg['categoria'],
        'fixa': cfg.get('fixa', True),
        'telas': passos,
        'logo': data_uri(lp) if lp else '',
        'capa': os.path.exists(os.path.join(ED, slug, 'capa.webp')),
    }

def build_pages(cfgs):
    dados = json.dumps([card(c) for c in cfgs if not c.get('rascunho')], ensure_ascii=False).replace('</', '<\\/')
    for src, dst in [('index.html', 'apresentacoes/index.html'), ('entrar.html', 'entrar/index.html')]:
        page = read(os.path.join(CAT, src)).replace('{{FONTS}}', FONTS).replace('{{DADOS}}', dados)
        page = page.replace('{{IMG:capa}}', IMGS['capa'])
        page = conv_units(page)
        left = re.findall(r'\{\{[^}]+\}\}', page)
        if left: sys.exit(f'{src}: placeholders sobrando {left[:5]}')
        out = os.path.join(PUB, dst)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(page)
        print(f'  {dst}')

def main():
    slugs = sorted(d for d in os.listdir(ED) if os.path.exists(os.path.join(ED, d, 'edicao.json')))
    cfgs = [load(s) for s in slugs]
    alvo = sys.argv[1:] or slugs
    # remove pastas de edições que não existem mais
    ap = os.path.join(PUB, 'apresentacoes')
    if os.path.isdir(ap):
        for d in os.listdir(ap):
            if os.path.isdir(os.path.join(ap, d)) and d not in slugs: shutil.rmtree(os.path.join(ap, d))
    print('edições:')
    for c in cfgs:
        if c['slug'] in alvo: build_deck(c)
    print('páginas:')
    build_pages(cfgs)
    shutil.copyfile(os.path.join(CAT, '_headers'), os.path.join(PUB, '_headers'))
    old = os.path.join(PUB, 'index.html')
    if os.path.exists(old): os.remove(old)

if __name__ == '__main__':
    main()
