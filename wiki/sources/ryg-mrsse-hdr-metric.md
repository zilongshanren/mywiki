---
tags: [source, 渲染, HDR, 纹理压缩, BC6H, 误差度量]
date: 2026-04-19
sources: 1
---

# MRSSE（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2024 年 11 月的短文，揭示 Oodle Texture BC6H encoder 内部所用的 HDR 块错误度量 **MRSSE**（Mean Relative Sum of Squared Errors）——为解决「用半对数空间 SSE 度量 HDR 块会导致过饱和鲜艳光源的色相严重偏移」而设计。

## 摘要

BC6H 把 float16 按 16-bit 整数解读（等价于半对数映射），所以最直观的 encoder 错误度量就是这些整数上的 SSE。这在白光/低饱和场景下没问题，但在颜色极饱和、亮度极大的 emissive 光源上会崩：比如 (2.34, 0.02, 0.01) 这种纯红高光，对数空间里「绿通道差 0.001」和「红通道差 0.1」权重相同，encoder 宁愿整体偏色（调亮度）也要避免几乎无法察觉的 hue shift——视觉上就是错的。MRSSE 把 SSE 的分子保留、分母换成两向量平方长度之和（或 asymmetric 形式下直接用参考向量的平方长度作分母加一个微小 bias），得到一个**相对误差平方和**。Asymmetric 版本尤其适合 encoder 内循环——固定源像素 x，候选 y 每块只计算一次 per-pixel weight，随后的「最小化加权 SSE」就变回一个线性问题，closed-form 可解。RAD 评测了 8~9 种度量（含 ICtCp/PQ 变体、semi-log2），MRSSE 是唯一全部场景都赢下来的，同时计算便宜，最终成为 Oodle Texture 出厂默认。

## 关键要点

- **HDR 错误度量的核心诉求**：能区分相对亮度差（rgb=2 vs 2.1 差很小） vs 绝对亮度差（0.02 vs 0.12 差很大），而半对数空间刚好把这个判断搞反。
- **MRSSE 公式**：$\frac{\|x-y\|^2}{\|x\|^2 + \|y\|^2 + \epsilon}$（symmetric）或 $\frac{\|x-y\|^2}{\|x\|^2 + \epsilon}$（asymmetric）。
- **为什么偏爱「squared error 形式」**：一阶偏导线性，minimize 变线性方程，encoder 内循环能跑得飞起。
- **encoder 设计哲学**：不追物理正确、不追 CIE2000，而追「内循环便宜 + 严峻场景下视觉可接受」。
- **出厂只留这一个**：之前保留过 3 种（PQ ICtCp 变体、semi-log2、MRSSE），后来发现 MRSSE 从未被另外两种在实际图像上明显超越，干脆删掉。
- **Shipping** Oodle Texture 以来 RAD 没见过其它 BC6H encoder 在 quality 上追平 MRSSE 的版本。

## 链接到的概念

- [[mrsse-hdr-error-metric]]
- [[oodle-compression-suite]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/11/14/mrsse/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-11-14_mrsse.md`
