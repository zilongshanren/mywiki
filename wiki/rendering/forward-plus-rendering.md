---
tags: [渲染管线, 前向渲染, 光照, 剔除, 实时渲染]
date: 2026-04-27
sources: 1
---

# Forward+ 渲染（Light Indexed Rendering）

Forward+ 是在传统 Forward 渲染管线上的改进，核心思路是**用 Tile 或 Cluster 结构在屏幕空间对光源做运行时剔除，代替 Forward 中必须对几何体做 CSG 切割来分配光源的方式**。

## 与 Forward 的关系

传统 Forward 渲染要把光源绑定到 draw call，多个动态光源若要精确剔除就必须在几何层面切分场景，或者用着色器排列组合爆炸（每种光源数量/类型组合一个 shader 变体）来处理。Forward+ 将这一责任转移到屏幕空间的数据结构：

- **Tiled**：屏幕分成若干 tile（如 16×16 像素），CPU/Compute 预先计算每个 tile 受哪些光源影响，填入 Light List，着色时只遍历 tile 对应的光源子集
- **Clustered**：进一步在深度方向分层，形成 3D Cluster，处理大深度范围下光源剔除精度更好

## 优势

- 无需几何切割，draw call 数量与 Forward 基准接近（而非 Forward 多光源时的指数级膨胀）
- 动态光源剔除效率远好于基础 Forward
- 支持 MSAA（与 Deferred 不同）
- 材质多样性无限制（同 Forward）

## 代价

- 必须有完整的**深度预通**（Depth Pre-pass）才能精确剔除；若使用 Clustered 则可软化这一要求，但覆盖大量灯光时精度下降
- 所有 shadowmap 必须在主光照通道前全部生成完毕（不能按光源逐帧摊销）
- 光照/阴影类型变化必须靠着色器内动态分支处理，ubershader 化程度高
- 与基础 Forward 相比，并非「免费」解决了排列组合问题——实质上只是把 per-draw 的静态排列组合换成了单一 ubershader 内的动态分支

## 与 Deferred 的对比

Forward+ 和 Deferred 的带宽/复杂度权衡方向相反：Deferred 在复杂光照/材质场景下更高效，但无法做 MSAA 且基线成本高。Forward+ 在中等规模动态光源、需要 MSAA 或特殊材质的场景下更合适。

[[angelo-pesce]] 指出对 Tiled 演示「数千点光源」的炫技应持保留态度——廉价无阴影点光源制造的是圆形光斑而非真实间接光，并非真正的光照质量提升，只是光源数量可扩展性的展示。

## 相关

- [[deferred-rendering]]
- [[light-prepass-pipeline]]
- [[tiled-light-prepass]]
- [[tiled-light-culling]]
- [[cascaded-shadow-maps]]

## Sources

- [[sources/c0de517e-realtime-renderer-notes]]
