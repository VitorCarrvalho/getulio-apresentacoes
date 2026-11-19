# Gera parts/body.html do modelo "Empresa Lucrativa" (77 telas = 77 slides do PPTX, mesma ordem)
S = []
def sec(n, cls, inner, extra=''):
    S.append(f'<!-- {n} -->\n<section class="slide {cls}" id="n{n:02d}" data-n="{n:02d}" data-num="{n}"{extra}>\n{inner}\n</section>\n')

def capa(n):
    sec(n, 'withphoto capa', '''  <div class="photo"><img src="{{IMG:capa}}" alt="Getúlio Cavalcante"></div>
  <div class="frame"><div class="body">
    <div class="k in" style="--d:.2">PALESTRA</div>
    <h1 class="h" data-words>Empresa <span class="g">Lucrativa</span></h1>
    <div class="who in" style="--d:1.2">GETÚLIO CAVALCANTE</div>{{CLIENT_LOGO}}
  </div></div>''', ' data-nofoot')

def video(n, nome, arq):
    sec(n, 'vid', f'''  <div class="lv" data-noclick-video></div>
  <div class="frame"><div class="body">
    <div class="play in" style="--d:.1">{{{{IC:play}}}}</div>
    <div class="lbl in" style="--d:.35">{nome.upper()}</div>
    <div class="pick" data-noclick>Arquivo esperado: <b>{arq}</b> (na pasta da apresentação)<br>
      <label>Escolher o vídeo<input type="file" accept="video/*"></label><br>ou arraste o arquivo para esta tela</div>
  </div></div>''', f' data-video-file="{arq}" data-nofoot')

def stmt(n, html, size='m2', cls='', extra=''):
    sec(n, f'stmt {cls}'.strip(), f'''  <div class="frame"><div class="body"><h2 class="h {size}" data-words data-delay="0.2">{html}</h2></div></div>''', extra)

def gold(n, html, size='md'):
    sec(n, 'goldbg ctr stmt', f'''  <div class="frame"><div class="body"><h2 class="h {size}" data-words data-delay="0.5">{html}</h2></div></div>''', ' data-foot="dk"')

LOGOS_A = '''<div class="lg in" style="--d:.30">{{LOGO:1}}</div>
      <div class="lg in" style="--d:.38"><img src="{{IMG:south}}" alt="South Tecnologia"></div>
      <div class="lg in" style="--d:.46">{{LOGO:3}}</div>
      <div class="lg in" style="--d:.54">{{LOGO:4}}</div>
      <div class="lg in" style="--d:.62">{{LOGO:5}}</div>
      <div class="lg in s" style="--d:.70">{{LOGO:6}}</div>
      <div class="lg in" style="--d:.78">{{LOGO:7}}</div>
      <div class="lg in" style="--d:.86">{{LOGO:8}}</div>
      <div class="lg in" style="--d:.94">{{LOGO:9}}</div>
'''

capa(1)
video(2, 'Vídeo de abertura', 'videos/abertura.mp4')
capa(3)
sec(4, 'withphoto sig', '''  <div class="photo"><img src="{{IMG:capa}}" alt="Getúlio Cavalcante"></div>
  <div class="frame"><div class="body">
    <h2 class="h" data-words data-delay="0.4">O que <span class="g">realmente</span> sustenta times.</h2>
    <div class="bar"></div>
    <div class="who in" style="--d:1.6">Getúlio Cavalcante</div>
  </div></div>''')
sec(5, '', '''  <div class="full"><img src="{{IMG:livro}}" alt="Livro Como Encantar Seu Time"></div>''', ' data-nofoot')
sec(6, 'tres', '''  <div class="frame"><div class="body">
    <div class="big in" style="--d:0">3</div>
    <div class="vl"></div>
    <p class="h" data-words data-delay="0.7"><span class="g">perguntas</span> que definem o <span class="g">presente</span> e o <span class="g">futuro</span> dos seus negócios.</p>
  </div></div>''')
stmt(7, 'O que transforma plano em <span class="g">resultado</span>?', 'md')
stmt(8, 'O que separa <span class="g">crescimento</span> de colapso?', 'md')
stmt(9, 'O que faz o negócio <span class="g">existir</span> além de você?', 'md')
stmt(10, '<span class="g">Pessoas.</span>', 'xl')
stmt(11, 'Pessoas <span class="g">certas.</span>', 'l', extra=' data-tr="fade"')
sec(12, 'withphoto bio2', '''  <div class="photo"><img src="{{IMG:bio}}" alt="Getúlio Cavalcante"></div>
  <div class="frame"><div class="body">
    <h2 class="h in" style="--d:.1">Getúlio Cavalcante</h2>
    <ul class="facts">
      <li class="in" style="--d:.45">46 anos</li>
      <li class="in" style="--d:.55">Casado com a Raphaela</li>
      <li class="in" style="--d:.65">Pai do Raphael e do Getulinho</li>
      <li class="in" style="--d:.75">Empresário há 31 anos</li>
      <li class="in" style="--d:.85">Líder, mentor e treinador</li>
      <li class="in" style="--d:.95">Baiano, carioca, mineiro, americano e paulista</li>
    </ul>
  </div></div>''')
sec(13, 'emp', f'''  <div class="fxscan"></div>
  <div class="frame"><div class="body"><div class="logos">
      {LOGOS_A}
  </div></div></div>''')
sec(14, 'emp2', f'''  <div class="frame"><div class="body">
    <div class="logos">
      {LOGOS_A}
    </div>
    <div class="vl"></div>
    <ul class="nums">
      <li class="in" style="--d:.5">Presença em <b>14 estados</b></li>
      <li class="in" style="--d:.65">Mais de <b>130 lojas</b> e escritórios</li>
      <li class="in" style="--d:.8">Mais de <b>1.500 colaboradores</b></li>
      <li class="in" style="--d:.95">Mais de <b>20 eventos</b> por ano</li>
      <li class="in" style="--d:1.1">Mais de <b>R$ 500 milhões</b> de faturamento por ano</li>
    </ul>
  </div></div>''')
sec(15, 'withphoto', '''  <div class="photo"><img src="{{IMG:bw}}" alt="Getúlio Cavalcante"></div>
  <div class="frame"><div class="body">
    <h2 class="h" style="font-size:99u;max-width:1000u" data-words data-delay="0.9">Mas quem eu sou <span class="g">realmente?</span></h2>
  </div></div>''')
video(16, 'Vídeo da casa', 'videos/casa.mp4')
stmt(17, 'Pessoas <span class="g">certas.</span>', 'l')
stmt(18, 'Ter o <span class="g">time</span> certo.', 'l', extra=' data-tr="fade"')
stmt(19, 'O <span class="g">time</span> que você quer é o time que <span class="g">você constrói.</span>', 'md')

TIPOS = [('ADIA', 'DOR'), ('MUDA', 'DOR'), ('FAZE', 'DOR'), ('SUPERA', 'DOR')]
def qv(n, k):
    ts = ''
    for i, (p, s) in enumerate(TIPOS[:k]):
        c = 't' + (' act' if i == k - 1 else '') + (' new' if i == k - 1 else '')
        ts += f'\n      <div class="{c}"><span class="p">{p}</span><span class="s">{s}</span></div>'
    sec(n, 'qv', f'''  <div class="frame"><div class="body">
    <h2 class="h{' in' if k == 0 else ''}" style="--d:.1">Quem <span class="g">é você?</span></h2>
    <div class="types">{ts}
    </div>
  </div></div>''', ' data-tr="fade"' if k else '')
for i in range(5): qv(20 + i, i)

gold(25, 'Se você é o maior da mesa, está sentado na mesa errada.', 'md')

MESAS = [('Receber', '(aprender)'), ('Dar', '(ensinar)'), ('Ser', '')]
def mesas(n, k):
    cols = ''
    for i, (a, b) in enumerate(MESAS):
        cl = 'col' + (' off' if i >= k else '') + (' new' if i == k - 1 else '')
        cols += f'''\n      <div class="{cl}"><div class="lb"><span>{a}{f'<small>{b}</small>' if b else ''}</span></div><img src="{{{{IMG:mesa}}}}" alt="Mesa"></div>'''
    sec(n, 'mesas', f'''  <div class="frame"><div class="body">
    <div class="top{' in' if k == 1 else ''}"><span class="n">3</span><h2 class="h">mesas</h2></div>
    <div class="row">{cols}
    </div>
  </div></div>''', ' data-tr="fade"' if k > 1 else '')
for i in range(3): mesas(26 + i, i + 1)

TIPS = [(29, 5), (1, 28), (-5, 53), (1, 74), (18, 91)]
PIL = ['Ambiente de trabalho', 'Possibilidade de crescimento', 'Orgulho pra quem trabalha', 'Pertencimento', 'Dinheiro']
def mao(n, labels):
    labs = ''
    if labels:
        for i, ((x, y), t) in enumerate(zip(TIPS, PIL)):
            labs += f'\n      <div class="lab" style="left:{x - 1}%;top:{y}%"><span class="in" style="--d:{.6 + i * .15:.2f}">{t}</span></div>'
    sec(n, 'mao' + (' lbls' if labels else ''), f'''  <div class="frame"><div class="body">
    <div class="ttl in" style="--d:.1"><div class="n">5</div><h2 class="h">pilares</h2><div class="sub">PARA ENCANTAR SEU TIME</div></div>
    <div class="handbox in" style="--d:.3"><img src="{{{{IMG:hand0}}}}" alt="Mão">{labs}
    </div>
  </div></div>''', ' data-tr="fade"' if labels else '')
mao(29, False)
mao(30, True)

PILARES = [
    ('amb', 'Ambiente de <span class="g">trabalho</span>', 'Ambiente <span class="g">saudável</span> é <span class="g">físico e emocional</span>, porque ninguém prospera onde <span class="g">não consegue respirar.</span>', 'width:min(60%,1100u);height:100%'),
    ('cresc', 'Possibilidade de <span class="g">crescimento</span>', 'Quando a empresa cresce <span class="g">por dentro</span>, ela cresce <span class="g">por fora.</span>', 'width:min(72%,1450u);height:100%'),
    ('orgulho', 'Orgulho pra quem <span class="g">trabalha</span>', 'Não faça trabalharem <span class="g">para você</span>, faça se orgulharem de <span class="g">caminhar com você.</span>', 'width:min(64%,1200u);height:92%'),
    ('pert', '<span class="g">Pertencimento</span>', 'Pertencimento é o combustível que <span class="g">transforma</span> colaboradores em <span class="g">embaixadores.</span>', 'width:min(62%,1150u);height:88%'),
    ('dinheiro', '<span class="g">Dinheiro</span>', '<span class="g">Gente boa dá</span> retorno, gente ruim dá <span class="g">despesa.</span>', 'width:min(56%,1000u);height:80%;bottom:8%;right:4%'),
]
for i, (img, tt, fr, st) in enumerate(PILARES):
    for k in (0, 1):
        n = 31 + i * 2 + k
        phrase = f'\n    <p class="phrase h" data-words data-delay="0.4">{fr}</p>' if k else ''
        sec(n, 'pil2' + (' dim' if k else ''), f'''  <div class="art" style="{st}"><img src="{{{{IMG:{img}}}}}" alt=""></div>
  <div class="frame"><div class="body" style="justify-content:flex-start">
    <div class="pk in" style="--d:0">PILAR {i + 1} DE 5</div>
    <h2 class="h pt in" style="--d:.1">{tt}</h2>{phrase}
  </div></div>''', ' data-tr="fade"' if k else '')

def duo(n, left, right, cls='', extra=''):
    sec(n, f'duo {cls}'.strip(), f'''  <div class="frame"><div class="body">
    <div class="lft">{left}</div>
    <div class="rgt">{right}</div>
  </div></div>''', extra)
POSI = '<h2 class="h tt in" style="--d:.1">Posicione-se</h2>'
duo(41, POSI, '<p class="h" data-words data-delay="0.5">Lidere com <span class="g">coragem</span>, assuma <span class="g">responsabilidades</span> e <span class="g">inspire</span> os outros <span class="g">com ações</span>, não apenas com palavras.</p>')
def fonte(num, linhas, d=.1):
    return f'<div class="fonte in" style="--d:{d}"><div class="n">{num}</div><div class="tx">' + ''.join(f'<span{" class=g" if g else ""}>{t}</span>' for t, g in linhas) + '</div></div>'
duo(42, fonte(7, [('fontes de', 0), ('poder', 0), ('da liderança', 1)]), '')
F6 = fonte(6, [('fontes de', 0), ('poder', 0), ('do líder', 1)])
duo(43, F6, '<ul class="poderes">' + ''.join(f'<li class="in" style="--d:{.4 + i * .12:.2f}">{p}</li>' for i, p in enumerate(['Dinheiro', 'Influência', 'Conhecimento', 'Carisma', 'Hierarquia', 'Medo'])) + '</ul>')
duo(44, F6, '<p class="p1 in" style="--d:.4">Todo líder usa instintivamente <span class="g">2 poderes.</span></p>', extra=' data-tr="fade"')
duo(45, F6, '<p class="p1">Todo líder usa instintivamente <span class="g">2 poderes.</span></p><p class="p2 in" style="--d:.4">Mas deve saber usar todos quando necessário.</p>', extra=' data-tr="fade"')
sec(46, 'ext2', '''  <div class="ph"><img src="{{IMG:ext}}" alt="Extintor"></div>
  <div class="frame"><div class="body">
    <h2 class="h" data-words data-delay="0.6" data-step-ms="70">Alguns poderes são como extintores: <span class="g">protegem quando usados na emergência</span> e destroem o ambiente quando viram rotina.</h2>
  </div></div>''')
duo(47, fonte(7, [('fontes de', 0), ('poder', 0), ('espírito do líder', 1)]), '<div class="huge" data-words data-delay="0.8">Propósito</div>')
duo(48, POSI, '<p class="h" data-words data-delay="0.5">Quando você não ocupa <span class="g">o seu lugar de líder</span>, alguém sem os seus <span class="g">valores ocupa.</span></p>')
sec(49, 'pont2', '''  <div class="frame"><div class="body dia-row">
    <div class="txt"><h2 class="h in" style="--d:.1">Posicione-se</h2></div>
    <div class="diag">
      <svg class="lines" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path class="draw" style="--d:.7" pathLength="1" d="M49 51 L17.5 10.5"/>
        <path class="draw" style="--d:.8" pathLength="1" d="M49 51 L82.5 10.5"/>
        <path class="draw" style="--d:.9" pathLength="1" d="M49 51 L17.5 89.5"/>
        <path class="draw" style="--d:1.0" pathLength="1" d="M49 51 L82.5 89.5"/>
      </svg>
      <div class="node pop" style="left:0;top:0;--d:1.3"><span class="ic">{{IC:hand}}</span>Sócios e acionistas</div>
      <div class="node pop" style="left:65%;top:0;--d:1.4"><span class="ic">{{IC:chart}}</span>Clientes</div>
      <div class="node pop" style="left:0;top:79%;--d:1.5"><span class="ic">{{IC:people}}</span>Colaboradores</div>
      <div class="node pop" style="left:65%;top:79%;--d:1.6"><span class="ic">{{IC:building}}</span>Empresa</div>
      <div class="hub pop" style="--d:.3">Liderança</div>
    </div>
  </div></div>''')
sec(50, 'ciclo2', '''  <div class="frame"><div class="body dia-row">
    <div class="txt"><h2 class="h in" style="--d:.1">Ciclo virtuoso</h2><div class="sub in" style="--d:.25">LIDERANÇA EFICAZ</div></div>
    <div class="diag">
      <svg class="lines" viewBox="0 0 100 100" preserveAspectRatio="none">
        <path class="draw" style="--d:.8" pathLength="1" d="M50 10 L85 49"/>
        <path class="draw" style="--d:1.1" pathLength="1" d="M85 49 L50 90"/>
        <path class="draw" style="--d:1.4" pathLength="1" d="M50 90 L15 49"/>
        <path class="draw" style="--d:1.7" pathLength="1" d="M15 49 L50 10"/>
      </svg>
      <div class="node pop" style="left:50%;top:10%;--d:.7">Motivação</div>
      <div class="node pop" style="left:85%;top:49%;--d:1.0">Alta performance</div>
      <div class="node pop" style="left:50%;top:90%;--d:1.3">Gera resultados</div>
      <div class="node pop" style="left:15%;top:49%;--d:1.6">Pessoas felizes</div>
      <div class="hub pop" style="--d:.3">Liderança eficaz</div>
    </div>
  </div></div>''')
CUR = '<h2 class="h tt{}"><span>Liderança</span><span class="g">curativa</span></h2>'
duo(51, CUR.format(' in'), '', 'cur2')
duo(52, CUR.format(''), '<div class="it in" style="--d:.2">Conte histórias</div><div class="it in" style="--d:.45">O que fazer</div>', 'cur2', ' data-tr="fade"')
duo(53, CUR.format(''), '<div class="it">Conte histórias</div><div class="it"><span class="strk">O que fazer</span></div><div class="it g in" style="--d:1.6">Por que fazer</div>', 'cur2', ' data-tr="fade"')
MOM = ['Admissão', 'Onboarding', 'Avaliação', 'Feedback', 'Advertência e disciplina', 'Promoção', 'Demissão']
sec(54, 'mom7', '''  <div class="frame"><div class="body">
    <div class="k in" style="--d:0">A LIDERANÇA CURATIVA APLICADA</div>
    <h2 class="h in" style="--d:.12">Os 7 momentos<br>da <span class="g">verdade</span></h2>
    <ul class="list">''' + ''.join(f'\n      <li class="in" style="--d:{.4 + i * .1:.2f}"><b>{i + 1:02d}</b>{m}</li>' for i, m in enumerate(MOM)) + '''
    </ul>
  </div></div>''')
FRASES = [
    'Quando você contrata mal, são os bons que começam a <span class="g">pedir demissão.</span>',
    'Colocar alguém para produzir antes de pertencer é <span class="g">mandá-lo para a guerra</span> sem apresentar seus aliados.',
    'Quem é visto não precisa <span class="g">ser vigiado.</span>',
    'Feedback é para quem você <span class="g">quer que fique.</span>',
    'O líder pode ser amigo, mas <span class="g">nunca pode ser comparsa.</span>',
    'Promova pelo caráter. <span class="g">Competência se treina;</span> caráter se revela quando recebe poder.',
    'Demissão é um ato de <span class="g">amor.</span>',
]
for i, (m, fr) in enumerate(zip(MOM, FRASES)):
    n = 55 + i * 2
    sec(n, 'mom', f'''  <div class="gnum">{i + 1}</div>
  <div class="frame"><div class="body">
    <div class="k in" style="--d:.1">MOMENTO {i + 1}</div>
    <h2 class="h tt in" style="--d:.25">{m}</h2>
  </div></div>''')
    sec(n + 1, 'mom', f'''  <div class="gnum">{i + 1}</div>
  <div class="frame"><div class="body">
    <p class="fr h" data-words data-delay="0.4" data-step-ms="80">{fr}</p>
  </div></div>''', ' data-tr="fade"')
stmt(69, 'Quer ajudar?<br>Dê dinheiro, <span class="g">não emprego.</span>', 'md')
stmt(70, 'Será que isso <span class="g">funciona</span> mesmo?', 'm2')
sec(71, 'prova', '''  <div class="frame"><div class="body">
    <div class="txt">
      <h2 class="h in" style="--d:.15">Ela foi demitida.</h2>
      <div class="ic in" style="--d:.7">{{IC:quote}}</div>
      <blockquote class="serif" data-words data-delay="1.0">“A demissão foi fator crucial para eu me encontrar.”</blockquote>
    </div>
    <div class="shot"><img src="{{IMG:print1}}" alt="Print da conversa"></div>
  </div></div>''')
sec(72, 'prova', '''  <div class="frame"><div class="body">
    <div class="txt">
      <h2 class="h in" style="--d:.15">Ela também saiu da empresa.</h2>
      <div class="ic in" style="--d:.7">{{IC:quote}}</div>
      <blockquote class="serif" data-words data-delay="1.0">“Até hoje, carrego os aprendizados que tive com você.”</blockquote>
    </div>
    <div class="shot"><img src="{{IMG:print2}}" alt="Print da conversa"></div>
  </div></div>''')
gold(73, 'Quando até quem sai defende a cultura, ela não era discurso.', 'md')
sec(74, 'sem2', '''  <div class="art"><img src="{{IMG:semeador}}" alt=""></div>
  <div class="frame"><div class="body">
    <h2 class="h in" style="--d:.1">O semeador</h2>
    <div class="sub in" style="--d:.3">MATEUS 13</div>
  </div></div>''')
sec(75, 'sem2 dim', '''  <div class="art"><img src="{{IMG:semeador}}" alt=""></div>
  <div class="frame"><div class="body">
    <div class="lines">
      <span class="in" style="--d:.3">Nem toda <span class="g">semente brota.</span></span>
      <span class="in" style="--d:.7">Nem todo <span class="g">broto cresce.</span></span>
      <span class="in" style="--d:1.1">Nem todo <span class="g">pé dá fruto.</span></span>
    </div>
    <h2 class="h fim in" style="--d:1.9">Mas <span class="g">todo fruto</span> que nasce carrega <span class="g">novas sementes.</span></h2>
  </div></div>''', ' data-tr="fade"')
video(76, 'Vídeo de encerramento', 'videos/encerramento.mp4')
sec(77, 'withphoto fim2', '''  <div class="photo"><img src="{{IMG:familia}}" alt="Getúlio e família"></div>
  <div class="frame"><div class="body">
    <h2 class="h" style="font-size:64u;line-height:1.3;max-width:900u" data-words data-delay="0.8" data-step-ms="70"><span class="g">O sonho de um líder</span> só é grande quando, nele, <span class="g">cabem os sonhos</span> de quem caminha ao seu lado.</h2>
    <div class="bot" style="display:flex;align-items:center;gap:50u;margin-top:90u">
      <div>
        <div class="serif g in" style="--d:2.4;font-size:69u">Muito obrigado!</div>
        <div class="in" style="--d:2.6;font-size:35u;font-weight:700;margin-top:14u">@getulio.cavalcante</div>
      </div>
      <div class="qr in" style="--d:2.8;width:180u;height:180u;background:#fff;border-radius:12u;padding:14u">{{QR}}</div>
    </div>
  </div></div>''', ' data-nofoot')

assert len(S) == 77, len(S)
pre = '''<body class="modelo">
<div id="hint">F · tela cheia &nbsp;&nbsp; P · modo apresentador &nbsp;&nbsp; → avançar &nbsp;&nbsp; número + pausa · pular para o slide</div>
<button id="presBtn" class="ctl" type="button" title="Modo apresentador (P)">Apresentador</button>
<button id="fsBtn" class="ctl" type="button" title="Tela cheia (F)">Tela cheia</button>

<main id="deck">

'''
post = '''
</main>
<footer id="foot"><span>@getulio.cavalcante</span><span class="num"></span></footer>
<nav id="hud"></nav>
'''
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'parts', 'body.html'), 'w').write(pre + ''.join(S) + post)
print('ok', len(S))
