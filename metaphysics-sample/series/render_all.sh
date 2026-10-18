#!/usr/bin/env bash
# 依次出全部 14 集（已配好的音频会复用，不会重复扣费）。
# 用法：GEMINI_API_KEY=... bash series/render_all.sh [起始集] [结束集]
#      TTS=minimax MINIMAX_API_KEY=... bash series/render_all.sh
set -euo pipefail
cd "$(dirname "$0")"
for e in $(seq "${1:-1}" "${2:-14}"); do
  echo "=== 第 $e 集 ==="
  python3 make.py --ep "$e" --tts "${TTS:-gemini}" 2>&1 | grep -vE "^  场景"
done
