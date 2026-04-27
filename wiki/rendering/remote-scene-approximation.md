---
tags: [渲染, LOD, 远景近似, 八面体 impostor, 点云, 体素, 网格简化, 场景传输]
date: 2026-04-27
sources: 1
---

# 远端场景近似（Remote Scene Approximation）

"远端场景近似"是 [[angelo-pesce]] 为一类问题起的名字：**用更廉价的表示替代远处（或来自远端服务器）的场景几何，使客户端只需加载和渲染一个压缩的代理物**。其约束比通常的 LOD 更严苛——源几何不在客户端本地，必须在服务器生成、压缩后传输，并优先保证客户端运行时性能与内存。

这篇工作日志式文章（Roblox 背景，2023 年）的价值不在于给出一个成品方案，而在于以"分支—实验—归纳"的节奏，将**整个解空间映射成一张对比图**，并通过多轮原型排除或验证主要风险点。

## 设计维度

Pesce 列出五个正交的选择轴：

- **视图无关 vs 视图相关**：视图无关（如 remeshing LOD、[[octahedral-impostors]]）对服务器友好，不需针对每个玩家视角生成；视图相关质量更好但服务器成本高。
- **表示类型**：图像（billboard/impostor）、点云/体素、网格、体积（NeRF/Gaussian Splat）。
- **外观与几何的耦合程度**：传统 octahedral impostor 把外观和可见性一起烘焙，非常冗余；解耦后（仅存深度 per viewpoint + 单独 UV 属性）可大幅节省传输量。
- **压缩友好性**：规则结构（heightfield、隐式体素）天然可 delta 更新；自由形状（任意网格）压缩效率低。
- **客户端转码缓存**：允许客户端额外处理（如从深度图 transcode 到 billboard）可解锁更紧凑的传输格式。

## 原型轨迹

**原型一：Octahedral Impostors（快速验证）**。技术成熟、工具齐全，可直接在 Unreal/Unity 插件中测试。主要发现：对非凸几何（如城市网格）遮挡层次复杂，impostor 出现透视穿帮；更致命的是**贴图开销极大**，因为要同时存颜色/法线/粗糙度 per-view，适合高度实例化对象，不适合"一次性多边形汤"。

**原型二：基于体素的网格重建（Blender Python → C++）**。流程：体素化（OpenVDB）→ 边塌陷简化（QEM）→ 自动 UV → 多视点光栅属性烘焙。Blender 脚本证明流程可行，但光追烘焙太慢。切到 C++ 后改用多视点深度图生成点云 + Poisson 重建（screened Poisson），10k 面网格可在数秒内完成，成为初步可用的基线。

**原型三：2D 低多边形包裹验证**。为快速验证"是否能不通过 decimation 直接拟合低多边形 mesh"，在 CToy 写了 2D 线段版本：体素化 → 内外投票 → SDF → 低分辨率网格 + 梯度驱动收缩（类布料解算）。证明原理可行，但 3D 扩展的计算成本仍是未解风险。

## 连接点

整个探索中反复出现的等价关系：点云 → 压缩整数坐标 → 二进制稀疏体素八叉树；深度图 → 点云；heightfield → 低密度点云 → billboard；Octahedral impostor → 多视点深度图 → 点云。这种"各方法之间存在连续谱"的观察是文章最有价值的元论点。

## 相关

- [[dynamic-occlusion-culling-roblox]] — 同一作者同期对深度图生成点云/体素的遮挡剔除探索
- [[gaussian-splatting-web]] — Gaussian Splat 作为体积表示的现代选项，文中提及
- [[occlusion-culling]]、[[hierarchical-z-buffer]]
- [[efficient-sparse-voxel-octrees]]
- [[nanite-reyes-comparison]] — 关于极限 LOD 表示的另一视角

## Sources

- [[sources/c0de517e-remote-scene-approximation]]
