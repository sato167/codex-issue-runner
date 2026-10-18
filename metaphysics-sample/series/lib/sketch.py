#!/usr/bin/env python3
"""系列共享画笔库：每个元素 = 一组按落笔顺序排列的笔画 + 马克笔涂色。

各集的 epXX/draw.py 定义 build(s: Sketch)，用 s.begin(元素id, 镜头框) 开始一个元素，
元素 id 与该集 script.json 中短句的 el 一一对应；player.html 按配音时间逐笔回放。
"""
from __future__ import annotations

import contextlib
import json
import math
import re
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

    def swallow(self, x, y, k=1.0):
        """俯视的燕子：剪刀尾 + 两片后掠的翅膀，头朝右。"""
        P = lambda pts: [(x + u * k, y + v * k) for u, v in pts]
        body = P([(22, 0), (10, -7), (-14, -5), (-44, -18), (-30, 0), (-44, 18), (-14, 5), (10, 7)])
        up = P([(6, -5), (-8, -30), (-34, -52), (-20, -22), (-6, -5)])
        dn = P([(6, 5), (-8, 30), (-34, 52), (-20, 22), (-6, 5)])
        for sh in (up, dn, body):
            self.curve(sh, 3.2, closed=True)
            self.fill(sh, NAVY, 8)
        self.dot(x + 12 * k, y - 1 * k, 3)

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

    @contextlib.contextmanager
    def scaled(self, k, origin):
        """把块内新画的笔画以 origin 为中心整体缩放 k 倍。"""
        start = len(self.cur["items"])
        yield
        ox, oy = origin
        num = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")
        f = lambda m: f"{ox + (float(m.group(1)) - ox) * k:.1f},{oy + (float(m.group(2)) - oy) * k:.1f}"
        for it in self.cur["items"][start:]:
            it["d"] = num.sub(f, it["d"])
            if "clip" in it:
                it["clip"] = num.sub(f, it["clip"])
            it["w"] = round(it["w"] * max(k, 0.7), 2)

    def rrect(self, x, y, w, h, r=14):
        """圆角矩形顶点（顺时针）。"""
        pts = []
        for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
            pts += self.epts(cx, cy, r, r, a0, a0 + 90, n=4)
        return pts

    def rot_rect(self, x, y, w, h, ang, pivot):
        """矩形绕 pivot 旋转 ang 度后的四个顶点。"""
        a = math.radians(ang)
        px, py = pivot
        out = []
        for u, v in ((x, y), (x + w, y), (x + w, y + h), (x, y + h)):
            dx, dy = u - px, v - py
            out.append((px + dx * math.cos(a) - dy * math.sin(a), py + dx * math.sin(a) + dy * math.cos(a)))
        return out

    def note(self, x, y, color=None):
        self.ell(x, y, 10, 7, 3.0, rot=-20)
        self.fill_ell(x, y, 9, 6, color or INK, rot=-20)
        self.line((x + 9, y - 2), (x + 9, y - 40), 3.0)
        self.curve([(x + 9, y - 40), (x + 22, y - 30), (x + 20, y - 18)], 3.0)

    # ---------- 通用人物与道具（各集复用） ----------
    def person(self, cx, hy, r=40, hair="short", look=(0, 0), mouth="smile", hands=((-60, 90), (60, 90)),
               body_h=150, shirt=None, legs=True, big_eyes=False, cheeks=True, eye_style="dot"):
        """Q 版小人。hy 为头心；hands 为左右手相对头心的位置。"""
        self.circle(cx, hy, r)
        if hair == "short":
            self.curve([(cx - r, hy - 4), (cx - r * 0.6, hy - r * 0.9), (cx + r * 0.3, hy - r * 1.02), (cx + r, hy - 8)], 3.6)
        elif hair == "bun":
            self.circle(cx, hy - r - 12, r * 0.35, 3.6)
            self.curve([(cx - r, hy - 6), (cx - r * 0.5, hy - r * 0.9), (cx + r * 0.5, hy - r * 0.9), (cx + r, hy - 6)], 3.6)
        elif hair == "spike":
            pts = []
            for i in range(9):
                a = math.radians(205 + i * 16.25)
                rr = r * (1.0 if i % 2 == 0 else 1.28)
                pts.append((cx + rr * math.cos(a), hy + rr * math.sin(a)))
            self.poly(pts, 3.6)
        elif hair == "curly":
            for i in range(7):
                t = math.radians(200 + i * 23)
                self.arc(cx + r * math.cos(t), hy + r * math.sin(t), r * 0.32, r * 0.3, 110, 400, 3.2)
        if eye_style == "spiral":
            for sx in (-1, 1):
                self.spiral(cx + sx * r * 0.36, hy - r * 0.05, r * 0.2, 2.0, 2.6)
        elif eye_style == "closed":
            for sx in (-1, 1):
                self.arc(cx + sx * r * 0.36, hy - r * 0.08, r * 0.16, r * 0.1, 20, 160, 3.2)
        else:
            self.eyes(cx, hy - r * 0.05, r * 0.36, look, big=big_eyes)
        my = hy + r * 0.42
        if mouth == "smile":
            self.arc(cx, my - 4, r * 0.3, r * 0.2, 20, 160, 3.4)
        elif mouth == "grin":
            pts = self.epts(cx, my - 6, r * 0.32, r * 0.26, 0, 180, n=10)
            self.curve(pts + [pts[0]], 3.4)
        elif mouth == "o":
            self.ell(cx, my, r * 0.12, r * 0.16, 3.2)
        elif mouth == "flat":
            self.line((cx - r * 0.2, my), (cx + r * 0.2, my), 3.2)
        elif mouth == "frown":
            self.arc(cx, my + 6, r * 0.24, r * 0.16, 200, 340, 3.4)
        if cheeks:
            self.cheeks(cx, hy + r * 0.3, r * 0.62)
        top = hy + r
        sh = r * 0.9
        body = [(cx - sh * 0.55, top), (cx - sh, top + body_h * 0.35), (cx - sh * 1.05, top + body_h),
                (cx + sh * 1.05, top + body_h), (cx + sh, top + body_h * 0.35), (cx + sh * 0.55, top)]
        self.curve(body, 4.2)
        if shirt:
            self.fill(body, shirt)
        for sx, (dx, dy) in zip((-1, 1), hands):
            s0 = (cx + sx * sh * 0.75, top + body_h * 0.22)
            hx_, hy_ = cx + dx, hy + dy
            mid = ((s0[0] + hx_) / 2 + sx * 10, (s0[1] + hy_) / 2 + 8)
            self.curve([s0, mid, (hx_, hy_)], 4.0)
            self.circle(hx_, hy_, r * 0.26, 3.6)
        if legs:
            for sx in (-1, 1):
                self.line((cx + sx * sh * 0.45, top + body_h), (cx + sx * sh * 0.5, top + body_h + 40))
                self.ell(cx + sx * sh * 0.62, top + body_h + 44, 16, 7, 3.4)

    def sun(self, cx, cy, r, color=None, nrays=10):
        self.circle(cx, cy, r)
        self.fill_ell(cx, cy, r - 2, r - 2, color or ORANGE)
        self.rays(cx, cy, r + 14, r + 36, nrays)

    def bulb(self, cx, cy, r=30, lit=True):
        self.circle(cx, cy, r)
        if lit:
            self.fill_ell(cx, cy, r - 2, r - 2, YEL)
        self.poly([(cx - r * 0.45, cy + r), (cx + r * 0.45, cy + r), (cx + r * 0.4, cy + r * 1.6), (cx - r * 0.4, cy + r * 1.6)], 3.4, closed=True)
        self.line((cx - r * 0.4, cy + r * 1.3), (cx + r * 0.4, cy + r * 1.3), 2.6)
        self.curve([(cx - r * 0.2, cy + r * 0.9), (cx - r * 0.15, cy + r * 0.25)], 2.8)
        self.curve([(cx + r * 0.2, cy + r * 0.9), (cx + r * 0.15, cy + r * 0.25)], 2.8)
        self.arc(cx, cy + r * 0.13, r * 0.3, r * 0.22, 0, 330, 2.8)
        if lit:
            self.rays(cx, cy, r + 10, r + 28, 5, 200, 340, ORANGE)

    def book(self, cx, cy, w=120, h=80, color=None, open_=True):
        if open_:
            L = [(cx, cy - h / 2 + 8), (cx - w / 2, cy - h / 2), (cx - w / 2, cy + h / 2), (cx, cy + h / 2 + 8)]
            R = [(cx, cy - h / 2 + 8), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx, cy + h / 2 + 8)]
            self.poly(L, 3.6)
            self.poly(R, 3.6)
            self.line((cx, cy - h / 2 + 8), (cx, cy + h / 2 + 8), 3.2)
            for k in range(3):
                y = cy - h / 4 + k * h / 5
                self.line((cx - w * 0.4, y), (cx - w * 0.1, y + 3), 2.4, GRAY)
                self.line((cx + w * 0.1, y + 3), (cx + w * 0.4, y), 2.4, GRAY)
            if color:
                self.fill(L, color)
                self.fill(R, color)
        else:
            pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
            self.poly(pts, 4.0, closed=True)
            self.line((cx - w / 2 + 12, cy - h / 2), (cx - w / 2 + 12, cy + h / 2), 3.0)
            if color:
                self.fill(pts, color)

    def gear(self, cx, cy, r, teeth=10, color=None):
        pts = []
        for i in range(teeth * 4):
            t = 2 * math.pi * i / (teeth * 4)
            rr = r if (i // 2) % 2 == 0 else r * 0.8
            pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
        self.poly(pts, 3.8, closed=True)
        if color:
            self.fill(pts, color)
        self.circle(cx, cy, r * 0.28, 3.4)

    def magnifier(self, cx, cy, r, ang=45, glass=True):
        if glass:
            self.fill_ell(cx, cy, r - 3, r - 3, "#d7ecff")
        self.circle(cx, cy, r, 5.6)
        a = math.radians(ang)
        p0 = (cx + r * math.cos(a), cy + r * math.sin(a))
        p1 = (cx + r * 2.0 * math.cos(a), cy + r * 2.0 * math.sin(a))
        n = (-math.sin(a) * 9, math.cos(a) * 9)
        h = [(p0[0] + n[0], p0[1] + n[1]), (p1[0] + n[0], p1[1] + n[1]), (p1[0] - n[0], p1[1] - n[1]), (p0[0] - n[0], p0[1] - n[1])]
        self.poly(h, 3.6, closed=True)
        self.fill(h, BROWN, 9)

    def tree(self, cx, gy, h=200, color=None):
        self.curve([(cx - 12, gy), (cx - 8, gy - h * 0.45), (cx - 10, gy - h * 0.55)])
        self.curve([(cx + 12, gy), (cx + 8, gy - h * 0.45), (cx + 10, gy - h * 0.55)])
        crown = self.cloud(cx, gy - h * 0.72, h * 0.34, h * 0.28, 9)
        self.curve(crown + crown[:2], 4.2)
        self.fill(crown, color or GREEN)

    def sprout(self, cx, gy, h=80):
        self.curve([(cx, gy), (cx + 3, gy - h * 0.5), (cx, gy - h)], 3.8)
        for sx in (-1, 1):
            leaf = [(cx, gy - h * 0.7), (cx + sx * h * 0.3, gy - h * 0.95), (cx + sx * h * 0.55, gy - h * 0.85), (cx + sx * h * 0.25, gy - h * 0.62)]
            self.curve(leaf, 3.4, closed=True)
            self.fill(leaf, GREEN, 9)

    def arrow(self, a, b, c=INK, w=4.0, head=16):
        self.line(a, b, w, c)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for da in (2.6, -2.6):
            self.line(b, (b[0] + head * math.cos(ang + da), b[1] + head * math.sin(ang + da)), w, c)

    def sweat(self, x, y, s=1.0):
        d = [(x, y - 14 * s), (x + 8 * s, y + 2 * s), (x, y + 9 * s), (x - 8 * s, y + 2 * s)]
        self.curve(d, 3.0, closed=True)
        self.fill(d, SKY, 7)

    def spiral(self, cx, cy, r, turns=2.2, w=3.0, c=INK):
        pts = []
        n = int(turns * 24)
        for i in range(n + 1):
            t = i / n
            a = t * turns * 2 * math.pi
            pts.append((cx + r * t * math.cos(a), cy + r * t * math.sin(a)))
        self.curve(pts, w, c)

    def plato(self, cx, cy, point_up=True):
        """柏拉图（Q 版）：秃顶、两鬓头发、长直胡子、橙色披带，手指向天。cy 为头心。"""
        r = 58
        self.arc(cx, cy, r, r, 190, 350, 4.2)
        for sx in (-1, 1):
            self.curve([(cx + sx * r, cy - 6), (cx + sx * (r + 12), cy + 10), (cx + sx * (r + 4), cy + 30)], 3.6)
            self.curve([(cx + sx * (r - 2), cy - 20), (cx + sx * (r + 14), cy - 8)], 3.2)
        self.curve([(cx - 34, cy - 18), (cx - 20, cy - 24), (cx - 8, cy - 20)], 3.6)
        self.curve([(cx + 8, cy - 20), (cx + 20, cy - 24), (cx + 34, cy - 18)], 3.6)
        self.eyes(cx, cy - 4, 22, (0.4, -0.8), big=True)
        self.curve([(cx, cy), (cx - 5, cy + 14), (cx + 6, cy + 16)], 3.4)
        beard = [(cx - r + 6, cy + 18), (cx - 44, cy + 90), (cx - 30, cy + 150), (cx, cy + 162), (cx + 30, cy + 150),
                 (cx + 44, cy + 90), (cx + r - 6, cy + 18), (cx + 28, cy + 30), (cx, cy + 26), (cx - 28, cy + 30)]
        self.curve(beard, 4.2, closed=True)
        for x0 in (cx - 18, cx, cx + 18):
            self.curve([(x0, cy + 60), (x0 + 3, cy + 100), (x0, cy + 140)], 2.6)
        self.fill(beard, "#e4e8ef")
        self.arc(cx, cy + 36, 12, 8, 20, 160, 3.6)
        top, bot = cy + 100, cy + 350
        self.curve([(cx - 46, top), (cx - 90, top + 40), (cx - 104, bot - 120), (cx - 114, bot)])
        self.curve([(cx + 46, top), (cx + 90, top + 40), (cx + 104, bot - 120), (cx + 114, bot)])
        self.line((cx - 114, bot), (cx + 114, bot))
        sash = [(cx + 84, top + 34), (cx + 60, top + 18), (cx - 100, bot - 90), (cx - 104, bot - 50)]
        self.line(sash[0], sash[3], 3.6)
        self.line(sash[1], sash[2], 3.6)
        self.fill(sash, ORANGE)
        for sx in (-1, 1):
            self.ell(cx + sx * 40, bot + 10, 26, 11, 3.6)
            self.fill_ell(cx + sx * 40, bot + 10, 24, 9, BROWN)
        if point_up:
            self.curve([(cx + 86, top + 46), (cx + 120, top - 20), (cx + 128, top - 90)])
            self.curve([(cx + 94, top + 74), (cx + 146, top), (cx + 154, top - 86)])
            self.circle(cx + 141, top - 104, 20)
            self.fill_ell(cx + 141, top - 104, 18, 18, "#ffd9bf")
            self.line((cx + 138, top - 122), (cx + 136, top - 160), 4.6)

    def qmark(self, x, y, s=1.0, c=CORAL, w=5.0):
        """问号，(x, y) 为顶部弯钩的中心。"""
        P = [(x - 22 * s, y + 6 * s), (x - 16 * s, y - 18 * s), (x + 6 * s, y - 28 * s), (x + 26 * s, y - 16 * s),
             (x + 26 * s, y + 8 * s), (x + 6 * s, y + 24 * s), (x, y + 44 * s), (x, y + 56 * s)]
        self.curve(P, w, c)
        self.dot(x, y + 76 * s, 7 * max(s, 0.6))

    def card(self, x, y, w=70, h=96, color=CREAM, q=True, rot=0.0):
        pts = self.rot_rect(x - w / 2, y - h / 2, w, h, rot, (x, y))
        self.poly(pts, 3.8, closed=True)
        self.fill(pts, color, 10)
        if q:
            self.qmark(x, y - 22, 0.6, CORAL, 4.0)

    def candle(self, cx, gy, h=140, lit=True):
        body = [(cx - 26, gy), (cx - 26, gy - h), (cx + 26, gy - h), (cx + 26, gy)]
        self.poly(body, 4.0)
        self.line((cx - 30, gy), (cx + 30, gy), 4.0)
        self.curve([(cx - 26, gy - h + 4), (cx - 14, gy - h + 18), (cx - 12, gy - h + 40), (cx - 6, gy - h + 16), (cx + 26, gy - h + 6)], 3.2)
        self.fill(body, "#fff1c9", 10)
        self.line((cx, gy - h), (cx, gy - h - 14), 3.0)
        if lit:
            fl = [(cx, gy - h - 62), (cx + 16, gy - h - 30), (cx, gy - h - 14), (cx - 16, gy - h - 30)]
            self.curve(fl, 3.4, closed=True)
            self.fill(fl, ORANGE, 8)

    def check(self, x, y, s=1.0, c="#2fa84f", w=8.0):
        self.poly([(x - 26 * s, y), (x - 6 * s, y + 24 * s), (x + 30 * s, y - 28 * s)], w, c)

    def cross(self, x, y, s=1.0, c=CORAL, w=8.0):
        self.line((x - 24 * s, y - 24 * s), (x + 24 * s, y + 24 * s), w, c)
        self.line((x + 24 * s, y - 24 * s), (x - 24 * s, y + 24 * s), w, c)

    def tablet(self, cx, cy, w=220, h=150, color="#dfe3ea"):
        pts = [(cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2 + 40)] + \
            self.epts(cx, cy - h / 2 + 40, w / 2, 40, 180, 360, n=14)[1:-1] + [(cx + w / 2, cy - h / 2 + 40), (cx + w / 2, cy + h / 2)]
        self.curve(pts + [pts[0]], 4.2)
        self.fill(pts, color)
        self.line((cx, cy - h / 2 + 10), (cx, cy + h / 2 - 14), 3.4)
        self.check(cx - w / 4, cy + 8, 0.9)
        self.cross(cx + w / 4, cy + 8, 0.8)

    def bubble(self, cx, cy, rx, ry, tail):
        """对话气泡，tail 为尾巴尖端坐标。"""
        a = math.degrees(math.atan2(tail[1] - cy, tail[0] - cx))
        pts = self.epts(cx, cy, rx, ry, a + 12, a + 348, n=30)
        self.curve(pts + [tail, pts[0]], 4.0)
        return pts

    def clock(self, cx, cy, r, color=None):
        self.circle(cx, cy, r)
        if color:
            self.fill_ell(cx, cy, r - 2, r - 2, color)
        for k in range(12):
            t = math.radians(k * 30)
            self.line((cx + r * 0.8 * math.cos(t), cy + r * 0.8 * math.sin(t)), (cx + r * 0.9 * math.cos(t), cy + r * 0.9 * math.sin(t)), 2.4)
        self.line((cx, cy), (cx, cy - r * 0.6), 3.6)
        self.line((cx, cy), (cx + r * 0.45, cy + r * 0.1), 3.6)

    def house(self, cx, gy, w=200, h=140, roof=CORAL, wall=CREAM):
        wall_pts = [(cx - w / 2, gy), (cx - w / 2, gy - h), (cx + w / 2, gy - h), (cx + w / 2, gy)]
        self.poly(wall_pts, 4.0, closed=True)
        self.fill(wall_pts, wall)
        rf = [(cx - w / 2 - 20, gy - h), (cx, gy - h - w * 0.45), (cx + w / 2 + 20, gy - h)]
        self.poly(rf, 4.2, closed=True)
        self.fill(rf, roof)
        door = [(cx - w * 0.12, gy), (cx - w * 0.12, gy - h * 0.55), (cx + w * 0.12, gy - h * 0.55), (cx + w * 0.12, gy)]
        self.poly(door, 3.6)
        self.fill(door, BROWN, 9)
        win = [(cx + w * 0.22, gy - h * 0.75), (cx + w * 0.4, gy - h * 0.75), (cx + w * 0.4, gy - h * 0.5), (cx + w * 0.22, gy - h * 0.5)]
        self.poly(win, 3.2, closed=True)
        self.fill(win, SKY, 8)

    def fish(self, x, y, k=1.0, color=SKY):
        body = self.epts(x, y, 34 * k, 18 * k, 0, 360, n=18)[:-1]
        self.curve(body + body[:1], 3.6)
        self.fill(body, color, 9)
        tail = [(x - 32 * k, y), (x - 56 * k, y - 16 * k), (x - 52 * k, y + 16 * k)]
        self.poly(tail, 3.4, closed=True)
        self.fill(tail, color, 8)
        self.dot(x + 18 * k, y - 4 * k, 4)

    def chicken(self, x, y, k=1.0, face=1):
        """站立的小鸡，face=1 朝右。(x, y) 为身体中心。"""
        P = lambda u, v: (x + face * u * k, y + v * k)
        body = [P(-60, 0), P(-40, -40), P(10, -44), P(40, -20), P(50, 20), P(10, 50), P(-40, 44)]
        self.curve(body, 4.0, closed=True)
        self.fill(body, "#ffffff")
        self.circle(*P(40, -60), 28 * k, 4.0)
        for u in (24, 40, 56):
            self.arc(*P(u, -92), 9 * k, 10 * k, 180, 360, 3.4, CORAL)
        self.fill([P(18, -88), P(62, -88), P(58, -100), P(22, -100)], CORAL, 8)
        bk = [P(66, -64), P(86, -56), P(66, -50)]
        self.poly(bk, 3.4, closed=True)
        self.fill(bk, ORANGE, 7)
        self.dot(*P(48, -66), 5)
        self.curve([P(-20, -6), P(0, 14), P(-30, 20)], 3.2)
        for u in (-10, 20):
            self.line(P(u, 50), P(u, 84), 3.6, ORANGE)
            self.line(P(u, 84), P(u + 14, 88), 3.4, ORANGE)

    def duck(self, x, y, k=1.0, face=1):
        P = lambda u, v: (x + face * u * k, y + v * k)
        body = [P(-64, -10), P(-30, -30), P(20, -30), P(54, 0), P(30, 40), P(-30, 44), P(-60, 20)]
        self.curve(body, 4.0, closed=True)
        self.fill(body, YEL)
        self.circle(*P(36, -62), 28 * k, 4.0)
        self.fill_ell(*P(36, -62), 26 * k, 26 * k, YEL)
        bill = [P(58, -62), P(92, -60), P(92, -48), P(58, -48)]
        self.curve(bill, 3.4, closed=True)
        self.fill(bill, ORANGE, 7)
        self.dot(*P(42, -70), 5)
        self.curve([P(-30, 0), P(0, 18), P(-24, 22)], 3.2)
        for u in (-10, 20):
            self.line(P(u, 42), P(u, 76), 3.6, ORANGE)
            self.poly([P(u - 8, 80), P(u, 76), P(u + 16, 82)], 3.4, ORANGE)
