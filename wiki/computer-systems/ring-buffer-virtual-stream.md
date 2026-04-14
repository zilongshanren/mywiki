---
tags: [环形缓冲区, 并发, spsc, 不变量, io]
date: 2026-04-14
sources: 1
---

# 环形缓冲区：数组索引 vs 虚拟流

单生产者单消费者（SPSC）环形缓冲区是硬件 / 驱动 / 音频 / 异步 IO 层最常见的一种有界 FIFO。数据结构本身极简：

```c
struct FIFO {
  ElemType Elem[SIZE];
  uint ReadPos;
  uint WritePos;
};
```

真正值得推敲的是 `ReadPos` / `WritePos` 两个位置指针**到底表示什么**。[[fabian-giesen|ryg]] 把常见的两种语义叫做「数组索引」和「虚拟流」，并论证后者在几乎所有用软件维护的 FIFO 里都更清爽。

## 模型 1：数组索引（mod SIZE）

`ReadPos`、`WritePos` 就是 `[0, SIZE)` 范围内的下标。写入是

```c
Elem[WritePos] = x;
WritePos = (WritePos + 1) % SIZE;
```

`ReadPos == WritePos` 被定义为「空」。这种模型直接映射到硬件寄存器（`DMA_RPTR` / `DMA_WPTR`）。它有一个让人抓狂的**满 / 空二义性**：`ReadPos == WritePos` 既像空、也可能是缓冲区刚好被填满了一整圈。ryg 给的解法不是玩花活儿，而是**就别让这种事发生**——当元素数达到 `SIZE - 1` 时阻塞生产者。为空、满写不同的特殊编码会让 lock-free 实现变得异常难写，而硬件对话场景下本来就**没有锁可用**。

## 模型 2：虚拟流（延迟取模）

把 `ReadPos` / `WritePos` 解释成「从开始到现在共走过多少元素」——也就是一个单调递增的虚拟流位置，访问数据时才做 `Elem[WritePos % SIZE]`。当 `SIZE` 是 2 的幂时，`%` 只是一次掩码，而且整数溢出能**自动**做对的事：`WritePos - ReadPos` 用 unsigned 减法得到的就是当前队列里的元素数，不需要分支，不管是否有一方 wrap 过。缓冲区满的条件变成非常直观的 `WritePos == ReadPos + SIZE`。

## 虚拟流是一种表达力

这个模型最大的好处不是省几条指令，而是**让不变量变简单**：

- 如果你在从磁盘做顺序流式读取，`WritePos` 可以直接当文件偏移用。异步读的那条请求参数、环形缓冲区的当前写入位置、「已读到哪」——全部都是同一个变量，没有冗余也不会对不上。再把缓冲区的目标地址按异步 IO 对齐要求对齐，由于低位自然匹配，可以**直接 DMA 到缓冲区**，一次 copy 都不需要。
- **音频播放场景**更典型：硬件是个不停往前走的消费者，只要你供得慢，它就越界继续消费、还得告诉你「跑远了多少 ms」以便对音画同步做补偿。虚拟流模型里这个问题是零开销的——只要把 read 指针加进去就行。而几乎所有的音频 API 都只暴露 mod-SIZE 的 read 位置，逼上层去拉一个墙钟来回估算「是不是绕了一圈」，ryg 吐槽这完全是 API 设计问题：驱动自己因为每播完一个 block 都会收到中断，其实**知道准确的累积位置**，只是故意不告诉你。
- **PowerPC 上的额外福利**：当 `SIZE` 和 `sizeof(ElemType)` 都是 2 的幂时，`Elem[WritePos % SIZE]` 的地址生成可以被一条 `rlwinm` 指令合并完成，甚至比「先加 1 再取模」更轻。

## 溢出 vs 2 的幂

虚拟流模型在 32 位 / 64 位指针上会绕回来——但这不影响正确性。只要你**所有的比较都通过 `WritePos - ReadPos` 的无符号差值**来做，且 `SIZE` 是 2 的幂且不超过指针类型可表示范围的一半，wrap-around 就是透明的。评论区的讨论把这一点解释得很透：把 `WritePos >= ReadPos` 写成 `(signed)(WritePos - ReadPos) >= 0` 即可。

## 一般性结论

ryg 把这条经验归纳成一句话：**如果环形缓冲区是唯一的通讯通道**，那就用虚拟流；**如果你有独立的反馈通道**（比如中断、回调），可以用数组索引。前者是把「还剩几条信息在缓冲区里」这个关键量直接编进指针的代数里，后者是把它外包给外部状态——如果外部状态本身不可靠，FIFO 本身也就不可靠。

## 和其他话题的连线

- [[cache-friendliness]]：软件版的 FIFO 通常把 `ReadPos` 和 `WritePos` 放在不同的 cache line 上以避免 false sharing。
- [[data-structure-invariants]]：和链表 sentinel 同样思路——让数据结构的状态空间没有空洞，特判自然消失。
- [[gpu-fence-timeline-semaphore]]：GPU timeline semaphore 用的就是虚拟流模型（单调 64 位计数器），和这里的论证完全重合。

## 相关

- [[fabian-giesen]]
- [[data-structure-invariants]]
- [[cache-friendliness]]
- [[gpu-fence-timeline-semaphore]]
- [[memory-hierarchy]]

## Sources

- [[sources/ryg-ring-buffers-and-queues]]
