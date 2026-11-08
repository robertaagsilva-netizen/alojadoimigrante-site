"""Linha do tempo do Reels "Existe recibo verde na Espanha? (autónomo)".
Enquanto não há narração: frases com tempos ESTIMADOS (ritmo ~5,8 sílabas/s).
Com a voz real: preencher MEASURED (início/fim de cada frase no áudio), SEG_SRC e GAPS."""
import re

FPS = 30

from phrases import PHRASES, OVERRIDE
NSEG = 6
RATE, PH_GAP = 5.8, 0.32
MEASURED_V = [(0.05, 6.61),(6.84, 8.56),(8.98, 10.41),(10.68, 11.28),(11.69, 17.22),(17.62, 18.69),(19.04, 23.94),(24.29, 30.44),(30.79, 40.83),(41.20, 47.59),(48.02, 51.94),(52.26, 53.50),(53.80, 58.40),(58.72, 65.40),(65.63, 69.99),(70.34, 76.70),(77.04, 79.59),(79.94, 83.54),(83.94, 87.14),(87.45, 88.28),(88.60, 90.18),(90.45, 94.19),(94.40, 95.54)]
SEG_SRC = None
GAPS = [0.3] + [0.55] * 5
HOLD_END = 3.0


def syll(tok):
    if tok in OVERRIDE:
        return OVERRIDE[tok]
    w = re.sub(r"[^\wÀ-ÿ]", "", tok).lower()
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w)))


def _expand():
    out, k = [], 0
    for r in _RAW:
        if r[0] == "split":
            _, a, b, n = r
            sy = [sum(syll(x) for x in PHRASES[k + i][1].split(" ")) for i in range(n)]
            t = a
            for v in sy:
                d = (b - a) * v / sum(sy); out.append((t, t + d)); t += d
            k += n
        else:
            out.append(r); k += 1
    assert len(out) == len(PHRASES)
    return out


MEASURED = MEASURED_V


def _estimate():
    """tempos estimados num 'áudio virtual' contínuo"""
    out, t, cur = [], 0.0, -1
    for seg, txt in PHRASES:
        if seg != cur and cur >= 0:
            t += 0.5
        cur = seg
        d = sum(syll(x) for x in txt.split(" ")) / RATE
        out.append((t, t + d)); t += d + PH_GAP
    return out


_M = MEASURED or _estimate()
if SEG_SRC is None:
    SEG_SRC = []
    for s in range(NSEG):
        iv = [m for (sg, _), m in zip(PHRASES, _M) if sg == s]
        SEG_SRC.append((max(0.0, iv[0][0] - 0.05), iv[-1][1] + 0.12))
PLACE = []
_t = 0
for _g, (_a, _b) in zip(GAPS, SEG_SRC):
    _t += _g; PLACE.append(round(_t, 2)); _t += _b - _a


def to_video(seg, t):
    return PLACE[seg] + (t - SEG_SRC[seg][0])


def build_words():
    words = []
    for (seg, txt), (a, b) in zip(PHRASES, _M):
        toks = txt.split(" ")
        sy = [syll(x) for x in toks]
        per = (b - a) / sum(sy)
        t = a
        for k, (tok, s) in enumerate(zip(toks, sy)):
            words.append(dict(seg=seg, tok=tok, t0=to_video(seg, t), t1=to_video(seg, t + s * per), pend=k == len(toks) - 1))
            t += s * per
    return words


WORDS = build_words()
END = round(max(w["t1"] for w in WORDS) + HOLD_END, 1)


def norm(x):
    return re.sub(r"[^\wÀ-ÿ\-]", "", x).lower()


def kw(seg, word, n=1):
    c = 0
    for w in WORDS:
        if w["seg"] == seg and norm(w["tok"]) == word.lower():
            c += 1
            if c == n:
                return w["t0"]
    raise KeyError((seg, word, n))


def seg_start(i):
    return min(w["t0"] for w in WORDS if w["seg"] == i)


def seg_end(i):
    return max(w["t1"] for w in WORDS if w["seg"] == i)


# ---- marcos ----
S = [seg_start(i) - (0.3 if i == 0 else 0.6) for i in range(NSEG)]
S[0] = 0.0
M = dict(
    c0_william=kw(0, "william"), c0_recibo=kw(0, "recibo"), c0_portugal=kw(0, "portugal"), c0_autonomo=kw(0, "autónomo"), c0_diferente=kw(0, "diferente"), c0_atencao=kw(0, "atenção"),
    c1_portugal=kw(1, "portugal"), c1_isento=kw(1, "isento"), c1_espanha=kw(1, "espanha"), c1_paga=kw(1, "paga"), c1_mes=kw(1, "mês"), c1_pouco=kw(1, "pouco"),
    c1_depende=kw(1, "depende"), c1_200=kw(1, "200"), c1_600=kw(1, "600"),
    c2_noticia=kw(2, "notícia"), c2_primeira=kw(2, "primeira"), c2_2=kw(2, "2"), c2_80=kw(2, "80"), c2_ano=kw(2, "ano"),
    c3_imigrante=kw(3, "imigrante"), c3_turista=kw(3, "turista"), c3_abrir=kw(3, "abrir"), c3_autorizacao=kw(3, "autorização"), c3_trabalhar=kw(3, "trabalhar"),
    c4_tres=kw(4, "três"), c4_um=kw(4, "um"), c4_consulado=kw(4, "consulado"), c4_projeto=kw(4, "projeto"), c4_vale=kw(4, "vale"), c4_regiao=kw(4, "região"),
    c4_dois=kw(4, "dois"), c4_arraigo=kw(4, "arraigo"), c4_familiar=kw(4, "familiar"), c4_tres2=kw(4, "três", 2), c4_contrato=kw(4, "contrato"), c4_tempo=kw(4, "tempo"),
    c5_tem=kw(5, "tem"), c5_custa=kw(5, "custa"), c5_legalizado=kw(5, "legalizado"), c5_prefere=kw(5, "prefere"), c5_comenta=kw(5, "comenta"), c5_ajuda=kw(5, "ajuda"), c5_bio=kw(5, "bio"),
)


def _lines(ws, maxline):
    txt = " ".join(w["tok"] for w in ws)
    if len(txt) <= maxline:
        return [ws]
    best, bi = 1e9, 1
    for k in range(1, len(ws)):
        a = len(" ".join(w["tok"] for w in ws[:k])); b = len(" ".join(w["tok"] for w in ws[k:]))
        sc = max(a, b) + (6 if ws[k - 1]["tok"] in ("e", "a", "o", "de", "da", "na", "que", "um", "uma") else 0)
        if sc < best:
            best, bi = sc, k
    return [ws[:bi], ws[bi:]]


def _split(g, lim):
    L = lambda ws: len(" ".join(w["tok"] for w in ws))
    if L(g) <= lim or len(g) < 4:
        return [g]
    best, bi = 1e9, len(g) // 2
    for k in range(2, len(g) - 1):
        a, b = L(g[:k]), L(g[k:])
        if min(a, b) < 12:
            continue
        sc = abs(a - b) - (40 if g[k - 1]["tok"].endswith((",", ":")) else 0) + (10 if g[k - 1]["tok"] in ("e", "a", "o", "de", "da", "na", "um", "uma", "no", "do", "essa", "este", "seu", "sua", "para", "com", "em", "o", "comunicado", "dos", "das", "os", "as") else 0)
        if sc < best:
            best, bi = sc, k
    return _split(g[:bi], lim) + _split(g[bi:], lim)


def caption_chunks(maxline=28):
    groups, cur = [], []
    for w in WORDS:
        cur.append(w)
        if w["pend"]:
            groups.append(cur); cur = []
    chunks = []
    for g in groups:
        txt = " ".join(w["tok"] for w in g)
        parts = _split(g, 2 * maxline - 4)
        for part in parts:
            ls = _lines(part, maxline)
            ww = []
            for li, l in enumerate(ls):
                for w in l:
                    w = dict(w); w["line"] = li; ww.append(w)
            chunks.append(dict(words=ww, nlines=len(ls)))
    for i, c in enumerate(chunks):
        c["t0"] = c["words"][0]["t0"] - 0.06
        nxt = chunks[i + 1]["words"][0]["t0"] - 0.06 if i + 1 < len(chunks) else END
        c["t1"] = min(nxt, c["words"][-1]["t1"] + 0.9)
    return chunks


CHUNKS = caption_chunks()

if __name__ == "__main__":
    for c in CHUNKS:
        ls = [" ".join(w["tok"] for w in c["words"] if w["line"] == l) for l in range(c["nlines"])]
        print(f'{c["t0"]:6.2f}', " / ".join(ls))
    print("PLACE", PLACE, "END", END)
