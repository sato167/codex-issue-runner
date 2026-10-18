"""《申辩篇》第 1 集（17a–24b）：我知道我无知。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from props import *  # noqa: F401,F403,E402


def scene1(s):
    s.begin("court", (40, 100, 600, 690))
    for x in (90, 570):
        s.line((x - 22, 170), (x - 22, 640))
        s.line((x + 22, 170), (x + 22, 640))
        s.poly([(x - 34, 150), (x + 34, 150), (x + 34, 170), (x - 34, 170)], 3.6, closed=True)
    s.line((50, 140), (610, 140), 4.4)
    podium(s, 330, 680, 260, 50)
    with s.scaled(0.78, (330, 330)):
        socrates(s, 330, 330)
    s.line((40, 682), (620, 682), 3.4)

    s.begin("charges", (650, 90, 470, 400))
    scroll(s, 885, 280, 380, 240)
    s.person(800, 250, 24, hair="short", mouth="frown", hands=((-34, 40), (34, 40)), body_h=50, shirt=SKY, legs=False)
    s.line((760, 330), (840, 210), 4.0, CORAL)
    s.poly([(920, 330), (920, 260), (970, 230), (1020, 260), (1020, 330)], 3.6, closed=True)
    s.fill([(920, 330), (920, 260), (970, 230), (1020, 260), (1020, 330)], "#e3eeff", 9)
    s.qmark(970, 260, 0.45)
    voice(s, 1040, 210, 18)

    s.begin("jury", (640, 480, 930, 320))
    jury(s, 700, 560, 13, 3, 62, 62, 18, None)
    s.line((660, 760), (1560, 760), 3.4)

    s.begin("plain", (1130, 90, 440, 400))
    b1 = s.bubble(1260, 210, 120, 70, (1200, 300))
    for k in range(3):
        s.spiral(1210 + k * 50, 210, 18, 1.6, 3.0, ORANGE)
    s.twinkle(1360, 160, 10, YEL)
    s.cross(1260, 210, 1.6)
    s.bubble(1440, 380, 110, 64, (1380, 460))
    s.check(1440, 380, 1.1)


def scene2(s):
    s.begin("rumor", (40, 90, 580, 400))
    for k, (x, y) in enumerate(((140, 380), (300, 330), (460, 390))):
        s.circle(x, y, 30, 3.4, GRAY)
        s.curve([(x - 36, y + 80), (x - 30, y + 36), (x + 30, y + 36), (x + 36, y + 80)], 3.4, GRAY)
        bx, by = x + (40 if k % 2 else -20), y - 130 + (k % 2) * 20
        s.bubble(bx, by, 70, 44, (x + 10, y - 40))
        for j in range(3):
            s.dot(bx - 22 + j * 22, by, 6)
    s.line((60, 472), (600, 472), 3.4)

    s.begin("basket", (630, 70, 480, 720))
    s.line((870, 80), (870, 330), 3.4)
    s.line((870, 80), (1060, 80), 4.4)
    s.line((1060, 80), (1060, 780), 4.4)
    socrates_head(s, 870, 390, 50)
    bk = [(760, 460), (980, 460), (950, 560), (790, 560)]
    s.poly(bk, 4.2, closed=True)
    s.fill(bk, BROWN)
    for x in (810, 850, 890, 930):
        s.line((x, 462), (x + 6, 556), 2.4)
    for k in (-1, 1):
        s.line((870, 330), (870 + k * 110, 460), 3.0)
    s.sun(720, 180, 26, YEL, 8)
    for x, y in ((990, 220), (1020, 160), (760, 300)):
        s.star(x, y, 12, YEL, 2.8)
    mask(s, 760, 690, 34, True)
    mask(s, 860, 700, 34, False, SKY)
    s.line((650, 772), (1100, 772), 3.4)

    s.begin("nofee", (1120, 90, 450, 700))
    s.person(1260, 270, 36, hair="curly", mouth="grin", hands=((-50, 90), (70, 70)), body_h=120, shirt=ORANGE)
    bag = [(1310, 330), (1380, 330), (1400, 400), (1290, 400)]
    s.curve(bag + bag[:1], 4.0)
    s.fill(bag, BROWN)
    for k in range(3):
        coin(s, 1420 + k * 24, 300 - k * 30, 14)
    socrates_head(s, 1400, 560, 40)
    for sx in (-1, 1):
        s.circle(1400 + sx * 90, 650, 14, 3.4)
        s.curve([(1400 + sx * 40, 640), (1400 + sx * 70, 652), (1400 + sx * 80, 650)], 3.6)
    coin(s, 1490, 560, 18)
    s.cross(1490, 560, 0.8)


def scene3(s):
    s.begin("chaerephon", (40, 280, 440, 520))
    s.person(240, 470, 34, hair="spike", look=(1, 0), mouth="o", big_eyes=True, hands=((-80, 30), (70, 90)), body_h=120, shirt=TEAL, legs=False)
    s.line((220, 624), (180, 700), 4.2)
    s.line((260, 624), (320, 690), 4.2)
    for k in range(4):
        s.line((60, 470 + k * 34), (120, 470 + k * 34), 3.2, GRAY)
    s.line((60, 712), (460, 712), 3.4)

    s.begin("delphi", (470, 80, 640, 710))
    s.poly([(560, 260), (790, 150), (1020, 260)], 4.0, closed=True)
    s.fill([(576, 256), (790, 160), (1004, 256)], "#e3eeff")
    for x in (600, 680, 900, 980):
        s.line((x - 14, 262), (x - 14, 560), 3.6)
        s.line((x + 14, 262), (x + 14, 560), 3.6)
    s.line((560, 262), (1020, 262), 4.0)
    pythia(s, 790, 740)
    s.person(600, 650, 26, hair="spike", look=(1, -0.5), mouth="o", hands=((-40, 40), (30, -30)), body_h=60, shirt=TEAL, legs=False)
    s.qmark(640, 540, 0.5)
    s.line((480, 742), (1100, 742), 3.4)

    s.begin("answer", (470, 80, 640, 710))
    s.bubble(960, 400, 90, 70, (860, 480))
    digit(s, "0", 940, 360, 80, CORAL, 7.0)

    s.begin("puzzled", (1120, 110, 450, 690))
    with s.scaled(0.75, (1340, 400)):
        socrates(s, 1340, 400)
    s.qmark(1460, 210, 0.9)
    s.qmark(1520, 280, 0.6, ORANGE)
    s.line((1150, 640), (1550, 640), 3.4)


def scene4(s):
    s.begin("politician", (40, 80, 500, 400))
    s.person(170, 250, 40, hair="short", mouth="grin", hands=((-60, 60), (64, 20)), body_h=130, shirt="#ffffff", legs=False)
    laurel(s, 170, 214, 44)
    s.line((134, 300), (210, 420), 7.0, CORAL)
    s.ground(60, 520, 452)

    s.begin("talk", (40, 80, 500, 400))
    socrates_head(s, 430, 260, 36)
    s.bubble(260, 130, 70, 40, (210, 190))
    for k in range(3):
        s.dot(234 + k * 26, 130, 6)
    cl = s.bubble(380, 140, 50, 34, (410, 200))
    s.qmark(380, 120, 0.35)

    s.begin("insight", (550, 80, 520, 400))
    s.circle(680, 300, 50)
    s.dot(664, 292, 6)
    s.dot(696, 292, 6)
    s.arc(680, 314, 14, 8, 20, 160, 3.2)
    s.bulb(680, 170, 30, lit=False)
    s.poly([(668, 150), (684, 170), (672, 186), (690, 200)], 3.4, CORAL)
    s.cross(680, 170, 1.3)
    socrates_head(s, 940, 300, 46)
    s.qmark(940, 150, 0.7, TEAL)
    s.rays(940, 175, 46, 66, 8, 0, 360, YEL, 3.4)
    s.ground(570, 1060, 452)

    s.begin("slightly", (1080, 80, 490, 400))
    s.line((1120, 420), (1540, 420), 4.0)
    for x, h, c in ((1210, 200, GRAY), (1420, 214, TEAL)):
        bar = [(x - 50, 420), (x - 50, 420 - h), (x + 50, 420 - h), (x + 50, 420)]
        s.poly(bar, 4.0, closed=True)
        s.fill(bar, c)
    s.magnifier(1420, 196, 34, 40, glass=False)
    s.arrow((1300, 208), (1360, 208), CORAL, 3.4, 10)

    s.begin("poets", (40, 480, 760, 320))
    s.person(170, 620, 36, hair="curly", eye_style="closed", mouth="smile", hands=((60, 50), (90, 10)), body_h=100, shirt=PINK, legs=False)
    s.lyre(300, 640, 0.6)
    for k in range(3):
        s.twinkle(240 + k * 50, 530 - (k % 2) * 20, 10, YEL)
    socrates_head(s, 600, 650, 34)
    s.bubble(470, 560, 70, 40, (560, 610))
    s.qmark(470, 540, 0.4)
    s.note(380, 560, SKY)
    s.line((60, 772), (780, 772), 3.4)

    s.begin("craftsmen", (800, 480, 770, 320))
    s.person(940, 630, 36, hair="spike", mouth="grin", hands=((-60, 50), (70, 30)), body_h=100, shirt=ORANGE, legs=False)
    apron = [(910, 690), (970, 690), (976, 760), (904, 760)]
    s.poly(apron, 3.4, closed=True)
    s.fill(apron, BROWN, 8)
    s.line((1010, 660), (1060, 600), 5.0, BROWN)
    hd = s.rot_rect(1040, 570, 50, 24, -40, (1065, 582))
    s.poly(hd, 3.6, closed=True)
    s.fill(hd, GRAY, 8)
    cl = s.cloud(1260, 560, 150, 70, 9)
    s.curve(cl + cl[:2], 3.8)
    g = s.epts(1220, 560, 34, 34, 0, 360, n=16)[:-1]
    s.curve(g + g[:1], 3.4)
    s.fill(g, "#d7ecff", 8)
    s.ell(1220, 560, 34, 12, 2.4)
    s.poly([(1300, 580), (1300, 540), (1320, 556), (1340, 530), (1360, 556), (1380, 540), (1380, 580)], 3.6, closed=True)
    s.fill([(1300, 580), (1300, 540), (1320, 556), (1340, 530), (1360, 556), (1380, 540), (1380, 580)], YEL, 8)
    s.dot(1000, 600, 6)
    s.dot(1040, 610, 8)
    socrates_head(s, 1480, 700, 30)
    s.qmark(1520, 610, 0.45)
    s.line((820, 772), (1560, 772), 3.4)


def scene5(s):
    s.begin("meaning", (40, 80, 500, 400))
    s.line((280, 440), (280, 200), 4.4)
    s.poly([(240, 440), (320, 440), (300, 420), (260, 420)], 3.6, closed=True)
    s.line((120, 250), (440, 190), 4.4)
    for x, y in ((120, 250), (440, 190)):
        s.line((x, y), (x - 44, y + 80), 2.6)
        s.line((x, y), (x + 44, y + 80), 2.6)
        pan = s.epts(x, y + 80, 56, 16, 0, 180, n=10)
        s.curve(pan + [pan[0]], 3.8)
    s.circle(120, 318, 12, 3.4)
    s.fill_ell(120, 318, 10, 10, GRAY)
    s.star_glow(440, 236, 22)

    s.begin("example", (550, 80, 520, 400))
    podium(s, 810, 440, 200, 60)
    socrates_head(s, 810, 300, 46)
    beam = [(810, 90), (720, 380), (900, 380)]
    s.fill(beam, "#fff1b0", 16)
    s.arrow((980, 160), (880, 260), ORANGE, 4.0, 14)
    s.qmark(1000, 130, 0.5, TEAL)

    s.begin("enemies", (1080, 80, 490, 400))
    for k, (x, y) in enumerate(((1170, 300), (1310, 260), (1450, 310))):
        s.person(x, y, 32, hair=("short", "curly", "spike")[k], mouth="frown", hands=((-44, 50), (44, 50)), body_h=70, shirt=(CORAL, ORANGE, CORAL)[k], legs=False)
        s.line((x - 20, y - 18), (x - 6, y - 12), 3.0)
        s.line((x + 6, y - 12), (x + 20, y - 18), 3.0)
        steam(s, x + 30, y - 46, 9)
    s.circle(1310, 150, 36, 3.6)
    s.fill_ell(1310, 150, 34, 34, PINK)
    s.line((1354, 110), (1390, 80), 3.4)
    s.rays(1310, 150, 46, 66, 8, 0, 360, CORAL, 3.0)

    s.begin("youth", (40, 480, 1530, 320))
    with s.scaled(0.55, (300, 560)):
        socrates(s, 300, 560)
    for k in range(3):
        s.person(470 + k * 110, 640, 26, hair=("short", "bun", "spike")[k], mouth="o", hands=((-36, 40), (36, 30)), body_h=70, shirt=(SKY, PINK, YEL)[k])
    s.person(1100, 600, 40, hair="curly", mouth="frown", hands=((-110, -10), (60, 80)), body_h=110, shirt=CORAL)
    steam(s, 1140, 540, 11)
    steam(s, 1060, 540, 9)
    s.arrow((980, 590), (420, 560), CORAL, 4.0, 16)
    for k in range(3):
        s.qmark(820 + k * 50, 560, 0.4, (SKY, PINK, YEL)[k])
    s.line((60, 782), (1560, 782), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
    scene5(s)
