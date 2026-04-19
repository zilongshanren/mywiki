---
tags: [GPU, 并行, wave-intrinsics, 调度, hlsl, nanite]
date: 2026-04-19
sources: 1
---

# 变长工作的波内打包原语（variable sized work）

一个在 GPU 并行编程里反复出现、却**没有被主流原语覆盖**的需求：

> **生产者以常量成本排入变长工作；消费者把这些工作完美打包进 wave，每条 lane 都在干事。**

[[brian-karis|Brian Karis]] 在 Nanite Tessellation 的 split / dice 阶段遇到了它，顺手写了一段通用 HLSL，值得作为一个**可迁移的 parallel primitive** 单独记录。适用面远不限于 tessellation——本质上是 [[d3d12-work-graphs|work graphs]] 想解决的问题的子集，在 wave 尺度上的解法。

## 与光栅化的同构

Karis 指出这和**三角形 → 像素**展开是同一个问题：1 个三角形产生变量个 fragment，需要打包到 wave / tile。硬件光栅器就是为这件事造的。他真试过"把 HW rasterizer 当 work dispatcher 用"——VS 扮演生成器，PS 扮演消费器，用 rect list 做 2×N 的细粒度展开。结果**跑不过软方案**——rasterizer 有 tile 亲和性、有 overlap 串行化等专为像素准备的额外约束。

## Nanite 软光栅为什么比硬光栅快：数据流动决定一切

作为对比，Karis 解释了 Nanite 软光栅能领先 HW 的根本原因：**不做 binning**。HW 光栅化假定工作量大（pixel-bound），要做 triangle setup → bin 到 tile list → 多级 mask → prefix sum 打包 → 散发到 ROP。这些都有数据移动代价，只有当 pixel 工作规模足够大才能摊销。Nanite 软光栅跳过这一切，直接从 register 状态写像素——**当三角形都是 micropoly 时，不移动数据比任何打包都快**。

同样的道理搬到 tessellation：split/dice 产生的新工作项是不定数，如果真的写到内存 queue 再重新读回来就浪费太多带宽；应当**局部在 wave 内分发**，让生产者的 register state 直接被消费者读。

## 核心算法：wave 内 pull-based 分发

数据流：

1. wave 里每条 lane 声明自己要生产 `NumWorkItems` 个子任务。
2. 用 `WavePrefixSum` 算出每条 lane 的起始偏移 `FirstWorkItem`；wave 总量是最后一条 lane 的值。
3. 进入 pull 循环：每轮取 32 项（一个 wave 的量），每条消费 lane 想"我要处理的第 `ItemIndex` 个子任务由哪个生产 lane 提供"。
4. 关键技巧：用 `groupshared` + `WaveActiveBallot` + `firstbithigh` 构建**二分检索**，快速把 `ItemIndex` 映射到 `(SourceLane, LocalItemIndex)`。
5. 消费 lane 用 `WaveReadLaneAt(SourceData, SourceLane)` **直接从生产 lane 的 register 读数据**——不走 groupshared，不走 memory queue。

```hlsl
groupshared uint WorkBatch[ THREADGROUP_SIZE ];

template< typename FTask >
void DistributeWork( FTask Task, uint GroupIndex, uint NumWorkItems )
{
    const uint LaneCount  = WaveGetLaneCount();
    const uint LaneIndex  = GroupIndex & ( LaneCount - 1 );
    const uint QueueOffset = GroupIndex & ~( LaneCount - 1 );

    uint FirstWorkItem  = WavePrefixSum( NumWorkItems );
    uint TotalWorkItems = WaveReadLaneAt( FirstWorkItem + NumWorkItems, LaneCount - 1 );
    uint SourceData     = ( FirstWorkItem << 8 ) | LaneIndex;

    for( uint BatchFirstItem = 0; BatchFirstItem < TotalWorkItems; BatchFirstItem += LaneCount )
    {
        uint ItemIndex = BatchFirstItem + LaneIndex;
        WorkBatch[ GroupIndex ] = 0xFFFFFFFFu;
        GroupMemoryBarrier();

        if( NumWorkItems > 0u )
        {
            int FirstItemLane = int( FirstWorkItem - BatchFirstItem );
            if( FirstItemLane < ( int )LaneCount &&
                FirstItemLane + ( int )NumWorkItems - 1 >= 0 )
                WorkBatch[ QueueOffset + max( FirstItemLane, 0 ) ] = SourceData;
        }
        GroupMemoryBarrier();

        uint BatchValue = WorkBatch[ GroupIndex ];
        uint BatchMask  = WaveActiveBallot( BatchValue != 0xFFFFFFFFu ).x;
        uint BatchLane  = firstbithigh( BatchMask & ~( 0xFFFFFFFEu << LaneIndex ) );
        uint SourceValue     = WaveReadLaneAt( BatchValue, BatchLane );
        uint SourceLane      = SourceValue & 0xFFu;
        uint LocalItemIndex  = ItemIndex - ( SourceValue >> 8 );

        bool bActive = ItemIndex < TotalWorkItems;
        Task.RunChild( bActive, SourceLane, LocalItemIndex );
    }
}
```

Rune 的优化：当 `NumWorkItems == 0` 时不需要 compaction，减少公共路径上的分支。

## 代价与边界

这个原语不是银弹，**它只能在一个 wave 内做负载均衡**：

- 优点：子任务的状态留在生产 lane 的 register 里、不进 memory queue，带宽成本最低；threads 动态打包，只有最后一轮可能有空 lane。
- 缺点：如果单个 wave 产出大量工作，"一个 wave 串行完，其它 wave 空等"——必须限制 `TotalWorkItems` 的上界（在 Nanite 场景里由 TessFactor 上限天然保证）。
- 对于需要跨 threadgroup 或跨 dispatch 的变长分发，要么分阶段（Nanite 的 PatchSplit 就是，先 wave 内 split 一次，剩余写 queue 进下一轮），要么上 [[d3d12-work-graphs|work graphs]]。

## Nanite Tessellation 里的三处应用

Karis 在 [[nanite-tessellation-approach|Nanite Tessellation]] 里用了三次这个原语：

1. **ClusterRasterize 里的就地 dicing** —— 当 base patch 的 TessFactors ≤ MaxDiceFactor 时，不进 dice queue 直接在 wave 内把 dice 出的三角形分发给剩余 lane 做光栅化。
2. **ClusterRasterize 里的就地一步 split** —— 已经算出 SplitFactors 就不浪费，第一层 split 在 wave 内分发子 subpatch 的 barycentric 计算与写入；只有真正需要多层递归的才写进 split queue。
3. **PatchSplit 里的 split 工作分发** —— 同样，wave 内先分发子 subpatch 生成，再把生成结果写到下一轮的 split queue。

## 相关

- [[nanite-tessellation-approach]] —— 使用它的完整管线
- [[d3d12-work-graphs]] —— 跨 threadgroup 尺度的变长工作调度；两者互补
- [[meshlets-and-mesh-shaders]] —— Amplification shader 里的 `WavePrefixCountBits / WaveActiveCountBits` 是同一类思路的特化
- [[nanite-virtualized-geometry]] —— cluster 层级遍历也用类似的 persistent thread + 全局队列
- [[brian-karis]]

## Sources

- [[sources/karis-variable-sized-work]]
