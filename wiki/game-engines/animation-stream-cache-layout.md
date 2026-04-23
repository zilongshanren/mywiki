---
tags: [animation, cache-layout, streaming, data-oriented, bitsquid]
date: 2026-04-19
sources: 1
---

# 动画数据的流式缓存布局

Bitsquid 引擎对"曲线拟合后的动画数据如何排布"给出的答案：按**需要的时间**而不是按 track 排序，得到一条可顺序扫描的流；同时维护一个小的 **active 数组**装当前正在求值的曲线点。结果是整个动画评估只需要两次 memory access——active 数组访问 + 流指针前进。

## 问题

角色动画由若干 track 组成（100 骨骼 × 2 通道 = 200 track 起步），每 track 是一串曲线点 `(t_i, A_i)`。评估时刻 `t` 需要前后两个点。**按 track 排序、再按时间排序**是最自然的布局，但这样每帧都要在 200 条 track 里各跳一次——200 次 cache miss。光"按时间排"也不行，因为一条恒定曲线只有首尾两点，会躺在流的两端。

## 解法

**分离 hot / cold**：
- **active 数组**（hot）——所有 track 当前"正在夹住 `t`"的那两个曲线点。绝大多数时间只读它，一次 cache line 够用。
- **动画流**（cold）——所有曲线点按**它们何时被需要**顺序串起来。播放器只需一个指针指向下一个该拉进 active 的点。

时间推进到某个阈值时，把新点从流 copy 进 active，老点踢出，再评估。由于流是严格顺序访问，可以再 gzip 压缩一倍，也可以直接从磁盘 streaming。每个流里的点需要额外 11 bit 告诉播放器该放回 active 数组的哪一格（10 bit joint index + 1 bit 区分 position / rotation），这是"全局单流"必付的协议税。

## 代价与补丁

缺点是**不能任意跳转**——你只能从头快进。需要跳转时加 **jump frame** 索引：在若干关键时刻保存 active 数组状态 + 流 offset，跳转时从最近的 jump frame 恢复，再快进一点点。jump frame 密度是空间/跳转延迟的 tradeoff。

## 这是 [[cache-friendliness]] 的一般模式

> "把 hot data 集中，让 cold data 按访问顺序摆。"

它和 [[parameter-nodes-intrusive-linked-list]] 的手法同宗：都是先识别"哪些数据一起被用"，再用**分配策略**让它们物理相邻。也和 [[aos-vs-soa]] 的讨论相关——这里是比 SoA 更激进的"按时间 interleave"。

## 相关

- [[parameter-nodes-intrusive-linked-list]]
- [[pragmatic-performance-philosophy]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[data-driven-architecture]]

## Sources

- [[sources/bitsquid-low-level-animation-part-2]]
