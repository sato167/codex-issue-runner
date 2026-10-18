"""第 11 集 · 卷十一（Κ）：复习课、运动与无限。"""
from sketch import *  # noqa: F401,F403

ICONS = [(640, 270), (900, 270), (1160, 270), (1420, 270), (1160, 590), (900, 590)]


def scene1(s):
    s.begin("notebook", (40, 130, 470, 600))
    L = [(80, 220), (270, 240), (270, 680), (80, 660)]
    R = [(270, 240), (460, 220), (460, 660), (270, 680)]
    for pg in (L, R):
        s.poly(pg, 4.2, closed=True)
        s.fill(pg, CREAM)
    for k in range(7):
        y = 290 + k * 50
        s.line((100, y - 2), (250, y + 4), 2.4, SKY)
        s.line((290, y + 4), (440, y - 2), 2.4, SKY)
    for k in range(5):
        s.circle(270, 280 + k * 90, 8, 2.8)
    s.line((380, 560), (500, 380), 6.0, ORANGE)
    s.poly([(380, 560), (372, 590), (396, 572)], 3.4, closed=True)

    s.begin("chain", (520, 90, 1050, 640))
    s.curve([ICONS[0], ICONS[1], ICONS[2], ICONS[3], (1500, 430), ICONS[4], ICONS[5], (700, 600)], 3.4, GRAY)
    x, y = ICONS[0]
    s.curve([(x - 50, y), (x - 25, y - 26), (x + 25, y - 26), (x + 50, y)], 4.0)
    s.curve([(x - 50, y), (x - 25, y + 26), (x + 25, y + 26), (x + 50, y)], 4.0)
    s.fill_ell(x, y, 18, 18, SKY)
    s.dot(x, y, 10)
    x, y = ICONS[1]
    dr = [(x - 40, y + 50), (x - 40, y - 50), (x + 40, y - 50), (x + 40, y + 50)]
    s.poly(dr, 4.0, closed=True)
    s.fill(dr, "#f6d7a7")
    s.line((x, y - 50), (x, y + 50), 3.4)
    s.arrow((x - 80, y + 6), (x - 20, y), INK, 3.4, 10)
    x, y = ICONS[2]
    s.curve([(x - 60, y + 10), (x - 20, y - 30), (x + 20, y - 10), (x - 10, y + 20), (x - 30, y - 10), (x + 20, y - 30), (x + 60, y + 10)], 6.0, BROWN)
    x, y = ICONS[3]
    s.tablet(x, y, 120, 90)
    x, y = ICONS[4]
    bk = [(x - 50, y - 60), (x + 40, y - 66), (x + 46, y + 56), (x - 44, y + 62)]
    s.poly(bk, 4.0, closed=True)
    s.fill(bk, NAVY)
    s.fill([(x - 20, y - 30), (x + 20, y - 32), (x + 22, y), (x - 18, y + 2)], CREAM, 8)
    x, y = ICONS[5]
    s.dice(x - 20, y, 60, -12, "#ffffff", 5)
    s.dice(x + 40, y + 20, 50, 18, "#ffe6e0", 3)

    s.begin("checks", (520, 90, 1050, 640))
    for x, y in ICONS:
        s.check(x + 40, y - 70, 0.6)


def scene2(s):
    s.begin("runner", (40, 110, 460, 400))
    s.circle(260, 220, 34)
    s.eyes(264, 216, 12, (1, 0))
    s.arc(268, 232, 10, 6, 20, 160, 3.2)
    s.line((256, 254), (236, 360), 4.4)
    s.curve([(250, 280), (210, 300), (190, 270)], 4.2)
    s.curve([(250, 280), (300, 290), (320, 250)], 4.2)
    s.curve([(236, 360), (200, 400), (170, 400)], 4.2)
    s.curve([(236, 360), (276, 390), (290, 440)], 4.2)
    for k in range(4):
        s.line((90, 240 + k * 40), (150, 240 + k * 40), 3.4, GRAY)
    s.ground(60, 480, 452)

    s.begin("growing", (500, 90, 1070, 380))
    sd = s.epts(600, 400, 22, 15, 0, 360, n=14, rot=-20)[:-1]
    s.curve(sd + sd[:1], 3.8)
    s.fill(sd, BROWN, 8)
    s.arrow((650, 380), (760, 380), ORANGE, 4.0, 14)
    s.sprout(900, 420, 160)
    ring = s.epts(900, 330, 120, 120, 0, 360, n=30)
    for i in range(0, len(ring) - 1, 2):
        s.line(ring[i], ring[i + 1], 3.4, CORAL)
    s.arrow((1040, 380), (1150, 380), ORANGE, 4.0, 14)
    s.tree(1340, 420, 300, GREEN)
    s.ground(520, 1560, 422)

    s.begin("wall", (40, 480, 700, 320))
    for row in range(4):
        for i in range(6 if row < 2 else (4 if row == 2 else 2)):
            bx, by = 100 + i * 84 + (row % 2) * 42, 740 - row * 34
            b = [(bx, by), (bx + 80, by), (bx + 80, by + 30), (bx, by + 30)]
            s.poly(b, 3.4, closed=True)
            s.fill(b, "#f4a28c", 8)
    nb = [(520, 560), (600, 560), (600, 590), (520, 590)]
    s.poly(nb, 3.8, closed=True)
    s.fill(nb, CORAL, 9)
    s.circle(620, 560, 18)
    s.curve([(636, 566), (680, 590), (720, 640)], 4.2)
    s.line((60, 772), (720, 772), 3.4)

    s.begin("progress", (740, 500, 830, 300))
    bar = s.rrect(800, 610, 700, 70, 30)
    s.curve(bar + bar[:1], 4.4)
    s.fill([(806, 616), (1150, 616), (1150, 674), (806, 674)], TEAL, 12)
    s.poly([(1170, 600), (1220, 645), (1170, 690)], 4.4, CORAL, closed=True)
    s.fill([(1170, 600), (1220, 645), (1170, 690)], CORAL, 8)
    for x in (900, 1000, 1100):
        s.line((x, 560), (x + 30, 560), 3.0, GRAY)


def scene3(s):
    s.begin("infinity", (40, 80, 500, 360))
    pts = []
    for i in range(41):
        t = 2 * math.pi * i / 40
        d = 1 + math.sin(t) ** 2
        pts.append((260 + 170 * math.cos(t) / d, 260 + 170 * math.sin(t) * math.cos(t) / d))
    s.curve(pts, 8.0, SKY)
    s.qmark(470, 140, 0.8)

    s.begin("aristotle", (1170, 120, 400, 680))
    with s.scaled(0.72, (1370, 420)):
        s.aristotle(1370, 420, wave=True)
    s.ground(1190, 1550, 680)

    s.begin("numbers", (560, 90, 600, 320))
    for k, ch in enumerate("12345"):
        h = 80 - k * 10
        digit(s, ch, 600 + k * 90, 260 - h / 2, h, (CORAL, ORANGE, YEL, GREEN, SKY)[k])
    for k in range(3):
        s.dot(1060 + k * 26, 260, 7 - k)

    s.begin("halving", (560, 420, 600, 220))
    s.line((600, 540), (1120, 540), 4.4)
    for k, (x, h) in enumerate(((600, 40), (1120, 40), (860, 34), (730, 28), (665, 22), (632, 18), (616, 14))):
        s.line((x, 540 - h), (x, 540 + h), 3.6, NAVY if k < 2 else CORAL)
    s.qmark(600, 460, 0.4, ORANGE)

    s.begin("road", (40, 460, 1120, 340))
    s.line((100, 790), (560, 640), 4.2)
    s.line((420, 790), (600, 640), 4.2)
    for k in range(6):
        t0 = k / 6
        y0 = 780 - t0 * 130
        s.line((260 + (580 - 260) * t0, y0), (270 + (580 - 260) * t0, y0 - 14), 4.0 - k * 0.5, YEL)
    for k in range(4):
        s.dot(620 + k * 40, 630 - k * 8, 7 - k * 1.4)
    s.line((640, 640), (1140, 640), 2.6, GRAY)
    hg = [(900, 700), (960, 700), (930, 740)]
    s.poly(hg, 3.6, closed=True)
    s.fill(hg, YEL, 8)
    s.poly([(900, 780), (960, 780), (930, 740)], 3.6, closed=True)
    s.line((894, 700), (966, 700), 4.0)
    s.line((894, 780), (966, 780), 4.0)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
