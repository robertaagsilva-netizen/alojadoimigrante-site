"""Vídeo 3D 'Checagem vídeo do Moro': three.js (Chromium headless) + textos em cairo, sincronizado com timeline.py"""
import sys, io, base64, math, subprocess
import cairo
from playwright.sync_api import sync_playwright
from engine import text, measure, rrect, p, eo, eio, eback, lerp, W, H, MONO
from timeline import S, M, END, CHUNKS, FPS
XB = ("Inter ExtraBold", False)
MONOB = ("JetBrains Mono ExtraBold", False)
YEL = (1.0, 0.831, 0.278); INK = (0.08, 0.08, 0.08); CRM = (1.0, 0.953, 0.839)
DARK = (0.17, 0.17, 0.16); GREY = (0.55, 0.55, 0.53)
TIM = dict(S=S, M=M, END=END)
NCH = len(S)
CHAP = ["VIRALIZOU", "O QUE É VERDADE", "ONDE EXAGERA", "A POLÍCIA FEDERAL", "O OUTRO LADO", "RESUMO"]
SRC = {
    0: "Checagem Loja do Imigrante · vídeo de @sf_moro · verificado em 19/10/2026",
    1: "Fontes: CNN Brasil (íntegra da entrevista) · Poder360 (votação da CPMI, 12/03/2026)",
    2: "Fontes: Lei 12.850/2013 (delação precisa de provas) · CNN Brasil",
    3: "Fontes: Gazeta do Povo · Agência Brasil · BPMoney",
    4: "Fontes: CNN Brasil · Poder360",
}
NOTE = {0: "ilustração", 1: "ilustração", 2: "ilustração", 3: "ilustração · mesma cor para todos", 4: "ilustração · mesma cor para todos"}
def win(t, i):
    """visibilidade do capítulo i (entra no início, sai antes do próximo)"""
    a = S[i]; b = S[i + 1] if i < NCH - 1 else END + 1
    return eo(p(t, a + 0.15, a + 0.55)) * (1 - eio(p(t, b - 0.35, b)))


def pop(t, t0, d=0.4):
    k = p(t, t0, t0 + d)
    return eo(k), (lerp(0.75, 1, eback(k, 2.0)) if k > 0 else 0.75)


class Zoom:
    def __init__(s, ctx, k, x, y): s.c, s.k, s.x, s.y = ctx, k, x, y
    def __enter__(s): s.c.save(); s.c.translate(s.x, s.y); s.c.scale(s.k, s.k); s.c.translate(-s.x, -s.y)
    def __exit__(s, *a): s.c.restore()


def pill(ctx, s, cx, cy, size, fg, bg, a, font=MONOB, pad=26, h=None, ls=2):
    if a <= 0:
        return
    w = measure(ctx, s, font, size, ls) + 2 * pad
    if w > 940:
        size *= 940 / w; w = 940
    h = h or size * 2.1
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, h / 2); ctx.set_source_rgba(*bg, a); ctx.fill()
    text(ctx, s, cx, cy + size * 0.36, font, size, fg, a, ls=ls)


def stack(ctx, t, i, items):
    """pílulas empilhadas no topo: [(texto, t0, amarela?)]"""
    a0 = win(t, i)
    y = 410
    for j, (s, t0, yel) in enumerate(items):
        a, k = pop(t, t0)
        a *= a0
        if a > 0:
            with Zoom(ctx, k, 540, y):
                if j == 0:
                    pill(ctx, s, 540, y, 30, INK, YEL, a)
                else:
                    pill(ctx, s, 540, y, 24, INK if yel else CRM, YEL if yel else DARK, a)
        y += 76 if j == 0 else 64


def tag(ctx, s, anc, t0, t, a0=1.0, yellow=False, dy=0):
    if anc is None or anc[2] > 1:
        return
    x, y = anc[0], anc[1] + dy
    a, k = pop(t, t0); a *= a0
    if a <= 0:
        return
    with Zoom(ctx, k, x, y):
        size = 30
        w = measure(ctx, s, XB, size, 0) + 36; h = 54
        rrect(ctx, x - w / 2, y - h - 14, w, h, 10); ctx.set_source_rgba(*(YEL if yellow else CRM), 0.96 * a); ctx.fill()
        ctx.move_to(x - 10, y - 14); ctx.line_to(x + 10, y - 14); ctx.line_to(x, y); ctx.close_path(); ctx.fill()
        text(ctx, s, x, y - 14 - h / 2 + 11, XB, size, INK, a)


def caption(ctx, t):
    import re
    for c in CHUNKS:
        if not (c["t0"] <= t < c["t1"]):
            continue
        a = eo(p(t, c["t0"], c["t0"] + 0.12))
        size = 60; f = XB; sp = measure(ctx, " ", f, size); lh = 74
        lines = [[w for w in c["words"] if w["line"] == l] for l in range(c["nlines"])]
        y0 = 1500 - (len(lines) - 1) * lh / 2
        bw = max(sum(measure(ctx, w["tok"], f, size) for w in l) + sp * (len(l) - 1) for l in lines) + 70
        rrect(ctx, 540 - bw / 2, y0 - 60, bw, len(lines) * lh + 32, 18); ctx.set_source_rgba(0, 0, 0, 0.45 * a); ctx.fill()
        for li, l in enumerate(lines):
            lw = sum(measure(ctx, w["tok"], f, size) for w in l) + sp * (len(l) - 1)
            x = 540 - lw / 2
            for w in l:
                on = eo(p(t, w["t0"] - 0.03, w["t0"] + 0.12))
                col = tuple(lerp(GREY[j], YEL[j], on) for j in range(3))
                text(ctx, w["tok"], x, y0 + li * lh, f, size, col, a, "l")
                x += measure(ctx, w["tok"], f, size) + sp




def val(ctx, s, anc, a, big=40, yel=False):
    x, y, z = anc
    if a > 0 and z < 1:
        text(ctx, s, x, y, XB, big, YEL if yel else CRM, a, ls=-1)


def overlay(ctx, t, A):
    a0 = eo(p(t, 0.0, 0.5))
    text(ctx, "LOJA DO IMIGRANTE · CHECAGEM", 70, 236, MONO, 22, CRM, 0.75 * a0, "l", ls=5)
    k = 0
    for i in range(NCH):
        if t >= S[i]:
            k = i
    ka = win(t, k)
    lb = "• " + CHAP[k]
    w = measure(ctx, lb, MONOB, 26, 3) + 92
    rrect(ctx, 64, 262, w, 58, 29); ctx.set_source_rgba(0.13, 0.13, 0.12, 0.92 * a0); ctx.fill()
    ctx.arc(96, 291, 13, 0, 2 * math.pi); ctx.set_source_rgba(*YEL, a0); ctx.fill()
    text(ctx, lb, 122, 300, MONOB, 26, CRM, a0 * ka, "l", ls=3)

    # 0
    w0 = win(t, 0)
    stack(ctx, t, 0, [("ESSE VÍDEO VIRALIZOU", 0.2, 1), ("SENADOR SERGIO MORO · +1 MI DE CURTIDAS", M["c0_curtidas"] - 0.6, 0),
                      ("“LULA MENTE”", M["c0_mente"] - 0.3, 0), ("“O GOVERNO LULA ACABOU”", M["c0_acabou"] - 0.3, 0),
                      ("FATO OU ACUSAÇÃO?", M["c0_acusacao"] - 0.5, 1)])
    a, kz = pop(t, M["c0_fatos"] - 0.2, 0.4)
    if a > 0:
        with Zoom(ctx, kz, 540, 1250):
            pill(ctx, "VAMOS AOS FATOS", 540, 1250, 40, INK, YEL, w0 * a, h=90)
    # 1
    w1 = win(t, 1)
    stack(ctx, t, 1, [("O QUE É VERDADE", S[1] + 0.3, 1), ("A ENTREVISTA À CNN EXISTE", M["c1_cnn"] - 0.4, 0),
                      ("ELA DISSE: “LULA MENTE” · “A CULPA É DO LULA”", M["c1_mente"] - 0.4, 0),
                      ("CPMI DO INSS REJEITOU A CONVOCAÇÃO: 16 x 12", M["c1_16"] - 0.5, 0), ("8 DOS 16 VOTOS CONTRA: PT", M["c1_pt"] - 0.5, 0),
                      ("ELA É INVESTIGADA PELA PF · DEFESA NEGA", M["c1_investigada"] - 0.4, 0)])
    for j, (s_, mk) in enumerate([("ENTREVISTA", "c1_cnn"), ("CPMI", "c1_16"), ("INVESTIGAÇÃO", "c1_investigada")]):
        tag(ctx, s_, A["c1"][j], M[mk] - 0.1, t, w1, True)
    # 2
    w2 = win(t, 2)
    stack(ctx, t, 2, [("ONDE O VÍDEO EXAGERA", S[2] + 0.3, 1), ("“LULA MENTE” = ACUSAÇÃO DELA, SEM PROVA", M["c2_mente"] - 0.3, 0),
                      ("A DELAÇÃO NÃO FOI ASSINADA", M["c2_delacao"] - 0.3, 0), ("SÓ A PALAVRA DO DELATOR NÃO CONDENA", M["c2_lei"] - 0.3, 0),
                      ("“SEGUINDO ORDENS DE QUEM?”: INSINUAÇÃO", M["c2_insinuacao"] - 1.2, 1)])
    tag(ctx, "ACUSAÇÃO", A["c2a"], M["c2_mente"] - 0.1, t, w2, False)
    tag(ctx, "PROVA?", A["c2b"], M["c2_prova"] - 0.1, t, w2, True)
    # 3
    w3 = win(t, 3)
    stack(ctx, t, 3, [("O DIRETOR DA PF", S[3] + 0.3, 0), ("BRIGA REAL: MENDONÇA (STF) x ANDREI (PF)", M["c3_mendonca"] - 0.3, 0),
                      ("MOTIVO: TROCA DE DELEGADOS NO CASO", M["c3_delegados"] - 0.4, 0), ("SEM CONCLUSÃO DE QUE PROTEGEU ALGUÉM", M["c3_conclusao"] - 0.3, 1),
                      ("ANDREI NEGA: “NÃO PROTEGE NEM PERSEGUE”", M["c3_nega"] - 0.3, 0)])
    # 4
    w4 = win(t, 4)
    stack(ctx, t, 4, [("O OUTRO LADO", S[4] + 0.3, 1)])
    tag(ctx, "DESCONHECE OS FATOS", A["c4a"], M["c4_desconhece"] - 0.2, t, w4, False)
    tag(ctx, "NEGA IRREGULARIDADE", A["c4b"], M["c4_nega"] - 0.3, t, w4, False)
    # 5
    a5 = win(t, 5)
    stack(ctx, t, 5, [("RESUMO", S[5] + 0.3, 1), ("MORO: SENADOR DE OPOSIÇÃO", M["c5_oposicao"] - 0.4, 0), ("VÍDEO NA SEMANA DO 2º TURNO", M["c5_turno"] - 0.8, 0)])
    tag(ctx, "FATOS REAIS", A["c5"][0], M["c5_reais"] - 0.1, t, a5, True)
    tag(ctx, "ACUSAÇÕES NÃO PROVADAS", A["c5"][1], M["c5_provadas"] - 0.3, t, a5, False)
    a, kz = pop(t, M["c5_comenta"] - 0.1)
    with Zoom(ctx, kz, 540, 1220):
        pill(ctx, "QUAL VÍDEO A GENTE CHECA?", 540, 1220, 32, INK, YEL, a * a5, h=82)
    pill(ctx, "PRECISA DE AJUDA COM O SEU PROCESSO? LINK NA BIO", 540, 1310, 20, CRM, DARK, 0.95 * a5 * eo(p(t, M["c5_ajuda"] - 0.3, M["c5_ajuda"] + 0.2)), h=52)
    text(ctx, "LOJA DO IMIGRANTE · CONTEÚDO APARTIDÁRIO", 540, 1372, MONOB, 20, CRM, 0.8 * a5 * eo(p(t, M["c5_bio"] + 0.2, M["c5_bio"] + 0.6)), ls=4)
    for i, s_ in NOTE.items():
        wi = win(t, i)
        if wi > 0:
            text(ctx, s_, 540, 1330, MONO, 16 if len(s_) > 70 else 18, CRM, 0.6 * wi)

    for i, s_ in SRC.items():
        wi = win(t, i)
        if wi > 0:
            text(ctx, s_, 540, 1368, MONO, 16 if len(s_) > 70 else 17, CRM, 0.65 * wi)
    caption(ctx, t)
    fa = max(1 - p(t, 0, 0.35), p(t, END - 0.6, END))
    if fa > 0:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, fa); ctx.fill()


def main(out, only=None, rng=None):
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.on("console", lambda m: print("console:", m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: print("pageerror:", e))
        pg.goto("http://localhost:8778/scene.html"); pg.wait_for_function("window.ready === true", timeout=60000)
        ff = None
        if not only:
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                   "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        NF = int(round(END * FPS))
        f0, f1 = rng or (0, NF)
        frames = only or [n / FPS for n in range(f0, min(f1, NF))]
        for n, t in enumerate(frames):
            r = pg.evaluate("([t, T]) => window.renderAt(t, T)", [t, TIM])
            surf = cairo.ImageSurface.create_from_png(io.BytesIO(base64.b64decode(r["img"].split(",")[1])))
            fsur = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(fsur)
            ctx.set_source_surface(surf, 0, 0); ctx.paint()
            overlay(ctx, t, r["anchors"])
            if only:
                fsur.write_to_png(f"st/f_{t:05.2f}.png")
            else:
                ff.stdin.write(bytes(fsur.get_data()))
                if n % 300 == 0:
                    print("frame", n, flush=True)
        if ff:
            ff.stdin.close(); ff.wait()
        b.close()


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        main(None, [float(x) for x in sys.argv[2:]])
    elif len(sys.argv) > 3:
        main(sys.argv[1], rng=(int(sys.argv[2]), int(sys.argv[3])))
    else:
        main(sys.argv[1])
