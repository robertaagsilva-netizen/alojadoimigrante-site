import cairo, math, json, sys
D=json.load(open(sys.argv[1])); out=sys.argv[2]
W,H=1080,1920
s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H); c=cairo.Context(s)
def hx(h,a=1): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(a,)
YEL,INK,MUTE,PANEL,LINE=hx('#ffd447'),hx('#f3efe4'),hx('#a29d90'),hx('#191815'),hx('#2b2a26')
g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgba(0,*hx('#15140f')); g.add_color_stop_rgba(1,*hx('#0a0a09')); c.set_source(g); c.paint()
for y in range(30,H,40):
    for x in range(30,W,40): c.set_source_rgba(*hx('#f3efe4',0.05)); c.arc(x,y,1.8,0,6.283); c.fill()
def T(t,size,x,y,col,font="Inter Display",bold=1,align="l"):
    c.select_font_face(font,0,bold); c.set_font_size(size); e=c.text_extents(t)
    if align=="c": x=x-e.width/2-e.x_bearing
    if align=="r": x=x-e.width-e.x_bearing
    c.set_source_rgba(*col); c.move_to(x,y); c.show_text(t); return e
def rr(x,y,w,h,r):
    c.new_sub_path(); c.arc(x+w-r,y+r,r,-math.pi/2,0); c.arc(x+w-r,y+h-r,r,0,math.pi/2); c.arc(x+r,y+h-r,r,math.pi/2,math.pi); c.arc(x+r,y+r,r,math.pi,1.5*math.pi); c.close_path()
def sun(x,y,r):
    c.set_source_rgba(*YEL); c.arc(x,y,r,0,6.283); c.fill()
    c.set_line_width(7); c.set_line_cap(1)
    for k in range(8):
        a=k*math.pi/4; c.move_to(x+math.cos(a)*(r+12),y+math.sin(a)*(r+12)); c.line_to(x+math.cos(a)*(r+26),y+math.sin(a)*(r+26)); c.stroke()
def cloud(x,y,sc,col):
    c.set_source_rgba(*col)
    for dx,dy,r in ((-28,8,24),(0,-10,32),(30,6,24)): c.arc(x+dx*sc,y+dy*sc,r*sc,0,6.283); c.fill()
    rr(x-52*sc,y+4*sc,104*sc,32*sc,16*sc); c.fill()
def icon(kind,x,y):
    if kind=="sol": sun(x,y,30)
    elif kind=="nuvem": sun(x-22,y-18,22); cloud(x+12,y+10,1.0,INK)
    else:
        cloud(x,y-6,1.0,INK); c.set_source_rgba(*hx('#7cc4ff')); c.set_line_width(6)
        for dx in (-26,0,26): c.move_to(x+dx,y+40); c.line_to(x+dx-8,y+60); c.stroke()
# topo
T("LOJA DO IMIGRANTE",34,90,250,YEL,font="Inter")
T("Bom dia, Portugal",92,90,355,INK)
T(D["data"],44,90,420,MUTE,font="Inter",bold=0)
y=480
for cid in D["cidades"]:
    rr(70,y,940,215,36); c.set_source_rgba(*PANEL); c.fill_preserve(); c.set_source_rgba(*LINE); c.set_line_width(2); c.stroke()
    icon(cid["icone"],195,y+108)
    T(cid["nome"],56,310,y+95,INK)
    T(cid["texto"],32,310,y+150,MUTE,font="Inter",bold=0)
    T(f'{cid["max"]}°',100,960,y+130,YEL,align="r")
    T(f'mín. {cid["min"]}°',34,960,y+182,MUTE,font="Inter",bold=0,align="r")
    y+=240
# dica
y+=10
c.select_font_face("Inter Display",0,1); fs=42; c.set_font_size(fs)
words=D["dica"].split(); lines=[]; cur=""
for w in words:
    t=(cur+" "+w).strip()
    if c.text_extents(t).width>840: lines.append(cur); cur=w
    else: cur=t
lines.append(cur); lines=lines[:4]
bh=130+len(lines)*54; rr(70,y,940,bh,36); c.set_source_rgba(*YEL); c.fill()
T(D.get("rotulo","DICA DO IMIGRANTE"),30,120,y+68,hx('#0c0c0b'),font="Inter")
for i,l in enumerate(lines): T(l,fs,120,y+130+i*54,hx('#0c0c0b'))
y+=bh+70
T("Todo dia às 6h aqui nos stories",32,W/2,y,MUTE,font="Inter",bold=0,align="c")
T("@alojadoimigrante.pt",36,W/2,y+52,INK,font="Inter",align="c")
s.write_to_png(out)
