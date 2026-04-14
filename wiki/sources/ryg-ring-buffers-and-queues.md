---
tags: [source, 数据结构, 并发, io, 音频]
date: 2026-04-14
sources: 1
---

# Ring buffers and queues（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 12 月的一篇关于单生产者单消费者环形 FIFO 的笔记。把 `ReadPos` / `WritePos` 的两种常见语义（纯数组索引 vs 虚拟流位置）放在一起比较，并论证**虚拟流模型几乎总是更好**。

## 摘要

SPSC 环形缓冲区最核心的选择是 `ReadPos` / `WritePos` 到底指什么。模型 1 是 `[0, SIZE)` 的数组索引——和硬件 DMA 寄存器直接对齐，但会遇到「满 / 空二义性」。ryg 对此的建议是**不要聪明**——当 `count == SIZE - 1` 时就阻塞生产者，把问题消灭掉；任何 clever encoding 都会让 lock-free 实现坍塌。模型 2 是虚拟流：`ReadPos` / `WritePos` 是「从开始到现在一共走了多少元素」的单调计数器，访问时再做 `Elem[Pos & (SIZE-1)]`。好处是元素数就是 `WritePos - ReadPos`，无符号减法天然处理 wrap-around；满条件也直接对应 `WritePos - ReadPos == SIZE`。虚拟流最大的胜利是**不变量变短了**：流式文件读 → `WritePos` 直接就是文件偏移，不需要单独保存；音频播放 → 驱动知道的是累积位置，但几乎所有 API 只暴露 mod-SIZE 的 read 位置，逼上层用墙钟估算有没有绕过一圈——完全是 API 设计问题。2 的幂 + PPC 上 `rlwinm` 一条指令就能合并地址生成，甚至比模型 1 更便宜。评论区反复纠结于「`WritePos` 会不会溢出」：只要 `SIZE` 是 2 的幂、所有比较都通过 `WritePos - ReadPos` 的无符号差值，溢出就是透明的。

## 关键要点

- 数组索引模型的「满 vs 空」二义性用阻塞生产者解决，不要特殊编码。
- 虚拟流模型下 `WritePos - ReadPos` 给出元素数，无符号减法自动处理 wrap-around。
- 2 的幂尺寸让虚拟流「零成本」——`%` 退化为 `& (SIZE-1)`。
- 流式 IO 场景里 `WritePos` 可以直接当文件偏移用，DMA 目的地址对齐后可做零拷贝。
- 大多数音频 API 只暴露 mod-SIZE 位置而不是累积位置，逼上层用墙钟估算绕圈次数——是 API 设计失误而非必然。
- 一般原则：有独立反馈通道用数组索引也行；若 FIFO 是唯一通道，虚拟流更有表达力。

## 链接到的概念

- [[ring-buffer-virtual-stream]]
- [[fabian-giesen]]
- [[data-structure-invariants]]
- [[cache-friendliness]]
- [[gpu-fence-timeline-semaphore]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/12/14/ring-buffers-and-queues/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-12-14_ring-buffers-and-queues.md`
