"""Linha do tempo do Reels "Checagem: vídeo do Moro sobre Luchsinger (3D)".
Enquanto não há narração: frases com tempos ESTIMADOS (ritmo ~5,8 sílabas/s).
Com a voz real: preencher MEASURED (início/fim de cada frase no áudio), SEG_SRC e GAPS."""
import re

FPS = 30

from phrases import PHRASES, OVERRIDE
NSEG = 6
RATE, PH_GAP = 5.8, 0.32
MEASURED_V = [(0.04, 3.79),(4.38, 6.41),(6.85, 9.61),(10.18, 10.91),(11.41, 20.53),(21.09, 23.53),(23.90, 27.42),(28.01, 28.74),(29.26, 33.13),(33.60, 35.23),(35.71, 38.00),(38.50, 39.90),(40.31, 40.63),(40.96, 44.67),(45.13, 48.14),(48.64, 54.15),(54.58, 55.33),(55.69, 58.60),(59.01, 63.77),(64.23, 65.69),(66.01, 70.21),(70.61, 72.91),(73.30, 78.72)]
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
    c0_protesto=kw(0, "protesto"), c0_parlamento=kw(0, "parlamento"), c0_errado=kw(0, "errado"), c0_atencao=kw(0, "atenção"),
    c1_secretario=kw(1, "secretário"), c1_cancelada=kw(1, "cancelada"), c1_ordem=kw(1, "ordem"), c1_nova=kw(1, "nova"), c1_85=kw(1, "85"), c1_existia=kw(1, "existia"),
    c2_policia=kw(2, "polícia"), c2_aima=kw(2, "aima"), c2_tribunal=kw(2, "tribunal"), c2_suspende=kw(2, "suspende"),
    c3_proibido=kw(3, "proibido"), c3_nao=kw(3, "não"), c3_manifestacao=kw(3, "manifestação"), c3_ameaca=kw(3, "ameaça"), c3_estudante=kw(3, "estudante"), c3_porto=kw(3, "porto"),
    c4_lado=kw(4, "lado"), c4_socialista=kw(4, "socialista"), c4_intimidacao=kw(4, "intimidação"), c4_sindicato=kw(4, "sindicato"), c4_perigoso=kw(4, "perigoso"),
    c5_protestar=kw(5, "protestar"), c5_ameacar=kw(5, "ameaçar"), c5_custar=kw(5, "custar"), c5_manda=kw(5, "manda"), c5_ajuda=kw(5, "ajuda"), c5_direct=kw(5, "direct"),
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
