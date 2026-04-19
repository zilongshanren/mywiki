---
tags: [source, 计算机体系结构, cpu, intel, 调试, oodle]
date: 2026-04-19
sources: 1
---

# Oodle 2.9.14 and Intel 13th/14th gen CPUs（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2025 年 5 月的文章，讲 Oodle Data 在 Intel 13 / 14 代桌面 CPU 上遇到的间歇性解压失败——从两年的 debug 黑箱到找到 smoking gun，再到出一个 work-around。

## 摘要

2023 年春 Fortnite 开始在 Intel 13 代 CPU 上大量报 Oodle shader 解压错误。一路排查走了很多弯路（坏声卡驱动、主板厂 BIOS 乱配、SIMD 代码怀疑），到 2024 年 Intel 终于确认是**时钟树电路物理退化**造成的硬件 bug。Oodle 侧一直没有可稳定复现的 case，直到 2025 年春一个客户提供了"同一数据重试常常成功"的 repro。深度 debug 发现：(1) 从不发生 bitstream desync——bit reader 永远跑完；(2) 错位永远**单字节**、间隔 7-10K 字节；(3) 错值永远在 1-11 之间——正好是 Oodle Huffman 码长字段。推论：`mov [rDest], ch`（存寄存器高字节）偶尔退化成 `mov [rDest], cl`（存低字节），因为 x86-64 byte-high register store 的控制信号 mux 在高频 / 超频下 timing slack 不足。Work-around：显式 `shr ecx, 8` 再 `mov [rDest], cl`，躲开 byte-high 存储——成本 0.5% 吞吐损失。Oodle 2.9.14 ship 该 work-around。

## 关键要点

- **症状的统计模式**（值域 1-11、单字节间隔 7-10K）是硬件 bug 的强信号，比 perf counter 有用。
- **"第二次解压同数据常成功"** 排除 ECC / memory stomp / disk corruption——是 CPU 运行时 flake。
- **byte-high register mov**（`mov [mem], ch`）是 x86-64 少见特性；Intel 13/14 代下它的 mux 控制信号偶尔超时，退化成 low-byte 存储。
- Work-around **只是缓解**，不是修复；受影响机器的硬件已物理损坏需要换。
- `gcc` / `clang` 会生成相同 byte-high 指令——不是 ASM 手写的错。
- 历史教训：**没有 reliable repro 时 debug 两年**，真正突破来自客户的"同数据重试成功"观察。

## 链接到的概念

- [[intel-13th-14th-gen-clock-degradation]]
- [[oodle-compression-suite]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2025/05/21/oodle-2-9-14-and-intel-13th-14th-gen-cpus/
- 本地：`raw/articles/fgiesen.wordpress.com/2025-05-21_oodle-2-9-14-and-intel-13th-14th-gen-cpus.md`
