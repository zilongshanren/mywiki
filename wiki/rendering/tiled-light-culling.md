---
tags: [渲染, 光照, 延迟渲染, forward-plus, 分块]
date: 2026-04-14
sources: 1
---

# 分块光照剔除（Tiled Light Culling）

**Tiled deferred / tiled forward（Forward+）的共同光源剔除机制**：把屏幕切成 16×16 的 tile，为每个 tile 计算 min/max 深度、构造一个视锥小棱台，再和每个光源的影响球做相交测试——得到的 per-tile 光源列表被实际着色阶段复用。这是 2012 年前后从 DICE / Intel 起逐步成为主流的高光源数量方案。

**[[brian-karis|Brian Karis]]** 2012 年在 Graphic Rants 上提出了一个不一样的想法：**让 specular 的光泽度参与剔除**，而不是只用一个固定半径的球。注意这个概念和 [[tiled-light-prepass]] 不同——后者指 Crystal Dynamics Foundation 引擎那套「先 light 后材质」的二次几何提交方案，是管线结构；而 tiled light culling 指 tile 级的光源可见性剪枝，和 deferred/forward 的管线结构正交。

## 光衰减与剔除半径的矛盾

物理正确的光衰减是 $1/d^2$——**任何非零距离都有非零贡献**，对游戏引擎是噩梦。一张地图里几百上千个光源，理论上每个像素都要考虑全部。实践中必须人为截断，常见两种做法：

1. **减常数再 max 0**：$\text{fall} = \max(0,\ 1/d^2 - \text{tol})$。整个影响域内全局损失能量。
2. **距离窗口函数**：例如 $(1 - d^2/a^2)^2$ 在有限半径内平滑衰减到 0。近处能量不变、远处主动削掉。

Karis 选了第一种作为讨论起点——**tol 是这个光源的能量误差容差**。这也是 tiled culling 里那个「每个光源有一个半径」的物理来源。

## 为什么 specular 破坏了这个框架

能量守恒的 specular 峰值**远高于 Lambert diffuse**——即便在介电体上也是。一根蜡烛离镜面铬球 20 米，diffuse 贡献早就被容差削光了，但 specular 高光仍然清晰可见（那一小块铬球上所有像素都会采样到它）。**Diffuse 的剔除半径和 specular 的剔除半径差好几个数量级**，如果两者都用 `radius = max(diffuse_radius, spec_radius)`，那就等于 specular 的大半径永远覆盖住 diffuse 需求——diffuse 剔除白干了。

## 关键观察：能量守恒反过来帮剔除

Karis 的观察：能量守恒约束下，**高光泽度的 BRDF 虽然峰值强、作用距离远，但其作用立体角很小**——镜面铬球反射出的那根蜡烛只占一像素大小的反射区域。**峰值** × **作用立体角 ≈ 常数**。

这意味着——**每个 tile 的 specular 剔除不止是距离问题，还是方向问题**：一个 tile 内所有像素的反射向量 $R$ 构成一个锥（normal cone 的 specular 版本），tile 内的 per-light 剔除除了距离门槛之外，还可以检查该光源方向是否落在这个 specular cone 内。

## Specular cone 剔除

对 Phong 形式 $\frac{n+2}{2} (L \cdot R)^n$，给定容差 $\text{tol}$，非零的 $L$ 构成一个围绕 $R$ 的锥，锥角：

$$
\text{angle} = \arccos\left( \sqrt[n]{\frac{2\,\text{tol}}{n+2}} \right)
$$

把 tile 内所有 pixel 的 $R$ 向量做**锥并**（cone union），得到 tile 的 specular 影响锥。任何一个光源若同时满足「在距离门槛外」**或**「方向在 specular cone 外」，就对该 tile 的 specular 无贡献。

具体工程上：

- **球距离剔除 + 方向锥剔除**合并进一个剔除 kernel，光源通过剔除当且仅当 `diffuse_contribution > tol` **或** `specular_contribution > tol`——Karis 强调**不要**维护两份独立的 diffuse/specular 光源列表（diffuse 本来就比 specular 便宜，算一次两用）。
- 注意 $(n+2)/2$ 因子应该卷进距离衰减而不是角度门槛里，这样 spec 锥角简化成 $\arccos(\text{tol}^{1/n})$。
- 高光泽光源的**影响球半径也要扩大**——gloss 越高，特殊情况下反射高光所需的距离越远（想象一面镜子反射一公里外的霓虹灯）。

## 与 importance sampling 的关系

Karis 把这个方案类比为**偏置的重要性采样**——它不是严格的剔除，而是**给每个光源一个已知的能量误差容差**，可以精确控制偏差幅度。好处：

- 反射表面的**视觉丰富度**显著提高——远处 specular 高光不再被粗暴砍掉，而是按能量阈值自适应保留。
- **误差可控**——不像 artist-authored radius 那种靠美术手感调出来的黑魔法。

## 落地策略：runtime + 预烘焙的分割

Karis 在 Prey 2 当前世代（360/PS3）上的实际做法是**把 deferred 光源的影响范围截在一个 artist 手工设定的半径**，超出半径的部分被**预先烘焙进 lightmap（diffuse）和 env map（specular）**——从而物理上保住 $1/d^2$ 的衰减律不丢能量，只是把远场部分固化成静态贡献。这个分割很重要：**远处光源的 specular 高光仍然能在反光表面上出现**，而不是被硬砍掉。他希望用 specular cone culling 替代这种「slop」（手动烘焙带来的误差），用一套 runtime 剔除实现同样的视觉完整性。

## 和 Brian Karis 更大图景的关系

这篇博客（以及下一篇 [[sparse-shadows-cone-tracing]]）预告的几个思想——**cone 剔除、多几何表示、trace 做远场 specular shadow**——几乎一字不差地出现在十年后的 UE5 Lumen 里：Lumen 的 screen probe GI 和 reflection passes 正是在 tile / probe 粒度上做 cone-based 的可见性 + 遮蔽计算。从这个意义上，Graphic Rants 的 2012 年博客是 Lumen 架构的起点笔记之一。

## 相关

- [[deferred-rendering]] —— tile 剔除的典型宿主
- [[tiled-light-prepass]] —— Foundation 引擎的 thin G-Buffer 二次几何提交方案，不是同一件事
- [[microfacet-brdf]] —— specular 剔除靠的就是能量守恒约束
- [[physically-based-shading]]
- [[culling]] —— normal cone / backface 剔除是同类思路
- [[sparse-shadows-cone-tracing]] —— Karis 后续一篇：把 specular shadow 留给 cone trace
- [[brian-karis]]
- [[tiled-light-trees]] —— O'Donnell & Chajdas I3D 2017：tile 内再建 BVH 解决 clustered shading 的"坏 tile"问题（高深度方差下光源列表膨胀），并用 tree + clustered 混合方案在几乎所有场景下都不慢于任一单路

## Sources

- [[sources/karis-tiled-light-culling]]
