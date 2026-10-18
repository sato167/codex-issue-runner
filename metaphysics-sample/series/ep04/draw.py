"""第 4 集 · 卷四（Γ）：存在之为存在、不矛盾律。"""
from sketch import *  # noqa: F401,F403


def fish(s, x, y, k=1.0, color=SKY):
    body = s.epts(x, y, 34 * k, 18 * k, 0, 360, n=18)[:-1]
    s.curve(body + body[:1], 3.6)
    s.fill(body, color, 9)
    tail = [(x - 32 * k, y), (x - 56 * k, y - 16 * k), (x - 52 * k, y + 16 * k)]
    s.poly(tail, 3.4, closed=True)
    s.fill(tail, color, 8)
    s.dot(x + 18 * k, y - 4 * k, 4)


def scene1(s):
    s.begin("aristotle", (40, 140, 400, 650))
    with s.scaled(0.72, (210, 430)):
        s.aristotle(210, 430, wave=True)
    s.ground(60, 400, 690)

    s.begin("everything", (430, 90, 580, 480))
    big = s.epts(720, 330, 210, 210, 0, 360, n=40)[:-1]
    s.fill(big, "#fff3c4", 16)
    s.curve(big + big[:2], 4.4)
    s.tree(640, 470, 140, GREEN)
    fish(s, 810, 270, 1.0)
    s.star(680, 210, 26, YEL)
    s.house(810, 450, 110, 70)
    cl = s.cloud(600, 300, 40, 20, 6)
    s.curve(cl + cl[:2], 3.2)

    s.begin("experts", (1020, 110, 560, 480))
    s.person(1150, 400, 36, hair="short", mouth="smile", hands=((-56, 80), (56, 20)), body_h=110, shirt=SKY)
    tri = [(1196, 400), (1236, 400), (1206, 350)]
    s.poly(tri, 3.6, closed=True)
    s.fill(tri, YEL, 8)
    s.person(1430, 400, 36, hair="bun", mouth="smile", hands=((-56, 80), (56, 80)), body_h=110, shirt="#ffffff")
    s.curve([(1400, 436), (1394, 480), (1420, 506), (1446, 480), (1460, 436)], 3.2)
    s.circle(1420, 512, 8, 3.0)
    for dx, dy in ((0, -10), (0, 10), (-10, 0), (10, 0)):
        s.line((1452, 520), (1452 + dx, 520 + dy), 4.0, CORAL)
    for x, c in ((1150, SKY), (1430, CORAL)):
        wedge = [(x, 260)] + s.epts(x, 260, 60, 60, -120, -60, n=6)
        s.poly(wedge + [(x, 260)], 3.6)
        s.fill(wedge, c, 9)

    s.begin("whole", (430, 90, 580, 480))
    for a in (0, 72, 144, 216, 288):
        t = math.radians(a)
        for k in range(5):
            r0, r1 = 20 + k * 40, 38 + k * 40
            s.line((720 + r0 * math.cos(t), 330 + r0 * math.sin(t)), (720 + r1 * math.cos(t), 330 + r1 * math.sin(t)), 2.6, GRAY)
    s.circle(720, 330, 232, 7.0, TEAL)
    s.rays(720, 330, 248, 272, 16, 0, 360, YEL, 4.0)


def scene2(s):
    s.begin("word", (40, 110, 480, 360))
    s.bubble(260, 250, 190, 110, (180, 400))
    s.dot(260, 250, 12)
    for a in range(0, 360, 60):
        t = math.radians(a + 20)
        s.arrow((260 + 22 * math.cos(t), 250 + 22 * math.sin(t)), (260 + 120 * math.cos(t), 250 + 70 * math.sin(t)),
                (CORAL, SKY, ORANGE, TEAL, CORAL, SKY)[a // 60], 3.6, 12)

    s.begin("heart", (560, 330, 480, 300))
    s.heart(800, 470, 66, CORAL)
    s.dot(780, 450, 6)
    s.dot(820, 450, 6)
    s.arc(800, 470, 16, 10, 20, 160, 3.4)

    s.begin("three", (540, 110, 520, 690))
    ap = [(620, 250), (596, 240), (570, 256), (566, 290), (586, 320), (620, 330), (654, 320), (674, 290), (670, 256), (644, 240)]
    s.curve(ap, 4.0, closed=True)
    s.fill(ap, CORAL)
    s.line((620, 250), (626, 226), 3.4)
    leaf = [(626, 232), (650, 214), (664, 228), (636, 240)]
    s.curve(leaf, 3.2, closed=True)
    s.fill(leaf, GREEN, 8)
    s.circle(980, 280, 44)
    s.dot(964, 272, 6)
    s.dot(996, 272, 6)
    s.arc(980, 290, 18, 12, 20, 160, 3.6)
    s.cheeks(980, 296, 28)
    for k in range(3):
        s.twinkle(1040 + k * 8, 220 + k * 40, 8, ORANGE)
    s.circle(800, 650, 26)
    s.line((800, 676), (790, 730), 4.0)
    s.curve([(796, 694), (770, 700), (754, 684)], 3.8)
    s.curve([(796, 694), (826, 690), (840, 670)], 3.8)
    s.curve([(790, 730), (770, 752), (752, 754)], 3.8)
    s.curve([(790, 730), (816, 748), (826, 772)], 3.8)
    for k in range(3):
        s.line((720, 660 + k * 20), (744, 660 + k * 20), 3.0, GRAY)

    s.begin("arrows", (540, 110, 520, 690))
    s.arrow((664, 330), (744, 410), TEAL, 4.4, 16)
    s.arrow((940, 330), (858, 410), TEAL, 4.4, 16)
    s.arrow((800, 620), (800, 550), TEAL, 4.4, 16)

    s.begin("substance", (1080, 110, 500, 690))
    cube = [(1280, 440), (1360, 440), (1360, 520), (1280, 520)]
    s.poly(cube, 4.4, closed=True)
    s.poly([(1280, 440), (1306, 414), (1386, 414), (1360, 440)], 3.8)
    s.poly([(1360, 520), (1386, 494), (1386, 414)], 3.8)
    s.fill(cube, ORANGE)
    pal = s.epts(1180, 260, 54, 40, 0, 360, n=20)[:-1]
    s.curve(pal + pal[:1], 3.8)
    for (dx, dy, c) in ((-24, -10, CORAL), (0, -18, YEL), (24, -8, SKY), (10, 14, GREEN)):
        s.fill_ell(1180 + dx, 260 + dy, 9, 9, c)
    rl = [(1420, 240), (1540, 240), (1540, 276), (1420, 276)]
    s.poly(rl, 3.8, closed=True)
    s.fill(rl, YEL, 9)
    for k in range(7):
        s.line((1432 + k * 16, 240), (1432 + k * 16, 254 if k % 2 else 262), 2.4)
    s.clock(1180, 680, 46, "#e3f2ff")
    pin = [(1480, 720)] + s.epts(1480, 650, 36, 36, 150, 390, n=14)
    s.curve(pin + [(1480, 720)], 4.0)
    s.fill(pin, CORAL)
    s.circle(1480, 650, 12, 3.2)
    for a, b in (((1220, 300), (1290, 410)), ((1460, 290), (1370, 410)), ((1214, 640), (1290, 540)), ((1450, 620), (1370, 540))):
        s.arrow(a, b, TEAL, 4.0, 14)


def scene3(s):
    s.begin("foundation", (40, 380, 540, 420))
    s.house(300, 640, 220, 130)
    for row, y in enumerate((640, 680, 720)):
        for i in range(5 - (row == 0)):
            x = 90 + i * 92 + (46 if row == 0 else 0) - (0 if row else 0)
            b = [(x, y), (x + 88, y), (x + 88, y + 38), (x, y + 38)]
            s.poly(b, 3.4, closed=True)
            s.fill(b, YEL if (row == 2 and i == 2) else "#dfe3ea", 10)
    s.rays(320, 739, 60, 80, 6, 20, 160, YEL, 3.6)

    s.begin("lamp", (600, 100, 470, 460))
    s.circle(830, 270, 70)
    left = s.epts(830, 270, 66, 66, 90, 270, n=14)
    s.fill(left, YEL)
    s.rays(830, 270, 86, 116, 5, 120, 240, ORANGE)
    s.line((830, 200), (830, 340), 2.6, GRAY)
    s.poly([(800, 340), (860, 340), (856, 390), (804, 390)], 3.8, closed=True)
    s.line((806, 365), (854, 365), 2.6)
    s.circle(830, 300, 150, 7.0, CORAL)
    s.line((724, 406), (936, 194), 7.0, CORAL)

    s.begin("doors", (1100, 100, 480, 460))
    for x0 in (1140, 1360):
        s.poly([(x0, 470), (x0, 210), (x0 + 160, 210), (x0 + 160, 470)], 4.2)
    od = [(1140, 470), (1140, 210), (1210, 236), (1210, 450)]
    s.poly(od, 4.0, closed=True)
    s.fill(od, BROWN)
    cd = [(1362, 468), (1362, 212), (1518, 212), (1518, 468)]
    s.fill(cd, BROWN)
    s.circle(1500, 340, 8, 3.2)
    s.check(1220, 150, 0.8)
    s.check(1440, 150, 0.8)
    s.line((1330, 200), (1330, 480), 3.0, GRAY)

    s.begin("tablet", (620, 560, 940, 240))
    s.tablet(1000, 690, 300, 170)
    s.arrow((840, 720), (600, 720), GRAY, 3.6, 14)


def scene4(s):
    s.begin("denier", (40, 300, 400, 500))
    s.person(210, 440, 44, hair="spike", mouth="frown", hands=((-22, 104), (22, 104)), body_h=150, shirt=GRAY)
    s.line((168, 546), (252, 546), 4.0)
    s.line((180, 406), (200, 414), 3.4)
    s.line((220, 414), (240, 406), 3.4)
    s.ground(60, 400, 680)

    s.begin("shh", (440, 140, 400, 650))
    with s.scaled(0.72, (620, 430)):
        s.aristotle(620, 430, wave=True)
    s.ground(460, 820, 690)

    s.begin("bubble", (40, 40, 540, 340))
    s.bubble(260, 200, 170, 100, (220, 360))
    ap = [(260, 190), (236, 180), (210, 196), (206, 228), (226, 256), (260, 266), (294, 256), (314, 228), (310, 196), (284, 180)]
    s.curve(ap, 3.8, closed=True)
    s.fill(ap, CORAL)
    s.line((260, 190), (266, 166), 3.4)

    s.begin("already", (40, 40, 800, 380))
    s.arrow((440, 200), (540, 200), TEAL, 4.4, 16)
    s.tablet(660, 210, 190, 130)
    s.rays(660, 210, 120, 146, 8, 180, 360, YEL, 3.6)

    s.begin("well", (860, 280, 720, 520))
    s.ell(1300, 600, 110, 30, 4.4)
    s.curve([(1190, 600), (1192, 700), (1300, 730), (1408, 700), (1410, 600)], 4.4)
    for k in range(4):
        s.line((1200 + k * 70, 640 + (k % 2) * 30), (1240 + k * 70, 642 + (k % 2) * 30), 2.6, GRAY)
    s.fill(s.epts(1300, 600, 100, 24, 0, 360, n=20)[:-1], NAVY, 9)
    s.line((1210, 600), (1210, 450), 4.0)
    s.line((1390, 600), (1390, 450), 4.0)
    roof = [(1180, 460), (1300, 400), (1420, 460)]
    s.poly(roof, 4.2, closed=True)
    s.fill(roof, CORAL)
    s.person(990, 560, 34, mouth="o", look=(1, 0.3), hands=((-50, 70), (50, 60)), body_h=100, shirt=TEAL)
    pts = s.epts(1300, 640, 230, 150, 160, 380, n=24)
    for i in range(0, len(pts) - 1, 2):
        s.line(pts[i], pts[i + 1], 3.6, ORANGE)
    s.arrow(pts[-2], pts[-1], ORANGE, 3.6, 14)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
