---
tags: [source, 渲染, alpha, 纹理, 预乘]
date: 2026-04-19
sources: 1
---

# Beware of Transparent Pixels（Adrian Courrèges / 2017）

[[adrian-courreges]] 2017 年 5 月的短文。用 PS3 XMB（home menu）上 *Limbo* logo 在白色背景上 fade-in 时出现的**灰色色斑**作为案例，解释 alpha=0 像素的 RGB 值**在 bilinear filtering / mipmap 生成**时会**泄露**到邻居可见像素上，造成肉眼可见的边缘脏色。

## 摘要

文章先用一个 12×12 红十字 sprite 做实验：把 alpha=0 的区域分别填绿、蓝、红，三张纹理肉眼看起来一模一样，但在半像素偏移的 bilinear filtering 下边缘会分别渗出**棕、紫、正确**——因为 GPU 在采样时不区分 alpha 是否为 0，无脑对 RGBA 四通道一起做双线性平均。这一混合值再被 framebuffer 上的背景 alpha-blend，最终颜色就是 `0.5 × (0.5, 0, 0.5) + 0.5 × white = 不正确的紫灰`。

解法两条：

- **美术侧："让它流血"（edge padding / flood fill）**——导出前把可见像素颜色**主动灌**进邻居 alpha=0 的 RGB，这样运行时反向渗染时至少渗的是"对"的颜色。GTA V 的树叶 sprite atlas 就是典型案例（alpha 通道关掉看 RGB，能看到非透明区周围有一圈颜色 halo）。Photoshop 有 Solidify 插件、Gimp 也有对应插件可做。注意 PNG 导出时很多工具会为了压缩"丢掉"alpha=0 像素的 RGB 数据，Photoshop 需要 SuperPNG 插件才能保留。
- **程序侧：预乘 alpha**——存 `(αR, αG, αB, α)` 而不是 `(R,G,B,α)`。bilinear 插到 `(0.5,0,0,0.5)` 和原始插值数学等价，但 alpha=0 的像素 RGB 天然被置 0，**彻底消除了 RGB 泄露的可能**。blend state 从 `GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA` 改成 `GL_ONE, GL_ONE_MINUS_SRC_ALPHA`。还附带解决 mipmap 链生成、多层透明合成等等场景的同族问题。

Carmack 和 Tom Forsyth 都明确倡导预乘 alpha；Eric Haines 的 *"GPUs prefer premultiplication"* 是进一步的深挖。

## 关键要点

- Alpha=0 像素的 RGB 值**不是"没用"**——bilinear filter 和 mipmap 会按 RGBA 四通道平均，脏 RGB 会渗到可见边缘。
- *Limbo* logo 在白背景 fade-in 出现灰斑，扒开 PNG 看 B/O 字母的空心里填的是错误 RGB（不是白）。
- 美术层兜底：flood-fill / edge-padding / solidify。
- 程序层根治：[[alpha-compositing|预乘 alpha]] + 改 blend state。
- 很多流行工具默认会把 alpha=0 的 RGB 清零"帮你省压缩"——实际是帮倒忙，要显式关掉。

## 链接到的概念

- [[alpha-compositing]]
- [[alpha-blending]]
- [[srgb-premultiplied-alpha-compression]] — 这套"预乘必须在线性域"的更完整版
- [[mipmap-generation-sampling]]
- [[adrian-courreges]]

## 原文

- 链接：<http://www.adriancourreges.com/blog/2017/05/09/beware-of-transparent-pixels/>
- 本地：`raw/articles/adriancourreges.com/2017-05-09_beware-of-transparent-pixels-adrian-courreges.md`
