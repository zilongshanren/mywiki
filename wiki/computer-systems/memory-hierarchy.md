---
tags: [计算机体系结构, 性能, 缓存]
date: 2026-04-05
sources: 2
---

# 存储层次（Memory Hierarchy）

**跨越 5 个数量级延迟**的存储分层：

| 层级 | 典型延迟 | 大小 |
|---|---|---|
| Register | 0 cycle | 几十字节 |
| L1 Cache | 1-4 cycles | 32-64 KB |
| L2 Cache | 10-25 cycles | 256 KB - 1 MB |
| L3 Cache | 30-60 cycles | 8-64 MB |
| DRAM | 200-300 cycles | GB 量级 |
| SSD | ~100,000 cycles | TB 量级 |

## 不对称的代价

- **一次 DRAM miss ≈ 100 次 L1 hit**。
- 一次 SSD miss ≈ 1,000,000 次 L1 hit。

**Cache miss 比指令低效率贵得多**——优先级上远超指令级优化。

## 局部性原理让它有效

> "The memory hierarchy takes advantage of the principle of locality." — CAQA

注意"takes advantage of"：我们**利用**程序的局部性行为，而不是**依赖**。详见 [[locality-principle]]。

## 游戏开发的直接影响

- **ECS/DOTS** 的 SoA 布局：数据连续，cache 命中率极高。
- **Mipmap**：纹理缩放级别保持空间局部性。
- **Texture Atlas**：避免 texture switch 的同时改善局部性。

## CSAPP 的观察

> "Application programmers aware of cache memories can exploit them to improve performance by an order of magnitude."

10× 级别的性能差距，不靠换算法或并行化，靠数据布局。

## 相关

- [[locality-principle]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[cpu-performance-formula]]

## Sources

- [[sources/caqa-day02]]
- [[sources/csapp-day01]]
