import math, random, sys, subprocess
import cairo

W, H = 1080, 1920
CX = 530  # centro visual (deslocado p/ longe dos botões à direita)

BG = (0x0C / 255, 0x10 / 255, 0x19 / 255)
INK = (0xF3 / 255, 0xEF / 255, 0xE6 / 255)
BLUE = (0x73 / 255, 0x9A / 255, 0xFF / 255)
CARD = (0x12 / 255, 0x18 / 255, 0x25 / 255)
AMBER = (0xF2 / 255, 0xB0 / 255, 0x4F / 255)

SERIF, SERIF_I = ("Instrument Serif", False), ("Instrument Serif", True)
SANS, SANS_M, SANS_SB = ("Inter", False), ("Inter Medium", False), ("Inter SemiBold", False)
MONO = ("JetBrains Mono Medium", False)


# ---------- utilidades ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def p(t, a, b):
    return clamp((t - a) / (b - a)) if b != a else float(t >= a)


def eo(x):  # ease out cubic
    return 1 - (1 - x) ** 3


def eio(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def eback(x, s=1.4):
    x = x - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def lerp(a, b, x):
    return a + (b - a) * x


def lerpc(c1, c2, x):
    return tuple(lerp(a, b, x) for a, b in zip(c1, c2))


def fade(t, a, b, fi=0.45, fo=0.45):
    """alfa de um elemento visível entre a e b"""
    return min(eo(p(t, a, a + fi)), 1 - eio(p(t, b - fo, b))) if b is not None else eo(p(t, a, a + fi))


def font(ctx, f, size):
    fam, it = f
    ctx.select_font_face(fam, cairo.FONT_SLANT_ITALIC if it else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def measure(ctx, s, f, size, ls=0):
    font(ctx, f, size)
    w = 0
    for i, ch in enumerate(s):
        w += ctx.text_extents(ch).x_advance + (ls if i < len(s) - 1 else 0)
    return w


def text(ctx, s, x, y, f, size, col, a=1.0, anchor="c", ls=0):
    if a <= 0.003:
        return 0
    w = measure(ctx, s, f, size, ls)
    x0 = x - (w / 2 if anchor == "c" else (w if anchor == "r" else 0))
    ctx.set_source_rgba(*col, a)
    if ls == 0:
        ctx.move_to(x0, y)
        ctx.show_text(s)
    else:
        for ch in s:
            ctx.move_to(x0, y)
            ctx.show_text(ch)
            x0 += ctx.text_extents(ch).x_advance + ls
    return w


def fit(ctx, s, f, maxw, maxsize, ls=0):
    size = maxsize
    while size > 10 and measure(ctx, s, f, size, ls) > maxw:
        size -= 2
    return size


def wrap(ctx, s, f, size, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if measure(ctx, t, f, size) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


class Zoom:
    def __init__(self, ctx, s, cx=CX, cy=H / 2, dy=0):
        self.ctx, self.s, self.cx, self.cy, self.dy = ctx, s, cx, cy, dy

    def __enter__(self):
        c = self.ctx
        c.save()
        c.translate(self.cx, self.cy + self.dy)
        c.scale(self.s, self.s)
        c.translate(-self.cx, -self.cy)

    def __exit__(self, *a):
        self.ctx.restore()


def rise(t, t0, dur=0.55, dist=36):
    k = eo(p(t, t0, t0 + dur))
    return k, (1 - k) * dist


# ---------- fundo ----------
def make_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    c.set_source_rgb(*BG)
    c.paint()
    c.set_line_width(1)
    c.set_source_rgba(*INK, 0.035)
    for x in range(0, W + 1, 60):
        c.move_to(x + 0.5, 0); c.line_to(x + 0.5, H)
    for y in range(0, H + 1, 60):
        c.move_to(0, y + 0.5); c.line_to(W, y + 0.5)
    c.stroke()
    # pontos nos cruzamentos a cada 240px
    c.set_source_rgba(*INK, 0.09)
    for x in range(0, W + 1, 240):
        for y in range(0, H + 1, 240):
            c.rectangle(x - 1, y - 1, 3, 3)
    c.fill()
    g = cairo.RadialGradient(CX, H * 0.45, 200, CX, H * 0.45, 1250)
    g.add_color_stop_rgba(0, *BG, 0)
    g.add_color_stop_rgba(1, *BG, 0.85)
    c.set_source(g)
    c.paint()
    return s


BGS = make_bg()
# ---------- legendas ----------
def captions(ctx, t, CHUNKS):
    size, lh = 52, 66
    for c in CHUNKS:
        if not (c["t0"] <= t < c["t1"]):
            continue
        a = min(eo(p(t, c["t0"], c["t0"] + 0.12)), 1 - p(t, c["t1"] - 0.1, c["t1"]) if c["t1"] - c["t0"] > 1.2 and c is CHUNKS[-1] else 1)
        dy = (1 - eo(p(t, c["t0"], c["t0"] + 0.2))) * 10
        n = c["nlines"]
        base = 1478 - (lh / 2 if n == 2 else 0) + 18
        font(ctx, SANS_SB, size)
        sp = ctx.text_extents(" ").x_advance
        for li in range(n):
            ws = [w for w in c["words"] if w["line"] == li]
            widths = [measure(ctx, w["tok"], SANS_SB, size) for w in ws]
            tot = sum(widths) + sp * (len(ws) - 1)
            x = CX - tot / 2
            y = base + li * lh + dy
            for w, wd in zip(ws, widths):
                on = eo(p(t, w["t0"] - 0.04, w["t0"] + 0.1))
                col = lerpc((0.55, 0.56, 0.6), INK, on)
                # sombra leve p/ contraste
                text(ctx, w["tok"], x + 2, y + 3, SANS_SB, size, (0, 0, 0), 0.45 * a, "l")
                text(ctx, w["tok"], x, y, SANS_SB, size, col, a, "l")
                x += wd + sp


