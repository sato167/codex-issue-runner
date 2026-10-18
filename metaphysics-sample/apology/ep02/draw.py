"""《申辩篇》第 2 集（24b–35d）：牛虻。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from props import *  # noqa: F401,F403,E402


def soc_arm_up(s, cx, cy, k=1.0):
    """给 socrates() 补一只举起指天的手（与 socrates 同一缩放中心使用）。"""
    top = cy + 86
    s.curve([(cx + 70, top + 50), (cx + 120, top - 20), (cx + 128, top - 100)])
    s.curve([(cx + 84, top + 80), (cx + 146, top), (cx + 154, top - 96)])
    s.circle(cx + 141, top - 114, 20)
    s.fill_ell(cx + 141, top - 114, 18, 18, "#ffd9bf")
    s.line((cx + 138, top - 132), (cx + 136, top - 170), 4.6)


def scene1(s):
    s.begin("meletus", (40, 90, 500, 700))
    meletus(s, 180, 380, 40, hands=((-60, 100), (100, 30)))
    socrates_head(s, 420, 330, 40)
    s.bubble(400, 180, 80, 48, (410, 260))
    s.person(380, 172, 14, hair="short", mouth="smile", hands=((-20, 24), (20, 24)), body_h=24, shirt=SKY, legs=False, cheeks=False)
    s.qmark(450, 160, 0.35)
    s.line((60, 712), (520, 712), 3.4)

    s.begin("all", (540, 90, 530, 390))
    raised_crowd(s, 600, 220, 6, 3, 60, 76, 16, GRAY)
    s.check(700, 150, 0.8)
    socrates_head(s, 1000, 300, 36)
    s.cross(1000, 200, 0.8)

    s.begin("horses", (1080, 90, 490, 390))
    horse(s, 1380, 330, 0.75, -1)
    s.person(1170, 330, 28, hair="short", mouth="smile", hands=((-40, 50), (60, 0)), body_h=80, shirt=TEAL, legs=False)
    s.check(1170, 230, 0.7)
    for k in range(3):
        s.person(1300 + k * 70, 220 - (k % 2) * 10, 16, hair="spike", mouth="o", hands=((-24, 26), (24, 26)), body_h=30, shirt=GRAY, legs=False, cheeks=False)
    s.cross(1480, 160, 0.6)

    s.begin("neighbor", (540, 490, 530, 310))
    s.person(660, 640, 30, hair="short", mouth="grin", hands=((-40, 50), (60, 10)), body_h=80, shirt=CORAL, legs=False)
    s.person(920, 640, 30, hair="spike", mouth="frown", hands=((-60, 10), (40, 50)), body_h=80, shirt=GRAY, legs=False)
    cl = s.cloud(790, 560, 40, 22, 6)
    s.curve(cl + cl[:2], 3.0, GRAY)
    s.fill(cl, GRAY)
    s.arrow((730, 610), (850, 610), GRAY, 3.6, 12)
    s.arrow((850, 680), (730, 680), CORAL, 3.6, 12)
    s.qmark(1010, 560, 0.5)

    s.begin("teach", (1080, 490, 490, 310))
    socrates_head(s, 1170, 650, 30)
    s.person(1300, 650, 28, hair="curly", mouth="smile", hands=((-40, 40), (40, 40)), body_h=70, shirt=YEL, legs=False)
    s.bubble(1240, 560, 50, 28, (1270, 610))
    s.heart(1240, 560, 10, PINK)
    s.poly([(1420, 720), (1420, 640), (1470, 610), (1520, 640), (1520, 720)], 3.6, closed=True)
    s.cross(1470, 670, 0.9)
    s.line((1100, 732), (1560, 732), 3.4)


def scene2(s):
    s.begin("atheist", (40, 90, 500, 700))
    meletus(s, 180, 380, 40, hands=((-50, 100), (150, 0)), mouth="frown")
    s.poly([(320, 330), (320, 250), (390, 210), (460, 250), (460, 330)], 4.0, closed=True)
    s.fill([(320, 330), (320, 250), (390, 210), (460, 250), (460, 330)], "#e3eeff")
    s.cross(390, 270, 1.4)
    s.line((60, 712), (520, 712), 3.4)

    s.begin("contra", (540, 90, 530, 380))
    scroll(s, 800, 280, 360, 220)
    voice(s, 800, 280, 46)
    s.arrow((980, 160), (900, 230), CORAL, 4.0, 14)

    s.begin("mule", (540, 470, 1030, 330))
    horse(s, 690, 680, 0.45, -1, "#e8c9a0")
    s.line((830, 640), (870, 640), 5.0)
    s.line((850, 620), (850, 660), 5.0)
    horse(s, 1010, 680, 0.45, -1, "#c9ced8", ears=2.0)
    s.line((1150, 630), (1190, 630), 5.0)
    s.line((1150, 652), (1190, 652), 5.0)
    horse(s, 1340, 680, 0.45, -1, "#d8b88f", ears=1.6)
    s.qmark(1500, 560, 0.6)


def scene3(s):
    s.begin("shame", (40, 90, 500, 700))
    s.person(170, 380, 40, hair="curly", mouth="frown", hands=((-50, 100), (110, -10)), body_h=130, shirt=ORANGE)
    s.line((280, 370), (290, 330), 4.0)
    socrates_head(s, 400, 400, 42)
    s.line((60, 642), (520, 642), 3.4)

    s.begin("post", (540, 90, 530, 700))
    soldier(s, 800, 340, 40)
    s.line((640, 640), (640, 260), 4.0)
    fl = [(640, 260), (720, 280), (640, 300)]
    s.poly(fl, 3.4, closed=True)
    s.fill(fl, CORAL, 8)
    for k in range(3):
        s.arrow((1050, 220 + k * 70), (960, 250 + k * 70), GRAY, 3.2, 12)
    s.line((560, 682), (1060, 682), 3.4)

    s.begin("fear", (1080, 90, 490, 700))
    dr = [(1360, 640), (1360, 300), (1520, 300), (1520, 640)]
    s.poly(dr, 4.4, closed=True)
    s.fill(dr, NAVY)
    s.qmark(1440, 400, 1.0, YEL)
    s.person(1200, 500, 32, hair="spike", mouth="o", big_eyes=True, look=(1, 0), hands=((-70, 0), (-40, 70)), body_h=90, shirt=YEL)
    s.sweat(1240, 470)
    for k in range(3):
        s.line((1100, 520 + k * 24), (1140, 520 + k * 24), 3.0, GRAY)
    s.line((1100, 682), (1560, 682), 3.4)


def scene4(s):
    s.begin("offer", (40, 90, 500, 390))
    gate = [(120, 420), (120, 180), (300, 180), (300, 420)]
    s.poly(gate, 4.2)
    s.poly([(300, 180), (380, 210), (380, 400), (300, 420)], 4.0, closed=True)
    s.fill([(300, 180), (380, 210), (380, 400), (300, 420)], BROWN)
    s.book(210, 290, 110, 60, CREAM)
    s.cross(210, 290, 1.2)
    s.arrow((440, 300), (390, 300), ORANGE, 4.0, 12)

    s.begin("obey", (540, 90, 530, 700))
    beam = [(870, 90), (760, 700), (980, 700)]
    s.fill(beam, "#fff1b0", 16)
    with s.scaled(0.7, (800, 360)):
        socrates(s, 800, 360)
        soc_arm_up(s, 800, 360)
    s.sun(1000, 150, 26, YEL, 8)
    s.line((560, 622), (1060, 622), 3.4)

    s.begin("soul", (1080, 90, 490, 390))
    s.line((1320, 430), (1320, 190), 4.4)
    s.poly([(1280, 430), (1360, 430), (1340, 410), (1300, 410)], 3.6, closed=True)
    s.line((1170, 260), (1470, 200), 4.4)
    for x, y in ((1170, 260), (1470, 200)):
        s.line((x, y), (x - 44, y + 76), 2.6)
        s.line((x, y), (x + 44, y + 76), 2.6)
        pan = s.epts(x, y + 76, 56, 16, 0, 180, n=10)
        s.curve(pan + [pan[0]], 3.8)
    for k in range(3):
        coin(s, 1140 + k * 24, 318 - (k % 2) * 10, 12)
    laurel(s, 1180, 300, 26)
    s.heart(1470, 250, 22, CORAL)
    s.rays(1470, 250, 32, 46, 6, 200, 340, YEL, 3.0)
    s.qmark(1320, 120, 0.5)

    s.begin("bounce", (1080, 490, 490, 310))
    jury(s, 1120, 600, 4, 2, 50, 56, 14, GRAY)
    socrates_head(s, 1470, 640, 34)
    s.curve([(1340, 600), (1400, 580), (1420, 610)], 4.0, CORAL)
    s.arrow((1420, 640), (1330, 680), CORAL, 4.0, 14)
    s.arc(1470, 640, 60, 60, 120, 240, 4.0, TEAL)


def scene5(s):
    s.begin("horse", (80, 160, 1120, 640))
    horse(s, 700, 520, 1.5, -1, "#e8c9a0", sleepy=True)
    for k, (x, y, sz) in enumerate(((470, 260, 20), (510, 220, 26), (560, 170, 32))):
        s.poly([(x, y), (x + sz, y), (x, y + sz), (x + sz, y + sz)], 3.4, SKY)
    s.line((120, 722), (1180, 722), 3.4)

    s.begin("sting", (80, 160, 1120, 640))
    gadfly(s, 520, 380, 1.4)
    s.circle(448, 316, 14, 3.4)
    s.dot(444, 316, 7)
    for a in (200, 240, 280, 320):
        t = math.radians(a)
        s.line((448 + 30 * math.cos(t), 316 + 30 * math.sin(t)), (448 + 48 * math.cos(t), 316 + 48 * math.sin(t)), 3.4, CORAL)

    s.begin("swat", (1100, 160, 470, 640))
    big_hand(s, 1340, 360, 1.0)
    for k in range(3):
        s.line((1260 + k * 60, 270), (1260 + k * 60, 300), 3.4, GRAY)
    s.poly([(1300, 520), (1330, 500), (1360, 530), (1390, 505)], 3.0, NAVY)
    for k, (x, y, sz) in enumerate(((1320, 640, 18), (1360, 600, 24), (1410, 560, 30))):
        s.poly([(x, y), (x + sz, y), (x, y + sz), (x + sz, y + sz)], 3.4, SKY)
    s.qmark(1500, 600, 0.5, GRAY)


def scene6(s):
    s.begin("voice", (40, 90, 500, 390))
    socrates_head(s, 200, 320, 50)
    voice(s, 380, 200, 46)
    palm = [(355, 180), (405, 180), (410, 230), (350, 230)]
    s.poly(palm, 3.4, CORAL, closed=True)
    s.line((300, 250), (330, 230), 3.0, TEAL)

    s.begin("politics", (540, 90, 530, 390))
    s.poly([(620, 260), (800, 170), (980, 260)], 4.0, closed=True)
    for x in (650, 720, 880, 950):
        s.line((x, 262), (x, 420), 3.6)
    s.line((610, 262), (990, 262), 4.0)
    s.line((610, 422), (990, 422), 4.0)
    oct_ = [(800 + 44 * math.cos(math.radians(22.5 + i * 45)), 340 + 44 * math.sin(math.radians(22.5 + i * 45))) for i in range(8)]
    s.poly(oct_, 4.0, closed=True)
    s.fill(oct_, CORAL, 9)
    s.line((780, 340), (820, 340), 6.0, "#ffffff")
    socrates_head(s, 1040, 400, 24)

    s.begin("generals", (1080, 90, 490, 390))
    raised_crowd(s, 1130, 270, 5, 1, 56, 70, 16, GRAY)
    socrates_head(s, 1480, 300, 34)
    s.cross(1480, 190, 0.8)
    s.line((1110, 372), (1560, 372), 3.4)

    s.begin("leon", (40, 480, 900, 320))
    for k in range(4):
        x = 420 + k * 80
        s.person(x, 640, 22, hair="spike", mouth="flat", hands=((-30, 40), (30, 40)), body_h=60, shirt=GRAY)
    s.arrow((760, 650), (880, 650), GRAY, 4.0, 14)
    socrates_head(s, 250, 640, 30)
    s.arrow((200, 700), (110, 700), TEAL, 4.0, 14)
    s.house(90, 760, 90, 70)
    s.line((40, 772), (900, 772), 3.4)

    s.begin("children", (940, 480, 630, 320))
    for k in range(3):
        x = 1060 + k * 120
        s.person(x, 640, 26, hair=("bun", "short", "bun")[k], mouth="frown", eye_style="closed", hands=((-36, 30), (36, 30)), body_h=60, shirt=(PINK, SKY, YEL)[k])
        s.sweat(x - 14, 650, 0.6)
        s.sweat(x + 14, 650, 0.6)
    s.cross(1180, 600, 2.4)
    s.line((960, 772), (1560, 772), 3.4)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
    scene5(s)
    scene6(s)
