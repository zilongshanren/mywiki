---
tags: [渲染, 蒙特卡洛, 采样, 数值积分]
date: 2026-04-14
sources: 1
---

# 拟蒙特卡洛（Quasi-Monte Carlo, QMC）

**QMC** 指使用**确定性**点列代替伪随机点列来做数值积分。标准的蒙特卡洛估计器期望误差是 $\sigma \propto \tfrac{1}{\sqrt{N}}$，收敛慢；如果我们愿意放弃「无偏」这个性质，可以换来接近线性的 $\tfrac{\log^d N}{N}$ 收敛率——这就是 QMC 的核心交易。

## 核心思想：放弃随机，换来 discrepancy

Monte Carlo 的精度取决于方差；QMC 把方差这个概率概念换成了一个纯几何量——**星差（star-discrepancy）$D^*_N$**。对单位立方体上的点列 $x_i$，$D^*_N$ 是「任取一个原点在左下角的矩形，矩形内样本的比例与矩形体积的最大差」。它直观衡量「这组点覆盖得均不均匀」。

**Koksma–Hlawka 不等式**：只要 $f$ 有有界变差 $V(f)$，估计器误差最多是 $V(f) \cdot D^*_N$。这把误差完全推给点列本身。

## 和 PRNG 的关系

固定种子的 PRNG 产生的也是确定性点列，因此也算 QMC——但它的 $D^*_N$ 只以 $\tfrac{1}{\sqrt{N}}$ 衰减，收敛率和普通 Monte Carlo 没差。**真正让 QMC 值得用的是 [[low-discrepancy-sequence]]**：Halton、Sobol 等专门设计的序列，$D^*_N \propto \tfrac{\log^d N}{N}$，在低维下渐近优于随机。

## 代价和限制

- **有偏**：QMC 估计器对同一种子总是返回同一个值，多次平均不会降误差——只能加样本。
- **高维退化**：$\log^d N$ 里 $d$ 在分子，维度一高，常数就崩了。高维下（例如 path tracing 的 bounce 数）通常要么退化成 MC，要么配合 [[stratified-sampling]] / scrambling 等混合方案。
- **不好并行**：样本必须来自同一个序列，不能把子问题独立分配。

## 在渲染里的用途

[[poisson-disk-sampling]] 是早期图形里负相关采样的代表；现代 path tracer 则几乎全面转向 Sobol + Owen scrambling 这类 QMC 方案——它们既比 PRNG 方差小，又比完整分层更能处理高维 BRDF/光源/时间采样。Halton 序列因为实现简单，也常用于离线预烘焙。

## 相关

- [[stratified-sampling]] — 通过负相关显式降低方差的姊妹技术
- [[low-discrepancy-sequence]] — 让 QMC 真正有优势的点列类
- [[poisson-disk-sampling]] — 渐进性 + 空间均匀的另一条路
- [[max-slater]]
- [[continuous-probability]] — 同系列 Part 1，数学前置
- [[spherical-integration]] — 同系列所需的积分坐标变换

## Sources

- [[sources/slater-qmc-crash-course]]
