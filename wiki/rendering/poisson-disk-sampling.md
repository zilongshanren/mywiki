---
tags: [渲染, 采样, 信号处理]
date: 2026-04-14
sources: 2
---

# 泊松盘采样（Poisson Disk Sampling）

**Poisson disk sampling** 生成一组在空间中尽可能均匀但不规则的点：任意两点之间距离都不小于某个最小半径，同时在足够大的尺度上覆盖率均匀。这比规则网格采样在视觉上更自然（避免周期性 moiré 伪影），又比纯随机采样更均匀（避免聚团 / 空洞）。

## 在渲染里的用途

- **阴影柔化（PCF / PCSS）**：用 Poisson 偏移采样阴影贴图，避免格子状的硬边和摩尔条纹
- **景深（DoF）模糊**：在 CoC 半径内做 Poisson 采样，用很少的样本得到「盘形 bokeh」
- **SSAO**：半球内的 Poisson 采样作为方向集
- **重要性采样**：纯蒙特卡洛的低差异替代品
- **泛 blur 内核**：圆形或方形 Poisson 内核可以避免方向偏好

## 「渐进」（progressive）顺序

[[bartosz-wronski|Bart Wronski]] 的[小工具](https://github.com/bartwronski/PoissonSamplingGenerator)按一个有用的属性生成序列：**前 N 个点本身也是一个良好的 Poisson 分布**。这意味着可以根据自适应分支只取前一半甚至前几个样本，仍然得到合理方差——例如 DoF 里 CoC 小的像素只取前 4 个样本，CoC 大的像素取全部 25 个。

实现思路：每加一个新点时，在候选池里挑一个「到所有已有点的最小距离最大」的点。算法本质是 Mitchell's best-candidate 或 Bridson 算法的简化版。

## 支持的形状

工具支持四种典型场景：

- **disk**：单位圆盘，常用于 PCF / DoF
- **disk with central tap**：第一个点强制为原点，方便在中心叠 weighting
- **square**：单位方块
- **repeating square**：考虑周期性边界，让方块拼接时也保持均匀——常用于 screen-space tiling

## 缓存优化

工具有一个可选的「按 tile 排序」选项：把生成的点序列按 n×n 网格分桶，让相邻索引的样本位置在空间上也相邻。对采样大区域（large kernel）或纹理空间不连贯的访问是显著优化——降低 cache miss。

## 输出

直接生成 HLSL / C++ 数组，复制粘贴即用。这种「离线生成 + 烘进代码」的工作流是图形里很常见的模式，避免运行时再算 / 再加载小型常量数据。

## 相关
- [[aliasing]]
- [[bartosz-wronski]]
- [[hero-wavelength-spectral-sampling]] — 类似的分层抖动思路在波长维度的应用
- [[projected-solid-angle-sampling]] — 球形面光源的高效采样
- [[quasi-monte-carlo]] — QMC 把「随机」换成「低差异」的另一条降方差路线
- [[stratified-sampling]] — 负相关采样的更便宜变种
- [[low-discrepancy-sequence]] — Halton / Sobol 等 QMC 常用点列
- [[shadow-mapping-basics]] — 软阴影的 Fibonacci 圆盘采样是同一思路
- [[max-slater]]
- [[swap-and-pop-removal]] — active list 随机消费场景下的 O(1) 删除技巧
- [[poisson-rect-process]] — 把点过程扩展成无限平面上的无重叠随机矩形
- [[infinite-chunked-procedural-generation]] — 点过程/矩形过程共用的分块无关方法论
- [[iterative-sample-point-relaxation]] —— Pesce 2010 的 stochastic Lloyd 变体，用 importance 本地化权重到排斥半径

## Sources
- [[sources/bartwronski-poisson-sampling]]
- [[sources/vertexfragment-list-removal]]
- [[sources/bartwronski-poisson-gui]]
- [[sources/c0de517e-sample-generator-3d]]
