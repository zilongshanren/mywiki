---
tags: [cpu, 微架构, 后端, 调度器, nsq, amd, intel]
date: 2026-04-19
sources: 3
---

# 非调度队列（NSQ）：给调度器加个候补席

[[cpu-scheduler-design|调度器]]（也叫 reservation station）每周期要对所有条目做 wake-up/ready-check：某指令的所有操作数到齐了没，好挑一条放上执行端口。这个全连接的 wake-up 矩阵面积与功耗都随条目数非线性膨胀，是 CPU 后端里最贵的结构之一。**非调度队列（non-scheduling queue, NSQ）**是个省成本的手段：在调度器前放一道更便宜的 FIFO 队列，只做"排队等位"，**不参与每周期 wake-up 检查**。

## 三个出处

- **AMD Zen 2 FP 侧**：36 项 FP scheduler + **64 项 NSQ**，让 FPU 侧总容量达到 100。见 [[zen2-microarchitecture]]。
- **Intel Tremont**：调度器只有 24 项，但塞了 33 项 NSQ，整条 FP 流水可容 57 条 uop 在等——和 Skylake 的 FP scheduler 容量打平。
- **Intel Gracemont**：三口 FP 队列 + NSQ 共计 91 项 FP/vec 容量（256-bit 指令吃两槽），逼近大核水平；memory 侧 NSQ 让 backend 可有 84 条 memory op 等 AGU 而不 stall rename。

## 为什么有用

关键权衡：**"我能看见多少条未发射指令"** vs **"每周期我能挑多少条就绪的"**。真正 wake-up 只需要看调度器里最前面那几条；已经排在 NSQ 里的远处指令反正还轮不到它们就绪，每周期扫它们纯属浪费电。只要 rename 阶段不被后端挤塞反压（这是 NSQ 的主要目的），NSQ 就成功了。

## 探测方法

Chester Lam 发明了专门的探测方法：跟 Henry Wong 的"调度器大小"标准做法不同，他**固定 NOP 数量、改变依赖关系**——让一部分指令依赖长延迟的 pointer chasing load。如果只有部分指令阻塞在调度器里，另一部分未依赖者仍能发射，就能把真正的 scheduler size 剥出来，把 NSQ 的贡献分开。Gracemont 表面看有 91 项 FP scheduler，用此法分离出真实 scheduler 小得多 + 大 NSQ。

## 代价

NSQ 的代价是**就绪检查延迟**：某条指令其实已经就绪了但还没被送进调度器，会多等几个周期才真正发射。对吞吐友好、对单指令延迟不友好。作为低功耗核的标配、作为高性能核的补丁都说得通。

## 参见

- [[cpu-scheduler-design]]
- [[zen2-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[tremont-microarchitecture]]
- [[dispatch-stall-breakdown]]

## Sources

- [[sources/chipsandcheese-tremont]]
- [[sources/chipsandcheese-gracemont]]
- [[sources/chipsandcheese-zen2-cinebench-analysis]]
