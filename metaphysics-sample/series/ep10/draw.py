"""第 10 集 · 卷十（Ι）：“一”与尺度。"""
from sketch import *  # noqa: F401,F403


def ruler(s, x, y, w, h=40, color=YEL):
    rl = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    s.poly(rl, 4.0, closed=True)
    s.fill(rl, color, 10)
    n = int(w / 20)
    for k in range(1, n):
        s.line((x + k * 20, y), (x + k * 20, y + (h * 0.5 if k % 5 == 0 else h * 0.3)), 2.4)


def balance(s, cx, base_y, left=None, right=None, tilt=0):
    s.poly([(cx - 60, base_y), (cx + 60, base_y), (cx + 40, base_y - 20), (cx - 40, base_y - 20)], 4.0, closed=True)
    s.line((cx, base_y - 20), (cx, base_y - 220), 4.4)
    s.poly([(cx - 10, base_y - 230), (cx, base_y - 250), (cx + 10, base_y - 230)], 3.6, closed=True)
    ly, ry = base_y - 220 + tilt, base_y - 220 - tilt
    s.line((cx - 160, ly), (cx + 160, ry), 4.4)
    for x, y, item in ((cx - 160, ly, left), (cx + 160, ry, right)):
        s.line((x, y), (x - 50, y + 90), 2.6)
        s.line((x, y), (x + 50, y + 90), 2.6)
        pan = s.epts(x, y + 90, 64, 18, 0, 180, n=10)
        s.curve(pan + [pan[0]], 4.0)
        if item:
            item(x, y + 90)


def snowflake(s, cx, cy, r, c=SKY):
    for a in (0, 60, 120):
        t = math.radians(a)
        s.line((cx - r * math.cos(t), cy - r * math.sin(t)), (cx + r * math.cos(t), cy + r * math.sin(t)), 4.0, c)
    for a in range(0, 360, 60):
        t = math.radians(a)
        px, py = cx + r * 0.6 * math.cos(t), cy + r * 0.6 * math.sin(t)
        for d in (-40, 40):
            tt = t + math.radians(d)
            s.line((px, py), (px + r * 0.3 * math.cos(tt), py + r * 0.3 * math.sin(tt)), 3.2, c)


def scene1(s):
    s.begin("one", (40, 110, 380, 380))
    one = [(200, 180), (250, 150), (250, 420), (290, 420), (290, 444), (170, 444), (170, 420), (210, 420), (210, 196), (186, 210)]
    s.poly(one, 4.6, closed=True)
    s.fill(one, CORAL, 10)
    s.rays(230, 300, 150, 180, 9, 190, 350, YEL, 4.0)

    s.begin("ruler", (440, 110, 580, 200))
    ruler(s, 480, 180, 480, 50)

    s.begin("pencil", (440, 110, 580, 340))
    pen = [(520, 340), (840, 340), (880, 360), (840, 380), (520, 380)]
    s.poly(pen, 4.0, closed=True)
    s.fill(pen[:2] + [(840, 380), (520, 380)], ORANGE, 9)
    s.poly([(840, 340), (880, 360), (840, 380)], 3.6, closed=True)
    s.dot(872, 360, 5)
    for x in (520, 840):
        dashed(s, [(x, 236), (x, 330)], GRAY, 3.0, closed=False)

    s.begin("scale", (1040, 90, 530, 390))
    balance(s, 1300, 450,
            left=lambda x, y: s.fill(s.rot_rect(x - 30, y - 50, 60, 50, 0, (x, y)), BROWN, 9) or s.poly(s.rot_rect(x - 30, y - 50, 60, 50, 0, (x, y)), 3.6, closed=True),
            right=lambda x, y: (s.poly([(x - 24, y), (x + 24, y), (x + 16, y - 40), (x - 16, y - 40)], 3.8, closed=True),
                                s.fill([(x - 24, y), (x + 24, y), (x + 16, y - 40), (x - 16, y - 40)], GRAY, 8),
                                s.circle(x, y - 48, 9, 3.4)))

    s.begin("music", (40, 490, 480, 310))
    s.line((180, 760), (180, 640), 5.0)
    s.curve([(150, 540), (150, 600), (180, 640), (210, 600), (210, 540)], 5.0)
    for k in range(3):
        s.arc(180, 560, 50 + k * 22, 50 + k * 22, -40, 40, 3.2, ORANGE)
        s.arc(180, 560, 50 + k * 22, 50 + k * 22, 140, 220, 3.2, ORANGE)
    s.note(360, 640, CORAL)
    s.note(440, 600, SKY)

    s.begin("letters", (540, 490, 520, 310))
    for k, (x, ch) in enumerate(((620, "Α"), (740, "Β"), (860, "Γ"), (980, "Δ"))):
        blk = [(x - 50, 760), (x - 50, 660), (x + 50, 660), (x + 50, 760)]
        s.poly(blk, 4.0, closed=True)
        s.fill(blk, (YEL, SKY, PINK, GREEN)[k], 10)
        if ch == "Α":
            s.poly([(x - 26, 744), (x, 676), (x + 26, 744)], 4.4)
            s.line((x - 14, 716), (x + 14, 716), 4.0)
        elif ch == "Β":
            s.line((x - 18, 676), (x - 18, 744), 4.4)
            s.arc(x - 18, 693, 28, 17, -90, 90, 4.4)
            s.arc(x - 18, 727, 32, 17, -90, 90, 4.4)
        elif ch == "Γ":
            s.poly([(x - 16, 744), (x - 16, 676), (x + 22, 676)], 4.4)
        else:
            s.poly([(x - 28, 744), (x, 676), (x + 28, 744)], 4.4, closed=True)

    s.begin("units", (1080, 490, 490, 310))
    bar = [(1120, 620), (1520, 620), (1520, 670), (1120, 670)]
    s.poly(bar, 4.0, closed=True)
    s.fill(bar, SKY, 10)
    for k in range(1, 8):
        dashed(s, [(1120 + k * 50, 620), (1120 + k * 50, 670)], NAVY, 2.6, closed=False)
    u = [(1120, 720), (1170, 720), (1170, 770), (1120, 770)]
    s.poly(u, 4.0, closed=True)
    s.fill(u, CORAL, 9)
    s.arrow((1180, 745), (1300, 745), GRAY, 3.4, 12)
    s.arc(1145, 600, 26, 18, 200, 340, 3.2, ORANGE)


def scene2(s):
    s.begin("compare", (40, 90, 480, 400))
    balance(s, 280, 440)

    s.begin("same", (540, 90, 520, 380))
    apple(s, 680, 300, 50)
    apple(s, 900, 300, 50)
    s.line((770, 290), (810, 290), 5.0)
    s.line((770, 314), (810, 314), 5.0)

    s.begin("similar", (1080, 90, 490, 380))
    cat(s, 1200, 230, "#ffcf99")
    cat(s, 1420, 230, "#cfd6e2")

    s.begin("different", (40, 480, 480, 320))
    apple(s, 160, 650, 46)
    s.line((280, 640), (330, 640), 5.0, CORAL)
    s.line((280, 664), (330, 664), 5.0, CORAL)
    s.line((318, 614), (292, 690), 5.0, CORAL)
    s.line((400, 720), (450, 600), 6.0, BROWN)
    hd = s.rot_rect(410, 570, 80, 34, 22, (450, 587))
    s.poly(hd, 4.0, closed=True)
    s.fill(hd, GRAY, 9)

    s.begin("opposite", (540, 480, 520, 320))
    s.arrow((700, 640), (600, 640), NAVY, 4.0, 14)
    s.arrow((900, 640), (1000, 640), NAVY, 4.0, 14)
    s.line((700, 640), (900, 640), 4.0)
    s.sun(640, 560, 32, ORANGE, 8)
    snowflake(s, 960, 560, 40)

    s.begin("bw", (1080, 480, 490, 320))
    th = [(1160, 760), (1160, 520), (1200, 520), (1200, 760)]
    s.poly(th, 4.0, closed=True)
    s.fill([(1162, 520), (1198, 520), (1198, 640), (1162, 640)], CORAL, 8)
    s.fill([(1162, 640), (1198, 640), (1198, 758), (1162, 758)], SKY, 8)
    for x0, c in ((1300, NAVY), (1440, None)):
        sq = [(x0, 580), (x0 + 100, 580), (x0 + 100, 680), (x0, 680)]
        s.poly(sq, 4.2, closed=True)
        if c:
            s.fill(sq, "#22304a", 10)
    s.line((1410, 630), (1430, 630), 3.4)


def scene3(s):
    s.begin("onemany", (40, 90, 740, 380))
    s.dot(180, 280, 30)
    s.line((300, 240), (300, 320), 3.4, GRAY)
    rnd = random.Random(5)
    for k in range(18):
        s.dot(400 + rnd.uniform(0, 330), 180 + rnd.uniform(0, 200), 14)

    s.begin("tree", (800, 90, 770, 380))
    s.tree(980, 440, 300, GREEN)
    s.arrow((1110, 300), (1210, 300), ORANGE, 4.0, 14)
    for k in range(5):
        s.tree(1270 + k * 60, 440 - (k % 2) * 20, 160 + (k % 3) * 20, ("#7bd389", "#5cc27a", "#9be0a6")[k % 3])
    s.ground(820, 1560, 442)

    s.begin("forest", (40, 470, 1530, 330))
    for k in range(12):
        x = 120 + k * 120
        s.tree(x, 780, 200 + (k % 3) * 30, YEL if k == 5 else ("#7bd389", "#5cc27a", "#9be0a6")[k % 3])
    s.arrow((720, 520), (720, 580), CORAL, 4.4, 16)
    s.ground(60, 1560, 782)


def scene_one_of(s):
    s.begin("lonely1", (40, 90, 500, 380))
    one = [(240, 180), (280, 156), (280, 380), (310, 380), (310, 400), (220, 400), (220, 380), (250, 380), (250, 196), (230, 206)]
    s.poly(one, 4.4, closed=True)
    s.fill(one, CORAL, 9)
    ring = s.epts(265, 280, 150, 150, 0, 360, n=36)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 3.0, GRAY)
    s.qmark(450, 180, 0.8)

    s.begin("nope10", (1130, 110, 440, 680))
    with s.scaled(0.72, (1360, 420)):
        s.aristotle(1360, 420, wave=True)
    s.line((1170, 680), (1540, 680), 3.4)

    s.begin("color1", (560, 90, 560, 380))
    for k, c in enumerate((SKY, YEL, CORAL, GREEN, PINK)):
        x = 640 + k * 100
        s.circle(x, 280, 36, 3.6)
        s.fill_ell(x, 280, 34, 34, c)
    s.circle(840, 280, 58, 5.0, TEAL)
    s.arrow((840, 180), (840, 214), TEAL, 4.0, 12)

    s.begin("sound1", (40, 480, 520, 320))
    for k in range(5):
        s.line((80, 580 + k * 24), (520, 580 + k * 24), 2.4, GRAY)
    for k, (x, y) in enumerate(((140, 652), (220, 628), (300, 604), (380, 640), (460, 616))):
        s.ell(x, y, 13, 9, 3.2, NAVY if k == 2 else GRAY, rot=-20)
        s.fill_ell(x, y, 12, 8, NAVY if k == 2 else GRAY, rot=-20)
        s.line((x + 12, y - 2), (x + 12, y - 54), 3.0, NAVY if k == 2 else GRAY)
    s.circle(306, 590, 46, 4.4, TEAL)

    s.begin("man1", (560, 480, 560, 320))
    for k in range(5):
        x = 640 + k * 100
        if k == 2:
            s.person(x, 620, 28, hair="bun", mouth="grin", hands=((-40, 50), (40, 50)), body_h=70, shirt=CORAL, legs=False)
        else:
            s.circle(x, 620, 26, 3.0, GRAY)
            s.curve([(x - 26, 720), (x - 22, 660), (x + 22, 660), (x + 26, 720)], 3.0, GRAY)
    s.circle(840, 660, 84, 4.4, TEAL)
    s.line((580, 762), (1100, 762), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene_one_of(s)
    scene3(s)
