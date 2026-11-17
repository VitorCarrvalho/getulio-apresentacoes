import sys,numpy as np,potrace
from PIL import Image
def trace(path,scale=4,thr=100):
    im=Image.open(path).convert('RGBA')
    a=np.array(im).astype(float)
    lum=(a[...,0]*.3+a[...,1]*.59+a[...,2]*.11)/255
    m=a[...,3]/255*lum  # white ink
    big=Image.fromarray((m*255).astype('uint8')).resize((im.width*scale,im.height*scale),Image.LANCZOS)
    bm=~(np.array(big)>thr)
    bmp=potrace.Bitmap(bm)
    pl=bmp.trace(turdsize=6,alphamax=1.0,opticurve=True,opttolerance=0.2)
    d=[]
    for c in pl:
        s=c.start_point; d.append(f'M{s.x:.1f} {s.y:.1f}')
        for seg in c.segments:
            if seg.is_corner: d.append(f'L{seg.c.x:.1f} {seg.c.y:.1f}L{seg.end_point.x:.1f} {seg.end_point.y:.1f}')
            else: d.append(f'C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}')
        d.append('Z')
    W,H=big.size
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" fill-rule="evenodd" d="{"".join(d)}"/></svg>'
if __name__=='__main__':
    for p in sys.argv[1:]:
        out='/home/claude/build/assets/'+p.split('/')[-1].replace('.png','.svg')
        open(out,'w').write(trace(p)); print(out)
