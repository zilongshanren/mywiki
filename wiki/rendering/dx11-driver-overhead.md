---
tags: [rendering, graphics-api, dx11, driver, performance, cpu-overhead]
date: 2026-04-27
sources: 1
---

# DX11 驱动开销的结构性根因

DX11 的"驱动开销"是 2012–2015 年间 PC 游戏优化的核心话题。理解它的根因对评估后续低层 API（[[mantle-api|Mantle]]、[[graphics-api-history|DX12/Vulkan]]）的价值不可或缺。

## 三个核心问题

[[angelo-pesce]] 在 2013 年的分析将 DX11 驱动开销归结为三类结构性缺陷：

### 1. 延迟状态翻译

GPU 硬件并没有一个与 DX11 API 完全对应的"状态寄存器组"。驱动必须收集从上次 draw 以来所有 `IASetVertexBuffers`、`RSSetState`、`VSSetShader` 等调用，在 draw call 触发时统一翻译成 GPU 可执行的命令字节流。这意味着每个 draw call 都有一次不可避免的"状态快照 + 翻译"开销，无法提前并行化。

### 2. 资源生命周期管理

DX API 的语义允许应用随时用 `Map(DISCARD)`/`UpdateSubresource` 更新 buffer，但 GPU 可能还在引用旧版本。驱动必须：保留旧 buffer 直到 GPU 完成、分配新内存、记录 refcount——这产生了大量隐式分配和跨帧的生命周期追踪。

### 3. Deferred context 的空洞问题

DX11 允许动态 buffer 跨 immediate context 和 deferred context 可见。这意味着 deferred context 录制的命令流中，更新操作的最终顺序取决于 context 被 `ExecuteCommandList` 调用的时序。驱动要么不真正生成 GPU 命令缓冲（退化为"命令列表 replay"），要么留空洞等待晚到的 immediate context 操作。两种选择都限制了多线程效益。

## 程度评估

Pesce 强调：这些问题把 DX11 变成"不如它本可以做到的"，但不是"完全不可用"。他认为有些开销本可以通过"API 内的 API"——即与 GPU 厂商协商某个不触发昂贵路径的"快速通道"调用序列——规避，但这需要双方的持续投入，商业上没人愿意为之买单。

## 影响

正是这三点构成了 [[mantle-api|Mantle]]、D3D12 和 Vulkan 的设计对立面：显式状态对象（Pipeline State Object）、显式内存管理、显式命令缓冲录制与提交。

## 相关

- [[mantle-api]]
- [[graphics-api-history]]
- [[low-level-gpu-api]]
- [[buffer-renaming]]

## Sources

- [[sources/c0de517e-on-mantle]]
