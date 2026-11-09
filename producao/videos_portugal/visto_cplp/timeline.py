"""Linha do tempo do Reels "Visto CPLP: o caminho para morar em Portugal".
Enquanto não há narração: frases com tempos ESTIMADOS (ritmo ~5,8 sílabas/s).
Com a voz real: preencher MEASURED (início/fim de cada frase no áudio), SEG_SRC e GAPS."""
import re

FPS = 30

from phrases import PHRASES, OVERRIDE
NSEG = 7
RATE, PH_GAP = 5.8, 0.32
MEASURED_V = [(0.06, 1.06),(1.50, 5.69),(6.08, 6.71),(7.23, 9.25),(9.75, 13.06),(13.41, 19.18),(19.67, 25.20),(25.64, 29.34),(29.79, 31.63),(32.23, 33.21),(33.71, 35.56),(35.99, 38.21),(38.61, 42.65),(42.98, 47.60),(47.94, 51.89),(52.16, 53.78),(54.25, 57.09),(57.48, 65.42),(65.86, 67.44),(67.77, 73.67),(73.97, 77.57),(78.02, 79.36),(79.70, 87.55),(87.82, 92.33),(92.79, 99.40),(99.70, 103.22),(103.68, 112.16),(112.47, 115.12),(115.47, 117.10),(117.41, 121.18),(121.45, 122.61)]
SEG_SRC = None
GAPS = [0.3] + [0.55] * 6
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
    c0_turista=kw(0, "turista"), c0_morador=kw(0, "morador"), c0_acabou=kw(0, "acabou"), c0_hoje=kw(0, "hoje"),
    c1_manifestacao=kw(1, "manifestação"), c1_2024=kw(1, "2024"), c1_lei=kw(1, "lei"), c1_turista=kw(1, "turista"), c1_residencia=kw(1, "residência"),
    c2_cplp=kw(2, "cplp"), c2_brasil=kw(2, "brasil"), c2_consulado=kw(2, "consulado"), c2_viajar=kw(2, "viajar"), c2_emprego=kw(2, "emprego"),
    c3_passaporte=kw(3, "passaporte"), c3_antecedentes=kw(3, "antecedentes"), c3_graca=kw(3, "graça"), c3_federal=kw(3, "federal"), c3_cartorio=kw(3, "cartório"), c3_haia=kw(3, "haia"),
    c3_90=kw(3, "90"), c3_cedo=kw(3, "cedo"), c3_sustentar=kw(3, "sustentar"), c3_dinheiro=kw(3, "dinheiro"), c3_termo=kw(3, "termo"), c3_legalmente=kw(3, "legalmente"),
    c4_embarca=kw(4, "embarca"), c4_aima=kw(4, "aima"), c4_anos=kw(4, "anos"), c4_cartao=kw(4, "cartão"), c4_meses=kw(4, "meses"),
    c5_brasil=kw(5, "brasil"), c5_saida=kw(5, "saída"), c5_fevereiro=kw(5, "fevereiro"), c5_residente=kw(5, "residente"), c5_dinheiro=kw(5, "dinheiro"), c5_iof=kw(5, "iof"), c5_350=kw(5, "350"),
    c6_visto=kw(6, "visto"), c6_antecedentes=kw(6, "antecedentes"), c6_sustento=kw(6, "sustento"), c6_aima=kw(6, "aima"), c6_receita=kw(6, "receita"), c6_salva=kw(6, "salva"), c6_ajuda=kw(6, "ajuda"), c6_bio=kw(6, "bio"),
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
