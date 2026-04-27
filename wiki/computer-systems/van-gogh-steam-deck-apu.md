---
tags: [apu, amd, van-gogh, steam-deck, zen2, rdna2, lpddr5, igpu, 嵌入式, 游戏主机]
date: 2026-04-27
sources: 1
---

# Van Gogh：Steam Deck 的 APU 设计

Van Gogh（AMD Custom APU 0405）是专为 Valve Steam Deck 设计的片上系统，将四枚 Zen 2 核心与 RDNA 2 iGPU 整合于 TSMC 7nm 工艺的单颗芯片。它不是通用笔记本芯片，而是一颗以游戏性能为中心、在极低功耗（≤16 W）下取得 GPU-CPU 权衡极端化的主机芯片。

## 配置概览

- CPU：4 核 8 线程 Zen 2，单 CCX，4 MB L3，最高 3.5 GHz boost
- GPU：RDNA 2，4 WGP，512 FP32 通道，最高 1.6 GHz
- 内存：16 GB LPDDR5-5500，4×32-bit 通道，理论 88 GB/s

## CPU 侧的深度妥协

Van Gogh 的 CPU 在多个维度上与桌面/主流笔记本 Zen 2 拉开差距：

**L3 缓存**：仅 4 MB（单 CCX），而桌面 Zen 2 每 CCX 为 16 MB。在 Linux schedutil governor 下 L3 延迟测试几乎消失（可能是 OS 电源策略问题），切换到 performance 模式后恢复。

**LPDDR5 内存性能**：对 CPU 而言是灾难性的——延迟超过 150 ns（接近服务器 DRAM），带宽仅约 25 GB/s（理论 88 GB/s 的不到 1/3，更接近 2015 年的 DDR4-2133 水准）。这个问题在 Windows 下同样存在，排除了 OS 驱动因素。Chester Lam 推测是内存控制器实现问题。

**时钟爬升**：从冷启动到达最高频率约需 1 秒，而 Renoir 笔记本需 9.35 ms，Piledriver 也能在 100 ms 内完成。这是有意为之的电池寿命策略，代价是显著的响应延迟感。

**单 CCX**：多线程性能相比 Renoir（双 CCX）打折扣，最大 boost clock 也是所有 Zen 2 实现中最保守的之一。

## GPU 侧的设计亮点

RDNA 2 iGPU 是 Van Gogh 真正的用心所在：

**高内存带宽**：LPDDR5 的高带宽（GPU 可实测 >70 GB/s）是 Van Gogh 不需要 Infinity Cache 的根本原因。GPU 的 compute/bandwidth 比接近游戏主机（PS5/Xbox Series X），确保 GPU 在与 CPU 共享内存总线时仍有充足带宽。

**缓存结构**：延续 RDNA 2 的四级架构，但 L2 仅 1 MB（为 WGP 数目而言偏大，设计上有意为 iGPU 场景优化延迟）。与桌面 RDNA 2 锁定同等时钟后，L2 延迟甚至更低——因为客户端数更少。

**架构优势保留**：尽管频率低（1.6 GHz vs 桌面 1.7+ GHz），RDNA 2 的向量延迟、缓存带宽特性对比 Renoir 的 Vega iGPU 仍有明显优势。

## APU 与主机芯片的类比

Van Gogh 与 PS5/Xbox Series X APU 的共同模式：CPU 侧小缓存、保守时钟和高内存延迟；GPU 侧高带宽、优化延迟。这反映了 AMD 在 APU 产品线上面向不同用途的差异化——游戏主机把预算集中在 GPU 而非 CPU 上，是有意识的设计而非妥协。

AMD 在这一市场的竞争优势在于同时拥有 CPU（Zen）和 GPU（RDNA）技术，使其能为 Valve、Sony、Microsoft 提供定制 APU，而 Nvidia 和 Intel 单独都难以复制这一组合。

## 参见

- [[rendering/rdna2-architecture]] — RDNA 2 GPU 架构完整说明
- [[computer-systems/zen2-microarchitecture]] — Zen 2 核心架构
- [[computer-systems/gpu-memory-hierarchy-latency]] — GPU 缓存延迟基准
- [[computer-systems/cpu-clock-frequency-ramp]] — 时钟爬升行为分析

## Sources

- [[sources/chipsandcheese-van-gogh-steam-deck]]
