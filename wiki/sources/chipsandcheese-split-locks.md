---
tags: [source, x86, atomic, cache-coherence, linux]
date: 2026-04-19
sources: 1
---

# Investigating Split Locks on x86-64（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2026 年 4 月的 split lock 跨 x86-64 硬件横测。

## 摘要

split lock = 原子操作跨 cache line 边界。Intel/AMD 没有机制同时锁两条 line，只能退回所谓 "bus lock"——术语源于真有共享总线的年代，现在已没有精确含义。文章在 Arrow Lake、Alder Lake、Zen 5、Zen 2、Piledriver、Skylake、Goldmont Plus 共 7 种硬件上压测 split lock，结合 Geekbench 6 photo filter / asset compression 作为真实 workload proxy。发现硬件差异巨大：AMD Piledriver 最优（只影响 DRAM，不影响任何 cache），Intel Alder Lake 隔离性最好（其它核受害最小），AMD Zen 2/5 最糟（L1D 以外全崩，~10× 退化）。Linux 默认 mitigation（trap + 毫秒级延迟）被作者评价为对桌面场景过度反应。

## 关键要点

- "bus lock" 术语已失真，Chester 呼吁厂商用更精确文档替换
- Piledriver：split lock 不影响 L3，10 MB cache 全保住
- Zen 2/5：L1D 以外全 10× 退化，推测退到 Infinity Fabric Coherent Station
- Alder Lake：E-Core 受害轻微，P-Core latency 达 7 µs
- Arrow Lake：L2 内免疫，L2 miss 后 bandwidth 减半
- Skylake 比 Arrow Lake/Alder Lake 的 split lock latency 还低
- Linux `split_lock_mitigate` 默认 = 把 split lock 变机械硬盘寻道级延迟
- 游戏长期用 split lock，Linux 默认值可能让 Linux 版掉到 10 FPS

## 链接到的概念

- [[split-lock-x86]]
- [[cache-coherence-cross-cluster]]

## 原文

- 链接：https://chipsandcheese.com/p/investigating-split-locks-on-x86
- 本地：`raw/articles/chipsandcheese.com/2026-04-08_investigating-split-locks-on-x86-64.md`
