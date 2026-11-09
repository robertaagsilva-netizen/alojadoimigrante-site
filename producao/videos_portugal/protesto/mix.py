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
put(A.pop(), M["c0_protesto"] - 0.3, 0.4); put(A.bell(), M["c0_parlamento"] - 0.4, 0.35); put(A.thud(), M["c0_errado"] - 0.3, 0.5)
put(A.bell(), M["c1_cancelada"] - 0.3, 0.35); put(A.thud(), M["c1_nova"] - 0.3, 0.5); put(A.impact_small(), M["c1_85"] - 0.4, 0.5)
for k in ("c2_policia", "c2_aima", "c2_tribunal"): put(A.pop(), M[k] - 0.3, 0.45)
put(A.thud(), M["c2_suspende"] - 0.3, 0.5)
put(A.bell(), M["c3_nao"] - 0.2, 0.45); put(A.thud(), M["c3_ameaca"] - 0.3, 0.5); put(A.pop(), M["c3_estudante"] - 0.4, 0.35)
for k in ("c4_lado", "c4_intimidacao", "c4_perigoso"): put(A.pop(), M[k] - 0.4, 0.4)
put(A.bell(), M["c5_protestar"] - 0.3, 0.4); put(A.thud(), M["c5_ameacar"] - 0.3, 0.5); put(A.pop(), M["c5_manda"] - 0.1, 0.4); put(A.impact_small(), M["c5_ajuda"] - 0.3, 0.5)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
