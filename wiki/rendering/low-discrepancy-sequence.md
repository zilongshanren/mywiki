---
tags: [渲染, 蒙特卡洛, 采样, 数值积分]
date: 2026-04-14
sources: 1
---

# 低差异序列（Low-Discrepancy Sequence）

**低差异序列**是专门构造的确定性点列，其星差 $D^*_N$ 以 $\tfrac{\log^d N}{N}$ 的速度衰减——**渐近优于 $\tfrac{1}{\sqrt{N}}$**。它们是 [[quasi-monte-carlo]] 真正能比普通 Monte Carlo 快的原因。

## Halton 序列

最容易理解的低差异序列。一维 Halton 以某个底 $b$ 的**基数反射（radical inverse）** $\Psi_b(n)$ 定义：把 $n$ 写成 $b$ 进制数字 $d_k d_{k-1} \dots d_1 d_0$，然后翻转到小数部分得 $0.d_0 d_1 \dots d_k$（$b$ 进制）。例如 $b = 10$ 时 $\Psi_{10}(1234) = 0.4321$。

$d$ 维 Halton 就是把 $d$ 个互素的 $b_1, \dots, b_d$ 各做一次一维 Halton 拼成点。$(2, 3)$ 是最常见的二维 Halton，在低维下能得到近似线性的收敛率。

## 高维退化与 scrambling

维度上去以后，高底的 Halton（比如 $b = 29, 31$）在前很多个样本上几乎是一条直线，*星差很高*，需要很多样本才能「起效」。实践中常用的修正叫 **scrambling**：在基数反射前对数字做一个随机置换 $\rho$，让低样本数下的分布也看起来合理：

$$
\Psi_b^\rho(n) = \sum \rho(d_i) \cdot b^{-(i+1)}
$$

scrambling 可以把 bias 打回到 QMC 在低样本数也能用的程度。

## Sobol 序列

比 Halton 更主流的选择。Sobol' 序列用 $(0, s)$-sequence 的构造，能在保证低差异的同时获得极高效的位运算生成——一个 XOR 一个查表就能出下一个样本。配合 Owen scrambling，是现代离线 / 实时 path tracer 的默认采样器。

## 和 stratification 的关系

很多低差异序列（包括 Sobol）都可以视为**分层的一种严格形式**：在每一层的样本数上界内强制分布。它们既有 [[stratified-sampling]] 的负相关优点，又能向高维扩展。

## 实践注意

- **只在低维下优**：常数因子 $\log^d N$ 里 $d$ 在分子，维度一高，优势会被吃光。
- **序列有记忆**：必须保留全序列状态，不能把子问题独立分给多线程。
- **和 PRNG 混用**：在多次独立 rerun（比如 denoising 的多帧积累）里，给每次 run 一个不同的 scramble，可以既去 bias 又保 discrepancy。

## 相关

- [[quasi-monte-carlo]]
- [[stratified-sampling]]
- [[poisson-disk-sampling]]
- [[max-slater]]

## Sources

- [[sources/slater-qmc-crash-course]]
