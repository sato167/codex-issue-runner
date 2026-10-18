"""第 12 集 · 卷十二（Λ）：不动的推动者。"""
from sketch import *  # noqa: F401,F403


def crown(s, cx, cy, w=60, color=YEL):
    pts = [(cx - w / 2, cy + w * 0.3), (cx - w / 2, cy - w * 0.25), (cx - w / 4, cy), (cx, cy - w * 0.4),
           (cx + w / 4, cy), (cx + w / 2, cy - w * 0.25), (cx + w / 2, cy + w * 0.3)]
    s.poly(pts, 3.6, closed=True)
    s.fill(pts, color, 8)


def head_profile(s, cx, cy, r):
    s.circle(cx, cy, r, max(2.6, r / 14))
    s.dot(cx + r * 0.35, cy - r * 0.1, max(3, r / 9))
    s.arc(cx + r * 0.3, cy + r * 0.3, r * 0.25, r * 0.15, 20, 160, max(2.4, r / 16))


def scene1(s):
    s.begin("peak", (40, 90, 500, 420))
    s.poly([(70, 470), (230, 220), (290, 290), (360, 150), (520, 470)], 4.4)
    snow = [(330, 196), (360, 150), (392, 202), (372, 192), (360, 206), (346, 192)]
    s.poly(snow, 3.4, closed=True)
    s.fill(snow, "#e3eeff", 9)
    s.line((360, 152), (360, 100), 3.6)
    fl = [(360, 100), (404, 114), (360, 128)]
    s.poly(fl, 3.4, closed=True)
    s.fill(fl, CORAL, 8)
    s.sun(470, 160, 30, YEL, 8)
    s.ground(50, 540, 472)

    s.begin("podium", (40, 500, 500, 300))
    for k, (x, h, c) in enumerate(((100, 90, SKY), (220, 150, YEL), (340, 120, GREEN))):
        st = [(x, 780), (x, 780 - h), (x + 120, 780 - h), (x + 120, 780)]
        s.poly(st, 4.2, closed=True)
        s.fill(st, c)
        digit(s, "213"[k], x + 46, 780 - h + 14, 40)

    s.begin("flower", (560, 90, 460, 380))
    for x, wilt in ((680, False), (900, True)):
        if not wilt:
            s.curve([(x, 420), (x + 4, 330), (x, 260)], 3.8, GREEN)
            for i in range(6):
                t = i * math.pi / 3
                s.circle(x + 24 * math.cos(t), 230 + 24 * math.sin(t), 16, 3.2)
                s.fill_ell(x + 24 * math.cos(t), 230 + 24 * math.sin(t), 14, 14, PINK)
            s.circle(x, 230, 12, 3.2)
            s.fill_ell(x, 230, 10, 10, YEL)
        else:
            s.curve([(x, 420), (x + 10, 340), (x + 40, 300), (x + 60, 310)], 3.8, "#a3a86b")
            for k in range(4):
                pet = s.epts(x + 70 + k * 6, 330 + k * 12, 14, 8, 0, 360, n=10, rot=60 + k * 20)[:-1]
                s.curve(pet + pet[:1], 3.0)
                s.fill(pet, "#d9b8a0", 7)
            s.poly([(x + 30, 430), (x + 50, 440), (x + 70, 432)], 3.0, "#d9b8a0")
    s.arrow((740, 330), (840, 330), GRAY, 3.6, 12)
    s.ground(580, 1000, 422)

    s.begin("orbit", (1040, 80, 530, 400))
    for k, (rx, ry) in enumerate(((90, 34), (160, 60), (230, 86))):
        s.ell(1300, 280, rx, ry, 3.0, GRAY, rot=-12)
        a = math.radians(40 + k * 100)
        px = 1300 + rx * math.cos(a) * math.cos(math.radians(-12)) - ry * math.sin(a) * math.sin(math.radians(-12))
        py = 280 + rx * math.cos(a) * math.sin(math.radians(-12)) + ry * math.sin(a) * math.cos(math.radians(-12))
        s.circle(px, py, 16, 3.4)
        s.fill_ell(px, py, 14, 14, (SKY, CORAL, YEL)[k])
        s.arc(px, py, 30, 20, 120, 200, 3.0, ORANGE)
    s.circle(1300, 280, 26, 3.6)
    s.fill_ell(1300, 280, 24, 24, ORANGE)

    s.begin("mover", (560, 470, 1010, 330))
    s.star_glow(1060, 640, 54)
    for a, b in (((960, 640), (680, 640)), ((1160, 640), (1440, 640)), ((990, 580), (820, 500)), ((1130, 580), (1300, 500))):
        dashed(s, [a, b], TEAL, 3.4, closed=False)


def scene2(s):
    s.begin("gears", (40, 90, 780, 420))
    for k, (x, y, r, c) in enumerate(((160, 300, 90, YEL), (320, 250, 60, TEAL), (450, 320, 70, SKY), (600, 260, 56, CORAL))):
        s.gear(x, y, r, 10 if r > 70 else 8, c)
        s.arc(x, y, r + 20, r + 20, -60, 20, 3.0, ORANGE)
    s.rays(160, 300, 104, 130, 10, 0, 360, YEL, 3.6)

    s.begin("regress", (840, 90, 730, 420))
    s.gear(1100, 300, 70, 9, GRAY)
    s.circle(1240, 300, 20)
    s.curve([(1256, 310), (1320, 320), (1380, 300)], 4.2)
    s.circle(1400, 300, 20)
    s.curve([(1416, 310), (1470, 320), (1520, 300)], 4.2)
    for k in range(3):
        s.dot(1530 + k * 14, 260, 6 - k)
    s.qmark(1100, 150, 0.7)

    s.begin("still", (40, 510, 1530, 290))
    s.star_glow(800, 650, 60)
    s.circle(800, 650, 130, 4.0, TEAL)
    s.check(1000, 560, 1.0)
    for x in (300, 1300):
        s.line((x - 80, 650), (x + 80, 650), 3.0, GRAY)


def scene3(s):
    s.begin("q", (40, 90, 380, 340))
    s.qmark(200, 200, 1.4)
    s.star(330, 360, 30, YEL)

    s.begin("hand", (420, 90, 500, 340))
    s.circle(780, 270, 50)
    s.fill_ell(780, 270, 48, 48, SKY)
    palm = [(560, 230), (680, 230), (700, 250), (700, 300), (680, 320), (560, 320)]
    s.curve(palm, 4.0, closed=True)
    s.fill(palm, "#ffd9bf")
    for k in range(3):
        s.line((690, 248 + k * 20), (720, 248 + k * 20), 4.0)
    s.cross(680, 270, 2.6)

    s.begin("lover", (40, 440, 800, 360))
    s.person(200, 600, 40, hair="bun", mouth="grin", hands=((60, -20), (70, 30)), body_h=110, shirt=PINK)
    for sx in (-1, 1):
        s.heart(200 + sx * 14, 598, 6, CORAL)
    s.star_glow(640, 560, 46)
    for k in range(3):
        s.heart(360 + k * 70, 560 - (k % 2) * 40, 12 + k * 2, CORAL)
    s.line((60, 772), (800, 772), 3.4)

    s.begin("lighthouse", (840, 90, 730, 710))
    rock = [(1220, 640), (1260, 600), (1440, 600), (1500, 660)]
    s.curve(rock, 4.2)
    lh = [(1300, 600), (1320, 300), (1380, 300), (1400, 600)]
    s.poly(lh, 4.2, closed=True)
    for k in range(3):
        y = 360 + k * 80
        band = [(1320 - k * 7, y), (1380 + k * 7, y), (1384 + k * 7, y + 36), (1316 - k * 7, y + 36)]
        s.fill(band, CORAL, 9)
    top = [(1310, 300), (1390, 300), (1380, 240), (1320, 240)]
    s.poly(top, 4.0, closed=True)
    s.fill(top, YEL, 8)
    s.poly([(1306, 240), (1350, 200), (1394, 240)], 4.0, closed=True)
    beam = [(1320, 270), (900, 180), (900, 360)]
    s.fill(beam, "#fff1b0", 16)
    s.line(beam[0], beam[1], 2.6, ORANGE)
    s.line(beam[0], beam[2], 2.6, ORANGE)
    hull = [(900, 620), (1060, 620), (1030, 670), (930, 670)]
    s.poly(hull, 4.0, closed=True)
    s.fill(hull, BROWN)
    s.line((980, 620), (980, 520), 4.0)
    sail = [(986, 526), (1050, 610), (986, 610)]
    s.poly(sail, 3.8, closed=True)
    s.fill(sail, "#ffffff")
    for k in range(4):
        s.line((1080 + k * 40, 645), (1100 + k * 40, 645), 3.4, TEAL)
    s.arrow((1240, 645), (1250, 645), TEAL, 3.4, 12)
    for k in range(3):
        xs = [880 + 30 * i for i in range(23)]
        s.curve([(x, 700 + k * 26 + (5 if i % 2 else -5)) for i, x in enumerate(xs)], 3.0, SKY)


def scene4(s):
    s.begin("thinker", (40, 90, 500, 380))
    s.star_glow(220, 300, 54)
    cl = s.cloud(420, 160, 80, 44, 8)
    s.curve(cl + cl[:2], 3.6)
    s.dot(330, 230, 7)
    s.dot(350, 210, 9)
    for k in range(3):
        s.dot(395 + k * 25, 160, 6)

    s.begin("loop", (560, 90, 560, 380))
    head_profile(s, 680, 360, 70)
    cl = s.cloud(880, 230, 150, 100, 9)
    s.curve(cl + cl[:2], 3.8)
    s.dot(760, 300, 8)
    s.dot(780, 280, 10)
    head_profile(s, 830, 250, 34)
    cl2 = s.cloud(920, 190, 60, 40, 7)
    s.curve(cl2 + cl2[:2], 3.0)
    head_profile(s, 905, 195, 14)
    s.dot(950, 180, 4)
    s.arrow((1010, 330), (960, 400), ORANGE, 3.4, 12)
    s.curve([(960, 400), (840, 440), (740, 430)], 3.4, ORANGE)

    s.begin("god", (1140, 90, 430, 380))
    for k in range(3):
        s.circle(1350, 270, 60 + k * 30, 3.4 - k * 0.6, (YEL, ORANGE, CORAL)[k])
    s.star(1350, 270, 46, YEL)
    s.rays(1350, 270, 160, 190, 16, 0, 360, YEL, 3.6)

    s.begin("crowns", (40, 480, 1530, 320))
    for k in range(4):
        x = 140 + k * 130
        s.person(x, 640, 30, hair="short", mouth="frown", hands=((-44, 40), (44, 40)), body_h=70, shirt=(GRAY, "#b9b3d6", GRAY, "#b9b3d6")[k], legs=False)
        crown(s, x, 594, 50)
    for k in range(3):
        s.line((200 + k * 130, 560), (220 + k * 130, 540), 3.4, CORAL)
    s.cross(340, 520, 1.0)
    s.line((760, 520), (760, 790), 3.0, GRAY)
    s.person(1150, 650, 40, hair="curly", mouth="grin", hands=((-60, 50), (60, 50)), body_h=90, shirt=TEAL, legs=False)
    crown(s, 1150, 590, 70)
    s.check(1300, 560, 1.0)
    s.rays(1150, 620, 120, 146, 8, 200, 340, YEL, 3.6)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
