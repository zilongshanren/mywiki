---
tags: [内存, 分配器, 性能]
date: 2026-04-14
sources: 1
---

# 线性分配器（Linear Allocator）

**最简单的一种内存分配器**：一块连续缓冲 + 一个偏移指针。每次分配只做 `ptr += size`，释放则整体 reset。O(1) 分配、几乎零开销，非常适合**生命周期一致、使用周期短**的内存——典型场景是一帧内的临时数据。

## 结构

- 一段预分配的内存页（page），记录 `base`、`offset`、`pageSize`
- `Allocate(size, alignment)`：把 offset 对齐后取出一段，向前推进
- 单页满了就挂一个新页到 page pool
- `Reset()`：所有 offset 回到 0，整批释放——**不支持单个 free**

## 碎片

- **内部碎片**：对齐把请求 padding 上去。典型例子是只存一个 4×4 矩阵的 constant buffer，请求 64B 但 D3D12 要求 256B 对齐，浪费 192B
- **外部碎片**：连续两次分配对齐不同时，中间留下的空洞

碎片是代价，换来的是**单调推进指针**的速度——写入一个原子变量就完事，不存在自由链表、合并、搜索。

## 为什么游戏引擎爱用

- **每帧的动态数据**天然满足"分配一批，一次回收"：粒子、UI 顶点、动态常量、立即模式 debug 绘制
- [[d3d12-resource-binding|D3D12 的 UploadBuffer]] 就是典型的线性分配器，用一段 upload heap 存每帧上传给 GPU 的数据
- 命令缓冲（command buffer）的存储本身也常用线性分配
- 可和 [[cache-friendliness|缓存友好]] 策略协同：顺序分配意味着顺序读取

## 变种

- **Stack allocator**：额外记录一个"标记"，允许 pop 到某个 checkpoint
- **Double-buffered / ring**：两段交替 reset，让当前帧使用 buffer A 时上一帧的 buffer B 在 GPU 上执行
- **Frame allocator**：多个命令列表各持一个独立的线性分配器，避免线程争用
- **双端分配器（double-ended allocator）**：同一块内存从两端向中间推进，两端的 offset 分别维护。云风在 2002 年前后为大话西游客户端在 64M 内存上写过这类分配器，并可和栈式分配器协同工作——例如一端用栈式跨帧保留资源，另一端用线性分配放当帧临时缓冲。参见 [[sources/cloudwu-game-engine-memory]]。

## 相关
- [[d3d12-resource-binding]]
- [[cache-friendliness]]
- [[virtual-memory]]
- [[render-graph]]
- [[gpu-fence-timeline-semaphore]] —— 线性分配器帧循环回收的前置条件
- [[buffer-renaming]] —— 现代 API 用线性分配器取代驱动隐式 renaming
- [[cheat-by-solving-less]] —— Ben Supnik 把 bump allocator 作为「解一个更小问题」的标本
- [[bump-allocator-wasm-guest]] — Wasm guest 端的 bump 分配器模式
- [[hash-trie-intrusive]] — 配合 arena 使用的无 resize 哈希结构
- [[msi-hash-table]] — 同样配合 arena 使用的扁平索引表
- [[segment-array]] — 与 arena 配合最好的增长容器，追加不搬迁、不留洞

## Sources

- [[sources/3dgep-learning-directx12-lesson3]]
- [[sources/cloudwu-game-engine-memory]]
