# Story diário "Bom dia, Portugal" (Loja do Imigrante)
Não é publicado no site (excluído do FTP).
1. Buscar a previsão de hoje para Lisboa, Porto e Faro (ferramenta de tempo) e gravar tempo.json:
   [{"nome":"Lisboa","max":..,"min":..,"chuva":..,"condicao":"clear"}, {"nome":"Porto",...}, {"nome":"Faro",...}]
2. python3 stories/gerar.py tempo.json AAAA-MM-DD  -> cria LojaDoImigrante_story_tempo_AAAA-MM-DD.jpg
3. calendario.json = prazos (tipo prazo/aviso); dicas.json = dicas checadas, uma por dia em rodízio.
Regra: nunca inventar prazo. Itens com "confirmar": true devem ser conferidos na agenda fiscal oficial antes do dia.
