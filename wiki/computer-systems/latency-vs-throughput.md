---
tags: [计算机体系结构, 性能]
date: 2026-04-05
sources: 1
---

# Latency vs Throughput

两种性能指标，**常常互相权衡**。

## 定义

- **Latency（延迟 / 响应时间）**：完成**一个**任务需要多长时间。
- **Throughput（吞吐量）**：单位时间内能完成**多少**任务。

## 权衡示例

**流水线**：
- 增加 Throughput（每周期出一个结果）
- **恶化** Latency（一条指令走完整个流水线的总时间更长）

**Batching**：
- 增加 Throughput（批量处理降低 per-item 开销）
- **恶化** Latency（必须等待 batch 填满）

**Caching**：
- Cache Hit 时两者都改善
- Cache Miss 时延迟极差（100 倍 L1 hit 的时间）

## 游戏开发场景

- **帧率 vs 延迟**：高帧率（高 throughput）不等于低 input latency。VR 游戏特别敏感。
- **批处理 vs 响应性**：合 DrawCall 改善吞吐但可能打断响应式逻辑。
- **异步加载**：改善整体流畅度（throughput）但单次加载延迟可能更长。

## Ousterhout 的视角

这个权衡与 APoSD 无直接关系，但"优化需明确目标"的思想相通——不清楚是为 latency 还是 throughput 优化，就会做出错误权衡。

## 相关

- [[amdahls-law]]
- [[cpu-performance-formula]]
- [[memory-hierarchy]]

## Sources

- [[sources/caqa-day01]]
