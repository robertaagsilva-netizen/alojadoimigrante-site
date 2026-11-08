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
put(A.pop(), M["c0_idioma"] - 0.4, 0.4); put(A.bell(), M["c0_razao"] - 0.3, 0.35); put(A.thud(), M["c0_anos"] - 0.4, 0.5)
put(A.pop(), M["c1_anos"] - 0.3, 0.4); put(A.pop(), M["c1_anos"] + 0.05, 0.4); put(A.thud(), M["c1_turista"] - 0.3, 0.5); put(A.thud(), M["c1_estudante"] - 0.2, 0.5)
put(A.bell(), M["c2_dele"] - 0.3, 0.45); put(A.pop(), M["c2_nao"] - 0.5, 0.45); put(A.pop(), M["c2_138"] - 0.6, 0.35)
put(A.bell(), M["c3_ccse"] - 0.3, 0.4)
for i in range(25): put(A.click(1700 + i * 30), M["c3_25"] - 0.2 + i * 0.05, 0.15)
put(A.bell(), M["c4_ficha"] - 0.2, 0.4); put(A.pop(), M["c4_noticia"] - 0.3, 0.4); put(A.impact_small(), M["c4_nacionalidade"] - 0.6, 0.45)
for k in ("c5_anos", "c5_espanhol", "c5_cultura", "c5_ficha"): put(A.pop(), M[k] - 0.3, 0.4)
put(A.pop(), M["c5_fala"] - 0.3, 0.45); put(A.pop(), M["c5_ajuda"] - 0.3, 0.3)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
