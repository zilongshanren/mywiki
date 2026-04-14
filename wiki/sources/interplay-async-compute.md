---
tags: [source, 渲染, GPU, D3D12, async-compute, 调度]
date: 2026-04-14
sources: 1
---

# Async compute all the things（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou]] 发表于 2025 年 5 月的实操文章，在 toy engine 里为 GTAO / BRDF LUT / RTGI ray gen 等 compute pass 加入 async compute 路径，量化几组不同 pairing 的收益。

## 摘要

Kostas 的出发点是一张 GPU trace 截图——一帧里 shadow pass 和 gbuffer pass 把 World Pipe (几何) 和 VRAM 推满、但 SM 闲置一半；而 GTAO/RTGI 这种 screen-space 任务反过来压 SM/ 缓存却浪费几何单元。文章先讲清楚 D3D12 的 command queue 模型和 fence 同步（Signal/Wait 是 GPU 阻塞、CPU 不阻塞），点出"compute queue 看不到 RT/PS resource state，对应 transition 只能在 graphics queue 上做"这条硬限制。然后给出多组 **RTX 3080 mobile / 1080p** 的实测数据：GTAO 盖在 raytraced shadows（RT core bound）上串行 5.73 ms → 并行 4.60 ms；GTAO+BRDF+Hi-z+Shadowmap 四流 7.0 → 5.7；**把 shadowmap 和 gbuffer 调换顺序后，几何 bound 的 rasterized shadowmap 能同时吞掉 GTAO+RTGI+BRDF，6.63 → 4.71 ms**。反面例子：GTAO 盖在同样 SM 密集的 RTGI+Lighting 上只赚 0.7 ms。几个关键观察：**单独放到 compute queue 跑不变慢**（说明 cross-pipe 本身不收税，慢是资源争用）；**单 pass 成本会涨**（GTAO 1.97 → 3.22 ms），但合计仍赚；**SM 是动态再分配**（把 shadow 加速后 GTAO 跌到 2.3 ms）；**Priority 字段在 NVidia 上无感**。作者警告 bubble 风险：Wait 撞上 Signal 未到会 drain pipe；并强调每个 async task 都应保留同步 fallback——不只是兜底，更是 profile 单 pass 改动影响时唯一可信的 baseline。

## 关键要点

- **async compute 是 scheduling 机制，任务仍抢同一 SM 池**——pairing 不好会双输
- **好 pairing 的判据**：bottleneck 互补（RT core × SM、几何 × SM、cache × ALU）
- **坏 pairing**：两个都是 SM+cache 密集——GTAO ⊕ RTGI+Lighting 只赚 10%
- **典型空洞**：frame 开头的 shadow/z-prepass/gbuffer 是几何 bound，SM 大片空闲——screen-space compute 最适合填
- **pass 重排是免费优化**：shadowmap 和 gbuffer 顺序调换就能让 shadowmap 盖住后面 3 个 compute pass
- **Wait 阻塞 GPU 但不阻塞 CPU**——CPU 仍可继续提交命令
- **Compute queue 不能做 RT/PS resource transition**——必须留在 graphics queue
- **测量要看总耗时，不要看单 pass**：单 pass 一定会变慢
- **SM 分配是动态的**：不是按 pipe 静态切分；空闲一侧可以把 SM 让给另一侧
- **D3D12 的 priority 字段在 3080 mobile 上无感**
- **保留同步 fallback**：作为 baseline + profiler 参照
- 读者评论区问了一个好问题："work graph 内部是不是在做 async compute？"

## 链接到的概念

- [[async-compute]]
- [[d3d12-work-graphs]]
- [[bottleneck-analysis]]
- [[gpu-fence-timeline-semaphore]]
- [[gcn-wave-occupancy]]
- [[render-graph]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/05/27/async-compute-all-the-things/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-05-27_async-compute-all-the-things.md`
