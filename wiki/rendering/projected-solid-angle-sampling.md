---
tags: [渲染, 采样, 光源, 阴影, 实时渲染]
date: 2026-04-14
sources: 1
---

# 投影立体角采样（Projected Solid Angle Sampling）

**面光源着色**需要对光源表面做蒙特卡洛采样，方差取决于采样密度和被积函数匹配得有多好。对于漫反射表面，理论上最优的策略是**按投影立体角**（projected solid angle = 立体角 × $\cos\theta$）采样——这样恰好消去了 Lambertian 余弦项，把方差几乎压到零。

问题是：对**球形光源**而言，「把球面以余弦加权投影到单位半球后的分布」是一个很丑的形状（一个圆形立体角在法线平面上的投影，被余弦加权）——它既不是圆也不是椭圆，也没有简便的解析反 CDF。离线渲染的已有算法存在，但对 GPU 不友好。

Christoph Peters 和 Carsten Dachsbacher 在 i3D 2019 的论文给出了一个**实时可用**的解法。

## 核心洞察：cut disk 分解

一个被地平面（切线平面）裁掉下半部分的圆盘叫 **cut disk**。论文的核心观察是：

> **球形光源的投影立体角可以精确分解（或至少良好近似）为若干个 cut disk 的并集**。

cut disk 本身是可以高效采样的——论文给出专门的 `SampleCutUnitDisk()` 算法。把球形光源拆成 cut disks 后，只要按面积加权选一个、对它做 cut disk 采样，就能得到一个（接近）按投影立体角分布的方向。

偏差是**可证明有界**的——对于那些"不是精确分解而是近似"的配置，论文给出了误差上界。

## 性能

相比"简单按立体角采样"（不考虑 $\cos\theta$），这个方法只贵 2-3 倍，但**方差低得多**——几乎没有噪声。在 1 spp 的 ray-traced soft shadow 场景里直接可用，不需要 denoiser 的重拳。

## 适用范围

- **漫反射表面 + 球形光源 + 无遮挡**：直接用，效果最好。
- **有遮挡**：可见性仍然需要 ray cast 评估，方差会回来。
- **非球形光源**：方法思想可以推广，但具体 cut disk 分解要重新推导。

## 一个学术细节：勘误

论文 Algorithm 2/3/4 的伪代码里，调用 `SampleCutUnitDisk()` 时第一参数应该减去 $\pi/2$——这是论文正式版和作者版都有的笔误。**附带的源代码是正确的**，实现者请以源码为准。

## 相关

- [[poisson-disk-sampling]] — 另一类方差削减的思路
- [[rendering-pipeline]]
- [[christoph-peters]]

## Sources

- [[sources/peters-projected-spherical-caps]]
