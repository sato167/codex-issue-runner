"""第 9 集 · 卷九（Θ）：潜能与现实。"""
from sketch import *  # noqa: F401,F403


def dashed_person(s, cx, hy, r, body_h, c=GRAY):
    dashed(s, s.epts(cx, hy, r, r, 0, 360, n=14)[:-1], c, 3.2)
    dashed(s, [(cx - r * 0.5, hy + r), (cx - r * 1.0, hy + r + body_h), (cx + r * 1.0, hy + r + body_h), (cx + r * 0.5, hy + r)], c, 3.2, closed=False)


def seed(s, x, y):
    sd = s.epts(x, y, 22, 15, 0, 360, n=14, rot=-20)[:-1]
    s.curve(sd + sd[:1], 3.8)
    s.fill(sd, BROWN, 8)


def scene1(s):
    s.begin("cards", (1100, 110, 470, 360))
    for x, kind in ((1210, "seed"), (1430, "tree")):
        c = s.rrect(x - 90, 150, 180, 240, 16)
        s.curve(c + c[:1], 4.0)
        s.fill(c, CREAM if kind == "seed" else "#e2f6e4")
        if kind == "seed":
            seed(s, x, 300)
            dashed(s, [(x, 280), (x, 200)], GRAY, 3.0, closed=False)
        else:
            s.tree(x, 360, 180, GREEN)
    s.arrow((1306, 270), (1334, 270), ORANGE, 4.0, 12)

    s.begin("seed", (40, 90, 520, 400))
    s.ground(60, 1060, 460)
    seed(s, 200, 440)
    crown = s.cloud(200, 230, 90, 74, 9)
    dashed(s, crown, GRAY, 3.2)
    dashed(s, [(190, 420), (190, 300)], GRAY, 3.2, closed=False)
    dashed(s, [(210, 420), (210, 300)], GRAY, 3.2, closed=False)

    s.begin("tree", (500, 90, 580, 400))
    s.arrow((310, 400), (520, 400), ORANGE, 4.4, 16)
    s.tree(760, 460, 340, GREEN)
    for k in range(3):
        s.circle(700 + k * 50, 300 - (k % 2) * 30, 10, 3.0)
        s.fill_ell(700 + k * 50, 300 - (k % 2) * 30, 8, 8, CORAL)
    s.rays(760, 260, 170, 196, 9, 190, 350, YEL, 3.6)

    s.begin("kid", (40, 480, 540, 320))
    s.person(160, 680, 28, hair="bun", mouth="grin", hands=((-40, 50), (40, 50)), body_h=60, shirt=PINK)
    dashed_person(s, 380, 560, 38, 160)
    s.arrow((220, 700), (310, 700), ORANGE, 4.0, 14)
    s.line((60, 782), (520, 782), 3.4)

    s.begin("wood", (580, 480, 560, 320))
    log = [(620, 760), (620, 600), (720, 600), (720, 760)]
    s.poly(log, 4.2, closed=True)
    s.fill(log, BROWN)
    s.ell(670, 600, 50, 14, 3.6)
    for k in range(3):
        s.arc(670, 600, 12 + k * 12, 4 + k * 3, 0, 360, 2.4)
    s.arrow((750, 680), (830, 680), ORANGE, 4.0, 14)
    dashed(s, s.epts(940, 560, 30, 30, 0, 360, n=14)[:-1], GRAY, 3.2)
    dashed(s, [(915, 590), (880, 740), (1000, 740), (965, 590)], GRAY, 3.2, closed=False)
    dashed(s, [(860, 740), (1020, 740), (1020, 770), (860, 770)], GRAY, 3.2)
    s.line((600, 782), (1100, 782), 3.4)


def scene2(s):
    s.begin("megara", (40, 100, 420, 420))
    for x, hair, c in ((140, "short", GRAY), (320, "spike", "#b9b3d6")):
        s.person(x, 230, 38, hair=hair, mouth="flat", hands=((-20, 96), (20, 96)), body_h=120, shirt=c)
        s.line((x - 40, 330), (x + 40, 330), 4.0)
    s.ground(60, 420, 432)

    s.begin("building", (480, 90, 540, 380))
    s.person(600, 230, 36, hair="short", look=(1, 0.5), mouth="grin", hands=((-50, 90), (100, 90)), body_h=120, shirt=ORANGE)
    helm = s.epts(600, 212, 42, 30, 180, 360, n=14)
    s.curve(helm + [helm[0]], 4.0)
    s.fill(helm, YEL)
    for row in range(3):
        for i in range(4 - row):
            bx, by = 740 + i * 64 + row * 32, 410 - row * 26
            b = [(bx, by), (bx + 60, by), (bx + 60, by + 24), (bx, by + 24)]
            s.poly(b, 3.4, closed=True)
            s.fill(b, "#f4a28c", 8)
    s.line((500, 436), (1000, 436), 3.4)

    s.begin("resting", (480, 480, 540, 320))
    s.person(640, 640, 36, hair="short", eye_style="closed", mouth="flat", hands=((-50, 80), (50, 80)), body_h=90, shirt=ORANGE, legs=False)
    helm = s.epts(640, 622, 42, 30, 180, 360, n=14)
    s.curve(helm + [helm[0]], 4.0)
    s.fill(helm, YEL)
    for k, (x, y, sz) in enumerate(((720, 580, 16), (760, 540, 22), (810, 490, 28))):
        s.poly([(x, y), (x + sz, y), (x, y + sz), (x + sz, y + sz)], 3.4, SKY)
    s.qmark(900, 600, 0.7)
    s.line((500, 772), (1000, 772), 3.4)

    s.begin("aristotle", (40, 470, 420, 330))
    with s.scaled(0.55, (230, 560)):
        s.aristotle(230, 560, wave=True)
    s.line((80, 760), (400, 760), 3.4)

    s.begin("blink", (1040, 90, 530, 710))
    s.person(1300, 330, 70, hair="curly", eye_style="closed", mouth="o", hands=((-120, 190), (120, 190)), body_h=230, shirt=TEAL)
    for k, (x, closed) in enumerate(((1120, False), (1220, True), (1320, False), (1420, True))):
        y = 160
        if closed:
            s.arc(x, y, 26, 12, 20, 160, 3.6)
        else:
            s.curve([(x - 30, y), (x - 14, y - 16), (x + 14, y - 16), (x + 30, y)], 3.4)
            s.curve([(x - 30, y), (x - 14, y + 16), (x + 14, y + 16), (x + 30, y)], 3.4)
            s.dot(x, y, 10)
    s.qmark(1500, 330, 0.8)
    s.line((1460, 400), (1464, 440), 6.0, CORAL)
    s.dot(1466, 460, 7)


def scene3(s):
    s.begin("order", (40, 90, 540, 380))
    s.person(170, 220, 40, hair="short", mouth="smile", hands=((-60, 100), (64, 100)), body_h=150, shirt=SKY)
    s.person(400, 320, 26, hair="bun", mouth="grin", hands=((-40, 50), (40, 50)), body_h=60, shirt=PINK)
    s.arrow((260, 200), (360, 260), ORANGE, 4.0, 14)
    s.ground(60, 520, 452)

    s.begin("master", (600, 90, 520, 380))
    s.person(700, 220, 38, hair="curly", mouth="smile", hands=((-56, 100), (90, 40)), body_h=140, shirt=ORANGE)
    s.person(940, 280, 28, hair="short", look=(-1, 0), mouth="o", hands=((-40, 60), (40, 60)), body_h=90, shirt=TEAL)
    sh = [(790, 220), (880, 200), (890, 270), (800, 290)]
    s.poly(sh, 3.6, closed=True)
    s.fill(sh, SKY, 9)
    s.poly([(815, 270), (815, 240), (840, 222), (865, 236), (866, 264)], 2.8, "#ffffff")
    s.ground(620, 1100, 452)

    s.begin("chickegg", (40, 480, 1080, 320))
    s.chicken(260, 680, 1.0, 1)
    s.check(260, 540, 0.9)
    s.arrow((400, 680), (560, 680), ORANGE, 4.4, 16)
    egg = s.epts(680, 690, 52, 66, 0, 360, n=22)[:-1]
    s.curve(egg + egg[:1], 4.2)
    s.fill(egg, CREAM)
    s.poly([(640, 690), (660, 674), (676, 696), (694, 672), (716, 692)], 3.2)
    s.line((100, 776), (800, 776), 3.4)

    s.begin("goal", (1140, 100, 430, 680))
    for r, c in ((150, CORAL), (100, "#fff4e0"), (50, CORAL)):
        s.circle(1360, 430, r, 4.0)
        s.fill_ell(1360, 430, r - 2, r - 2, c)
    s.arrow((1180, 230), (1352, 424), NAVY, 5.0, 20)
    s.sprout(1200, 280, 60)


def scene4(s):
    s.begin("ring", (40, 90, 520, 380))
    pts = s.epts(280, 280, 140, 140, -60, 250, n=30)
    s.curve(pts, 7.0, TEAL)
    s.arrow(pts[-3], pts[-1], TEAL, 7.0, 22)
    s.star(280, 280, 44, YEL)

    s.begin("seeing", (580, 90, 540, 380))
    s.curve([(620, 280), (670, 220), (770, 220), (820, 280)], 4.6)
    s.curve([(620, 280), (670, 340), (770, 340), (820, 280)], 4.6)
    s.circle(720, 280, 40)
    s.fill_ell(720, 280, 38, 38, SKY)
    s.dot(720, 280, 16)
    dashed(s, [(840, 280), (950, 280)], YEL, 4.0, closed=False)
    s.sun(1030, 280, 36, YEL, 8)
    s.check(720, 150, 0.9)

    s.begin("living", (40, 480, 700, 320))
    s.person(240, 610, 40, hair="bun", mouth="grin", hands=((-70, 30), (70, 30)), body_h=110, shirt=YEL)
    s.heart(380, 560, 26, CORAL)
    s.bulb(480, 600, 28)
    s.sun(600, 560, 30, ORANGE, 8)
    s.line((80, 782), (700, 782), 3.4)

    s.begin("halfhouse", (740, 480, 830, 320))
    wall = [(900, 770), (900, 640), (1160, 640), (1160, 770)]
    s.poly(wall, 4.2)
    for row in range(4):
        for i in range(4 if row < 2 else 2):
            bx, by = 904 + i * 64, 744 - row * 26
            b = [(bx, by), (bx + 60, by), (bx + 60, by + 24), (bx, by + 24)]
            s.poly(b, 3.0, closed=True)
            s.fill(b, "#f4a28c", 8)
    for x in (880, 1180):
        s.line((x, 780), (x, 560), 3.6, BROWN)
    s.line((870, 600), (1190, 600), 3.6, BROWN)
    s.line((1300, 780), (1300, 520), 4.4)
    s.line((1300, 520), (1480, 520), 4.4)
    s.line((1460, 520), (1460, 600), 3.0)
    hg = [(1430, 600), (1490, 600), (1460, 640)]
    s.poly(hg, 3.4, closed=True)
    s.fill(hg, YEL, 8)
    s.poly([(1430, 680), (1490, 680), (1460, 640)], 3.4, closed=True)
    s.line((760, 782), (1560, 782), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
