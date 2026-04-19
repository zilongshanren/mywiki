---
tags: [渲染, 全局光照, 阴影, 半影, 几何]
date: 2026-04-19
sources: 2
---

# 半影假设（Penumbra Hypothesis）

**半影假设**由 Alexander Sannikov 在 [[radiance-cascades|Radiance Cascades]] 论文里提出，是一个关于光在场景中**哪里需要几何精度、哪里需要方向精度**的直观命题：

> 阴影的半影需要**靠近光源的高 linear 分辨率**（更多探针/像素）和**远离光源的高 angular 分辨率**（每个探针更多射线方向）；两者**反比**。

- **Linear resolution**（线性/空间分辨率）：单位面积内采样点的数量。
- **Angular resolution**（角度分辨率）：每个采样点发射射线的方向数。

越近越"需要细像素少方向"；越远越"需要粗像素多方向"。

## 为什么反比

考虑一个不透明半平面挡住的点光源（Sannikov 论文的经典图）。shadow 区和 full-lit 区之间的过渡带就是 penumbra。它的**角宽度**由"光源和遮挡物"决定，是个固定的角度 `α`。

- 距离光源 `d` 处，penumbra 的**线性宽度**大约是 `α * d`。距离 `d → 0` 时 penumbra 无限细：要分辨它需要**无数个像素**（高 linear 分辨率），但只需要在**接近光源的方向**采样（低 angular 分辨率就够）。
- 距离 `d → ∞` 时 penumbra 变成**巨大的柔和区域**：空间上几乎是均匀的（低 linear 分辨率够用），但像素从"半影任意一点"朝光源看过去，光源只占了**一个细长的角度范围**——需要密集的方向采样才能把光源对这个像素的贡献正确积分（高 angular 分辨率）。

一句话：**"penumbra 的总自由度是守恒的"**——你可以用密集探针粗略扫方向，或者稀疏探针密集扫方向，都能刻画同一条 penumbra。这给了一个非常有用的权衡框架。

## 对算法设计的启示

经典 GI 方案（path tracing、light probes、irradiance volumes）往往给**所有位置**一样的方向采样数，或者给**所有方向**一样的空间分辨率——这浪费了预算。半影假设给出了一条更聪明的路线：

- 在**近光源**铺密集探针，每个探针只发少量射线。
- 在**远光源**只放稀疏探针，每个探针发大量射线。
- 用某种机制把两端的数据**合并**成最终 radiance field。

这条路线的具体落地就是 [[radiance-cascades]]：每级级联对应一个距离段，空间分辨率和角度分辨率按反比 scaling——cascade 0 的探针最密、射线最少，cascade N 的探针最稀、射线最多。把相邻级联 bilinearly merge 就自动实现了"不同距离用不同精度"的策略。

## 直觉试验

tmpvar 的 [radiance-cascades playground](https://tmpvar.com/poc/radiance-cascades/) 把这个假设做成交互可视化：

- 把 cascade 0 的探针往光源拉近，你会看到探针数量自动稠密、方向稀疏。
- 把某个探针拉远，它接收的射线方向立即增多、空间邻居变稀。

这种"拖拽式理解"比公式高效——半影假设本质是几何的，可视化最对路。

## 局限

- 严格来说只适用于**点光源/面光源在均匀介质中的硬/软阴影**；对**体积介质**（[[volumetric-fog-froxels|fog]]、[[volumetric-raymarching-intro|raymarching volume]]）的适用性需要额外建模，但 Part 2 里 Yaazarai 指出 RC 对体积介质也能用（把 skybox 积分 merge 进最高 angular 级联即可）。
- 对**高光/view-dependent BRDF**不适用——半影假设只讨论 diffuse GI；specular 没法用"探针 + 射线方向"这个框架直接表达，因为 specular lobe 随视角变化。评论区已经有读者注意到这个限制。
- 对**interference/wave-like 的光学现象**（薄膜、衍射、彩虹）不适用——那是波动光学，半影是几何光学。评论区里"为什么没反映光的波长"的疑问就源于此。

## 相关

- [[radiance-cascades]] —— 把半影假设变成具体算法
- [[shadow-mapping-basics]] —— 传统 shadow 的软化路径（PCF、Poisson disk）
- [[moment-shadow-mapping]] —— 另一条用统计矩做 softshadow 的路径
- [[microfacet-brdf]] —— specular 的标准框架
- [[alexander-sannikov]]

## Sources

- [[sources/yaazarai-radiance-cascades]]
- [[sources/yaazarai-radiance-cascades-2]]
