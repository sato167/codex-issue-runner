#!/usr/bin/env python3
"""白话《形而上学》系列出片。

epXX/script.json（短句 ↔ 画面元素）+ epXX/draw.py（逐笔矢量线稿）
→ 逐短句配音（默认 Gemini TTS，音色 Aoede）→ 时间轴 → 逐笔回放渲染 → 合成音轨 → 翻页转场合并。

用法:
  GEMINI_API_KEY=... python series/make.py --ep 1                # 出第 1 集 → series/out/ep01.mp4
  python series/make.py --ep 2 --preview                          # 不配音：按语速估算，输出每幕完成图检查构图
  python series/make.py --ep 2 --scenes 3                         # 只重渲染第 3 幕并重新合并
  MINIMAX_API_KEY=... python series/make.py --ep 1 --tts minimax --voice janey
依赖: ffmpeg、node + 全局 playwright、npm（首次自动下载 LXGW 文楷字体到 series/.cache）
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / "lib"
CACHE = HERE / ".cache"
LEAD, TAIL, XFADE = 0.6, 1.6, 0.6
SOFT_GAP, HARD_GAP = 0.18, 0.42      # 逗号类停顿 / 句末停顿
PREVIEW_CPS = 4.0                    # 预览模式估算语速（字/秒）
GEMINI_STYLE = "[warm, lively storytelling] "   # 方括号语气标签：Gemini 3.8 TTS 不会念出


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration_s(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def font_css() -> Path:
    css = CACHE / "font" / "package" / "lxgwwenkai-bold.css"
    if not css.exists():
        (CACHE / "font").mkdir(parents=True, exist_ok=True)
        run(["npm", "pack", "lxgw-wenkai-webfont@1.7.0"], cwd=CACHE / "font", capture_output=True)
        with tarfile.open(CACHE / "font" / "lxgw-wenkai-webfont-1.7.0.tgz") as t:
            t.extractall(CACHE / "font", filter="data")
    return css


# ---------------------------------------------------------------- 配音
class GeminiTTS:
    def __init__(self, voice: str, model: str):
        self.key = os.environ.get("GEMINI_API_KEY") or sys.exit("[错误] 请设置 GEMINI_API_KEY")
        self.voice, self.model = voice, model

    def __call__(self, text: str, out: Path) -> None:
        body = {"contents": [{"parts": [{"text": GEMINI_STYLE + text}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": self.voice}}}}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        for attempt in range(6):
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"x-goog-api-key": self.key, "Content-Type": "application/json"})
            try:
                d = json.loads(urllib.request.urlopen(req, timeout=180).read())
                data = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
                break
            except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
                msg = e.read()[:200] if isinstance(e, urllib.error.HTTPError) else e
                if isinstance(e, urllib.error.HTTPError) and 400 <= e.code < 500 and e.code != 429:
                    sys.exit(f"[错误] Gemini TTS 返回 {e.code}（不重试）：{msg}")
                print(f"  [重试 {attempt + 1}] {text[:12]}… {msg}", file=sys.stderr)
                time.sleep(2 ** attempt * 2)
        else:
            sys.exit(f"[错误] Gemini TTS 多次失败：{text}")
        raw = out.with_suffix(".raw")
        raw.write_bytes(data)
        # 返回体可能是带头的 WAV，也可能是裸 PCM（24kHz s16le 单声道）
        src = ["-i", str(raw)] if data[:4] == b"RIFF" else ["-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(raw)]
        run(["ffmpeg", "-y", "-loglevel", "error", *src, "-ar", "44100", str(out)])
        raw.unlink()


class MiniMaxTTS:
    def __init__(self, voice: str, model: str):
        sys.path.insert(0, str(HERE.parent / "tools"))
        from make_sample import pick_host, resolve_voice, tts
        self.key = os.environ.get("MINIMAX_API_KEY") or sys.exit("[错误] 请设置 MINIMAX_API_KEY")
        self.host, voices = pick_host(self.key, ["api.minimax.io", "api.minimaxi.com"])
        self.voice, self.model, self._tts = resolve_voice(voices, voice), model, tts

    def __call__(self, text: str, out: Path) -> None:
        mp3 = out.with_suffix(".mp3")
        self._tts(self.host, self.key, self.voice, self.model, text, mp3)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ar", "44100", str(out)])
        mp3.unlink()


# ---------------------------------------------------------------- 主流程
def load_draw(ep_dir: Path, out_json: Path) -> dict:
    sys.path.insert(0, str(LIB))
    import sketch
    spec = importlib.util.spec_from_file_location(f"draw_{ep_dir.name}", ep_dir / "draw.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    s = sketch.Sketch(2026)
    mod.build(s)
    data = {"width": sketch.W, "height": sketch.H, "elements": s.elements}
    out_json.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--root", default=str(HERE), help="项目目录（含 epXX/），默认本系列；如 ../apology")
    ap.add_argument("--tts", default="gemini", choices=["gemini", "minimax"])
    ap.add_argument("--voice", default=None, help="默认 gemini=Aoede，minimax=janey")
    ap.add_argument("--model", default=None, help="默认 gemini-3.8-flash-tts / speech-2.6-hd")
    ap.add_argument("--scenes", default=None, help="只渲染这些幕，如 1,3")
    ap.add_argument("--preview", action="store_true", help="不配音，输出每幕完成图")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--vertical", action="store_true", help="出 9:16 竖屏版 → out/epXX_竖屏.mp4")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    out_dir = root / "out"
    ep_dir = root / f"ep{a.ep:02d}"
    script = json.loads((ep_dir / "script.json").read_text(encoding="utf-8"))
    build = root / "build" / ep_dir.name
    audio = build / f"audio-{a.tts}"
    audio.mkdir(parents=True, exist_ok=True)
    data = load_draw(ep_dir, build / "scenes.json")
    missing = [p["el"] for sc in script["scenes"] for p in sc["phrases"] if p["el"] not in data["elements"]]
    if missing:
        sys.exit(f"[错误] draw.py 缺少元素：{missing}")

    tts = None
    if not a.preview:
        if a.tts == "gemini":
            tts = GeminiTTS(a.voice or "Aoede", a.model or "gemini-3.8-flash-tts")
        else:
            tts = MiniMaxTTS(a.voice or "janey", a.model or "speech-2.6-hd")

    # 1) 逐短句配音 + 时间轴
    timeline = {"title": script["title"], "subtitle": script["subtitle"], "scenes": [], "footer": script.get("footer"),
                "layout": "vertical" if a.vertical else "landscape"}
    vs = "-v" if a.vertical else ""   # 竖屏版的中间文件后缀
    texts_path = audio / "texts.json"
    cached = json.loads(texts_path.read_text(encoding="utf-8")) if texts_path.exists() else {}
    for sc in script["scenes"]:
        t, phrases = LEAD, []
        for i, ph in enumerate(sc["phrases"], 1):
            clip = audio / f"{sc['id']}-{i:02d}.wav"
            if a.preview:
                d = len(ph["text"]) / PREVIEW_CPS
            else:
                if not clip.exists() or cached.get(clip.name) != ph["text"]:
                    tts(ph["text"], clip)
                d = duration_s(clip)
            phrases.append({**ph, "start": round(t, 3), "end": round(t + d, 3), "clip": str(clip)})
            t += d + (HARD_GAP if ph["text"][-1] in "。？！；" else SOFT_GAP)
        timeline["scenes"].append({"id": sc["id"], "name": sc["name"], "phrases": phrases,
                                   "duration": round(phrases[-1]["end"] + TAIL, 3)})
    if not a.preview:
        texts = {f"{sc['id']}-{i:02d}.wav": p["text"] for sc in script["scenes"] for i, p in enumerate(sc["phrases"], 1)}
        texts_path.write_text(json.dumps(texts, ensure_ascii=False, indent=1), encoding="utf-8")
    tl_path = build / f"timeline{vs}.json"
    tl_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    css = font_css()
    render = ["node", str(LIB / "render.mjs"), str(build / "scenes.json"), str(tl_path)]
    if a.preview:
        run([*render, "stills", str(build / "preview"), str(css)])
        print(f"PREVIEW={build / 'preview'}")
        return

    # 2) 逐幕渲染 + 合成音轨
    pick = [int(x) - 1 for x in a.scenes.split(",")] if a.scenes else range(len(timeline["scenes"]))
    for idx in pick:
        sc = timeline["scenes"][idx]
        silent, final = build / f"{sc['id']}{vs}-silent.mp4", build / f"{sc['id']}{vs}.mp4"
        run([*render, str(idx), str(silent), str(css), str(a.fps)])
        inputs, filt, labels = ["-i", str(silent)], [], []
        for k, ph in enumerate(sc["phrases"]):
            ms = int(ph["start"] * 1000)
            inputs += ["-i", ph["clip"]]
            filt.append(f"[{k + 1}:a]adelay={ms}|{ms}[a{k}]")
            labels.append(f"[a{k}]")
        filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={sc['duration']}[aout]")
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
             "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-ar", "44100", "-t", str(sc["duration"]), str(final)])
        print(f"[完成] {final}")

    # 3) 翻页转场合并（所有已渲染的幕）
    finals = [(build / f"{sc['id']}{vs}.mp4", sc["duration"]) for sc in timeline["scenes"]]
    if not all(f.exists() for f, _ in finals):
        print("[提示] 还有幕未渲染，暂不合并")
        return
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{ep_dir.name}{'_竖屏' if a.vertical else ''}.mp4"
    if len(finals) == 1:
        run(["cp", str(finals[0][0]), str(out)])
        print(f"OUTPUT={out}")
        return
    inputs, vf, af, off = [], [], [], 0.0
    for f, _ in finals:
        inputs += ["-i", str(f)]
    v, au = "[0:v]", "[0:a]"
    for k in range(1, len(finals)):
        off += finals[k - 1][1] - XFADE
        vf.append(f"{v}[{k}:v]xfade=transition=slideleft:duration={XFADE}:offset={off:.3f}[v{k}]")
        af.append(f"{au}[{k}:a]acrossfade=d={XFADE}[a{k}]")
        v, au = f"[v{k}]", f"[a{k}]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(vf + af),
         "-map", v, "-map", au, "-c:v", "libx264", "-crf", "24", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    print(f"OUTPUT={out}")


if __name__ == "__main__":
    main()
