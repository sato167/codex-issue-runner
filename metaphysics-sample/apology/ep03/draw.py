"""《申辩篇》第 3 集（35e–42a）：未经审视的人生。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from props import *  # noqa: F401,F403,E402


def cup(s, cx, gy, color=NAVY):
    bowl = s.epts(cx, gy - 70, 40, 34, 0, 180, n=12)
    s.curve(bowl + [bowl[0]], 4.0)
    s.fill(bowl + [bowl[0]], color, 8)
    s.line((cx, gy - 36), (cx, gy - 6), 4.0)
    s.line((cx - 24, gy), (cx + 24, gy), 4.0)


def hooded(s, cx, hy, r=30, color="#9aa5b8", speed=False):
    """追赶者：死亡（慢，灰）或邪恶（快，深色）。"""
    hood = [(cx - r, hy + r * 0.6), (cx - r * 0.9, hy - r * 0.6), (cx, hy - r * 1.2), (cx + r * 0.9, hy - r * 0.6),
            (cx + r, hy + r * 0.6), (cx + r * 1.4, hy + r * 3.6), (cx - r * 1.4, hy + r * 3.6)]
    s.curve(hood, 4.0, closed=True)
    s.fill(hood, color)
    s.dot(cx + r * 0.25, hy - r * 0.05, 5)
    if speed:
        for k in range(4):
            s.line((cx - r * 2.0 - k * 6, hy + k * r * 0.7), (cx - r * 3.6 - k * 10, hy + k * r * 0.7), 3.4, GRAY)


def scene1(s):
    s.begin("vote", (40, 90, 1060, 700))
    urn(s, 300, 560, 300, NAVY)
    urn(s, 800, 560, 300, "#f3ead8")
    pebbles(s, 300, 650, 28, NAVY, 200)
    pebbles(s, 800, 650, 22, "#ffffff", 180)
    for k, ch in enumerate("280"):
        digit(s, ch, 230 + k * 52, 680, 80, CORAL, 7.0)
    for k, ch in enumerate("220"):
        digit(s, ch, 730 + k * 52, 680, 80, TEAL, 7.0)
    s.cross(300, 200, 0.9)
    s.check(800, 200, 0.9)

    s.begin("thirty", (1110, 90, 460, 700))
    socrates_head(s, 1330, 300, 50)
    s.curve([(1180, 560), (1330, 470), (1480, 560)], 4.4, ORANGE)
    s.arrow((1460, 548), (1484, 566), ORANGE, 4.4, 16)
    digit(s, "3", 1290, 560, 80, ORANGE, 7.0)
    digit(s, "0", 1342, 560, 80, ORANGE, 7.0)
    for k in range(5):
        s.fill_ell(1190 + k * 16, 600 - (k % 2) * 8, 8, 6, NAVY)


def scene2(s):
    s.begin("rule", (40, 90, 500, 400))
    for x, who in ((160, "m"), (380, "s")):
        c = s.rrect(x - 90, 140, 180, 260, 16)
        s.curve(c + c[:1], 4.0)
        s.fill(c, CREAM)
        if who == "m":
            s.circle(x, 190, 22, 3.4)
            s.curve([(x - 20, 180), (x - 26, 210), (x - 22, 230)], 3.0, BROWN)
            s.curve([(x + 20, 180), (x + 26, 210), (x + 22, 230)], 3.0, BROWN)
        else:
            socrates_head(s, x, 186, 22)
        s.line((x - 60, 250), (x + 60, 250), 2.6, GRAY)

    s.begin("deathcard", (40, 90, 500, 400))
    cup(s, 160, 370)

    s.begin("deserve", (550, 90, 520, 400))
    socrates_head(s, 760, 320, 54)
    cl = s.cloud(930, 190, 110, 60, 8)
    s.curve(cl + cl[:2], 3.8)
    s.heart(930, 190, 26, CORAL)
    s.dot(850, 260, 7)
    s.dot(870, 240, 9)

    s.begin("prytaneum", (40, 480, 740, 320))
    s.line((80, 680), (740, 680), 4.4)
    s.line((120, 680), (110, 770), 4.0)
    s.line((700, 680), (710, 770), 4.0)
    for k in range(3):
        pl = s.epts(220 + k * 160, 670, 56, 12, 0, 360, n=14)[:-1]
        s.curve(pl + pl[:1], 3.4)
    s.ell(220, 650, 36, 20, 3.6)
    s.fill_ell(220, 650, 34, 18, BROWN)
    for k in range(5):
        s.circle(370 + (k % 3) * 18, 640 + (k // 3) * 16, 9, 2.8)
        s.fill_ell(370 + (k % 3) * 18, 640 + (k // 3) * 16, 7, 7, "#9b6bb5")
    laurel(s, 540, 650, 40)
    socrates_head(s, 380, 540, 36)
    s.circle(620, 550, 30, 3.4)
    laurel(s, 620, 526, 32)

    s.begin("happy", (800, 480, 770, 320))
    mask(s, 960, 620, 54, True, YEL)
    s.line((1080, 610), (1120, 610), 5.0, CORAL)
    s.line((1080, 634), (1120, 634), 5.0, CORAL)
    s.line((1110, 590), (1090, 654), 5.0, CORAL)
    s.person(1300, 600, 40, hair="curly", mouth="grin", hands=((-60, 40), (60, 40)), body_h=90, shirt=TEAL, legs=False)
    s.heart(1300, 700, 18, CORAL)
    s.rays(1300, 600, 70, 96, 8, 200, 340, YEL, 3.4)


def scene5(s):
    s.begin("exile", (40, 90, 760, 380))
    for x in (120, 420, 700):
        s.poly([(x - 60, 400), (x - 60, 320), (x - 30, 320), (x - 30, 300), (x, 300), (x, 320), (x + 30, 320), (x + 30, 300), (x + 60, 300), (x + 60, 400)], 3.6)
    s.line((60, 402), (780, 402), 3.4)
    socrates_head(s, 280, 320, 30)
    s.arrow((300, 370), (360, 370), GRAY, 3.6, 12)
    s.qmark(330, 240, 0.4)
    socrates_head(s, 560, 320, 30)
    s.arrow((580, 370), (640, 370), GRAY, 3.6, 12)
    s.qmark(610, 240, 0.4)
    s.cross(720, 220, 0.9)

    s.begin("quiet", (820, 90, 750, 380))
    s.person(1050, 280, 40, hair="spike", mouth="flat", hands=((0, 40), (80, 80)), body_h=110, shirt=GRAY)
    s.line((1050, 300), (1050, 340), 4.0)
    socrates_head(s, 1350, 300, 46)
    s.qmark(1350, 160, 0.5)

    s.begin("examined", (40, 480, 1060, 320))
    mr = s.epts(560, 640, 90, 120, 0, 360, n=26)[:-1]
    s.fill(mr, "#d7ecff", 16)
    s.curve(mr + mr[:2], 5.0)
    s.line((560, 760), (560, 790), 5.0)
    socrates_head(s, 560, 620, 36)
    s.magnifier(330, 620, 60, 40)
    s.person(200, 640, 30, hair="bun", mouth="o", hands=((-40, 50), (60, -10)), body_h=80, shirt=PINK, legs=False)
    s.rays(560, 640, 140, 166, 10, 0, 360, YEL, 3.4)
    s.qmark(800, 560, 0.6, TEAL)
    s.heart(880, 640, 22, CORAL)

    s.begin("fine", (1110, 480, 460, 320))
    for k in range(6):
        coin(s, 1160 + (k % 3) * 34, 600 - (k // 3) * 30, 16)
    for k in range(4):
        s.circle(1330 + k * 50, 560, 18, 3.0)
        s.curve([(1310 + k * 50, 610), (1314 + k * 50, 584), (1346 + k * 50, 584), (1350 + k * 50, 610)], 3.0)
    s.arrow((1240, 680), (1320, 700), GRAY, 3.4, 12)
    cup(s, 1400, 780)


def scene3(s):
    s.begin("notwords", (40, 90, 500, 380))
    socrates_head(s, 160, 320, 50)
    for k in range(2):
        x = 330 + k * 110
        s.circle(x, 280, 30, 3.4)
        s.arc(x, 274, 12, 8, 20, 160, 3.0)
        s.arc(x, 300, 14, 10, 200, 340, 3.0)
        s.sweat(x - 14, 296, 0.5)
    s.cross(385, 280, 1.8)

    s.begin("race", (550, 90, 1020, 380))
    s.line((580, 430), (1560, 430), 3.4)
    hooded(s, 760, 290, 30, "#c9ced8")
    for k in range(2):
        s.ell(740 + k * 40, 432, 14, 5, 2.6, GRAY)
    hooded(s, 1280, 290, 30, "#3a3f55", speed=True)
    s.twinkle(1400, 230, 10, CORAL)

    s.begin("caught", (40, 480, 1060, 320))
    socrates_head(s, 200, 620, 38)
    hooded(s, 110, 580, 24, "#c9ced8")
    s.curve([(130, 620), (160, 630), (170, 640)], 3.4)
    for k in range(3):
        s.person(620 + k * 80, 620, 24, hair=("spike", "curly", "short")[k], mouth="frown", hands=((-30, 40), (30, 40)), body_h=60, shirt=(CORAL, ORANGE, "#b9b3d6")[k])
    hooded(s, 520, 560, 30, "#3a3f55", speed=True)
    s.line((60, 772), (1080, 772), 3.4)

    s.begin("more", (1110, 480, 460, 320))
    for k in range(5):
        x = 1170 + k * 80
        s.person(x, 640, 22, hair=("short", "bun", "spike", "curly", "short")[k], mouth="o", hands=((-30, 40), (30, -20)), body_h=60, shirt=(SKY, PINK, YEL, TEAL, CORAL)[k])
        s.qmark(x + 10, 560, 0.35, (SKY, PINK, YEL, TEAL, CORAL)[k])
    s.line((1130, 772), (1560, 772), 3.4)


def scene4(s):
    s.begin("silence", (40, 90, 500, 380))
    socrates_head(s, 200, 320, 52)
    voice(s, 390, 200, 46, present=False)

    s.begin("good", (550, 90, 380, 380))
    s.sun(740, 280, 70, YEL, 12)
    s.dot(716, 268, 7)
    s.dot(764, 268, 7)
    s.arc(740, 290, 22, 14, 20, 160, 4.0)

    s.begin("sleep", (940, 90, 630, 380))
    s.person(1200, 360, 34, hair="short", eye_style="closed", mouth="smile", hands=((-40, 40), (40, 40)), body_h=50, shirt=None, legs=False, cheeks=True)
    bl = [(1120, 420), (1480, 420), (1480, 470), (1120, 470)]
    s.poly(bl, 4.0, closed=True)
    s.fill(bl, SKY)
    outer = s.epts(1440, 180, 40, 40, 60, 300, n=18)
    inner = s.epts(1460, 172, 32, 32, 250, 110, n=14)
    s.curve(outer + inner, 4.0)
    s.fill(outer + inner, YEL)
    for x, y in ((1020, 160), (1120, 220), (1300, 150), (1520, 300)):
        s.star(x, y, 12, YEL, 2.8)
    for k, (x, y, sz) in enumerate(((1250, 300, 16), (1280, 270, 20), (1316, 236, 24))):
        s.poly([(x, y), (x + sz, y), (x, y + sz), (x + sz, y + sz)], 3.0, SKY)

    s.begin("journey", (40, 480, 1530, 320))
    s.curve([(80, 780), (300, 720), (500, 760), (700, 700)], 4.0)
    socrates_head(s, 300, 640, 34)
    s.arrow((350, 700), (420, 700), GRAY, 3.4, 12)
    s.person(860, 620, 34, hair="curly", eye_style="closed", mouth="smile", hands=((60, 40), (80, 0)), body_h=100, shirt="#ffffff", legs=False)
    s.lyre(960, 650, 0.5)
    soldier(s, 1200, 600, 30)
    s.person(1420, 620, 30, hair="spike", mouth="o", hands=((-40, 50), (40, 50)), body_h=90, shirt=SKY, legs=False)
    for x in (900, 1220, 1440):
        s.qmark(x + 30, 520, 0.4, TEAL)
    s.rays(1150, 600, 340, 370, 12, 200, 340, YEL, 3.0)


def scene6(s):
    s.begin("nogood", (40, 90, 500, 380))
    sh = [(270, 150), (390, 190), (380, 320), (270, 420), (160, 320), (150, 190)]
    s.curve(sh, 4.6, closed=True)
    s.fill(sh, "#d9f5f1")
    s.heart(270, 280, 36, CORAL)
    for k in range(3):
        s.arrow((80, 180 + k * 90), (140, 220 + k * 80), GRAY, 3.4, 12)
    s.rays(270, 280, 160, 186, 8, 200, 340, YEL, 3.4)

    s.begin("sons", (550, 90, 560, 380))
    for k, (h, r) in enumerate(((150, 30), (120, 26), (90, 22))):
        x = 650 + k * 110
        s.person(x, 420 - h - r, r, hair=("short", "spike", "bun")[k], mouth="smile", hands=((-r * 1.4, r * 1.6), (r * 1.4, r * 1.6)), body_h=h * 0.6, shirt=(SKY, YEL, PINK)[k])
    for k in range(3):
        coin(s, 1000 + k * 26, 220 - (k % 2) * 14, 14)
    s.heart(1060, 310, 20, CORAL)
    s.line((960, 260), (1100, 260), 2.6, GRAY)
    s.line((1000, 180), (1010, 150), 4.0)
    s.line((560, 422), (1100, 422), 3.4)

    s.begin("depart", (40, 470, 1530, 330))
    door = [(1300, 780), (1300, 520), (1440, 520), (1440, 780)]
    s.fill(door, "#fff1b0", 14)
    s.poly(door, 4.4, closed=True)
    s.rays(1370, 650, 120, 150, 9, 200, 340, YEL, 3.4)
    with s.scaled(0.5, (1180, 560)):
        socrates(s, 1180, 560)
    s.arrow((1210, 760), (1290, 760), TEAL, 3.6, 12)
    jury(s, 140, 620, 7, 2, 56, 60, 16, GRAY)
    s.arrow((560, 740), (480, 740), GRAY, 3.6, 12)
    s.qmark(820, 560, 0.8, ORANGE)
    s.line((60, 782), (1560, 782), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene5(s)
    scene3(s)
    scene4(s)
    scene6(s)
