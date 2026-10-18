"""第 2 集 · 卷二（α）：真理难也不难。"""
from sketch import *  # noqa: F401,F403


def domino(s, x, ang, color=None):
    """立在 y=380 地面上的多米诺骨牌，绕右下角向右倾倒 ang 度。"""
    pts = s.rot_rect(x, 270, 34, 110, ang, (x + 34, 380))
    s.poly(pts, 3.8, closed=True)
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    a = math.radians(ang)
    for d in (-22, 22):
        s.dot(cx - d * math.sin(a), cy + d * math.cos(a), 6)
    if color:
        s.fill(pts, color, 9)
    return pts


def scene1(s):
    s.begin("mountain", (50, 100, 440, 500))
    peak = [(70, 560), (200, 300), (250, 360), (330, 170), (470, 560)]
    s.poly(peak, 4.2)
    snow = [(296, 236), (330, 170), (364, 240), (346, 228), (330, 244), (313, 228)]
    s.poly(snow, 3.4, closed=True)
    s.fill(snow, "#e3eeff", 9)
    s.line((330, 172), (330, 118), 3.6)
    flag = [(330, 118), (374, 132), (330, 148)]
    s.poly(flag, 3.4, closed=True)
    s.fill(flag, CORAL, 9)
    for k in range(7):
        x0, y0 = 150 + k * 22, 540 - k * 44
        s.line((x0, y0), (x0 + 14 if k % 2 == 0 else x0 - 4, y0 - 26), 3.0, ORANGE)
    s.circle(262, 420, 10, 3.2)
    s.line((262, 430), (258, 462), 3.2)
    s.line((258, 446), (276, 432), 3.0)
    s.line((258, 462), (248, 478), 3.0)
    s.line((258, 462), (270, 478), 3.0)
    s.ground(50, 490, 562)

    s.begin("archer", (480, 280, 380, 500))
    s.person(600, 440, 42, hair="short", look=(1, 0), mouth="flat", hands=((40, 55), (118, 50)), body_h=140, shirt=TEAL)
    s.curve([(718, 395), (752, 490), (718, 585)], 4.6)
    s.poly([(718, 395), (640, 495), (718, 585)], 2.6)
    s.arrow((640, 495), (800, 492), INK, 3.8, 18)
    s.ground(500, 820, 668)

    s.begin("door", (850, 120, 470, 660))
    frame = [(900, 170), (1280, 170), (1280, 740), (900, 740)]
    s.poly(frame, 4.6, closed=True)
    s.fill(frame, "#f6d7a7", 16)
    s.line((1090, 170), (1090, 740), 4.0)
    for y in (300, 440, 600):
        s.line((914, y), (1076, y + 2), 2.6, BROWN)
        s.line((1104, y + 2), (1266, y), 2.6, BROWN)
    s.circle(1068, 470, 9, 3.4)
    s.circle(1112, 470, 9, 3.4)
    for k in range(5):
        s.line((808 + k * 22, 500 + k * 12), (820 + k * 22, 506 + k * 12), 3.0, GRAY)
    s.line((934, 560), (1004, 556), 4.0)
    s.poly([(934, 560), (918, 548), (926, 560), (918, 572)], 3.0, closed=True)
    s.fill([(934, 560), (918, 548), (926, 560), (918, 572)], CORAL, 7)
    s.rays(1006, 556, 14, 30, 5, -60, 60, ORANGE)

    s.begin("bullseye", (1000, 200, 320, 320))
    for r, c in ((30, CORAL), (19, "#fff4e0"), (8, CORAL)):
        s.circle(1180, 330, r, 3.6)
        s.fill_ell(1180, 330, r - 2, r - 2, c)
    for x, y in ((1110, 270), (1248, 392), (1140, 420), (1252, 280)):
        s.line((x - 40, y + 4), (x, y), 3.6)
        s.poly([(x - 40, y + 4), (x - 52, y - 6), (x - 46, y + 4), (x - 52, y + 14)], 2.8, closed=True)

    s.begin("sweat", (480, 280, 380, 500))
    s.sweat(658, 392)
    s.sweat(670, 420, 0.8)
    for k in range(3):
        s.curve([(570 + k * 26, 372), (576 + k * 26, 360), (570 + k * 26, 348)], 3.0, CORAL)
    s.line((574, 418), (592, 426), 3.0)
    s.line((626, 426), (644, 418), 3.0)


def scene2(s):
    s.begin("mirror", (40, 140, 420, 620))
    s.person(180, 380, 42, hair="curly", look=(1, 0), mouth="o", hands=((-6, 72), (110, 40)), body_h=150, shirt=YEL)
    s.ell(312, 344, 40, 54, 4.2)
    s.fill_ell(312, 344, 36, 50, "#d7ecff")
    s.line((304, 398), (292, 420), 4.0)
    s.circle(312, 340, 18, 3.0)
    s.dot(305, 336, 4)
    s.dot(319, 336, 4)
    s.ell(312, 350, 4, 5, 2.6)
    s.arrow((150, 520), (176, 456), CORAL, 3.4, 12)
    s.ground(60, 420, 614)

    s.begin("bat", (460, 240, 380, 300))
    bx, by = 640, 400
    body = s.epts(bx, by, 26, 36, 0, 360, n=20)[:-1]
    for sx in (-1, 1):
        wing = [(bx + sx * 22, by - 20), (bx + sx * 70, by - 58), (bx + sx * 140, by - 66), (bx + sx * 122, by - 30),
                (bx + sx * 104, by - 8), (bx + sx * 80, by - 16), (bx + sx * 60, by + 10), (bx + sx * 24, by + 6)]
        s.poly(wing, 3.8, closed=True)
        s.fill(wing, "#9b93c9")
    s.curve(body + body[:1], 4.0)
    s.fill(body, "#6f6799")
    for sx in (-1, 1):
        s.poly([(bx + sx * 8, by - 32), (bx + sx * 18, by - 58), (bx + sx * 24, by - 26)], 3.4)
        s.circle(bx + sx * 11, by - 14, 8, 3.0)
    s.poly([(bx - 6, by + 4), (bx - 3, by + 12), (bx, by + 4), (bx + 3, by + 12), (bx + 6, by + 4)], 2.6)

    s.begin("sun", (600, 60, 560, 480))
    s.sun(980, 190, 70, YEL, 12)
    s.ell(640, 336, 54, 13, 2.6, ORANGE)
    for k, x in enumerate((596, 640, 684)):
        s.star(x, 336 + (8 if k == 1 else -4), 9, YEL, 2.6)
    for sx in (-1, 1):
        s.poly([(640 + sx * 4, by - 14 - 7), (640 + sx * 16, by - 14), (640 + sx * 4, by - 14 + 7)], 3.4, CORAL)

    s.begin("dazzle", (1100, 90, 470, 380))
    s.book(1250, 210, 190, 110, CREAM)
    s.rays(1250, 210, 112, 150, 12, 0, 360, YEL, 4.6)
    s.person(1460, 270, 32, hair="short", mouth="o", hands=((-50, 30), (50, 30)), body_h=90, eye_style="spiral", legs=False)

    s.begin("bricks", (460, 520, 680, 270))
    for row, (n, y) in enumerate(((6, 742), (5, 708), (3, 674))):
        for i in range(n):
            x = 520 + i * 84 + (row % 2) * 42
            b = [(x, y), (x + 80, y), (x + 80, y + 30), (x, y + 30)]
            s.poly(b, 3.4, closed=True)
            if (i + row) % 2 == 0:
                s.fill(b, "#f4a28c", 9)
    nb = [(866, 594), (946, 594), (946, 624), (866, 624)]
    s.poly(nb, 3.8, closed=True)
    s.fill(nb, CORAL, 9)
    for x in (880, 906, 932):
        s.line((x, 566), (x, 584), 3.0, GRAY)

    s.begin("glasses", (1130, 470, 440, 320))
    s.person(1340, 560, 40, hair="bun", mouth="grin", hands=((-70, 70), (44, -4)), body_h=120, shirt=SKY)
    for sx in (-1, 1):
        s.circle(1340 + sx * 15, 558, 15, 3.6)
    s.line((1335, 556), (1345, 556), 3.0)
    s.twinkle(1400, 520, 10, ORANGE)
    s.ground(1180, 1520, 762)


def scene3(s):
    s.begin("gear", (40, 100, 420, 360))
    s.gear(190, 260, 82, 10, YEL)
    s.gear(304, 336, 46, 8, TEAL)
    s.magnifier(340, 186, 44, 40)

    s.begin("dominoes", (440, 130, 1140, 300))
    for k in range(10):
        ang = (60, 44, 28, 12)[k] if k < 4 else 0
        domino(s, 480 + k * 95, ang)
    s.line((470, 382), (1420, 382), 3.4)
    for x in (1440, 1474, 1508):
        s.dot(x, 340, 9)

    s.begin("stop", (50, 400, 400, 400))
    with s.scaled(0.72, (220, 470)):
        s.aristotle(220, 470, wave=True)
    s.ground(80, 420, 730)

    s.begin("ladder", (520, 400, 440, 400))
    for x0, x1 in ((640, 760), (720, 800)):
        s.line((x0, 770), (x1, 470), 4.2)
    for k in range(8):
        t = k / 8
        y = 760 - t * 280
        s.line((640 + (760 - 640) * (770 - y) / 300, y), (720 + (800 - 720) * (770 - y) / 300, y), 3.4)
    cl = s.cloud(790, 455, 90, 40, 8)
    s.curve(cl + cl[:2], 4.0)
    s.fill(cl, GRAY)
    for k in range(3):
        s.dot(860 + k * 26, 400 - k * 22, 6)

    s.begin("shrug", (950, 400, 380, 400))
    s.person(1100, 520, 42, hair="short", mouth="flat", hands=((-96, -6), (96, -6)), body_h=130, shirt=GRAY)
    s.curve([(1076, 494), (1086, 488)], 3.0)
    s.curve([(1114, 488), (1124, 494)], 3.0)
    q = [(1180, 430), (1186, 404), (1210, 394), (1232, 404), (1234, 426), (1216, 440), (1210, 456)]
    s.curve(q, 5.0, CORAL)
    s.dot(1210, 476, 7)
    s.ground(980, 1300, 734)

    s.begin("first", (380, 120, 500, 330))
    pts = s.rot_rect(480, 270, 34, 110, 60, (514, 380))
    s.fill(pts, YEL, 9)
    s.star(450, 230, 24, YEL)
    s.arrow((390, 330), (452, 330), CORAL, 4.2, 14)


def scene4(s):
    s.begin("student", (40, 180, 400, 600))
    s.person(210, 400, 44, hair="bun", look=(0, 1), mouth="smile", hands=((-40, 98), (40, 98)), body_h=150, shirt=CORAL)
    s.book(210, 500, 140, 74, CREAM)
    s.ground(60, 380, 640)

    s.begin("ruler", (430, 120, 420, 360))
    tri = [(470, 420), (470, 200), (690, 420)]
    s.poly(tri, 4.2, closed=True)
    s.fill(tri, SKY)
    s.poly([(500, 390), (500, 280), (610, 390)], 3.2, closed=True)
    for k in range(8):
        s.line((470, 410 - k * 26), (486, 410 - k * 26), 2.6)
    s.circle(770, 170, 10, 3.4)
    s.line((766, 178), (724, 410), 4.0)
    s.line((774, 178), (816, 410), 4.0)
    s.arc(770, 170, 240, 240, 72, 108, 2.6, ORANGE)

    s.begin("lyre", (860, 120, 450, 360))
    card = s.rrect(880, 170, 170, 130, 12)
    s.curve(card + card[:1], 4.0)
    s.fill(card, CREAM)
    s.tree(940, 286, 100, GREEN)
    s.sun(1010, 206, 14, ORANGE, 6)
    s.curve([(1140, 420), (1120, 330), (1140, 230), (1160, 210)], 4.2)
    s.curve([(1240, 420), (1260, 330), (1240, 230), (1220, 210)], 4.2)
    s.line((1130, 250), (1250, 250), 4.0)
    base = [(1130, 410), (1250, 410), (1250, 432), (1130, 432)]
    s.poly(base, 3.6, closed=True)
    s.fill(base, YEL, 9)
    for x in (1160, 1180, 1200, 1220):
        s.line((x, 252), (x, 408), 2.4)
    s.note(1290, 230, CORAL)
    s.note(1100, 200, SKY)

    s.begin("fuzzy", (430, 470, 680, 320))
    tri = [(480, 720), (620, 720), (550, 560)]
    s.poly(tri, 4.2, closed=True)
    s.fill(tri, SKY)
    for x in (500, 530, 560, 590):
        s.line((x, 720), (x, 708), 2.4)
    s.line((680, 626), (740, 626), 5.0, CORAL)
    s.line((680, 650), (740, 650), 5.0, CORAL)
    s.line((726, 600), (694, 676), 5.0, CORAL)
    cl = s.cloud(900, 640, 120, 66, 9)
    s.curve(cl + cl[:2], 4.0)
    s.fill(cl, GRAY)
    for k in range(3):
        s.curve([(820 + k * 50, 740), (836 + k * 50, 730), (852 + k * 50, 740)], 3.0, GRAY)

    s.begin("nature", (1120, 440, 460, 350))
    pot = [(1250, 680), (1350, 680), (1336, 760), (1264, 760)]
    s.poly(pot, 4.0, closed=True)
    s.fill(pot, "#e08d5e", 10)
    s.sprout(1300, 680, 120)
    s.magnifier(1440, 600, 44, 130)
    s.sun(1500, 480, 22, YEL, 8)
    for x, y in ((1200, 560), (1380, 520)):
        s.twinkle(x, y, 9, ORANGE)


def build(s):
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
