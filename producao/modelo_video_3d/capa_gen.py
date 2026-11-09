import sys, cairo
from engine import text, fit, W, H, MONO
from compose import YEL, INK, CRM, pill
HEAVY = ("Inter Black", False)
bgf, kicker, top, l1, l2, bottom, fontes, out = sys.argv[1:9]
bg = cairo.ImageSurface.create_from_png(bgf)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
c.set_source_rgb(0.03, 0.03, 0.03); c.paint()
c.set_source_surface(bg, 0, 160); c.paint()
g = cairo.LinearGradient(0, 0, 0, 950); g.add_color_stop_rgba(0, 0.03, 0.03, 0.03, 1); g.add_color_stop_rgba(0.72, 0.03, 0.03, 0.03, 0.85); g.add_color_stop_rgba(1, 0.03, 0.03, 0.03, 0)
c.rectangle(0, 0, W, 950); c.set_source(g); c.fill()
text(c, kicker, 540, 340, MONO, 26, CRM, 0.8, ls=6)
pill(c, top, 540, 410, 28, INK, YEL, 1)
for y, t_, col in [(560, l1, CRM), (680, l2, YEL)]:
    text(c, t_, 540, y, HEAVY, fit(c, t_, HEAVY, 960, 112, -3), col, 1, ls=-3)
pill(c, bottom, 540, 1560, 26, INK, YEL, 1)
text(c, fontes, 540, 1640, MONO, 20, CRM, 0.7, ls=1)
text(c, "@alojadoimigrante.pt", 540, 1700, MONO, 28, CRM, 0.9, ls=3)
s.write_to_png(out)
