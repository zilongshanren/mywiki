---
tags: [source, 渲染, shader, gamma, srgb, color]
date: 2026-04-19
sources: 1
---

# GM Shaders: Gamma（mini.gmshaders.com / Xor）

[[xor-shader-artist]] 2025 年 1 月 mini 短教程：shader 里正确处理 sRGB ↔ linear 编解码。

## 摘要

屏幕和贴图默认是 sRGB 编码的 gamma 空间，shader 里如果想做线性混合（加法、乘法、插值）必须先解码到 linear。近似做法 `pow(c, 2.2)` / `pow(c, 1/2.2)` 够用；精确做法是 sRGB 的分段函数。GameMaker 里没有自动 linear color space，所以采样后必须手动 decode，输出前 encode。

## 关键要点

- gamma 空间直接混合会让中间色调偏暗
- 近似：`pow(c, 2.2)` decode / `pow(c, 1/2.2)` encode
- 精确：sRGB 分段函数（低亮度走线性、高亮度走 2.4 次方）

## 链接到的概念

- [[gamma-correction-srgb]]
- [[color-space]]

## 原文

- 链接：<https://mini.gmshaders.com/p/gamma>
- 本地：`raw/articles/mini.gmshaders.com/2025-01-24_gm-shaders-gamma.md`
