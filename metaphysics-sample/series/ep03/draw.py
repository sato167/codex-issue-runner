"""第 3 集 · 卷三（Β）：先解开绳结。"""
from sketch import *  # noqa: F401,F403


def cup(s, cx, gy, w, h, color, handle=True):
    body = [(cx - w / 2, gy - h), (cx + w / 2, gy - h), (cx + w / 2 - 8, gy), (cx - w / 2 + 8, gy)]
    s.poly(body, 4.0, closed=True)
    s.fill(body, color)
    if handle:
        s.arc(cx + w / 2 + 2, gy - h / 2, 22, h * 0.28, -90, 90, 4.0)


def scene1(s):
    s.begin("cards", (40, 140, 460, 640))
    with s.scaled(0.7, (170, 420)):
        s.aristotle(170, 420)
    s.line((290, 610), (480, 610), 4.0)
    s.line((300, 612), (300, 700), 3.6)
    s.line((470, 612), (470, 700), 3.6)
    for k, x in enumerate((322, 386, 450)):
        s.card(x, 560, 54, 76, CREAM, rot=(-8, 2, 10)[k])
    s.ground(50, 500, 702)

    s.begin("rope", (520, 110, 500, 360))
    s.curve([(540, 330), (600, 300), (660, 320), (720, 300)], 9.0, BROWN)
    s.curve([(720, 300), (760, 240), (820, 250), (812, 310), (760, 330), (740, 280), (800, 260), (850, 300)], 9.0, BROWN)
    s.curve([(850, 300), (900, 330), (950, 300), (1000, 320)], 9.0, BROWN)
    for x in (570, 640, 900, 960):
        s.line((x - 6, 318), (x + 6, 306), 2.4)

    s.begin("untie", (520, 110, 500, 360))
    s.magnifier(790, 280, 70, 40, glass=False)
    s.twinkle(700, 200, 10, ORANGE)
    s.twinkle(880, 190, 12, ORANGE)

    s.begin("road", (1040, 110, 530, 400))
    s.curve([(1150, 480), (1200, 380), (1120, 260), (1080, 200)], 4.0)
    s.curve([(1260, 480), (1300, 380), (1420, 280), (1500, 210)], 4.0)
    s.line((1300, 180), (1300, 450), 4.6)
    for k, (sx, y) in enumerate(((-1, 210), (1, 270))):
        x0 = 1300
        pts = [(x0, y), (x0 + sx * 110, y), (x0 + sx * 136, y + 22), (x0 + sx * 110, y + 44), (x0, y + 44)]
        s.poly(pts, 3.8, closed=True)
        s.fill(pts, YEL)
    s.person(1440, 380, 30, mouth="o", hands=((-36, 20), (14, -40)), body_h=70, shirt=TEAL, legs=False)
    s.qmark(1488, 300, 0.55)

    s.begin("finish", (520, 500, 1050, 300))
    s.line((1300, 770), (1300, 540), 4.6)
    flag = [(1300, 540), (1440, 540), (1440, 630), (1300, 630)]
    s.poly(flag, 4.0, closed=True)
    for i in range(4):
        for j in range(3):
            if (i + j) % 2 == 0:
                s.fill([(1300 + i * 35, 540 + j * 30), (1335 + i * 35, 540 + j * 30),
                        (1335 + i * 35, 570 + j * 30), (1300 + i * 35, 570 + j * 30)], NAVY, 8)
    for k in range(8):
        s.line((900 + k * 60, 770), (930 + k * 60, 770), 3.2, GRAY)
    s.person(1480, 600, 36, eye_style="closed", mouth="smile", hands=((-60, 70), (60, 70)), body_h=110, shirt=CORAL)
    for k in range(3):
        s.line((1540 + k * 10, 640 + k * 26), (1566 + k * 10, 640 + k * 26), 3.0, GRAY)
    s.line((560, 772), (1560, 772), 3.4)


def scene2(s):
    s.begin("icons", (60, 300, 720, 220))
    cube = [(110, 380), (170, 380), (170, 440), (110, 440)]
    s.poly(cube, 4.0, closed=True)
    s.poly([(110, 380), (130, 360), (190, 360), (170, 380)], 3.6)
    s.poly([(170, 440), (190, 420), (190, 360)], 3.6)
    s.fill(cube, "#d9a066")
    bp = [(270, 360), (370, 360), (370, 440), (270, 440)]
    s.poly(bp, 4.0, closed=True)
    s.fill(bp, SKY)
    s.circle(320, 400, 22, 3.0)
    s.line((280, 400), (360, 400), 2.4)
    s.line((320, 366), (320, 434), 2.4)
    s.line((480, 450), (530, 370), 5.0, BROWN)
    head = s.rot_rect(500, 344, 70, 30, 32, (535, 359))
    s.poly(head, 4.0, closed=True)
    s.fill(head, ORANGE, 9)
    for r, c in ((40, CORAL), (26, "#fff4e0"), (12, CORAL)):
        s.circle(680, 400, r, 3.6)
        s.fill_ell(680, 400, r - 2, r - 2, c)

    s.begin("umbrella", (40, 80, 760, 440))
    can = [(90, 320)]
    for k in range(6):
        x0 = 90 + k * 106
        can += s.epts(x0 + 53, 320, 53, 22, 180, 360, n=6)[1:]
    top = s.epts(408, 320, 318, 170, 180, 360, n=24)
    s.curve(top, 4.4)
    s.curve(can, 4.0)
    s.fill(top[1:-1] + can[::-1], TEAL)
    s.line((408, 150), (408, 130), 4.0)
    s.qmark(760, 160, 1.0)

    s.begin("logic", (820, 120, 740, 420))
    cube = [(880, 330), (960, 330), (960, 410), (880, 410)]
    s.poly(cube, 4.0, closed=True)
    s.poly([(880, 330), (906, 304), (986, 304), (960, 330)], 3.6)
    s.poly([(960, 410), (986, 384), (986, 304)], 3.6)
    s.fill(cube, ORANGE)
    for k in range(3):
        s.ell(1080 + k * 80, 360, 50, 30, 4.0)
    s.fill_ell(1080, 360, 46, 26, YEL)
    s.fill_ell(1240, 360, 46, 26, YEL)
    s.arrow((1300, 360), (1380, 360), INK, 4.0, 14)
    for k in range(3):
        x, y = 1430 + (k - 1) * 30, 360 + (14 if k != 1 else -14)
        s.dot(x, y, 9)
    s.qmark(1480, 200, 0.9)

    s.begin("pile", (40, 520, 1540, 280))
    for k in range(13):
        x = 160 + k * 100
        s.card(x, 680 + (k % 3) * 12 - 12, 70, 96, (CREAM, "#ffe6e0", "#e3f2ff")[k % 3], rot=(-10, 4, 12, -4)[k % 4])
    s.person(1480, 560, 30, mouth="grin", hands=((-50, 40), (40, -30)), body_h=60, shirt=YEL, legs=False)


def scene3(s):
    s.begin("cups", (40, 440, 740, 350))
    cup(s, 160, 740, 90, 120, CORAL)
    cup(s, 360, 740, 110, 80, SKY)
    cup(s, 560, 740, 80, 150, GREEN)
    s.line((70, 742), (720, 742), 3.4)

    s.begin("ghost", (40, 70, 740, 420))
    cl = s.cloud(380, 230, 260, 120, 11)
    s.curve(cl + cl[:2], 4.0)
    body = [(340, 180), (420, 180), (412, 280), (348, 280)]
    s.arc(424, 230, 24, 28, -80, 80, 3.6, NAVY)
    for a, b in zip(body, body[1:] + body[:1]):
        for k in range(4):
            t0, t1 = k / 4, k / 4 + 0.14
            s.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 3.6, NAVY)
    s.rays(380, 235, 90, 112, 8, 0, 360, YEL, 4.0)
    for x, y1 in ((160, 610), (360, 650), (560, 580)):
        for k in range(5):
            t0, t1 = k / 5, k / 5 + 0.1
            s.line((380 + (x - 380) * t0, 355 + (y1 - 355) * t0), (380 + (x - 380) * t1, 355 + (y1 - 355) * t1), 3.0, GRAY)

    s.begin("plato", (800, 80, 400, 720))
    with s.scaled(0.78, (960, 330)):
        s.plato(960, 330)
    cl = s.cloud(1090, 150, 100, 52, 8)
    s.curve(cl + cl[:2], 3.8)
    s.circle(1060, 150, 18, 3.4)
    s.fill_ell(1060, 150, 16, 16, YEL)
    tri = [(1104, 132), (1126, 168), (1082, 168)]
    s.poly(tri, 3.4, closed=True)
    s.fill(tri, SKY, 8)

    s.begin("doubt", (1220, 120, 360, 680))
    with s.scaled(0.75, (1400, 360)):
        s.aristotle(1400, 360, ponder=True)
    s.curve([(1440, 300), (1458, 288), (1474, 296)], 3.4)
    for k in range(3):
        s.dot(1500 + k * 22, 250 - k * 26, 5 + k * 2)
    s.line((1240, 642), (1560, 642), 3.4)


def scene4(s):
    s.begin("candle", (40, 100, 500, 400))
    s.candle(170, 440, 150)
    for k in range(2):
        s.curve([(150 + k * 30, 296), (148 + k * 30, 320), (152 + k * 30, 330)], 3.0)
    s.line((260, 330), (300, 330), 4.0, CORAL)
    s.line((300, 330), (288, 320), 4.0, CORAL)
    s.star(410, 260, 60, YEL, 4.2)
    for x, y in ((350, 170), (480, 190), (470, 340)):
        s.twinkle(x, y, 10, ORANGE)

    s.begin("one", (560, 100, 460, 400))
    one = [(760, 200), (800, 170), (800, 400), (840, 400), (840, 420), (740, 420), (740, 400), (780, 400), (780, 214), (760, 226)]
    s.poly(one, 4.4, closed=True)
    s.fill(one, CORAL, 10)
    s.poly([(700, 440), (880, 440), (900, 470), (680, 470)], 4.0, closed=True)
    s.rays(790, 300, 150, 182, 10, 190, 350, YEL, 4.4)

    s.begin("yarn", (1040, 100, 530, 420))
    ball = s.epts(1300, 290, 110, 104, 0, 360, n=36)[:-1]
    s.fill(ball, PINK)
    s.curve(ball + ball[:2], 4.2)
    rnd = random.Random(7)
    for k in range(9):
        a = rnd.uniform(0, 360)
        s.arc(1300 + rnd.uniform(-30, 30), 290 + rnd.uniform(-30, 30), rnd.uniform(50, 90), rnd.uniform(30, 80), a, a + rnd.uniform(120, 220), 3.0)
    s.curve([(1400, 340), (1450, 390), (1430, 420), (1480, 440)], 3.6)

    s.begin("table", (40, 500, 900, 300))
    s.line((80, 700), (860, 700), 4.4)
    s.line((80, 716), (860, 716), 3.4)
    s.line((120, 716), (112, 790), 4.0)
    s.line((820, 716), (828, 790), 4.0)
    for k in range(6):
        s.card(150 + k * 126, 640, 66, 90, (CREAM, "#ffe6e0", "#e3f2ff")[k % 3], rot=(-6, 4, -3, 7, -5, 3)[k])

    s.begin("path", (920, 480, 660, 320))
    s.curve([(960, 790), (1080, 720), (1040, 660), (1180, 620), (1300, 640), (1360, 590)], 4.0)
    s.curve([(1040, 790), (1150, 726), (1110, 676), (1220, 646), (1320, 660), (1390, 600)], 4.0)
    s.curve([(1300, 600), (1420, 540), (1560, 590)], 4.0)
    s.sun(1510, 580, 26, YEL, 8)
    s.line((1390, 600), (1390, 520), 4.0)
    fl = [(1390, 520), (1440, 534), (1390, 550)]
    s.poly(fl, 3.4, closed=True)
    s.fill(fl, CORAL, 8)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
