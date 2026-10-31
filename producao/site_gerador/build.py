"""Gera o site 'Fatos e Fontes' da Loja do Imigrante a partir dos docs do Painel.
Saída: site/out/checagens/  (index.html + <slug>.html + capas/)
Modo --preview: index.html sem <!doctype>/<head> (para o Artifact)."""
import json, re, os, sys, html, shutil
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from entries import E, CATS, CLAIM, URGENT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = "--preview" in sys.argv
OUT = os.path.join(ROOT, "site", "preview" if PREVIEW else "out", "checagens")
IG = "https://www.instagram.com/alojadoimigrante.pt/"
ICON = {"ok": "✓", "warn": "!", "bad": "✕", "info": "i"}
MESES = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800;900&family=JetBrains+Mono:wght@500;700&display=swap">'

CSS = """
/* Layout: arquivo de checagens — faixa de marca, filtros e grade de capas verticais; página de vídeo em duas colunas (capa | relato + fontes). */
:root{
  --bg:#0c0c0b; --panel:#161614; --line:#2b2a26; --ink:#f3efe4; --mute:#a29d90; --yel:#ffd447;
  --ok:#8ad49a; --warn:#ffb15c; --bad:#ff7d6e; --info:#cfcabd;
  --display:"Inter","Helvetica Neue",Arial,sans-serif; --body:"Inter","Helvetica Neue",Arial,sans-serif; --mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--body);-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top{border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:18px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font:700 13px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase}
.brand i{width:12px;height:12px;border-radius:50%;background:var(--yel);display:inline-block}
.ig{font:700 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;text-decoration:none;color:var(--yel)}
.ig:hover,.ig:focus-visible{text-decoration:underline}
.hero .wrap{padding-block:48px 28px;display:grid;gap:14px}
.eyebrow{font:700 12px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--yel)}
h1{font:900 clamp(38px,7vw,76px)/.98 var(--display);letter-spacing:-.035em;margin:0;text-wrap:balance}
h1 em{font-style:normal;color:var(--yel)}
.lede{max-width:60ch;color:var(--mute);margin:0;font-size:17px}
.tools{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding-block:4px 26px}
.chip{font:700 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:11px 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--yel);color:#141414;border-color:var(--yel)}
.chip:focus-visible,.search:focus-visible,a:focus-visible{outline:2px solid var(--yel);outline-offset:2px}
.search{flex:1 1 220px;min-width:0;max-width:360px;margin-left:auto;font:500 15px var(--body);color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:11px 16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px;padding-bottom:56px}
.card{display:grid;gap:10px;text-decoration:none;min-width:0}
.thumb{aspect-ratio:4/5;max-width:100%;border-radius:14px;overflow:hidden;background:var(--panel);border:1px solid var(--line);position:relative}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:50% 38%;display:block;transition:transform .35s ease}
.card:hover .thumb img{transform:scale(1.03)}
.meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font:700 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.v{display:inline-flex;align-items:center;gap:6px;padding:6px 9px;border-radius:6px;border:1px solid currentColor}
.v.ok{color:var(--ok)} .v.warn{color:var(--warn)} .v.bad{color:var(--bad)} .v.info{color:var(--info)}
.card h2{font:800 19px/1.2 var(--display);letter-spacing:-.01em;margin:0;text-wrap:balance}
.claim{margin:0;font:600 15px/1.4 var(--body);color:var(--ink)}
.claim span{display:block;font:700 10px/1.6 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.legend{font-size:14px;color:var(--mute);margin:0;max-width:70ch}
.legend b{color:var(--ink);font-weight:600}
.hotb{position:absolute;left:10px;top:10px;background:var(--bad);color:#141414;font:800 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:7px 9px;border-radius:6px}
.hotb.static{position:static;display:inline-block}
.card.hot .thumb{border-color:var(--bad);box-shadow:0 0 0 2px var(--bad)}
.chip[data-cat="urgente"]{color:var(--bad);border-color:var(--bad)}
.chip[data-cat="urgente"][aria-pressed="true"]{background:var(--bad);color:#141414}
.empty{color:var(--mute);padding-block:24px}
.foot{border-top:1px solid var(--line);color:var(--mute);font-size:14px}
.foot .wrap{padding-block:26px;display:grid;gap:6px}
/* página do vídeo */
.back{display:inline-block;margin-top:26px;font:700 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);text-decoration:none}
.back:hover{color:var(--ink)}
.art{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:44px;padding-block:24px 64px;align-items:start}
.art .thumb{aspect-ratio:9/16;position:sticky;top:calc(env(safe-area-inset-top,0px) + 20px)}
.art .thumb img{object-position:50% 50%}
.art h1{font-size:clamp(32px,5vw,54px)}
.text{min-width:0;display:grid;gap:22px}
.verdict{border:1px solid var(--line);background:var(--panel);border-radius:14px;padding:18px 20px;display:grid;gap:8px}
.verdict .v{justify-self:start;font:700 12px/1 var(--mono);letter-spacing:.12em}
.verdict p{margin:0;font-size:17px}
.body p{margin:0 0 14px;max-width:66ch}
.body ul{margin:0 0 14px;padding-left:20px;max-width:64ch}
.body li{margin-bottom:6px}
.sources{border-top:1px solid var(--line);padding-top:20px}
.sources h3,.cta h3{font:700 12px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--yel);margin:0 0 14px}
.sources ol{margin:0;padding-left:22px;display:grid;gap:10px}
.sources a{color:var(--ink);text-decoration-color:var(--yel);text-underline-offset:3px;overflow-wrap:anywhere}
.sources a:hover{color:var(--yel)}
.sources .host{display:block;font:500 12px/1.4 var(--mono);color:var(--mute);overflow-wrap:anywhere}
.note{font-size:14px;color:var(--mute);max-width:66ch;margin:0}
.cta{border:1px solid var(--yel);border-radius:14px;padding:18px 20px}
.cta p{margin:0 0 12px}
.btn{display:inline-block;background:var(--yel);color:#141414;font:800 15px/1 var(--display);padding:13px 18px;border-radius:999px;text-decoration:none}
@media (max-width:760px){.art{grid-template-columns:1fr;gap:22px}.art .thumb{position:static;max-width:300px}.hero .wrap{padding-block:32px 20px}}
@media (prefers-reduced-motion:reduce){.thumb img{transition:none}}
"""

def esc(s): return html.escape(s, quote=True)

def emoji_strip(s):
    return re.sub(r"^[\U0001F000-\U0001FFFF☀-➿←-⇿⬀-⯿️‍\s]+", "", s).strip()

def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

URL = re.compile(r"https?://\S+")

def parse(leg):
    lines = [l.rstrip() for l in leg.split("\n")]
    body, sources, notes = [], [], []
    in_src = False
    for l in lines:
        s = l.strip()
        if not s:
            body.append(""); continue
        if s.startswith("#"):
            continue
        plain = emoji_strip(s)
        low = plain.lower()
        if low.startswith("fontes:") or low.startswith("fonte:") or low == "fontes" or low.startswith("📚") or s.startswith("📚"):
            rest = plain.split(":", 1)[1].strip() if ":" in plain else ""
            if rest and not URL.search(rest):
                for part in re.split(r";\s*|\s·\s", rest):
                    part = part.strip(" .")
                    if part and not part.lower().startswith(("informação verificada", "verificação", "verificado")):
                        sources.append((part, None))
                    elif part:
                        notes.append(part)
            in_src = True; continue
        m = URL.search(s)
        if m:
            url = m.group(0).rstrip(").,")
            label = s[:m.start()].strip(" :—-") or url
            sources.append((emoji_strip(label), url)); continue
        if in_src:
            continue
        if s[0] in "💬📲👉➕💾" or low.startswith(("comenta", "manda", "segue", "siga", "salva", "compartilha")):
            continue
        if s.startswith("ℹ️") or low.startswith("conteúdo informativo") or low.startswith("informação geral"):
            notes.append(plain); continue
        body.append(s)
    return body, sources, notes

def render_body(body):
    out, ul = [], []
    def flush():
        nonlocal ul
        if ul:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>"); ul = []
    for s in body:
        if not s:
            flush(); continue
        if s[0] in "•→-" or re.match(r"^\d+\.\s", s):
            ul.append(re.sub(r"^(•|→|-)\s*", "", s)); continue
        flush()
        out.append(f"<p>{inline(s)}</p>")
    flush()
    return "\n".join(out)

def host(u):
    m = re.match(r"https?://(www\.)?([^/]+)", u); return m.group(2) if m else u

def date_label(d):
    try:
        dd, mm, yy = d.split("/"); return f"{int(dd)} {MESES[int(mm)]} {yy}"
    except Exception:
        return d

CF_BEACON = """<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "21872373fe264540a79be1f6ea406933"}'></script><!-- End Cloudflare Web Analytics -->"""

def page_shell(title, desc, inner, full=True, canonical=""):
    head = f'<title>{esc(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="description" content="{esc(desc)}">\n<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n{FONTS}\n<style>{CSS}</style>\n'
    if not full:
        return head + inner
    return f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n{head}</head>\n<body>\n{inner}\n{CF_BEACON}\n</body>\n</html>\n'

TOP = f'''<header class="top"><div class="wrap"><a class="brand" href="./"><i></i>Loja do Imigrante · Fatos e Fontes</a><a class="ig" href="{IG}" target="_blank" rel="noopener">@alojadoimigrante.pt ↗</a></div></header>'''
FOOT = f'''<footer class="foot"><div class="wrap"><span>Loja do Imigrante · conteúdo informativo e apartidário.</span><span>Cada vídeo traz as fontes usadas na pesquisa. Encontrou um erro? Mande uma mensagem no <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</span></div></footer>'''

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "capas"))
    items = []
    for slug, doc, cat, (vk, vl), capa in E:
        d = json.load(open(os.path.join(ROOT, "painel", "docs", doc + ".json")))
        title = re.sub(r"\s*\(3D[^)]*\)\s*$", "", d["titulo"]).replace("—", "·")
        leg = d.get("legenda") or ""
        if not leg.strip():
            leg = d.get("roteiro", "")
        body, sources, notes = parse(leg)
        if doc == "checagem_10mil_3d":
            sources = [("Tabela do Simples Nacional, Anexo II (2ª faixa, alíquota efetiva ~5,8%)", None), ("Lei 15.270/2025 (retenção de 10% sobre dividendos acima de R$ 50 mil/mês)", None),
                       ("Tesouro Nacional: carga tributária de 2025", None), ("Banco Central / Copom: taxa Selic", None)]
        lead = next((x for x in body if x), "")
        rest = body[body.index(lead) + 1:] if lead in body else body
        im = Image.open(os.path.join(ROOT, capa)).convert("RGB")
        im.thumbnail((720, 1280))
        im.save(os.path.join(OUT, "capas", slug + ".jpg"), quality=80, optimize=True)
        items.append(dict(claim=CLAIM.get(slug, ""), slug=slug, cat=cat, vk=vk, vl=vl, title=title, date=d.get("criado_em", ""), tema=d.get("tema", ""), lead=lead))
        src_html = "".join(
            f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(lbl)}</a><span class="host">{esc(host(u))}</span></li>' if u else f"<li>{esc(lbl)}</li>"
            for lbl, u in sources) or "<li>Fontes indicadas no vídeo.</li>"
        note_html = "".join(f'<p class="note">{esc(n)}</p>' for n in notes)
        desc = emoji_strip(lead)[:155]
        inner = f'''{TOP}
<main class="wrap">
<a class="back" href="./">← Todas as checagens</a>
<article class="art">
  <div class="thumb"><img src="capas/{slug}.jpg" alt="Capa do vídeo: {esc(title)}"></div>
  <div class="text">
    <div class="meta">{('<span class="hotb static">● Última hora · ' + URGENT[slug][8:10].lstrip("0") + " " + MESES[int(URGENT[slug][5:7])] + ", " + URGENT[slug][11:16].replace(":", "h") + '</span>') if slug in URGENT else ""}<span>{esc(date_label(d.get("criado_em","")))}</span><span>{esc(d.get("tema",""))}</span></div>
    <h1>{esc(title)}</h1>
    <div class="verdict">{('<p class="claim"><span>O que circulou nas redes</span>“' + esc(CLAIM[slug].strip("“”")) + '”</p><span class="v ' + vk + '">Nossa checagem: ' + ICON[vk] + ' ' + esc(vl) + '</span>') if slug in CLAIM else ('<span class="v ' + vk + '">' + ICON[vk] + ' ' + esc(vl) + '</span>')}<p>{inline(emoji_strip(lead))}</p></div>
    <div class="body">{render_body(rest)}</div>
    <section class="sources"><h3>Fontes ({len(sources)})</h3><ol>{src_html}</ol></section>
    {note_html}
    <div class="cta"><h3>Veja o vídeo</h3><p>Este conteúdo foi publicado em vídeo no Instagram da Loja do Imigrante.</p><a class="btn" href="{IG}" target="_blank" rel="noopener">Abrir @alojadoimigrante.pt</a></div>
  </div>
</article>
</main>
{FOOT}'''
        open(os.path.join(OUT, slug + ".html"), "w").write(page_shell(f"{title} · Loja do Imigrante", desc, inner, True))
    chips = "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="{str(k == "todos").lower()}">{esc(v)}</button>' for k, v in CATS)
    def urg_label(iso):
        d, h = iso[:10], iso[11:16]; y, m, dd = d.split("-"); return f"{int(dd)} {MESES[int(m)]}, {h.replace(':', 'h')}"
    cards = "\n".join(f'''<a class="card" href="{i["slug"]}.html" data-cat="{i["cat"]}" data-urgent="{URGENT.get(i["slug"], "")}" data-q="{esc((i["title"] + " " + i["tema"] + " " + i["lead"]).lower())}">
  <div class="thumb"><img src="capas/{i["slug"]}.jpg" alt="" loading="lazy">{('<span class="hotb" hidden>● Última hora · ' + urg_label(URGENT[i["slug"]]) + '</span>') if i["slug"] in URGENT else ""}</div>
  <div class="meta"><span class="v {i["vk"]}">{ICON[i["vk"]]} {esc(i["vl"])}</span><span>{esc(date_label(i["date"]))}</span></div>
  {('<p class="claim"><span>O que circulou</span>“' + esc(i["claim"].strip("“”")) + '”</p>') if i["claim"] else ""}
  <h2>{esc(i["title"])}</h2>
</a>''' for i in items)
    inner = f'''{TOP}
<section class="hero"><div class="wrap">
  <span class="eyebrow">{len(items)} vídeos checados · fontes abertas</span>
  <h1>Viu no vídeo?<br><em>Confira a fonte.</em></h1>
  <p class="legend"><b>Como ler o selo:</b> nas checagens, o selo julga a afirmação que circulou nas redes, não o nosso vídeo. ✕ Não é verdade · ! Falta contexto · ✓ Confirmado · i Explicado.</p>
  <p class="lede">Aqui ficam as fontes de cada vídeo da Loja do Imigrante, com links para os documentos, relatórios e reportagens que usamos. Notícias do Brasil e de Portugal para quem vive fora.</p>
</div></section>
<main class="wrap">
  <div class="tools" role="toolbar" aria-label="Filtrar vídeos">{chips}<input class="search" id="q" type="search" placeholder="Buscar: passaporte, AIMA, eleições…" aria-label="Buscar vídeos"></div>
  <div class="grid" id="grid">
{cards}
  </div>
  <p class="empty" id="empty" hidden>Nenhum vídeo com esse termo. Tente outra palavra.</p>
</main>
{FOOT}
<script>
(function(){{
  var now=Date.now(), grid=document.getElementById('grid');
  [].slice.call(document.querySelectorAll('.card')).forEach(function(c){{ var u=c.dataset.urgent; if(!u) return; var t=Date.parse(u); if(isNaN(t)||now-t>48*3600*1000) return;
    c.classList.add('hot'); var b=c.querySelector('.hotb'); if(b) b.hidden=false; grid.insertBefore(c, grid.firstChild); }});
  var hotN=document.querySelectorAll('.card.hot').length, hc=document.querySelector('.chip[data-cat="urgente"]'); if(hc&&!hotN) hc.hidden=true;
  var cat='todos', q=document.getElementById('q'), cards=[].slice.call(document.querySelectorAll('.card')), chips=[].slice.call(document.querySelectorAll('.chip')), empty=document.getElementById('empty');
  function apply(){{ var t=(q.value||'').toLowerCase().trim(), n=0;
    cards.forEach(function(c){{ var ok=(cat==='todos'||c.dataset.cat===cat||(cat==='urgente'&&c.classList.contains('hot')))&&(!t||c.dataset.q.indexOf(t)>-1); c.hidden=!ok; if(ok)n++; }});
    empty.hidden=n>0; }}
  chips.forEach(function(b){{ b.addEventListener('click',function(){{ cat=b.dataset.cat; chips.forEach(function(x){{x.setAttribute('aria-pressed',String(x===b));}}); apply(); }}); }});
  q.addEventListener('input',apply);
}})();
</script>'''
    open(os.path.join(OUT, "index.html"), "w").write(page_shell("Fatos e Fontes · Loja do Imigrante", "As fontes de cada vídeo da Loja do Imigrante, com links para os documentos e reportagens usados.", inner, not PREVIEW))

    # ---------- página principal (link da bio) ----------
    HUB_OUT = os.path.join(os.path.dirname(OUT))
    chk = "https://claude.ai/artifact/77wjfyvrkMEvXqrUhdiquC" if PREVIEW else "checagens/"
    wa = "https://wa.me/351935149920?text=" + "Ol%C3%A1%21%20Vim%20pelo%20Instagram%20e%20quero%20agendar%20uma%20consultoria."
    shutil.copy(os.path.join(ROOT, "site", "logo.png"), os.path.join(HUB_OUT, "logo.png"))
    latest = items[:3]
    def cpath(s): return ("checagens/" if not PREVIEW else "checagens/") + "capas/" + s + ".jpg"
    mini = "".join(f'<a class="mini" href="{chk + (i["slug"] + ".html" if not PREVIEW else "")}"><img src="{cpath(i["slug"])}" alt=""><span><b class="v {i["vk"]}">{ICON[i["vk"]]} {esc(i["vl"])}</b>{esc(i["title"])}</span></a>' for i in latest)
    HUBCSS = """
.hub{max-width:560px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 48px;display:grid;gap:22px}
.id{display:grid;justify-items:center;text-align:center;gap:12px}
.id img{width:112px;height:112px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px var(--yel)}
.id h1{font:900 30px/1.05 var(--display);letter-spacing:-.02em}
.id p{margin:0;color:var(--mute);max-width:42ch}
.badge{font:700 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--yel)}
.links{display:grid;gap:12px}
.lk{display:grid;grid-template-columns:44px minmax(0,1fr) auto;align-items:center;gap:14px;padding:14px 16px;border-radius:16px;border:1px solid var(--line);background:var(--panel);text-decoration:none;transition:border-color .2s,transform .2s}
.lk:hover{border-color:var(--yel);transform:translateY(-1px)}
.lk .ic{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:#22211d;font:800 18px/1 var(--display);color:var(--yel)}
.lk b{display:block;font:800 17px/1.25 var(--display)}
.lk small{display:block;color:var(--mute);font-size:13.5px;line-height:1.35}
.lk .go{font:700 18px/1 var(--mono);color:var(--mute)}
.lk.main{background:var(--yel);border-color:var(--yel);color:#141414}
.lk.main .ic{background:#141414}
.lk.main small,.lk.main .go{color:#3b3a33}
.sec{font:700 12px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--yel);margin:10px 0 0}
.minis{display:grid;gap:10px}
.mini{display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px;align-items:center;text-decoration:none;padding:8px;border-radius:12px;border:1px solid var(--line)}
.mini img{width:64px;height:80px;object-fit:cover;border-radius:8px}
.mini span{font:700 15px/1.3 var(--display);min-width:0}
.mini .v{display:flex;width:max-content;margin-bottom:6px;font:700 10px/1 var(--mono);letter-spacing:.1em;padding:5px 7px}
.num{font:500 13px/1.4 var(--mono);color:var(--mute);text-align:center;margin:0}
.num b{color:var(--ink);user-select:all}
"""
    hub_inner = f'''<main class="hub">
  <section class="id">
    <img src="logo.png" alt="Logo A Loja do Imigrante">
    <span class="badge">Mais de 21 anos de experiência</span>
    <h1>A Loja do Imigrante</h1>
    <p>Consultoria especializada para quem quer viver na Europa, e notícias checadas para quem já vive fora.</p>
  </section>
  <nav class="links" aria-label="Links principais">
    <a class="lk main" href="{wa if PREVIEW else 'whatsapp.html'}" target="_blank" rel="noopener"><span class="ic">✆</span><span><b>Agendar consultoria</b><small>Fale com a gente pelo WhatsApp</small></span><span class="go">↗</span></a>
    <a class="lk" href="do-sonho-a-europa/#kit"><span class="ic">↓</span><span><b>E-book grátis: Pasta do Imigrante</b><small>Checklist de documentos e prazos, em PDF</small></span><span class="go">→</span></a>
    <a class="lk" href="do-sonho-a-europa/"><span class="ic">★</span><span><b>Do Sonho à Europa</b><small>Guias grátis e consultoria</small></span><span class="go">↗</span></a>
    <a class="lk" href="{chk}"><span class="ic">✓</span><span><b>Fatos e Fontes dos vídeos</b><small>As fontes de cada vídeo, com links</small></span><span class="go">→</span></a>
    <a class="lk" href="https://ig.me/m/alojadoimigrante.pt" target="_blank" rel="noopener"><span class="ic">✉</span><span><b>Mandar Direct no Instagram</b><small>@alojadoimigrante.pt</small></span><span class="go">↗</span></a>
    <a class="lk" href="https://www.threads.net/@alojadoimigrante.pt" target="_blank" rel="noopener"><span class="ic">@</span><span><b>Threads</b><small>@alojadoimigrante.pt</small></span><span class="go">↗</span></a>
  </nav>
  <p class="num">WhatsApp: <b>+351 935 149 920</b></p>
  <h2 class="sec">Últimas checagens</h2>
  <div class="minis">{mini}</div>
</main>
{FOOT}'''
    if not PREVIEW:
        open(os.path.join(HUB_OUT, "whatsapp.html"), "w").write(f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Abrindo o WhatsApp…</title><meta name="robots" content="noindex">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#0f1a14;color:#e8f3ec;font:600 18px system-ui,sans-serif;text-align:center;padding:16px}}a{{color:#25d366}}</style>
</head><body><p>Abrindo o WhatsApp…<br><small>Se não abrir, <a href="{wa}">toque aqui</a>.</small></p>
{CF_BEACON}
<script>setTimeout(function(){{location.replace({json.dumps(wa)})}},900)</script>
</body></html>
''')
    open(os.path.join(HUB_OUT, "index.html"), "w").write(page_shell("A Loja do Imigrante", "Consultoria para viver na Europa e notícias checadas para quem vive fora. Agende pelo WhatsApp.", hub_inner.replace("<style>", "<style>"), not PREVIEW).replace("</style>", HUBCSS + "</style>", 1))
    print(len(items), "páginas em", OUT)

main()
