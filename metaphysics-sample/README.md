# 白话《形而上学》· 白板动画样板

按 [geeklee/srt-whiteboard-animation](https://github.com/geeklee/srt-whiteboard-animation) 的风格（暖米黄纸底、深灰手绘线、红/橙/蓝少量点缀、分区流式笔迹）制作的样板视频，配音使用 MiniMax 音色 `janey`。

样板内容：第一卷开篇“求知是人的天性”，2 幕 × 3 句，约 45 秒（见 `script.json`）。

## 文件

- `script.json`：白话文案、分幕、音色
- `tools/draw_lineart.py` + `tools/svg2png.mjs`：程序化手绘线稿（无任何文字）
- `tools/clean_hand.py`：去掉参考仓库手部素材笔杆上的原作者标识 → `assets/drawing-hand-clean.png`
- `tools/make_sample.py`：配音 → 按真实音频时长生成 SRT / annotation.json → 流式笔迹渲染 → 合成音轨 + 字幕 → 合并
- `assets/whiteboard/metaphysics/`：线稿 PNG、标注、SRT
- `metaphysics-sample-preview-silent.mp4`：无声预览（时长按语速估算）

## 生成带配音的正式样片

```bash
git clone https://github.com/geeklee/srt-whiteboard-animation ../srt-whiteboard-animation
python ../srt-whiteboard-animation/scripts/prepare_env.py          # 末行 ENV_PY=...
MINIMAX_API_KEY=sk-api-... python tools/make_sample.py \
  --skill ../srt-whiteboard-animation --env-py <ENV_PY>
# 输出 metaphysics-sample.mp4
```

可选参数：`--voice`（音色名或 voice_id，会先在账号音色列表里匹配 janey）、`--model`（默认 `speech-2.6-hd`）、`MINIMAX_HOST`（默认依次尝试 `api.minimaxi.com`、`api.minimax.io`）。
