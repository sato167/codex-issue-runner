"""第 5 集 · 卷五（Δ）：哲学小词典。"""
from sketch import *  # noqa: F401,F403

BRONZE = "#c98a4b"


def scene1(s):
    s.begin("dict", (60, 140, 500, 600))
    cover = [(150, 260), (450, 240), (460, 640), (160, 660)]
    s.poly(cover, 4.6, closed=True)
    s.fill(cover, NAVY)
    s.poly([(160, 660), (190, 690), (490, 670), (460, 640)], 4.0)
    s.poly([(450, 240), (480, 270), (490, 670)], 4.0)
    for k in range(5):
        y = 290 + k * 70
        tab = [(456 + k * 0.6, y), (490, y + 4), (492, y + 40), (458, y + 36)]
        s.poly(tab, 3.2, closed=True)
        s.fill(tab, (CORAL, YEL, TEAL, SKY, PINK)[k], 8)
    lab = [(220, 330), (390, 320), (394, 400), (224, 410)]
    s.poly(lab, 3.4, closed=True)
    s.fill(lab, CREAM, 10)
    s.book(306, 364, 80, 44)

    s.begin("cards", (540, 90, 580, 540))
    icons = ("sun", "fish", "gear", "heart", "cube", "q")
    for k, ic in enumerate(icons):
        t = math.radians(198 + k * 25)
        x, y = 780 + 260 * math.cos(t) + 120, 520 + 300 * math.sin(t)
        s.card(x, y, 90, 110, CREAM, q=False, rot=(-12, 6, -4, 10, -8, 4)[k])
        if ic == "sun":
            s.sun(x, y, 18, YEL, 6)
        elif ic == "fish":
            s.fish(x + 8, y, 0.7)
        elif ic == "gear":
            s.gear(x, y, 26, 8, TEAL)
        elif ic == "heart":
            s.heart(x, y, 22, CORAL)
        elif ic == "cube":
            c = [(x - 20, y - 14), (x + 14, y - 14), (x + 14, y + 20), (x - 20, y + 20)]
            s.poly(c, 3.4, closed=True)
            s.fill(c, ORANGE, 8)
        else:
            s.qmark(x, y - 20, 0.6)
    for k in range(4):
        s.line((480 + k * 14, 300 - k * 30), (500 + k * 14, 290 - k * 30), 3.0, GRAY)

    s.begin("meanings", (1100, 120, 470, 600))
    s.card(1250, 440, 110, 140, "#ffe6e0", q=False)
    s.heart(1250, 440, 30, CORAL)
    for k, y in enumerate((230, 440, 630)):
        s.arrow((1312, 440 + (k - 1) * 30), (1410, y), TEAL, 4.0, 14)
    s.tree(1490, 280, 120, GREEN)
    s.house(1490, 480, 110, 70)
    s.star(1490, 620, 34, YEL)


def scene2(s):
    s.begin("statue", (620, 120, 360, 680))
    ped = [(690, 640), (910, 640), (900, 760), (700, 760)]
    s.poly(ped, 4.4, closed=True)
    s.fill(ped, "#dfe3ea")
    s.poly([(670, 640), (930, 640), (930, 618), (670, 618)], 4.0, closed=True)
    s.person(800, 300, 50, hair="curly", mouth="smile", hands=((-80, 80), (80, -40)), body_h=210, shirt=BRONZE, legs=True)
    s.fill_ell(800, 300, 48, 48, BRONZE)
    s.line((880, 260), (890, 560), 5.0)
    s.poly([(880, 260), (870, 230), (890, 218), (900, 256)], 3.6, closed=True)

    s.begin("material", (40, 100, 560, 360))
    for k, (x, y) in enumerate(((180, 380), (320, 380), (250, 320), (400, 380), (330, 320))):
        ing = [(x - 60, y + 20), (x + 60, y + 20), (x + 44, y - 24), (x - 44, y - 24)]
        s.poly(ing, 4.0, closed=True)
        s.fill(ing, BRONZE)
    for x, y in ((140, 250), (440, 260), (300, 230)):
        s.twinkle(x, y, 10, YEL)

    s.begin("form", (40, 460, 560, 340))
    sheet = [(90, 500), (520, 500), (520, 780), (90, 780)]
    s.poly(sheet, 4.0, closed=True)
    s.fill(sheet, SKY)
    for x in range(130, 520, 40):
        s.line((x, 510), (x, 770), 1.8, "#cfe4ff")
    cs = s.epts(305, 560, 30, 30, 0, 360, n=16)
    for i in range(0, len(cs) - 1, 2):
        s.line(cs[i], cs[i + 1], 3.6, "#ffffff")
    for a, b in (((270, 600), (240, 740)), ((340, 600), (370, 740)), ((240, 740), (370, 740))):
        for k in range(5):
            t0, t1 = k / 5, k / 5 + 0.12
            s.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 3.6, "#ffffff")

    s.begin("maker", (1000, 100, 560, 380))
    s.person(1180, 280, 40, hair="short", look=(1, 0.5), mouth="grin", hands=((80, 30), (110, 60)), body_h=120, shirt=TEAL, legs=False)
    s.line((1290, 340), (1340, 300), 5.0, GRAY)
    s.line((1260, 310), (1300, 270), 5.0, BROWN)
    hd = s.rot_rect(1280, 250, 50, 24, -40, (1300, 262))
    s.poly(hd, 3.6, closed=True)
    s.fill(hd, GRAY, 8)
    blk = [(1360, 300), (1500, 300), (1500, 440), (1360, 440)]
    s.poly(blk, 4.0, closed=True)
    s.fill(blk, "#dfe3ea")
    s.curve([(1400, 330), (1420, 360), (1410, 400), (1440, 420)], 3.0, GRAY)
    for x, y in ((1350, 270), (1372, 250), (1340, 240)):
        s.poly([(x, y), (x + 8, y - 6), (x + 10, y + 4)], 2.8, closed=True)

    s.begin("purpose", (1000, 460, 560, 340))
    for sx in (-1, 1):
        pts = s.epts(1280, 640, 110, 120, 90 + sx * 20, 90 + sx * 160, n=12)
        s.curve(pts, 4.0, GREEN)
        for i in range(1, len(pts) - 1, 2):
            x, y = pts[i]
            lf = s.epts(x, y, 18, 9, 0, 360, n=10, rot=math.degrees(math.atan2(y - 640, x - 1280)) + 90)[:-1]
            s.curve(lf + lf[:1], 3.0)
            s.fill(lf, GREEN, 7)
    s.heart(1280, 640, 36, CORAL)


def scene3(s):
    s.begin("seed", (40, 100, 760, 380))
    sd = s.epts(120, 380, 24, 16, 0, 360, n=14, rot=-20)[:-1]
    s.curve(sd + sd[:1], 3.8)
    s.fill(sd, BROWN, 8)
    s.arrow((170, 380), (240, 380), ORANGE, 4.0, 14)
    s.sprout(320, 420, 100)
    s.arrow((400, 380), (470, 380), ORANGE, 4.0, 14)
    s.tree(620, 440, 300, GREEN)
    s.ground(60, 760, 442)

    s.begin("bed", (800, 100, 770, 400))
    s.ground(820, 1560, 420)
    bed = [(1000, 420), (1000, 380), (1300, 380), (1300, 420)]
    s.poly(bed, 4.0)
    s.line((1000, 380), (1000, 330), 4.0)
    s.line((1300, 380), (1300, 350), 4.0)
    for k in range(4):
        s.line((960 + k * 120, 450 + (k % 2) * 16), (990 + k * 120, 448 + (k % 2) * 16), 2.6, BROWN)
    s.fill([(1002, 418), (1002, 384), (1298, 384), (1298, 418)], BROWN, 9)
    s.tree(1150, 380, 260, GREEN)
    hb = [(1370, 330), (1370, 250), (1400, 250), (1400, 330)]
    s.poly(hb, 3.8, closed=True)
    s.fill(hb, BROWN, 8)
    mat = [(1400, 300), (1510, 300), (1510, 322), (1400, 322)]
    s.poly(mat, 3.6, closed=True)
    s.fill(mat, SKY, 8)
    s.ell(1420, 290, 16, 9, 3.2)
    s.line((1510, 322), (1510, 340), 3.6)
    s.line((1372, 330), (1372, 340), 3.6)
    s.cross(1440, 296, 1.3)

    s.begin("necessary", (300, 470, 1000, 330))
    tri = [(400, 760), (720, 760), (540, 520)]
    s.poly(tri, 4.4, closed=True)
    s.fill(tri, SKY)
    s.arc(400, 760, 46, 46, -53, 0, 3.6, CORAL)
    s.arc(720, 760, 46, 46, 180, 233, 3.6, ORANGE)
    s.arc(540, 520, 40, 40, 53, 127, 3.6, TEAL)
    s.line((790, 630), (850, 630), 5.0)
    s.line((790, 654), (850, 654), 5.0)
    for x0 in (920, 1100):
        s.poly([(x0, 560), (x0, 720), (x0 + 140, 720)], 4.4)
        sq = [(x0, 690), (x0 + 30, 690), (x0 + 30, 720), (x0, 720)]
        s.poly(sq, 3.0)
        s.fill(sq, YEL, 7)
    s.line((1065, 640), (1085, 640), 4.0)
    s.line((1075, 630), (1075, 650), 4.0)


def scene4(s):
    s.begin("stick", (40, 110, 480, 300))
    st = [(80, 250), (480, 210), (484, 236), (84, 276)]
    s.poly(st, 4.0, closed=True)
    s.fill(st, BROWN)
    for x in (180, 300, 400):
        s.line((x, 248 - (x - 80) * 0.1), (x + 20, 246 - (x - 80) * 0.1), 2.4)
    s.rays(282, 244, 60, 80, 6, 200, 340, YEL, 3.6)

    s.begin("fish", (520, 110, 560, 300))
    for k, (x, kk) in enumerate(((640, 1.2), (800, 0.9), (940, 1.0))):
        s.fish(x, 260, kk, SKY)
    ring = s.epts(790, 260, 230, 80, 0, 360, n=30)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 3.0, TEAL)

    s.begin("being", (1080, 110, 490, 300))
    cube = [(1130, 230), (1200, 230), (1200, 300), (1130, 300)]
    s.poly(cube, 4.2, closed=True)
    s.poly([(1130, 230), (1152, 208), (1222, 208), (1200, 230)], 3.6)
    s.poly([(1200, 300), (1222, 278), (1222, 208)], 3.6)
    s.fill(cube, ORANGE)
    pin = [(1340, 320)] + s.epts(1340, 254, 32, 32, 150, 390, n=14)
    s.curve(pin + [(1340, 320)], 4.0)
    s.fill(pin, CORAL)
    s.circle(1340, 254, 10, 3.0)
    rl = [(1420, 240), (1540, 240), (1540, 276), (1420, 276)]
    s.poly(rl, 3.8, closed=True)
    s.fill(rl, YEL, 9)
    for k in range(7):
        s.line((1432 + k * 16, 240), (1432 + k * 16, 254 if k % 2 else 262), 2.4)

    s.begin("alone", (40, 420, 600, 380))
    cone = [(300, 430), (200, 780), (420, 780)]
    s.fill(cone, "#fff1b0", 16)
    for a, b in ((cone[0], cone[1]), (cone[0], cone[2])):
        for k in range(6):
            t0, t1 = k / 6, k / 6 + 0.1
            s.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 2.6, ORANGE)
    s.person(310, 590, 36, hair="bun", mouth="smile", hands=((-56, 70), (56, 70)), body_h=110, shirt=CORAL)
    s.line((120, 782), (500, 782), 3.4)

    s.begin("chickduck", (640, 420, 930, 380))
    s.chicken(820, 680, 1.0, 1)
    s.duck(1340, 690, 1.0, -1)
    s.bubble(860, 500, 90, 56, (880, 590))
    s.circle(860, 500, 24, 3.6)
    s.fill_ell(860, 500, 22, 22, CORAL)
    s.bubble(1300, 500, 90, 56, (1280, 590))
    tri = [(1300, 474), (1326, 522), (1274, 522)]
    s.poly(tri, 3.6, closed=True)
    s.fill(tri, SKY, 8)
    s.qmark(1060, 520, 0.7)
    s.qmark(1110, 560, 0.5, ORANGE)
    s.line((680, 782), (1540, 782), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
