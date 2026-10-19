# Produção Loja do Imigrante (backup)
Não vai para o site (excluído do FTP).
- modelo_video_3d/: pipeline do vídeo 3D (three.js em Chromium headless + cairo). Último usado: checagem do Moro.
  Passos: voz.mp3 -> ffmpeg -ac 1 -ar 48000 voz48.wav; phrases.py (frases da fala, números em dígitos + OVERRIDE de sílabas);
  python3 align.py > meas.txt -> colar em MEASURED_V do timeline.py; marcos kw() em M; scene.html (capítulos + CAM); compose.py (textos);
  python3 -m http.server <porta> (porta igual à do compose.py); python3 mix.py; ./render.sh. node_modules: npm i three.
- site_gerador/: build.py + entries.py (gera alojadoimigrante.com/checagens a partir de painel_docs). Ajustar ROOT/caminhos das capas.
- painel_docs/: cópia dos documentos do Painel (artifact HN7sHug2tkqQhYTG1iMoeK, coleção "videos").
- legendas/, youtube/: textos prontos.
Regras: apartidário, mesmas cores para candidatos, sem fotos, marcar ilustração, não inventar dado, CTA WhatsApp/link da bio (discreto em eleição).
