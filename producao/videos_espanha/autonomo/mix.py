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
put(A.pop(), M["c0_recibo"] - 0.3, 0.4); put(A.bell(), M["c0_autonomo"] - 0.3, 0.35); put(A.impact_small(), M["c0_atencao"] - 0.2, 0.5)
put(A.pop(), M["c1_isento"] - 0.4, 0.4); put(A.thud(), M["c1_espanha"] - 0.3, 0.5)
for i in range(3): put(A.click(), M["c1_paga"] - 0.1 + i * 0.25, 0.3)
for i in range(11): put(A.click(1800 + i * 60), M["c1_200"] - 0.1 + i * 0.27, 0.25)
for i in range(12): put(A.pop(), M["c2_noticia"] + i * 0.12, 0.15)
put(A.bell(), M["c2_80"] - 0.3, 0.45)
put(A.thud(), M["c3_abrir"] - 0.2, 0.6); put(A.bell(), M["c3_autorizacao"] - 0.2, 0.4)
for k in ("c4_um", "c4_dois", "c4_tres2"): put(A.impact_small(), M[k] - 0.3, 0.45)
put(A.pop(), M["c4_consulado"] + 0.2, 0.35)
put(A.bell(), M["c5_tem"] - 0.4, 0.35); put(A.pop(), M["c5_legalizado"] - 0.4, 0.4); put(A.pop(), M["c5_prefere"] - 0.1, 0.45); put(A.pop(), M["c5_ajuda"] - 0.3, 0.3)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
