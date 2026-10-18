#!/usr/bin/env python3
"""白话《形而上学》样板视频一键管线。

script.json → MiniMax 配音（默认音色 janey）→ 按真实音频时长生成 SRT 与 annotation.json
→ srt-whiteboard-animation 流式笔迹渲染 → 合成音轨 + 烧录字幕 → 多幕合并。

用法:
  MINIMAX_API_KEY=sk-api-... python make_sample.py --skill <srt-whiteboard-animation 目录> --env-py <ENV_PY>
  python make_sample.py --skill ... --env-py ... --offline    # 无网络：按语速估算时长，输出无声预览
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "assets" / "whiteboard" / "metaphysics"
GAP_MS = 350          # 句间停顿
LEAD_MS = 400         # 开场留白
TAIL_MS = 900         # 结尾凝视
OFFLINE_CPS = 4.3     # 离线估算语速（字/秒）

# 每幕三个区域（与 draw_lineart.py 的构图对应），按叙事顺序排列
REGIONS = {
    "scene-01": [
        ("aristotle", "亚里士多德持卷", "人物与论点登场", "character", (70, 170, 490, 690)),
        ("eye", "爱看的眼睛与万物", "给出证据：人天生爱看", "concept", (600, 180, 510, 650)),
        ("shapes", "孩子分辨形状", "解释原因：看能分辨差别", "character", (1150, 170, 480, 640)),
    ],
    "scene-02": [
        ("stairs", "感觉→记忆→经验", "认识的阶梯", "structure", (60, 310, 560, 510)),
        ("why", "放大镜追问原因", "智慧在于追问为什么", "character", (640, 150, 480, 680)),
        ("wonder", "仰望星空的惊奇", "结论：哲学始于惊奇", "character", (1150, 100, 490, 720)),
    ],
}


# ---------------------------------------------------------------- MiniMax
def _post(host: str, path: str, key: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"https://{host}{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def pick_host(key: str, hosts: list[str]) -> tuple[str, dict]:
    last = None
    for h in hosts:
        try:
            data = _post(h, "/v1/get_voice", key, {"voice_type": "all"})
            if data.get("base_resp", {}).get("status_code", 0) == 0:
                return h, data
            last = data.get("base_resp")
        except Exception as e:  # noqa: BLE001
            last = e
    sys.exit(f"[错误] 无法连接 MiniMax（{', '.join(hosts)}）：{last}")


def resolve_voice(voices: dict, name: str) -> str:
    want = name.lower()
    for group in ("voice_cloning", "voice_generation", "system_voice"):
        for v in voices.get(group) or []:
            if want in (v.get("voice_id", "").lower(), (v.get("voice_name") or "").lower()):
                return v["voice_id"]
    fuzzy = [v for group in ("voice_cloning", "voice_generation", "system_voice") for v in voices.get(group) or []
             if want in v.get("voice_id", "").lower() or want in (v.get("voice_name") or "").lower()]
    if fuzzy:  # 多个同名克隆音色时取最新创建的
        return max(fuzzy, key=lambda v: v.get("created_time", ""))["voice_id"]
    print(f"[提示] 音色列表中未找到 “{name}”，直接作为 voice_id 使用", file=sys.stderr)
    return name


def tts(host: str, key: str, voice_id: str, model: str, text: str, out: Path) -> None:
    body = {
        "model": model, "text": text, "stream": False, "output_format": "hex",
        "voice_setting": {"voice_id": voice_id, "speed": 1.0, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }
    data = _post(host, "/v1/t2a_v2", key, body)
    code = data.get("base_resp", {}).get("status_code")
    if code != 0:
        sys.exit(f"[错误] TTS 失败（{model}/{voice_id}）：{data.get('base_resp')}")
    out.write_bytes(bytes.fromhex(data["data"]["audio"]))


# ---------------------------------------------------------------- 工具
def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def duration_ms(path: Path) -> int:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return int(float(out.strip()) * 1000)


def srt_time(ms: int) -> str:
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_scene(scene: dict, line_ms: list[int], out_dir: Path, stem: str) -> dict:
    cues, t = [], LEAD_MS
    for text, d in zip(scene["lines"], line_ms):
        cues.append((t, t + d, text))
        t += d + GAP_MS
    total = cues[-1][1] + TAIL_MS
    (out_dir / f"{stem}.srt").write_text(
        "\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1)),
        encoding="utf-8")
    elements = []
    for seq, ((eid, label, role, typ, (x, y, w, h)), (a, b, txt)) in enumerate(
            zip(REGIONS[scene["sceneId"]], cues), 1):
        elements.append({
            "id": eid, "label": label, "sequence": seq, "narrativeRole": role, "subtitle": txt, "type": typ,
            "region": {"x": x, "y": y, "width": w, "height": h},
            "reveal": {"direction": "top_to_bottom", "startMs": a, "durationMs": max(1200, b - a - 150),
                       "maskPaddingPx": 22, "protectedRegions": []},
            "handPath": {"start": [x + w // 2, y + 10], "end": [x + w // 2, y + h - 10], "easing": "easeInOut"},
        })
    ann = {"sceneId": scene["sceneId"], "canvas": {"width": 1672, "height": 941},
           "storyBasis": scene["core"], "sceneDurationMs": total, "elements": elements}
    (out_dir / f"{stem}.annotation.json").write_text(json.dumps(ann, ensure_ascii=False, indent=2), encoding="utf-8")
    return ann


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="srt-whiteboard-animation 仓库目录")
    ap.add_argument("--env-py", required=True, help="prepare_env.py 输出的 ENV_PY")
    ap.add_argument("--voice", default=None, help="音色名或 voice_id（默认取 script.json 的 voice）")
    ap.add_argument("--model", default="speech-2.6-hd")
    ap.add_argument("--hosts", default=os.environ.get("MINIMAX_HOST", "api.minimaxi.com,api.minimax.io"))
    ap.add_argument("--offline", action="store_true", help="不配音，按语速估算时长，出无声预览")
    a = ap.parse_args()

    script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
    skill = Path(a.skill).resolve()
    audio_dir = PROJECT / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    if not a.offline:
        key = os.environ.get("MINIMAX_API_KEY") or sys.exit("[错误] 请设置 MINIMAX_API_KEY")
        host, voices = pick_host(key, [h.strip() for h in a.hosts.split(",") if h.strip()])
        voice_id = resolve_voice(voices, a.voice or script["voice"])
        print(f"[配音] host={host} voice_id={voice_id} model={a.model}")

    finals = []
    for scene in script["scenes"]:
        stem = f"{scene['sceneId']}-{scene['name']}"
        line_ms, clips = [], []
        for i, text in enumerate(scene["lines"], 1):
            if a.offline:
                line_ms.append(int(len(text) / OFFLINE_CPS * 1000))
                continue
            clip = audio_dir / f"{stem}-{i:02d}.mp3"
            if not clip.exists():
                tts(host, key, voice_id, a.model, text, clip)
            clips.append(clip)
            line_ms.append(duration_ms(clip))
        ann = build_scene(scene, line_ms, PROJECT, stem)

        silent = PROJECT / f"{stem}-whiteboard.mp4"
        subprocess.run([a.env_py, str(skill / "scripts/render_stream_whiteboard.py"),
                        str(PROJECT / f"{stem}.png"), str(PROJECT / f"{stem}.annotation.json"),
                        str(silent), str(ROOT / "assets/drawing-hand-clean.png"),
                        "--ink-path", "grid", "--color-fill", "contour-wipe"], check=True)

        inputs = ["-i", str(silent)]
        if clips:  # 句间插入静音，拼成与字幕对齐的整幕音轨
            filt, labels = [], []
            for k, (clip, cue) in enumerate(zip(clips, ann["elements"])):
                inputs += ["-i", str(clip)]
                filt.append(f"[{k + 1}:a]adelay={cue['reveal']['startMs']}|{cue['reveal']['startMs']}[a{k}]")
                labels.append(f"[a{k}]")
            filt.append(f"{''.join(labels)}amix=inputs={len(clips)}:normalize=0,"
                        f"apad=whole_dur={ann['sceneDurationMs'] / 1000}[aout]")
            audio_args = ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
                          "-c:a", "aac", "-b:a", "160k"]
        else:
            audio_args = ["-map", "0:v"]
        srt = (PROJECT / f"{stem}.srt").as_posix().replace(":", r"\:")
        style = "FontName=WenQuanYi Zen Hei,FontSize=12,PrimaryColour=&H00313B3B,OutlineColour=&H00D7EBF5,Outline=2,Shadow=0,MarginV=7"
        final = PROJECT / f"{stem}-final.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, *audio_args,
                        "-vf", f"subtitles='{srt}':force_style='{style}'",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-shortest", str(final)], check=True)
        finals.append(final)
        print(f"[完成] {final}")

    out = ROOT / ("metaphysics-sample-preview-silent.mp4" if a.offline else "metaphysics-sample.mp4")
    lst = PROJECT / "concat.txt"
    lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in finals))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out)], check=True)
    print(f"OUTPUT={out}")


if __name__ == "__main__":
    main()
