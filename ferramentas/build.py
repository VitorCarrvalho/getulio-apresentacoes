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
IMGS = json.load(open(os.path.join(F, 'assets/imgs.json')))
ICONS = json.load(open(os.path.join(F, 'assets/icons.json')))
HEAD = read(os.path.join(F, 'parts/head.html'))
BODY = read(os.path.join(F, 'parts/body.html'))
SCRIPT = read(os.path.join(F, 'parts/script.html'))

SEC = re.compile(r'(?:<!--[^\n]*-->\n)?<section\b[^>]*\bid="([^"]+)"[\s\S]*?</section>\n*')
secs = list(SEC.finditer(BODY))
PRE, POST = BODY[:secs[0].start()], BODY[secs[-1].end():]
SECTIONS = {m.group(1): m.group(0) for m in secs}
ORDEM = [m.group(1) for m in secs]
FIXAS = ['s-capa', 's-fim']          # capa e encerramento nunca saem
CATEGORIAS = {'original', 'empresa', 'igreja', 'evento'}
MIME = {'.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}

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
    telas = ORDEM if cfg.get('telas', 'todas') == 'todas' else cfg['telas']
    desconhecidas = [t for t in telas if t not in SECTIONS]
    assert not desconhecidas, f'{slug}: telas inexistentes {desconhecidas}'
    assert len(set(telas)) == len(telas), f'{slug}: tela repetida'
    for t in FIXAS: assert t in telas, f'{slug}: {t} é obrigatória'
    if cfg.get('logo'): assert os.path.exists(logo_path(slug, cfg)), f'{slug}: logo não encontrado'
    cfg['_telas'] = telas
    return cfg

def build_deck(cfg):
    slug = cfg['slug']
    body = PRE + ''.join(SECTIONS[t] for t in cfg['_telas']) + POST
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
    script = SCRIPT.replace('{{SYNC_SUFFIX}}', '' if slug == 'original' else '-' + slug)
    html = conv_units(HEAD + body + script)
    html = html.replace('{{FONTS}}', FONTS)
    html = re.sub(r'\{\{IMG:(\w+)\}\}', lambda m: IMGS[m.group(1)], html)
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
    print(f'  {slug:<24} {len(cfg["_telas"]):>2} telas  {len(html.encode())/1e6:.2f} MB')

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
    dados = json.dumps([card(c) for c in cfgs], ensure_ascii=False).replace('</', '<\\/')
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
