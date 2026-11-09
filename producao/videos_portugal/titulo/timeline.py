"""Linha do tempo do Reels "Checagem: vídeo do Moro sobre Luchsinger (3D)".
Enquanto não há narração: frases com tempos ESTIMADOS (ritmo ~5,8 sílabas/s).
Com a voz real: preencher MEASURED (início/fim de cada frase no áudio), SEG_SRC e GAPS."""
import re

FPS = 30

from phrases import PHRASES, OVERRIDE
NSEG = 6
RATE, PH_GAP = 5.8, 0.32
MEASURED_V = [(0.06, 4.04),(4.66, 7.89),(8.29, 8.99),(9.48, 13.35),(13.87, 15.79),(16.25, 25.71),(26.10, 30.69),(31.14, 37.70),(38.10, 41.00),(41.39, 44.68),(45.13, 46.86),(47.19, 48.70),(49.08, 50.57),(51.01, 53.94),(54.41, 57.97),(58.33, 61.04),(61.43, 64.04),(64.50, 65.55),(65.95, 66.57),(66.89, 74.83),(75.21, 80.41),(80.88, 85.98),(86.37, 88.89),(89.30, 95.45)]
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
    c0_reabriu=kw(0, "reabriu"), c0_prazo=kw(0, "prazo"), c0_perder=kw(0, "perder"), c0_atencao=kw(0, "atenção"),
    c1_novembro=kw(1, "novembro"), c1_fechado=kw(1, "fechado"), c1_primeiro=kw(1, "primeiro"), c1_regularizar=kw(1, "regularizar"), c1_local=kw(1, "local"), c1_transferir=kw(1, "transferir"),
    c2_internet=kw(2, "internet"), c2_tse=kw(2, "tse"), c2_cpf=kw(2, "cpf"), c2_morada=kw(2, "morada"), c2_presidente=kw(2, "presidente"), c2_prefeito=kw(2, "prefeito"),
    c3_urgente=kw(3, "urgente"), c3_justificar=kw(3, "justificar"), c3_primeiro=kw(3, "primeiro"), c3_segundo=kw(3, "segundo"), c3_separada=kw(3, "separada"), c3_etitulo=kw(3, "e-título"),
    c4_multa=kw(4, "multa"), c4_tres=kw(4, "três"), c4_cancelado=kw(4, "cancelado"), c4_passaporte=kw(4, "passaporte"),
    c5_resumo=kw(5, "resumo"), c5_dia=kw(5, "dia"), c5_manda=kw(5, "manda"), c5_ajuda=kw(5, "ajuda"), c5_direct=kw(5, "direct"),
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
