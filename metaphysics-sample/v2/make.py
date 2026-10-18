#!/usr/bin/env python3
"""v2 一键出片：逐短句 MiniMax 配音 → 时间轴 → 逐笔矢量回放渲染 → 合成音轨 → 翻页转场合并。

用法:
  MINIMAX_API_KEY=sk-api-... python v2/make.py            # 默认音色 janey，国际站 api.minimax.io
  python v2/make.py --scenes 1                             # 只渲染第 1 幕（调试用）
依赖: ffmpeg、node + 全局 playwright、npm（首次自动下载 LXGW 文楷字体到 v2/.cache）
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from make_sample import pick_host, resolve_voice, tts, duration_ms  # noqa: E402

BUILD = HERE / "build"
CACHE = HERE / ".cache"
LEAD, TAIL, XFADE = 0.6, 1.6, 0.6
SOFT_GAP, HARD_GAP = 0.18, 0.42   # 逗号类停顿 / 句末停顿


def font_css() -> Path:
    css = CACHE / "font" / "package" / "lxgwwenkai-bold.css"
    if not css.exists():
        (CACHE / "font").mkdir(parents=True, exist_ok=True)
        subprocess.run(["npm", "pack", "lxgw-wenkai-webfont@1.7.0"], cwd=CACHE / "font", check=True, capture_output=True)
        with tarfile.open(CACHE / "font" / "lxgw-wenkai-webfont-1.7.0.tgz") as t:
            t.extractall(CACHE / "font", filter="data")
    return css


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=None)
    ap.add_argument("--model", default="speech-2.6-hd")
    ap.add_argument("--hosts", default=os.environ.get("MINIMAX_HOST", "api.minimax.io,api.minimaxi.com"))
    ap.add_argument("--scenes", default=None, help="只渲染这些幕，如 1,3")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    script = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
    BUILD.mkdir(exist_ok=True)
    audio = BUILD / "audio"
    audio.mkdir(exist_ok=True)

    key = os.environ.get("MINIMAX_API_KEY") or sys.exit("[错误] 请设置 MINIMAX_API_KEY")
    host, voices = pick_host(key, [h.strip() for h in a.hosts.split(",") if h.strip()])
    voice_id = resolve_voice(voices, a.voice or script["voice"])
    print(f"[配音] host={host} voice_id={voice_id} model={a.model}")

    # 1) 逐短句配音 + 时间轴
    timeline = {"title": script["title"], "subtitle": script["subtitle"], "scenes": []}
    for sc in script["scenes"]:
        t, phrases = LEAD, []
        for i, ph in enumerate(sc["phrases"], 1):
            clip = audio / f"{sc['id']}-{i:02d}.mp3"
            if not clip.exists():
                tts(host, key, voice_id, a.model, ph["text"], clip)
            d = duration_ms(clip) / 1000
            phrases.append({**ph, "start": round(t, 3), "end": round(t + d, 3), "clip": str(clip)})
            t += d + (HARD_GAP if ph["text"][-1] in "。？！；" else SOFT_GAP)
        timeline["scenes"].append({"id": sc["id"], "name": sc["name"], "phrases": phrases,
                                   "duration": round(phrases[-1]["end"] + TAIL, 3)})
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "draw.py"), str(BUILD / "scenes.json")], check=True)

    # 2) 逐幕渲染 + 合成音轨
    pick = [int(x) - 1 for x in a.scenes.split(",")] if a.scenes else range(len(timeline["scenes"]))
    css = font_css()
    finals = []
    for idx in pick:
        sc = timeline["scenes"][idx]
        silent, final = BUILD / f"{sc['id']}-silent.mp4", BUILD / f"{sc['id']}.mp4"
        subprocess.run(["node", str(HERE / "render.mjs"), str(BUILD / "scenes.json"), str(BUILD / "timeline.json"),
                        str(idx), str(silent), str(css), str(a.fps)], check=True)
        inputs, filt, labels = ["-i", str(silent)], [], []
        for k, ph in enumerate(sc["phrases"]):
            ms = int(ph["start"] * 1000)
            inputs += ["-i", ph["clip"]]
            filt.append(f"[{k + 1}:a]adelay={ms}|{ms}[a{k}]")
            labels.append(f"[a{k}]")
        filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={sc['duration']}[aout]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                        "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-ar", "44100", "-t", str(sc["duration"]), str(final)], check=True)
        finals.append((final, sc["duration"]))
        print(f"[完成] {final}")

    # 3) 翻页转场合并
    out = HERE.parent / ("metaphysics-v2.mp4" if not a.scenes else "metaphysics-v2-partial.mp4")
    if len(finals) == 1:
        subprocess.run(["cp", str(finals[0][0]), str(out)], check=True)
    else:
        inputs, vf, af, off = [], [], [], 0.0
        for f, _ in finals:
            inputs += ["-i", str(f)]
        v, au = "[0:v]", "[0:a]"
        for k in range(1, len(finals)):
            off += finals[k - 1][1] - XFADE
            vf.append(f"{v}[{k}:v]xfade=transition=slideleft:duration={XFADE}:offset={off:.3f}[v{k}]")
            af.append(f"{au}[{k}:a]acrossfade=d={XFADE}[a{k}]")
            v, au = f"[v{k}]", f"[a{k}]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(vf + af),
                        "-map", v, "-map", au, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
    print(f"OUTPUT={out}")


if __name__ == "__main__":
    main()
