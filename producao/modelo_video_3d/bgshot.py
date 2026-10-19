import sys, base64
from playwright.sync_api import sync_playwright
from timeline import S, M, END
t=float(sys.argv[1])
with sync_playwright() as pw:
    b=pw.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":1080,"height":1920}); pg.goto("http://localhost:8778/scene.html"); pg.wait_for_function("window.ready === true",timeout=60000)
    r=pg.evaluate("([t,T])=>window.renderAt(t,T)",[t,dict(S=S,M=M,END=END)])
    open(f"chk/bg_{t}.png","wb").write(base64.b64decode(r["img"].split(",")[1])); b.close()
