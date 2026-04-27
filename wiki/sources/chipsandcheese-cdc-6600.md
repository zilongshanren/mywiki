---
tags: [source, computer-systems, cpu, history, hpc, cdc-6600, seymour-cray]
date: 2026-04-27
sources: 1
---

# Inside Control Data Corporation's CDC 6600（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 4 月（愚人节）的文章，以"现代评测"视角解析 1964 年 Seymour Cray 设计的 CDC 6600 大型机，寓幽默于严肃的微架构分析之中。

## 摘要

文章以一本正经的 Chips and Cheese 风格逐节剖析 CDC 6600 的微架构：60 位标量顺序执行流水线、无分支预测、8 字节指令队列（兼作循环缓冲）、10 个非流水化并行功能单元（scoreboard 调度）、基于 Reference Address + Field Length 的分段内存保护（无虚拟内存与分页）以及多 bank 核心存储器（Core Memory）。文章结尾揭示其反讽意图：这台 1964 年的机器运行在 10 MHz，正是今天那些"乱序大机器"无法存在的铁证——当然，这恰恰证明 Cray 的设计哲学影响深远。通过反向对比，文章展示了现代 CPU 中分支预测、乱序执行、缓存层次等机制的价值所在。

## 关键要点

- CDC 6600 核心处理器：60 位、顺序执行、10 MHz，无分支预测，无缓存（直连 Core Memory）
- 10 个独立非流水化功能单元（整数加减各1、移位1、布尔逻辑1、增量×2、FP 加法1、FP 乘法×2、除法1），理论上可并行运行
- Scoreboard 机制追踪寄存器依赖，处理 RAW 与 WAR 冒险（无寄存器重命名）
- 24 个寄存器：8 个 60 位操作数（X0-X7）、8 个 18 位地址（A0-A7）、8 个 18 位增量（B0-B7）
- 分段内存保护：RA（基地址）+ FL（长度），越界即停机，无精确异常
- Core Memory 32 bank，峰值 75 MB/s，bank 冲突检测用超时而非地址比较
- Extended Core Storage 最大 14 MB，行宽 488 位，运行在 312.5 KHz
- 文章反讽：1964 年的设计原则（简单 ISA 直接执行、无投机、无缓存）正是"Spectre 免疫"的来源

## 链接到的概念

- [[computer-systems/cdc-6600-architecture]]
- [[computer-systems/scoreboard-scheduling]]
- [[computer-systems/isa-implementation-not-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-control-data-corporations-cdc-6600
- 本地：`raw/articles/chipsandcheese.com/2024-04-01_inside-control-data-corporations-cdc-6600.md`
