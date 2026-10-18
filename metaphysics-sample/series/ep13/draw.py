"""第 13 集 · 卷十三（Μ）：数学对象在哪里。"""
from sketch import *  # noqa: F401,F403


def wheel(s, cx, cy, r, rim=BROWN, spokes=8):
    s.circle(cx, cy, r, 5.0)
    s.circle(cx, cy, r * 0.82, 3.4)
    ring = s.epts(cx, cy, r, r, 0, 360, n=30)[:-1] + s.epts(cx, cy, r * 0.82, r * 0.82, 360, 0, n=30)[1:]
    s.fill(ring, rim, 9)
    s.circle(cx, cy, r * 0.14, 3.4)
    for k in range(spokes):
        t = math.radians(k * 360 / spokes)
        s.line((cx + r * 0.14 * math.cos(t), cy + r * 0.14 * math.sin(t)), (cx + r * 0.82 * math.cos(t), cy + r * 0.82 * math.sin(t)), 3.2)


def scene1(s):
    s.begin("float", (40, 90, 780, 380))
    for (ch, x, y, h, c) in (("7", 120, 200, 60, SKY), ("2", 300, 300, 50, CORAL), ("5", 640, 180, 56, GREEN)):
        digit(s, ch, x, y, h, c)
    s.circle(480, 230, 34, 4.0)
    sq = [(200, 360), (260, 360), (260, 420), (200, 420)]
    s.poly(sq, 4.0, closed=True)
    s.fill(sq, YEL, 9)
    s.poly([(560, 420), (620, 420), (590, 360)], 4.0, closed=True)
    s.qmark(740, 320, 0.8)

    s.begin("three", (840, 90, 730, 380))
    digit(s, "3", 900, 160, 200, CORAL, 9.0)
    s.circle(1200, 260, 90, 5.0)
    s.fill_ell(1200, 260, 88, 88, YEL)
    tri = [(1340, 360), (1540, 360), (1440, 170)]
    s.poly(tri, 5.0, closed=True)
    s.fill(tri, SKY)

    s.begin("where", (40, 480, 1530, 320))
    g = s.epts(800, 650, 120, 120, 0, 360, n=30)[:-1]
    s.fill(g, "#d7ecff", 14)
    s.curve(g + g[:2], 4.4)
    s.ell(800, 650, 120, 40, 2.8)
    s.ell(800, 650, 50, 120, 2.8)
    pin = [(800, 560)] + s.epts(800, 500, 32, 32, 150, 390, n=14)
    s.curve(pin + [(800, 560)], 4.0)
    s.fill(pin, CORAL)
    s.circle(800, 500, 10, 3.0)
    s.qmark(980, 560, 0.9)
    s.qmark(600, 560, 0.7, ORANGE)


def scene2(s):
    s.begin("plato", (40, 80, 540, 720))
    with s.scaled(0.78, (230, 400)):
        s.plato(230, 400)
    s.line((70, 700), (420, 700), 3.4)

    s.begin("perfect", (560, 80, 560, 380))
    cl = s.cloud(820, 200, 230, 100, 11)
    s.curve(cl + cl[:2], 4.0)
    s.circle(740, 200, 46, 4.0)
    s.fill_ell(740, 200, 44, 44, YEL)
    s.poly([(860, 240), (940, 240), (900, 160)], 4.0, closed=True)
    s.fill([(860, 240), (940, 240), (900, 160)], SKY, 9)
    s.rays(820, 200, 250, 274, 10, 0, 360, YEL, 3.2)
    rnd = random.Random(2)
    wob = [(820 + (42 + rnd.uniform(-6, 6)) * math.cos(t), 410 + (42 + rnd.uniform(-6, 6)) * math.sin(t))
           for t in [i * 2 * math.pi / 10 for i in range(10)]]
    s.curve(wob, 3.4, GRAY, closed=True)
    dashed(s, [(820, 360), (820, 310)], GRAY, 3.0, closed=False)

    s.begin("aristotle", (1130, 110, 440, 690))
    with s.scaled(0.72, (1350, 400)):
        s.aristotle(1350, 400, ponder=True)
    s.line((1170, 662), (1530, 662), 3.4)

    s.begin("inthings", (560, 480, 290, 320))
    apple(s, 700, 650, 70)
    ring = s.epts(700, 650, 96, 96, 0, 360, n=30)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 3.6, TEAL)

    s.begin("pull", (840, 480, 290, 320))
    head = s.epts(1000, 640, 60, 66, 0, 360, n=24)[:-1]
    s.curve(head + head[:1], 4.2)
    s.dot(1020, 630, 6)
    s.arc(1016, 660, 14, 8, 20, 160, 3.2)
    s.arrow((900, 650), (950, 650), ORANGE, 4.0, 12)
    s.circle(1060, 540, 26, 4.0, TEAL)
    s.arrow((1010, 590), (1040, 566), TEAL, 3.4, 10)


def scene3(s):
    s.begin("wheel", (40, 90, 500, 380))
    wheel(s, 280, 280, 150)
    ring = s.epts(280, 280, 170, 170, 0, 360, n=36)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 4.0, TEAL)

    s.begin("materials", (560, 90, 560, 380))
    wheel(s, 700, 280, 90, BROWN)
    wheel(s, 980, 280, 90, GRAY)
    s.line((820, 270), (860, 270), 5.0)
    s.line((820, 294), (860, 294), 5.0)

    s.begin("apples", (1140, 90, 430, 380))
    for k in range(3):
        apple(s, 1200 + k * 80, 250 + (k % 2) * 30, 34)
    s.arrow((1240, 340), (1300, 400), ORANGE, 4.0, 12)
    digit(s, "3", 1340, 360, 90, CORAL, 7.0)

    s.begin("distill", (40, 480, 1530, 320))
    s.tree(160, 760, 180, GREEN)
    s.house(320, 760, 120, 80)
    cat(s, 470, 640, "#ffcf99")
    fun = [(620, 560), (900, 560), (790, 680), (790, 740), (730, 740), (730, 680)]
    s.poly(fun, 4.4, closed=True)
    s.fill(fun, "#d7ecff")
    s.arrow((560, 620), (640, 600), ORANGE, 4.0, 12)
    s.arrow((800, 750), (980, 700), ORANGE, 4.0, 14)
    s.circle(1060, 680, 40, 4.0)
    s.fill_ell(1060, 680, 38, 38, YEL)
    tri = [(1140, 720), (1220, 720), (1180, 640)]
    s.poly(tri, 4.0, closed=True)
    s.fill(tri, SKY, 9)
    digit(s, "3", 1260, 630, 80, CORAL)
    digit(s, "7", 1330, 630, 80, GREEN)
    s.rays(1200, 680, 210, 236, 8, 200, 340, YEL, 3.4)


def scene_doubled(s):
    s.begin("socq", (40, 90, 460, 700))
    with s.scaled(0.8, (230, 380)):
        socrates(s, 230, 380)
    s.qmark(400, 180, 0.7)
    sh = [(340, 270), (400, 270), (400, 320), (370, 350), (340, 320)]
    s.poly(sh, 3.8, closed=True)
    s.fill(sh, SKY, 8)
    s.line((450, 260), (450, 340), 3.4)
    s.line((420, 280), (480, 280), 3.4)
    for x in (420, 480):
        pan = s.epts(x, 300, 16, 6, 0, 180, n=6)
        s.curve(pan + [pan[0]], 3.0)
    s.line((70, 672), (420, 672), 3.4)

    s.begin("nosep", (520, 90, 560, 380))
    cl = s.cloud(800, 260, 200, 100, 10)
    s.curve(cl + cl[:2], 4.0)
    s.circle(740, 260, 34, 3.6)
    s.poly([(830, 290), (890, 290), (860, 230)], 3.6, closed=True)
    s.cross(800, 260, 2.6)

    s.begin("scissors", (520, 480, 560, 320))
    for k, (x, c) in enumerate(((590, CORAL), (670, SKY))):
        cupp = [(x - 26, 700), (x + 26, 700), (x + 20, 760), (x - 20, 760)]
        s.poly(cupp, 3.6, closed=True)
        s.fill(cupp, c, 8)
    s.line((550, 762), (720, 762), 3.4)
    cs = s.epts(1000, 540, 40, 40, 0, 360, n=16)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.2, GRAY)
    dashed(s, [(680, 690), (960, 560)], GRAY, 3.0, closed=False)
    with s.scaled(2.2, (820, 640)):
        for sx in (-1, 1):
            s.circle(820 + sx * 16, 660, 13, 3.6)
            s.line((820 + sx * 10, 648), (812 - sx * 26, 590), 4.4)
        s.fill_ell(804, 660, 11, 11, ORANGE)
        s.fill_ell(836, 660, 11, 11, ORANGE)
    s.rays(820, 620, 30, 50, 4, 200, 340, CORAL, 3.4)

    s.begin("double", (1100, 90, 470, 700))
    s.person(1220, 300, 38, hair="spike", mouth="o", hands=((-50, 100), (60, 110)), body_h=120, shirt=YEL)
    s.sweat(1268, 270)
    for k in range(3):
        apple(s, 1170 + k * 50, 560, 20)
    s.arrow((1310, 560), (1370, 560), ORANGE, 4.0, 12)
    for k in range(6):
        apple(s, 1400 + (k % 3) * 50, 540 + (k // 3) * 50, 20)
    s.qmark(1480, 420, 0.7)
    s.line((1120, 640), (1560, 640), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene_doubled(s)
    scene3(s)
