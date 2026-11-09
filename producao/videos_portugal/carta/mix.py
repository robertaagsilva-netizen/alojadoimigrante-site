import numpy as np, wave
import audio_lib as A
from timeline import S, M, END
A.BPM = 92; A.BEAT = 60 / 92; A.BAR = 4 * A.BEAT
mL, mR = A.music()
SFX = np.zeros(A.N)
def put(sig, t0, g=1.0): A.add(SFX, sig, t0, g)
for s in S[1:]:
    put(A.whoosh(0.9, 200, 2500), s - 0.1, 0.55)
put(A.impact_small(), 0.05, 0.7)
put(A.pop(), M["c0_carta"] - 0.4, 0.45); put(A.thud(), M["c0_indeferido"] - 0.4, 0.5); put(A.bell(), M["c0_calma"] - 0.2, 0.35)
for i in range(6): put(A.click(1500), M["c0_relogio"] - 0.2 + i * 0.4, 0.25)
put(A.pop(), M["c1_decisao"] - 0.3, 0.4); put(A.impact_small(), M["c1_10"] - 0.3, 0.5)
for i in range(10): put(A.click(2000 - i * 60), M["c2_prazo"] + i * 0.28, 0.3)
put(A.thud(), M["c2_definitiva"] - 0.4, 0.6)
for k in ("c3_morada", "c3_contrato", "c3_salario", "c3_seguranca"): put(A.pop(), M[k] - 0.3, 0.4)
put(A.bell(), M["c3_junte"] - 0.2, 0.35)
put(A.thud(), M["c4_saiu"] - 0.6, 0.45); put(A.pop(), M["c4_recurso"] - 0.3, 0.4); put(A.bell(), M["c4_advogado"] - 0.3, 0.35)
put(A.thud(), M["c5_gaveta"] - 0.4, 0.5); put(A.impact_small(), M["c5_10"] - 0.3, 0.5); put(A.pop(), M["c5_salva"] - 0.1, 0.4); put(A.impact_small(), M["c5_ajuda"] - 0.3, 0.5)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
