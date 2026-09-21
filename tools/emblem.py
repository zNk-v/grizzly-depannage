from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from collections import deque
X0,Y0=330,20; W=580
src=Image.open('assets/img/logo-src.png').convert('RGB').crop((X0,Y0,X0+W,Y0+W))
A=np.asarray(src).astype(float); lum=A.mean(axis=2); Rr,Gg,Bb=A[...,0],A[...,1],A[...,2]
head=np.load('tools/head-mask.npy')
CUT=330; cx,cy,R,RW=268,300,222,18
yy,xx=np.mgrid[0:W,0:W]
N4=((1,0),(-1,0),(0,1),(0,-1))
def lab(m):
    L=np.zeros(m.shape,int); sizes=[0]; n=0; Hh,Ww=m.shape
    for y0,x0 in zip(*np.nonzero(m)):
        if L[y0,x0]: continue
        n+=1; q=deque([(y0,x0)]); L[y0,x0]=n; c=0
        while q:
            y,x=q.popleft(); c+=1
            for dy,dx in N4:
                ny,nx=y+dy,x+dx
                if 0<=ny<Hh and 0<=nx<Ww and m[ny,nx] and not L[ny,nx]: L[ny,nx]=n; q.append((ny,nx))
        sizes.append(c)
    return L,np.array(sizes)
# 1) peel: from outside, remove every non-dark pixel (yellow sticker, light specks) until the bear's black outline
outside=~head; outside[CUT-2:]=False
dist=np.full((W,W),99); q=deque()
for y,x in zip(*np.nonzero(outside)): dist[y,x]=0; q.append((y,x))
while q:
    y,x=q.popleft()
    if dist[y,x]>=11: continue
    for dy,dx in N4:
        ny,nx=y+dy,x+dx
        if 0<=ny<CUT-2 and 0<=nx<W and dist[ny,nx]==99 and head[ny,nx] and (lum[ny,nx]>=62 or dist[y,x]<3):
            dist[ny,nx]=dist[y,x]+1; q.append((ny,nx))
matte=head & ~((dist>0)&(dist<99))
# 2) keep main blob, fill holes
L,sz=lab(matte); matte=L==(np.argmax(sz[1:])+1)
Lb,_=lab(~matte); matte=~(Lb==Lb[0,0])
# 3) smooth at 2x + anti-aliasing (no recolouring of the bear)
S=2; W2=W*S
def blf(m,r): return np.asarray(Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r))).astype(float)/255
m2=np.asarray(Image.fromarray((matte*255).astype('uint8')).resize((W2,W2),Image.LANCZOS)).astype(float)/255>0.5
m2=blf(m2,2.2)>0.5            # smooth ragged edges
m2=blf(m2,0.1)>0.5
raw=np.asarray(Image.fromarray((matte*255).astype('uint8')).resize((W2,W2),Image.NEAREST))>127
# the smoothing must never bring back pixels the matte had excluded (yellow between fur spikes)
m2&=raw
A2u=np.asarray(src.resize((W2,W2),Image.LANCZOS)).astype(float)
yel=(A2u[...,0]>120)&(A2u[...,2]<0.45*A2u[...,0])&(A2u[...,1]>0.6*A2u[...,0])
e2=m2.copy()
for _ in range(12):
    t=e2.copy(); t[1:]&=e2[:-1]; t[:-1]&=e2[1:]; t[:,1:]&=e2[:,:-1]; t[:,:-1]&=e2[:,1:]; e2=t
Y2,X2=np.mgrid[0:W2,0:W2]
pawbox=(X2>370)&(X2<580)&(Y2<250)
edge_yel=yel&~e2&(Y2<CUT*2-34)&~pawbox
m2&=~edge_yel
m2&=~(yel&(X2<262)&(Y2>540)&(Y2<700))
# erode 1px (2x) so the edge sits inside the black outline
e=m2.copy(); e[1:]&=m2[:-1]; e[:-1]&=m2[1:]; e[:,1:]&=m2[:,:-1]; e[:,:-1]&=m2[:,1:]; m2=e
alpha_head=blf(m2,0.7)
# 4) artwork at 2x, untouched for the bear; background clean-up only outside the bear
art=np.asarray(src.resize((W2,W2),Image.LANCZOS)).astype(float)
yy2,xx2=np.mgrid[0:W2,0:W2]; CUT2,cx2,cy2,R2,RW2=CUT*S,cx*S,cy*S,R*S,RW*S
BLACK=np.array([5,5,6.])
lowbg=np.zeros((W2,W2))
# yellow splatter in the lower background (big pure yellow blobs outside the body)
A2=art; y2=(A2[...,0]>170)&(A2[...,1]>120)&(A2[...,2]<70)&(A2[...,1]>0.66*A2[...,0])&(((yy2>=CUT2-10))|((xx2>700)&(yy2>=565)))&~((xx2>280)&(xx2<720)&(yy2<780))
Ly,szy=lab(y2); lowbg=np.maximum(lowbg,((szy<1200)[Ly]&y2).astype(float))
# grey car on the left
mx=A2.max(axis=2); mn=A2.min(axis=2); lc=A2.mean(axis=2)
grey=((mx-mn)<38)&(lc>28)&(xx2<330)&(yy2>=CUT2-60)&(yy2<900)&~m2
Lg,_=lab(grey); touch=np.unique(Lg[:, :230][Lg[:, :230]>0]); lowbg=np.maximum(lowbg,blf(np.isin(Lg,touch),2)>0.2)
ox,oy=cx2-447,cy2-518
poly=[(0,470),(112,470),(168,535),(214,598),(204,650),(194,705),(166,740),(120,752),(0,752)]
pm=Image.new('L',(W2,W2),0); ImageDraw.Draw(pm).polygon([(x+ox,y+oy) for x,y in poly],fill=255)
lowbg=np.maximum(lowbg,np.asarray(pm.filter(ImageFilter.GaussianBlur(1.5))).astype(float)/255)
lowbg*=(1-alpha_head)
lower=art*(1-lowbg[...,None])+BLACK*lowbg[...,None]
# 5) compose
SS=3
def circ(r):
    m=Image.new('L',(W2*SS,W2*SS),0); ImageDraw.Draw(m).ellipse(((cx2-r)*SS,(cy2-r)*SS,(cx2+r)*SS,(cy2+r)*SS),fill=255)
    return np.asarray(m.resize((W2,W2),Image.LANCZOS)).astype(float)/255
disc=circ(R2); inner=circ(R2-RW2)
rgb=np.tile(BLACK,(W2,W2,1)); a=disc.copy()
lowmask=((yy2>=CUT2-8)|((xx2>700)&(yy2>=575))).astype(float)*inner
rgb=rgb*(1-lowmask[...,None])+lower*lowmask[...,None]
hin=alpha_head*inner
rgb=rgb*(1-hin[...,None])+art*hin[...,None]
ring=np.clip(disc-inner,0,1)
rgb=rgb*(1-ring[...,None])+np.array([251,194,12.])*ring[...,None]
# head in front of the ring: ears + cap only (angular window free of the cheeks)
d2=np.sqrt((xx2-cx2)**2+(yy2-cy2)**2); rb=(d2>=R2-RW2-3)&(d2<=R2+3)
ang=np.degrees(np.arctan2(xx2-cx2,-(yy2-cy2)))
lim={}
for side in (1,-1):
    for a0 in range(20,100):
        if not (m2&rb&(np.abs(ang-side*a0)<0.6)).any(): lim[side]=a0; break
front=(((ang>=0)&(ang<lim[1]))|((ang<0)&(ang>-lim[-1])))&(yy2<cy2)
hf=alpha_head*front
rgb=rgb*(1-hf[...,None])+art*hf[...,None]
a=np.maximum(a,hf)
out=Image.fromarray(np.dstack([np.clip(rgb,0,255),np.clip(a*255,0,255)]).astype('uint8'))
bbox=out.getbbox(); out=out.crop(bbox)
out.save('assets/img/emblem-3d.webp',quality=94,method=6)
bg=Image.new('RGBA',out.size,(10,10,11,255)); bg.alpha_composite(out); pass
print(out.size,'center',cx2-bbox[0],cy2-bbox[1],'lim',lim)
