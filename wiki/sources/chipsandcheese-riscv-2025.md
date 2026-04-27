---
tags: [source, computer-systems, risc-v, sifive, p550, c910, benchmark, out-of-order, ecosystem]
date: 2026-04-27
sources: 1
---

# A RISC-V Progress Check: Benchmarking P550 and C910（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 1 月的横向评测文章，以 SPEC CPU2017、7-Zip、SHA256 和 x264 等工作负载，对 SiFive P550 与玄铁 C910 进行系统性对比，并与 Arm Cortex A73、Intel Goldmont Plus 及 Cortex A55 基准。

## 摘要

两款乱序 RISC-V 核心在所有测试中均落后于 A73 和 Goldmont Plus——低时钟频率是核心原因（P550 仅 1.4 GHz，C910 仅 1.85 GHz），但这并不能完全解释差距，因为 C910 即便频率更高也常被 P550 持平甚至落后。更令人担忧的是，供给完善的 Cortex A55（更高频+更低内存延迟）在多项 SPEC 整数子测中能与两者比肩。x264 编码测试暴露了生态问题：libx264 没有任何 RISC-V 向量汇编路径，导致两核均只能跑纯 C 代码，性能灾难性地落后于 A73 甚至 A55。P550 在平衡性上优于 C910——调度器容量合理、IPC 利用率较高。C910 拥有更高频率和更大 ROB，但内存子系统极弱导致乱序窗口常难填满。文章总结：RISC-V 硬件层面仍与主流有明显差距，软件生态碎片化则是更长期的挑战。

## 关键要点

- SPEC CPU2017 整数/浮点：P550 ≈ C910，均明显弱于 A73（更高频）和 Goldmont Plus
- Cortex A55（更高频+低延迟 DRAM 配置）在多个整数测试中追平 P550 和 C910
- x264 编码：无 RISC-V 向量汇编，指令数爆炸，P550 和 C910 均遭灾难性性能损失
- P550 的乱序平衡性优于 C910——部分测试 P550 IPC 接近 3 的核心宽度上限
- C910 在 SHA256 等纯计算任务中接近 2 IPC，但整体整数性能仍输给 P550
- RISC-V ISA 碎片化（扩展版本差异）导致发行版二进制以最低公分母为目标编译，缺乏优化
- 软件生态建设需要先有足够强的硬件吸引开发者，而后者目前仍有差距

## 链接到的概念

- [[computer-systems/sifive-p550-microarchitecture]]
- [[computer-systems/xuantie-c910-microarchitecture]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/a-risc-v-progress-check-benchmarking
- 本地：`raw/articles/chipsandcheese.com/2025-01-30_a-risc-v-progress-check-benchmarking-p550-and-c910.md`
