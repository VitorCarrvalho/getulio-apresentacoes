import sys,glob
from PIL import Image,ImageDraw
d,pat,out=sys.argv[1],sys.argv[2],sys.argv[3]; cols=int(sys.argv[4]) if len(sys.argv)>4 else 4
fs=sorted(glob.glob(f'{d}/{pat}'))
im=Image.open(fs[0]);tw=600;th=int(im.height*tw/im.width)
for part in range(0,len(fs),20):
  sub=fs[part:part+20];rows=(len(sub)+cols-1)//cols
  S=Image.new('RGB',(cols*(tw+8),rows*(th+30)),(255,0,90))
  for k,f in enumerate(sub):
    x=(k%cols)*(tw+8);y=(k//cols)*(th+30)
    S.paste(Image.open(f).convert('RGB').resize((tw,th)),(x,y+26));ImageDraw.Draw(S).text((x+4,y+6),f.split('/')[-1],fill='white')
  S.save(f'{out}_{part//20+1}.jpg',quality=80);print(f'{out}_{part//20+1}.jpg')
