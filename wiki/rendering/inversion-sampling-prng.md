---
tags: [math, monte-carlo, sampling, prng]
date: 2026-04-19
sources: 1
---

# 采样方法：PRNG、拒绝、逆变换

[[max-slater]] *Monte Carlo Crash Course — Sampling* 给出 Monte Carlo 工程里采样的工具箱。渲染器的每一个 `sample_hemisphere()`、`sample_light()`、`sample_bsdf()` 都是本页三类方法之一的具体实现。

## PRNG：伪随机数生成器

现代渲染几乎都用 **PCG** 家族：体积小、速度快、通过 BigCrush 统计测试。它提供近似均匀的 [0,1] 浮点数序列，是所有下游采样的输入。

关键性质：
- **均匀**——长序列内分布均衡；
- **独立**——过去值不能预测未来值；
- **非周期**——周期远超实际样本需求（PCG32 的周期是 2⁶⁴）。

工程上要避免：
- **同 seed + 同计数器** 产生相同序列——多线程渲染每像素给独立 seed；
- **低熵 seed**——PCG 接受 64-bit seed，乱 hash 一下就够；
- **相关流**——两个邻近像素的序列应当不相关，要做 **stream splitting** 或 hash 像素坐标。

## Uniform Rejection Sampling

目标：在非矩形区域 Ω 均匀采样。做法：装进一个 bounding box，均匀撒点，不在 Ω 内就丢掉。

效率 = |Ω| / |bbox|。一个半径为 1 的圆嵌进 [-1,1]²，命中率 π/4 ≈ 78%——可以接受。但一个瘦长三角形嵌进它的 bbox，命中率可能只有 10%——就不值得。

## Non-uniform Rejection Sampling

目标：按 PDF p(x) 采样。引入易采样的 proposal q(x) 与上界 M 使得 p(x) ≤ M·q(x)。流程：

```
while true:
    x ~ q(x)
    u ~ Uniform(0, 1)
    if u < p(x) / (M * q(x)):
        return x
```

期望尝试次数 = M（越接近 1 越好）。适合 p 复杂但 q 好采样的情形。

## Inversion Sampling（逆变换采样）

若目标分布的 CDF F(x) 可闭式求逆：

```
u ~ Uniform(0, 1)
x = F⁻¹(u)   →  x ~ p
```

**每次调用 100% 成功**，是最高效的采样方式。标准实例：

- **指数分布**：p(x) = λe^(-λx)，F⁻¹(u) = -log(1-u)/λ；
- **Cosine-weighted hemisphere**：z = √u₁, φ = 2π·u₂，对 Lambert diffuse 是 importance sampling 的 sweet spot。

限制：多数实用分布 CDF 反函数没闭式。混合正态、GGX BRDF 等要用近似反函数或 LUT。

## 坐标变换与 Jacobian

从一个分布换到另一个（例如 disk 采样→球面采样）必须带上 **Jacobian**：

```
p_y(y) = p_x(x) · |det(dx/dy)|
```

忘带 Jacobian 是渲染器里最常见的「暗 bug」——结果看起来合理但能量不守恒，长时间曝光会偏亮或偏暗。Slater 专门给出球面 cosine-weighted 采样的 Jacobian 推导。

## 与其他采样页的关系
- [[stratified-sampling]]——把 Ω 切成 M 块，每块 1 个样本，保留 MC 的无偏性但降方差；
- [[low-discrepancy-sequence]]——Halton、Sobol 等确定性序列，QMC 的输入；
- [[poisson-disk-sampling]]——blue-noise 分布的采样，视觉更均匀但方差分析复杂；
- [[quasi-monte-carlo]]——用低差异取代 PRNG 的整体框架；
- [[pcg3d-hash]]——每像素独立 PRNG 的常见哈希种。
- [[mulberry32-rng]]——另一端的选择：32-bit Weyl + xor-shift，为「便利优先 + 确定性」场景设计，不追 PCG 的统计严谨度。
- [[rejection-vs-analytical-sampling]] — 实测结果完全反直觉：打开 `-O1` 后拒绝采样普遍快于解析解
- [[anisotropic-microfacet-sampling]] — marginal + conditional inversion 的经典工程案例（GGX/Beckmann/Blinn）

## Sources

- [[sources/slater-mc-sampling]]
