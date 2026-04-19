---
tags: [光线追踪, DXR, 加速结构, D3D12, SM6.10]
date: 2026-04-19
sources: 1
---

# DXR Tier 2.0：CLAS / Cluster Template / PTLAS

GDC 2026 上 Microsoft 公告的 [DXR Functional Spec Part 2](https://microsoft.github.io/DirectX-Specs/d3d/Raytracing2.html)，对应 `D3D12_RAYTRACING_TIER_2_0` 与 Shader Model 6.10。核心是把**加速结构从两层扩到三层**，并把"每帧从头重建 TLAS"这道坎撬松——[[adam-sawicki|Adam Sawicki]] 的 GDC 2026 评注认为这是本届最实在的一组新特性。

## 三个新结构

### 1. Cluster Level Acceleration Structure（CLAS）

- 像光追版的 meshlet：**最多 256 顶点 + 256 三角形**的一小块网格
- 真正的 **Bottom Level Acceleration Structure (BLAS)** 由 CLAS 组合而成
- 好处：
  - 构建成本可切成碎片，**跨帧摊销**
  - 天然配合 [[d3d12-work-graphs|meshlet/nanite]] 流水线的几何粒度
  - 允许只重建变形/进入 LOD 的局部 cluster

### 2. Cluster Template

- **没有顶点位置**的 CLAS 原型——一张"拓扑模板"
- 实际 CLAS 由 template + 顶点位置 `instantiate` 出来，适合动画角色每帧出不同姿态的 CLAS
- 规格说"intended to be an upgrade versus traditional updates / refits"——目标是取代现有的 BVH refit 模式

### 3. Compressed1 Position Encoding

- 顶点位置的新压缩编码
- 用**共享指数 + delta**（让 Sawicki 联想到浮点共享指数格式）
- 省显存——BLAS 建筑内存长期是光追的隐性成本大头

### 4. Partitioned TLAS（PTLAS）

- **TLAS 再上一层**：PTLAS → Partitions → Instances
- 一个 Partition 推荐 **100–1000 个 instance**
- 解决"每帧重建整个 TLAS"问题：只动变化的 partition
- 对开放世界、长直播放场景特别关键——主流引擎至今仍每帧 rebuild TLAS

## 新的 Indirect BLAS 构建

加速结构构建操作现在也能走 **Indirect** 命令——GPU 自己决定哪些 BLAS/CLAS 要建。配合 GPU-driven 几何管线可以完全脱离 CPU 干预。

## 为什么重要

- [[d3d12-work-graphs]] 让 rasterization 一侧脱离 CPU；DXR Tier 2 让 ray tracing 一侧也跟上
- "加速结构重建"长期是光追的**隐性卡点**：静态场景可接受，动态大场景里"每帧 TLAS"经常占一整个 ms
- cluster 粒度让 AS 构建和 meshlet 管线的几何粒度**对齐**——同一套 LOD 决策可以同时服务光栅和光追

## 相关

- [[adam-sawicki]]
- [[d3d12-work-graphs]]
- [[hybrid-raytracing-pipeline]]
- [[pix-api-and-dxdmp]]
- [[advanced-shader-delivery]]
- [[hlsl-cooperative-vectors-tensor-cores]]

## Sources

- [[sources/asawicki-dx12-gdc-2026-comments]]
