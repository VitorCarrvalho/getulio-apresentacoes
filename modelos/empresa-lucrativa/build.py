#!/usr/bin/env python3
"""Monta o modelo "Empresa Lucrativa" (77 telas numeradas) reaproveitando CSS, fontes e script da palestra-base.
Saída: out/empresa-lucrativa-modelo/index.html (+ pasta videos/ com instruções)."""
import json, re, os, base64, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(R, 'fonte')
L = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(L, 'out', 'empresa-lucrativa-modelo')
sys.path.insert(0, os.path.join(R, 'ferramentas'))

def read(p): return open(p, encoding='utf-8').read()
U = re.compile(r'(?<![\w#.\-])(-?\d+(?:\.\d+)?)u\b')
def conv(html):
    html = re.sub(r'(<style>)(.*?)(</style>)', lambda m: m.group(1) + U.sub(lambda x: f'calc(var(--u)*{x.group(1)})', m.group(2)) + m.group(3), html, flags=re.S)
    # unidades "u" também nos style="" inline do corpo
    return re.sub(r'style="([^"]*)"', lambda m: 'style="' + U.sub(lambda x: f'calc(var(--u)*{x.group(1)})', m.group(1)) + '"', html)

FONTS = read(os.path.join(F, 'assets/fonts.css'))
IMGS = json.load(open(os.path.join(F, 'assets/imgs.json')))
ICONS = json.load(open(os.path.join(F, 'assets/icons.json')))
MIME = {'.webp': 'image/webp', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg'}
for fn in os.listdir(os.path.join(L, 'assets')):
    k, ext = os.path.splitext(fn)
    if ext in MIME and k not in ('logo-atitude',):
        IMGS[k] = f'data:{MIME[ext]};base64,' + base64.b64encode(open(os.path.join(L, 'assets', fn), 'rb').read()).decode()

HEAD = read(os.path.join(F, 'parts/head.html')).replace('<title>Como Encantar Seu Time · Getúlio Cavalcante</title>', '<title>Empresa Lucrativa · Getúlio Cavalcante (modelo)</title>')
HEAD = HEAD.replace('</head>', read(os.path.join(L, 'parts/extra.css')) + '</head>')
BODY = read(os.path.join(L, 'parts/body.html'))
SCRIPT = read(os.path.join(F, 'parts/script.html'))

# notas do apresentador: uma por slide
NOTES = json.load(open(os.path.join(L, 'parts/notes.json'), encoding='utf-8'))
notes_js = 'const NOTES_BY_ID = ' + json.dumps({f'n{int(k):02d}': [v] for k, v in NOTES.items()}, ensure_ascii=False, indent=1) + ';\n'
SCRIPT = re.sub(r'const NOTES_BY_ID = \{.*?\n\};\n', lambda m: notes_js, SCRIPT, count=1, flags=re.S)

# vídeos locais no lugar do YouTube
VIDEO = read(os.path.join(L, 'parts/video.js'))
SCRIPT = re.sub(r'const Video = \(\(\) => \{.*?\n\}\)\(\);\n', lambda m: VIDEO, SCRIPT, count=1, flags=re.S)
SCRIPT = SCRIPT.replace("if (location.protocol === 'file:' && window.__ROLE === 'audience') hint.innerHTML += '<br><span style=\"color:#D4AF37\">Arquivo local: os vídeos do YouTube só tocam pelo link online.</span>';\n", '')
SCRIPT = SCRIPT.replace("if (slides[cur].dataset.video) { Video.toggle(); return; }", "if (slides[cur].dataset.videoFile) { Video.toggle(); return; }")
SCRIPT = SCRIPT.replace("slides[S.i].dataset.video ?", "slides[S.i].dataset.videoFile ?")
SCRIPT = SCRIPT.replace('{{SYNC_SUFFIX}}', '-lucrativa-modelo').replace("'Apresentador · Como Encantar Seu Time'", "'Apresentador · Empresa Lucrativa'")
SCRIPT = SCRIPT.replace('`Tela ${S.i + 1} de ${S.steps.length}` + (S.pn ? ` · slide ${S.pn} do roteiro` : \'\')', '`Slide ${S.i + 1} de ${S.steps.length}`')
for a in ['Video.enter', 'dataset.videoFile', 'NOTES_BY_ID = {\n "n01"']:
    assert a in SCRIPT, a

logo = f'\n    <div class="clogo in" style="--d:1.7"><i></i><img src="data:image/svg+xml;base64,{base64.b64encode(open(os.path.join(L, "assets/logo-atitude.svg"), "rb").read()).decode()}" alt="Igreja Batista Atitude"></div>'
html = conv(HEAD + BODY.replace('{{CLIENT_LOGO}}', logo) + SCRIPT)
html = html.replace('{{FONTS}}', FONTS)
html = re.sub(r'\{\{IMG:(\w+)\}\}', lambda m: IMGS[m.group(1)], html)
html = re.sub(r'\{\{IC:(\w+)\}\}', lambda m: ICONS[m.group(1)], html)
html = re.sub(r'\{\{LOGO:(\d+)\}\}', lambda m: read(os.path.join(F, f'assets/image-13-{m.group(1)}.svg')).replace('<svg ', '<svg role="img" preserveAspectRatio="xMidYMid meet" '), html)
html = html.replace('{{QR}}', read(os.path.join(F, 'assets/qr.svg')))
left = re.findall(r'\{\{[^}]+\}\}', html)
if left: sys.exit(f'placeholders sobrando {left[:5]}')
os.makedirs(os.path.join(OUT, 'videos'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(OUT, 'videos', 'LEIA-ME.txt'), 'w', encoding='utf-8').write(
    'Coloque aqui os três vídeos, com estes nomes exatos:\n\n'
    '  abertura.mp4      (slide 2, vídeo de abertura)\n'
    '  casa.mp4          (slide 16, vídeo da casa)\n'
    '  encerramento.mp4  (slide 76, vídeo de encerramento)\n\n'
    'Abra o index.html com duplo clique. O vídeo toca sozinho, com som, quando entra o slide.\n'
    'Se o arquivo não estiver aqui, o slide mostra um botão para escolher o vídeo ou arrastar o arquivo para a tela.\n'
    'Pausar ou retomar: tecla V, clique na tela ou botão Vídeo no modo apresentador.\n')
print(f'{OUT}/index.html  {len(html.encode())/1e6:.2f} MB')
