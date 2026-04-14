---
tags: [渲染, 球面基, 全局光照, 小波, 数学]
date: 2026-04-14
sources: 1
---

# Needlets（球面小波基）

**Needlet** 是一种定义在 $S^2$ 上的**局部化**球面基，由宇宙学家为处理 Cosmic Microwave Background（CMB）全天数据而发明。相比[[spherical-harmonics|球谐函数]]的「全局 Fourier 基」身份，Needlet 更像「球面上的 wavelet」——每一个 Needlet 都集中在球面上的一小块方向内，非零能量几乎不泄漏到背面，因此可以用来表达**带遮挡/掩码的信号**而不发生振铃。Robin Green 和 Mannie Ko 在 GDC 2012 *Math for Game Programmers* 讲座 *Frames, Quadratures and Global Illumination* 里首次把它引入游戏图形讨论。

## 动机：SH 的遮挡困境

SH 是**全局**基——它的每一个 $Y_\ell^m$ 都在整个球面上有支撑。于是如果你要把一个「只有上半球可见」的 visibility 信号投到 SH 上，边界附近（赤道）会出现类似 Fourier 在方波附近的 **Gibbs 振铃**。在宇宙学里这叫「galactic cut 问题」——银河系遮挡了一大片天区，要从 Planck 这样的数据里做 non-Gaussianity 分析必须先把银河带 mask 掉，而 mask 边界的 SH 伪影是硬伤。

游戏图形里的类比是：一个 light probe 的 visibility 通常只在部分方向有效，用 SH 存储 + 重建会在局部边界出现振铃和「ghost light」（绕到背面的伪光）。

## 需求

Robin Green 总结了 PRT 想要的一个球面基的四个性质，SH 满足前三个但不满足第一个：

- **局部化（localized）**——球面一侧的信号不会在另一侧产生能量；
- **球面原生（natural embedding on the sphere）**——不是在平面上构造再投影的 wavelet；
- **旋转不变（rotational invariance）**——重建精度不随方向变化，不会在旋转时「呼吸」；
- **保范数（norm-preserving）**——投影过程不丢能量。

Needlet 是目前已知同时满足这四条的最自然选择。代价：它**不是正交归一基**（ONB），而是 **tight frame**——所以失去了 ONB 的渐进逼近/独立系数解释，但保留了能量守恒等绝大多数好处。

## 构造配方

Marinucci 等 2008 年论文 *Spherical Needlets for CMB Data Analysis* 给了一个干净的实现配方：

1. **Littlewood-Paley 权重**：从一个 piecewise 指数 bump 函数 $f(t)$ 出发（形如 $\exp(-1/(1-t^2))$），通过数值积分得到一个光滑非递减的 $\psi(x)$，再用它构造一个对称的「1-on-plateau, smooth-down-to-0」分段函数 $\varphi(\xi)$，最后取正根得到权重 $b(\xi) = \sqrt{\varphi(\xi/B) - \varphi(\xi)}$。这里 $B$ 是 bandwidth 超参数，控制每个 Needlet 覆盖多少个 SH band。
2. **离散权重表**：对每一个层级 $j$，非零权重索引落在 $[B^{j-1}, B^{j+1}]$ 区间内，离线算出一张小表 $\{b(i)\}$ 备用——每个层级 $j$ 对应不同的频率段，类似小波的 scale level。
3. **Legendre 坍缩**：单个 Needlet 原本是一组 SH 的加权和，但**同一 band 内所有 SH 之和可以用单个 Legendre 多项式代替**——具体地 $\sum_m Y_\ell^m(\vec{e}) \overline{Y_\ell^m(\vec{e}_k)} = \frac{2\ell+1}{4\pi} P_\ell(\vec{e}\cdot\vec{e}_k)$。这条加法定理让评估代价从 $O(\ell^2)$ 降到 $O(\ell)$。
4. **Bonnet 递推**：$P_\ell$ 用 $(n+1)P_{n+1}(x) = (2n+1)\,x\,P_n(x) - n\,P_{n-1}(x)$ 从 $P_0=1, P_1=x$ 迭代得到，边迭代边累加权重，没有浪费。
5. **1D 查找表**：因为最终 Needlet 是一个关于 $x = \vec{e}\cdot\vec{e}_k$ 的 1D 函数（只依赖两个方向的夹角），可以离线打成查找表，运行时线性或二次插值重建——比 SH 的逐基现场评估便宜得多。

## 视觉直观

画出来的 Needlet 是一个高度方向性的球面 lobe，能量几乎全部在主方向 $\vec{e}_k$ 附近的一小个帽子里，绕到背面的「ghost light」伪影被几乎消除。因为每个 Needlet 是「零均值函数的正加权和」，它在整个球面上的积分**恒为零**——这给了它「纯方向性信息，不带 DC」的直观解释。

## 和其它球面基的对比

- vs. [[spherical-harmonics|SH]]：SH 全局基，Needlet 局部基；SH 是 ONB，Needlet 是 tight frame；SH 适合低频 diffuse，Needlet 适合带遮挡边界的信号。
- vs. spherical Gaussian：两者都是 lobe-shaped 局部基，但 SG 不是 frame，没有完备性保证；Needlet 从数学上更干净。
- vs. 平面上的 wavelet → 球面投影：投影方案会破坏旋转不变性；Needlet 是球面原生构造，旋转不变天然成立。

## 状态

Needlet 在图形学里的实际应用还算早期——它和 T-design 球面求积、Parseval tight frame 一起是 Green/Ko 在 GDC 2012 抛出的「新数学工具」。它的优势在 **visibility with partial occlusion** 和**方向性 lobe 表达**两类问题上最明显，但成熟的引擎集成案例还很少。

## 相关

- [[spherical-harmonics]] — 全局球面基，Needlet 的对立面
- [[robin-green]]

## Sources

- [[sources/green-implementing-needlets]]
