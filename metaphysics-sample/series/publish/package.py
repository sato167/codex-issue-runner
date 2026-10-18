#!/usr/bin/env python3
"""生成抖音发布文案，并把视频（横屏 + 竖屏）、封面、文案打成一个文件夹的压缩包。

用法: python series/publish/package.py <输出 zip 路径> [项目目录]
     项目目录默认本系列；其他项目需有 <项目>/publish/meta.json 和 <项目>/publish/covers/
前置: series/out/epXX.mp4、series/out/epXX_竖屏.mp4、series/publish/covers/*.png（node publish/covers.mjs 生成）
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERIES = HERE.parent      # 项目目录，main() 里可被参数改写
PUB = HERE                # 项目的 publish 目录
ROOT = "白话形而上学（14集）"
VOL = ['一 Α', '二 α', '三 Β', '四 Γ', '五 Δ', '六 Ε', '七 Ζ', '八 Η', '九 Θ', '十 Ι', '十一 Κ', '十二 Λ', '十三 Μ', '十四 Ν']
TITLE_MAX, DESC_MAX = 30, 300


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def clock(s: float) -> str:
    return f"{int(s // 60)}:{int(round(s % 60)):02d}"


def label(e: dict) -> str:
    return e.get("label") or f"卷{VOL[e['ep'] - 1]}"


def video_name(e: dict, vertical: bool) -> str:
    plain = e["cover"].replace("“", "").replace("”", "")
    return f"第{e['ep']:02d}集_{label(e).replace(' ', '')}_{plain}{'_竖屏' if vertical else ''}.mp4"


def build_copy(meta: dict) -> str:
    c = meta["collection"]
    total = sum(duration(SERIES / "out" / f"ep{e['ep']:02d}.mp4") for e in meta["episodes"])
    ctags = c.get("tags", ["哲学", "亚里士多德", "形而上学", "手绘动画", "知识科普"])[:5]
    n_ep = len(meta["episodes"])
    cdesc = c["desc"] + f"\n全{n_ep}集，约{max(1, round(total / 60))}分钟，建议按顺序看。\n" + " ".join("#" + t for t in ctags)
    assert len(cdesc) <= DESC_MAX, len(cdesc)
    L = [f"{meta.get('brand', '白话《形而上学》')}抖音发布文案",
         f"（标题≤{TITLE_MAX}字；简介含话题≤{DESC_MAX}字；每条5个话题；",
         " 抖音建议发 9:16 竖屏版；封面：竖3:4=1080×1440，横4:3=1440×1080）",
         "=" * 30, "",
         "【合集】", f"合集名称：{c['title']}（{len(c['title'])}字）", "合集简介：", cdesc, f"（{len(cdesc)}字）",
         "合集封面：封面/合集封面_横屏4比3.png", "", "=" * 30]
    last = meta["episodes"][-1]["ep"]
    for e in meta["episodes"]:
        n, cover = e["ep"], e["cover"]
        title = f"{e['hook']}｜{cover}"
        if len(title) > TITLE_MAX:
            title = e["hook"]
        assert len(title) <= TITLE_MAX, (n, title)
        tags = meta.get("base_tags", ["白话形而上学", "亚里士多德", "哲学"]) + e["tags"][:2]
        if "label" in e:
            outro = "全系列到这里讲完，谢谢你一路跟着笔尖走。" if n == last else "下一集在合集里，接着看。"
        else:
            outro = "十四卷到这里全部讲完，谢谢你一路跟着笔尖走。" if n == last else "一卷一集，跟着笔尖读完亚里士多德，下一集在合集里。"
        desc = f"第{n}集·{label(e)}《{cover}》\n{e['desc']}\n{outro}\n" + " ".join("#" + t for t in tags)
        assert len(desc) <= DESC_MAX, (n, len(desc))
        h = SERIES / "out" / f"ep{n:02d}.mp4"
        L += ["", f"【第{n}集】{label(e)} · {cover}（{clock(duration(h))}）",
              f"标题（{len(title)}字）：{title}", f"简介（{len(desc)}字）：", desc,
              f"竖封面：封面/第{n:02d}集_竖屏3比4.png", f"横封面：封面/第{n:02d}集_横屏4比3.png",
              f"竖屏视频（抖音推荐）：视频/竖屏9比16/{video_name(e, True)}",
              f"横屏视频：视频/横屏16比9/{video_name(e, False)}", "-" * 30]
    return "\n".join(L) + "\n"


def main() -> None:
    global SERIES, PUB, ROOT
    out = sys.argv[1]
    if len(sys.argv) > 2:
        SERIES = Path(sys.argv[2]).resolve()
        PUB = SERIES / "publish"
    meta = json.loads((PUB / "meta.json").read_text(encoding="utf-8"))
    ROOT = meta.get("folder", ROOT)
    copy_path = PUB / "发布文案.txt"
    copy_path.write_text(build_copy(meta), encoding="utf-8-sig", newline="\r\n")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
        for e in meta["episodes"]:
            n = e["ep"]
            z.write(SERIES / "out" / f"ep{n:02d}.mp4", f"{ROOT}/视频/横屏16比9/{video_name(e, False)}")
            v = SERIES / "out" / f"ep{n:02d}_竖屏.mp4"
            if v.exists():
                z.write(v, f"{ROOT}/视频/竖屏9比16/{video_name(e, True)}")
            else:
                print(f"[提示] 缺少第 {n} 集竖屏版", file=sys.stderr)
        for f in sorted(glob.glob(str(PUB / "covers" / "*.png"))):
            z.write(f, f"{ROOT}/封面/{os.path.basename(f)}")
        z.write(copy_path, f"{ROOT}/发布文案.txt")
        n_files = len(z.namelist())
    print(f"{n_files} 个文件，{os.path.getsize(out) / 1e6:.1f} MB → {out}")


if __name__ == "__main__":
    main()
