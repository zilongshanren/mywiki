---
tags: [渲染, 光谱, 蒙特卡洛, 重要性采样, 路径追踪]
date: 2026-04-14
sources: 1
---

# Hero Wavelength 光谱采样

[[spectral-rendering|光谱渲染]]要解的积分是

$$\int_{360~\mathrm{nm}}^{830~\mathrm{nm}} \begin{pmatrix}\bar{r}(\lambda)\\\bar{g}(\lambda)\\\bar{b}(\lambda)\end{pmatrix} i(\lambda) \prod_{j=1}^{n-1} a_j(\lambda)\, \mathrm{d}\lambda$$

早期光谱渲染器的做法是把 RGB 三元组替换成**一个定长向量**（16 个波长），在每次顶点处做分量乘法。问题是：16 个波长不够准，但又已经太重。更现代的做法是**每条路径只随机采 $m$ 个波长**（常用 $m=4$），用 Monte Carlo 估计这个积分。

## 波长密度的选择

给定概率密度 $p(\lambda)$，无偏估计就是

$$\frac{1}{m} \sum_{k=0}^{m-1} \frac{1}{p(\lambda_k)} \begin{pmatrix}\bar{r}(\lambda_k)\\\bar{g}(\lambda_k)\\\bar{b}(\lambda_k)\end{pmatrix} i(\lambda_k) \prod_{j=1}^{n-1} a_j(\lambda_k)$$

密度应该尽量贴合被积函数。反射率 $a_j(\lambda)$ 平滑、接近 1，几乎不影响方差；但发射光谱 $i(\lambda)$ 可能像金卤灯那样尖峰密布，**必须重要性采样**。Christoph Peters 的选择是：

$$p(\lambda) \propto i(\lambda) \cdot \|(\bar{r}, \bar{g}, \bar{b})(\lambda)\|_1$$

即「光源谱 × RGB 色匹配函数的 1-范数」，再归一化。色匹配函数把「人眼根本看不见的远紫外/远红外波段」也压低了权重。

## 实现：1D CDF LUT

离线对每个光源谱做一次 CDF 反演：生成一个分辨率 1024、16-bit half 的 **1D RGBA 纹理**，每个位置 $u \in [0,1)$ 存

$$\left(\bar{r}(\lambda_u), \bar{g}(\lambda_u), \bar{b}(\lambda_u), i(\lambda_u)\right) / p(\lambda_u) \quad \text{其中 } \lambda_u = F^{-1}(u)$$

每条光源谱只占 **8 KiB**。路径追踪时一次查表就拿到所有需要的因子（包括把波长转成 [[fourier-srgb-spectral-upsampling|Fourier sRGB]] 用的相位 $\varphi$，可以合并在同一步），极其 cache coherent。

## 分层抖动：Hero Wavelength 命名的由来

Peters 的策略灵感来自 **[Wilkie14] Hero Wavelength Spectral Sampling**——与其独立采 $m$ 个波长，不如只生成**一个**均匀随机数 $u \in [0,1)$，然后把它分成 $m$ 段：

$$u_k = \frac{u + k}{m}, \quad k \in \{0, 1, \ldots, m-1\}$$

这实际上是均匀抖动分层采样（stratified jittered sampling）。它让 $m$ 个样本均匀散布在 CDF 域上，**互相抗偏**，同样 sample count 下噪声明显更低。原始 Hero Wavelength 论文把 $u_0$ 对应的那个波长叫 "hero"，其它波长附带计算；Peters 的版本做了等价的分层但不强调谁是 hero。

## 多光源怎么办：未完全解决

上面的整套策略依赖「提前知道发射光谱是哪一条」。对**单光源场景 + 直接光照**这是自然成立的；但对**长路径 + 多种光源**就不行——路径构造的时候还没决定要连到哪个光源。三条现有思路：

1. **先选光源，再采波长**：适用于直接光照——对每个顶点单独决定光源+波长。
2. **把所有路径顶点的 Fourier sRGB 三元组 + BRDF 权重存下来**，挑完光源之后再补波长。线性存储、二次运行时，对短路径 OK，长路径就爆炸。
3. **Wavelength guiding [Ruit21]**：先低分辨率渲染一张粗略预览，估计每个像素最终要接触的光谱形状，再据此采波长。有效但受粗离散化的限制——极窄峰仍然是弱点。

## 开销实测

在 RTX 5070 Ti / 1080p / 1 spp：

| 场景 | 路径长度 | RGB | 光谱 |
|---|---|---|---|
| Cornell Box | 2 | 0.26 ms | 0.31 ms |
| Cornell Box | 8 | 0.83 ms | 1.13 ms |
| Bistro | 2 | 2.71 ms | 2.89 ms |
| Bistro | 8 | 14.3 ms | 14.6 ms |

Bistro 里相对开销 2%~7%，绝对开销永远 ≤ 0.3 ms。光谱渲染至少在这种配置下已经不是"奢侈品"。

## 相关

- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[spectral-brdf]]
- [[poisson-disk-sampling]] — 另一类分层/准随机采样思路
- [[christoph-peters]]

## Sources

- [[sources/peters-spectral-rendering-2-real-time]]
