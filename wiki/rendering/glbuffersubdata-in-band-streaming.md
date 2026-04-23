---
tags: [渲染, opengl, 驱动, ubo, 流式, 命令缓冲]
date: 2026-04-19
sources: 1
---

# glBufferSubData 的 in-band 流式更新

在 2015 年的桌面 GL 驱动（NVIDIA / AMD DX11-capable / Intel）上，全量替换或完整子区间覆盖一个 VBO/UBO 时，`glBufferSubData` 不再是当年那个"串行化陷阱"——它被广泛实现为 **in-band update**，与 `glMapBuffer` 配合得当甚至更快。[[ben-supnik|Supnik]] 2015 年这篇更正前作，重点讲述了这条 fast path 为什么在**多线程驱动架构**下成立。

## "in-band" 的两种实现形态

驱动有两种对等的实现都算 in-band：

1. **DMA in command stream**：把数据连同一条 DMA 命令塞进 FIFO，GPU 命令处理器到时候按顺序取出，直接灌进目标 VBO 的真实显存地址。
2. **资源 renaming**（[[buffer-renaming]]）：每次 SubData 等价于"分配一块新的同大小存储 + 把老存储挂给正在消费它的 draw"。对 app 仍然是同一个 buffer 名字。

两种形态对 app 透明，性能都取决于数据量与 marshal 开销。

## 为什么单向 API 能做到这点

`glBufferSubData(target, offset, size, data)` 没有返回值、也不要求外部可观察的副作用。完整的语义全部装在输入参数里，可以像 `glDrawElements` 一样 marshal 成一条后续命令，app 线程立即返回。与之相反，`glMapBuffer` 要求返回可写指针，见 [[glmapbuffer-threaded-driver-stall]]——无法延迟。

driver 真正执行时，若检测到 `offset == 0 && size == full`，可以安全地隐式 orphan（旧存储挂给尚未跑完的 draw），然后自己在驱动线程内 map+memcpy+unmap，整条调用链对 app 不可见。

## 为什么还是要付两次 memcpy

代价：**app 传入的 `data` 指针在返回后可能立刻失效**（app 会复用这块内存），驱动必须在 FIFO marshal 阶段把数据拷到内部缓存，等轮到执行时再 memcpy 到真显存。小数据（一个 UBO 里几个矩阵）两次 memcpy 忽略不计；几 MB 的大几何就变得昂贵——这时候显式 persistent map + 应用层同步更划算。

## UBO 流式更新：为什么影响 draw call rate

Supnik 强调 streaming uniform 是最残酷的 case——"几乎每个 draw call 前都要更新一个 UBO，UBO 更新速度就是 draw call rate"。候选方案的实测排序：

- `glMapBuffer` + orphan：**不可用**。跨线程同步一次就吃掉所有 UBO 更新预算。
- Loose uniforms（`glUniform*` 系列）：Windows 上表现良好，但 API 流量大——更新几字节要打好几次函数调用。
- **`glBufferSubData`**：≈ 或略优于 loose uniforms（小 UBO）。本文主推路线。
- 预构建覆盖多 draw 的大 UBO + 动态 offset：若能承担离线规划成本，是最快的。
- 用 attribute 替代 uniform：OS X 上能击败 loose uniform 约 2×，其他平台波动大。

两条 Next-gen 的提示：
- DX12 的 *upload heap* + 资源屏障让"把小量数据显式写进 GPU 读的内存"成为规范流程；
- Mantle/Vulkan 允许 UBO 保持 map 状态、跟着 command buffer 的记录写入，不存在 GL 的隐式 flush 问题。

## `glBufferData(NULL)` vs `glBufferSubData` 的选择

评论区提问：`glBufferSubData(target, 0, size, data)` 和 `glBufferData(target, size, data, usage)` 是否等价？Supnik 的回答：**用 SubData**。

最好情况 `glBufferData` 的驱动实现会判断"能走 SubData 路径"——但你付了一次额外的 CPU 判断；最糟情况驱动没识别出来，做了一次完整重分配。app 有知识（比如知道内容替换不需要重新分配），就该让它替驱动省事。该决策呼应 [[api-fast-path-design|API fast path]] 的设计原则。

但"orphan + map + memcpy + unmap" vs `glBufferSubData` 在不同驱动栈上波动很大——可观察到的 Daniel（Quake2 GL3 renderer 作者）测试中 Intel Iris Pro 上 `glBufferData` 翻倍，Radeon 上 +15%，Intel IvyBridge 与 NVIDIA 几乎无差。Supnik 的建议：**同一份代码留两条路径，在 NV 控制面板开/关 threaded driver 都测一遍**。

## 小批量 orphan 的坑

评论中追认：orphan 大量小 VBO 时，AMD 驱动会周期性暂停几 ms——orphan 隐含的分配器在小粒度下吃亏。VBO 的物理最小占位是 VM 页大小（4 KB 起），orphan 再小也要付这一页。**不要用小 VBO 当 staging**——要么合并，要么走 ring buffer（参见 [[glbuffersubdata-serialization]] 的 Rob Barris 方案）。

## 相关
- [[glmapbuffer-threaded-driver-stall]] —— 为什么 map 在同一驱动上反而变慢
- [[glbuffersubdata-serialization]] —— 同名调用的早期串行化陷阱
- [[buffer-renaming]]
- [[vbo-double-buffering-orphaning]]
- [[api-fast-path-design]]
- [[vulkan-explicit-performance]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-glmapbuffer-no-longer-cool]]
