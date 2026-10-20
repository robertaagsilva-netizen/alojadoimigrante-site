"""Gera o ebook 'Pasta do Imigrante 2026' (PDF A4) a partir dos guias conferidos."""
import json, html, datetime
from guias import G, VERIF
from playwright.sync_api import sync_playwright

e = html.escape
CAL = json.load(open("/home/claude/alojadoimigrante-site/stories/calendario.json"))
BY = {g["slug"]: g for g in G}
MES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:Figtree,Arial,sans-serif;color:#0F2A22;font-size:11pt;line-height:1.45}
h1,h2,h3{font-family:'Bricolage Grotesque',Arial,sans-serif;letter-spacing:-.02em;margin:0;line-height:1.08}
.pg{width:210mm;height:297mm;padding:18mm 17mm 16mm;position:relative;page-break-after:always;overflow:hidden;background:#FBF6E8}
.pg:last-child{page-break-after:auto}
.foot{position:absolute;left:17mm;right:17mm;bottom:9mm;display:flex;justify-content:space-between;font:9pt 'JetBrains Mono',monospace;color:#46625A}
.eyebrow{font:600 9pt 'JetBrains Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:#C65A0A}
h2{font-size:25pt;margin:6px 0 10px}
h3{font-size:14pt;margin:14px 0 6px}
p{margin:0 0 8px}
.lead{font-size:12.5pt;color:#46625A;max-width:150mm}
ul.ck{list-style:none;padding:0;margin:6px 0 10px;display:grid;gap:5px}
ul.ck li{padding-left:24px;position:relative}
ul.ck li::before{content:"";position:absolute;left:0;top:3px;width:13px;height:13px;border:1.6px solid #003D2E;border-radius:3px;background:#fff}
ul.dot{margin:6px 0 10px;padding-left:18px;display:grid;gap:4px}
.box{background:#FFF3D6;border-radius:10px;padding:12px 14px;margin:10px 0}
.box.org{border-left:4px solid #C65A0A}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.card{background:#fff;border:1px solid #E8DDBE;border-radius:10px;padding:12px 14px}
.card h3{margin-top:0}
.small{font-size:9.5pt;color:#46625A}
.src{font-size:8.5pt;color:#46625A;margin-top:6px}
table{width:100%;border-collapse:collapse;font-size:10.5pt}
td{padding:6px 8px;border-bottom:1px solid #E8DDBE;vertical-align:top}
td.d{font-family:'JetBrains Mono',monospace;white-space:nowrap;color:#C65A0A;font-weight:600}
code{font-family:'JetBrains Mono',monospace;font-size:9.5pt;background:#fff;padding:1px 5px;border-radius:4px;border:1px solid #E8DDBE}
.cover{background:#003D2E;color:#FFF3D6;padding:24mm 20mm}
.cover h1{font-size:46pt;color:#FFF3D6;max-width:150mm;margin-top:16mm}
.cover h1 em{font-style:normal;color:#FFD447}
.cover .sub{font-size:15pt;max-width:140mm;margin-top:10mm;opacity:.92}
.cover .tag{display:inline-block;background:#FFD447;color:#0F2A22;font:700 10pt 'JetBrains Mono',monospace;letter-spacing:.12em;padding:6px 12px;border-radius:5px}
.cover .bottom{position:absolute;left:20mm;right:20mm;bottom:20mm;display:flex;justify-content:space-between;align-items:flex-end;font-size:11pt}
.stamp{position:absolute;right:18mm;top:22mm;width:44mm;height:44mm;border-radius:50%;border:2px dashed rgba(255,212,71,.6);display:grid;place-items:center;text-align:center;font:600 9pt/1.6 'JetBrains Mono',monospace;letter-spacing:.14em;color:#FFD447;transform:rotate(-12deg)}
.toc{display:grid;gap:8px;margin-top:10px;font-size:12.5pt}
.toc div{display:flex;justify-content:space-between;border-bottom:1px dotted #C9BC97;padding-bottom:4px}
.end{background:#FFD447}
.price{font:800 40pt 'Bricolage Grotesque',Arial,sans-serif}
"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap">'

pages = []
n = [0]


def page(body, cls=""):
    n[0] += 1
    foot = "" if cls in ("cover",) else f'<div class="foot"><span>Pasta do Imigrante 2026 · A Loja do Imigrante</span><span>{n[0]}</span></div>'
    pages.append(f'<section class="pg {cls}">{body}{foot}</section>')


def items(slug, title):
    for h, its in BY[slug]["secoes"]:
        if h == title:
            return its
    raise KeyError((slug, title))


def ck(lst):
    return '<ul class="ck">' + "".join(f"<li>{e(x)}</li>" for x in lst) + "</ul>"


def dot(lst):
    return '<ul class="dot">' + "".join(f"<li>{e(x)}</li>" for x in lst) + "</ul>"


def src(*slugs):
    s = []
    for sl in slugs:
        for l, u in BY[sl]["fontes"]:
            s.append(f"{e(l)} ({e(u)})")
    return '<p class="src">Fontes: ' + " · ".join(s) + "</p>"


# 1 capa
page(f"""<div class="stamp">EXCLUSIVO<br>PARA<br>IMIGRANTES</div>
<span class="tag">GUIA GRÁTIS · EDIÇÃO 2026</span>
<h1>Pasta do <em>Imigrante</em></h1>
<p class="sub">O guia prático para organizar os seus documentos e resolver a burocracia entre Brasil e Portugal sem pagar intermediário.</p>
<div class="bottom"><span><b>A Loja do Imigrante</b><br>Do Sonho à Europa</span><span>Informações conferidas em {VERIF}</span></div>""", "cover")

# 2 sumário + como usar
page(f"""<span class="eyebrow">Antes de começar</span><h2>Como usar este guia</h2>
<p class="lead">Cada capítulo traz uma lista para você marcar o que já tem, os documentos pedidos e onde fazer. As informações foram conferidas nos sites oficiais em {VERIF}.</p>
<div class="box org"><b>Importante:</b> as regras mudam com frequência. Antes de pagar uma taxa ou enviar documentos, confirme sempre no site oficial indicado. Este guia é informativo e não substitui aconselhamento jurídico: a Loja do Imigrante é uma consultoria, não um escritório de advogados nem um órgão do governo.</div>
<h3>O que tem aqui</h3>
<div class="toc">
<div><span>1. A sua pasta digital</span><span>3</span></div>
<div><span>2. Chegando em Portugal: NIF, NISS e SNS</span><span>4</span></div>
<div><span>3. Residência na AIMA</span><span>5</span></div>
<div><span>4. Documentos do Brasil</span><span>6</span></div>
<div><span>5. Saúde: CDAM, o antigo PB4</span><span>8</span></div>
<div><span>6. Estudos e diploma</span><span>9</span></div>
<div><span>7. Carta de condução e nacionalidade</span><span>10</span></div>
<div><span>8. Os erros que mais travam processos</span><span>11</span></div>
<div><span>9. Calendário de prazos</span><span>12</span></div>
<div><span>10. Contactos úteis</span><span>13</span></div>
</div>""")

# 3 pasta digital
page("""<span class="eyebrow">Capítulo 1</span><h2>A sua pasta digital</h2>
<p class="lead">Metade das dores de cabeça vem de não encontrar o documento certo na hora certa. Monte esta pasta uma vez e mantenha-a atualizada.</p>
<div class="grid2">
<div class="card"><h3>As 7 subpastas</h3>
<ul class="dot"><li><code>01 Identidade</code> passaporte, título de residência, cartão de cidadão</li><li><code>02 Brasil</code> certidões, CPF, título de eleitor, reservista</li><li><code>03 Residência</code> pedidos e comprovativos da AIMA</li><li><code>04 Trabalho e Finanças</code> NIF, NISS, contratos, recibos</li><li><code>05 Saúde</code> CDAM, número de utente</li><li><code>06 Casa</code> contrato de arrendamento, atestado de residência</li><li><code>07 Estudos</code> diplomas, históricos, equivalências</li></ul></div>
<div class="card"><h3>Como dar nome aos arquivos</h3>
<p>Use sempre o mesmo padrão: data, tipo de documento e nome.</p>
<p><code>2026-10-20_passaporte_maria-silva.pdf</code></p>
<p><code>2026-09-02_certidao-nascimento-inteiro-teor_maria-silva.pdf</code></p>
<p class="small">Assim os arquivos ficam em ordem de data e você acha tudo pela pesquisa do celular.</p></div>
</div>
<h3>Regras de ouro</h3>
<ul class="ck"><li>Digitalize em PDF, a cores, com o documento inteiro e legível (frente e verso no mesmo arquivo).</li><li>Guarde uma cópia na nuvem e outra num pen drive ou no computador.</li><li>Guarde todos os comprovativos de pedidos e pagamentos: são eles que provam que você está dentro do prazo.</li><li>Anote a validade de cada documento. Antecedentes criminais, por exemplo, valem só 90 dias.</li><li>Documentos brasileiros para usar em Portugal costumam precisar de Apostila de Haia.</li></ul>""")

# 4 chegada
g = BY["nif-e-niss"]
page(f"""<span class="eyebrow">Capítulo 2</span><h2>Chegando em Portugal</h2>
<p class="lead">{e(g['intro'])}</p>
<div class="grid2">
<div class="card"><h3>NIF (Finanças)</h3>{dot(items('nif-e-niss','NIF (Finanças)'))}</div>
<div class="card"><h3>NISS (Segurança Social)</h3>{dot(items('nif-e-niss','NISS (Segurança Social)'))}</div>
</div>
<div class="card" style="margin-top:12px"><h3>Número de utente do SNS</h3>{dot(items('numero-de-utente-sns','Como conseguir'))}<p class="small">Para o SNS cobrir as despesas, ligue ao número: documento de identificação, NIF, morada em Portugal e autorização de residência válida.</p></div>
<div class="box"><b>Dica:</b> {e(g['dica'])} Os três pedidos são gratuitos.</div>
{src('nif-e-niss','numero-de-utente-sns')}""")

# 5 residência
g = BY["renovar-residencia-aima"]
page(f"""<span class="eyebrow">Capítulo 3</span><h2>Residência na AIMA</h2>
<p class="lead">{e(g['intro'])}</p>
<h3>Quando pedir a renovação</h3>{ck(items('renovar-residencia-aima','Quando pedir'))}
<h3>Como pedir</h3>{ck(items('renovar-residencia-aima','Como pedir'))}
<h3>Se a autorização caducou há mais de seis meses</h3>{dot(items('renovar-residencia-aima','Se a autorização caducou há mais de seis meses'))}
<div class="box"><b>Dica:</b> {e(g['dica'])}</div>
<div class="box org"><b>Recebeu um indeferimento?</b> Não deixe correr o prazo indicado na carta da AIMA. Leia com atenção o motivo e procure orientação antes de responder.</div>
<p class="small">Portal de renovações: portal-renovacoes.aima.gov.pt · Site da AIMA: aima.gov.pt</p>
{src('renovar-residencia-aima')}""")

# 6 Brasil: passaporte
g = BY["passaporte-brasileiro-em-portugal"]
page(f"""<span class="eyebrow">Capítulo 4</span><h2>Documentos do Brasil</h2>
<h3>Passaporte brasileiro</h3><p>{e(g['intro'])}</p>
<div class="grid2">
<div class="card"><h3>O seu consulado</h3>{dot(items('passaporte-brasileiro-em-portugal','1. Descubra o seu consulado'))}<p class="small">e-Consular: ec-lisboa.itamaraty.gov.br · ec-porto.itamaraty.gov.br · ec-faro.itamaraty.gov.br</p></div>
<div class="card"><h3>Documentos (adultos)</h3>{ck(items('passaporte-brasileiro-em-portugal','2. Separe os documentos (adultos)'))}</div>
</div>
<h3>No e-Consular</h3>{dot(items('passaporte-brasileiro-em-portugal','3. Peça no e-Consular'))}
<div class="box"><b>Taxas:</b> {e(g['custo'])}.<br><b>Dica:</b> {e(g['dica'])}</div>
{src('passaporte-brasileiro-em-portugal')}""")

# 7 Brasil: certidão, antecedentes
page(f"""<span class="eyebrow">Capítulo 4 · continuação</span><h2>Certidões do Brasil</h2>
<div class="card"><h3>2ª via de certidão (nascimento, casamento, óbito)</h3>{dot(items('segunda-via-de-certidao','Como pedir'))}<p>{e(items('segunda-via-de-certidao','Para usar em Portugal')[0])}</p><p class="small">Onde: registrocivil.org.br · Custo: taxa do cartório.</p></div>
<div class="card" style="margin-top:12px"><h3>Certidão de antecedentes criminais</h3>{dot(items('antecedentes-criminais','Como emitir'))}<p>{e(items('antecedentes-criminais','Para usar em Portugal')[0])}</p><p class="small">Onde: gov.br, serviço "Emitir Certidão de Antecedentes Criminais" · Gratuita.</p></div>
<div class="box"><b>Dica:</b> {e(BY['segunda-via-de-certidao']['dica'])}</div>
{src('segunda-via-de-certidao','antecedentes-criminais')}""")

# 8 saúde
g = BY["cdam-pb4"]
page(f"""<span class="eyebrow">Capítulo 5</span><h2>Saúde: CDAM, o antigo PB4</h2>
<p class="lead">{e(g['intro'])}</p>
<h3>Como pedir</h3>{ck(items('cdam-pb4','Como pedir'))}
<h3>Quem pode pedir</h3>{dot(items('cdam-pb4','Quem pode pedir'))}
<h3>Como usar em Portugal</h3>{dot(items('cdam-pb4','Como usar em Portugal'))}
<div class="box org"><b>Atenção:</b> {e(g['dica'])}</div>
{src('cdam-pb4')}""")

# 9 estudos
page(f"""<span class="eyebrow">Capítulo 6</span><h2>Estudos e diploma</h2>
<div class="card"><h3>Equivalência do ensino fundamental e médio</h3><p>{e(BY['equivalencia-ensino-basico-secundario']['intro'])}</p>{ck(items('equivalencia-ensino-basico-secundario','Documentos'))}<p class="small">{e(items('equivalencia-ensino-basico-secundario','A declaração da Embaixada')[0])} Gratuita. Validação em cerca de 30 dias.</p></div>
<div class="card" style="margin-top:12px"><h3>Reconhecimento de diploma universitário</h3>{dot(items('reconhecimento-de-diploma','Os três tipos'))}<p class="small">{e(BY['reconhecimento-de-diploma']['dica'])}</p></div>
{src('equivalencia-ensino-basico-secundario','reconhecimento-de-diploma')}""")

# 10 carta + nacionalidade
page(f"""<span class="eyebrow">Capítulo 7</span><h2>Carta de condução e nacionalidade</h2>
<div class="card"><h3>Conduzir com a carta brasileira</h3><p>{e(BY['carta-de-conducao-brasileira']['intro'])}</p>{ck(items('carta-de-conducao-brasileira','As condições (todas ao mesmo tempo)'))}<p class="small">Fora destas condições, confirme o seu caso no IMT (imt-ip.pt).</p></div>
<div class="card" style="margin-top:12px"><h3>Nacionalidade portuguesa por residência</h3><p>{e(BY['nacionalidade-portuguesa']['intro'])}</p>{dot(items('nacionalidade-portuguesa','O que mudou'))}<p class="small">{e(items('nacionalidade-portuguesa','Quem já tinha pedido')[0])} Linha Justiça: 800 910 220.</p></div>
{src('carta-de-conducao-brasileira','nacionalidade-portuguesa')}""")

# 11 erros comuns
page("""<span class="eyebrow">Capítulo 8</span><h2>Os erros que mais travam processos</h2>
<ul class="ck">
<li><b>Pedir a renovação da residência em cima da hora.</b> Nas autorizações temporárias, o pedido deve ser feito até 30 dias antes do fim da validade, e já pode ser feito a partir de 90 dias antes.</li>
<li><b>Usar o site da Polícia Federal para o passaporte.</b> Quem mora em Portugal pede no consulado, pelo e-Consular.</li>
<li><b>Certidão "breve relato" quando o processo pede inteiro teor.</b> Confirme antes de pedir, e peça já apostilada.</li>
<li><b>Antecedentes criminais vencidos.</b> A certidão vale 90 dias: emita perto da data em que vai usar.</li>
<li><b>Passaporte quase vencido.</b> Muitos países pedem seis meses de validade. Renove com antecedência.</li>
<li><b>Perder o comprovativo do pedido.</b> Guarde em PDF na pasta 03 Residência.</li>
<li><b>Contar o tempo para a nacionalidade a partir da chegada.</b> Conta a residência legal. Peça à AIMA a certidão do seu tempo de residência.</li>
<li><b>Pagar a intermediários por serviços gratuitos.</b> NIF, NISS, número de utente, CDAM, antecedentes e equivalência escolar são gratuitos nos canais oficiais.</li>
</ul>
<div class="box">Travou em algum destes pontos? A equipe da Loja do Imigrante orienta você e ajuda com agendamentos e pagamentos.</div>""")

# 12 calendário
rows = ""
for ev in CAL["eventos"]:
    if ev["tipo"] != "prazo":
        continue
    d = datetime.date.fromisoformat(ev["data"])
    rows += f'<tr><td class="d">{d.day:02d} {MES[d.month-1]} {d.year}</td><td>{e(ev["hoje"])}{" <span class=small>(confirmar data na agenda oficial)</span>" if ev.get("confirmar") else ""}</td></tr>'
rows += '<tr><td class="d">todo dia 20</td><td>Recibos verdes: as contribuições à Segurança Social pagam-se do dia 10 ao dia 20 de cada mês.</td></tr>'
page(f"""<span class="eyebrow">Capítulo 9</span><h2>Calendário de prazos</h2>
<p class="lead">Os prazos fiscais e da Segurança Social que mais afetam quem vive e trabalha em Portugal, de outubro de 2026 a março de 2027.</p>
<table>{rows}</table>
<div class="box">Todos os dias às 6h, nos stories do @alojadoimigrante.pt, avisamos o prazo da semana.</div>
<p class="src">Fontes: {e(" · ".join(CAL["fontes"]))}</p>""")

# 13 contactos
page("""<span class="eyebrow">Capítulo 10</span><h2>Contactos úteis</h2>
<table>
<tr><td><b>Finanças</b> (NIF, IRS)</td><td>Centro de Atendimento Telefónico: 217 206 707 · portaldasfinancas.gov.pt</td></tr>
<tr><td><b>Segurança Social</b> (NISS)</td><td>210 548 888 ou 300 088 888 · seg-social.pt · app SigaApp para marcações</td></tr>
<tr><td><b>AIMA</b> (residência)</td><td>aima.gov.pt · portal de renovações: portal-renovacoes.aima.gov.pt</td></tr>
<tr><td><b>SNS</b> (saúde)</td><td>SNS 24: sns24.gov.pt</td></tr>
<tr><td><b>Justiça</b> (nacionalidade)</td><td>Linha Justiça: 800 910 220 · justica.gov.pt</td></tr>
<tr><td><b>IMT</b> (carta de condução)</td><td>imt-ip.pt</td></tr>
<tr><td><b>Consulados do Brasil</b></td><td>e-Consular Lisboa, Porto e Faro: ec-lisboa / ec-porto / ec-faro .itamaraty.gov.br</td></tr>
<tr><td><b>Certidões do Brasil</b></td><td>registrocivil.org.br</td></tr>
<tr><td><b>Antecedentes criminais</b></td><td>gov.br, serviço "Emitir Certidão de Antecedentes Criminais"</td></tr>
<tr><td><b>Livro de Reclamações</b></td><td>livroreclamacoes.pt</td></tr>
</table>
<p class="small" style="margin-top:10px">Horários e números podem mudar: confirme no site de cada entidade.</p>""")

# 14 final
page("""<span class="eyebrow" style="color:#0F2A22">Travou?</span><h2>A gente ajuda.</h2>
<p class="lead" style="color:#0F2A22">Na consultoria personalizada da Loja do Imigrante, você recebe o diagnóstico do seu caso, um plano de ação com o caminho mais curto e um checklist feito para você. Também ajudamos com agendamentos e com o pagamento de guias e taxas.</p>
<div class="price">€95 <span style="font-size:14pt">por consulta</span></div>
<div class="box" style="background:#fff"><b>Agendar e pagar:</b> alojadoimigrante.com/do-sonho-a-europa<br><b>WhatsApp:</b> +351 935 149 920<br><b>E-mail:</b> alojadoimigrante.pt@gmail.com<br><b>Instagram:</b> @alojadoimigrante.pt</div>
<p class="small" style="color:#0F2A22">A Loja do Imigrante é uma consultoria privada operada por Elos Consentidos Unipessoal Lda (NIPC 515646822). Não somos órgão do governo e não prestamos serviços jurídicos. Os pedidos são feitos nos sites oficiais e as taxas são pagas diretamente às entidades.</p>
<p class="small" style="color:#0F2A22">Compartilhe este guia com quem está chegando: alojadoimigrante.com/do-sonho-a-europa</p>""", "end")

doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
open("ebook.html", "w").write(doc)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + __import__("os").path.abspath("ebook.html")); pg.wait_for_timeout(1500)
    pg.pdf(path="Pasta_do_Imigrante_2026.pdf", format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
print("pages", n[0])
