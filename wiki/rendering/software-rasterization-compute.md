---
tags: [渲染, 软件光栅化, compute, nanite, 几何, gpu]
date: 2026-04-27
sources: 1
---

# Compute 软件光栅化

将三角形光栅化的工作从 GPU 固定功能硬件搬移到 compute shader 的技术路线。

## 动机

硬件光栅器基于一个根深蒂固的假设：平均每个三角形覆盖约 10 个像素。当三角形密度达到像素级甚至亚像素级时，该假设彻底失效——2×2 quad 规则意味着每个像素级三角形至多只有 1/4 的线程做有效着色工作，效率降至约 25%。

这是 [[rendering/nanite-reyes-comparison]] 场景下固定功能光栅器被绕开的根本原因。[[people/brian-karis]] 在 Nanite 的公开访谈中印证了这一点：绝大多数三角形通过专门为此设计的 compute shader 软件光栅化。

## 基本结构

软件光栅的典型管线分三步：

1. **Cluster 剔除**（compute）：在 GPU 上对三角形集群做视锥、遮挡和背面剔除，过滤掉不可见几何体。[[rendering/culling]] 和 [[rendering/gpu-based-occlusion-culling]] 描述了现代 GPU 驱动剔除管线。

2. **软件光栅**（compute）：对通过剔除的三角形，每线程或每小组处理一个三角形，直接向 [[rendering/visibility-buffer]] 原子写像素覆盖信息（draw ID / triangle ID / barycentrics）。对无需剪裁、面积已接近像素的三角形，这条路径在吞吐量上可以超越固定功能光栅器。

3. **延迟材质求解**（compute）：从 visibility buffer 读取 ID，回查顶点属性重建 UV 和切线，再做材质着色。这使着色完全脱离三角形密度的约束。

## 软件 vs 硬件的取舍

软件光栅对小三角形有优势，但对需要剪裁、有 MSAA 或带输出合并（ROP）需求的三角形仍需退回硬件路径，因此实际系统通常是两条路径按三角形大小分派的混合方案。

另一个代价是丢失了基于 quad 的纹理梯度（`ddx/ddy`），所有纹理采样必须改用显式导数或 LOD，或依赖 [[rendering/temporal-antialiasing]] 来吸收由此产生的锯齿。

## 相关

- [[rendering/visibility-buffer]]
- [[rendering/nanite-reyes-comparison]]
- [[rendering/culling]]
- [[rendering/hierarchical-rasterization]]
- [[rendering/meshlets-and-mesh-shaders]]

## Sources

- [[sources/c0de517e-nanite-thoughts]]
- [[sources/karis-nanite-reyes]]
