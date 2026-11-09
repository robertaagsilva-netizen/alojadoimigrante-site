import re, sys
def apply(M_DICT, CHAP_CODE, UPD_CODE, ANCH_CODE, CAM, COMPOSE_HEAD, COMPOSE_BODY, MIX_BODY, OUT, PORT):
    meas=[l.split("#")[0].strip().rstrip(",") for l in open("meas.txt") if l.strip()]
    src=open("timeline.py").read()
    src=re.sub(r"MEASURED_V = \[.*?\]\n","MEASURED_V = ["+",".join(meas)+"]\n",src,flags=re.S)
    a=src.index("M = dict("); b=src.index("\n)\n",a)+3
    src=src[:a]+"M = dict(\n"+M_DICT+"\n)\n"+src[b:]
    open("timeline.py","w").write(src)
    s=open("scene.html").read()
    s=s.replace("""x.font = '900 250px Inter, Arial'; x.fillText(big, w / 2, 400);""","""x.font = (big.length > 4 ? '900 140px' : big.length > 3 ? '900 170px' : big.length > 2 ? '900 200px' : '900 250px') + ' Inter, Arial'; x.fillText(big, w / 2, 400);""")
    s=s.replace("""x.font = '800 50px Inter, Arial'; x.fillText(sub, w / 2, 540); }""","""x.font = (sub.length > 13 ? '800 34px' : sub.length > 10 ? '800 40px' : '800 50px') + ' Inter, Arial'; x.fillText(sub, w / 2, 540); }""")
    s=s.replace("""x.font = '900 64px Inter, Arial'; x.textAlign = 'center'; x.fillText(top, w / 2, 84);""","""x.font = (top.length > 10 ? '900 46px' : '900 64px') + ' Inter, Arial'; x.textAlign = 'center'; x.fillText(top, w / 2, 84);""")
    a=s.index("// cap 0: celular viralizou"); b=s.index("const CAM = [")
    s=s[:a]+CHAP_CODE+"\n"+s[b:]
    a=s.index("  // 0\n  phone.scale"); b=s.index("  for (let i = 0; i < N; i++) { const s = seeds[i];")
    s=s[:a]+UPD_CODE+"\n"+s[b:]
    a=s.index("  a.c1 = PX1"); b=s.index("  return { img:")
    s=s[:a]+ANCH_CODE+"\n"+s[b:]
    a=s.index("const CAM = [")+len("const CAM = ["); b=s.index("];",a)
    s=s[:a]+"\n"+CAM+"\n"+s[b:]
    open("scene.html","w").write(s)
    c=open("compose.py").read()
    a=c.index("CHAP = ["); b=c.index("def win(t, i):")
    c=c[:a]+COMPOSE_HEAD+"\n"+c[b:]
    a=c.index("    # 0\n    w0 = win(t, 0)"); b=c.index("    for i, s_ in NOTE.items():")
    c=c[:a]+COMPOSE_BODY+"\n"+c[b:]
    c=c.replace('"LOJA DO IMIGRANTE · CHECAGEM"','"LOJA DO IMIGRANTE · PORTUGAL"').replace("8778",PORT)
    open("compose.py","w").write(c)
    open("bgshot.py","w").write(open("bgshot.py").read().replace("8778",PORT)) if False else None
    bs=open("bgshot.py").read().replace("8778",PORT); open("bgshot.py","w").write(bs)
    m=open("mix.py").read()
    a=m.index('put(A.impact_small(), 0.05, 0.7)'); b=m.index('v, mask = A.voice()')
    m=m[:a]+"put(A.impact_small(), 0.05, 0.7)\n"+MIX_BODY+"\n"+m[b:]
    open("mix.py","w").write(m)
    r=open("render.sh").read().replace("LojaDoImigrante_checagem_Moro_3D.mp4",OUT)
    open("render.sh","w").write(r)
