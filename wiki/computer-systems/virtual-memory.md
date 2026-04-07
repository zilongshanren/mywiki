---
tags: [计算机系统, csapp]
date: 2026-04-05
sources: 1
---

# 虚拟内存（Virtual Memory）

**每个进程都拥有独立的连续地址空间**——是最重要的 OS 抽象之一。

## 核心幻觉

每个进程"以为"自己拥有 64-bit 的连续地址空间（实际物理内存可能远小于此，且由多进程共享）。

## 底层机制

- **页表（Page Table）**：把虚拟地址映射到物理地址。
- **TLB（Translation Lookaside Buffer）**：页表项的 cache，加速地址转换。
- **Page Fault**：访问未映射页时触发，OS 从磁盘换入。
- **Memory-Mapped I/O**：把文件映射成内存区域，透明访问。

## 为什么存在

- **隔离**：进程不能互相访问对方内存。
- **安全**：操作系统内存保护。
- **简化编程模型**：每个进程看到的是连续地址空间。
- **支持超过物理内存的程序**：Page Swap 让你能用更大的虚拟空间。

## 游戏开发的实际影响

- **内存映射文件**（mmap）：加载大资源文件时不全读入 RAM。
- **Shared Memory**：进程间通信（多进程编辑器）。
- **崩溃诊断**：`0x00000000` 访问是 null pointer；`0xCCCCCCCC` 是未初始化栈；`0xDEADBEEF` 是 debug sentinel——地址值暗含状态。

## 相关

- [[memory-hierarchy]]
- [[compilation-pipeline]]

## Sources

- [[sources/csapp-day01]]
