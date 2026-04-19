---
tags: [source, rendering, shader, debugging, precision]
date: 2026-04-19
sources: 1
---

# Common Shader Mistakes（Xor / GM Shaders Mini）

[[xor-shader-artist|Xor]] 发表于 2025-04-26 的一份**shader bug 目录**，基于他自己「写了上千小时仍然会栽」的经验。

## 摘要

分五块：**清晰度**——统一变量命名、消灭魔法数字、uniform 名对不上时静默变 0 是黑屏第一元凶。**颜色**——NaN 是传染病，产地是 `sqrt(-x)` / `log(0)` / `pow` / `acos|asin` 越界 / `0/0`；对应 `max`/`abs`/`clamp`/提前检查。衰减函数推荐 inverse square，banding 用 dither 掩盖，gamma 要在 linear 空间做再编回 sRGB。**纹理**——GameMaker 的 texture page 让 UV 不是 `[0,1]`；硬件双线性只有 256 步；mipmap 按 2×2 quad 选 LOD，UV 不连续（比如分支里的 fract）会引发 2×2 色块伪影，解决用 `textureGrad` 手动给导数；非 2 幂设备会暗中 pad。**坐标**——screen/world/texel/model 不同空间要显式转换；分辨率和宽高比鲁棒性是作品出门前的基本功。**精度**——mobile 默认 mediump，color 用 lowp、UV 用 mediump、**位置和程序化噪声必须 highp**；time uniform 累积溢出会让 shader 长跑后崩坏，测试时乘 1000 模拟几小时；常见修法是每 600s 循环一次。最后附 RenderDoc 和 SHADERed 作为调试工具。

## 关键要点

- 把 checklist 当 bug 清单复查，而不是「做完再优化」的待办。
- uniform 拼错不报错 + NaN 不可逆，是两个最高发的黑屏源。
- Mipmap 的 2×2 quad LOD 选取和 `fwidth` / derivative 行为是同一件事的两面。
- Time 精度是长时间 demo 的杀手。

## 链接到的概念

- [[common-shader-pitfalls]]
- [[gamma-correction-srgb]]
- [[mipmap-generation-sampling]]
- [[two-texture-sampling-tricks]]
- [[analytical-antialiasing]]
- [[floyd-steinberg-dithering]]

## 原文

- 链接：https://mini.gmshaders.com/p/mistakes
- 本地：`raw/articles/mini.gmshaders.com/2025-04-26_common-shader-mistakes.md`
