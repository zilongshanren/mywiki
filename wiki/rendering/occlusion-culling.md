---
tags: [渲染, 可见性, 剔除, 性能]
date: 2026-04-14
sources: 1
---

# 遮挡剔除（Occlusion Culling）

**遮挡剔除**是 [[culling|culling]] 层级里负责「挡在别的东西后面的物体不用画」的一层。和 [[culling|frustum culling / distance culling / contribution culling]] 不同的是：前几层只问「这个物体的包围盒几何上是否符合条件」，是 O(1) 判断；遮挡剔除要问「现有场景是否已经把它挡住了」——这是一个**相对于其他几何**的问题，必须要么做预计算、要么做运行时光栅化 / 查询。

## 几种主流方案的权衡

| 方案 | 代表作 | 优势 | 痛点 |
|---|---|---|---|
| **Static PVS**（Potentially Visible Set） | Quake | 运行时 O(1) | 预计算慢（10+ 小时），动态物体当作不遮挡 |
| **Portals** | 室内引擎 | 视锥逐 portal 裁剪，自然适合走廊门窗 | 只对室内好 |
| **Anti-portals** | 户外局部遮挡 | 动态便宜 | 数量有限，occluder fusion 实际不可行 |
| **Hardware Occlusion Queries (OQ)** | DX10+ | 支持任意动态场景 | latency、popping、CPU overhead、成本和屏占比正相关 |
| **HZB 查询** | [[sources/selfshadow-practical-visibility\|Splinter Cell: Conviction]] | 固定开销、逐物体可查、支持 [[cached-shadowmaps\|shadow caster culling]] | 大屏占物体精度略低 |
| **软件光栅遮挡** | [[sources/selfshadow-practical-visibility\|Battlefield 1/2]]、Warhawk、Intel Masked Occlusion | CPU（SPU）空闲资源利用、零 GPU 消耗 | 实现复杂，需要手写 rasteriser |

## 硬件 OQ 为什么实战不够用

[[stephen-hill|Hill]] & Collin 在 *Practical, Dynamic Visibility for Games* 里系统列了 OQ 的毛病：

- **无法 batch**——多个测试不能打进一个 draw call，每个 query 各占 CPU 开销，几百个就到头。
- **延迟 / 同步**——GPU 算完 CPU 才能读，要么等一帧（popping）要么插入屏障破坏并行。
- **Popping**——Latent queries 把结果延后一帧，相机 / 物体一移动就漏画，靠延伸 bounds / 扩大 frustum 能缓解但不能根除。
- **GPU overhead**——可见性不该跟直接渲染抢 GPU 时间，尤其是主机世代 CPU/SPU 还有富余。
- **可变成本**——测一个物体的成本正比于它的屏占面积，和它**真实的渲染成本**没关系。

## Conviction 的 GPU HZB 方案

[[hierarchical-z-buffer|Hierarchical Z-buffer]]（HZB）是 1993 年 Greene 提出的数据结构：从一个低分辨率 occluder depth buffer 开始做 mipmap，**但每层取 2×2 texel 的最大深度**（远值），得到一个越粗越保守的 z-pyramid。运行时对每个物体做：

1. 顶点着色器里把它的 world-space AABB 投影到屏幕，算出屏幕 bounds、最小深度 `min_z`、以及覆盖这个 bounds 的最粗 HZB mip 层。
2. 像素着色器里对该 mip 层的 4 个（或 4×4）角点 texel 做 `max`，得到该屏幕矩形下的最大场景深度 `max_z`。
3. `min_z > max_z` ⇒ 物体完全被挡住，输出 0；否则输出 1。

结果通过 memexport / stream-out 回读到 CPU。Xbox 360 上 22000 个物体一帧总成本约 **0.52 ms**，而且**与物体屏占无关**——比 OQ 更稳定。由于逐物体都能发起 query，剔除粒度也比需要 BVH 聚合的 OQ 方案更细。

它还能顺手带跑 contribution culling、texture streaming、LOD 选择、光照 / AO volume / decal 裁剪，因为「屏幕 extents」是所有这些决策的共同输入。

**Shadow caster culling**：对每个阴影级联走一遍同样流程——先做一遍 light-space HZB 测试决定哪些 caster 对阴影图有贡献，再把剩下 casters 的「active shaft bounds」变换到主相机空间，用主相机 HZB 再剔一次。两轮都是纯 HZB 查询，不需要 shadow volume。

## Battlefield 的 SPU 软光栅方案

DICE 在 Frostbite 引擎里选了另一条路：把 occluder 低模送到 SPU 上软件光栅化到 **256×114** 的 z-buffer，再把 occludee 的 AABB 投影到屏幕后用最小深度做矩形查询。SPU 上多个 job 各自有一个本地 z-buffer、用 mutex 串行合并到主内存里。典型场景 5 个 SPU 并行：

| 阶段 | Time / SPU |
|---|---|
| Triangle setup | 0.4 ms |
| Rasterisation | 1.0 ms |
| Frustum cull | 0.6 ms |
| Occlusion cull | 0.3 ms |
| **Total** | **2.3 ms** |

好处是完全不占 GPU、全动态、结果在 CPU 侧可以立即用来跳过动画 / 骨骼更新；代价是要自己写一个可靠的软光栅器。

## 两套方案的共同教训

- **艺术家手绘 occluder 很脆**：大项目里视觉几何会变，occluder 没人同步；艺术家倾向于把 occluder 当 collision 做，稍稍凸出真实表面一点就会导致 *scope mode* 下半屏消失。自动化合并 / 简化视觉网格也许是更好的路。
- **固定成本比尖峰便宜**：OQ 的问题不是平均成本高，而是最坏情况难以 bound；HZB / 软光栅的成本基本与物体数线性相关、无 spike。
- **查询粒度 > 每次查询精度**：逐物体 HZB 虽然单点精度不如真实光栅，但因为粒度更细，整体剔除率反而高于手工聚合的 OQ。

## 相关

- [[culling]] — 剔除分层全景
- [[hierarchical-z-buffer]] — HZB 数据结构与查询
- [[cached-shadowmaps]] — 时间维度的 caster 剔除
- [[z-buffer]]
- [[stephen-hill]]
- [[gpu-based-occlusion-culling]] —— Kostas 的 DX11 GPU-driven HZB + stream compaction retrofit

## Sources

- [[sources/selfshadow-practical-visibility]]
