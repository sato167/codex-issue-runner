"""第 6 集 · 卷六（Ε）：三门理论学问、偶然、真。"""
from sketch import *  # noqa: F401,F403


def column(s, x, top, bot, w=70):
    s.poly([(x - w / 2 - 14, top), (x + w / 2 + 14, top), (x + w / 2 + 14, top + 22), (x - w / 2 - 14, top + 22)], 3.8, closed=True)
    s.line((x - w / 2, top + 22), (x - w / 2, bot - 22))
    s.line((x + w / 2, top + 22), (x + w / 2, bot - 22))
    for k in (-1, 0, 1):
        s.line((x + k * w * 0.22, top + 40), (x + k * w * 0.22, bot - 40), 2.4, GRAY)
    s.poly([(x - w / 2 - 14, bot - 22), (x + w / 2 + 14, bot - 22), (x + w / 2 + 14, bot), (x - w / 2 - 14, bot)], 3.8, closed=True)


def scene1(s):
    s.begin("aristotle", (40, 140, 400, 650))
    with s.scaled(0.72, (210, 430)):
        s.aristotle(210, 430, wave=True)
    s.ground(60, 400, 690)

    s.begin("ship", (450, 140, 640, 430))
    hull = [(470, 420), (750, 420), (700, 490), (520, 490)]
    s.poly(hull, 4.4, closed=True)
    s.fill(hull, BROWN)
    s.line((610, 420), (610, 200), 4.4)
    sail = [(616, 210), (720, 400), (616, 400)]
    s.poly(sail, 4.0, closed=True)
    s.fill(sail, "#ffffff")
    sail2 = [(604, 240), (500, 400), (604, 400)]
    s.poly(sail2, 4.0, closed=True)
    s.fill(sail2, CORAL)
    for k in range(3):
        xs = [460 + 30 * i for i in range(11)]
        s.curve([(x, 510 + k * 22 + (5 if i % 2 else -5)) for i, x in enumerate(xs)], 3.0, SKY)
    bt = [(880, 300), (980, 300), (990, 500), (870, 500)]
    s.poly(bt, 4.2, closed=True)
    s.fill(bt, "#d7ecff")
    s.poly([(900, 300), (900, 260), (960, 260), (960, 300)], 3.8, closed=True)
    s.line((930, 360), (930, 440), 7.0, CORAL)
    s.line((890, 400), (970, 400), 7.0, CORAL)
    pill = s.epts(1040, 470, 28, 14, 0, 360, n=16, rot=-30)[:-1]
    s.curve(pill + pill[:1], 3.6)
    s.fill(pill, YEL, 8)

    s.begin("knower", (1100, 120, 470, 680))
    s.tree(1450, 700, 300, GREEN)
    s.person(1240, 520, 40, hair="bun", look=(0, 1), mouth="smile", hands=((-40, 96), (40, 96)), body_h=130, shirt=SKY, legs=False)
    s.book(1240, 620, 130, 64, CREAM)
    s.bulb(1240, 360, 34)
    s.heart(1330, 430, 18, PINK)
    s.ground(1110, 1560, 702)


def scene2(s):
    s.begin("pillars", (40, 300, 1520, 500))
    for x in (300, 800, 1300):
        column(s, x, 380, 770)
    s.line((120, 772), (1480, 772), 3.6)

    s.begin("physics", (80, 80, 460, 480))
    s.circle(220, 300, 40)
    s.fill_ell(220, 300, 38, 38, CORAL)
    for k in range(3):
        s.line((120, 280 + k * 20), (164, 280 + k * 20), 3.2, GRAY)
    s.arc(220, 300, 22, 22, 200, 320, 3.0, "#ffffff")
    leaf = s.epts(380, 200, 30, 14, 0, 360, n=14, rot=30)[:-1]
    s.curve(leaf + leaf[:1], 3.4)
    s.fill(leaf, ORANGE, 8)
    s.curve([(380, 140), (360, 160), (390, 180)], 2.8, GRAY)
    for k in range(2):
        xs = [300 + 24 * i for i in range(9)]
        s.curve([(x, 330 + k * 26 + (5 if i % 2 else -5)) for i, x in enumerate(xs)], 3.2, SKY)

    s.begin("math", (590, 80, 420, 480))
    tri = [(650, 330), (780, 330), (715, 210)]
    s.poly(tri, 4.2, closed=True)
    s.fill(tri, SKY)
    s.circle(890, 260, 56)
    s.fill_ell(890, 260, 54, 54, YEL)
    s.line((834, 260), (946, 260), 2.6)
    s.dice(800, 140, 54, 12, "#ffffff", 3)

    s.begin("theology", (1090, 70, 440, 480))
    s.star_glow(1300, 200, 46)
    cl = s.cloud(1300, 330, 150, 40, 9)
    s.curve(cl + cl[:2], 4.0)
    s.fill(cl, "#ffffff")


def scene3(s):
    s.begin("dice", (40, 90, 400, 330))
    s.dice(160, 240, 80, -14, "#ffffff", 5)
    s.dice(300, 290, 70, 22, "#ffe6e0", 3)
    for k in range(3):
        s.arc(230, 260, 120 + k * 16, 90 + k * 12, 200, 250, 3.0, GRAY)

    s.begin("digger", (40, 390, 540, 410))
    s.person(200, 520, 38, hair="short", look=(1, 1), mouth="grin", hands=((80, 70), (110, 120)), body_h=130, shirt=TEAL)
    s.line((270, 570), (360, 740), 5.0, BROWN)
    blade = [(346, 716), (384, 736), (372, 770), (340, 760)]
    s.poly(blade, 3.8, closed=True)
    s.fill(blade, GRAY, 8)
    s.sprout(110, 740, 90)
    s.ground(60, 540, 742)

    s.begin("treasure", (540, 440, 480, 360))
    hole = s.epts(760, 742, 170, 36, 0, 180, n=14)
    s.curve(hole, 4.0)
    s.chest(760, 742, 170, 90)
    s.line((560, 742), (590, 742), 3.4)
    s.line((930, 742), (1000, 742), 3.4)

    s.begin("lucky", (540, 90, 480, 340))
    s.tree(640, 380, 200, GREEN)
    s.check(640, 140, 0.8)
    s.chest(880, 360, 110, 60, open_=False)
    s.dice(960, 220, 56, 16, "#ffffff", 5)
    s.qmark(870, 200, 0.6, ORANGE)

    s.begin("builder", (1040, 90, 520, 470))
    s.person(1200, 300, 40, hair="short", mouth="grin", hands=((40, 110), (110, 70)), body_h=130, shirt=ORANGE)
    helm = s.epts(1200, 280, 46, 34, 180, 360, n=14)
    s.curve(helm + [helm[0]], 4.0)
    s.fill(helm, YEL)
    s.line((1146, 282), (1254, 282), 4.0)
    s.lyre(1360, 370, 0.8)
    s.note(1450, 250, CORAL)
    s.note(1480, 320, SKY)

    s.begin("blueprint", (1040, 560, 520, 240))
    sh = [(1080, 590), (1540, 590), (1540, 780), (1080, 780)]
    s.poly(sh, 4.0, closed=True)
    s.fill(sh, SKY)
    s.poly([(1130, 760), (1130, 680), (1200, 630), (1270, 680), (1270, 760)], 3.6, "#ffffff", closed=True)
    s.lyre(1420, 685, 0.5)
    s.cross(1420, 685, 1.6)


def scene4(s):
    s.begin("random", (40, 90, 500, 360))
    rnd = random.Random(3)
    pts = [(80 + i * 22, 260 + rnd.uniform(-90, 90)) for i in range(19)]
    s.curve(pts, 3.6, GRAY)
    for k in range(4):
        s.dice(120 + k * 110, 200 + rnd.uniform(-60, 120), 44, rnd.uniform(-30, 30), "#ffffff", rnd.choice((1, 3, 5)))

    s.begin("nobook", (40, 440, 500, 360))
    s.line((80, 740), (500, 740), 4.4)
    s.line((80, 560), (500, 560), 3.4)
    x = 100
    for k, (w, c) in enumerate(((40, CORAL), (34, SKY), (46, YEL), (0, None), (38, TEAL), (42, PINK))):
        if c is None:
            gap = [(x, 740), (x, 600), (x + 70, 600), (x + 70, 740)]
            for a, b in zip(gap, gap[1:]):
                for t in range(4):
                    t0, t1 = t / 4, t / 4 + 0.14
                    s.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 3.0, GRAY)
            s.cross(x + 35, 670, 0.7)
            x += 84
            continue
        bk = [(x, 740), (x, 590 + (k % 2) * 16), (x + w, 590 + (k % 2) * 16), (x + w, 740)]
        s.poly(bk, 3.6, closed=True)
        s.fill(bk, c, 9)
        x += w + 8

    s.begin("truth", (560, 90, 500, 360))
    s.bubble(810, 250, 200, 120, (720, 420))
    s.check(810, 250, 2.0)

    s.begin("judge", (560, 420, 560, 380))
    s.person(700, 620, 40, hair="curly", look=(1, -0.5), mouth="smile", hands=((-60, 80), (60, 80)), body_h=110, shirt=YEL, legs=False)
    cl = s.cloud(840, 500, 90, 48, 8)
    s.curve(cl + cl[:2], 3.8)
    s.check(810, 500, 0.6)
    s.cross(880, 500, 0.5)
    s.dot(760, 568, 6)
    s.dot(778, 548, 8)
    s.line((900, 760), (1080, 760), 4.0)
    ap = [(990, 700), (968, 690), (944, 704), (940, 734), (958, 760), (990, 766), (1022, 760), (1040, 734), (1036, 704), (1012, 690)]
    s.curve(ap, 3.8, closed=True)
    s.fill(ap, CORAL)
    s.arrow((900, 560), (970, 670), GRAY, 3.4, 12)

    s.begin("star", (1120, 90, 450, 700))
    s.star_glow(1340, 330, 70)
    cl = s.cloud(1340, 560, 190, 50, 10)
    s.curve(cl + cl[:2], 4.0)
    s.fill(cl, "#ffffff")
    for x, y in ((1180, 180), (1500, 200), (1200, 450), (1490, 460)):
        s.twinkle(x, y, 10, ORANGE)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
