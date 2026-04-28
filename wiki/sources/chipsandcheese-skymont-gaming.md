---
tags: [source, cpu, intel, skymont, e-core, 游戏负载, arrow-lake, 微架构]
date: 2026-04-27
sources: 1
---

# Skymont in Gaming Workloads（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 8 月的文章，以 Intel Core Ultra 9 285K（Arrow Lake）的 16 颗 Skymont E-Core 为测试对象，在 Palworld、COD Cold War 和 Cyberpunk 2077 上进行 top-down 分析，探究密度优化核心在低 IPC 游戏负载下的瓶颈特征。

## 摘要

Skymont 在游戏中以**后端内存延迟**为主要瓶颈，与同平台 Lion Cove P-Core 相似。这并不意外，因为两类核心共享 L2 之后的内存子系统，而 Arrow Lake 平台 L3 延迟偏高（约 14 ns）。Skymont 因分布式调度器效率低于 Zen 5 的统一调度器，ROB 较少填满；在分配层面也存在一定分配限制（allocation restrictions）。另一值得关注的现象是，部分后端停顿源于 PAUSE 指令引发的序列化（scoreboard stall），暗示游戏使用了自旋锁。文章以 Cyberpunk 2077 的主观可玩性测试证明 Skymont 在游戏中能提供流畅体验，但强调这只是"密度核的能力下限"，而非对 P-Core 的替代。

## 关键要点

- Skymont 游戏瓶颈：后端内存延迟 > 前端（与 Lion Cove 一致，均受 Arrow Lake 平台高 L3 延迟影响）
- 分布式调度器效率低于 Zen 5 统一调度器；微基准测试两者总调度器条目相近，但 Zen 5 更少出现调度器耗尽
- 416 条目 ROB 通常未填满，资源停顿先于 ROB 饱和
- 分配限制（allocation restrictions）存在，可能源于 8-wide rename 向同一调度器发送过多指令
- 序列化停顿（IQ_JEU_SCB / NON_C01_MS_SCB）：LFENCE/MFENCE 和 PAUSE 是主要触发源，后者与游戏自旋锁有关
- Skymont 4 MB L2 在高 L3 延迟环境下至关重要：L2-bound cycles 极少，L3-bound cycles 中等，DRAM-bound 最重
- 与 Crestmont 对比（Meteor Lake 笔记本）：Crestmont 256 条目 ROB 更常填满；调度器停顿分布差异明显
- 主观测试：将 285K affinity 固定至 16 E-Core，多款游戏均可流畅运行

## 链接到的概念

- [[computer-systems/skymont-microarchitecture]]
- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/crestmont-microarchitecture]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/skymont-in-gaming-workloads
- 本地：`raw/articles/chipsandcheese.com/2025-08-20_skymont-in-gaming-workloads.md`
