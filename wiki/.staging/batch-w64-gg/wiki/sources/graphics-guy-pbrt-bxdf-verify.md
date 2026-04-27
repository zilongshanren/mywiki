---
tags: [source, 渲染, brdf, 单元测试, pbrt]
date: 2026-04-19
sources: 1
---

# How does PBRT verify BXDF（A Graphics Guy's Note）

[[graphics-guy-notes]] 2018 年 3 月的文章，讲解 PBRT 自带的 `bsdftest` 程序做什么以及它背后的数学依据。

## 摘要

作者因为 BDPT 和 path tracing 结果分叉，花了很久才锁定是 BXDF 的小 bug——由此总结出「BXDF 在进 integrator 前必须先做单元测试」的教训。文章讲解 PBRT 的 `bsdftest`：把上半球划成 10×10 = 100 个子域（$\phi$ 均匀、$\cos\theta$ 均匀，让每格立体角都是 $2\pi/100$），对每个 BRDF 取 1000 万 importance sampling，用 Monte Carlo 估计 $\int_\Omega d\omega = 2\pi$。每格的估计量乘 100 应近似 $2\pi$，整体平均也应近似 $2\pi$；若不收敛则大概率有 bug。重点能抓出 sample 分布和 pdf 不一致、pdf 函数算错之类的 silent bias。

## 关键要点

- BXDF 接口四要求：evaluate、sample、pdf、pdf 与 evaluate 自洽（避免偏差）。
- bsdftest 核心是「上半球面积 = $2\pi$」的 MC 验证。
- $\theta$ 切分要让 $\cos\theta$ 均匀，每格立体角才相等。
- bad sample（NaN、负 pdf）数量应为 0；outside sample 多只是效率差，不一定 bug。
- 不测 BRDF 物理正确性，也不测 pdf 与 BRDF 形状匹配度——要额外 chi-square test 等。

## 链接到的概念

- [[bxdf-unit-test]]
- [[microfacet-brdf]]
- [[monte-carlo-integration]]
- [[inversion-sampling-prng]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/how_does_pbrt_verify_bxdf/
- 本地：`raw/articles/agraphicsguynotes.com/2018-03-09_how-does-pbrt-verify-bxdf.md`
