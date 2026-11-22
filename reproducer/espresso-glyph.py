# Original espresso demitasse glyph (1024x1024, white on transparent) in the outline-plus-
# selective-fill style of images/kettle/coffee.png: thick round-cap strokes, solid crema band.
from PIL import Image, ImageDraw
import math
S = 3
im = Image.new('L', (1024*S, 1024*S), 0)
d = ImageDraw.Draw(im)
def P(p): return (p[0]*S, p[1]*S)
def ell(cx, cy, rx, ry, v): d.ellipse(((cx-rx)*S, (cy-ry)*S, (cx+rx)*S, (cy+ry)*S), fill=v)
def bez(p0, p1, p2, p3, n=100):
    return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],
             (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]) for t in [i/n for i in range(n+1)]]
def arc(cx, cy, rx, ry, a0, a1, n=160):
    return [(cx+rx*math.cos(math.radians(a0+(a1-a0)*i/n)), cy+ry*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
def stroke(pts, w, v=255):
    q = [P(p) for p in pts]
    d.line(q, fill=v, width=int(w*S), joint='curve')
    for x, y in (q[0], q[-1]): d.ellipse((x-w*S/2, y-w*S/2, x+w*S/2, y+w*S/2), fill=v)
cx, W = 470, 30
# saucer: thick outline ellipse (front arc heavy) + short underside line
stroke(arc(cx, 760, 330, 70, 0, 360), W)
stroke(bez((cx-250, 850), (cx-120, 890), (cx+120, 890), (cx+250, 850)), 16)
# cup rim (outline) with solid crema band inside
stroke(arc(cx, 440, 215, 56, 0, 360), W)
ell(cx, 446, 150, 28, 255)
# cup body, straight-sided squat demitasse
stroke(bez((cx-215, 450), (cx-215, 620), (cx-150, 735), (cx-70, 748)), W)
stroke([(cx-70, 748), (cx+70, 748)], W)
stroke(bez((cx+70, 748), (cx+150, 735), (cx+215, 620), (cx+215, 450)), W)
# handle
stroke(bez((cx+205, 500), (cx+350, 480), (cx+362, 660), (cx+175, 662)), W)
# steam: three curls
for dx in (-80, 0, 80):
    stroke(bez((cx+dx, 360), (cx+dx-44, 316), (cx+dx+44, 284), (cx+dx, 214)), 22)
a = im.resize((1024, 1024), Image.LANCZOS)
out = Image.new('RGBA', (1024, 1024), (255, 255, 255, 0)); out.putalpha(a)
out.save('espresso.png', optimize=True)
print(a.getbbox())
