# slug do site -> (doc do painel, categoria, veredito, pasta/arquivo da capa)
# veredito: ("ok"|"warn"|"bad"|"info", rótulo)
E = [
 ("moro-luchsinger-video", "checagem_moro_3d", "checagem", ("warn", "FALTA CONTEXTO"), "moro/LojaDoImigrante_checagem_Moro_capa.jpg"),
 ("debate-band-lula-flavio", "checagem_debate_band_3d", "eleicoes", ("info", "FRASES CHECADAS"), "deb/LojaDoImigrante_checagem_debate_Band_capa.jpg"),
 ("cidadania-espanhola-2-anos", "cidadania_espanhola_3d", "checagem", ("warn", "MEIA VERDADE"), "esp/LojaDoImigrante_cidadania_espanhola_capa.jpg"),
 ("manifestacao-habitacao-lisboa", "manifestacao_habitacao_3d", "portugal", ("info", "EXPLICADO"), "hab/LojaDoImigrante_manifestacao_habitacao_capa.jpg"),
 ("wagner-moura-terras-raras", "checagem_terras_raras_3d", "checagem", ("warn", "FALTA CONTEXTO"), "wag/LojaDoImigrante_checagem_terras_raras_capa.jpg"),
 ("janja-parou-de-viajar", "checagem_janja_3d", "checagem", ("bad", "NÃO É VERDADE"), "janja/LojaDoImigrante_checagem_Janja_capa.jpg"),
 ("luchsinger-acusacao-lula", "checagem_luchsinger_3d", "checagem", ("warn", "NÃO PROVADO"), "luch/LojaDoImigrante_checagem_Luchsinger_capa.jpg"),
 ("brics-eleicao", "brics_3d", "eleicoes", ("info", "PRÓS E CONTRAS"), "brics/LojaDoImigrante_BRICS_eleicao_capa.jpg"),
 ("checagem-10-mil-reais-imposto", "checagem_10mil_3d", "checagem", ("bad", "CONTA ERRADA"), "site/10mil_frame.png"),
 ("passaporte-metade-do-preco", "passaporte_3d", "portugal", ("ok", "CONFIRMADO"), "pas/LojaDoImigrante_passaporte_mais_barato_capa.jpg"),
 ("eleicoes-empate-tecnico", "eleicoes_empate_3d", "eleicoes", ("info", "EXPLICADO"), "elc/LojaDoImigrante_eleicoes_empate_tecnico_capa.jpg"),
 ("brasileiros-em-portugal", "brasileiros_pt_3d", "portugal", ("ok", "DADOS OFICIAIS"), "brz/LojaDoImigrante_brasileiros_em_Portugal_3D_capa.jpg"),
 ("fim-da-escala-6x1", "escala6x1_3d", "eleicoes", ("info", "EXPLICADO"), "v3d/LojaDoImigrante_escala_6x1_3D_capa.jpg"),
 ("urna-eletronica-hackeada", "urna", "checagem", ("bad", "NÃO É VERDADE"), "urn/LojaDoImigrante_urna_capa.jpg"),
 ("ozempic-pib-dinamarca", "ozempic", "mundo", ("info", "CURIOSIDADE"), "ozm/LojaDoImigrante_Ozempic_capa.jpg"),
 ("segundo-turno-exterior", "segundo_turno", "eleicoes", ("info", "GUIA"), "elx/LojaDoImigrante_segundo_turno_capa.jpg"),
 ("muro-de-berlim", "berlim", "mundo", ("info", "HISTÓRIA"), "ber/LojaDoImigrante_Muro_de_Berlim_capa.jpg"),
 ("china-filho-unico", "china", "mundo", ("info", "CURIOSIDADE"), "chn/LojaDoImigrante_China_capa.jpg"),
 ("sns-estrangeiros", "sns", "portugal", ("warn", "FALTA CONTEXTO"), "sns/LojaDoImigrante_SNS_capa.jpg"),
 ("habitacao-porto-lisboa", "habitacao", "portugal", ("info", "EXPLICADO"), "hab/LojaDoImigrante_habitacao_capa.jpg"),
 ("tap-lufthansa", "tap", "portugal", ("info", "EXPLICADO"), "tap/LojaDoImigrante_TAP_capa.jpg"),
 ("irregular-em-portugal-e-crime", "irregular", "portugal", ("warn", "FALTA CONTEXTO"), "irr/LojaDoImigrante_irregular_capa.jpg"),
 ("irs-novembro-retencao", "irs", "portugal", ("info", "EXPLICADO"), "irs2/LojaDoImigrante_IRS_capa_amarela.jpg"),
]
CATS = [("todos", "Todos"), ("urgente", "● Última hora"), ("checagem", "Checagens"), ("eleicoes", "Eleições 2026"), ("portugal", "Viver em Portugal"), ("mundo", "Mundo")]

# o que circulou nas redes (a afirmação checada). Só para checagens.
CLAIM = {
 "moro-luchsinger-video": "As revelações de Luchsinger mostram que Lula mente",
 "cidadania-espanhola-2-anos": "Brasileiro vira espanhol em 2 anos e não faz prova de espanhol",
 "wagner-moura-terras-raras": "Só o Brasil pode substituir a China nas terras raras",
 "janja-parou-de-viajar": "Depois do processo, a Janja parou de viajar",
 "luchsinger-acusacao-lula": "Empresária diz que Lula a usou como “boi de piranha”",
 "checagem-10-mil-reais-imposto": "Metade do que uma padaria fatura fica com o governo",
 "urna-eletronica-hackeada": "A urna eletrônica pode ser hackeada pela internet",
 "sns-estrangeiros": "Estrangeiros vão ficar sem atendimento no SNS",
 "irregular-em-portugal-e-crime": "Estar irregular em Portugal é crime",
 "passaporte-metade-do-preco": "O passaporte no exterior ficou pela metade do preço",
 "brasileiros-em-portugal": "Quase 1 em cada 3 estrangeiros em Portugal é brasileiro",
}

# ÚLTIMA HORA: slug -> data/hora de publicação (o selo some sozinho depois de 48 h)
URGENT = {
 "manifestacao-habitacao-lisboa": "2026-10-18T17:20:00+02:00",
}
