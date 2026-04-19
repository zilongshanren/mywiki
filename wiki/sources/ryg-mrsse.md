---
tags: [source, 渲染, bc6h, hdr, 纹理压缩]
date: 2026-04-19
sources: 1
---

# MRSSE（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2024 年 11 月的短文，介绍 Oodle Texture BC6H encoder 所用的 HDR 块错误度量 **MRSSE**（Mean Relative Sum of Squared Errors），并说明为什么半对数空间的 SSD 在饱和色光源上会彻底崩掉。

## 摘要

BC6H 把 float16 当 16-bit 整数处理，直觉上的错误度量是在这个半对数域上做 SSD。问题在于亮度变化和色相变化的权重被对数拉平了——亮红色高光 `(2.34, 0.02, 0.01)` 里绿通道差 0.001 和红通道差 0.1 权重相同，encoder 会为保 hue 而大幅改亮度。MRSSE 以对称形式 $\|x-y\|^2 / (\|x\|^2 + \|y\|^2 + \varepsilon)$ 或非对称形式 $\|x-y\|^2 / (\|x\|^2 + \varepsilon)$ 给出**相对平方误差**，既保留 squared error 的"导数线性、线性系统可解"性质，又按亮度自动缩放容忍度。RAD 评估过 8~9 种 HDR 度量，3 种活到出厂测试，最终只留 MRSSE——它是唯一"没被任何其它度量在真实图像上明显超越"的。asymmetric 版本在 encoder 内循环特别高效：固定源像素 $x$、变化候选 $y$，每 block 预计算一次权重，随后内循环就是带权 SSE。

## 关键要点

- 半对数 RGB 空间 SSE **在饱和色上失效**——hue shift 和 brightness shift 的权重搞反。
- MRSSE 是**相对误差平方和**：分母自动按亮度缩放。
- 保持 **squared 形式**很关键：线性优化系统、内循环数百次 solve 变线性代数。
- **实证选型**：8-9 种度量横评，MRSSE 最便宜 + 视觉最好。

## 链接到的概念

- [[mrsse-hdr-error-metric]]
- [[oodle-compression-suite]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/11/14/mrsse/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-11-14_mrsse.md`
