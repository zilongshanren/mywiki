---
tags: [渲染, 光线追踪, BVH, 加速结构, AABB, SAH, 空间数据结构]
date: 2026-04-27
sources: 1
---

# BVH 构建算法

**包围体层次（Bounding Volume Hierarchy，BVH）**是光线追踪加速结构的标准形式。本页聚焦于 BVH 的**构建**侧；硬件遍历策略详见 [[rendering/bvh-traversal-hardware]]，DirectX 12 / Vulkan API 层的加速结构接口详见 [[sources/alain-rt-acceleration-structures]]。

## BVH 节点结构

最简 BVH 节点可表示为 64 字节（可进一步压缩），存储左右子 AABB 及子树指针：

```hlsl
struct BVHNode {
    float3 leftMin;  float3 leftMax;   // 左子节点 AABB
    float3 rightMin; float3 rightMax;  // 右子节点 AABB
    uint leftPointer; uint rightPointer;
};
```

三角形应通过**索引列表**引用而非直接嵌入节点，以便 BVH 在动画/变形时重排三角形顺序而不重写几何体。

## KD-Tree 对比

KD-Tree 节点更轻量（仅含父/左/右指针和分割平面标志），构建更快，但遍历效率低于 BVH。实时渲染优先采用 BVH。

## 构建策略三类

| 类别 | 代表 | 特点 |
|------|------|------|
| 自顶向下（Top-down） | SAH 分割 BVH | 质量高，适合离线 |
| 自底向上（Bottom-up） | PLOC（GPU 并行） | GPU 友好，速度快 |
| 插入式（Insertion） | 较少用于实时 | 增量构建灵活 |

实时渲染多用**自底向上**方式，因其高度并行，适合每帧/每几帧重建动态场景的 BVH。

## SAH（Surface Area Heuristic）

SAH 通过子节点包围盒面积之比估计光线命中概率，用于评估和优化分割质量：

```
SAH(node) = SA(left)/SA(parent) * N_left + SA(right)/SA(parent) * N_right
```

PLOC 等 GPU 构建器在 bottom-up 合并时用 SAH 选择最优配对，在 build quality 与 build speed 之间取得平衡。

## Morton 码加速

对 BVH 节点的 3D 位置编码为 **Morton 码**（32 位哈希，将 XYZ 三分量按 bit 交织），可在构建时快速排序空间位置相近的节点，降低 bottom-up 构建时配对搜索的复杂度。PLOC 使用此技术。

## 2 级 BVH（TLAS / BLAS）

DirectX 12 和 Vulkan 的硬件光追采用**两级 BVH**：

- **BLAS（Bottom Level AS）**：每个网格的几何体 BVH，用顶点/索引缓冲区构建
- **TLAS（Top Level AS）**：场景实例 BVH，每个实例持有 BLAS 引用及变换矩阵

这种设计允许同一 BLAS 被多个 TLAS 实例引用（实例化），动态物体可独立更新/重建其 BLAS 而不影响静态几何体。

## Sources

- [[sources/alain-rt-acceleration-structures]]
