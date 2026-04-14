---
tags: [source, 渲染, 阴影, 矩, 数学]
date: 2026-04-14
sources: 1
---

# Moment Shadow Mapping（Christoph Peters, Reinhard Klein）

[[christoph-peters]] 与 Reinhard Klein 在 2015 年 I3D 发表的论文摘要页，提出 [[moment-shadow-mapping|矩阴影贴图]]——一种可直接用硬件纹理滤波的硬阴影技术。

## 摘要

经典 shadow map 的深度比较不可线性滤波，而 Variance Shadow Maps 通过存一阶 + 二阶矩换来了可过滤的概率下界，代价是 Chebyshev 不等式太松、漏光严重。这篇论文把「存几阶矩」推到**四阶**——每个 texel 存 `(z, z², z³, z⁴)`——然后通过求解一个截断 Hausdorff 矩问题得到对阴影强度**最锐利可能的下界**。阶数「4」不是拍脑袋定的：作者自动枚举数千个候选构造，发现四阶幂矩在 quality / memory / cost 三轴上帕累托最优。配合一个专门设计的线性变换 + 16-bit unorm 量化，整套算法只需要 64 bits/texel 就能在单样本/像素下拿到接近 ground truth 的硬阴影。

## 关键要点

- **四阶幂矩**：是对「在 [0,1] 区间上带界分布用多少阶矩压缩最划算」这个问题的枚举最优解。
- **Hausdorff 矩问题**：经典数学里的「给定前 N 阶矩，CDF 在某点能取到的最大值」问题，论文给出实时闭式解。
- **64 bits/texel**：和 VSM 的存储预算相同，但阴影质量远超 VSM；16-bit 量化有专门的线性变换配合。
- **直接继承硬件滤波**：可以对 moment shadow map 做双线性、mipmap、各向异性、MSAA resolve，无需特殊路径。
- **errata**：作者的 author version 修正了两处印刷错误（算法区间 `I=[0,1]` 应为 `I=ℝ`，以及返回值 `1-w₃` 应为 `1-w₁`）——博客提供修订版。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[shadow-mapping-basics]]
- [[christoph-peters]]
- [[polynomial-root-finding-gpu]]

## 原文

- 链接：<http://momentsingraphics.de/I3D2015.html>
- DOI：<https://doi.org/10.1145/2699276.2699277>
- 本地：`raw/articles/momentsingraphics.de/2015-01-01_moment-shadow-mapping.md`
