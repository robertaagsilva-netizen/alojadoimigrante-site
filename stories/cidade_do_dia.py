"""Uso: python3 cidade_do_dia.py [AAAA-MM-DD]
Imprime as 3 cidades do story do dia: Lisboa e Porto fixas + 1 cidade em rodízio (cidades.json)."""
import json, sys, os, datetime
AQUI = os.path.dirname(os.path.abspath(__file__))
hoje = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
C = json.load(open(os.path.join(AQUI, "cidades.json")))
extra = C[hoje.toordinal() % len(C)]
print(json.dumps([{"nome": "Lisboa", "lat": 38.7223, "lon": -9.1393}, {"nome": "Porto", "lat": 41.1579, "lon": -8.6291}, extra], ensure_ascii=False))
