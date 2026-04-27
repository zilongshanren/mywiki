---
tags: [source, computer-systems, loongson, china, cpu, microarchitecture, risc-cisc, domestic-chip]
date: 2026-04-27
sources: 1
---

# Can China's Loongson Catch Western Designs? Probably Not.（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 4 月的文章，通过梳理龙芯二十余年的研发历史，评估其追赶英特尔/AMD 的可能性，结论偏悲观。

## 摘要

文章从 2003 年的 Godson-2（130 nm，4-wide OoO，434 MHz）一路梳理到 2024 年的 3A6000（LA664，SMIC 12 nm，2.5 GHz），对龙芯每代架构与同期 AMD/Intel 竞品进行横向比较。核心发现：龙芯历代设计在每周期性能（IPC）方面均保持合理水准，但始终无法突破时钟频率瓶颈——Godson-2E 于 2006 年达到 1 GHz，而同期 Intel Core 2 可运行在 2 GHz 以上。到 2024 年，3A6000 的 2.5 GHz 仍无法与 AMD Zen 4（5 GHz+）抗衡。此外，龙芯还面临软件生态分裂（两套不兼容 Linux 发行版）、核心数量落后（2024 年仍是四核）、内存带宽长期不足、以及完全依赖国产工艺节点（SMIC）的制约——后者意味着无法享受台积电等先进工艺。文章指出，苹果靠极高 IPC 与宽核弥补频率不足，但龙芯两方面均无法达到同等水平。

## 关键要点

- Godson-2（2003）：4-wide OoO，434 MHz，SMIC 180 nm；K8 同期达 2.2 GHz
- Godson-2E（2006）：1 GHz，90 nm，引入片上 L2 与内存控制器；内存带宽仅约 1 GB/s
- Godson-3B1500（2013）：8 核，32/28 nm，1.5 GHz；Haswell 同期 3.5 GHz+
- GS464E（~2015）：IPC 大幅提升，但在 40 nm 国产节点上频率反而退步
- LA464（3A5000，SMIC 12 nm）：2.5 GHz，与 [[loongson-3a5000-microarchitecture]] 呼应
- 软件生态：LBrowser v3（Chromium）Speedometer 3.0 得分仅为 AMD 3950X 的 1/4.8
- 制造瓶颈：全依赖 SMIC，无法使用 TSMC 先进节点，而 AMD Zen 4 用 TSMC 5 nm
- 龙芯的真正短板是时钟频率，而非 IPC；IPC 历代均尚可，但频率从未追上

## 链接到的概念

- [[computer-systems/loongson-3a5000-microarchitecture]]
- [[computer-systems/loongson-historical-trajectory]]
- [[computer-systems/isa-implementation-not-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/can-chinas-loongson-catch-western-designs-probably-not
- 本地：`raw/articles/chipsandcheese.com/2024-04-29_can-chinas-loongson-catch-western-designs-probably-not.md`
