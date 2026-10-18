"""《申辩篇》专用道具：马、驴、骡、牛虻、投票陶罐、陪审团、美勒托、女祭司、士兵等。"""
from sketch import *  # noqa: F401,F403


def horse(s, x, y, k=1.0, face=-1, color="#e8c9a0", sleepy=False, ears=1.0):
    """侧面的马（ears>1 变驴/骡），(x, y) 为躯干中心，face=-1 头朝左。"""
    P = lambda u, v: (x + (u if face < 0 else -u) * k, y + v * k)
    body = [P(-110, -10), P(-80, -50), P(40, -54), P(110, -30), P(120, 20), P(80, 50), P(-80, 50), P(-118, 20)]
    s.curve(body, 4.2, closed=True)
    s.fill(body, color)
    neck = [P(-70, -48), P(-104, -100), P(-128, -150), P(-150, -168), P(-176, -170), P(-226, -128), P(-232, -104),
            P(-214, -94), P(-180, -100), P(-150, -110), P(-120, -60), P(-104, -20)]
    s.curve(neck, 4.2)
    s.fill(neck, color)
    for d in (0, 14):
        s.poly([P(-142 - d, -164), P(-136 - d, -164 - 34 * ears), P(-126 - d, -160)], 3.6, closed=True)
        s.fill([P(-142 - d, -164), P(-136 - d, -164 - 34 * ears), P(-126 - d, -160)], color, 6)
    if sleepy:
        s.arc(*P(-176, -140), 11 * k, 7 * k, 20, 160, 3.2)
    else:
        s.dot(*P(-176, -142), 7)
    s.dot(*P(-222, -112), 4)
    s.arc(*P(-214, -96), 10 * k, 6 * k, 200, 320, 2.6)
    if ears < 1.3:
        s.curve([P(-124, -162), P(-100, -130), P(-86, -96), P(-70, -56)], 7.0, BROWN)
    for u in (-80, -50, 60, 90):
        s.line(P(u, 46), P(u + 4, 130), 4.2)
        s.line(P(u + 4, 130), P(u + 14, 132), 4.2)
    s.curve([P(116, -20), P(150, 10), P(150, 70)], 5.0, BROWN)


def gadfly(s, x, y, k=1.0):
    body = s.epts(x, y, 14 * k, 8 * k, 0, 360, n=12)[:-1]
    s.curve(body + body[:1], 3.0)
    s.fill(body, NAVY, 6)
    for sx in (-1, 1):
        w = s.epts(x + sx * 4 * k, y - 12 * k, 10 * k, 14 * k, 0, 360, n=10, rot=sx * 30)[:-1]
        s.curve(w + w[:1], 2.6)
        s.fill(w, "#d7ecff", 6)
    s.dot(x - 14 * k, y - 2 * k, 4)
    for k2 in range(3):
        s.line((x + 20 * k, y + 6 - k2 * 6), (x + 34 * k, y + 6 - k2 * 8), 2.4, GRAY)


def urn(s, cx, gy, h=160, color="#e08d5e"):
    w = h * 0.55
    pts = [(cx - w * 0.3, gy), (cx - w * 0.55, gy - h * 0.35), (cx - w * 0.5, gy - h * 0.7), (cx - w * 0.22, gy - h * 0.85),
           (cx - w * 0.25, gy - h), (cx + w * 0.25, gy - h), (cx + w * 0.22, gy - h * 0.85), (cx + w * 0.5, gy - h * 0.7),
           (cx + w * 0.55, gy - h * 0.35), (cx + w * 0.3, gy)]
    s.curve(pts + [pts[0]], 4.2)
    s.fill(pts, color)
    s.line((cx - w * 0.48, gy - h * 0.5), (cx + w * 0.48, gy - h * 0.5), 2.6, NAVY)


def pebbles(s, cx, gy, n, color, spread=120):
    rnd = random.Random(n)
    for i in range(n):
        row = int(math.sqrt(i * 2))
        x = cx + rnd.uniform(-spread / 2, spread / 2) * (1 - row * 0.08)
        y = gy - 8 - row * 12 + rnd.uniform(-3, 3)
        s.fill_ell(x, y, 8, 6, color)
        s.ell(x, y, 8, 6, 2.2)


def jury(s, x0, y0, cols, rows, dx=60, dy=60, r=18, color=None):
    for j in range(rows):
        for i in range(cols):
            x, y = x0 + i * dx + (j % 2) * dx / 2, y0 + j * dy
            s.circle(x, y, r, 3.0)
            s.curve([(x - r * 1.2, y + r * 2.2), (x - r, y + r * 1.1), (x + r, y + r * 1.1), (x + r * 1.2, y + r * 2.2)], 3.0)
            if color:
                s.fill([(x - r * 1.2, y + r * 2.2), (x - r, y + r * 1.1), (x + r, y + r * 1.1), (x + r * 1.2, y + r * 2.2)], color, 6)


def meletus(s, cx, hy, r=40, hands=((-60, 100), (90, 20)), mouth="flat", look=(1, 0)):
    """美勒托：长头发、稀疏胡子、鹰钩鼻（《游叙弗伦》2b 的描写）。"""
    s.person(cx, hy, r, hair="short", look=look, mouth=mouth, hands=hands, body_h=140, shirt="#b9b3d6", cheeks=False)
    for sx in (-1, 1):
        s.curve([(cx + sx * r * 0.9, hy - r * 0.4), (cx + sx * r * 1.15, hy + r * 0.4), (cx + sx * r * 1.05, hy + r * 1.3)], 3.6, BROWN)
    s.curve([(cx + r * 0.05, hy - r * 0.05), (cx + r * 0.32, hy + r * 0.12), (cx + r * 0.12, hy + r * 0.28)], 3.6)
    for k in range(4):
        s.line((cx - r * 0.3 + k * r * 0.2, hy + r * 0.66), (cx - r * 0.32 + k * r * 0.2, hy + r * 0.78), 2.4)


def pythia(s, cx, gy):
    """德尔斐女祭司坐在三脚鼎上，地缝冒烟。"""
    for sx in (-1, 0, 1):
        s.line((cx + sx * 50, gy), (cx + sx * 20, gy - 110), 4.2)
    bowl = s.epts(cx, gy - 120, 70, 24, 0, 180, n=12)
    s.curve(bowl + [bowl[0]], 4.2)
    s.fill(bowl + [bowl[0]], BRONZE, 9)
    s.person(cx, gy - 230, 34, hair="bun", eye_style="closed", mouth="flat", hands=((-60, 40), (60, 40)), body_h=80, shirt="#ffffff", legs=False)
    s.curve([(cx - 40, gy - 260), (cx - 20, gy - 290), (cx + 20, gy - 290), (cx + 40, gy - 260)], 3.4, GREEN)
    for k in range(3):
        x0 = cx - 120 + k * 20
        s.curve([(x0, gy), (x0 - 16, gy - 40), (x0 + 10, gy - 80), (x0 - 10, gy - 120)], 3.0, GRAY)


def soldier(s, cx, hy, r=36):
    s.person(cx, hy, r, hair="short", mouth="flat", hands=((-50, 90), (70, 60)), body_h=120, shirt=CORAL)
    helm = s.epts(cx, hy - 6, r + 6, r + 4, 180, 360, n=14)
    s.curve(helm + [helm[0]], 4.0)
    s.fill(helm, BRONZE)
    s.curve([(cx - 8, hy - r - 6), (cx - 30, hy - r - 40), (cx + 30, hy - r - 40), (cx + 8, hy - r - 6)], 3.6, CORAL)
    sh = s.epts(cx - 50, hy + 110, 40, 48, 0, 360, n=20)[:-1]
    s.curve(sh + sh[:1], 4.2)
    s.fill(sh, BRONZE)
    s.circle(cx - 50, hy + 110, 12, 3.0)
    s.line((cx + 72, hy - 80), (cx + 72, hy + 200), 4.6, BROWN)
    s.poly([(cx + 64, hy - 80), (cx + 72, hy - 110), (cx + 80, hy - 80)], 3.6, closed=True)


def coin(s, x, y, r=16):
    s.circle(x, y, r, 3.2)
    s.fill_ell(x, y, r - 2, r - 2, YEL)
    s.circle(x, y, r * 0.5, 2.2)


def scroll(s, cx, cy, w=200, h=140, color=CREAM):
    paper = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    s.poly(paper, 3.8, closed=True)
    s.fill(paper, color)
    for x0 in (cx - w / 2, cx + w / 2):
        s.ell(x0, cy, 10, h / 2 + 8, 3.6)
        s.fill_ell(x0, cy, 8, h / 2 + 6, BROWN)


def podium(s, cx, gy, w=160, h=60):
    pts = [(cx - w / 2, gy), (cx - w / 2, gy - h), (cx + w / 2, gy - h), (cx + w / 2, gy)]
    s.poly(pts, 4.0, closed=True)
    s.fill(pts, "#dfe3ea")
    s.line((cx - w / 2 - 14, gy - h), (cx + w / 2 + 14, gy - h), 4.0)


def voice(s, x, y, r=30, present=True):
    """苏格拉底内心的声音：发光的小云。present=False 画成虚线（没出现）。"""
    cl = s.cloud(x, y, r * 1.4, r, 7)
    if present:
        s.curve(cl + cl[:2], 3.4, TEAL)
        s.fill(cl, "#d9f5f1")
        s.rays(x, y, r * 1.7, r * 2.1, 6, 200, 340, TEAL, 3.0)
    else:
        dashed(s, cl, GRAY, 3.0)


def socrates_head(s, cx, cy, r=56):
    """只画苏格拉底的头（秃顶、塌鼻子、蓬胡子），用在篮子里、人群中等位置。"""
    s.circle(cx, cy, r)
    for sx in (-1, 1):
        s.curve([(cx + sx * (r - 2), cy - 4), (cx + sx * (r + 10), cy + 8), (cx + sx * (r + 2), cy + 22)], 3.4)
    s.eyes(cx, cy - 6, r * 0.4, (0, 0), big=True)
    s.ell(cx, cy + r * 0.22, r * 0.28, r * 0.18, 3.4)
    s.dot(cx - r * 0.1, cy + r * 0.23, 3.5)
    s.dot(cx + r * 0.1, cy + r * 0.23, 3.5)
    beard = [(cx - r + 8, cy + r * 0.42), (cx - r * 0.85, cy + r * 1.1), (cx - r * 0.35, cy + r * 1.5), (cx, cy + r * 1.62),
             (cx + r * 0.35, cy + r * 1.5), (cx + r * 0.85, cy + r * 1.1), (cx + r - 8, cy + r * 0.42),
             (cx + r * 0.42, cy + r * 0.64), (cx, cy + r * 0.6), (cx - r * 0.42, cy + r * 0.64)]
    s.curve(beard, 3.8, closed=True)
    s.fill(beard, "#c9ced8")


def laurel(s, cx, cy, r, color=GREEN):
    for sx in (-1, 1):
        pts = s.epts(cx, cy, r, r * 0.6, 270 + sx * 20, 270 + sx * 110, n=6)
        for x, y in pts[1:]:
            lf = s.epts(x, y, 9, 5, 0, 360, n=8, rot=sx * 40)[:-1]
            s.curve(lf + lf[:1], 2.4)
            s.fill(lf, color, 6)


def mask(s, cx, cy, r=34, happy=True, color=YEL):
    face = s.epts(cx, cy, r, r * 1.15, 0, 360, n=20)[:-1]
    s.curve(face + face[:1], 3.6)
    s.fill(face, color)
    for sx in (-1, 1):
        s.arc(cx + sx * r * 0.38, cy - r * 0.2, r * 0.18, r * 0.12, 200 if happy else 20, 340 if happy else 160, 3.2)
    s.arc(cx, cy + r * 0.35, r * 0.4, r * 0.28, 20 if happy else 200, 160 if happy else 340, 3.6)


def steam(s, x, y, r=10):
    """生气时头顶冒的小气团。"""
    for k, (dx, dy) in enumerate(((0, 0), (14, -16), (4, -34))):
        s.circle(x + dx, y + dy, r - k * 2, 2.8, GRAY)


def raised_crowd(s, x0, y0, cols, rows=1, dx=56, dy=70, r=16, color=GRAY):
    """举手的人群（表示“赞成/都认为”）。"""
    for j in range(rows):
        for i in range(cols):
            x, y = x0 + i * dx + (j % 2) * dx / 2, y0 + j * dy
            s.circle(x, y, r, 3.0)
            sh = [(x - r * 1.3, y + r * 2.6), (x - r * 1.1, y + r * 1.2), (x + r * 1.1, y + r * 1.2), (x + r * 1.3, y + r * 2.6)]
            s.curve(sh, 3.0)
            s.fill(sh, color, 6)
            s.curve([(x + r * 0.9, y + r * 1.4), (x + r * 1.6, y + r * 0.2), (x + r * 1.7, y - r * 1.2)], 3.0)
            s.circle(x + r * 1.7, y - r * 1.5, r * 0.32, 2.6)


def big_hand(s, cx, cy, k=1.0, color="#ffd9bf"):
    """手掌朝下的大手（拍东西用）。"""
    P = lambda u, v: (cx + u * k, cy + v * k)
    palm = [P(-70, -40), P(40, -50), P(70, -10), P(60, 40), P(-60, 46), P(-80, 10)]
    s.curve(palm, 4.0, closed=True)
    s.fill(palm, color)
    for i, (u, L) in enumerate(((-52, 60), (-18, 72), (16, 70), (48, 58))):
        f = [P(u - 13, 40), P(u - 12, 40 + L), P(u + 12, 40 + L), P(u + 13, 40)]
        s.curve(f, 3.6)
        s.fill(f, color, 7)
    th = [P(-70, -10), P(-120, 10), P(-126, 34), P(-70, 30)]
    s.curve(th, 3.6)
    s.fill(th, color, 7)
