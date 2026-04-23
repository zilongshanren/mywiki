---
tags: [source, 渲染, gamma, diffuse, shader, 技巧]
date: 2026-04-19
sources: 1
---

# Gamma and diffuse shading（Angelo Pesce / C0DE517E 2011-02-08）

[[angelo-pesce]] 2011 年 2 月的一条极短技术速记——全文只有一个恒等式。

## 摘要

配方本身：**若贴图已做 γ=1/b 的 pre-encode（即贴图存的是 `tex^(1/b)`），shading 乘完再 γ=b encode 的结果**等价于 **原始 linear tex 乘以 `shading^b`**。换言之：

> **`(tex^a · shading)^b ≡ tex · shading^b`**，前提 `a = 1/b`。

**适用场景**：diffuse-only 粒子、植被这类廉价材质——不需要 per-light / per-material 精确 BRDF，只有一个 shading 标量乘贴图。做法是**把 sRGB decode 从 shader 里省掉**：既然贴图是 sRGB、输出也是 sRGB，那两侧 gamma 曲线都保留，只要把 shading 项改成 `shading^(1/γ)` 或用 `pow(shading, 2.2)` 的 cheap 近似，整条管线**视觉上等价 linear 乘法**但省掉了 decode / encode 两次 pow。

**重要限制**：**这只是 software gamma**——fragment shader 里的数学 trick，**不改变 blend 阶段的行为**。也就是说 **alpha blending、additive blending 仍然发生在 sRGB 空间，仍然不是 gamma-correct 混合**。Pesce 在正文明确提醒「this assuming software gamma in the shader, that will give you no gamma-correct blending」——这是该技巧的明确边界。要真正 gamma-correct blending，必须走 [[linear-lighting-pipeline|framebuffer_sRGB 扩展]]或 HDR 浮点 RT 两条路径之一。

## 关键要点

- **恒等式**：`(tex^a · shading)^b = tex · shading^b` 当 `a = 1/b`。
- **工程含义**：diffuse-only 粒子 / 植被可以**把 decode / encode 两次 pow 省掉**，只把 gamma 负担压到 shading 项上。
- **适用前提**：单次 diffuse 乘法，无多光源 additive 累积，无 alpha blending 精度要求。
- **明确边界**：这是 **shader 内 software gamma**，不解决 blend 阶段的 gamma——那属于 [[linear-lighting-pipeline]] 路径二（`GL_ARB_framebuffer_sRGB`）或路径三（HDR RT）的责任范围。
- 短贴士风格——全文一句话，没有扩展论证、无评论。

## 链接到的概念

- [[angelo-pesce]]
- [[gamma-correction-srgb]]
- [[linear-lighting-pipeline]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/02/gamma-and-diffuse-shading.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-02-08_gamma-and-diffuse-shading.md`（`-2.md` 为归档副本）
