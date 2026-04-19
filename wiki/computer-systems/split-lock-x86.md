---
tags: [x86, 原子操作, 缓存一致性, 多核, 性能]
date: 2026-04-19
sources: 1
---

# x86-64 Split Lock

**Split lock** 指访问跨 cache line 边界的原子操作（`lock cmpxchg`、`lock add` 等）。正常情况下现代 CPU 用缓存一致性协议锁单条 cache line，不妨碍其它核心对无关地址的访问。但 Intel 和 AMD 都没机制一次锁两条 line，遇到跨行 atomic 只能回退到所谓 **bus lock**——一种行为上可以"把整个系统按停"的 fallback 路径。

## 名字里的"bus"已经名存实亡

早期多处理器系统真有共享总线，`lock` 前缀就是锁这条总线。现代互连是非阻塞、分布式的（Intel 的 IDI + ring bus、AMD 的 Infinity Fabric 一众组件）。Intel 和 AMD 仍然沿用"bus lock"术语但含义不再清晰，观测表现也因硬件而异。Chester 呼吁厂商精确文档化"split lock 在我们家硬件上到底影响什么"，而不是继续沿用 bus lock 一刀切描述。

## 不同硬件的惩罚差异极大

测法：core-to-core latency 测试让两核用 `_InterlockedCompareExchange64` 互抛一个 counter，把目标值的起始地址放在靠近 line 末尾处造出跨行。同时另起线程跑内存延迟/带宽基准与 Geekbench 6（photo filter / asset compression），测其它线程的受害程度。

| 平台 | split lock c2c latency | 受影响范围 |
|---|---|---|
| AMD FX-8350（Piledriver） | 2–3× 同行 | **完全不影响 cache hit，甚至 L3 都不受影响**；只在 DRAM 层有惩罚 |
| Intel Skylake i5-6600K | 比 Arrow Lake 好 | L2 hit 不受影响，L2 miss 受损 |
| Intel Celeron J4125（Goldmont Plus） | 高 | L2 可 hit 不受影响；DRAM 带宽降 |
| Intel Alder Lake i7-1265U | ~7 µs P-core 间 | L3 只是轻微下滑；GB6 几乎不掉 |
| Intel Arrow Lake 285K | 7 µs | L2 内完全免疫，L2 miss 后 bandwidth 减半 |
| AMD Zen 2（3950X） | ~几百 ns | **L1D 以外全崩**（L2/L3/DRAM 带宽延迟 ~10×） |
| AMD Zen 5（9900X） | ~500 ns | **L1D 以外全崩**（同 Zen 2） |

Piledriver 是最亮眼的反直觉结果——用老架构的粗粒度一致性协议反而保住了 10 MB cache 不被 split lock 污染。Alder Lake 的 Intel 硬件虽然 latency 高，但对其它核"邻居"隔离最好。AMD 在 Zen 2/5 上退化最严重——推测 split lock 直接回退到 Infinity Fabric 的 Coherent Station 层处理，见 [[cache-coherence-cross-cluster]]。

## Linux 的默认 mitigation

`split_lock_mitigate` 默认开启，做法是 trap + 故意注入 **毫秒级** 延迟，让调用方"感到烦躁"。效果相当于把 split lock 变成机械硬盘寻道级的行为。Chester 的评价一分为二：
- 服务器/多租户：合理，和 cache partitioning / 带宽节流一样属于 QoS
- 消费者桌面：过度反应——很多游戏长期用 split lock 没出过事，却可能因为默认 mitigation 在 Linux 上掉到 10 FPS，Windows 正常 200 FPS。这种"scream test"恰恰是阻碍 Linux 桌面普及的老毛病

## 实践含义

程序员应该尽量避免 split lock（对齐 atomic 变量到其 natural alignment 足够）。硬件侧空间也很大：Piledriver 证明了 split lock 不必把整个缓存层次拖下水。

## 相关

- [[cache-coherence-cross-cluster]]
- [[memory-hierarchy]]
- [[undefined-behavior-c-cpp]]
- [[calling-conventions-x86]]

## Sources

- [[sources/chipsandcheese-split-locks]]
