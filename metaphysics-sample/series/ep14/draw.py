"""第 14 集 · 卷十四（Ν）：数不是万物的原因；全系列收尾。"""
from sketch import *  # noqa: F401,F403

STOPS = [(120, 470), (230, 380), (340, 450), (450, 360), (560, 430), (670, 340), (780, 410), (890, 320),
         (1000, 390), (1110, 300), (1220, 370), (1330, 280), (1440, 340), (1520, 250)]


def scene1(s):
    s.begin("debate", (40, 90, 760, 420))
    with s.scaled(0.55, (180, 250)):
        s.aristotle(180, 250)
    with s.scaled(0.55, (560, 250)):
        s.plato(560, 250, point_up=False)
    s.bubble(320, 140, 70, 44, (250, 200))
    s.qmark(320, 120, 0.45)
    s.bubble(440, 140, 70, 44, (500, 200))
    digit(s, "1", 430, 118, 44, CORAL)
    for k in range(3):
        s.line((360 + k * 14, 210), (372 + k * 14, 226), 3.0, ORANGE)
    s.line((60, 452), (740, 452), 3.4)

    s.begin("pythagoras", (800, 90, 770, 420))
    s.person(940, 260, 44, hair="curly", mouth="smile", hands=((-60, 100), (90, 40)), body_h=150, shirt=SKY)
    tri = [(1040, 320), (1140, 320), (1040, 240)]
    s.poly(tri, 4.0, closed=True)
    s.fill(tri, YEL, 9)
    sq = [(1040, 240), (1040, 320), (960, 320), (960, 240)]
    for (ch, x, y, c) in (("1", 1200, 160, CORAL), ("2", 1300, 230, ORANGE), ("3", 1400, 160, GREEN), ("4", 1480, 260, SKY)):
        digit(s, ch, x, y, 60, c)
    s.tree(1250, 470, 150, GREEN)
    s.fish(1420, 420, 0.9)
    s.line((820, 472), (1550, 472), 3.4)

    s.begin("platonists", (40, 510, 1530, 290))
    one = [(150, 560), (190, 540), (190, 740), (220, 740), (220, 760), (130, 760), (130, 740), (160, 740), (160, 576), (140, 586)]
    s.poly(one, 4.2, closed=True)
    s.fill(one, CORAL, 9)
    s.line((280, 650), (320, 650), 5.0)
    s.line((300, 630), (300, 670), 5.0)
    s.circle(420, 650, 70, 4.0)
    s.fill_ell(420, 650, 68, 68, SKY)
    s.circle(540, 670, 26, 4.0)
    s.fill_ell(540, 670, 24, 24, SKY)
    s.arrow((610, 650), (720, 650), ORANGE, 4.4, 16)
    s.house(830, 760, 120, 80)
    s.tree(990, 760, 160, GREEN)
    cat(s, 1140, 640, "#ffcf99")
    s.star(1300, 620, 34, YEL)
    s.qmark(1420, 600, 0.8)


def scene2(s):
    s.begin("seven", (40, 90, 480, 380))
    digit(s, "7", 120, 160, 200, CORAL, 9.0)
    s.qmark(300, 160, 0.8)
    s.curve([(420, 440), (424, 360), (420, 300)], 3.8, GREEN)
    for i in range(6):
        t = i * math.pi / 3
        s.circle(420 + 22 * math.cos(t), 280 + 22 * math.sin(t), 14, 3.0)
        s.fill_ell(420 + 22 * math.cos(t), 280 + 22 * math.sin(t), 12, 12, PINK)
    s.circle(420, 280, 10, 3.0)

    s.begin("sevens", (540, 90, 1030, 380))
    s.lyre(660, 270, 0.9)
    for k in range(7):
        a = math.radians(200 + k * 22)
        s.star(980 + 110 * math.cos(a) * 0.9, 300 + 80 * math.sin(a), 16, YEL, 3.0)
    s.person(1350, 260, 56, hair="short", mouth="grin", hands=((-70, 110), (70, 110)), body_h=120, shirt=TEAL)
    s.fill([(1336, 270), (1346, 270), (1346, 284), (1336, 284)], "#ffffff", 6)
    s.line((1336, 268), (1336, 284), 2.4)

    s.begin("notcause", (540, 480, 600, 320))
    for k, y in enumerate((540, 640, 740)):
        s.circle(620, y, 20, 3.4)
        s.fill_ell(620, y, 18, 18, (YEL, SKY, TEAL)[k])
        s.arrow((650, y), (850, 640), GRAY, 3.4, 12)
    digit(s, "7", 880, 590, 100, CORAL)
    s.cross(910, 640, 2.2)

    s.begin("measure", (1140, 480, 430, 320))
    rl = [(1180, 600), (1520, 600), (1520, 650), (1180, 650)]
    s.poly(rl, 4.0, closed=True)
    s.fill(rl, YEL, 10)
    for k in range(1, 17):
        s.line((1180 + k * 20, 600), (1180 + k * 20, 625 if k % 5 == 0 else 614), 2.4)
    s.check(1350, 720, 1.0)


def scene3(s):
    s.begin("path", (40, 180, 1530, 360))
    s.curve(STOPS, 6.0, "#e9dcc0")
    s.curve(STOPS, 3.0, BROWN)
    for k, (x, y) in enumerate(STOPS):
        s.circle(x, y, 14, 3.4)
        s.fill_ell(x, y, 12, 12, (CORAL, YEL, SKY, GREEN, PINK, TEAL, ORANGE)[k % 7])

    s.begin("start", (40, 300, 420, 340))
    x, y = STOPS[0][0], STOPS[0][1] + 110
    s.curve([(x - 60, y), (x - 30, y - 30), (x + 30, y - 30), (x + 60, y)], 4.2)
    s.curve([(x - 60, y), (x - 30, y + 30), (x + 30, y + 30), (x + 60, y)], 4.2)
    s.fill_ell(x, y, 20, 20, SKY)
    s.dot(x, y, 10)
    s.person(260, 560, 26, hair="bun", mouth="grin", hands=((-40, 40), (40, -10)), body_h=60, shirt=PINK, legs=False)

    s.begin("middle", (440, 180, 800, 400))
    cube = [(530, 520), (590, 520), (590, 580), (530, 580)]
    s.poly(cube, 4.0, closed=True)
    s.fill(cube, ORANGE, 9)
    s.gear(780, 510, 40, 8, TEAL)
    sd = s.epts(980, 500, 18, 12, 0, 360, n=12, rot=-20)[:-1]
    s.curve(sd + sd[:1], 3.4)
    s.fill(sd, BROWN, 7)
    s.arrow((1006, 500), (1046, 500), ORANGE, 3.4, 10)
    s.tree(1100, 540, 110, GREEN)

    s.begin("end", (1200, 90, 370, 400))
    s.star_glow(1520, 160, 40)
    s.line((1520, 210), (1520, 240), 3.0, ORANGE)


def scene4(s):
    s.begin("night", (0, 0, 1600, 900))
    sky = [(0, 0), (1600, 0), (1600, 610), (0, 610)]
    s.fill(sky, "#3a4f7a", 30)
    outer = s.epts(1300, 180, 64, 64, 60, 300, n=22)
    inner = s.epts(1332, 166, 52, 52, 250, 110, n=18)
    s.curve(outer + inner, 4.2, YEL)
    s.fill(outer + inner, YEL)
    rnd = random.Random(14)
    for k in range(16):
        x, y = rnd.uniform(80, 1520), rnd.uniform(90, 480)
        if abs(x - 1300) < 120 and y < 280:
            continue
        s.star(x, y, rnd.uniform(8, 18), YEL if k % 3 else "#ffffff", 2.6)
    s.curve([(0, 600), (400, 545), (800, 530), (1200, 550), (1600, 600)], 4.2)
    s.fill([(0, 600), (400, 545), (800, 530), (1200, 550), (1600, 600), (1600, 790), (0, 790)], "#bfe6c3", 18)

    s.begin("kid", (380, 300, 840, 500))
    s.person(700, 620, 40, hair="bun", look=(0.3, -1), mouth="o", big_eyes=True, hands=((-70, 40), (60, -50)), body_h=90, shirt=PINK, legs=False)
    with s.scaled(0.55, (900, 560)):
        s.aristotle(900, 560, wave=True)
    for k in range(3):
        s.dot(770 + k * 30, 540 - k * 30, 5 + k)
    s.twinkle(840, 430, 14, YEL)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
