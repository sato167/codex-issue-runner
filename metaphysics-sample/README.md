# 白话《形而上学》· 白板动画样板

按 [geeklee/srt-whiteboard-animation](https://github.com/geeklee/srt-whiteboard-animation) 的风格（暖米黄纸底、深灰手绘线、红/橙/蓝少量点缀、分区流式笔迹）制作的样板视频，配音使用 MiniMax 音色 `janey`。

样板内容：第一卷开篇“求知是人的天性”，2 幕 × 3 句，约 45 秒（见 `script.json`）。

## 文件

- `script.json`：白话文案、分幕、音色
- `tools/draw_lineart.py` + `tools/svg2png.mjs`：程序化手绘线稿（无任何文字）
- `tools/clean_hand.py`：去掉参考仓库手部素材笔杆上的原作者标识 → `assets/drawing-hand-clean.png`
- `tools/make_sample.py`：配音 → 按真实音频时长生成 SRT / annotation.json → 流式笔迹渲染 → 合成音轨 + 字幕 → 合并
- `assets/whiteboard/metaphysics/`：线稿 PNG、标注、SRT
- `metaphysics-sample.mp4`：带 janey 配音的样片（约 62 秒）
- `metaphysics-sample-preview-silent.mp4`：早期无声预览（时长按语速估算）

## 生成带配音的正式样片

```bash
git clone https://github.com/geeklee/srt-whiteboard-animation ../srt-whiteboard-animation
python ../srt-whiteboard-animation/scripts/prepare_env.py          # 末行 ENV_PY=...
MINIMAX_API_KEY=sk-api-... python tools/make_sample.py \
  --skill ../srt-whiteboard-animation --env-py <ENV_PY>
# 输出 metaphysics-sample.mp4
```

可选参数：`--voice`（音色名或 voice_id，会先在账号音色列表里匹配 janey）、`--model`（默认 `speech-2.6-hd`）、`MINIMAX_HOST`（默认依次尝试 `api.minimaxi.com`、`api.minimax.io`）。

## v2（自研矢量渲染，推荐）

`v2/` 是在 v1 基础上重新做的一版，画面和节奏都和参考仓库区分开：

- **说的和画的一一对应**：按短句分段配音（`v2/script.json` 每个短句绑定一个画面元素），说到哪画到哪
- **逐笔动画**：笔尖沿真实笔画行进，马克笔来回涂色；手和笔是自己画的
- **镜头**：推近正在画的元素，每幕结束拉远看全貌；幕间翻页转场
- **画面**：方格纸底、更亮的配色、霞鹜文楷手写字幕，荧光笔随语音推进

```bash
MINIMAX_API_KEY=sk-api-... python v2/make.py            # 输出 metaphysics-v2.mp4
python v2/make.py --scenes 4                             # 只重渲染第 4 幕并重新合并
```
