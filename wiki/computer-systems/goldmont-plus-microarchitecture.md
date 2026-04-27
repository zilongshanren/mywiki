---
tags: [cpu, 微架构, intel, atom, goldmont-plus, gemini-lake]
date: 2026-04-27
sources: 1
---

# Goldmont Plus 微架构

Goldmont Plus（GLP）是 Intel Atom 在 2017 年推出的微架构，搭载于 Gemini Lake 平台（14 nm），2020 年停产。它处于 Atom 演化史上一个微妙的过渡位置：相比早期手机导向的 Silvermont 有显著提升，但尚未达到为混合核战略服务的 [[tremont-microarchitecture|Tremont]] 所拥有的完整能力。

## 核心结构

Goldmont Plus 是 3-wide 超标量乱序架构。ROB 93 条目（Silvermont 仅 32 条目，Core 2 也是约 96 条目量级），整数/浮点寄存器堆采用 PRF 方案（整数 66 条目，浮点 75 条目）。浮点/向量执行为双管道 128-bit，不支持 AVX。Silvermont 使用 ROB-based 寄存器方案，GLP 切换为 PRF 是一次现代化升级，节省了退役时的寄存器复制开销。

## 前端特点

前端有 32 KB 指令缓存，以及独立的 64 KB 预解码缓存（predecode cache）。预解码缓存与 L1i 解耦，即使指令被 L1i 驱逐，预解码信息仍可保留，避免重复预解码开销——这是 Arm 设计（预解码信息随 L1i 行存储）所不具备的。解码宽度 3 uop/cycle，重命名器 4-wide（宽于前端，Chester Lam 推测是为 Tremont 的 4-wide 前端铺路）。

BTB 2048 条目，3 cycle 延迟，分支预测能力接近 Skylake 但受 BTB 容量限制在大分支足迹时有压力。

## 内存与缓存

L1D 仅 24 KB（低于 Intel/AMD 大核的 32 KB），且为 write-through 设计，配合 4 KB 写合并缓冲（write-coalescing cache），类似 Bulldozer 策略。这会增加 L2 写流量，在面积受限下是一种节省设计。

缓存层次为两级：L1D 24 KB + 共享 L2（Celeron J4125 为 4 MB）。无共享 L3，L2 直接面对 DRAM。L2 19 cycle 延迟，性能接近 Intel Core 2 L2。DRAM 延迟超过 180 ns（远高于同期低端 Core 平台的约 60–80 ns）。

## 在 Atom 演化链中的意义

Goldmont Plus 标志着 Atom 面积效率路线的局部终点：它有了能让乱序执行真正发挥作用的足够大缓冲区，但 14 nm 节点和手机形态遗留的功耗约束使它既无法在超薄设备中保持低功耗，又无法与同期入门级 Core ULV 抗衡。Intel 随后在 [[tremont-microarchitecture|Tremont]] 中引入 [[clustered-decode-atom|集簇解码]] 并切换到 10 nm，才算真正打开了 Atom 融入混合核设计的大门。

## Sources

- [[sources/chipsandcheese-goldmont-plus]]
