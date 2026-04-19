---
tags: [source, graphics, visibility-buffer, gpu-driven, executeindirect, async-compute, forge]
date: 2026-04-19
sources: 1
---

# Triangle Visibility Buffer（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 2018 年 3 月首发（2021 年两次更新）的长文，完整描述 Confetti 在 [[the-forge-renderer|The Forge]] 中实现的 **Triangle [[visibility-buffer|Visibility Buffer]]** 管线，同时把 2015 年启动的研究项目彻底梳理成一份 postmortem 式的技术总结。

## 摘要

文章覆盖从**三角形剔除 → VB 填充 → Forward++ 分簇光照**的完整流水线。起点是 2015 年 Christoph Schied 到 Confetti 办公室用 OpenGL 复现 *Deferred Attribute Interpolation* 的原型；经过 2.5 年的简化与工程化，最终演变为 Burns & Hunt *Visibility Buffer* 的一个**加了 triangle filtering + draw call compaction**的工业版本，用 DX12 `ExecuteIndirect` + async compute 重新组织。核心管线分四步：(1) CPU 做 cluster cone culling 先砍一批组；(2) async compute 对剩下的三角形逐条做背面 / 近裁面 / 视锥 / 小图元测试，Olano-Greer 2D 齐次矩阵判背面、子像素 bbox 测小图元；(3) draw call compaction 去空洞压紧 indirect argument；(4) 一次 `ExecuteIndirect` 光栅到 **R8G8B8A8 VB + depth** 两张 32-bit RT。后续 shading pass 用 drawID / triangleID 反查 IB/VB，显式计算屏幕空间重心偏导（Schied 论文 Eq.4），走 tiled light list 一次算完 directional + 所有 point light。文章同时附带 1080p / 4K 下的 VB vs 5-rendertarget G-Buffer 带宽对比，以及 San Miguel 8M 三角形在多视点剔除后的具体数字（主视 2.32M、阴影视 1.84M）。

跨平台实现同时提供 DX12 / Vulkan / Linux VK / macOS Metal 2 / 主机版本（主机版本 on-request），所有代码在 The Forge 公开 repo，文中所有 `.fsl` shader 文件都给出 GitHub 链接。

## 关键要点

- **三级剔除**：CPU cluster cone + GPU 三角形过滤 + draw call compaction，配合 `ExecuteIndirect` 最终只提交"按摩过"的可见几何
- **Multi-View 剔除**：主视 + 阴影视 + RSM 同一个 compute 里同时做；牺牲剔除率，换**每个三角形只 fetch 一次**的带宽优势
- **Olano-Greer 2D 齐次坐标背面判据**：`det(float3x3(v0.xyw, v1.xyw, v2.xyw)) ≥ 0` 即为背面 / 退化，理论 50% 剔除
- **Small primitive test**：用子像素 bbox 测是否覆盖 MSAA 采样点，避免小三角形在光栅里空转
- **VB 布局 64 bit**：`[1 alphaMasked][8 drawID][23 triangleID]` + 32 bit depth，显著优于 5 张 G-Buffer
- **Forward++**：VB 保证每像素一层，shading pass 重建 barycentric 偏导 + tiled light list 一次算完所有光源
- **99% L2 cache hit** 对 texture/VB/IB，因为屏幕空间访问模式是 GPU 架构的"理想形状"
- **memory bandwidth 是 VB 的主要收益**——1080p 2× MSAA 下 VB ≈ G-Buffer 的 1/3，分辨率越高差距越大
- 该管线在 Supergiant *Hades* 等出货游戏上验证
- 评论区 **MJP** 指出 barycentric 偏导公式在近裁面处会炸（越过摄像机的三角形 W 接近零投影失效），需要显式 near-plane clip 或 3D 长算法回退

## 链接到的概念

- [[visibility-buffer]]
- [[triangle-filtering-pipeline]]
- [[the-forge-renderer]]
- [[deferred-rendering]]
- [[async-compute]]
- [[bindless-rendering]]
- [[gpu-based-occlusion-culling]]
- [[multidraw-indirect-occlusion-culling]]
- [[meshlets-and-mesh-shaders]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2018/03/triangle-visibility-buffer.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2018-03-30_triangle-visibility-buffer.md`
