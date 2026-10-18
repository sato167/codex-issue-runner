#!/usr/bin/env bash
# 依次出竖屏 9:16 版（配音复用横屏版的缓存）。用法：TTS=minimax MINIMAX_API_KEY=... bash series/render_vertical.sh [起始集] [结束集]
set -euo pipefail
cd "$(dirname "$0")"
for e in $(seq "${1:-1}" "${2:-14}"); do
  echo "=== 第 $e 集（竖屏）==="
  python3 make.py --ep "$e" --vertical --tts "${TTS:-gemini}" 2>&1 | grep -vE "^  场景"
done
