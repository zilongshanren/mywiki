---
tags: [渲染, gpu, instancing, opengl, benchmark, 历史]
date: 2026-04-19
sources: 1
---

# X-Plane 2011 GPU instancing 吞吐数据点

一个**时代坐标**。Ben Supnik 2011 年 3 月报了 X-Plane 在一台 Mac Pro 上跑 OpenGL GPU instancing 的实际数字，作为当时 OpenGL 论坛里各种「instancing 到底多快」争论的一个现场样本。

## 硬件与数字

- **平台**：2.8 GHz Mac Pro（当时几年前的机型）、ATI Radeon 4870、OS X 10.6.6
- **吞吐**：**87,000 个 mesh @ 接近 60 fps**，使用 GPU instancing
- **每次 draw call 平均 32 个 instance**

换算一下：`87000 / 32 ≈ 2718` draw call 每帧，乘 60 fps ≈ **16 万 draw call/秒**——在当时 OpenGL 的典型 CPU 预算下算高位区。

## 为什么保留这个数字

单点数据没有规律性，但作为**时代基线**有用：

1. **校正直觉**。2011 年 GPU 已经能一帧内 instancing 推 87K 个 mesh——说明同年代做场景图的人「担心 instance 数」多半是搞错了瓶颈。
2. **对照后来的甜点**。[[opengl-draw-call-batching-sweet-spot|Outerra 2016 的测试]]把问题推进一步：**不是 instance 数量的上限，而是单个 instanced draw 内部三角形数的甜点**（5k-20k tri/instance）。Supnik 的 32 instance/call 是向外一层的维度。
3. **mesh 粒度 vs draw call**。Supnik 报的是「mesh 数」不是「三角形数」——X-Plane 的 mesh 多半是建筑、树、小物件，单 mesh 三角形不高。落在 Outerra 后来警告的「小 mesh + 小 instance」象限里，但 2011 年的 NVIDIA/ATI 还没有 AMD GCN 新架构那个 5k 阈值的奇怪拐点。

## 一个 Supnik 式的细节
他的数字**没有给 frustum cull 之前的原始 object 数**——所以这 87K 是已经粗选过的，还是全量？对标别家数据时要注意。他本人也只是「给数字 / 不解释」，就像当时所有 OpenGL 论坛里你问一个人要 instancing 数字，人家扔个短帖就算答。

## 两个月后的续篇：上下限

2011-05-24 的 [[sources/supnik-instancing-limits|Instancing Limits]] 给同一组数字加了边界。上限：在 ATI Mac 上 instanced batch 数往上压到 **≈100k** 就卡住。下限：单个 batch 里 instance 数少于 **2–3** 时，immediate mode 多次 draw 反而更快。另有 OS X 10.6.x 的陷阱——instance 数据走 client array（系统内存）不走 VBO 会掉到非加速路径，性能直接塌。更深一层的待调甜点是 clump 粒度：大 clump 省 driver 调用但 cull 不彻底，小 clump cull 干净但 driver 调用多。

## 相关

- [[draw-call]]
- [[sprite-batch-instance-draw]]
- [[opengl-draw-call-batching-sweet-spot]] —— Outerra 2016 更系统的后续测试
- [[gpu-instanced-grass-urp]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-instancing-numbers]]
- [[sources/supnik-instancing-limits]]
