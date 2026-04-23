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
- [[non-cryptographic-hash]] —— Burst 与原生 C 的 codegen 差异是不显眼的瓶颈子类
- [[dynamic-resolution-scaling]] —— 瓶颈识别结论是 Pixel-bound 后的下一步：按比例砍像素计算量
- [[xplane-headlight-perf-teardown]] —— 2011 X-Plane 10 车灯全流程瓶颈手术案例
- [[simd-memory-bandwidth-bound]] —— 「更聪明的 SIMD 反而更慢」的判别路径

## Sources

- [[sources/rtr-day01]]
- [[sources/playcanvas-profiler]]
- [[sources/gameknife-gkengine-rendering-optimization]] —— Intel GPA 逐 pass 时间分析的实战范例，把『先剖析再修改』的方法论落到具体 shader 指令数
