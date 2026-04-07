---
tags: [渲染, 性能]
date: 2026-04-05
sources: 1
---

# 瓶颈分析（Bottleneck Analysis）

渲染优化的第一原则：**找到瓶颈，只优化瓶颈**。管线并行运行但被最慢阶段拖住——优化非瓶颈阶段是白做功。

## 瓶颈识别方法

| 测试 | 结果 | 瓶颈位置 |
|---|---|---|
| 降低分辨率一半 | FPS 大幅提升 | Pixel Processing（GPU-bound，fillrate/bandwidth） |
| 降低分辨率一半 | FPS 几乎不变 | CPU 或 Geometry |
| 减半 DrawCall 数 | FPS 大幅提升 | CPU（DrawCall cost） |
| 简化顶点数 | FPS 大幅提升 | Geometry（vertex processing） |
| 简化 fragment shader | FPS 大幅提升 | Pixel shading ALU |

## 常见瓶颈分布

- **移动端**：通常是带宽或 CPU DrawCall（而非 GPU ALU）。
- **桌面端**：通常是 pixel shader ALU 或 fillrate。
- **VR 游戏**：pixel processing（双眼 + 高分辨率）。

## 相关

- [[rendering-pipeline]]
- [[draw-call]]
- [[overdraw]]

## Sources

- [[sources/rtr-day01]]
