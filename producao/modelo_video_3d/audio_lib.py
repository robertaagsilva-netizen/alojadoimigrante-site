"""Trilha original (sintetizada) + efeitos sonoros, sincronizados com timeline.py"""
import numpy as np, wave, sys
from timeline import *

SR = 48000
N = int(END * SR)
rng = np.random.default_rng(3)


def tt(d):
    return np.arange(int(d * SR)) / SR


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    # vetorizado por blocos via filtro recursivo simples
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)


def bp(x, lo, hi):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, fc, order=2):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, fc, btype="low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, fc, btype="high", fs=SR, output="sos"), x)


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def add(buf, sig, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    if i < 0:
        sig = sig[-i:]; i = 0
    buf[i:j] += sig[: j - i] * gain


# ---------------- música ----------------
BPM = 100
BEAT = 60 / BPM
BAR = 4 * BEAT
# Fmaj9 | Dm9 | Bbmaj7 | C6  (mais quente)
CHORDS = [
    (41, [53, 57, 60, 64, 67]),   # F
    (50, [50, 57, 60, 64, 65]),   # Dm
    (46, [46, 53, 57, 62, 65]),   # Bb
    (48, [48, 55, 60, 62, 64]),   # C
]


def music():
    L = np.zeros(N); R = np.zeros(N)
    nb = int(np.ceil(END / BAR))
    for b in range(0, nb, 2):
        root, ch = CHORDS[(b // 2) % 4]
        t0 = b * BAR
        d = 2 * BAR + 0.6
        t = tt(d)
        env = np.minimum(1, t / 0.9) * np.minimum(1, np.maximum(0, (d - t) / 0.8))
        pad = np.zeros_like(t)
        for k, m in enumerate(ch):
            f = note(m + 12 if k > 2 else m)
            for det in (-0.12, 0.12):
                ph = rng.uniform(0, 6.28)
                fr = f * 2 ** (det / 12)
                # triângulo suave
                pad += (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * fr * t + ph)) * 0.5
        pad = lp(pad, 1400) * env * 0.035
        add(L, pad, t0); add(R, np.roll(pad, 240), t0)
        # baixo
        bt = tt(2 * BAR)
        bass = np.sin(2 * np.pi * note(root - 12) * bt) * np.minimum(1, bt / 0.05) * np.exp(-bt * 0.6) * 0.09
        add(L, bass, t0); add(R, bass, t0)
        add(L, bass * 0.7, t0 + BAR); add(R, bass * 0.7, t0 + BAR)
        # arpejo em colcheias
        arp = [ch[1], ch[2], ch[3], ch[4], ch[3], ch[2], ch[3], ch[4]]
        for i in range(16):
            tn = t0 + i * BEAT / 2
            if tn > END - 2:
                break
            m = arp[i % 8] + 12
            pt = tt(0.9)
            pl = (np.sin(2 * np.pi * note(m) * pt) + 0.25 * np.sin(4 * np.pi * note(m) * pt)) * np.exp(-pt * 6) * np.minimum(1, pt / 0.004)
            g = 0.030 * (1.0 if i % 2 == 0 else 0.7)
            pan = 0.35 + 0.3 * ((i * 3) % 5) / 4
            add(L, pl, tn, g * (1 - pan) * 2); add(R, pl, tn, g * pan * 2)
    # chimbal leve nos contratempos a partir do 2º compasso
    for i in range(int(END / BEAT)):
        tn = i * BEAT + BEAT / 2
        if tn < BAR * 1 or tn > END - 2.5:
            continue
        n = hp(rng.standard_normal(int(0.05 * SR)), 7000) * np.exp(-tt(0.05) * 90)
        add(L, n, tn, 0.010); add(R, n, tn + 0.004, 0.010)
    # bumbo suave nos tempos 1 e 3
    for i in range(0, int(END / BEAT), 2):
        tn = i * BEAT
        if tn < BAR * 2 or tn > END - 3:
            continue
        kt = tt(0.35)
        f = 52 + 60 * np.exp(-kt * 30)
        k = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-kt * 9) * 0.08
        add(L, k, tn); add(R, k, tn)
    return L, R


# ---------------- efeitos ----------------
def impact_deep():
    t = tt(1.6)
    f = 38 + 85 * np.exp(-t * 7)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    click = lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 40) * 0.6
    return (body + click) * 0.55


def impact_small():
    t = tt(0.7)
    f = 70 + 120 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    tick = bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-t * 120) * 0.5
    return (body + tick) * 0.35


def click(pitch=2200):
    t = tt(0.06)
    s = np.sin(2 * np.pi * pitch * t) * np.exp(-t * 140)
    n = bp(rng.standard_normal(len(t)), 2500, 9000) * np.exp(-t * 300) * 0.4
    return (s + n) * 0.10


def whoosh(d=0.55, lo=300, hi=3500):
    t = tt(d)
    n = rng.standard_normal(len(t))
    # varredura: mistura de duas bandas ao longo do tempo
    a = bp(n, lo, lo * 3)
    b = bp(n, hi / 3, hi)
    x = t / d
    sig = a * (1 - x) + b * x
    env = np.sin(np.pi * x) ** 2
    return sig * env * 0.10


def bell():
    t = tt(1.8)
    s = sum(np.sin(2 * np.pi * f * t) * g * np.exp(-t * dcy) for f, g, dcy in [(880, 1, 2.2), (1320, 0.45, 3.0), (2640, 0.15, 5)])
    return s * np.minimum(1, t / 0.005) * 0.07


def pop():
    t = tt(0.25)
    f = 500 + 900 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18) * 0.10


def thud():
    t = tt(0.35)
    f = 90 + 80 * np.exp(-t * 25)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12) + bp(rng.standard_normal(len(t)), 800, 3000) * np.exp(-t * 80) * 0.3) * 0.22


def sfx():
    L = np.zeros(N); R = np.zeros(N)

    def put(sig, t0, g=1.0, pan=0.5):
        add(L, sig, t0, g * (1 - pan) * 2 ** 0.5); add(R, sig, t0, g * pan * 2 ** 0.5)

    put(whoosh(0.6, 300, 3000), 0.4, 0.45)                # cartão do deserto
    put(whoosh(0.6, 400, 3500), T_ECON - 0.2, 0.45)        # deserto -> mapa
    put(impact_small(), T_EUROPEU - 0.15, 0.7)             # Dinamarca acende
    put(click(2200), T_EXAG - 0.1, 0.8)
    for ts in [S2, S3, S4, S5, S6, S7]:
        put(whoosh(0.5, 250, 2400), ts - 0.15, 0.5)
    put(pop(), S2 + 0.4, 0.5)
    put(whoosh(0.4, 900, 5000), T_VENENO - 0.2, 0.35)      # gota
    put(pop(), T_GILA - 0.2, 0.6)
    put(click(2300), T_HORM - 0.2, 0.6); put(impact_small(), T_GLP - 0.1, 0.6)
    put(whoosh(0.7, 300, 3000), S3 + 0.5, 0.45)             # caneta desliza
    put(click(2100), T_NOVO - 0.2, 0.6); put(pop(), T_SEMA - 0.1, 0.6)
    put(click(2300), T_OZ - 0.15, 0.6); put(click(2500), T_WEG - 0.15, 0.6)
    put(pop(), T_PIB - 0.2, 0.5)
    for v in range(5):
        put(click(1800 + v * 120), T_PREV - 0.6 + v * 0.12, 0.3)
    put(whoosh(0.8, 200, 2000), T_18 - 0.3, 0.4); put(whoosh(0.8, 200, 2400), T_4 - 0.3, 0.5)
    put(impact_small(), T_4 + 0.5, 0.6)
    put(pop(), S5 + 0.5, 0.5); put(click(2200), T_VENDAS - 0.3, 0.6); put(click(2400), T_VENDAS + 0.7, 0.5)
    put(thud(), T_CORTES - 0.3, 0.5); put(click(2000), T_ACORDO - 0.2, 0.5); put(thud(), T_30 - 0.3, 0.5)
    put(pop(), T_ECONOM - 0.2, 0.6); put(click(2300), T_POUCOS - 0.2, 0.6)
    put(pop(), T_SABIA - 0.2, 0.6); put(pop(), T_COMENTA - 0.2, 0.7)
    return L, R


def duck_curve():
    """música abaixa na frase do imposto anual"""
    t = np.arange(N) / SR
    g = np.ones(N)
    # fade in/out da trilha
    g *= np.clip(t / 0.4, 0, 1) * np.clip((END - t) / 2.2, 0, 1)
    return g


def voice():
    w = wave.open("voz48.wav")
    v = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
    out = np.zeros(N)
    mask = np.zeros(N)
    fl = int(0.012 * SR)
    for seg, (a, b) in enumerate(SEG_SRC):
        clip = v[int(a * SR):int(b * SR)].copy()
        clip[:fl] *= np.linspace(0, 1, fl)
        clip[-fl:] *= np.linspace(1, 0, fl)
        add(out, clip, PLACE[seg])
        i0 = int(PLACE[seg] * SR); mask[i0:i0 + len(clip)] = 1
    return out, mask


def voice_duck(mask):
    # música abaixa suavemente enquanto há fala
    k = int(0.25 * SR)
    m = np.convolve(mask, np.ones(k) / k, mode="same")
    return 1 - 0.45 * m


if __name__ == "__main__":
    mL, mR = music()
    g = duck_curve()
    sL, sR = sfx()
    import os
    if os.path.exists("voz48.wav") and PLACE:
        v, mask = voice()
        v = v / (np.abs(v).max() + 1e-9) * 0.95
    else:
        v, mask = np.zeros(N), np.zeros(N)
    gm = g * voice_duck(mask) * 0.55     # música bem abaixo da voz
    L = mL * gm + sL * 0.8 + v
    R = mR * gm + sR * 0.8 + v
    st = np.stack([L, R], 1)
    st /= max(1e-9, np.abs(st).max()) / 0.89
    out = sys.argv[1]
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("ok", out)
