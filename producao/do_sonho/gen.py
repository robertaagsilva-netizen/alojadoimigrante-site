"""Gera o site Do Sonho à Europa em out/. Uso: python3 gen.py [--preview]"""
import os, sys, html, shutil, json
from guias import G, VERIF

PREVIEW = "--preview" in sys.argv
OUT = "out"
WA = "351935149920"
CF = """<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "21872373fe264540a79be1f6ea406933"}'></script>"""
STRIPE = "https://buy.stripe.com/6oU3cx0FscGH3Rh5xL0VO00"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap">'
STAGES = [("chegada", "Chegando em Portugal", "Etapa 1"), ("residencia", "Residência", "Etapa 2"), ("brasil", "Documentos do Brasil", "Etapa 3"),
          ("estudos", "Estudos e trabalho", "Etapa 4"), ("carro", "Carro", "Etapa 5"), ("nacionalidade", "Nacionalidade", "Etapa 6")]
EXTRA = {
 "residencia": [dict(tag="Portugal", title="Residência indeferida", card="Recebeu um indeferimento da AIMA? Entenda o motivo e os prazos antes de fazer qualquer coisa.", help="residência indeferida", only_help=True)],
 "brasil": [dict(tag="Brasil · consulado", title="CPF, título de eleitor e registos", card="Regularizar o CPF, votar no exterior e registar nascimento ou casamento feito em Portugal, no consulado.", help="CPF / título / registo consular", links=[("Portal Consular", "https://www.gov.br/mre/pt-br/assuntos/portal-consular")], soon=True)],
}
e = html.escape


def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text=" + quote(text)


def page(title, desc, body, depth=0, extra_head=""):
    up = "../" * depth
    robots = '<meta name="robots" content="noindex, nofollow">' if PREVIEW else ""
    banner = '<div style="background:#C65A0A;color:#fff;text-align:center;font:600 13px/1.4 system-ui,sans-serif;padding:8px 16px">PRÉVIA · versão de teste, ainda não é o site oficial</div>' if PREVIEW else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{robots}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:locale" content="pt_BR">
{FONTS}
<link rel="stylesheet" href="{up}site.css">
{extra_head}
{"" if PREVIEW else CF}
</head>
<body>
{banner}
{body}
{footer(up)}
<nav class="dock" aria-label="Atalhos"><div>
<a class="btn btn-green" href="{wa('Olá! Vim pelo site Do Sonho à Europa e preciso de ajuda.')}" target="_blank" rel="noopener">Falar no WhatsApp</a>
<a class="btn btn-yel" href="{up}index.html#consultoria">Agendar · €95</a>
</div></nav>
</body>
</html>
"""


def footer(up):
    return f"""<footer><div class="wrap">
<strong>Do Sonho à Europa · A Loja do Imigrante</strong>
<span>WhatsApp: +351 935 149 920 · E-mail: alojadoimigrante.pt@gmail.com · Instagram: @alojadoimigrante.pt</span>
<span><a href="{up}privacidade.html">Política de privacidade</a> · <a href="https://www.livroreclamacoes.pt" target="_blank" rel="noopener">Livro de Reclamações</a> · <a href="https://alojadoimigrante.com/checagens/" target="_blank" rel="noopener">Notícias checadas</a></span>
<span class="legal">© 2026 Do Sonho à Europa. Operado por Elos Consentidos Unipessoal Lda · NIPC 515646822. Não somos um órgão do governo: os pedidos são feitos nos sites oficiais e as taxas são pagas diretamente às entidades.</span>
</div></footer>"""


def card(g, guide_link=None):
    links = ""
    if guide_link:
        links += f'<a class="off" href="{guide_link}">Ler o guia</a>'
    elif g.get("links"):
        l = g["links"][0]; links += f'<a class="off" href="{e(l[1])}" target="_blank" rel="noopener">{e(l[0])}</a>'
    label = "Falar com a equipe" if g.get("only_help") else "Travou? A gente ajuda"
    links += f'<a class="help" href="{wa("Olá! Vim pelo site e preciso de ajuda com: " + g["help"] + ".")}" target="_blank" rel="noopener">{label}</a>'
    soon = '<span class="soon">Guia completo em breve</span>' if g.get("soon") else ""
    return f'<article class="guide"><span class="tag">{e(g["tag"])}</span><h4>{e(g["title"])}</h4><p>{e(g["card"])}</p><div class="row">{links}</div>{soon}</article>'


def home():
    stages = ""
    for key, name, n in STAGES:
        cards = "".join(card(g, f"guias/{g['slug']}.html") for g in G if g["stage"] == key)
        cards += "".join(card(x) for x in EXTRA.get(key, []))
        stages += f'<div class="stage" data-s="{key}"><h3>{e(name)} <small>{n}</small></h3><div class="grid">{cards}</div></div>'
    chips = '<button class="chip" aria-pressed="true" data-f="all" id="f-all">Ver tudo</button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-f="{k}" id="f-{k}">{lab}</button>' for k, lab in
        [("chegada", "Acabei de chegar"), ("residencia", "Residência / AIMA"), ("brasil", "Documentos do Brasil"), ("estudos", "Estudos e diploma"), ("carro", "Carta de condução"), ("nacionalidade", "Nacionalidade")])
    body = f"""<div class="news"><div class="wrap"><b>NOVO</b><span>Estamos de cara nova: guias atualizados, triagem rápida e kit grátis.</span></div></div>
<header class="hero"><div class="stamp">EXCLUSIVO<br>PARA<br>IMIGRANTES</div><div class="wrap">
<div class="brand"><i>LI</i><span>Do Sonho à Europa<small>por A Loja do Imigrante · mais de 21 anos de experiência</small></span></div>
<h1>Resolva a sua documentação <em>sem pagar intermediário.</em></h1>
<p>Os links oficiais de Brasil e Portugal, explicados em português e organizados por etapa. Se travar, a nossa equipe orienta você e ajuda com agendamentos e pagamentos.</p>
<div class="ctas"><a class="btn btn-yel" href="#guias">Ver os guias</a><a class="btn btn-ghost" href="#consultoria">Consultoria · €95</a></div>
<div class="facts"><span>Só links oficiais</span><span>Atendimento em português</span><span>Taxas pagas direto ao governo</span></div>
</div></header>
<main>
<section id="guias"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Triagem rápida</span><h2>O que você precisa resolver?</h2><p>Toque numa opção e veja só o que importa para você. Cada guia diz onde fazer, quanto custa e leva ao site oficial. Informações conferidas em {VERIF}.</p></div>
<div class="chips" role="group" aria-label="Filtrar guias">{chips}</div>
{stages}
</div></section>
<section class="kit" id="kit"><div class="wrap">
<div><span class="eyebrow" style="color:var(--yel)">Grátis</span><h2>Kit <em>Pasta do Imigrante</em></h2>
<p>O checklist dos documentos que todo brasileiro em Portugal precisa ter organizados, com onde tirar cada um, e o calendário de prazos do imigrante.</p>
<ul><li>Checklist por objetivo: chegada, residência, renovação</li><li>Como nomear e guardar os PDFs para não travar no atendimento</li><li>Calendário de prazos atualizado</li><li>Bónus: ebook "O Mapa Invisível da Coragem"</li></ul>
<span class="pdf">PDF · ENVIADO PARA O SEU E-MAIL</span></div>
<form id="lead" novalidate>
<label for="ln">Nome<input id="ln" name="nome" type="text" autocomplete="name" placeholder="Seu nome" required></label>
<label for="le">E-mail<input id="le" name="email" type="email" autocomplete="email" placeholder="voce@email.com" required></label>
<label for="lw">WhatsApp (opcional)<input id="lw" name="whatsapp" type="tel" autocomplete="tel" placeholder="+351 …"></label>
<label for="lp">Você mora em<select id="lp" name="pais"><option>Portugal</option><option>Brasil (vou mudar)</option><option>Espanha</option><option>Outro país da Europa</option></select></label>
<label class="consent" for="lc"><input id="lc" type="checkbox" required><span>Aceito receber o kit e avisos da Loja do Imigrante por e-mail. Posso cancelar quando quiser. Ver a <a href="privacidade.html">política de privacidade</a>.</span></label>
<button class="btn btn-green" type="submit">Quero o kit grátis</button>
<div class="ok" id="lok" hidden></div>
</form></div></section>
<section id="consultoria"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Dois caminhos</span><h2>Faça você mesmo, ou deixe com a gente.</h2></div>
<div class="offer">
<div class="box diy"><h3>Resolver sozinho</h3><div class="price">€0</div><ul><li>Guias e links oficiais acima</li><li>Kit Pasta do Imigrante grátis</li><li>As taxas oficiais você paga direto ao governo</li></ul><a class="btn btn-green" href="#guias">Ver os guias</a></div>
<div class="box pro"><h3>Consultoria personalizada</h3><div class="price">€95 <small>por consulta</small></div><ul><li>Diagnóstico do seu caso</li><li>Plano de ação com o caminho mais curto</li><li>Checklist feito para você</li><li>Ajuda com agendamentos e pagamento de guias e taxas</li></ul><a class="btn btn-green" href="{STRIPE}" target="_blank" rel="noopener">Agendar e pagar · €95</a></div>
</div>
<div class="steps"><div>Você paga a consulta pelo link seguro</div><div>A equipe chama você no WhatsApp para agendar</div><div>Recebe o plano e o checklist</div><div>Segue o plano, com a nossa ajuda nos agendamentos e pagamentos</div></div>
</div></section>
<section style="padding-top:0"><div class="wrap duo">
<div class="box"><span class="eyebrow">Comunidade</span><h3>Entre Elas Europa</h3><p style="margin:0">Uma rede de apoio para mulheres imigrantes: conteúdos ao longo da semana, lives e encontros presenciais.</p><a class="btn btn-green" style="justify-self:start" href="https://chat.whatsapp.com/GBNBUGSrE3L4ankyJoQA9J" target="_blank" rel="noopener">Entrar no grupo</a></div>
<div class="box"><span class="eyebrow">Notícias checadas</span><h3>Fatos e Fontes</h3><p style="margin:0">As notícias que mexem com o imigrante, com a fonte de cada informação.</p><a class="btn btn-green" style="justify-self:start" href="https://alojadoimigrante.com/checagens/" target="_blank" rel="noopener">Ver as checagens</a></div>
</div></section>
<section id="faq" style="padding-top:0"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Perguntas frequentes</span><h2>Antes de agendar</h2></div>
<details><summary>A Loja do Imigrante é um órgão oficial?</summary><p>Não. Somos uma consultoria privada. Os pedidos são feitos nos sites oficiais, e as taxas são pagas direto às entidades.</p></details>
<details><summary>Vocês fazem o processo por mim?</summary><p>Ajudamos com agendamentos e com o pagamento de guias e taxas, a partir dos dados e valores que você nos envia. Não preenchemos nem fazemos documentos no seu lugar, e não prestamos serviços jurídicos: não somos advogados. Se o seu caso precisar de um advogado, avisamos.</p></details>
<details><summary>Quanto custa?</summary><p>A consulta custa €95. Os guias e o kit deste site são gratuitos.</p></details>
<details><summary>Atendem quem está fora de Portugal?</summary><p>Sim, o atendimento é online, em português.</p></details>
<details><summary>Posso falar pelo WhatsApp?</summary><p>Pode: +351 935 149 920. A triagem começa por lá.</p></details>
</div></section>
</main>
<script>
(function(){{
  var chips=document.querySelectorAll(".chip"),stages=document.querySelectorAll(".stage");
  chips.forEach(function(c){{c.addEventListener("click",function(){{
    chips.forEach(function(x){{x.setAttribute("aria-pressed",x===c?"true":"false");}});
    var f=c.dataset.f; stages.forEach(function(s){{s.hidden=!(f==="all"||s.dataset.s===f);}});
  }});}});
  var PREVIEW_MSG={json.dumps("Prévia: no site publicado, o kit vai para o e-mail informado." if PREVIEW else "Obrigado! O kit grátis está a ser preparado e chega em breve ao seu e-mail. Enquanto isso, fale connosco pelo WhatsApp: +351 935 149 920.")};
  var form=document.getElementById("lead"),ok=document.getElementById("lok");
  form.addEventListener("submit",function(ev){{
    ev.preventDefault();
    var email=document.getElementById("le").value.trim(),nome=document.getElementById("ln").value.trim();
    ok.hidden=false;
    if(!nome||!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)){{ok.textContent="Preencha o seu nome e um e-mail válido.";return;}}
    if(!document.getElementById("lc").checked){{ok.textContent="Marque a caixa de consentimento para receber o kit.";return;}}
    ok.textContent=PREVIEW_MSG;
  }});
}})();
</script>"""
    return page("Do Sonho à Europa · A Loja do Imigrante", "Guias com os links oficiais para a documentação de brasileiros em Portugal: NIF, NISS, AIMA, passaporte, certidões, PB4, equivalência e nacionalidade.", body)


def guide(g):
    secs = ""
    for h, items in g["secoes"]:
        tagname = "ol" if h.startswith("Como") else "ul"
        secs += f"<section style='padding:0'><h2>{e(h)}</h2><{tagname}>" + "".join(f"<li>{e(i)}</li>" for i in items) + f"</{tagname}></section>"
    links = "".join(f'<a class="lk" href="{e(u)}" target="_blank" rel="noopener">{e(l)} ↗</a>' for l, u in g["links"])
    fontes = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in g["fontes"])
    stage = dict((k, n) for k, n, _ in STAGES)[g["stage"]]
    body = f"""<header class="hero ghero"><div class="wrap">
<span class="crumb"><a href="../index.html">Do Sonho à Europa</a> · {e(stage)}</span>
<h1>{e(g['title'])}</h1>
<div class="meta"><span>{e(g['tag'])}</span><span>Custo: {e(g['custo'])}</span><span>Conferido em {VERIF}</span></div>
</div></header>
<main><section><div class="wrap gbody">
<article>
<div class="lead"><p>{e(g['intro'])}</p></div>
{secs}
<div class="tip"><strong>Dica:</strong> {e(g['dica'])}</div>
<p class="src">Fontes: {fontes}. As regras mudam: confirme sempre no site oficial antes de pagar ou enviar documentos.</p>
</article>
<aside class="side">
<div class="box"><span class="eyebrow">Onde fazer</span>{links}</div>
<div class="box pro"><h3>Travou?</h3><p style="margin:0">A nossa equipe orienta você e ajuda com agendamentos e pagamentos. Consulta de €95, com plano e checklist do seu caso.</p>
<a class="btn btn-green" href="{STRIPE}" target="_blank" rel="noopener">Agendar e pagar · €95</a><a class="btn" style="box-shadow:inset 0 0 0 2px #0F2A22;color:#0F2A22" href="{wa('Olá! Li o guia ' + g['title'] + ' e tenho uma dúvida.')}" target="_blank" rel="noopener">Tirar dúvida no WhatsApp</a></div>
</aside>
</div></section></main>"""
    return page(f"{g['title']} · Do Sonho à Europa", g["card"], body, depth=1)


def privacidade():
    body = """<header class="hero ghero"><div class="wrap"><span class="crumb"><a href="index.html">Do Sonho à Europa</a></span><h1>Política de privacidade</h1></div></header>
<main><section><div class="wrap"><article style="display:grid;gap:18px;max-width:70ch">
<p><strong>Responsável pelo tratamento:</strong> Elos Consentidos Unipessoal Lda, NIPC 515646822, que opera o site Do Sonho à Europa e a marca A Loja do Imigrante.</p>
<p><strong>Que dados recolhemos:</strong> nome, e-mail, número de WhatsApp (opcional) e país de residência, quando você pede o kit grátis; e as mensagens que nos envia pelo WhatsApp.</p>
<p><strong>Para quê:</strong> enviar o kit pedido e, se você aceitou, avisos sobre prazos, mudanças nas regras e serviços da Loja do Imigrante.</p>
<p><strong>Base legal:</strong> o seu consentimento, que pode retirar a qualquer momento, pelo link de cancelamento em cada e-mail ou pelo WhatsApp.</p>
<p><strong>Quem mais tem acesso:</strong> o serviço de envio de e-mails que usamos para guardar a lista e enviar o kit, com servidores na União Europeia. Não vendemos nem cedemos os seus dados a terceiros.</p>
<p><strong>Por quanto tempo:</strong> enquanto mantiver a inscrição. Ao cancelar, os seus dados são apagados da lista.</p>
<p><strong>Os seus direitos:</strong> pode pedir acesso, correção ou apagamento dos seus dados, ou opor-se ao tratamento, pelo e-mail alojadoimigrante.pt@gmail.com ou pelo WhatsApp +351 935 149 920. Também pode apresentar queixa à Comissão Nacional de Proteção de Dados (CNPD).</p>
<p class="src">Última atualização: 20/10/2026.</p>
</article></div></section></main>"""
    return page("Política de privacidade · Do Sonho à Europa", "Como a Loja do Imigrante trata os seus dados.", body)


if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(f"{OUT}/guias")
shutil.copy("site.css", f"{OUT}/site.css")
os.makedirs(f"{OUT}/kit", exist_ok=True)
shutil.copy("Pasta_do_Imigrante_2026.pdf", f"{OUT}/kit/Pasta_do_Imigrante_2026.pdf")
open(f"{OUT}/index.html", "w").write(home())
open(f"{OUT}/privacidade.html", "w").write(privacidade())
for g in G:
    open(f"{OUT}/guias/{g['slug']}.html", "w").write(guide(g))
print("ok", len(G), "guias")
