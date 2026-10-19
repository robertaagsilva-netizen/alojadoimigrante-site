import numpy as np, wave, re
from phrases import PHRASES as PH, OVERRIDE as OV
def syl(t):
    if t in OV: return OV[t]
    w=re.sub(r"[^\wÀ-ÿ]","",t).lower(); return max(1,len(re.findall(r"[aeiouáéíóúâêôãõà]+",w)))
S=[sum(syl(x) for x in p.split()) for _,p in PH]
w=wave.open('voz48.wav'); v=np.frombuffer(w.readframes(w.getnframes()),np.int16)/32768.
f=480; n=len(v)//f; r=np.sqrt((v[:n*f].reshape(n,f)**2).mean(1))+1e-9; db=20*np.log10(r)
on=db>np.percentile(db,95)-35
segs=[];i=0
while i<n:
  if on[i]:
    j=i
    while j<n and on[j]: j+=1
    segs.append([i/100,j/100]); i=j
  else: i+=1
m=[segs[0]]
for a,b in segs[1:]:
  if a-m[-1][1]<0.18: m[-1][1]=b
  else: m.append([a,b])
m=[x for x in m if x[1]-x[0]>0.05]
K=len(m); P=len(PH)
rate=sum(S)/sum(b-a for a,b in m)
INF=1e9; D=np.full((P+1,K+1),INF); B=np.zeros((P+1,K+1),int); D[0][0]=0
for p in range(1,P+1):
  for k in range(1,K+1):
    for j in range(p-1,k):
      if D[p-1][j]>=INF: continue
      dur=sum(b-a for a,b in m[j:k]); c=(np.log(dur*rate/S[p-1]))**2
      # pausa interna longa penaliza
      gaps=[m[q+1][0]-m[q][1] for q in range(j,k-1)]
      c+=sum(max(0,g-0.45)*2 for g in gaps)
      if D[p-1][j]+c<D[p][k]: D[p][k]=D[p-1][j]+c; B[p][k]=j
k=K; out=[]
for p in range(P,0,-1):
  j=B[p][k]; out.append((m[j][0],m[k-1][1])); k=j
out=out[::-1]
for (s,t),(a,b) in zip(PH,out): print(f"({a:.2f}, {b:.2f}),  # {t[:50]}")
