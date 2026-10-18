"""第 7 集 · 卷七（Ζ）：什么是实体。"""
from sketch import *  # noqa: F401,F403

BRONZE = "#c98a4b"


def scene1(s):
    s.begin("aristotle", (40, 120, 440, 680))
    with s.scaled(0.72, (210, 440)):
        s.aristotle(210, 440, ponder=True)
    s.qmark(330, 240, 1.0)
    s.ground(60, 420, 700)

    s.begin("cat", (470, 160, 560, 640))
    cone = [(760, 180), (600, 790), (920, 790)]
    s.fill(cone, "#fff1b0", 16)
    cat(s, 760, 520)
    s.line((520, 792), (1000, 792), 3.4)
    s.arrow((560, 300), (660, 420), CORAL, 4.4, 16)

    s.begin("attrs", (980, 120, 590, 680))
    pal = s.epts(1260, 260, 60, 44, 0, 360, n=20)[:-1]
    s.curve(pal + pal[:1], 3.8)
    for (dx, dy, c) in ((-26, -10, CORAL), (0, -20, YEL), (26, -8, SKY), (10, 16, GREEN)):
        s.fill_ell(1260 + dx, 260 + dy, 10, 10, c)
    rl = [(1360, 440), (1520, 440), (1520, 480), (1360, 480)]
    s.poly(rl, 3.8, closed=True)
    s.fill(rl, YEL, 9)
    for k in range(9):
        s.line((1372 + k * 16, 440), (1372 + k * 16, 454 if k % 2 else 462), 2.4)
    pin = [(1260, 720)] + s.epts(1260, 650, 36, 36, 150, 390, n=14)
    s.curve(pin + [(1260, 720)], 4.0)
    s.fill(pin, CORAL)
    s.circle(1260, 650, 12, 3.2)
    for a in ((1200, 290), (1360, 460), (1222, 650)):
        dashed(s, [a, (860, 560)], GRAY, 3.0, closed=False)


def scene2(s):
    s.begin("clay", (40, 140, 400, 400))
    blk = [(110, 360), (250, 360), (250, 480), (110, 480)]
    s.poly(blk, 4.2, closed=True)
    s.poly([(110, 360), (150, 320), (290, 320), (250, 360)], 3.8)
    s.poly([(250, 480), (290, 440), (290, 320)], 3.8)
    s.fill(blk, BRONZE)
    s.qmark(340, 230, 0.9)

    s.begin("onion", (420, 90, 640, 560))
    on = [(700, 200), (650, 260), (610, 360), (630, 450), (700, 490), (770, 450), (790, 360), (750, 260)]
    s.curve(on, 4.4, closed=True)
    s.fill(on, "#e9b3d6")
    for k in (1, 2):
        s.curve([(700, 200), (700 - 40 * k * 0.6, 300), (700 - 50 * k * 0.6, 400), (700, 488)], 3.0)
        s.curve([(700, 200), (700 + 40 * k * 0.6, 300), (700 + 50 * k * 0.6, 400), (700, 488)], 3.0)
    s.curve([(690, 200), (680, 160), (700, 130), (720, 160), (710, 200)], 3.6, GREEN)
    for k, (x, y, rot, c) in enumerate(((880, 220, 30, CORAL), (930, 360, 60, YEL), (880, 500, 100, SKY))):
        peel = s.epts(x, y, 60, 24, 180, 360, n=12, rot=rot)
        s.curve(peel, 4.0)
        s.fill(peel + [peel[0]], c, 9)
        s.arrow((800, 250 + k * 120), (x - 50, y), GRAY, 3.0, 12)

    s.begin("blob", (1060, 140, 500, 440))
    rnd = random.Random(11)
    bl = [(1300 + (120 + rnd.uniform(-30, 30)) * math.cos(t), 360 + (90 + rnd.uniform(-25, 25)) * math.sin(t))
          for t in [i * 2 * math.pi / 12 for i in range(12)]]
    s.curve(bl, 4.2, closed=True)
    s.fill(bl, GRAY)
    s.qmark(1300, 300, 0.8, NAVY)

    s.begin("nope", (1060, 140, 500, 440))
    s.cross(1300, 360, 3.6, CORAL, 10.0)


def scene3(s):
    s.begin("house", (40, 120, 480, 420))
    s.house(270, 480, 260, 180)
    s.ground(60, 500, 482)

    s.begin("form", (40, 120, 480, 420))
    dashed(s, [(110, 490), (110, 290), (270, 160), (430, 290), (430, 490)], TEAL, 4.0)
    s.rays(270, 340, 230, 256, 10, 190, 350, YEL, 3.6)

    s.begin("ball", (560, 90, 1000, 360))
    blk = [(620, 300), (740, 300), (740, 380), (620, 380)]
    s.poly(blk, 4.0, closed=True)
    s.poly([(620, 300), (650, 270), (770, 270), (740, 300)], 3.6)
    s.poly([(740, 380), (770, 350), (770, 270)], 3.6)
    s.fill(blk, BRONZE)
    s.line((830, 320), (870, 320), 5.0)
    s.line((850, 300), (850, 340), 5.0)
    cs = s.epts(990, 320, 70, 70, 0, 360, n=24)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.8, TEAL)
    s.line((1110, 306), (1160, 306), 5.0)
    s.line((1110, 334), (1160, 334), 5.0)
    s.circle(1300, 320, 74)
    s.fill_ell(1300, 320, 72, 72, BRONZE)
    s.arc(1300, 320, 50, 50, 200, 260, 4.0, "#ffffff")
    s.twinkle(1400, 240, 12, YEL)

    s.begin("smith", (540, 420, 560, 380))
    s.person(680, 560, 40, hair="spike", look=(1, 1), mouth="grin", hands=((70, 50), (110, 30)), body_h=130, shirt=CORAL)
    anv = [(820, 700), (1000, 700), (980, 660), (960, 640), (860, 640), (840, 660)]
    s.poly(anv, 4.2, closed=True)
    s.fill(anv, NAVY)
    s.poly([(880, 700), (940, 700), (950, 770), (870, 770)], 4.0, closed=True)
    s.circle(910, 610, 30)
    s.fill_ell(910, 610, 28, 28, BRONZE)
    s.line((790, 590), (850, 520), 5.0, BROWN)
    hd = s.rot_rect(830, 490, 60, 30, -40, (860, 505))
    s.poly(hd, 3.8, closed=True)
    s.fill(hd, GRAY, 8)
    for a in (200, 250, 300, 340):
        t = math.radians(a)
        s.line((910 + 44 * math.cos(t), 610 + 44 * math.sin(t)), (910 + 62 * math.cos(t), 610 + 62 * math.sin(t)), 3.4, ORANGE)
    s.line((560, 772), (1080, 772), 3.4)

    s.begin("into", (1080, 400, 480, 400))
    cs = s.epts(1300, 480, 60, 60, 0, 360, n=20)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.8, TEAL)
    s.arrow((1300, 560), (1300, 640), TEAL, 4.4, 16)
    blk = [(1240, 700), (1360, 700), (1360, 760), (1240, 760)]
    s.poly(blk, 4.0, closed=True)
    s.fill(blk, BRONZE)
    s.arrow((1380, 730), (1440, 730), GRAY, 3.6, 12)
    s.circle(1500, 720, 40)
    s.fill_ell(1500, 720, 38, 38, BRONZE)


def scene4(s):
    s.begin("people", (40, 90, 760, 440))
    for k, (x, hair, c) in enumerate(((140, "short", TEAL), (300, "bun", CORAL), (460, "curly", YEL), (620, "spike", SKY))):
        s.person(x, 360, 30, hair=hair, mouth="smile", hands=((-44, 60), (44, 60)), body_h=90, shirt=c)
    dashed(s, s.epts(380, 170, 26, 26, 0, 360, n=14)[:-1], NAVY, 3.4)
    dashed(s, [(350, 196), (320, 290), (440, 290), (410, 196)], NAVY, 3.4, closed=False)
    s.qmark(520, 130, 0.6)

    s.begin("stop", (790, 120, 400, 660))
    with s.scaled(0.72, (980, 420)):
        s.aristotle(980, 420, wave=True)
    s.ground(820, 1160, 680)

    s.begin("socrates", (1190, 110, 380, 690))
    cone = [(1380, 120), (1230, 790), (1530, 790)]
    s.fill(cone, "#fff1b0", 16)
    with s.scaled(0.85, (1380, 380)):
        socrates(s, 1380, 380)
    s.line((1220, 792), (1550, 792), 3.4)

    s.begin("many", (40, 520, 760, 280))
    for i in range(10):
        x, y = 100 + i * 64, 640 + (i % 2) * 40
        s.circle(x, y, 14, 3.0, GRAY)
        s.curve([(x - 16, y + 46), (x - 12, y + 18), (x + 12, y + 18), (x + 16, y + 46)], 3.0, GRAY)
    ring = s.epts(390, 670, 340, 90, 0, 360, n=36)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 3.0, TEAL)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
