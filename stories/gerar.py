"""Gera o story diário 'Bom dia, Portugal'.
Uso: python3 gerar.py tempo.json [AAAA-MM-DD]
tempo.json = [{"nome":"Lisboa","max":21.7,"min":15.0,"chuva":0,"condicao":"clear"}, ...]
(dados da ferramenta de previsão do tempo para Lisboa, Porto e Faro)"""
import json, sys, datetime, subprocess, os
from PIL import Image
AQUI=os.path.dirname(os.path.abspath(__file__))
DIAS=["Segunda-feira","Terça-feira","Quarta-feira","Quinta-feira","Sexta-feira","Sábado","Domingo"]
MESES=["","janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
COND={"clear":"Céu limpo","sunny":"Sol","partly_cloudy":"Sol e nuvens","cloudy":"Nublado","overcast":"Nublado","fog":"Nevoeiro",
      "drizzle":"Chuvisco","rain":"Chuva","showers":"Aguaceiros","thunderstorm":"Trovoada","snow":"Neve","wind":"Vento"}
def texto_dia(hoje):
    cal=json.load(open(os.path.join(AQUI,"calendario.json")))
    for ev in cal["eventos"]:
        d=datetime.date.fromisoformat(ev["data"]); n=(d-hoje).days
        prazo=ev.get("tipo")=="prazo"
        if n==0: return ("PRAZO DE HOJE" if prazo else "HOJE"), ev["hoje"], ev.get("confirmar",False)
        if 0<n<=ev["aviso"]:
            dt=f"{d.day}/{d.month}"
            return ((f"FALTA{'M' if n>1 else ''} {n} DIA{'S' if n>1 else ''}") if prazo else "AVISO"), ev["antes"].replace("{data}",dt), ev.get("confirmar",False)
    m=cal["mensal"]
    if hoje.day==m["dia"] and hoje.weekday()<5: return "PRAZO DE HOJE", m["texto"], False
    dicas=json.load(open(os.path.join(AQUI,"dicas.json")))
    return "DICA DO IMIGRANTE", dicas[hoje.toordinal()%len(dicas)], False
def main():
    tempo=json.load(open(sys.argv[1]))
    hoje=datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv)>2 else datetime.date.today()
    rot,dica,conf=texto_dia(hoje)
    cid=[]
    for t in tempo:
        c=t.get("condicao","clear"); ch=int(round(t.get("chuva",0)))
        ic="chuva" if (ch>=40 or c in("drizzle","rain","showers","thunderstorm")) else ("nuvem" if c in("partly_cloudy","cloudy","overcast","fog") or ch>=20 else "sol")
        cid.append({"nome":t["nome"],"icone":ic,"max":round(t["max"]),"min":round(t["min"]),"texto":f'{COND.get(c,"Previsão")} · chuva {ch}%'})
    dados={"data":f"{DIAS[hoje.weekday()]}, {hoje.day} de {MESES[hoje.month]}","cidades":cid,"dica":dica,"rotulo":rot}
    jp=os.path.join(AQUI,"_hoje.json"); json.dump(dados,open(jp,"w"),ensure_ascii=False)
    png=os.path.join(AQUI,"_story.png"); subprocess.run([sys.executable,os.path.join(AQUI,"desenho.py"),jp,png],check=True)
    out=os.path.abspath(f"LojaDoImigrante_story_tempo_{hoje.isoformat()}.jpg")
    Image.open(png).convert("RGB").save(out,quality=92)
    print(json.dumps({"arquivo":out,"rotulo":rot,"texto":dica,"conferir_data_oficial":conf},ensure_ascii=False))
main()
