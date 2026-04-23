---
tags: [渲染, 性能, X-Plane, profiling, 案例]
date: 2026-04-19
sources: 1
---

# X-Plane 车流/车灯性能拆解（Supnik 2011）

[[ben-supnik|Supnik]] 2011 年 5 月对 X-Plane 10 的「汽车」系统做了一轮完整的性能手术。这个案例把 [[bottleneck-analysis|瓶颈分析]] 的全流程跑了一遍——**隔离、测量、剪掉无用功、再 SIMD**——值得当成 X-Plane 10 时代 CPU 渲染性能工程的样板范例。

## 测试隔离

要看汽车成本，先把别的东西都「降智」：视距拉满、车数拉满、飞行模型简化、同时跑 10.5.8 与 10.6.7 排除驱动差异，并用两种视角拆分：

- **暂停 + 前向视角** → 没有 AI，只剩绘制；
- **不暂停 + 下视 + 世界被 cull** → 没有绘制，只剩 AI。

两个视角独立 Shark profile、全线程状态、聚焦主线程。这种「一次拆一变量」的隔离技术是整轮优化的基础。

## 初步发现

- AI 约 20 ms/帧；
- 50 万个车灯以 7–8 fps 在推——**真正的主要瓶颈**；
- 3-d 车辆本身几乎零成本（视距短 + 全走 instancing 路径）。

热点再细拆：

- AI：quad-tree 编辑。即便有 cache，剩下的操作依然慢，因为要访问**未被 inline 的 per-object 访问器**。
- 绘制：车灯矩阵变换。

## 剪掉无用功

**最大的一刀**：前向渲染路径里也在为 deferred "spill" light 做变换——这些 light 在前向路径里被直接丢掉。砍掉这段几乎**绘制性能翻倍**。相关的一类决策：白天也在为车灯做全量工作（X-Plane 10 把日/夜开关交给 GPU），暂不改；车灯的「相位调制」对于车灯**毫无意义**（不是频闪灯），砍掉——695k 车灯到 14.5 fps。

> **没有什么比「不做」更快**——是这一段最硬的教训。

其他可剪：dynamic scenery 的 deferred light 设 cutoff 距离；迁到 geometry shader / instancing；worker 线程预建 VBO。从 20 km 视距砍到 5 km：从 210 万 deferred light 顶点 @ 5 fps → 128k 顶点 @ 10 fps；2 km → 12 fps。

## Inlining 不是微优化

AI 热点里的非 inline 访问器被 profile 点名后，Supnik 用宏控制「inline 代码从头文件 include 还是从 translation unit include」——既保持 debug 模式的干净 GDB 行为和编译速度，又让 release 里彻底内联。结果：44k 辆车从 ~30 fps 到 41 fps，**纯 inlining 带来的加速**。这反映 GCC 4.0 在**跨函数常量传播**上的局限：call site 不 inline 时，`if (flag)` 分支裁剪看不穿调用链。Supnik 的临时解是**手工 function specialization**，把常值参数版本写成单独函数。

## SIMD 在哪值得

全部剪完之后，头灯变换剩下的热点仍在矩阵变换本体。L2 cache profile**不显示**这里的 miss 集中——意味着不是内存带宽瓶颈，可以继续压指令。SSE 改完给了 ≈15% 改善。最后一栏数据：车灯占 23% 帧时间，SSE 让总帧时间降 6%（即车灯子系统 ≈26% 加速）。

## 为什么不丢到 GPU / 多线程

- 变换目标是 AGP 映射内存，多线程填需要 OpenGL sync + 多驱动兼容验证，投入产出比不划算；
- 顶点数据来自不规则结构，GPU 侧构建要求的最低硬件基线 X-Plane 支持不起。
- 但 AI 可以「免费」地并行化：与飞行模型分线程跑，多核机上 worker 不饱和就是白得。下视状态从 65 → 80 fps。

## 方法论收敛

这一系列改动的顺序是**值得背诵**的：

1. **隔离变量**（暂停 vs. 下视）
2. **双维度 profile**（时间 + L2）
3. **砍无用功**（占比最大的一次性胜利）
4. **inline 热访问器**（让编译器看穿数据流）
5. **在 compute-bound 区用 SIMD**（见 [[simd-memory-bandwidth-bound|反面教训]]）
6. **最后才考虑并行化**（只在新代价低于收益时）

放到 [[optimization-leverage-ratio|杠杆率]] 框架里：步骤 1–3 是砍高杠杆项，步骤 4–6 是在剩余高杠杆段里二次挤压。

## 相关

- [[bottleneck-analysis]]
- [[optimization-leverage-ratio]]
- [[simd-memory-bandwidth-bound]]
- [[cache-friendliness]]
- [[deferred-rendering]]
- [[gpu-instancing]]
- [[draw-call]]
- [[xplane-instancing-2011-numbers]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-performance-tuning-cars]]
