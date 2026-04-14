---
tags: [渲染, 全局光照, 光照, 虚拟点光源, 延迟渲染]
date: 2026-04-14
sources: 1
---

# Instant Radiosity 与虚拟点光源（VPL）

**Instant Radiosity** 是一种近似一次反弹全局光照的经典技术：把**间接光**表达成一大堆廉价的点光源。它的核心直觉很朴素——从主光源（比如方向光）向场景投射一束射线，击中表面的每一点都记录下来，然后在命中点生成一个新的**虚拟点光源**（Virtual Point Light，简称 VPL），颜色取自该点的表面 albedo、方向取自该点的法线半球。之后场景的「间接光」就退化成了「一场在众多弱小点光源下的普通直接光照」，实时渲染管线里现成的光照机制就能吃下来。

## 为什么和 light prepass / deferred 契合

[[tiled-light-prepass|Light prepass]] 与 [[deferred-rendering|deferred shading]] 都把几何和光照解耦，天生擅长处理「大量光源」这种情形；而 Instant Radiosity 生成的 VPL 动辄几百上千个，放在 forward 管线下几乎是灾难。deferred 下 G-Buffer 体积会因为更复杂的光照增大，light prepass 则相对轻量——这也是 [[kostas-anagnostou|Kostas Anagnostou]] 在 Hieroglyph 的 light prepass 渲染器上做这个原型的原因。

## 用 RSM 代替 CPU raycast

如何找到「光线 × 几何」的交点？可以走 CPU raycast、也可以走 GPU 路径追踪（比如 OptiX）。但还有一条更便宜的路子：**Reflective Shadowmap**（RSM）。从光源的视角把场景渲染一遍，得到两张小分辨率的 render target——一张存世界空间位置（或法线＋深度），一张存表面 albedo。每个 texel 就是一个 VPL。Kostas 在 32×32 的分辨率上就得到了可用的效果，最大的好处是不用把任何东西读回 CPU：两张纹理直接作为 shader 输入喂给光照 pass，从中提取 VPL 坐标和颜色。

这本质上和原始的 RSM 技术同出一辙，区别在于这里存的是**表面 albedo** 而非 *radiant flux*——这简化了实现，代价是后续如果要支持彩色光源就必须做两遍光照（一遍主光、一遍 VPL）。

## 已知的短板

- **无遮挡**——这是 Instant Radiosity 的老毛病：VPL 只是一个全向的点光源，光线可以「穿墙」照到它本不应该到达的地方。想要正确遮挡需要给每个 VPL 做一次 shadow query，成本极高；一个折衷是用 depth buffer 在屏幕空间做一次粗略的 occlusion。
- **不支持点光源作为主光**——因为 RSM 是「从光源看场景」的一次渲染，方向光和 spot light 天然能跑，而点光源需要 cube shadow map 或 dual-paraboloid 类方案。
- **主光数量必须极少**——每个主光都要一遍 RSM prepass，成本随之线性涨。
- **彩色光**需要额外的一遍光照。
- **密度有限**——32×32 意味着只有 ~1024 个 VPL，对大场景稀疏，好在也因此主光移动时闪烁较轻。

## 相关

- [[deferred-rendering]] — 大量小光源的天然消费者
- [[tiled-light-prepass]] — 原型使用的管线形态
- [[shadow-mapping-basics]] — RSM 是一次 shadow map 渲染的副产品
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-instant-radiosity-light-prepass]]
