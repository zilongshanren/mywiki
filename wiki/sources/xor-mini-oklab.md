---
tags: [source, 渲染, 颜色, 色彩管理, shader]
date: 2026-04-14
sources: 1
---

# Mini: OkLab（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2023 年 12 月的一篇，主题是 **颜色混合的正确方式**——为什么 sRGB / linear RGB 的直接插值不好看，以及 **OKLab** 如何以最小的数学代价得到感知均匀的过渡。

## 摘要

文章先用「黄色和蓝色对半混」这个反例指出 sRGB 的问题：中点变成中灰，色度消失。sRGB 在设计上是为 CRT 电压响应优化的编码，既不是物理光线性空间，也不是人眼感知均匀空间。转到 linear RGB 修正了 gamma 但中点色度问题依旧。真正感知均匀的是 Björn Ottosson 的 **OKLab**：两次 3×3 矩阵乘 + 一次立方根，就能把 linear RGB 映到 L/a/b 三分量（lightness + 绿-洋红 + 蓝-黄）。文末给了 Inigo Quilez 的优化 `oklab_mix`，把两端转换折叠成一次，并加了微小的中点 gain 拉亮。

## 关键要点

- **sRGB 是编码不是感知空间**。CRT 兼容而已，数学运算必须先 `pow(x, 2.2)` 到 linear。
- **linear RGB 仍不均匀**。混合中点无色度，因为 RGB 三通道的感知权重不同。
- **OKLab** = linear RGB → LMS（视锥响应近似） → 立方根 → 感知三轴；两个 3×3 矩阵 + 一次立方根即可。
- 管线必须是 `sRGB → linear → OKLab → mix → linear → sRGB`——忘一步 gamma 就毁了感知性质。
- **iq 的 `oklab_mix`** 把两次转换合一，并在中点加 `1 + 0.2*a*(1-a)` 的 gain——严格说已不是纯 OKLab，但视觉更讨喜。
- 应用：调色盘生成、UI 渐变、颜色量化（挑「感知最不同的 N 色」）、色盲辅助。
- **Ottosson 也给了 OKHSV / OKHSL** 作为 HSV/HSL 的感知替代。

## 链接到的概念

- [[oklab-color-space]]
- [[color-space]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/oklab
- Ottosson 原文：https://bottosson.github.io/posts/oklab/
- 本地：`raw/articles/mini.gmshaders.com/2023-12-02_mini-oklab.md`
