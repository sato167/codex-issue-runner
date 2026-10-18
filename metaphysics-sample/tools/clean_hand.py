#!/usr/bin/env python3
import cv2, numpy as np, sys
# 去掉参考仓库 drawing-hand.png 笔杆上的原作者标识文字（白色笔杆轮廓内的非白像素 → inpaint）。
# 用法: <ENV_PY> -I clean_hand.py <drawing-hand.png> <输出.png>
img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
bgr, a = img[..., :3].copy(), img[..., 3]
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY); sat = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[..., 1]
white = ((gray > 190) & (sat < 40) & (a > 200)).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(white)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
barrel = (lab == big).astype(np.uint8) * 255
# 填洞：外部轮廓填充 → 文字即“白色笔杆轮廓内的非白色像素”
cnts, _ = cv2.findContours(barrel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
filled = np.zeros_like(barrel); cv2.drawContours(filled, cnts, -1, 255, -1)
filled = cv2.erode(filled, np.ones((7, 7), np.uint8))
text = ((filled > 0) & (barrel == 0)).astype(np.uint8) * 255
text = cv2.dilate(text, np.ones((5, 5), np.uint8)) & filled
out = cv2.inpaint(bgr, text, 9, cv2.INPAINT_TELEA)
cv2.imwrite(sys.argv[2], np.dstack([out, a]))
print('area', st[big, cv2.CC_STAT_AREA], 'text px', int((text > 0).sum()))
