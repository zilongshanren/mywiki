---
tags: [cpu, 微架构, arm, neoverse, ampere-altra, cortex-a76]
date: 2026-04-19
sources: 1
---

# ARM Neoverse N1 微架构实测

Neoverse N1 是 ARM 2019 年发布、基于 Cortex-A76 血统的服务器核，Ampere Altra 是其最知名的商用落地。与同代 [[zen2-microarchitecture|Zen 2]] 都用 TSMC 7nm，但实现目标差距明显：Zen 2 要同时覆盖笔记本、桌面、服务器、超算，更深、更宽、频率更高；N1 更像"从手机核加大做服务器"。Chester Lam 用四核 Altra 实例对比 3950X（关闭 SMT、4 核），得到如下结论。

## 整体印象

- **非向量整数负载**（7z 压缩、GCC 编译 Gem5）：N1 与 Zen 2 同频相差 <20%，编译场景 N1 甚至领先 Zen 2 同频 1%，算代次相当。
- **向量/FP 重负载**（libx264、libx265、Blender、libaom-av1）：Zen 2 以 40%–数量级不等领先。这不完全是核的锅——AVX2 宽度是 NEON 两倍，且 x86 侧有成熟的手写汇编。
- **公钥加密**（OpenSSL RSA2048）：N1 惨败，3 GHz 下 Zen 2 快 4 倍。三条 ALU 管道却跑不过两条 ALU 的 FX-8350，属于架构硬伤，作者认为 ARM 需补。

## 分支预测器

N1 走了与 Zen 2 相反的权衡：**速度优先于精度**。

- **L1 BTB 快**：Cortex-A76 为 web workload 做过专门优化，taken branch 带宽高，L2 BTB 与 decoder 计算地址惩罚都小。
- **精度一般**：在 Blender / 7z / 编译里命中率都明显落后 Zen 2 与 Skylake，与 Piledriver 在一个档位之上不多。

在模式识别 microbench（随机 0/1 数组）中 N1 从 512 条目开始劣化，2048 后显著下跌；Zen 2 的 pattern recognition 最强，是它精度领先的主因。见 [[branch-predictor-design]]。

## 后端规模

通过寄存器文件 microbench 推断：N1 有 88 条整数 renaming 寄存器、96 条 FP/SIMD。考虑 ARMv8 架构暴露的 32 + 32 逻辑寄存器，物理文件估算是 120 INT、128 FP/SIMD。

## 功耗与能效

ARM 官方给 N1 在 2.6–3.1 GHz 下每核 1–1.8 W。Ampere Altra 实例跑在 3 GHz，估 1.8 W 上下。Zen 2 3 GHz 每核功耗比 N1 高 48%–98%，取决于是否触发 AVX2。同频 Zen 2 的性能优势通常小于这一功耗差，因此**只要不算 libx265 这类 ISA 生态惨败的场景，N1 在能效上更优**——前提是 ARM 给的数字靠谱。

这条判断呼应 [[isa-implementation-not-architecture|ISA 无关论]]：N1 的低功耗不是 ARM ISA 赏的，是 ARM 的 design team 面向特定市场优化的结果。

## 软件生态是实际瓶颈

N1 的真实性能天花板往往是软件生态。libaom-av1 在 aarch64 上没手写汇编，Altra 几天都跑不完 Zen 2 一小时可做的事。libx265 的 NEON 加速到 2020 初才补齐。对只想跑特定负载的云厂商 N1 可用，但要进 PC 市场生态补齐是硬工。

## 参见
- [[zen2-microarchitecture]]
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]
- [[op-cache-decoded-uop-cache]]
- [[cache-size-vs-latency-tradeoff]] — Altra L3 延迟是 Zen 2 两倍，是作者否定 IOD L4 的依据
- [[gracemont-microarchitecture]] — Intel 押 hyperscale server 的答卷，直接对标 N1
- [[tremont-microarchitecture]] — 类似保守的 store forwarding 取舍

## Sources
- [[sources/chipsandcheese-neoverse-n1-vs-zen2]]
- [[sources/chipsandcheese-neoverse-n1-deep-dive]]
