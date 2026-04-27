---
tags: [cpu, 微架构, intel, tremont, atom, x86, jasper-lake]
date: 2026-04-19
sources: 1
---

# Tremont：Atom 转向的那一代

Tremont 是 Intel 2019 年发布的 Atom 架构，用在 Jasper Lake、Snow Ridge、Lakefield。它是 [[gracemont-microarchitecture|Gracemont]] 的直系前辈：先在 Tremont 上验证的 [[clustered-decode-atom|双解码簇]]、[[non-scheduling-queue|非调度队列]]、"Core class branch prediction"这几招，都被 Gracemont 放大复用。"Gracemont 就是加大号的 Tremont"——Chester Lam 的一句话足以概括两代关系。

## 分支预测：第一次把 Atom 拉到 Skylake 水准

方向预测器用 overriding 双级结构，但 L1 预测器已经足够强，L2 很少真正接管。4096 项 BTB，**可回到 512 条 zero-bubble 分支**（当年只有 Gracemont、Zen 3 能并肩）。L2 BTB 多一个 pipeline stage，以节功耗换容量。实测在 7-Zip、libx264 上略逊 Skylake，但已经是同代 Atom 里的跃升。

## 前端：双 3-wide 解码簇

这是 Tremont 首次引入的核心创新——两个复制粘贴自 Goldmont Plus 的 3-wide 解码器，靠分支预测器在 **taken branch** 处做 round-robin 分流，让每簇接力处理后续指令，末端 mux 重排成线性流。省在：不需重造 4/5/6-wide 解码器、不需调 instruction queue 出口宽度。缺点很明显：**taken 分支太稀疏时退化为 3-wide**，Intel 优化手册里甚至建议每 16–32 指令插一条无条件 JMP。实测 128–160 条无 taken 分支后就卡 3-wide。Gracemont 把这招改成自动切换后，问题大幅缓解。

L1i 只有 32 KB（Gracemont 64 KB），且 NOP 流不能打满 L2 带宽。

## 后端：重排序接近 Haswell/Skylake，但调度器偏小

Tremont 的 ROB 达到 Haswell/Skylake 水准，寄存器堆也大，因为**没有 AVX**（向量寄存器只 128-bit），也**没有 SMT**（不必留一份影子寄存器）。这让它在用更小面积的前提下，达到可观的 reorder 容量。

整数调度器却是短板：分布式 45 项（其中一个端口只做分支，常用整数调度仅 31 项）。Zen 2 分布式也有 64 项且更灵活，Skylake 统一调度器更省。libx264 实测 Tremont 的 backend stall 中，整数/内存调度器填满是主要原因，而不是 ROB 填满——说明"指令重排空间"存在但"就绪检查"跟不上。

ALU 三口，multiplier 较慢（5 周期），LEA/rotate/bit test 都只有一个端口；memory unit 每周期 2×128-bit load + 1×128-bit store。

## 向量侧：没有 AVX 是硬伤

Tremont 完全不支持 AVX，SSE 场景下吞吐也意外羸弱（2×64-bit 整数加法只能做到 1/cycle）。在 hybrid 配置里这是致命问题：OS 可以在大小核之间迁移线程，程序若在大核检测到 AVX 然后被迁到 Tremont 就会 crash。**Gracemont 补齐 AVX 支持，就是为了让 hybrid 可行**——这是从 Tremont（Lakefield）到 Alder Lake 的关键设计修正。

## 存储与 store forwarding

Tremont 的 store forwarding **只在 load 地址与 store 按 load 大小对齐时成功**：64-bit store 的上下 32 bit 可转 32-bit load，其余情况全 fail（12–13 周期）。Skylake 的转发是 load 完全包含于 store 即成，延迟仅 7–8 周期，差距显著。ARM Neoverse N1 做类似保守转发但能跨 cache line，Tremont 跨 cache line 直接再加 1 周期。两种设计的共性：低功耗优先。

## 内存子系统：受限明显

L1D 3 周期、L2 1.5 MB、L3 从 Alder Lake 借来（在 Jasper Lake 则是独立 4 MB LLC）。单核 L3 带宽"比移动 SoC SLC 还差"，L2 每核只 16 B/cycle、整簇 32 B/cycle。Gracemont 把 L2 口翻倍到 32 B/core + 64 B/cluster，就是针对这个痛点调的。

## 定位：转型期的中间状态

Tremont 跨越手机→桌面/边缘的转向。Intel 往 Atom 里加总内存加密（对抗冷启动攻击）、加 QoS（云场景隔离租户）、加"accelerator interfacing"（配合 GPU offload）。单核功耗极低（Celeron N5095 每核 2 W 多），perf/W 显著优于 Skylake，但绝对性能仍被甩开一代。它不强，但它是 Intel 把 Atom 从手机撤出来、押注"大小核 + hyperscale"战略的起点。

## 参见

- [[gracemont-microarchitecture]]
- [[clustered-decode-atom]]
- [[non-scheduling-queue]]
- [[intel-hybrid-alder-lake]]
- [[branch-predictor-design]]
- [[cpu-scheduler-design]]
- [[neoverse-n1-microarchitecture]] — 低功耗核的相似 store forwarding 取舍

## Sources

- [[sources/chipsandcheese-tremont]]
- [[sources/chipsandcheese-alder-lake-caching-power]]
- [[sources/chipsandcheese-goldmont-plus]] — Goldmont Plus 至 Tremont 演化分析
