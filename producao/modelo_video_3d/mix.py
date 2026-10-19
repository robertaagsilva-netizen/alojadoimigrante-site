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
for i in range(8): put(A.pop(), M["c0_curtidas"] - 0.5 + i * 0.12, 0.25)
put(A.thud(), M["c0_mente"] - 0.3, 0.5); put(A.thud(), M["c0_acabou"] - 0.3, 0.5); put(A.bell(), M["c0_acusacao"] - 0.4, 0.3); put(A.impact_small(), M["c0_fatos"] - 0.2, 0.7)
for k in ("c1_cnn", "c1_16", "c1_investigada"): put(A.bell(), M[k] - 0.3, 0.35)
put(A.pop(), M["c1_mente"] - 0.4, 0.4); put(A.pop(), M["c1_pt"] - 0.5, 0.4); put(A.pop(), M["c1_defesa"] - 0.3, 0.35)
put(A.thud(), M["c2_mente"] - 0.4, 0.7); put(A.pop(), M["c2_prova"] - 0.4, 0.5); put(A.thud(), M["c2_delacao"] - 0.3, 0.5); put(A.pop(), M["c2_lei"] - 0.3, 0.4); put(A.impact_small(), M["c2_insinuacao"] - 1.2, 0.6)
put(A.impact_small(), M["c3_mendonca"] - 0.4, 0.5); put(A.pop(), M["c3_delegados"] - 0.4, 0.4); put(A.bell(), M["c3_conclusao"] - 0.3, 0.3); put(A.pop(), M["c3_nega"] - 0.3, 0.4)
put(A.bell(), M["c4_lado"] - 0.3, 0.3); put(A.pop(), M["c4_desconhece"] - 0.2, 0.45); put(A.pop(), M["c4_nega"] - 0.3, 0.45)
put(A.bell(), M["c5_reais"] - 0.3, 0.35); put(A.thud(), M["c5_provadas"] - 0.3, 0.6); put(A.pop(), M["c5_oposicao"] - 0.4, 0.4)
put(A.pop(), M["c5_comenta"] - 0.1, 0.5); put(A.pop(), M["c5_ajuda"] - 0.3, 0.35)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
