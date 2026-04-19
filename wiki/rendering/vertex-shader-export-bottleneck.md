---
tags: [vertex-shader, 性能瓶颈, nvidia-gpu, 固定功能单元]
date: 2026-04-19
sources: 1
---

# Vertex Shader 导出数瓶颈（ISBE / PE / TRAM）

Nvidia GPU 上 VS 导出的属性数并不"免费"——哪怕 PS 几乎不用、哪怕 VS 本身极简单，export 多了 drawcall 成本也会显著上涨。[[kostas-anagnostou|Kostas Anagnostou]] 2025 年用 RTX 3080 mobile 做了受控实验，1→10 个 float4 export 让 drawcall 成本**近 3 倍**。原因在 VS→PS 之间有多个可以成为瓶颈的固定功能单元和中间存储。

## N 卡的数据流

```
VS → [L1: ISBE] → Primitive Engine (含 VPC 做 cull/clip) → [L1: TRAM] → PS
```

- **ISBE**：VS 输出 attribute 在 SM L1 里的专门分配
- **PE（Primitive Engine）**：读 ISBE 做 culling / clipping，把处理后的 per-triangle attribute 写入 TRAM。VPC 是 PE 里做 cull/clip 的子单元
- **TRAM**：每 SM 16KB，每 attribute component 每三角形 12 字节（3 顶点 × 4 字节）——1 个 float4 attribute 48 字节 / 三角形，10 个就 480 字节 / 三角形
- **stall 类型**：allocation stall（容量不够）、fill stall（上游填不够快）

实测随 export 增加：TRAM 分配 1405 → 4646 字节/SM、TRAM fill stall 显著上升、VPC 压力显著上升、L1↔L2 流量显著上升（提示 VPC 用 L2 做中转）；ISBE 分配本身基本不变，但 VS warp 因 ISBE 容量不够 stall 的比例上升——**VS 和 PS 同时被拖慢**。

## 精彩反例：PS 不用 VS exports

如果 PS 不读 VS exports，drawcall 成本**完全不变**、TRAM 分配不变——编译器或硬件能感知没人用，不分配。这解释了为啥"多导出但未用"通常不是热点。

## 粒度和跨厂商对比

- **分配粒度是 float 不是 float4**：8 个 float 约等于 2 个 float4 的 TRAM，N 卡不会 round up
- **float vs int 交错 export**：没测到显著差别，这颗 GPU 不区分插值 / 非插值类型
- **AMD GCN 5.0**：不管 PS 用不用 exports，drawcall 成本**都不变**；且随 export 数上升的斜率远小于 N 卡

## 实用建议

- **N 卡上 VS export 是真实瓶颈**，要紧盯 pack / 压缩 interpolant
- **AMD GCN 上几乎不是问题**——别一刀切照搬 N 卡的建议
- 极简 PS + 极简 VS 的 test 放大了 export 成本的可见性；真实 shader 里 export stall 可能被更重的计算隐藏
- 可以改用 pull model（从 buffer 里 fetch 顶点数据）或 mesh shader 绕开传统 VS export 路径

## 相关

- [[gpu-utilisation-holistic-tuning]]
- [[vertex-shader-basics]]
- [[compact-vertex-format]]
- [[meshlets-and-mesh-shaders]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-vertex-shader-exports]]
