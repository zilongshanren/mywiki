---
tags: [gpu, amd, rdna, overclocking, bios, navi10]
date: 2026-04-19
sources: 1
---

# RDNA 1 / Navi 10 超频分级实操

Chips and Cheese 2021 年 4 月的 RX 5000 系列超频指南把对 Navi 10（RDNA 1）的压榨分成三层递进，从"打开 Wattman 拉满滑块"到"VBIOS 刷写 + Soft Power Play Table"，记录了每一阶段的性能/功耗实测曲线，以及一个至今仍未被 AMD 澄清的黑箱参数——SOC Maximum Clock。

## 三阶段增量

第一阶段是 Wattman 基础超频。对 RX 5700（非 XT 全开版）而言，手动把 GPU / VRAM / Power 三组滑块拉满即可，单卡 Firestrike 性能 +5%，功耗 +19%。收益远非线性——硅片与架构设计限制在这里直接体现：功率投入的边际收益迅速递减。

第二阶段是 VBIOS 跨型号刷写。RX 5700 可刷同厂同型号 RX 5700 XT 的 BIOS（必须 PCB 相同，否则可能砖），再叠加 Wattman 超频可累计 +14.57% 性能，代价是功耗暴涨 70%（相对原始 stock）、瞬时功率峰值冲到 278 W。

第三阶段是 More Power Tool + Red Bios Editor 修改 VBIOS：放开功率限制上限（+99%）、把 GFX/Memory 最大时钟提到 2150/1000 MHz、手动把 VRAM timing 的 1550 MHz block 复制到更低频的 block（带宽密集场景下改善 1% 低帧与帧时间一致性）。

## SOC Maximum Clock 之谜

作者把 Voltage → Maximum Voltage SOC 拉到 1200 mV 匹配 core 后，将 SOC Maximum (MHz) 拉到 1350——当时以为是在调 memory controller 到 L2 fabric 的时钟，但实测内存延迟数据与这一假设不符：拉高 SOC 时钟反而让某些场景下功耗下降、Firestrike 小幅提升。作者承认"不知道这个参数到底控制什么"，并呼吁 AMD 澄清。进一步把 SOC 拉到 1500 MHz 拿到了当时据其所知最高的风冷 5700 Timespy 成绩。

这种"用户空间可调但文档不详"的参数在消费级 GPU 超频社区很常见，也是 [[gpu-driver-support-lifecycle]] 讨论驱动废弃时被用户点名的价值所在——老卡能被压榨的空间比官方规格更大。

## 方法论启示

RDNA 1 作为 AMD 从 [[gcn-wave-occupancy|GCN]] 向 RDNA 过渡的第一代，功耗/频率曲线本身就留有余量，尤其是低 bin 的非 XT 版本，其硅片常因 yield（shader/logic 损伤）而非时钟瓶颈被降级——拉回满频反而能跑。这一现象与 [[samsung-8n-vs-tsmc-n7]] 讨论的"node 不是一切，架构 + 物理设计 + bin 才是"互为印证。

## Sources

- [[sources/chipsandcheese-rdna1-redux]]
