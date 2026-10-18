"""第 8 集 · 卷八（Η）：质料与形式。"""
from sketch import *  # noqa: F401,F403


def bricks(s, x, y, n=3):
    for row in range(n):
        for i in range(n - row):
            bx = x + i * 64 + row * 32
            by = y - row * 26
            b = [(bx, by), (bx + 60, by), (bx + 60, by + 24), (bx, by + 24)]
            s.poly(b, 3.4, closed=True)
            s.fill(b, "#f4a28c", 8)


def ingot(s, x, y, w=120, h=70):
    blk = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    s.poly(blk, 4.0, closed=True)
    s.poly([(x, y), (x + 28, y - 26), (x + w + 28, y - 26), (x + w, y)], 3.6)
    s.poly([(x + w, y + h), (x + w + 28, y + h - 26), (x + w + 28, y - 26)], 3.6)
    s.fill(blk, BRONZE)


def scene1(s):
    s.begin("equation", (40, 90, 980, 330))
    bricks(s, 80, 300)
    s.line((310, 300), (350, 300), 5.0)
    s.line((330, 280), (330, 320), 5.0)
    sh = [(390, 230), (540, 230), (540, 350), (390, 350)]
    s.poly(sh, 4.0, closed=True)
    s.fill(sh, SKY)
    s.poly([(420, 330), (420, 280), (465, 250), (510, 280), (510, 330)], 3.4, "#ffffff", closed=True)
    s.line((590, 280), (640, 280), 5.0)
    s.line((590, 306), (640, 306), 5.0)
    s.house(820, 370, 200, 140)
    s.ground(680, 980, 372)

    s.begin("diff", (1040, 90, 530, 330))
    for x, c in ((1140, CORAL), (1380, CORAL)):
        body = [(x - 50, 220), (x + 50, 220), (x + 42, 340), (x - 42, 340)]
        s.poly(body, 4.0, closed=True)
        s.fill(body, c)
    s.arc(1192, 280, 22, 34, -90, 90, 4.0)
    s.magnifier(1440, 280, 46, 50, glass=False)
    s.qmark(1260, 180, 0.6, ORANGE)

    s.begin("threshold", (40, 420, 480, 380))
    s.poly([(130, 760), (130, 470), (410, 470), (410, 760)], 4.4)
    door = [(150, 740), (150, 490), (390, 490), (390, 740)]
    s.fill(door, BROWN)
    s.circle(370, 620, 9, 3.2)
    th = [(110, 742), (430, 742), (440, 770), (100, 770)]
    s.poly(th, 4.2, closed=True)
    s.fill(th, YEL, 9)
    s.arrow((480, 700), (444, 750), CORAL, 4.0, 14)

    s.begin("ice", (560, 420, 480, 380))
    drop = [(660, 520), (700, 600), (690, 650), (660, 668), (630, 650), (620, 600)]
    s.curve(drop, 4.0, closed=True)
    s.fill(drop, SKY)
    s.arrow((730, 610), (800, 610), ORANGE, 4.0, 14)
    cube = [(840, 560), (950, 560), (950, 670), (840, 670)]
    s.poly(cube, 4.2, closed=True)
    s.poly([(840, 560), (870, 530), (980, 530), (950, 560)], 3.6)
    s.poly([(950, 670), (980, 640), (980, 530)], 3.6)
    s.fill(cube, "#cfeaff")
    for a in (0, 60, 120):
        t = math.radians(a)
        s.line((895 - 30 * math.cos(t), 615 - 30 * math.sin(t)), (895 + 30 * math.cos(t), 615 + 30 * math.sin(t)), 3.0, SKY)

    s.begin("shelter", (1080, 420, 490, 380))
    bricks(s, 1100, 740, 3)
    s.arrow((1310, 720), (1360, 720), ORANGE, 4.0, 14)
    s.house(1460, 760, 150, 110)
    cl = s.cloud(1460, 470, 90, 34, 8)
    s.curve(cl + cl[:2], 3.8)
    s.fill(cl, GRAY)
    for x in (1400, 1440, 1480, 1520):
        s.line((x, 516), (x - 10, 548), 3.2, SKY)


def scene2(s):
    s.begin("puzzle", (40, 90, 500, 360))
    a = [(90, 200), (230, 200), (230, 250), (260, 250), (260, 290), (230, 290), (230, 340), (90, 340)]
    s.poly(a, 4.0, closed=True)
    s.fill(a, BRONZE)
    b = [(320, 200), (460, 200), (460, 340), (320, 340), (320, 290), (350, 290), (350, 250), (320, 250)]
    s.poly(b, 4.0, closed=True)
    s.fill(b, TEAL)
    s.qmark(290, 120, 0.6)

    s.begin("howone", (560, 90, 520, 360))
    ingot(s, 600, 240, 90, 60)
    cs = s.epts(800, 270, 44, 44, 0, 360, n=16)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.6, TEAL)
    s.arrow((860, 270), (920, 270), GRAY, 3.6, 12)
    s.circle(990, 270, 50)
    s.fill_ell(990, 270, 48, 48, BRONZE)
    s.qmark(990, 150, 0.6)

    s.begin("aristotle", (1120, 100, 450, 700))
    with s.scaled(0.75, (1330, 400)):
        s.aristotle(1330, 400, ponder=True)
    s.bulb(1460, 200, 34)
    s.ground(1140, 1560, 670)

    s.begin("potential", (40, 470, 500, 330))
    ingot(s, 120, 640, 150, 90)
    cs = s.epts(220, 560, 60, 60, 0, 360, n=20)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.6, GRAY)
    s.sprout(400, 760, 70)

    s.begin("actual", (540, 470, 340, 330))
    s.circle(700, 640, 90)
    s.fill_ell(700, 640, 88, 88, BRONZE)
    s.arc(700, 640, 64, 64, 200, 260, 4.6, "#ffffff")
    s.rays(700, 640, 104, 130, 9, 0, 360, YEL, 3.8)

    s.begin("glue", (860, 470, 300, 330))
    bt = [(960, 760), (960, 620), (980, 600), (1020, 600), (1040, 620), (1040, 760)]
    s.poly(bt, 4.0, closed=True)
    s.fill(bt, "#ffffff")
    s.poly([(985, 600), (990, 560), (1010, 560), (1015, 600)], 3.4, closed=True)
    s.fill([(962, 660), (1038, 660), (1038, 720), (962, 720)], YEL, 8)
    s.cross(1000, 680, 1.8)


def scene3(s):
    s.begin("person", (40, 110, 480, 690))
    s.person(260, 300, 70, hair="curly", mouth="smile", hands=((-130, 200), (130, 200)), body_h=300, shirt=None)
    s.ground(80, 460, 720)

    s.begin("soul", (40, 110, 480, 690))
    s.heart(260, 500, 40, CORAL)
    s.rays(260, 500, 60, 90, 10, 0, 360, YEL, 4.0)

    s.begin("eye", (560, 120, 1000, 380))
    s.curve([(600, 300), (660, 230), (780, 230), (840, 300)], 5.0)
    s.curve([(600, 300), (660, 360), (780, 360), (840, 300)], 5.0)
    s.circle(720, 300, 46)
    s.fill_ell(720, 300, 44, 44, SKY)
    s.dot(720, 300, 18)
    for k in (-1, 0, 1):
        dashed(s, [(860, 300 + k * 30), (1200, 300 + k * 70)], YEL, 4.0, closed=False)
    fx, fy = 1320, 320
    for i in range(6):
        t = i * math.pi / 3
        s.circle(fx + 26 * math.cos(t), fy + 26 * math.sin(t), 18, 3.2)
        s.fill_ell(fx + 26 * math.cos(t), fy + 26 * math.sin(t), 16, 16, PINK)
    s.circle(fx, fy, 13, 3.2)
    s.fill_ell(fx, fy, 11, 11, YEL)
    s.curve([(fx, fy + 44), (fx + 6, fy + 100), (fx, fy + 160)], 3.6, GREEN)

    s.begin("stone", (560, 500, 1000, 300))
    head = s.epts(760, 640, 80, 96, 0, 360, n=26)[:-1]
    s.curve(head + head[:1], 4.4)
    s.fill(head, "#dfe3ea")
    for sx in (-1, 1):
        s.ell(760 + sx * 30, 620, 18, 10, 3.6)
    s.line((760, 630), (750, 670), 3.4)
    s.line((740, 690), (780, 690), 3.4)
    ped = [(690, 736), (830, 736), (840, 780), (680, 780)]
    s.poly(ped, 4.0, closed=True)
    s.fill(ped, GRAY)
    for k in range(3):
        s.dot(980 + k * 60, 640, 8)
    s.cross(1300, 640, 1.4)
    s.curve([(1200, 640), (1250, 600), (1350, 600), (1400, 640)], 4.0, GRAY)
    s.curve([(1200, 640), (1250, 680), (1350, 680), (1400, 640)], 4.0, GRAY)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
