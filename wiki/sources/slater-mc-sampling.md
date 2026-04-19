---
tags: [source, math, monte-carlo, sampling, prng]
date: 2026-04-19
sources: 1
---

# Monte Carlo Crash Course — Sampling（Max Slater）

[[max-slater]] *Monte Carlo Crash Course* 系列第三章（2025 年 4 月 12 日）。前一章证明了 Monte Carlo 积分的可行性，但假设我们能**在任意分布里采样**——这一章补齐这个关键工程缺口：PRNG、拒绝采样、逆变换采样、坐标变换。

## 摘要

- **PRNG**：物理随机不实际，MC 用伪随机数。作者选 **PCG** 家族——体积小、性能好、统计性质通过 BigCrush 测试。关键性质是 uniformity、independence、aperiodicity。
- **Uniform rejection sampling**：想在任意区域 Ω 里均匀采样——把 Ω 装在一个长方形里，均匀撒点，剔除不在 Ω 内的。简单但效率随 Ω/bbox 比例下降。
- **Non-uniform rejection sampling**：想按 PDF p 采样——在 (x, y) 空间里均匀采，`y < p(x) · M` 则接受。需要 proposal distribution 与 bound M。
- **Inversion sampling**——已知 CDF F 的解析反函数 F⁻¹ 时：u = uniform [0,1]，x = F⁻¹(u) 即服从 p。这是最高效的采样——每次调用都成功。缺点：多数实用分布的 CDF 反函数没闭式。
- **Changes of coordinates**——从球面均匀采样到 disk 采样，要根据 Jacobian 修正 PDF。作者给出球面 cosine-weighted 采样的推导。

## 关键要点

- **PCG** 是小-快-正确的 PRNG 参考——game dev / rendering 里的 de facto 选择。
- **拒绝采样**简单但效率不稳——proposal 和 target 差越大效率越低。
- **逆变换采样**是 MC 里最常见的准确采样方案——前提是 CDF 可闭式求逆（均匀、指数、Gaussian 分量等）。
- **坐标变换必须带上 Jacobian**——这一步错了整个估计有偏。球面 / 立体角 / 方向采样都牵涉这个。

## 链接到的概念

- [[inversion-sampling-prng]]
- [[monte-carlo-integration]]
- [[stratified-sampling]]
- [[low-discrepancy-sequence]]

## 原文

- 链接：https://thenumb.at/Sampling/
- 本地：`raw/articles/thenumb.at/2025-04-12_monte-carlo-crash-course.md`
