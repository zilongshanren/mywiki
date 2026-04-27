---
tags: [cpu, intel, cannon-lake, palm-cove, 10nm, microarchitecture, avx512]
date: 2026-04-27
sources: 1
---

# Cannon Lake 微架构（Palm Cove）

Cannon Lake 是 Intel 10nm 工艺的首款量产产品，CPU 核心架构代号 Palm Cove，本质上是 Skylake 的 10nm 工艺移植（"Tick"）。2018 年仅以单一 SKU 形式上市：Core i3-8121U（双核四线程，TDP 15W，最高 3.2 GHz）。它是 Intel "Tick-Tock" 战略中最惨烈的受害者之一，不仅姗姗来迟，还因 iGPU 良品率问题被迫禁用集成显卡，最终以灰色姿态淡出历史。

## 10nm 工艺问题

Intel 最初承诺 10nm 将比竞争对手的同名工艺密度更高，为此设置了激进的设计规则。实测结果令人失望：在相同功耗窗口内，14nm 的 Kaby Lake 反而比 Palm Cove 性能更好。即使仅对比核心功耗，Palm Cove 的改善也相当有限，且大部分优势来自 AVX-512 而非工艺本身。对比整数基准（7-Zip），去掉 AVX-512 的加成后，Palm Cove 甚至在低功耗下输给基于 14nm 的 Goldmont Plus（Atom 级架构），这暴露出 10nm 早期良率和性能调校的全面失败。

从芯片面积看，10nm 的密度优势是真实的——Palm Cove 核心面积仅为 Kaby Lake 的 43%，这也是它能在受限面积内塞入 AVX-512 的原因。但密度提升未能转化为性能/功耗改善。

## 核心变化

Palm Cove 相对 Skylake 的微架构改动刻意保持最小化，符合"Tick"定位：

- 数学调度器从 58 项增至 62 项
- 加载追踪队列从 72 项增至 80 项（退休前追踪）
- 存储队列从 56 项增至 58 项
- BTB 容量小幅增加（约 4608 项 vs Skylake 的约 4096 项），密集分支的零气泡行为略有改善

这些变化对性能影响微乎其微，主要体现 Intel 并不打算在"Tick"代做大改动的理念。

## AVX-512 实现

AVX-512 是 Palm Cove 相对客户端 Skylake 最显著的新特性。Intel 通过融合 port 0 和 port 1 上现有的两个 256-bit FMA 单元来处理 512-bit FMA：模式要么是 2×256-bit，要么是 1×512-bit，**不能同时支持两种模式**。这意味着在 256-bit 和 512-bit FMA 混合的代码中被卡在 1 IPC，无法充分发挥理论吞吐。Port 5 的向量整数单元则被扩展至完整 512 位，不受此限制。

L1D 带宽随 AVX-512 大幅提升（512-bit 加载/存储），实测在极低时钟下仍能保持对 4.5 GHz Kaby Lake 的带宽优势，说明带宽增益真实。相比 Skylake 客户端，L2 带宽也略有改善。

## iGPU（Gen 10）

Cannon Lake 最引人注目的部分不是 CPU 而是占据 **45% 芯片面积**的 Gen 10 iGPU（5 个子切片，每个 8 EU，共 320 FP32 lanes，远超 Skylake GT2 的 192）。Gen 10 引入了多项重大变化，后来均在 Gen 11 (Ice Lake) 中实现量产：

- 本地共享内存（SLM）从 iGPU L3 移入子切片内部，降低延迟、减少与全局内存的竞争
- iGPU L3 缓存扩大至约 1536 KB（Gen 9.5 为 768 KB）并重新布局，缩短子切片到缓存的路径
- 更强的媒体引擎（可能支持双路视频编解码）
- 更大的显示控制器缓冲区，支持突发式内存访问以节省功耗

由于 iGPU 良品率不足，Cannon Lake 出货时禁用了集成显卡，不得不搭配独立显卡驱动显示，严重破坏了超低功耗产品的功耗策略（独显需要额外为其 VRAM 供电）。这一决定使得 Cannon Lake 在实际功耗测试中表现远低于预期。

## 系统代理

Cannon Lake 的系统代理包含比前代更大的显示控制器（带有大型 SRAM 缓冲区，用于低功耗突发访问）和一个全新的图像处理单元（IPU），IPU 负责摄像头 RAW 数据处理（如去马赛克）。此外 Cannon Lake 还集成了 Intel 第一代高斯神经加速器（GNA），专为语音降噪和语音识别推理设计，功耗约等于 50% 的 1.1 GHz Atom 核心，体现了 Intel 当时向 SoC 化方向发展的尝试。

## 历史意义

Cannon Lake 代表了 Intel 在 AMD Zen 崛起前的战略：在 CPU 性能领先无忧的假设下，将 die area 投入 iGPU、IPU、GNA 等专用加速器，以应对 ARM 在移动端的冲击。10nm 的失败打断了这一路线，迫使 Intel 此后数年持续依赖 Skylake 衍生架构应战，并将精力重新集中于提升 CPU 多核性能。

## 相关

- [[skylake-microarchitecture]]
- [[sunny-cove-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[netburst-microarchitecture]]
- [[xe-hpg-architecture]]
- [[dennard-scaling]]
- [[cpu-clock-frequency-ramp]]

## Sources

- [[sources/chipsandcheese-cannon-lake]]
