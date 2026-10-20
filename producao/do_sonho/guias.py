# Guias do Do Sonho à Europa. Cada informação tem fonte; "verificado" = data da conferência.
VERIF = "20/10/2026"

G = [
 dict(slug="nif-e-niss", stage="chegada", tag="Portugal", title="NIF e NISS para estrangeiros",
  card="O NIF (Finanças) e o NISS (Segurança Social) são os primeiros números que você vai precisar em Portugal.",
  intro="Sem NIF não se aluga casa, não se abre conta nem se assina contrato. Sem NISS não se trabalha com contrato. Os dois pedidos são gratuitos.",
  secoes=[
   ("NIF (Finanças)", [
     "Presencial: marque atendimento pelo Centro de Atendimento Telefónico das Finanças, 217 206 707 (dias úteis, 9h–19h).",
     "Online, pelo e-balcão: só para quem mora fora da União Europeia, e através de um representante.",
     "Se você mora em Portugal: leve passaporte (ou documento do país de origem) e o título de residência. Com passaporte, leve também o visto de entrada.",
     "Se ainda não mora em Portugal: além do passaporte, precisa de um representante fiscal com morada em Portugal.",
     "Para crianças sem passaporte: certidão de nascimento.",
   ]),
   ("NISS (Segurança Social)", [
     "Pode pedir online, preenchendo o formulário no portal da Segurança Social e anexando os documentos.",
     "Para cidadãos de fora da UE: passaporte, visto de trabalho e autorização de residência (ou outro documento de identificação), mais um comprovativo de trabalho, como o contrato.",
     "Se for começar a trabalhar por conta de outrem, o empregador também pode pedir o NISS por você, com procuração ou o formulário PA-12.",
     "O NISS não sai na hora: chega uma carta registada à sua morada, e depois você levanta o número num balcão da Segurança Social (marcação pela SigaApp ou 210 548 888).",
   ]),
  ],
  dica="Quem já tem morada em Portugal pode pedir o NIF, o NISS e o número de utente do SNS de uma só vez.",
  custo="Gratuito", links=[("Guia oficial no gov.pt", "https://www.gov.pt/guias/como-pedir-o-nif-e-o-niss-para-pessoas-estrangeiras-em-portugal"), ("Portal das Finanças", "https://www.portaldasfinancas.gov.pt"), ("Segurança Social", "https://www.seg-social.pt")],
  fontes=[("gov.pt · Como pedir o NIF e o NISS para pessoas estrangeiras", "https://www.gov.pt/guias/como-pedir-o-nif-e-o-niss-para-pessoas-estrangeiras-em-portugal")], help="NIF / NISS"),

 dict(slug="numero-de-utente-sns", stage="chegada", tag="Saúde", title="Número de utente do SNS",
  card="Para ter médico de família e para o SNS cobrir as suas consultas.",
  intro="Qualquer estrangeiro com residência legal em Portugal pode ter número de utente. E, em qualquer situação, quem adoece tem direito a ser assistido num centro de saúde ou hospital.",
  secoes=[
   ("Como conseguir", [
     "O número é atribuído na primeira vez que você vai a uma unidade pública, como um centro de saúde ou hospital.",
     "Também pode pedir online, no serviço \"Pedir o número de utente do SNS\" do gov.pt.",
     "Depois, inscreva-se no centro de saúde da sua área de residência para ter médico de família.",
   ]),
   ("O que ligar ao número", [
     "Documento de identificação.",
     "NIF português.",
     "Morada completa em Portugal.",
     "Autorização de residência válida.",
   ]),
  ],
  dica="Ainda sem autorização de residência? O CDAM (antigo PB4) garante atendimento no SNS a brasileiros. Veja o guia do CDAM.",
  custo="Gratuito", links=[("Guia oficial no gov.pt", "https://www.gov.pt/guias/migrantes-cuidados-de-saude-em-portugal"), ("SNS 24", "https://www.sns24.gov.pt")],
  fontes=[("gov.pt · Migrantes: cuidados de saúde em Portugal", "https://www.gov.pt/guias/migrantes-cuidados-de-saude-em-portugal")], help="número de utente"),

 dict(slug="renovar-residencia-aima", stage="residencia", tag="Portugal", title="Renovar a autorização de residência",
  card="A renovação é pedida online, no portal de renovações da AIMA. Atenção ao prazo.",
  intro="Quem tem autorização de residência válida, ou caducada há menos de seis meses, pede a renovação online, no portal de renovações da AIMA.",
  secoes=[
   ("Quando pedir", [
     "Pode pedir a partir de 90 dias antes de a autorização caducar.",
     "Nas autorizações temporárias, o pedido deve ser feito até 30 dias antes do fim da validade.",
   ]),
   ("Como pedir", [
     "Entre no portal de renovações da AIMA e faça o pedido online. Um representante legal também pode pedir por você.",
     "Se o seu caso exigir atendimento presencial, o IRN entra em contacto para marcar. O agendamento é obrigatório.",
     "Não é possível pedir autorização de residência num balcão dos Registos.",
   ]),
   ("Se a autorização caducou há mais de seis meses", [
     "Nesse caso, ou se ainda não tem autorização de residência, o pedido é feito num balcão da AIMA.",
   ]),
  ],
  dica="Guarde o comprovativo do pedido de renovação: é ele que mostra que você está dentro do prazo.",
  custo="A taxa depende do tipo de autorização: confira no portal da AIMA", links=[("Portal de renovações AIMA", "https://portal-renovacoes.aima.gov.pt/ords/r/aima/aima-pr/pr-home"), ("Site da AIMA", "https://aima.gov.pt/pt")],
  fontes=[("gov.pt · Renovar a autorização de residência", "https://www.gov.pt/servicos/renovar-a-autorizacao-de-residencia")], help="renovação da residência"),

 dict(slug="passaporte-brasileiro-em-portugal", stage="brasil", tag="Brasil · consulado", title="Passaporte brasileiro em Portugal",
  card="Quem mora em Portugal pede no consulado, pelo e-Consular. A taxa é paga ao consulado.",
  intro="Em Portugal, o passaporte brasileiro é pedido no consulado da sua área, com o pedido e o agendamento feitos pelo sistema e-Consular. O site da Polícia Federal é para quem está no Brasil.",
  secoes=[
   ("1. Descubra o seu consulado", [
     "Lisboa: maior parte do centro e do sul, Açores e Madeira.",
     "Porto: norte e parte do centro.",
     "Faro: distritos de Faro, Beja, Évora e alguns municípios de Setúbal.",
   ]),
   ("2. Separe os documentos (adultos)", [
     "Formulário de passaporte preenchido no site do Itamaraty.",
     "Uma foto 3x4 recente, com fundo branco.",
     "Passaporte anterior, mesmo vencido.",
     "Certidão de nascimento, ou de casamento com averbações se for casado, divorciado ou viúvo.",
     "Documento brasileiro com foto.",
     "Título de eleitor com comprovante de voto ou quitação eleitoral (18 a 70 anos).",
     "Certificado de reservista (homens de 18 a 45 anos).",
   ]),
   ("3. Peça no e-Consular", [
     "Escolha \"Novo serviço\", indique o tipo de passaporte e anexe os documentos digitalizados.",
     "O consulado analisa por ordem de chegada. Se faltar algo, você recebe um e-mail para corrigir.",
     "Depois de validado, marque o atendimento no próprio e-Consular.",
   ]),
   ("Menores de idade", [
     "Os documentos são outros. No Porto e em Faro a criança tem de ir ao consulado. Em Lisboa, basta a presença dos responsáveis.",
   ]),
  ],
  dica="Renove pelo menos seis meses antes do vencimento: muitos países exigem passaporte com seis meses de validade, até para turismo.",
  custo="€132 adultos · €88 dos 4 aos 17 anos · €44 até 3 anos (valores de 2024: confirme no consulado)", links=[("e-Consular Lisboa", "https://ec-lisboa.itamaraty.gov.br/"), ("e-Consular Porto", "https://ec-porto.itamaraty.gov.br/"), ("e-Consular Faro", "https://ec-faro.itamaraty.gov.br/")],
  fontes=[("DN Brasil · Como renovar o passaporte brasileiro em Portugal (ago/2024)", "https://dnbrasil.dn.pt/guia-do-imigrante-veja-como-renovar-o-passaporte-brasileiro-em-portugal")], help="passaporte"),

 dict(slug="segunda-via-de-certidao", stage="brasil", tag="Brasil", title="2ª via de certidão brasileira",
  card="Nascimento, casamento ou óbito, pedida online ao cartório onde foi registrada.",
  intro="A 2ª via de certidão de nascimento, casamento ou óbito é pedida online, no portal do Registro Civil, ao cartório onde o registo foi feito.",
  secoes=[
   ("Como pedir", [
     "Entre no portal do Registro Civil e escolha \"2ª via de certidão\".",
     "Escolha o tipo (nascimento, casamento ou óbito), o estado, a cidade e o cartório.",
     "Não sabe o cartório? Use o serviço \"Buscar certidão\" do próprio portal.",
     "Escolha o formato: breve relato ou inteiro teor.",
   ]),
   ("Para usar em Portugal", [
     "Processos em Portugal costumam pedir a certidão em inteiro teor, recente e com Apostila de Haia. Confirme o que o seu processo exige antes de pedir.",
   ]),
  ],
  dica="Peça já em inteiro teor e com apostila: evita pedir de novo e pagar duas vezes.",
  custo="Taxa do cartório, paga no próprio portal", links=[("Portal do Registro Civil", "https://registrocivil.org.br"), ("Legalização de documentos (Itamaraty)", "http://www.portalconsular.itamaraty.gov.br/legalizacao-de-documentos/")],
  fontes=[("Registro Civil · Meu Registro", "https://registrocivil.org.br")], help="2ª via de certidão"),

 dict(slug="antecedentes-criminais", stage="brasil", tag="Brasil", title="Certidão de antecedentes criminais",
  card="Emitida online e de graça pela Polícia Federal. Vale 90 dias.",
  intro="A certidão de antecedentes criminais da Polícia Federal é emitida pela internet, gratuitamente, e é muito pedida nos processos de residência e de nacionalidade.",
  secoes=[
   ("Como emitir", [
     "Entre no serviço \"Emitir Certidão de Antecedentes Criminais\" do gov.br.",
     "Preencha os seus dados e emita a certidão.",
     "Ela vale por 90 dias: emita perto da data em que vai usar.",
   ]),
   ("Para usar em Portugal", [
     "Muitos processos pedem o documento legalizado com apostila. Veja as orientações de legalização do Itamaraty.",
   ]),
  ],
  dica="Confira se o seu processo aceita a versão digital ou se exige a apostila antes de emitir.",
  custo="Gratuito", links=[("Emitir certidão (gov.br)", "https://www.gov.br/pt-br/servicos/emitir-certidao-de-antecedentes-criminais"), ("Legalização de documentos (Itamaraty)", "http://www.portalconsular.itamaraty.gov.br/legalizacao-de-documentos/")],
  fontes=[("Polícia Federal · Antecedentes criminais", "https://www.gov.br/pf/pt-br/assuntos/antecedentes-criminais")], help="antecedentes criminais"),

 dict(slug="cdam-pb4", stage="brasil", tag="Saúde", title="CDAM, o antigo PB4",
  card="Garante atendimento no SNS a brasileiros. Pedido online e gratuito.",
  intro="O CDAM (Certificado de Direito à Assistência Médica), conhecido em Portugal como PB4, garante ao brasileiro acesso à rede pública de saúde em Portugal.",
  secoes=[
   ("Como pedir", [
     "O pedido é online, no portal de serviços do governo federal, e o certificado é emitido pelo Ministério da Saúde.",
     "Entre com o CPF, preencha os seus dados e os dos dependentes e envie os documentos.",
     "Quando for aprovado, você recebe um link por e-mail e baixa o CDAM em \"Minhas solicitações\".",
     "Imprima e faça o apostilamento.",
   ]),
   ("Quem pode pedir", [
     "Brasileiros natos ou naturalizados e os seus dependentes. Menores entram como dependentes do adulto que pede.",
   ]),
   ("Como usar em Portugal", [
     "Leve o CDAM e o passaporte ao centro de saúde da sua freguesia.",
     "Quando tiver autorização de residência, peça o número de utente e o médico de família.",
   ]),
  ],
  dica="O CDAM vale 365 dias (nunca além da validade do passaporte) e não se renova: depois é preciso fazer um pedido novo. Ele não substitui seguro de viagem.",
  custo="Gratuito", links=[("Serviços do gov.br", "https://www.gov.br/pt-br/servicos")],
  fontes=[("Euro Dicas · CDAM (atualizado em jun/2025)", "https://www.eurodicas.com.br/cdam/")], help="CDAM / PB4"),

 dict(slug="equivalencia-ensino-basico-secundario", stage="estudos", tag="Portugal", title="Equivalência do ensino básico e secundário",
  card="Pedida numa escola portuguesa. Gratuita. Serve para universidade e emprego.",
  intro="A equivalência do ensino fundamental e médio feito no Brasil é pedida numa escola portuguesa, pública ou privada, de preferência da sua área. A escola analisa e envia o parecer à Direção-Geral da Educação, que decide.",
  secoes=[
   ("Documentos", [
     "Documento de identificação (título de residência, cartão de cidadão ou passaporte).",
     "Histórico escolar, com firma reconhecida em cartório e Apostila de Haia.",
     "Diploma ou certificado de conclusão, com os mesmos cuidados.",
     "Declaração de escala de notas e nota mínima, emitida pela Embaixada do Brasil em Lisboa.",
     "Requerimento de equivalência preenchido e assinado.",
   ]),
   ("A declaração da Embaixada", [
     "É pedida por correio à Embaixada do Brasil em Lisboa, com cópias do histórico e do diploma e um envelope de retorno selado.",
   ]),
   ("Prazo e uso", [
     "Pode pedir em qualquer época do ano. A validação leva, em média, cerca de 30 dias.",
     "Serve para se candidatar a uma licenciatura e para vagas de emprego que peçam o ensino básico ou secundário.",
   ]),
  ],
  dica="O curso tem de estar concluído. Confirme com a escola os documentos antes de enviar, porque as regras da Embaixada podem mudar.",
  custo="Gratuito", links=[("Requerimento (DGE)", "https://www.dge.mec.pt/sites/default/files/Equivalencias/requerimento_modelo.pdf"), ("Direção-Geral da Educação", "https://www.dge.mec.pt")],
  fontes=[("Euro Dicas · Equivalência do ensino médio (atualizado em out/2024)", "https://www.eurodicas.com.br/?p=15944"), ("DGE · Requerimento modelo", "https://www.dge.mec.pt/sites/default/files/Equivalencias/requerimento_modelo.pdf")], help="equivalência escolar"),

 dict(slug="reconhecimento-de-diploma", stage="estudos", tag="Portugal", title="Reconhecimento de diploma universitário",
  card="Três tipos de reconhecimento, com prazos de 30 a 90 dias. Pedido online.",
  intro="Para usar a sua faculdade brasileira em Portugal, o grau precisa de ser reconhecido. O pedido é feito por um formulário digital único, disponível a qualquer hora.",
  secoes=[
   ("Os três tipos", [
     "Reconhecimento automático: o mais simples, só para graus que já têm deliberação. Prazo de 30 dias depois do processo completo.",
     "Reconhecimento de nível: equipara o seu grau a licenciado, mestre ou doutor. Prazo de 90 dias.",
     "Reconhecimento específico: além do nível, compara a área de formação (por exemplo, \"licenciado em Biologia\"). Prazo de 90 dias.",
   ]),
   ("Onde pedir", [
     "No formulário digital, dirigido ao organismo de ensino superior ou a uma universidade pública portuguesa.",
     "Para dúvidas, existe o centro ENIC/NARIC.",
   ]),
  ],
  dica="Profissões reguladas, como médicos, enfermeiros e engenheiros, também precisam de inscrição na respetiva ordem profissional.",
  custo="Taxa conforme o tipo de reconhecimento: confira no site oficial", links=[("Reconhecimento de graus (oficial)", "https://www.iesuperior.pt")],
  fontes=[("Brochura oficial de reconhecimento 2026", "https://wwwcdn.dges.gov.pt/sites/default/files/brochuras_reconhecimento_ies_2026.pdf")], help="reconhecimento de diploma"),

 dict(slug="carta-de-conducao-brasileira", stage="carro", tag="Portugal", title="Carta de condução brasileira",
  card="Desde 2022, a carta da CPLP pode valer em Portugal, se cumprir três condições.",
  intro="Desde agosto de 2022, com o Decreto-Lei n.º 46/2022, as cartas de países da CPLP, como o Brasil, ficaram dispensadas de troca, tal como as da União Europeia, desde que cumpram as condições abaixo.",
  secoes=[
   ("As condições (todas ao mesmo tempo)", [
     "O país que emitiu a carta assina uma das convenções internacionais de trânsito ou tem acordo com Portugal.",
     "Não passaram mais de 15 anos desde a emissão ou a última renovação da carta.",
     "O condutor tem menos de 60 anos.",
     "A carta não está apreendida, suspensa, caducada ou cassada.",
   ]),
   ("Se não cumprir as condições", [
     "Confirme no IMT qual é o seu caso, por exemplo para categorias profissionais ou carta antiga.",
   ]),
  ],
  dica="Ande sempre com a carta original e o documento de identificação.",
  custo="Sem custo, se estiver dispensado da troca", links=[("IMT", "https://www.imt-ip.pt")],
  fontes=[("Pplware · Cartas de condução estrangeiras passam a ser válidas em Portugal", "https://pplware.sapo.pt/motores/cartas-de-conducao-estrangeiras-passam-a-ser-validas-em-portugal/")], help="carta de condução"),

 dict(slug="nacionalidade-portuguesa", stage="nacionalidade", tag="Portugal", title="Nacionalidade portuguesa por residência",
  card="Nova lei em vigor desde 19 de maio de 2026: 7 anos de residência para brasileiros.",
  intro="A nova Lei da Nacionalidade (Lei Orgânica n.º 1/2026) entrou em vigor a 19 de maio de 2026. Para cidadãos de países de língua portuguesa, como o Brasil, o prazo de residência legal passou a 7 anos.",
  secoes=[
   ("O que mudou", [
     "7 anos de residência legal para cidadãos da CPLP e da UE, e 10 anos para outras nacionalidades.",
     "É preciso mostrar conhecimento da cultura, da história e dos símbolos portugueses, e dos direitos e deveres do cidadão.",
     "Há uma declaração solene de adesão aos princípios do Estado de direito democrático.",
     "Uma condenação a pena de prisão efetiva superior a 3 anos por certos crimes graves impede o pedido.",
     "É preciso ter meios para assegurar a própria subsistência.",
   ]),
   ("Quem já tinha pedido", [
     "Os processos que entraram antes de 19 de maio de 2026 continuam com as regras antigas.",
   ]),
   ("Onde se informar", [
     "Parte das regras depende da regulamentação do governo. Confirme os detalhes na secção de nacionalidade do justica.gov.pt ou na Linha Justiça, 800 910 220 (dias úteis, 9h–18h).",
   ]),
  ],
  dica="Peça à AIMA a certidão do seu tempo de residência para saber exatamente quando completa o prazo.",
  custo="Taxa do IRN: confira em justica.gov.pt", links=[("Justiça.gov.pt · Nacionalidade", "https://justica.gov.pt")],
  fontes=[("Justiça.gov.pt · Lei da Nacionalidade: novas regras a 19 de maio", "https://justica.gov.pt/Noticias/Lei-da-Nacionalidade-novas-regras-entram-em-vigor-a-19-de-maio")], help="nacionalidade portuguesa"),
]
