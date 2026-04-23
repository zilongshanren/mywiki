---
tags: [渲染, 性能, opengl, draw-call, instanced-rendering, geometry-shader, outerra]
date: 2026-04-19
sources: 2
---

# Instanced Draw 的三角形吞吐甜点：5k-20k/实例

Outerra 2016 年做了一组严格的 OpenGL 三角形吞吐测试，测的不是 [[draw-call]] 数量上限，而是**「每个 instanced draw call 内部应该塞多少三角形，才能同时压榨住两家 GPU」**。两篇文章分别测 procedural grass（完全程序化、无 per-instance 数据）和 building blocks（有 128 bytes/block 的 per-instance 数据），覆盖 `glDrawArrays[Instanced]` / `glDrawElements[Instanced]`（strip vs list）/ Geometry Shader 三条路径。

## 结论（适合刻在脑子里）

> **把 instance 内部的 mesh 规模塞到 5k–20k 三角形，NVIDIA 和 AMD 都能吃满。**

- **NVIDIA**：小 mesh（< 80 tri/instance）会被 **CPU 侧 driver overhead** 拖垮；mesh 越小 driver 调用越多，CPU 就是墙。
- **AMD（GCN 1.1+，380/390/390X）**：小 mesh（< 1k tri）表现**异常差**，在跨过 5k 三角形阈值后出现**接近翻倍**的吞吐跳跃；更奇怪的是超过 20k 又开始掉。原因 Outerra 没问出来，但在两个独立测试（grass + blocks）里都重复出现，确定是架构层的拐点。
- **旧 AMD（1st-gen GCN 及更早）与 NVIDIA 一样怕小 mesh**（> 80 tri 即可），新架构反而更挑剔。

实践规则：**如果 per-instance mesh 只有几百三角形，手动把多个 instance 拼成一个大 instance**，让单次 instanced draw 的有效三角形数落进 5k-20k。

## Indexed triangle list > 其他

同等条件下**indexed triangle list** 的吞吐最高：

- `glDrawArrays`（strip）为了跨过 blade 之间需要插 2 个退化顶点——每个 blade 多付 2 verts 的代价，只有当每 instance 只画一个 blade（退化顶点不再需要）时才和 indexed 打平。
- **Indexed triangle list** 没有退化顶点开销，结构上也更贴合现代 GPU 的 vertex reuse cache。

顺带发现：**反转 bit 顺序做 blade 索引 shuffle**（保证相邻 thread 不访问相邻位置）在老架构上给个位数百分比的性能加成，现代 GPU 基本不敏感。

## Geometry Shader 基本等同最差 case

GS 的吞吐大致等价于「小 mesh + 小 instance」的 instanced VS，在 AMD 新卡上尤其糟。唯一能反杀的场景是**在 GS 内部做视锥早剔除**——当外部无法剔除的大量 off-screen 几何通过 GS 直接 discard 时，GS 省下的 setup 开销可能补上它吞吐的亏损。

另一个细节：**GS 吞吐随 fragment shader 的 interpolant 数量下降**，尤其 NVIDIA——从 0 个到 4 个 float 的 interpolant 就能明显压降 GS 数字。这让 GS 的性能预测比 VS 复杂得多。

## Back-face culling 与「per-instance 数据量」

blocks 测试的额外观察：

- **NVIDIA** 关闭背面剔除时吞吐掉约 30%（多算一倍真实三角形）。
- **AMD** 关闭背面剔除后掉得远更少——说明瓶颈不在 raster，而在更前端的 prim assembly / instance dispatch。
- **NVIDIA 更偏好 grass 那种「per-instance 数据少、vertex shader 更复杂」的 workload**；AMD 对两种情况差别较小。

## 设计启示

- **吞吐 ≠ draw-call 数量**。Draw call 已经够便宜了；现代 GPU 的真瓶颈在 **per-instance setup + CPU overhead**。与其把 instance 切得更多，不如把每个 instance 做厚。
- **跨厂可移植的安全区间是 5k-20k tri/instance**；低于它吃 CPU overhead，高于它吃 AMD 的奇怪拐点。
- **benchmark 源码是开放的**（`github.com/hrabcak/draw_call_perf`）——任何说「小 draw call 贵」或「geometry shader 很慢」的论断都可以回到这个 bench 里自测。

## 相关
- [[outerra-team]]
- [[draw-call]]
- [[batching]]
- [[gpu-driven-grass-tiles]]
- [[gpu-latency-hiding]]
- [[draw-procedural-gpu]]
- [[triangle-strips-vs-indexed-triangles]] — Supnik 用 CPU draw-call 成本证明 indexed triangles 比 strips 更优

## Sources

- [[sources/outerra-opengl-perf-grass]]
- [[sources/outerra-opengl-perf-blocks]]
