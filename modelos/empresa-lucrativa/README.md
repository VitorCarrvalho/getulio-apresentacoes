# Empresa Lucrativa · modelo (77 telas)

Recriação em HTML do PPTX "Atitude_Alphavile_Novembro_-_Completo_-_2026" (77 slides, mesma ordem), em preto e dourado.
Modelo de trabalho: cada tela mostra o número do slide (classe `modelo` no body). Na versão definitiva, tirar a classe.

- `gen_body.py` gera `parts/body.html` (uma section por slide, id n01..n77).
- `parts/extra.css` estilos próprios; `parts/video.js` vídeos locais (videos/abertura.mp4, casa.mp4, encerramento.mp4); `parts/notes.json` notas do apresentador.
- `assets/` ilustrações de giz e fotos recortadas do PPTX (WebP), logo da Atitude.
- `python3 gen_body.py && python3 build.py` → `out/empresa-lucrativa-modelo/index.html` (fora de publicar/: não vai para o ar).
