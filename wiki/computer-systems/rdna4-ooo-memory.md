---
tags: [gpu, amd, rdna4, memory, wave, vmcnt, out-of-order, dependency]
date: 2026-04-27
sources: 1
---

# RDNA 4 的乱序内存访问

RDNA 4 在内存子系统上做出了自 GCN 以来最显著的架构改动，核心目标是消除 RDNA 3 及更早架构中存在的两类隐性依赖问题。这些改动对光追工作负载尤为重要，因为光追在同一 WGP 上同时进行指针密集型 BVH 遍历和缓存友好的纹理采样，两者的内存访问模式截然不同。

## 跨 Wave 伪依赖的根源

GCN 以来，AMD GPU 用硬件计数器（`vmcnt`）追踪 wave 内待完成的内存访问，允许编译器通过等待计数器归零来处理数据依赖。但在 RDNA 3 及更早架构中，多个 wave 共享同一内存访问队列，且队列按全局顺序返回数据——某个 wave 的缓存缺失会阻塞队列中排在其后的条目，即使这些条目属于其他 wave 且数据早已就绪。

这意味着一个高延迟 wave（如做大跨度指针追逐的 BVH 遍历）可以拖慢同一 WGP 上其他低延迟 wave（如纹理采样）的内存访问速度。实验结果直接验证了这一点：在 RDNA 3 上，快 wave 的访问量与慢 wave 严格按循环展开倍数锁定。

## RDNA 4 的修复方式

RDNA 4 为每个 wave 提供独立的内存访问队列（或实现了乱序队列排空），使不同 wave 的访问相互独立。实验中两个 wave 的执行完全解耦，各自按内存延迟节奏推进。

## vmcnt 拆分：更细粒度的等待控制

与跨 wave 修复并行，RDNA 4 还将单一的 `vmcnt` 计数器拆分为多个独立类别：

- **全局内存访问**（原 vmcnt 主体）
- **纹理采样请求**（之前与全局内存合并）
- **光线相交测试结果**（raytracing 新增）

类似地，`lgkmcnt` 拆分为 `kmcnt`（标量内存）和 `dscnt`（LDS 访问）。

拆分后，编译器可以独立等待特定类别的访问，在等待纹理采样的同时继续发射 BVH 相交测试指令，或在等待全局内存时做 LDS 操作，大幅提升指令级并行度。

## 与 Intel / Nvidia 的对比

Intel 从 Gen 9（Skylake Graphics）起便无此跨 wave 伪依赖问题，XVE 使用软件管理的 scoreboard，任何指令均可独立设置/等待 scoreboard 条目，天然支持乱序。Nvidia 同样：Turing（图灵）起消除了此问题，但 Pascal 在同一 SM sub-partition 的 wave 之间存在类似的假依赖。

RDNA 4 的计数器方案与 Intel/Nvidia 的 scoreboard 方案各有取舍：计数器方案允许以一个 bit 的扩展就翻倍队列容量，但灵活性不如 scoreboard；scoreboard 方案可精确等待任意单条请求，但每个 scoreboard 条目占用更多硬件资源。

## Sources

- [[sources/chipsandcheese-rdna4-ooo-memory]]
