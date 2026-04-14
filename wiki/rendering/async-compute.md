---
tags: [渲染, GPU, D3D12, 异步计算, 调度, 性能]
date: 2026-04-14
sources: 1
---

# Async Compute

**Async Compute**（AMD 叫 Asynchronous Compute、NVidia 叫 Simultaneous Compute and Graphics）是让 GPU 在同一时刻**同时**消化两路任务的一种调度机制。它靠的是硬件里独立的 **graphics pipe** 和 **compute pipe** ——前者能看到完整的 VTG/IA/PA/VPC/ROP 固定功能栈，后者只能访问 SM、caches 和 memory 相关的单元。两路上来的指令都进入同一片 SM 池争夺资源——所以 async compute 本质上是**填洞**：把一路上用不满的 SM/ cache / memory 喂给另一路。

## 为什么要做

典型一帧的时间线 bottleneck 在不断切换：

- 帧开头的 **shadow pass / z-prepass / g-buffer pass** 吃**几何单元**（VTG、PA），SM 可能吃不饱；
- 中段 **GTAO / SSSR / GI / RTGI** 这种 screen-space lighting 是 **SM + cache** 密集；
- 末段 composite、tone map 又偏向 ROP 和 bandwidth。

各 pass 独自跑的时候，必有一大块 GPU 单元在闲置。async compute 的目标是把两条时间线**错位叠加**，让 pipe A 的 SM 空闲时段被 pipe B 的工作填满。

## API 形态

DX12 抽象成三种 command queue：**graphics**（最强、可以跑所有东西）、**compute**（只跑 compute shader 和 RT）、**copy**（只做数据搬运）。做 async compute 就是：

```cpp
D3D12_COMMAND_QUEUE_DESC d = {};
d.Type = D3D12_COMMAND_LIST_TYPE_COMPUTE;
m_device->CreateCommandQueue(&d, IID_PPV_ARGS(&m_computeQueue));
```

把原本在 graphics queue 上的 compute pass 挑出来，改成在 compute queue 上 ExecuteCommandLists。

**同步靠 fence**。想让 compute pipe 等 graphics pipe 先把 g-buffer 写完：`graphicsQueue->Signal(fenceA, v)` → `computeQueue->Wait(fenceA, v)`。反过来，让 graphics pipe 等 compute 的 GTAO 结果：`computeQueue->Signal(fenceB, v)` → `graphicsQueue->Wait(fenceB, v)`。`Wait` **阻塞 GPU 但不阻塞 CPU**，整条 pipe 会停下来等 signal。

一条**硬限制**：compute queue 看不到 RT/PS 相关 resource state，所以像 `D3D12_RESOURCE_STATE_RENDER_TARGET` 或 `PIXEL_SHADER_RESOURCE` 的转换**只能在 graphics queue 上做**。

## 关键原则：pairing 决定一切

所有任务还是抢同一片 SM 池。**配得好能赚，配不好会赔**。Kostas 在 RTX 3080 mobile / 1080p 上做的几组对照：

### 好配对

| 配对 | 串行成本 | async 成本 | 增量 |
|---|---|---|---|
| GTAO（SM+cache 密集）⊕ Raytraced Shadows（RT core 密集）| 5.73 ms | 4.60 ms | **−1.1 ms** |
| GTAO ⊕ BRDF LUT ⊕ Hi-z ⊕ Shadowmap（4 pass 合流）| 7.00 ms | 5.70 ms | **BRDF 免费** |
| GTAO + RTGI-RayGen + BRDF LUT ⊕ **光栅化 Shadowmap**（几何瓶颈）| 6.63 ms | 4.71 ms | **−1.9 ms** |

最后一组尤其说明问题：光栅化 shadowmap 是**几何单元 bottleneck**（VTG/PA），SM 闲置大半——这正是 async compute 填洞最有效的场景。

### 不那么好的配对

GTAO 盖在 GenerateRays(RTGI) + Lighting 上，两边都是 SM+cache 密集，最终只从 6.8 ms 降到 6.1 ms——**依然有收益，但幅度小**。同理，把两个都是 ALU-bound 的 pass 配在一起会互相抢 SM，甚至可能双输。

## 可量化的现象

- **单独跑没变慢**：把 GTAO 独自放到 compute queue 上跑，成本和放在 graphics queue 上**完全一样**——说明跨 pipe 本身不收税，慢下来的时候就是在 **SM 资源争用**。
- **个体成本会涨**：GTAO 在 async 并发中成本从 1.97 ms 涨到 3.22 ms；但合计仍比串行便宜。**评价维度必须是总耗时，不是单 pass**。
- **SM 分配是动态的**：把 shadow pass 人为加速后，GTAO 从"全遮盖 Shadowmask"的 3.22 ms 掉到"部分遮盖"的 2.3 ms——说明 SM 不是按 pipe 静态切分，而是按需重分配。
- **bubble 风险**：如果 `Wait()` 撞上 `Signal()` 还没到，对应 pipe 会 drain 成气泡。工作量差异大的两路任务很容易漏 timing。
- **Priority 字段在 NVidia 上无效**：`D3D12_COMMAND_QUEUE_PRIORITY_HIGH` 在 3080 上观察不到任何差别。

## 实战建议

- 先测单 pass 的 **bottleneck profile**（SM / cache / memory / 固定功能），然后找**互补**的两路来配。
- 调整帧内 pass 顺序是**免费的优化**：Kostas 发现把 shadowmap pass 和 gbuffer pass 对调，让 shadowmap（几何 bound）和 GTAO+RTGI+BRDF（SM bound）重叠，就能拿到一整 ms。
- 每个 async 任务都保留**同步版本**作为 fallback：一是用来当 baseline 测收益，二是**做优化的时候永远在同步版本上测**——async 并发会混淆单 pass 的改动是不是有效。
- GPU 架构差异大，配对策略**不跨 GPU 可移植**。要在每张目标卡上分别 profile。

## 和相关机制的关系

async compute 和 [[d3d12-work-graphs]] 想解决的问题有一部分重叠——work graph 评论区就有读者问 "它内部是不是在做 async compute？" 区别是：async compute 是**人工编排两路任务互相填洞**，work graph 是**一路管线内部让 GPU 自己切分工作**。前者需要理解 bottleneck，后者让 driver 做调度。

async 本身不是魔法——在 AAA 引擎里加入 async 路径的收益通常要靠**精细的 pass 重排 + per-GPU 调参**才能稳定拿到。小引擎和 indie 项目更多情况下先保证**单条 pipe 的 pass 排序和 bottleneck 平衡**，再考虑 async。

## 相关

- [[d3d12-work-graphs]] — 另一种改善 GPU 利用率的新机制，目标部分重合
- [[bottleneck-analysis]] — 判定"哪里瓶颈、SM 有没有空洞"的方法论
- [[gcn-wave-occupancy]] — 理解 SM 争用对 occupancy 的影响
- [[gpu-latency-hiding]] — 另一个"填洞"技巧，在 warp 层面而不是 pipe 层面
- [[gpu-fence-timeline-semaphore]] — fence 的更广义讨论
- [[render-graph]] — 重新排列 pass 顺序的框架支撑

## Sources

- [[sources/interplay-async-compute]]
