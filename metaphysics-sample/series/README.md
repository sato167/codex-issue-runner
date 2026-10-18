# 白话《形而上学》系列（14 集）

每卷一集，每集约 1–2 分钟。配音默认用 Gemini TTS（`gemini-3.8-flash-tts`，音色 Aoede），按短句分段配音，说到哪画到哪。各集主题见 [outline.md](outline.md)。

## 目录

```text
series/
├── make.py          # 出一集：配音 → 时间轴 → 逐笔回放渲染 → 合成音轨 → 翻页转场合并
├── render_all.sh    # 依次出全部 14 集
├── lib/
│   ├── sketch.py    # 共享画笔库：笔画、马克笔涂色、人物（亚里士多德/柏拉图/苏格拉底/小人）与道具
│   ├── player.html  # 回放器：逐笔动画、手和笔、镜头推拉、荧光笔字幕
│   └── render.mjs   # 用无头 Chromium 逐帧截图并编码
├── epXX/
│   ├── script.json  # 本集文案：每个短句绑定一个画面元素（el）
│   └── draw.py      # 本集画面：build(s) 里按 s.begin(元素id, 镜头框) 逐个元素作画
└── out/epXX.mp4     # 成片
```

## 用法

```bash
# 检查构图（不配音，按语速估算，输出每幕完成图到 series/build/epXX/preview/）
python series/make.py --ep 5 --preview

# 出一集 → series/out/ep05.mp4
GEMINI_API_KEY=... python series/make.py --ep 5

# 出全集（已生成的配音会复用，不会重复调用接口）
GEMINI_API_KEY=... bash series/render_all.sh

# 只重渲染某一幕并重新合并
GEMINI_API_KEY=... python series/make.py --ep 5 --scenes 2

# 改用 MiniMax 配音
MINIMAX_API_KEY=... python series/make.py --ep 1 --tts minimax --voice janey
```

修改文案后，只有文字变了的短句会重新配音。
