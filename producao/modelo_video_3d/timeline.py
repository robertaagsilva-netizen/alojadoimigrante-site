"""Linha do tempo do Reels "Checagem: vídeo do Moro sobre Luchsinger (3D)".
Enquanto não há narração: frases com tempos ESTIMADOS (ritmo ~5,8 sílabas/s).
Com a voz real: preencher MEASURED (início/fim de cada frase no áudio), SEG_SRC e GAPS."""
import re

FPS = 30

from phrases import PHRASES, OVERRIDE
NSEG = 6
RATE, PH_GAP = 5.8, 0.32
MEASURED_V = [(0.04, 4.91),(5.44, 12.75),(13.41, 15.88),(16.59, 17.44),(17.92, 19.30),(19.77, 22.61),(23.14, 32.15),(32.84, 40.12),(40.70, 42.73),(43.30, 49.32),(49.78, 52.02),(52.62, 54.65),(55.20, 57.78),(58.20, 61.05),(61.38, 63.16),(63.44, 67.29),(67.96, 72.39),(72.73, 73.99),(74.59, 82.95),(83.37, 85.72),(86.10, 90.35),(90.95, 96.01),(96.45, 99.26),(99.81, 106.33),(106.70, 111.78),(112.32, 114.30),(114.63, 117.58)]
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
    c0_viralizou=kw(0, "viralizou"), c0_curtidas=kw(0, "curtidas"), c0_mente=kw(0, "mente"), c0_acabou=kw(0, "acabou"), c0_acusacao=kw(0, "acusação"), c0_fatos=kw(0, "fatos"),
    c1_verdade=kw(1, "verdade"), c1_cnn=kw(1, "cnn"), c1_mente=kw(1, "mente"), c1_filhas=kw(1, "filhas"), c1_cpmi=kw(1, "cpmi"), c1_16=kw(1, "16"), c1_pt=kw(1, "pt"),
    c1_investigada=kw(1, "investigada"), c1_careca=kw(1, "careca"), c1_defesa=kw(1, "defesa"),
    c2_exagera=kw(2, "exagera"), c2_mente=kw(2, "mente"), c2_prova=kw(2, "prova"), c2_delacao=kw(2, "delação"), c2_lei=kw(2, "lei"), c2_insinuacao=kw(2, "insinuação"), c2_apresenta=kw(2, "apresenta", 2),
    c3_andrei=kw(3, "andrei"), c3_mendonca=kw(3, "mendonça"), c3_delegados=kw(3, "delegados"), c3_conclusao=kw(3, "conclusão"), c3_nega=kw(3, "nega"),
    c4_lado=kw(4, "lado"), c4_desconhece=kw(4, "desconhece"), c4_lulinha=kw(4, "lulinha"), c4_nega=kw(4, "nega"),
    c5_reais=kw(5, "reais"), c5_provadas=kw(5, "provadas"), c5_oposicao=kw(5, "oposição"), c5_turno=kw(5, "turno"), c5_comenta=kw(5, "comenta"), c5_ajuda=kw(5, "ajuda"), c5_bio=kw(5, "bio"),
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
