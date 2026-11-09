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
put(A.pop(), M["c0_reabriu"] - 0.4, 0.45); put(A.bell(), M["c0_prazo"] - 0.3, 0.4); put(A.thud(), M["c0_perder"] - 0.3, 0.5)
for k in ("c1_primeiro", "c1_regularizar", "c1_local", "c1_transferir"): put(A.pop(), M[k] - 0.3, 0.4)
put(A.pop(), M["c2_internet"] - 0.3, 0.4); put(A.bell(), M["c2_cpf"] - 0.3, 0.3); put(A.impact_small(), M["c2_presidente"] - 0.5, 0.45)
put(A.thud(), M["c3_urgente"] - 0.3, 0.5); put(A.impact_small(), M["c3_primeiro"] - 0.3, 0.45); put(A.impact_small(), M["c3_segundo"] - 0.3, 0.45); put(A.pop(), M["c3_etitulo"] - 0.6, 0.35)
put(A.pop(), M["c4_multa"] - 0.3, 0.4)
for i in range(3): put(A.click(1800 - i * 200), M["c4_tres"] + i * 0.35, 0.35)
put(A.thud(), M["c4_cancelado"] - 0.4, 0.55); put(A.thud(), M["c4_passaporte"] - 0.3, 0.5)
put(A.bell(), M["c5_resumo"] - 0.3, 0.4); put(A.pop(), M["c5_dia"] - 0.3, 0.4); put(A.pop(), M["c5_manda"] - 0.1, 0.4); put(A.impact_small(), M["c5_ajuda"] - 0.3, 0.5)
v, mask = A.voice(); v = v / (np.abs(v).max() + 1e-9) * 0.95
t = np.arange(A.N) / A.SR
g = np.clip(t / 0.6, 0, 1) * np.clip((END - t) / 2.0, 0, 1) * A.voice_duck(mask) * 0.5
L = mL * g + SFX * 0.8 + v; R = mR * g + SFX * 0.8 + v
st = np.stack([L, R], 1); st /= np.abs(st).max() / 0.89
with wave.open("mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
