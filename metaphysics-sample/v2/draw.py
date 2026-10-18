#!/usr/bin/env python3
"""v2 矢量手绘：每个元素 = 一组按落笔顺序排列的笔画 + 马克笔涂色。

输出 scenes.json，供 player.html 按配音时间逐笔回放。
每个元素的 id 与 script.json 中短句的 el 一一对应。
用法: python draw.py <输出 scenes.json>
"""
from __future__ import annotations

import json
import math
import random
import sys

W, H = 1600, 900
INK = "#22304a"
YEL, CORAL, TEAL, SKY = "#ffd23f", "#ff6b5b", "#2ec4b6", "#5fa8ff"
PINK, GREEN, BROWN, GRAY = "#ff9fb2", "#7bd389", "#d9a066", "#c9d1de"
ORANGE, CREAM, NAVY = "#ffa94d", "#fff1c9", "#3d5a80"


class Sketch:
    def __init__(self, seed: int):
        self.rnd = random.Random(seed)
        self.elements: dict[str, dict] = {}
        self.cur: dict | None = None

    def begin(self, el: str, focus):
        self.cur = self.elements.setdefault(el, {"id": el, "focus": list(focus), "items": []})

    # ---------- 路径 ----------
    def j(self, a=1.2):
        return self.rnd.uniform(-a, a)

    def _smooth(self, pts, closed=False, jitter=True):
        if closed:
            pts = list(pts) + list(pts[:3])
        p = [(x + self.j(), y + self.j()) if jitter else (x, y) for x, y in pts]
        d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
        for i in range(len(p) - 1):
            p0 = p[i - 1] if i > 0 else p[i]
            p1, p2 = p[i], p[i + 1]
            p3 = p[i + 2] if i + 2 < len(p) else p2
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d

    def curve(self, pts, w=4.2, c=INK, closed=False):
        self.cur["items"].append({"t": "s", "d": self._smooth(list(pts), closed), "w": w, "c": c})

    def line(self, a, b, w=4.2, c=INK):
        m = ((a[0] + b[0]) / 2 + self.j(1.5), (a[1] + b[1]) / 2 + self.j(1.5))
        self.curve([a, m, b], w, c)

    def poly(self, pts, w=4.2, c=INK, closed=False):
        """折线：一笔连续画完，拐角保留。"""
        seq = list(pts) + ([pts[0]] if closed else [])
        d = "M" + " L".join(f"{x + self.j():.1f},{y + self.j():.1f}" for x, y in seq)
        self.cur["items"].append({"t": "s", "d": d, "w": w, "c": c})

    def epts(self, cx, cy, rx, ry, a0=0.0, a1=360.0, n=None, rot=0.0):
        a0, a1 = math.radians(a0), math.radians(a1)
        n = n or max(8, int(abs(a1 - a0) * max(rx, ry) / 12))
        cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        out = []
        for i in range(n + 1):
            t = a0 + (a1 - a0) * i / n
            x, y = rx * math.cos(t), ry * math.sin(t)
            out.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
        return out

    def ell(self, cx, cy, rx, ry, w=4.2, c=INK, rot=0.0):
        a0 = self.rnd.uniform(0, 360)
        self.curve(self.epts(cx, cy, rx, ry, a0, a0 + 370, rot=rot), w, c)

    def circle(self, cx, cy, r, w=4.2, c=INK):
        self.ell(cx, cy, r, r, w, c)

    def arc(self, cx, cy, rx, ry, a0, a1, w=4.2, c=INK):
        self.curve(self.epts(cx, cy, rx, ry, a0, a1), w, c)

    def dot(self, cx, cy, r=5):
        self.ell(cx, cy, r * 0.5, r * 0.5, r * 1.2)

    # ---------- 马克笔涂色 ----------
    def fill(self, pts, color, w=13, angle=-28.0):
        pts = list(pts)
        a = math.radians(angle)
        ca, sa = math.cos(a), math.sin(a)
        rot = [(x * ca + y * sa, -x * sa + y * ca) for x, y in pts]
        vmin, vmax = min(p[1] for p in rot), max(p[1] for p in rot)
        step = w * 0.72
        rows, v, k = [], vmin + step * 0.4, 0
        while v < vmax:
            xs = []
            for (x1, y1), (x2, y2) in zip(rot, rot[1:] + rot[:1]):
                if (y1 <= v < y2) or (y2 <= v < y1):
                    xs.append(x1 + (v - y1) * (x2 - x1) / (y2 - y1))
            if len(xs) >= 2:
                lo, hi = min(xs) - w * 0.4, max(xs) + w * 0.4
                rows.append((hi, lo, v) if k % 2 else (lo, hi, v))
                k += 1
            v += step
        if not rows:
            return
        back = []
        for u0, u1, v in rows:
            back += [(u0 + self.j(2), v), (u1 + self.j(2), v)]
        real = [(u * ca - vv * sa, u * sa + vv * ca) for u, vv in back]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in real)
        clip = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
        self.cur["items"].append({"t": "f", "d": d, "clip": clip, "w": w, "c": color})

    def fill_ell(self, cx, cy, rx, ry, color, rot=0.0):
        self.fill(self.epts(cx, cy, rx, ry, 0, 360, n=28, rot=rot)[:-1], color)

    # ---------- 复合件 ----------
    def heart(self, cx, cy, s, color):
        pts = []
        for i in range(32):
            t = 2 * math.pi * i / 32
            pts.append((cx + s * 16 * math.sin(t) ** 3 / 16,
                        cy - s * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16))
        self.curve(pts, 4.0, closed=True)
        self.fill(pts, color, 10)

    def star(self, cx, cy, r, color=None, w=3.6):
        pts = []
        for i in range(10):
            rr = r if i % 2 == 0 else r * 0.45
            t = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
        self.poly(pts, w, closed=True)
        if color:
            self.fill(pts, color, 9)

    def twinkle(self, cx, cy, r, c=INK):
        self.line((cx - r, cy), (cx + r, cy), 3.2, c)
        self.line((cx, cy - r), (cx, cy + r), 3.2, c)

    def rays(self, cx, cy, r0, r1, n, a0=0, a1=360, c=INK, w=3.6):
        for i in range(n):
            t = math.radians(a0 + (a1 - a0) * (i + 0.5) / n)
            self.line((cx + r0 * math.cos(t), cy + r0 * math.sin(t)),
                      (cx + r1 * math.cos(t), cy + r1 * math.sin(t)), w, c)

    def cloud(self, cx, cy, rx, ry, n=8):
        pts = []
        for i in range(n):
            a0 = i * 360 / n
            c = (cx + rx * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0)))
            r = min(rx, ry) * 0.55
            pts += self.epts(c[0], c[1], r, r * 0.85, a0 - 70, a0 + 70, n=7)[1:-1]
        return pts

    def grass(self, x, y, s=1.0, c=GREEN):
        self.curve([(x, y), (x - 4 * s, y - 14 * s), (x - 10 * s, y - 22 * s)], 3.4, c)
        self.curve([(x + 5, y), (x + 6 * s, y - 18 * s), (x + 4 * s, y - 30 * s)], 3.4, c)
        self.curve([(x + 10, y), (x + 16 * s, y - 12 * s), (x + 24 * s, y - 18 * s)], 3.4, c)

    def ground(self, x0, x1, y):
        self.curve([(x0 + (x1 - x0) * i / 6, y + self.j(3)) for i in range(7)], 3.4)

    def eyes(self, cx, cy, gap, look=(0, 0), big=False):
        for sx in (-1, 1):
            ex = cx + sx * gap
            if big:
                self.circle(ex, cy, 11, 3.4)
                self.dot(ex + look[0] * 5, cy + look[1] * 5, 5.5)
            else:
                self.dot(ex + look[0] * 3, cy + look[1] * 3, 6.5)

    def cheeks(self, cx, cy, gap):
        for sx in (-1, 1):
            self.fill_ell(cx + sx * gap, cy, 11, 7, PINK)

    def aristotle(self, cx, cy, wave=False, ponder=False):
        """大胡子亚里士多德（Q 版）。cy 为头心。"""
        r = 60
        for i in range(10):  # 卷发
            t = math.radians(195 + i * 16.5)
            self.arc(cx + (r + 4) * math.cos(t), cy + (r + 4) * math.sin(t), 20, 18, 110, 400, 3.6)
        self.curve([(cx - r + 2, cy - 12), (cx - r + 2, cy + 18), (cx - r + 12, cy + 30)])
        self.curve([(cx + r - 2, cy - 12), (cx + r - 2, cy + 18), (cx + r - 12, cy + 30)])
        look = (0.3, -0.9) if ponder else (0, 0)
        self.curve([(cx - 34, cy - 22), (cx - 22, cy - 28), (cx - 10, cy - 24)], 3.6)
        self.curve([(cx + 10, cy - 24), (cx + 22, cy - 28), (cx + 34, cy - 22)], 3.6)
        self.eyes(cx, cy - 6, 22, look, big=True)
        self.curve([(cx + 2, cy), (cx - 4, cy + 14), (cx + 6, cy + 16)], 3.4)
        beard = [(cx - r + 6, cy + 18), (cx - r + 4, cy + 60), (cx - 34, cy + 100), (cx, cy + 118),
                 (cx + 34, cy + 100), (cx + r - 4, cy + 60), (cx + r - 6, cy + 18), (cx + 30, cy + 30),
                 (cx, cy + 26), (cx - 30, cy + 30)]
        self.curve(beard, 4.2, closed=True)
        for x0, y0 in ((cx - 26, cy + 58), (cx + 10, cy + 70), (cx - 6, cy + 94), (cx + 34, cy + 52)):
            self.curve([(x0 - 7, y0 - 8), (x0, y0 + 4), (x0 + 7, y0 - 8)], 3.0)
        self.fill(beard, "#e4e8ef")
        self.arc(cx, cy + 36, 12, 8, 20, 160, 3.6)
        # 长袍 + 腰带
        top, bot = cy + 92, cy + 340
        body_l = [(cx - 44, top), (cx - 86, top + 40), (cx - 102, bot - 120), (cx - 112, bot)]
        body_r = [(cx + 44, top), (cx + 86, top + 40), (cx + 102, bot - 120), (cx + 112, bot)]
        self.curve(body_l)
        self.curve(body_r)
        self.line((cx - 112, bot), (cx + 112, bot))
        sash = [(cx - 80, top + 34), (cx - 56, top + 18), (cx + 100, bot - 90), (cx + 104, bot - 50)]
        self.line(sash[0], sash[3], 3.6)
        self.line(sash[1], sash[2], 3.6)
        self.fill(sash, TEAL)
        for x0 in (cx - 60, cx - 20, cx + 30):
            self.curve([(x0, bot - 70), (x0 + 4, bot - 36), (x0 + 1, bot - 6)], 3.0)
        for sx in (-1, 1):
            self.ell(cx + sx * 40, bot + 10, 26, 11, 3.6)
            self.fill_ell(cx + sx * 40, bot + 10, 24, 9, BROWN)
        if wave:
            self.curve([(cx + 84, top + 46), (cx + 128, top - 10), (cx + 140, top - 70)])
            self.curve([(cx + 92, top + 74), (cx + 150, top + 10), (cx + 166, top - 64)])
            self.circle(cx + 154, top - 90, 24)
            self.fill_ell(cx + 154, top - 90, 22, 22, "#ffd9bf")
            for k in (0, 1):
                self.arc(cx + 154, top - 90, 44 + k * 16, 44 + k * 16, -60, -10, 3.2, CORAL)
                self.arc(cx + 154, top - 90, 44 + k * 16, 44 + k * 16, 190, 240, 3.2, CORAL)
        if ponder:
            self.curve([(cx - 86, top + 60), (cx - 100, top + 10), (cx - 70, cy + 70)])
            self.circle(cx - 62, cy + 62, 20)
            self.fill_ell(cx - 62, cy + 62, 18, 18, "#ffd9bf")


# =====================================================================
def scene1(s: Sketch):
    # 神庙
    s.begin("temple", (40, 140, 470, 540))
    s.poly([(80, 300), (270, 196), (460, 300)], closed=True)
    s.fill([(96, 296), (270, 206), (444, 296)], SKY)
    s.poly([(86, 300), (454, 300), (454, 334), (86, 334)], closed=True)
    for x in (120, 195, 270, 345, 420):
        s.line((x - 16, 334), (x - 16, 576))
        s.line((x + 16, 334), (x + 16, 576))
        s.line((x, 350), (x, 560), 2.6)
        s.poly([(x - 22, 334), (x + 22, 334), (x + 22, 346), (x - 22, 346)], 3.2, closed=True)
    s.poly([(78, 576), (462, 576), (462, 600), (78, 600)], closed=True)
    s.poly([(62, 600), (478, 600), (478, 626), (62, 626)], closed=True)
    s.fill([(80, 578), (460, 578), (460, 598), (80, 598)], YEL)
    s.circle(270, 262, 18, 3.4)
    s.circle(500, 190, 26)
    s.fill_ell(500, 190, 24, 24, ORANGE)
    s.rays(500, 190, 36, 54, 8)
    s.ground(40, 500, 640)
    s.grass(70, 642)
    s.grass(450, 642)

    # 亚里士多德挥手
    s.begin("aristotle", (500, 150, 360, 560))
    s.aristotle(650, 290, wave=True)
    s.ground(520, 800, 644)

    # 书桌与卷轴
    s.begin("scroll", (840, 390, 420, 330))
    s.line((860, 610), (1240, 610))
    s.line((860, 630), (1240, 630))
    s.line((890, 630), (884, 730))
    s.line((1210, 630), (1216, 730))
    paper = [(920, 598), (1180, 598), (1166, 500), (934, 500)]
    s.poly(paper, closed=True)
    s.fill(paper, CREAM)
    for x0 in (906, 1180):
        roll = [(x0, 606), (x0 + 22, 606), (x0 + 36, 494), (x0 + 14, 494)]
        s.poly(roll, closed=True)
        s.fill(roll, BROWN)

    # 羽毛笔写字
    s.begin("quill", (900, 250, 380, 420))
    quill = [(1062, 566), (1084, 520), (1130, 420), (1180, 330), (1214, 290), (1206, 340),
             (1170, 420), (1110, 510)]
    s.curve(quill, closed=True)
    s.line((1062, 566), (1200, 306), 3.0)
    for k in range(5):
        t = 0.35 + k * 0.12
        x, y = 1062 + (1200 - 1062) * t, 566 + (306 - 566) * t
        s.line((x, y), (x + 22, y + 6), 2.6)
    s.fill(quill, PINK)
    for k, y0 in enumerate((522, 546, 570)):
        x1 = 1130 if k < 2 else 1060
        xs = [950 + 14 * i for i in range(int((x1 - 950) / 14) + 1)]
        s.curve([(x, y0 + (4 if i % 2 else -4)) for i, x in enumerate(xs)], 3.0, NAVY)
    pot = [(1196, 556), (1240, 556), (1246, 600), (1190, 600)]
    s.poly(pot, closed=True)
    s.ell(1218, 554, 16, 6, 3.2)
    s.fill(pot, NAVY)

    # 三个人亮起灯泡
    s.begin("bulbs", (1250, 180, 340, 520))
    for i, (x, hair) in enumerate(((1310, "bun"), (1420, "spike"), (1530, "tail"))):
        y = 560
        s.circle(x, y, 38)
        if hair == "bun":
            s.circle(x, y - 46, 14, 3.6)
            s.curve([(x - 36, y - 10), (x - 20, y - 34), (x + 20, y - 34), (x + 36, y - 10)], 3.6)
        elif hair == "spike":
            s.poly([(x - 34, y - 16), (x - 24, y - 46), (x - 10, y - 30), (x, y - 52),
                    (x + 12, y - 30), (x + 26, y - 46), (x + 34, y - 16)], 3.6)
        else:
            s.curve([(x - 36, y - 8), (x - 10, y - 40), (x + 30, y - 30), (x + 52, y + 10), (x + 46, y + 40)], 3.6)
        s.eyes(x, y + 2, 13, (0, -1))
        s.arc(x, y + 14, 12, 8, 20, 160, 3.4)
        s.cheeks(x, y + 14, 24)
        s.curve([(x - 52, y + 110), (x - 46, y + 60), (x, y + 44), (x + 46, y + 60), (x + 52, y + 110)])
        by = 380 if i != 1 else 352
        s.circle(x, by, 30)
        s.fill_ell(x, by, 28, 28, YEL)
        s.poly([(x - 14, by + 30), (x + 14, by + 30), (x + 12, by + 50), (x - 12, by + 50)], 3.4, closed=True)
        s.line((x - 12, by + 40), (x + 12, by + 40), 2.6)
        s.curve([(x - 6, by + 26), (x - 4, by + 8)], 2.8)
        s.curve([(x + 6, by + 26), (x + 4, by + 8)], 2.8)
        s.arc(x, by + 4, 9, 7, 0, 330, 2.8)
        s.rays(x, by, 40, 58, 5, 200, 340, ORANGE)
    s.ground(1260, 1580, 670)


def scene2(s: Sketch):
    # 大眼睛
    s.begin("eye", (560, 60, 480, 300))
    s.curve([(630, 210), (720, 120), (880, 120), (970, 210)], 5.0)
    s.curve([(630, 210), (720, 290), (880, 290), (970, 210)], 5.0)
    s.circle(800, 208, 62, 4.6)
    s.fill_ell(800, 208, 60, 60, SKY)
    s.dot(800, 208, 26)
    s.circle(780, 186, 9, 3.0)
    for i in range(7):
        t = math.radians(212 + i * 19)
        bx, by = 800 + 180 * math.cos(t), 222 + 102 * math.sin(t)
        s.line((bx, by), (bx + 24 * math.cos(t), by + 30 * math.sin(t)), 4.0)
    s.twinkle(1000, 130, 12, ORANGE)
    s.twinkle(600, 140, 10, ORANGE)

    # 婴儿看气球
    s.begin("baby", (60, 300, 540, 470))
    bx, by = 250, 560
    s.circle(bx, by, 62)
    s.curve([(bx - 4, by - 62), (bx + 6, by - 82), (bx + 22, by - 76), (bx + 12, by - 66)], 3.6)
    s.eyes(bx - 2, by - 4, 22, (0.7, -0.7), big=True)
    s.ell(bx + 4, by + 28, 9, 11, 3.4)
    s.cheeks(bx, by + 18, 40)
    body = s.epts(bx, by + 118, 62, 54, 0, 360, n=26)[:-1]
    s.curve(body + body[:1])
    s.fill(body, PINK)
    s.curve([(bx + 44, by + 90), (bx + 80, by + 60), (bx + 104, by + 22)])
    s.circle(bx + 110, by + 12, 15)
    s.curve([(bx - 44, by + 92), (bx - 74, by + 110), (bx - 70, by + 140)])
    for sx in (-1, 1):
        s.ell(bx + sx * 36, by + 176, 26, 14)
    for (x, y, r, c) in ((370, 400, 44, CORAL), (468, 362, 40, SKY), (480, 462, 38, YEL)):
        s.ell(x, y, r, r * 1.16)
        s.fill_ell(x, y, r - 2, r * 1.16 - 2, c)
        s.arc(x - r * 0.3, y - r * 0.4, r * 0.5, r * 0.6, 200, 250, 3.0)
        s.poly([(x - 6, y + r * 1.16 + 8), (x, y + r * 1.16), (x + 6, y + r * 1.16 + 8)], 3.2, closed=True)
        s.curve([(x, y + r * 1.16 + 8), (x - 20, y + r * 1.16 + 50), (bx + 112, by - 2)], 2.8)
    s.rays(bx, by, 80, 98, 3, 230, 300, ORANGE)

    # 背包客看日出
    s.begin("sunrise", (980, 300, 600, 480))
    s.line((1000, 620), (1570, 620))
    sun = s.epts(1380, 620, 82, 82, 180, 360, n=20)
    s.curve(sun)
    s.fill(sun, ORANGE)
    s.rays(1380, 620, 98, 130, 7, 190, 350, ORANGE)
    for y0, x0, x1 in ((650, 1180, 1560), (684, 1240, 1540), (718, 1300, 1520)):
        xs = [x0 + 20 * i for i in range(int((x1 - x0) / 20) + 1)]
        s.curve([(x, y0 + (5 if i % 2 else -5)) for i, x in enumerate(xs)], 3.2, SKY)
    for x, y in ((1250, 470), (1300, 440)):
        s.curve([(x - 18, y - 6), (x - 8, y - 12), (x, y)], 3.2)
        s.curve([(x, y), (x + 8, y - 12), (x + 18, y - 6)], 3.2)
    px = 1110
    s.circle(px, 500, 34)
    s.curve([(px - 34, 494), (px - 20, 466), (px + 18, 464), (px + 34, 490)], 3.6)
    pack = [(px - 32, 548), (px + 32, 548), (px + 36, 640), (px - 36, 640)]
    s.curve(pack + pack[:1], 4.2)
    s.fill(pack, CORAL)
    s.line((px - 20, 590), (px + 20, 590), 3.0)
    s.curve([(px - 30, 548), (px - 62, 500), (px - 80, 446)])
    s.circle(px - 84, 432, 14)
    s.curve([(px + 30, 548), (px + 62, 500), (px + 80, 446)])
    s.circle(px + 84, 432, 14)
    s.line((px - 18, 640), (px - 22, 730))
    s.line((px + 18, 640), (px + 22, 730))
    s.curve([(990, 742), (1060, 728), (1170, 730), (1260, 746)])

    # 到处冒爱心
    s.begin("hearts", (0, 0, 1600, 900))
    for (x, y, sz, c) in ((150, 470, 26, CORAL), (350, 476, 20, PINK), (590, 300, 22, PINK),
                           (1030, 160, 24, CORAL), (1010, 500, 22, PINK), (1210, 420, 28, CORAL)):
        s.heart(x, y, sz, c)
    for x, y in ((420, 300), (720, 380), (1180, 360), (900, 330)):
        s.twinkle(x, y, 10, ORANGE)


def scene3(s: Sketch):
    # 放大镜里的眼睛
    s.begin("lens", (40, 170, 480, 500))
    glass = s.epts(250, 380, 132, 132, 0, 360, n=36)[:-1]
    s.fill(glass, "#d7ecff", 16)
    s.curve(glass + glass[:2], 7.0)
    s.arc(250, 380, 110, 110, 200, 250, 3.6)
    handle = [(338, 486), (364, 462), (480, 590), (452, 616)]
    s.poly(handle, closed=True)
    s.fill(handle, BROWN)
    s.curve([(170, 382), (210, 336), (290, 336), (330, 382)], 4.2)
    s.curve([(170, 382), (210, 424), (290, 424), (330, 382)], 4.2)
    s.circle(250, 380, 30)
    s.fill_ell(250, 380, 28, 28, SKY)
    s.dot(250, 380, 13)

    # 两张对比卡片 + 闪电
    s.begin("cards", (540, 90, 1020, 700))
    for x0 in (560, 1060):
        s.curve([(x0 + 20, 110), (x0 + 360, 110), (x0 + 380, 130), (x0 + 380, 740), (x0 + 360, 760),
                 (x0 + 20, 760), (x0, 740), (x0, 130), (x0 + 20, 110)], 4.2)
        for y in (318, 528):
            for k in range(8):
                s.line((x0 + 30 + k * 42, y), (x0 + 52 + k * 42, y), 2.6, GRAY)
    bolt = [(1010, 340), (982, 430), (1004, 430), (988, 510), (1034, 410), (1010, 410), (1030, 340)]
    s.poly(bolt, closed=True)
    s.fill(bolt, YEL, 9)

    # 红苹果 青苹果
    s.begin("apples", (540, 100, 940, 230))
    for x, c in ((750, CORAL), (1250, GREEN)):
        y = 220
        ap = [(x, y - 40), (x - 26, y - 52), (x - 56, y - 36), (x - 64, y + 2), (x - 46, y + 44),
              (x - 20, y + 58), (x, y + 50), (x + 20, y + 58), (x + 46, y + 44), (x + 64, y + 2),
              (x + 56, y - 36), (x + 26, y - 52)]
        s.curve(ap, closed=True)
        s.fill(ap, c)
        s.curve([(x, y - 40), (x + 4, y - 62), (x + 12, y - 74)], 3.6)
        leaf = [(x + 8, y - 60), (x + 30, y - 82), (x + 56, y - 76), (x + 34, y - 56)]
        s.curve(leaf, 3.4, closed=True)
        s.fill(leaf, "#3fae63", 8)
        s.arc(x - 30, y - 6, 18, 22, 190, 250, 3.2)

    # 圆月亮 弯月亮
    s.begin("moons", (540, 310, 940, 220))
    s.circle(750, 422, 64)
    s.fill_ell(750, 422, 62, 62, YEL)
    for (x, y, r) in ((728, 400, 12), (772, 440, 9), (760, 396, 6)):
        s.circle(x, y, r, 3.0)
    outer = s.epts(1250, 422, 64, 64, 60, 300, n=24)
    inner = s.epts(1282, 410, 54, 54, 250, 110, n=20)
    s.curve(outer + inner, 4.2)
    s.fill(outer + inner, YEL)
    s.twinkle(1340, 360, 10, ORANGE)

    # 小花猫 大老虎
    s.begin("cats", (540, 520, 940, 250))
    cx, cy = 750, 650
    s.poly([(cx - 50, cy - 30), (cx - 44, cy - 84), (cx - 12, cy - 52)], closed=True)
    s.poly([(cx + 50, cy - 30), (cx + 44, cy - 84), (cx + 12, cy - 52)], closed=True)
    head = s.epts(cx, cy, 58, 50, 0, 360, n=26)[:-1]
    s.curve(head + head[:1])
    s.fill(head, "#ffe0b8")
    s.eyes(cx, cy - 6, 22, (0, 0))
    s.poly([(cx - 7, cy + 8), (cx + 7, cy + 8), (cx, cy + 16)], 3.4, closed=True)
    s.curve([(cx - 12, cy + 26), (cx, cy + 18), (cx + 12, cy + 26)], 3.2)
    for sx in (-1, 1):
        for dy in (-4, 8):
            s.line((cx + sx * 26, cy + 14 + dy * 0.3), (cx + sx * 74, cy + 8 + dy), 2.8)
    tx, ty = 1250, 645
    for sx in (-1, 1):
        s.ell(tx + sx * 58, ty - 58, 22, 22)
    head = s.epts(tx, ty, 80, 68, 0, 360, n=30)[:-1]
    s.curve(head + head[:1])
    s.fill(head, ORANGE)
    for sx in (-1, 1):
        for k in range(3):
            y0 = ty - 30 + k * 22
            s.curve([(tx + sx * 80, y0), (tx + sx * 60, y0 + 4), (tx + sx * 46, y0 - 4)], 6.0)
    s.curve([(tx - 12, ty - 66), (tx - 6, ty - 46), (tx - 10, ty - 30)], 6.0)
    s.curve([(tx + 12, ty - 66), (tx + 6, ty - 46), (tx + 10, ty - 30)], 6.0)
    s.line((tx - 46, ty - 26), (tx - 18, ty - 16), 4.6)
    s.line((tx + 46, ty - 26), (tx + 18, ty - 16), 4.6)
    s.eyes(tx, ty - 6, 30, (0, 0))
    muzzle = s.epts(tx, ty + 30, 36, 24, 0, 360, n=20)[:-1]
    s.curve(muzzle + muzzle[:1], 3.6)
    s.poly([(tx - 10, ty + 16), (tx + 10, ty + 16), (tx, ty + 28)], 3.4, closed=True)
    s.poly([(tx - 12, ty + 40), (tx - 6, ty + 52), (tx, ty + 40), (tx + 6, ty + 52), (tx + 12, ty + 40)], 3.2)

    # 三个对勾
    s.begin("checks", (1360, 100, 240, 700))
    for y in (220, 422, 650):
        s.poly([(1478, y), (1504, y + 30), (1556, y - 34)], 10.0, "#2fa84f")


def scene4(s: Sketch):
    # 记忆云
    s.begin("memory", (40, 50, 540, 360))
    cl = s.cloud(300, 210, 220, 120, 10)
    s.curve(cl + cl[:2], 4.2)
    s.circle(140, 360, 14, 3.6)
    s.circle(112, 396, 8, 3.4)
    s.curve([(160, 214), (190, 188), (230, 188), (260, 214)], 3.6)
    s.curve([(160, 214), (190, 238), (230, 238), (260, 214)], 3.6)
    s.dot(210, 213, 12)
    s.poly([(280, 214), (318, 214)], 3.2, ORANGE)
    s.poly([(306, 204), (320, 214), (306, 224)], 3.2, ORANGE)
    sw = [(350, 214), (380, 200), (410, 204), (432, 190), (420, 214), (440, 236), (408, 224), (380, 230)]
    s.curve(sw, 3.4, closed=True)
    s.fill(sw, NAVY, 8)
    for x, y in ((400, 268), (430, 282), (370, 284)):
        drop = [(x, y - 12), (x + 7, y + 2), (x, y + 8), (x - 7, y + 2)]
        s.curve(drop, 3.0, closed=True)
        s.fill(drop, SKY, 7)

    # 老农与燕子
    s.begin("farmer", (40, 330, 560, 460))
    fx, fy = 170, 540
    s.circle(fx, fy, 46)
    brim = s.epts(fx, fy - 30, 88, 18, 0, 360, n=26)[:-1]
    s.curve(brim + brim[:1])
    crown = s.epts(fx, fy - 36, 46, 40, 180, 360, n=14)
    s.curve(crown, 4.2)
    s.fill(brim, YEL)
    s.fill(crown + [(fx + 46, fy - 34), (fx - 46, fy - 34)], YEL)
    s.eyes(fx, fy, 16, (1, 0))
    s.arc(fx, fy + 18, 14, 9, 20, 160, 3.4)
    s.curve([(fx - 30, fy - 10), (fx - 22, fy - 14)], 3.0)
    s.cheeks(fx, fy + 14, 30)
    s.curve([(fx - 36, fy + 30), (fx - 60, fy + 80), (fx - 64, fy + 190)])
    s.curve([(fx + 36, fy + 30), (fx + 60, fy + 80), (fx + 64, fy + 190)])
    s.curve([(fx + 44, fy + 64), (fx + 100, fy + 60), (fx + 150, fy + 40)])
    s.circle(fx + 160, fy + 36, 13)
    s.line((fx - 20, fy + 190), (fx - 24, fy + 214))
    s.line((fx + 20, fy + 190), (fx + 24, fy + 214))
    s.ground(50, 590, 760)
    for x in (300, 420, 540):
        s.grass(x, 762)
    for (x, y, k) in ((400, 690, 1.0), (500, 660, 0.8)):
        sw = [(x - 44 * k, y), (x - 10 * k, y - 10 * k), (x + 10 * k, y - 34 * k), (x + 18 * k, y - 8 * k),
              (x + 44 * k, y + 2 * k), (x + 14 * k, y + 6 * k), (x + 30 * k, y + 26 * k), (x - 4 * k, y + 8 * k)]
        s.curve(sw, 3.4, closed=True)
        s.fill(sw, NAVY, 8)
        s.curve([(x + 44 * k + 10, y - 2), (x + 90 * k, y - 4)], 2.6, GRAY)
    rc = s.cloud(470, 430, 90, 44, 8)
    s.curve(rc + rc[:2], 4.2)
    s.fill(rc, GRAY)
    for x in (420, 460, 500, 540):
        s.line((x, 490), (x - 12, 526), 3.4, SKY)

    # 亚里士多德追问
    s.begin("ponder", (590, 120, 400, 640))
    s.aristotle(790, 330, ponder=True)
    q = [(860, 210), (868, 176), (900, 160), (932, 172), (938, 202), (914, 222), (902, 246), (902, 262)]
    s.curve(q, 7.0, CORAL)
    s.dot(902, 290, 9)
    for (x, y, r) in ((846, 262, 6), (830, 282, 4)):
        s.circle(x, y, r, 3.0)

    # 仰望星空的人
    s.begin("stargazer", (980, 70, 610, 720))
    hill = [(990, 790), (1100, 700), (1290, 650), (1480, 700), (1590, 790)]
    s.curve(hill)
    s.fill(hill + [(1590, 795), (990, 795)], "#bfe6c3")
    hx, hy = 1290, 570
    s.circle(hx, hy, 38)
    s.curve([(hx - 38, hy - 4), (hx - 26, hy - 34), (hx + 10, hy - 42), (hx + 36, hy - 20)], 3.6)
    s.eyes(hx, hy - 4, 14, (0.3, -1), big=True)
    s.ell(hx + 2, hy + 18, 6, 8, 3.4)
    s.curve([(hx - 22, hy + 34), (hx - 46, hy + 64), (hx - 52, hy + 92)])
    s.curve([(hx + 22, hy + 34), (hx + 46, hy + 64), (hx + 52, hy + 92)])
    s.curve([(hx - 52, hy + 92), (hx, hy + 100), (hx + 52, hy + 92)])
    s.curve([(hx - 40, hy + 64), (hx - 80, hy + 50), (hx - 92, hy + 86), (hx - 56, hy + 98)], 4.0)
    s.curve([(hx + 40, hy + 64), (hx + 80, hy + 50), (hx + 92, hy + 86), (hx + 56, hy + 98)], 4.0)
    outer = s.epts(1480, 190, 56, 56, 60, 300, n=22)
    inner = s.epts(1508, 178, 46, 46, 250, 110, n=18)
    s.curve(outer + inner)
    s.fill(outer + inner, YEL)
    for (x, y, r, c) in ((1100, 170, 22, SKY), (1220, 260, 18, YEL), (1360, 140, 20, YEL),
                         (1550, 340, 16, SKY), (1070, 360, 14, None)):
        s.star(x, y, r, c)
    for x, y in ((1160, 110), (1300, 210), (1420, 300), (1580, 120)):
        s.twinkle(x, y, 9)

    # 流星 + 惊叹
    s.begin("wow", (980, 70, 610, 720))
    for k in range(3):
        s.line((1170 + k * 6, 222 - k * 14), (1360 + k * 10, 104 - k * 12), 3.4, ORANGE)
    s.star(1156, 236, 26, YEL)
    s.rays(hx, hy, 60, 92, 7, 190, 350, CORAL, 4.6)
    for x in (1206, 1376):
        s.line((x, 470), (x + 4, 510), 7.0, CORAL)
        s.dot(x + 6, 528, 8)


def build() -> dict:
    s = Sketch(2026)
    scene1(s)
    scene2(s)
    scene3(s)
    scene4(s)
    return {"width": W, "height": H, "elements": s.elements}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "scenes.json"
    data = build()
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    n = sum(len(e["items"]) for e in data["elements"].values())
    print(f"{len(data['elements'])} 个元素，{n} 笔 → {out}")
