#!/usr/bin/env python3
"""程序化手绘线稿：暖米黄纸底 + 深灰素描线 + 少量红/橙/蓝点缀，不含任何文字。

用法: python draw_lineart.py <输出目录>
输出 scene-01-desire-to-know.svg / scene-02-wonder.svg（再由 svg2png.mjs 栅格化）。
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

W, H = 1672, 941
PAPER = "#F5EBD7"
INK = "#3b3631"
RED, ORANGE, BLUE = "#d9665b", "#eea250", "#5b8fc7"


class Sketch:
    def __init__(self, seed: int):
        self.rnd = random.Random(seed)
        self.fills: list[str] = []
        self.inks: list[str] = []

    # ---------- 基础 ----------
    def j(self, a: float = 1.6) -> float:
        return self.rnd.uniform(-a, a)

    def _smooth(self, pts, closed=False) -> str:
        if closed:
            pts = pts + pts[:3]
        p = [(x + self.j(), y + self.j()) for x, y in pts]
        d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
        for i in range(len(p) - 1):
            p0 = p[i - 1] if i > 0 else p[i]
            p1, p2 = p[i], p[i + 1]
            p3 = p[i + 2] if i + 2 < len(p) else p2
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d

    def curve(self, pts, w=3.4, color=INK, closed=False):
        self.inks.append(
            f'<path d="{self._smooth(list(pts), closed)}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    def line(self, a, b, w=3.4, color=INK):
        m = ((a[0] + b[0]) / 2 + self.j(2), (a[1] + b[1]) / 2 + self.j(2))
        self.curve([a, m, b], w, color)

    def poly(self, pts, w=3.4, color=INK, closed=False):
        """折线（保留拐角），每段单独轻微抖动。"""
        seq = list(pts) + ([pts[0]] if closed else [])
        for a, b in zip(seq, seq[1:]):
            self.line(a, b, w, color)

    def ellipse_pts(self, cx, cy, rx, ry, a0=0.0, a1=2 * math.pi, n=None, rot=0.0):
        n = n or max(10, int(abs(a1 - a0) * max(rx, ry) / 14))
        out = []
        cr, sr = math.cos(rot), math.sin(rot)
        for i in range(n + 1):
            t = a0 + (a1 - a0) * i / n
            x, y = rx * math.cos(t), ry * math.sin(t)
            out.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
        return out

    def ellipse(self, cx, cy, rx, ry, w=3.4, color=INK, rot=0.0):
        a0 = self.rnd.uniform(0, 2 * math.pi)
        self.curve(self.ellipse_pts(cx, cy, rx, ry, a0, a0 + 2 * math.pi + 0.18, rot=rot), w, color)

    def circle(self, cx, cy, r, w=3.4, color=INK):
        self.ellipse(cx, cy, r, r, w, color)

    def arc(self, cx, cy, rx, ry, a0, a1, w=3.4, color=INK):
        self.curve(self.ellipse_pts(cx, cy, rx, ry, math.radians(a0), math.radians(a1)), w, color)

    def fill(self, pts, color, opacity=0.8):
        d = self._smooth([(x + self.j(3), y + self.j(3)) for x, y in pts], closed=True)
        self.fills.append(f'<path d="{d}" fill="{color}" fill-opacity="{opacity}" stroke="none"/>')

    def fill_ellipse(self, cx, cy, rx, ry, color, opacity=0.8):
        self.fill(self.ellipse_pts(cx + self.j(3), cy + self.j(3), rx, ry, n=24)[:-1], color, opacity)

    def dot(self, cx, cy, r, color=INK):
        self.inks.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/>')

    def svg(self) -> str:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
                + "".join(self.fills) + "".join(self.inks) + "</svg>")

    # ---------- 复合小件 ----------
    def star(self, cx, cy, r, color=None, w=3.0):
        pts = []
        for i in range(10):
            rr = r if i % 2 == 0 else r * 0.45
            t = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
        if color:
            self.fill(pts, color, 0.85)
        self.poly(pts, w, closed=True)

    def twinkle(self, cx, cy, r, w=2.6):
        self.line((cx - r, cy), (cx + r, cy), w)
        self.line((cx, cy - r), (cx, cy + r), w)

    def grass(self, x, y, s=1.0):
        self.curve([(x, y), (x - 4 * s, y - 14 * s), (x - 9 * s, y - 22 * s)], 2.4)
        self.curve([(x + 4, y), (x + 5 * s, y - 18 * s), (x + 3 * s, y - 28 * s)], 2.4)
        self.curve([(x + 8, y), (x + 14 * s, y - 12 * s), (x + 20 * s, y - 18 * s)], 2.4)

    def ground(self, x0, x1, y):
        xs = [x0 + (x1 - x0) * i / 6 for i in range(7)]
        self.curve([(x, y + self.j(4)) for x in xs], 2.6)


# =====================================================================
def scene1() -> Sketch:
    s = Sketch(11)
    # ---------- A 亚里士多德持卷（x 80-560） ----------
    cx, cy = 310, 300
    # 卷发
    for i in range(9):
        t = math.radians(200 + i * 17.5)
        s.arc(cx + 78 * math.cos(t), cy - 6 + 84 * math.sin(t), 22, 20, 120, 400, 3.0)
    # 脸
    s.curve([(242, 290), (244, 335), (262, 368)], 3.4)
    s.curve([(378, 290), (376, 335), (358, 368)], 3.4)
    # 闭目沉思 + 眉毛
    s.arc(285, 300, 15, 8, 20, 160, 3.2)
    s.arc(337, 300, 15, 8, 20, 160, 3.2)
    s.curve([(266, 278), (284, 270), (302, 276)], 3.0)
    s.curve([(318, 276), (336, 270), (354, 278)], 3.0)
    s.curve([(311, 300), (305, 330), (300, 342), (314, 344)], 3.0)
    # 胡须（扇贝轮廓）
    beard = []
    for i in range(8):
        t = math.radians(170 - i * 20)
        beard.append((cx + 70 * math.cos(t), 360 + 105 * math.sin(math.radians(10 + i * 22.5))))
    s.curve([(244, 335)] + [(cx - 66, 380), (cx - 52, 425), (cx - 28, 455), (cx, 468),
                            (cx + 28, 455), (cx + 52, 425), (cx + 66, 380)] + [(376, 335)], 3.4)
    for x0, y0 in [(cx - 40, 395), (cx, 410), (cx + 40, 395), (cx - 20, 440), (cx + 20, 440)]:
        s.curve([(x0 - 8, y0 - 10), (x0, y0 + 4), (x0 + 8, y0 - 10)], 2.4)
    s.curve([(cx - 34, 358), (cx - 14, 350), (cx, 356), (cx + 14, 350), (cx + 34, 358)], 3.0)
    # 长袍
    s.curve([(cx - 50, 452), (cx - 120, 488), (cx - 160, 540), (cx - 175, 660), (cx - 182, 810)], 3.4)
    s.curve([(cx + 50, 452), (cx + 120, 488), (cx + 160, 540), (cx + 175, 660), (cx + 182, 810)], 3.4)
    s.line((cx - 182, 810), (cx + 182, 810), 3.4)
    def band(t):  # 腰带沿左肩→右胯的插值点
        return [(cx - 135 + 300 * k, 500 + 250 * k) for k in t], [(cx - 95 + 260 * k, 482 + 218 * k) for k in t]
    lo, hi = band([i / 8 for i in range(9)])
    s.fill(lo + hi[::-1], BLUE, 0.75)
    for edge in band([0, 0.2, 0.33])+band([0.72, 0.86, 1.0]):
        s.curve(edge, 3.0)
    for x0 in (cx - 120, cx - 60, cx + 60, cx + 120):
        s.curve([(x0, 700), (x0 + 6, 750), (x0 + 2, 800)], 2.4)
    # 展开的卷轴 + 双手
    s.fill([(cx - 105, 572), (cx + 105, 572), (cx + 105, 668), (cx - 105, 668)], "#fbf4e6", 1.0)
    s.line((cx - 105, 572), (cx + 105, 572), 3.2)
    s.line((cx - 105, 668), (cx + 105, 668), 3.2)
    for x0 in (cx - 112, cx + 112):
        s.ellipse(x0, 620, 14, 56, 3.2)
        s.fill_ellipse(x0, 620, 12, 52, ORANGE, 0.7)
    for k, y0 in enumerate((598, 620, 642)):
        xs = [cx - 80 + 16 * i for i in range(11 - k * 2)]
        s.curve([(x, y0 + (3 if i % 2 else -3)) for i, x in enumerate(xs)], 2.2)
    for x0 in (cx - 135, cx + 135):
        s.ellipse(x0, 628, 22, 28, 3.2)
    s.ground(90, 540, 830)
    s.grass(110, 832)
    s.grass(505, 832, 0.9)

    # ---------- B 爱看：大眼睛与万物（x 610-1110） ----------
    ex, ey = 860, 450
    s.curve([(712, ey), (790, 372), (930, 372), (1008, ey)], 3.6)
    s.curve([(712, ey), (790, 520), (930, 520), (1008, ey)], 3.6)
    s.fill_ellipse(ex, ey, 54, 54, BLUE, 0.8)
    s.circle(ex, ey, 56, 3.4)
    s.dot(ex, ey, 22)
    s.inks.append(f'<circle cx="{ex - 18}" cy="{ey - 20}" r="9" fill="{PAPER}"/>')
    for i in range(6):
        t = math.radians(205 + i * 26)
        bx, by = ex + 150 * math.cos(t), ey + 4 + 82 * math.sin(t)
        s.line((bx, by), (bx + 22 * math.cos(t), by + 26 * math.sin(t)), 3.0)
    # 花
    fx, fy = 700, 690
    for i in range(6):
        t = i * math.pi / 3
        s.fill_ellipse(fx + 22 * math.cos(t), fy + 22 * math.sin(t), 14, 14, RED, 0.75)
        s.circle(fx + 22 * math.cos(t), fy + 22 * math.sin(t), 15, 2.8)
    s.circle(fx, fy, 11, 2.8)
    s.curve([(fx, fy + 36), (fx + 6, fy + 80), (fx, fy + 120)], 3.0)
    s.curve([(fx + 3, fy + 85), (fx + 28, fy + 70), (fx + 40, fy + 78), (fx + 4, fy + 95)], 2.6)
    # 星星、飞鸟、太阳
    s.star(1020, 690, 30, ORANGE)
    s.twinkle(1065, 640, 10)
    for bx, by, k in ((740, 240, 1.0), (800, 205, 0.8), (990, 230, 0.9)):
        s.curve([(bx - 26 * k, by - 6 * k), (bx - 12 * k, by - 14 * k), (bx, by)], 3.0)
        s.curve([(bx, by), (bx + 12 * k, by - 14 * k), (bx + 26 * k, by - 6 * k)], 3.0)
    # 视线虚线
    for tx, ty in ((735, 640), (990, 662), (800, 250)):
        n = 5
        for i in range(n):
            a, b = i / n + 0.03, i / n + 0.11
            x0 = ex + (tx - ex) * (0.42 + 0.5 * a); y0 = ey + (ty - ey) * (0.42 + 0.5 * a)
            x1 = ex + (tx - ex) * (0.42 + 0.5 * b); y1 = ey + (ty - ey) * (0.42 + 0.5 * b)
            s.line((x0, y0), (x1, y1), 2.4)

    # ---------- C 分辨差别：孩子与三种形状（x 1160-1620） ----------
    kx = 1390
    s.fill_ellipse(1240, 285, 46, 46, RED, 0.8)
    s.circle(1240, 285, 48, 3.4)
    tri = [(1390, 190), (1442, 290), (1338, 290)]
    s.fill(tri, ORANGE, 0.85)
    s.poly(tri, 3.4, closed=True)
    sq = [(1500, 245), (1585, 245), (1585, 330), (1500, 330)]
    s.fill(sq, BLUE, 0.8)
    s.poly(sq, 3.4, closed=True)
    for x0, y0 in ((1180, 230), (1452, 205), (1600, 225)):
        s.line((x0, y0), (x0 + 10, y0 - 14), 2.4)
        s.line((x0 + 14, y0 + 4), (x0 + 28, y0 - 4), 2.4)
    # 孩子头
    s.circle(kx, 515, 52, 3.4)
    s.curve([(kx - 50, 500), (kx - 30, 462), (kx + 5, 458), (kx + 30, 468), (kx + 52, 500)], 3.0)
    s.curve([(kx - 10, 462), (kx - 2, 448), (kx + 10, 455)], 2.6)
    s.circle(kx - 18, 505, 9, 2.8)
    s.circle(kx + 18, 505, 9, 2.8)
    s.dot(kx - 16, 500, 4.5)
    s.dot(kx + 20, 500, 4.5)
    s.ellipse(kx, 540, 9, 7, 2.8)
    s.fill_ellipse(kx - 34, 528, 8, 5, RED, 0.45)
    s.fill_ellipse(kx + 34, 528, 8, 5, RED, 0.45)
    # 身体（盘腿坐）
    s.curve([(kx - 30, 565), (kx - 55, 610), (kx - 62, 680)], 3.4)
    s.curve([(kx + 30, 565), (kx + 55, 610), (kx + 62, 680)], 3.4)
    s.curve([(kx - 62, 680), (kx - 130, 700), (kx - 120, 740), (kx, 745), (kx + 120, 740),
             (kx + 130, 700), (kx + 62, 680)], 3.4)
    s.curve([(kx - 70, 712), (kx, 722), (kx + 70, 712)], 2.6)
    # 举手指向三角形
    s.curve([(kx + 40, 590), (kx + 70, 560), (kx + 60, 470), (kx + 45, 395)], 3.4)
    s.curve([(kx + 58, 595), (kx + 88, 560), (kx + 80, 470), (kx + 62, 392)], 3.4)
    s.ellipse(kx + 52, 380, 14, 18, 3.0)
    s.line((kx + 46, 365), (kx + 40, 330), 3.0)
    s.curve([(kx - 40, 595), (kx - 30, 640), (kx + 5, 660)], 3.0)
    s.ground(1170, 1620, 770)
    s.grass(1190, 772, 0.9)
    s.grass(1585, 772)
    return s


def scene2() -> Sketch:
    s = Sketch(23)
    # ---------- A 感觉→记忆→经验 台阶（x 70-600） ----------
    stair = [(80, 800), (80, 715), (250, 715), (250, 595), (420, 595), (420, 475), (590, 475), (590, 800)]
    s.poly(stair, 3.4, closed=True)
    for x0, y0, y1 in ((165, 715, 800), (335, 595, 800), (505, 475, 800)):
        s.line((x0 - 70, y0 + 25), (x0 - 40, y0 + 25), 2.2)
    # 感觉：小眼睛 + 耳边声波
    s.curve([(115, 650), (145, 625), (185, 625), (215, 650)], 3.2)
    s.curve([(115, 650), (145, 675), (185, 675), (215, 650)], 3.2)
    s.fill_ellipse(165, 650, 16, 16, BLUE, 0.85)
    s.circle(165, 650, 17, 3.0)
    s.dot(165, 650, 6)
    for r in (40, 56):
        s.arc(165, 650, r + 40, r + 18, -35, 35, 2.4)
    # 记忆：思考云 + 小花
    cxm, cym = 335, 500
    cloud = []
    for i in range(9):  # 扇贝形外轮廓
        a0 = i * 40
        c = (cxm + 52 * math.cos(math.radians(a0 + 20)), cym + 36 * math.sin(math.radians(a0 + 20)))
        cloud += s.ellipse_pts(c[0], c[1], 24, 20, math.radians(a0 - 60), math.radians(a0 + 100), n=6)[1:-1]
    s.fill(cloud, "#fbf4e6", 1.0)
    s.curve(cloud, 3.0, closed=True)
    s.circle(cxm - 25, cym + 80, 9, 2.8)
    s.circle(cxm - 38, cym + 100, 5, 2.6)
    for i in range(5):
        t = i * 2 * math.pi / 5
        s.fill_ellipse(cxm + 14 * math.cos(t), cym + 14 * math.sin(t), 9, 9, RED, 0.75)
        s.circle(cxm + 14 * math.cos(t), cym + 14 * math.sin(t), 10, 2.4)
    s.circle(cxm, cym, 6, 2.4)
    # 经验：锤子
    hx, hy = 505, 400
    s.poly([(hx - 18, hy - 20), (hx + 18, hy - 20), (hx + 18, hy + 52), (hx - 18, hy + 52)], 3.2, closed=True)
    head = [(hx - 55, hy - 62), (hx + 50, hy - 62), (hx + 50, hy - 20), (hx - 55, hy - 20)]
    s.fill(head, ORANGE, 0.85)
    s.poly(head, 3.4, closed=True)
    s.curve([(hx + 50, hy - 62), (hx + 72, hy - 58), (hx + 78, hy - 40)], 3.0)
    for x0, y0 in ((hx - 75, hy - 70), (hx - 82, hy - 40), (hx + 82, hy - 10)):
        s.line((x0, y0), (x0 + (10 if x0 > hx else -12), y0 - 6), 2.4)
    # 上升箭头
    s.curve([(165, 590), (210, 530), (260, 505)], 2.6, ORANGE)
    s.curve([(395, 470), (430, 420), (440, 395)], 2.6, ORANGE)
    s.poly([(246, 494), (262, 505), (247, 518)], 2.6, ORANGE)
    s.poly([(428, 402), (442, 392), (450, 410)], 2.6, ORANGE)

    # ---------- B 追问为什么：放大镜看苹果（x 640-1110） ----------
    px = 790
    s.circle(px, 330, 50, 3.4)
    s.curve([(px - 48, 318), (px - 30, 278), (px + 10, 272), (px + 45, 300), (px + 50, 320)], 3.0)
    s.circle(px - 4, 330, 6, 2.6)
    s.circle(px + 26, 330, 6, 2.6)
    s.dot(px - 1, 328, 3.4)
    s.dot(px + 29, 328, 3.4)
    s.curve([(px - 16, 312), (px - 4, 306), (px + 6, 311)], 2.6)
    s.curve([(px + 18, 309), (px + 28, 302), (px + 40, 310)], 2.6)
    s.curve([(px + 2, 356), (px + 12, 360), (px + 24, 355)], 2.6)
    s.curve([(px - 10, 380), (px - 70, 420), (px - 80, 560), (px - 90, 790)], 3.4)
    s.curve([(px + 10, 380), (px + 70, 420), (px + 80, 560), (px + 90, 790)], 3.4)
    s.line((px - 90, 790), (px + 90, 790), 3.4)
    s.curve([(px - 50, 430), (px - 20, 600), (px - 30, 780)], 2.4)
    # 持镜手臂
    s.curve([(px + 50, 440), (px + 110, 450), (px + 150, 420)], 3.4)
    s.curve([(px + 55, 470), (px + 115, 478), (px + 160, 445)], 3.4)
    s.ellipse(px + 165, 428, 15, 20, 3.0)
    # 放大镜
    lx, ly = 1010, 340
    s.line((px + 170, 418), (lx - 40, ly + 38), 6.0)
    s.fill_ellipse(lx, ly, 52, 52, BLUE, 0.25)
    s.circle(lx, ly, 56, 4.2)
    s.arc(lx, ly, 42, 42, 200, 250, 2.6)
    # 苹果枝 + 苹果（在镜片后）
    s.curve([(1100, 170), (1060, 200), (1010, 215), (960, 212)], 3.4)
    s.curve([(1040, 205), (1055, 180), (1080, 172), (1062, 200)], 2.6)
    s.line((1012, 214), (1015, 300), 2.6)
    ax, ay = 1015, 342
    s.fill([(ax - 30, ay - 25), (ax - 5, ay - 30), (ax, ay - 25), (ax + 5, ay - 30), (ax + 30, ay - 25),
            (ax + 36, ay + 5), (ax + 22, ay + 34), (ax, ay + 30), (ax - 22, ay + 34), (ax - 36, ay + 5)], RED, 0.85)
    s.curve([(ax, ay - 25), (ax - 5, ay - 30), (ax - 30, ay - 25), (ax - 36, ay + 5), (ax - 22, ay + 34),
             (ax, ay + 30), (ax + 22, ay + 34), (ax + 36, ay + 5), (ax + 30, ay - 25), (ax + 5, ay - 30),
             (ax, ay - 25)], 3.0)
    s.curve([(ax, ay - 25), (ax + 2, ay - 38), (ax + 6, ay - 44)], 2.6)
    # 思考火花
    for a in (-120, -90, -60):
        t = math.radians(a)
        s.line((px + 12 + 70 * math.cos(t), 320 + 70 * math.sin(t)),
               (px + 12 + 92 * math.cos(t), 320 + 92 * math.sin(t)), 3.0, ORANGE)
    s.ground(660, 1100, 805)
    s.grass(1060, 807)

    # ---------- C 哲学始于惊奇：山丘望星空（x 1150-1620） ----------
    s.curve([(1160, 800), (1260, 735), (1390, 705), (1520, 735), (1620, 800)], 3.4)
    s.grass(1250, 752, 0.8)
    s.grass(1540, 760, 0.8)
    # 坐着仰望的人
    hx, hy = 1390, 585
    s.circle(hx, hy, 40, 3.4)
    s.curve([(hx - 40, hy - 5), (hx - 32, hy - 32), (hx, hy - 42), (hx + 30, hy - 34), (hx + 40, hy - 10)], 3.0)
    s.circle(hx - 14, hy - 2, 8, 2.6)
    s.circle(hx + 14, hy - 2, 8, 2.6)
    s.dot(hx - 13, hy - 6, 3.6)
    s.dot(hx + 15, hy - 6, 3.6)
    s.ellipse(hx, hy + 20, 6, 8, 2.6)
    s.curve([(hx - 22, hy + 38), (hx - 45, hy + 70), (hx - 52, hy + 110)], 3.4)
    s.curve([(hx + 22, hy + 38), (hx + 45, hy + 70), (hx + 52, hy + 110)], 3.4)
    s.curve([(hx - 52, hy + 110), (hx - 30, hy + 122), (hx + 30, hy + 122), (hx + 52, hy + 110)], 3.4)
    s.curve([(hx - 40, hy + 80), (hx - 75, hy + 60), (hx - 95, hy + 100), (hx - 60, hy + 118)], 3.2)
    s.curve([(hx + 40, hy + 80), (hx + 75, hy + 60), (hx + 95, hy + 100), (hx + 60, hy + 118)], 3.2)
    # 月亮与星星
    mx, my = 1515, 230
    moon = s.ellipse_pts(mx, my, 52, 52, math.radians(60), math.radians(300), n=18)
    inner = s.ellipse_pts(mx + 24, my - 6, 42, 42, math.radians(250), math.radians(110), n=14)
    s.fill(moon + inner, ORANGE, 0.85)
    s.curve(moon, 3.4)
    s.curve(inner, 3.0)
    s.star(1250, 200, 24, BLUE)
    s.star(1370, 300, 18, ORANGE)
    s.star(1590, 400, 16, BLUE)
    s.star(1220, 420, 14)
    for x0, y0 in ((1300, 160), (1440, 190), (1600, 120), (1180, 300), (1480, 380)):
        s.twinkle(x0, y0, 9)
    s.curve([(1430, 140), (1370, 165), (1310, 200)], 2.4)
    s.star(1440, 136, 10, ORANGE, 2.4)
    for a in (-110, -90, -70):
        t = math.radians(a)
        s.line((hx + 62 * math.cos(t), hy + 62 * math.sin(t)),
               (hx + 80 * math.cos(t), hy + 80 * math.sin(t)), 2.6)
    return s


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    out.mkdir(parents=True, exist_ok=True)
    (out / "scene-01-desire-to-know.svg").write_text(scene1().svg(), encoding="utf-8")
    (out / "scene-02-wonder.svg").write_text(scene2().svg(), encoding="utf-8")
    print("ok")
