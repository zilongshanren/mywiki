---
tags: [source, chipsandcheese, cpu, amd, zen5, desktop, granite-ridge, ryzen9000, avx512]
date: 2026-04-27
sources: 1
---

# AMD's Ryzen 9950X: Zen 5 on Desktop（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，以 Ryzen 9 9950X（Granite Ridge，双 CCD）为测试对象，聚焦桌面版 Zen 5 与移动版的差异，并用 libx264 和 Linux 内核编译两个实际工作负载做深入 top-down 分析。

## 摘要

桌面版 Zen 5 在移动版基础上增加了更多预算：每 CCD 32 MB L3（移动版仅 16 MB）、DDR5（约 70 ns 延迟 vs 移动版 LPDDR5 的 128 ns）、全宽 512-bit FP/向量单元、L1D 每周期双 512-bit 向量加载（移动版单路），以及 FP 加法延迟从 3 周期降至 2 周期。实测 libx264 IPC 提升约 22%（AVX-512 重度使用），Linux 内核编译提升约 15-22%（视对比 CCD 而定）。文章还借助 Zen 5 丰富的性能计数器做了详细的 top-down 流水线停顿分析，揭示整数寄存器堆容量是 Zen 5 的新瓶颈，以及跨 CCD 延迟高达 ~200 ns 的问题再次出现在桌面版上。

## 关键要点

- 桌面版 Zen 5 FP 单元全 512-bit 宽，L1D 支持 2×512-bit 加载/周期，移动版仅 1×512-bit
- FP 加法延迟桌面版 2 周期，移动版 3 周期（与 Zen 4 持平）
- 存储队列增至 104 项，且相邻写入同一 cacheline 仅用一个条目（优化 512-bit store 压力）
- libx264 中 Zen 5 最大停顿原因是 ROB 填满（好现象，说明其他资源比例合适）；内核编译中则是整数寄存器堆频繁满导致停顿
- 跨 CCD 延迟约 200 ns，几乎等同于服务器双插槽延迟，比 Ryzen 7950X3D 的 <80 ns 大幅退步
- VCache Zen 4（3D-V Cache）在时钟匹配测试中 IPC 更高，但较低的时钟导致整体落后 Zen 5

## 链接到的概念

- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[people/chester-lam]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-ryzen-9950x-zen-5-on-desktop
- 本地：`raw/articles/chipsandcheese.com/2024-08-14_amds-ryzen-9950x-zen-5-on-desktop.md`
