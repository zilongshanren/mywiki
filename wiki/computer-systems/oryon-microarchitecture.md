---
tags: [cpu, arm, qualcomm, microarchitecture, mobile, laptop]
date: 2026-04-27
sources: 1
---

# Qualcomm Oryon 微架构

Oryon 是高通自研的 CPU 核，搭载于 Snapdragon X Elite（2024 年），是高通自 2017 年 [[qualcomm-kryo-microarchitecture|Kryo]] 之后时隔七年重返自研核的成果。其起源可追溯至 2019 年成立、2021 年被高通收购的初创公司 Nuvia——Nuvia 创始人团队中有苹果前工程师，研发风格深受 Apple [[firestorm 核心]]设计哲学影响。

## 系统架构

Snapdragon X Elite 以三个四核簇的形式组织 12 颗 Oryon 核，每簇共享 12 MB L2 缓存。与 Kryo 类似，高通选择了同质大核方案而非 [[intel-hybrid-alder-lake|混合核]]架构，靠不同簇的最高频率上限区分单线程与多线程性能优先级。

簇内核间延迟约在合理范围，跨簇延迟则显著升高——对一颗单片 SoC 而言略高于预期，不如 [[amd-phoenix-soc|AMD Phoenix]] 同簇内的均一低延迟。另设全芯片共享的 System Level Cache（SLC，6 MB），可服务多个功能模块，但缓存容量偏小，限制了其对 CPU 侧代码的实际贡献。

## 前端

Oryon 的分支预测器是整核最突出的特性之一：

- **方向预测**：单层预测器，表现与 [[golden-cove-microarchitecture|Golden Cove]] 相当，但弱于 Zen 4 在长模式下的准确率。
- **BTB**：将 BTB 与 L1i 绑定，8 KB 以内的代码可获得单周期 taken branch 延迟（类似 AMD 所称"零气泡"分支）；超出则退为 3 周期，最大可覆盖 192 KB L1i 范围。此策略与 [[qualcomm-kryo-microarchitecture|Kryo]] 及苹果 M1 相似，区别于 Zen 4/Intel 的解耦 BTB 方案。
- **间接分支预测器**：2048 项，比 Golden Cove 更大，但小于 Zen 4 的 3072 项，且缺乏 Zen 4 超过 32 个目标后的渐进惩罚机制。
- **返回栈**：深达 48 项，接近苹果 M1 Firestorm 的 50 项，远超 Zen 4 的 32 项。

L1i 容量 192 KB，采用 8 宽解码，指令带宽充裕；代码规模小时表现出色，但一旦超出 L1i 发生缓存缺失，带宽将大幅下降，不及 Zen 4 从 L3 仍可维持高带宽的能力。

## 后端与乱序执行

Oryon 的乱序执行规模在业界属于顶级：

| 结构 | Oryon | Zen 4 | Golden Cove |
|------|-------|-------|-------------|
| ROB | 680 项 | ~320 项 | ~512 项 |
| 整数物理寄存器 | 384+32 项 | — | — |
| 整数 ALU 调度队列 | 120 项 | ~96 项（与 AGU 共享） | 97 项（整数+向量共享） |
| FP/向量调度队列 | 192 项 | — | — |

每个调度队列绑定单一执行端口，避免每周期多路仲裁的面积与功耗开销，这是高通压低调度器成本的设计手法。FP/向量侧有四条 128 位执行管道，与 Firestorm 相近；无 SVE 支持，向量宽度上限 128 位，但在不依赖 AVX2/AVX-512 的场景下，四管道 FMA 吞吐量可与 Zen 4 持平。

Move elimination 实现较 AMD/Intel 弱，不支持 XOR 自归零识别。

## 内存子系统

- **L1D**：96 KB，延迟约 4 周期，比 Zen 4 的 32 KB 大得多；
- **L2**：私有，延迟约 20 周期；
- **SLC**：6 MB 全芯片共享，延迟约 26–29 ns；
- **DRAM**：LPDDR5X，单核可达 80 GB/s 实测带宽；全芯片读带宽超 110 GB/s，显著优于搭载 DDR5 的 Phoenix 和 Meteor Lake。

L1 DTLB 达 224 项（7 路），与 Kryo 的宽大 TLB 传统一脉相承；L2 TLB 超过 8K 项，惟实测存在疑问（约 1536 项处出现延迟突变）。

## 总结

Oryon 是高通融合 Apple Firestorm 理念与自身 Kryo 传统的产物：超宽后端、深返回栈、大 TLB。在本机 ARM64 应用上性能具竞争力，但 x86 二进制翻译惩罚及 Arm 平台生态碎片化仍是其挑战。

## Sources

- [[sources/chipsandcheese-oryon-core]]
- [[sources/chipsandcheese-snapdragon-x2]]
