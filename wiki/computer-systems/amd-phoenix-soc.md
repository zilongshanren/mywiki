---
tags: [cpu, gpu, amd, phoenix, soc, apu, mobile, rdna3, zen4, xdna, lpddr5]
date: 2026-04-27
sources: 1
---

# AMD Phoenix SoC

Phoenix 是 AMD 2023 年发布的 APU（加速处理器），制造于 TSMC N4 工艺，die 面积 178mm²，254 亿晶体管，装入与 Rembrandt 相同的 25×35mm BGA 封装。Ryzen 7040 系列（含 Ryzen 7 7840HS）和 Ryzen Z1 Extreme（ASUS ROG Ally）均基于 Phoenix。

## CPU 侧

CPU 集群为 8 颗 [[computer-systems/zen4-microarchitecture|Zen 4]] 核，与桌面版架构相同但 L3 缩减至 16 MB（2 MB/核，桌面版为 4 MB/核）。L3 延迟与桌面版一致，实际延迟因频率限制（如 HP 锁 4.5 GHz，而 SKU 应可达 5.1 GHz）略高。内存控制器支持 DDR5 和 LPDDR5，后者实测延迟约 120ns，相比 [[rendering/van-gogh-steam-deck-apu|Van Gogh]]（Steam Deck）的 LPDDR 延迟有大幅改善。

CPU 到 Infinity Fabric 的接口为 32 bytes/cycle，读写路径对称（桌面版写路径仅 16 bytes/cycle）。CLZERO 指令清零优化使单核有效写带宽可超 68 GB/s，内存分配场景受益明显。

## GPU 侧

GPU 为 Radeon 780M，基于 [[rendering/rdna3-architecture|RDNA 3]] 架构：6 WGP，768 SIMD lanes（1536 FP32 ops/cycle），分布在两个 shader array，各 256 KB 中间层 cache，全局 2 MB L2 cache。2 MB L2 与 AMD RX 7600 独立显卡相同容量——在 iGPU 上配比相当奢侈，有效减少了 DRAM 访问。

由于无 Infinity Cache，L2 miss 直接打到 DDR5/LPDDR5，延迟明显高于同架构独立显卡。但 DDR5-5600 的带宽实测超越 GDDR5 GTX 1050，足够 iGPU 的 SIMD 规模使用，专门 Infinity Cache 难以成本合理化。与 Van Gogh 相比，L2 带宽提升数倍，SIMD 数量增加 50%。

GPU 前端与 shader array 运行在相同时钟，而非像 RX 7900 XTX 那样前端超频——理由是 iGPU 规模较小，shader array 本身是瓶颈而非分发端。

## Infinity Fabric 动态时钟

Phoenix 的 Infinity Fabric 实现了动态时钟策略：GPU 密集访存时降低 fabric 时钟（GPU 有 4×32B/cycle 端口，低频下带宽足够）；CPU 密集工作时升高时钟（CPU 应用对延迟更敏感）。与 Renoir 的固定 1.6 GHz fabric 时钟相比更灵活节能。

配合新增的 Z8 睡眠状态（介于 C0/C1 之间的极短断电态，唤醒延迟可察觉），视频播放场景可高度驻留在 Z8，媒体引擎的大缓冲区支持突发访存而非持续唤醒。

## XDNA AI 引擎

XDNA 来自 Xilinx 收购后的 AIE-ML 架构，Phoenix 集成 16 个 AIE-ML tile，支持 BF16（5 TFLOPS，~1.25 GHz）和 INT8，面向低功耗 ML 推理。每个 tile 有 64 KB 数据 SRAM（非 cache，无标签检查）、16 KB 程序 SRAM、以及专用 512-bit 累加器转发接口。引擎支持 50% 稀疏性，稀疏矩阵解压和 mask 计算由硬件完成。整体 L2 SRAM 推测约 2 MB（4 个 memory tile×512 KB）。

相比直接用 RDNA 3 iGPU 做 AI 推理，XDNA 功耗效率更高，是 AMD 首次在移动端给出 Intel GNA/IPU 的回应。

## 音频协处理器

Phoenix 集成 2 个 DSP 的音频协处理器，可在极低时钟下持续运行（语音唤醒场景），亦可运行小型 AI 降噪模型。此外利用 20-35 kHz 超声波（人耳不可听的频率范围）通过 Doppler shift 检测人体存在，支持第三方开放使用。

## Sources

- [[sources/chipsandcheese-phoenix-soc]]
