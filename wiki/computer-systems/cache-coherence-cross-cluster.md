---
tags: [缓存一致性, 互连, 多核]
date: 2026-04-19
sources: 1
---

# 跨簇缓存一致性

同核复合体（cluster / CCX）内部的缓存间搬运，与跨复合体的搬运，在现代多核里是两套机制、两套延迟档位。测 core-to-core latency（两核之间 bouncing 同一条 cache line）能把这两套边界清晰暴露出来。

## 两级一致性

- **同簇**：由簇内的 Snoop Control Unit + snoop filter 处理。Arm DSU-120 就是典型实现，簇内 cache 间直接 peer-to-peer 搬运，无需外部 fabric。
- **跨簇**：需要走外部 coherent fabric。Nvidia/Mediatek 在 GB10 上用的是 High Performance Coherent Fabric；AMD 用 Infinity Fabric 的 Coherent Station。

## 测量结果的"阶梯"

以 [[gb10-memory-subsystem|GB10]] 为例：
- X925 同簇：50–60 ns
- A725 跨簇最坏：240 ns
- Strix Halo 同等跨簇：~100 ns（AMD 明显更优）

跨簇的 latency 本质上是 fabric 层一次额外的 round-trip，Arm 这代 fabric 与 AMD Infinity Fabric 对照下处在劣势。对 OS scheduler 的含义是：**亲和性不仅要区分大小核，还要尽量把协作线程约束在同簇内**。

## 与 split lock 的关联

[[split-lock-x86]] 下，原子操作如果跨 cache line，CPU 会退化到所谓 "bus lock" 处理路径——在 Zen 系列上似乎会穿过 Infinity Fabric 的 Coherent Station，也就是跨簇一致性所走的同一条 fabric，这正是跨簇 atomic 延迟被放大的根因之一。

## 相关

- [[gb10-memory-subsystem]]
- [[split-lock-x86]]
- [[memory-hierarchy]]

## Sources

- [[sources/chipsandcheese-gb10-cpu-memory]]
