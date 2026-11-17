# Apresentações do Getúlio Cavalcante

Catálogo de palestras publicado em **lideresdosucesso.com/apresentacoes** (Cloudflare Worker com arquivos estáticos, ligado a este repositório; endereço técnico: getulio-apresentacoes.vitorcarrvalho.workers.dev). Todo push na `main` vai direto para produção.

A palestra-base é "Como Encantar Seu Time", recriada a partir do PowerPoint (55 slides) como **um único arquivo HTML autossuficiente**: fontes, imagens, ícones e QR code embutidos em base64. Roda offline com duplo clique. Formato principal: **painel de LED wide, cerca de 3:1**; também precisa funcionar em 2,4:1, 16:9, 16:10 e 4:3. São 46 telas e 55 cliques, na mesma sequência do PowerPoint (os slides 22 a 26 e 33 a 38 viraram uma tela com revelação a cada clique).

Cada **edição** é a palestra-base com escolha de telas (e ordem), logo do cliente na capa e dados para o catálogo. A "Original" é a palestra completa, sem logo.

## Estrutura
```
fonte/parts/head.html       CSS (tokens, slides, responsivo, animações, logo do cliente na capa)
fonte/parts/body.html       HTML das 46 telas (cada <section id="s-..."> é uma tela)
fonte/parts/script.html     JS: navegação, builds, contadores, vídeos, modo apresentador, notas
fonte/assets/               fontes, imagens WebP (imgs.json), ícones (icons.json), logos (image-13-N.svg), qr.svg
edicoes/<slug>/edicao.json  configuração de cada edição (+ logo do cliente + capa.webp do card)
catalogo/index.html         tela do catálogo (cards, busca, filtros, favoritos)
catalogo/entrar.html        tela do token
catalogo/_headers           cabeçalhos HTTP copiados para publicar/
src/worker.js               Worker: proteção por token e entrega dos arquivos de publicar/
wrangler.jsonc              configuração do Worker (pasta publicar/, nome do projeto)
ferramentas/build.py        monta tudo em publicar/
ferramentas/textcheck.js    confere o texto de cada edição contra o PPT
ferramentas/capas.js        gera a miniatura do card (edicoes/<slug>/capa.webp)
ferramentas/shots.js        screenshots do estado final das telas
ferramentas/sheet.py        junta screenshots em folhas de revisão
ferramentas/vec.py          vetoriza logos PNG (potracer)
original/                   o .pptx original e ppt_text.json (texto oficial extraído)
publicar/                   SAÍDA DO BUILD. É o que o Cloudflare publica. Nunca edite à mão.
```
No CSS, `120u` vira `calc(var(--u)*120)` no build. `--u = min(100vw/1778, 100vh/1000)`.

Dependências: Python 3 com Pillow (e potracer para vetorizar), Node com Playwright/Chromium.

## edicao.json
```json
{
  "slug": "premium",                    // pasta e endereço: /apresentacoes/premium/  (minúsculas, números, hífen)
  "titulo": "Como Encantar Seu Time",
  "evento": "Premium Proteção Veicular", // nome grande do card
  "cliente": "Premium Proteção Veicular",// texto alternativo do logo e busca
  "cidade": "São Paulo, SP",
  "data": "2026-12-05",                 // AAAA-MM-DD ou ""
  "duracao_min": 50,
  "categoria": "empresa",               // original | empresa | igreja | evento
  "fixa": true,                         // false = temporária: sai do catálogo depois da data, o link continua
  "logo": "logo.svg",                   // arquivo dentro de edicoes/<slug>/ ou "" (só aparece na capa)
  "logo_altura": 110,                   // opcional, em unidades de desenho
  "qr": true,                           // false tira o QR do encerramento
  "telas": "todas"                      // ou lista de ids em ordem: ["s-capa","s-vid1",...,"s-fim"]
}
```
Regras da edição: `s-capa` e `s-fim` são obrigatórias. Só o logo entra (nenhum texto novo nos slides). Paleta sempre a do Getúlio. Notas do apresentador são as mesmas da base. Os vídeos (`s-vid1`, `s-vid2`) e os prints (`s-prova1`, `s-prova2`) entram ou saem conforme o evento.

Ids das telas, na ordem: s-capa, s-vid1, s-livro, s-3p, s-q1, s-q2, s-q3, s-p1, s-p2, s-p3, s-bio, s-lab, s-emp, s-quem, s-chev, s-hist, s-time, s-160, s-vir, s-mesmas, s-dois, s-quem2 (22-26), s-energia, s-pod, s-2pod, s-ext, s-7, s-dom, s-pil (33-38), s-posi, s-ocupa, s-pont, s-ciclo, s-disc, s-mesas, s-agua, s-cur, s-conte, s-func, s-prova1, s-prova2, s-cult, s-sem, s-vid2, s-prom, s-fim.

## Rotina de mudança
1. Edite `fonte/` ou `edicoes/` (nunca `publicar/`).
2. `python3 ferramentas/build.py`
3. `node ferramentas/textcheck.js` → toda edição com `bad 0` e nenhuma linha `EXTRA`.
4. Se a capa mudou: `node ferramentas/capas.js <slug>` e `python3 ferramentas/build.py` de novo.
5. Screenshots: `node ferramentas/shots.js $PWD/publicar/apresentacoes/<slug>/index.html /tmp/shots 3000x1000 1920x1080 1024x768` e folhas com `sheet.py`. Olhe: texto sobreposto, cortes, legibilidade.
6. Commit e push na `main` → Cloudflare publica sozinho em 1 a 2 minutos.

## Acesso e Cloudflare
- Projeto Cloudflare **Worker** (Workers Builds) ligado ao GitHub. Tudo que importa está no `wrangler.jsonc`: os arquivos vêm de `publicar/` e passam antes pelo `src/worker.js`. Não precisa de build no Cloudflare: o `publicar/` já vai pronto no commit.
- Senha: secret **ACCESS_TOKEN** em Worker → Settings → Variables and Secrets. Sem ela, o site fica todo bloqueado. `keep_vars: true` impede que o deploy apague variáveis do painel.
- Quem acerta o token ganha um cookie assinado de 7 dias. Trocar a senha derruba todos os acessos. "Sair" no catálogo apaga o cookie.
- `/` redireciona para `/apresentacoes/`. A tela do token é `/entrar/`.
- Domínio: Worker → Settings → Domains & Routes → Custom domain `lideresdosucesso.com`.
- Favoritos ficam no navegador de cada aparelho.
- Teste local: `ACCESS_TOKEN=x` em `.dev.vars` e `npx wrangler dev`.

## Regras do cliente (obrigatórias)
1. **Texto 100% fiel ao PowerPoint.** Não altere, corrija nem "melhore" nenhuma palavra, acento ou pontuação. Depois de qualquer mudança, rode `node ferramentas/textcheck.js`: cada edição tem que dar `bad 0` e nenhuma linha `EXTRA`. Texto novo só entra se eu pedir.
2. **Preserve a paleta, as imagens e a identidade:**
   - Fundos: #141416, #1A1A1D, #2C2C31.
   - Dourado: #D4AF37 (destaques). Creme: #F5F2EA (texto). Cinza: #8F8A82 (texto secundário). #8A6D16 é o kicker sobre fundo creme.
   - Slides inteiros em dourado: 16, 21, 27, 32, 40, 45, 51. Slides com fundo creme: 28 e 44.
   - Fontes: Montserrat e Cormorant Garamond itálico (nas citações).
3. **Animação só na transição e na composição de cada slide.** Ela toca uma vez e para. **Nada pode ficar animado o tempo todo** (sem loops, partículas, brilhos, fundos vivos, efeitos que seguem o mouse) para não roubar a atenção da plateia. Estilo:
   - **Cinema** na base: fade com desfoque e zoom leve, sóbrio e luxuoso.
   - Momentos **Tech:** grade e linhas douradas finas que montam a composição e somem. Hoje estão nos slides 12, 13, 18, 19, 28, 33, 41, 42 e 44.
4. **Responsiva:** prioridade 3:1. Teste sempre com `shots.js` em 3000x1000, 2400x1000, 1920x1080, 1920x1200 e 1024x768, e olhe as folhas de revisão: texto sobreposto, cortes, legibilidade.
5. **Sem som/trilha.** O único som é o dos vídeos.
6. **Arquivo único e offline.** Nada de CDN ou fonte externa. A exceção são os vídeos do YouTube.
7. Estilo desejado: chique, futurista, fluido, elegante, que envolva quem assiste.

## Vídeos (YouTube)
- Slide 2 "VÍDEO DE ABERTURA" = Trajetória: https://youtu.be/4YjHS1yJxWU (`data-video="4YjHS1yJxWU"`)
- Slide 53 "VÍDEO DOS LÍDERES" = Homenagem: https://youtu.be/5pnLUOv5Bnk (`data-video="5pnLUOv5Bnk"`)
- Como funcionam:
  - O vídeo toca sozinho, com som, quando o passador entra no slide. O player é criado ao entrar e destruído ao sair.
  - O iframe não pega o foco, então o passador continua comandando.
  - Quando o vídeo termina, volta o card do slide, sem vídeos sugeridos.
  - Pausar ou retomar: tecla V/K, clique no painel ou botão "Vídeo" no apresentador.
  - Os espelhos do modo apresentador não carregam o vídeo, para não duplicar o som.
- Só tocam online (link do Cloudflare). Em arquivo local, o YouTube dá erro 153, então o HTML mantém o card e avisa na dica inicial.
- O dono dos vídeos precisa deixar "Permitir incorporação" ligado no YouTube.
- Alternativa offline, se pedirem: MP4 locais com `<video>`. Nesse caso a entrega vira uma pasta em vez de um arquivo único, e o limite do Cloudflare é 25 MB por arquivo.

## Navegação e modo apresentador (não quebrar)
- → / espaço / Enter / PageDown avançam. ← / PageUp voltam. F = tela cheia. P = modo apresentador. Número + pausa pula para a tela. `#N.P` na URL abre a tela N no passo P. `?mirror` mostra o estado final sem animação (usado nos testes).
- Papéis por URL: sem parâmetro = painel; `?presenter` = retorno; `?mirror` = miniaturas.
- A tecla P e os botões chamam **só** `window.open`, nada de tela cheia junto. Senão o Chrome bloqueia o pop-up.
- A sincronização usa postMessage, BroadcastChannel e localStorage, com deduplicação por id. Sem isso, um clique avança até 3 vezes.
- `var Sync` (não `const`). Pop-up bloqueado → toast com link, nunca `alert()`.
- O retorno mostra:
  - a tela atual e o próximo clique;
  - as notas (`NOTES_BY_ID` em script.html, uma entrada por passo);
  - "Tela X de 46 · slide N do roteiro";
  - cronômetro e relógio.
- Builds por clique: `data-steps` na section; `data-show="n"` / `data-only="n"` / `data-active="n"` nos elementos. O rodapé usa `data-num`, ou `data-nums` nas telas agrupadas.

## Fatos confirmados
- Filhos: Paulinho, Getulinho e Raphael. Os prints dos slides 49 e 50 têm autorização.
- QR code: https://www.instagram.com/getulio.cavalcante/
- Logos do grupo: vetorizados, exceto o da South (PNG original por causa da linha fina "Tecnologia").
- Palestra completa: cerca de 120 minutos.
