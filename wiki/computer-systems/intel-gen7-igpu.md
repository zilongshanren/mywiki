---
tags: [gpu, intel, igpu, gen7, ivy-bridge, eu, subslice, history]
date: 2026-04-27
sources: 1
---

# Intel Gen 7 集成显卡（Ivy Bridge）

Gen 7 是 Intel 随 Ivy Bridge（2012 年）发布的集成 GPU 架构，也称 HD 4000/4200 等。它标志着 Intel iGPU 从"附属显示单元"向可编程通用 GPU 的转型，引入 DirectX 11 支持，并奠定了延续至今的 Intel GPU 设计语言。

## 层次结构

Gen 7 的基本执行单元（EU）组织成 subslice。一个 subslice 内含若干 EU、私有的两级采样器缓存（L1/L2 sampler cache）以及 data port。Subslice 是 Gen 7 的可缩放粒度——Intel 可调节每个 subslice 的 EU 数量，实现非常细粒度的 GPU 规模调整，这与 AMD CU 和 Nvidia SM 的粒度不同（那两者不能内部再拆分）。GPU 级别有一个共享的 L3 cache（约 256 KB，部分容量留给固定功能硬件）。

## EU 执行模型

Gen 7 EU 不采用直接内存访问指令，而是通过 send 消息指令与 subslice 共享组件（data port、采样器）通信。这种解耦设计使 EU 与 subslice 共享逻辑相对独立，支持以 EU 粒度伸缩 GPU 规模。

寄存器文件采用固定分配策略：每个 wave 固定拥有 128 向量寄存器，调度器最多跟踪 8 个活跃 wave。与 AMD/Nvidia 不同，使用较少寄存器不会提升占用率，且不支持使用更多寄存器换低占用率（直至 Ponte Vecchio 引入 Large GRF 模式——可用 256 寄存器但占用率降至 4 wave）。这一固定占用模型延续至 [[rendering/xe-hpg-architecture|Xe]] 架构，只是 EU 改名 Vector Engine，subslice 改名 Xe Core。

调度器每周期可选择一对 wave 双发射到两条执行管道（FPU pipe + EM pipe）。EM pipe 原为扩展数学运算（倒数、逆平方根），Gen 7 扩展使其也能处理 FP 加法和 FMA。INT32 指令只能使用 FPU pipe，吞吐率是 FP32 的一半。

## 缓存延迟特性

Gen 7 的采样器缓存延迟异常高：L1 sampler cache 约 141ns，L2 sampler cache 约 145ns。这使得 compute kernel 倾向于绕过采样器、直接走 GPU L3（约 87ns 延迟）。L3 容量约 256 KB，部分被固定功能硬件占用，Surface Pro 测试平台上用户可见容量约 128 KB。

与 Nvidia Fermi（Quadro 600）对比，Intel iGPU 的 DRAM 延迟控制更好，受益于 CPU 侧高度优化的内存控制器。总体 L3 吞吐接近 Fermi，但采样器延迟差距明显。

本地内存（OpenCL local memory）从 GPU L3 分配而非专用 SRAM，导致 local memory 延迟远高于 Nvidia 的 SM-private shared memory，限制了 compute 场景的同步性能。

## 历史影响

Gen 7 建立的架构基因——subslice 分层、send 指令访存、固定 128 寄存器/8 wave 占用模型——贯穿整个后续 Gen 系列，并在 [[rendering/xe-hpg-architecture|Xe-HPG]] 时代基本保留。Intel 后来扩展成更大 iGPU（Ice Lake Gen 11、Tiger Lake Gen 12）并最终推出独立显卡，但均建立在 Gen 7 的设计语言之上。

## Sources

- [[sources/chipsandcheese-ivy-bridge-igpu]]
