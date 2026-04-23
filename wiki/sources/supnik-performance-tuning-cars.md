---
tags: [source, 性能优化, X-Plane, profiling, SSE, inlining, 案例]
date: 2026-04-19
sources: 1
---

# Performance Tuning Cars（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2011 年 5 月 18 日的一篇完整性能手术记录：把 X-Plane 10 的汽车系统（50 万车灯 + 车 AI）从 7–8 fps 推到可用水平。

## 摘要

文章按标准瓶颈分析流程推进：先隔离（暂停=纯绘制，下视=纯 AI），然后双维度 profile（时间 + L2）聚焦主线程。初步结论：AI 贡献 ≈ 20 ms/帧、车灯贡献约 50 万 @ 7–8 fps、3D 车身走 instancing 几乎无代价。具体热点上，AI 慢是 quad-tree 编辑调用未 inline 的 per-object 访问器；绘制慢是车灯矩阵变换。最大的一刀来自砍「无用功」：前向渲染路径仍在生成 deferred spill light（结果被丢弃），砍掉几乎绘制翻倍；HDR 模式下 210 万 deferred light 顶点 @ 5 fps，车灯 LOD 从 20 km 降到 5 km → 128k 顶点 @ 10 fps；车灯的「相位调制」对车灯无意义，砍掉后 695k 车灯 @ 14.5 fps。接着是 inlining：用宏控制 inline 从头文件 vs. translation unit 展开，既留 debug 可读又让 release 彻底 inline，44k 车 AI 到 41 fps。由此引出一个判断：**GCC 4.0 无法跨未 inline 的调用链传递常量分支**，所以有时必须手工 function specialization。最后才上 SSE：L2 profile 显示矩阵变换不是内存瓶颈（补进 [[simd-memory-bandwidth-bound|同月那条 SSE-memory]]  的反面），是 compute-bound，SSE 改完吃 ≈26% 车灯子系统加速，总帧时间 6%。不把工作丢到 GPU/多线程的原因：AGP 映射的多线程 sync 风险高；顶点数据不规则上不到最低硬件基线；AI 则可以「免费」并行到独立线程。

## 关键要点

- 隔离变量：暂停 vs. 下视，各自独立 profile
- 双维度 profile：时间榜 + L2 miss 榜重叠 → 内存瓶颈；不重叠 → compute-bound
- 最大一刀：剪无用功（前向下的 deferred spill light、白天的夜间效果、相位调制车灯）
- Inlining 不是微优化：44k 车 AI 有显著 fps 提升
- GCC 4.0 跨非 inline 调用的常量传播失败 → 手工 function specialization
- SSE 必须在 compute-bound 区段才值得做
- 多线程的门槛：driver/API 兼容性往往大于收益
- 方法论顺序：隔离 → 双 profile → 剪无用功 → inline 热访问器 → SIMD → 并行化

## 链接到的概念

- [[xplane-headlight-perf-teardown]]
- [[bottleneck-analysis]]
- [[optimization-leverage-ratio]]
- [[simd-memory-bandwidth-bound]]
- [[sse-tricks]]
- [[cache-friendliness]]
- [[deferred-rendering]]
- [[gpu-instancing]]
- [[xplane-instancing-2011-numbers]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/performance-tuning-cars.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-18_performance-tuning-cars.md`
