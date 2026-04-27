---
tags: [grass, gpu-driven, indirect-draw, blue-noise, lod, culling]
date: 2026-04-14
sources: 1
---

# GPU 驱动的瓦片化草地系统

这是 [[marco-giordano]] 在自研 Vulkan/DX12 引擎里实现的草地方案，和 [[deferred-grass-shader]] 是同一个问题（一大片实时草）走的两条完全不同的路线：Steven Sell 的版本走 tessellation + geometry shader + 延迟 alpha cutout；Marco 的版本走 **blue noise 预烘焙分布 + vertex 扩展 + compute 剔除 + 间接绘制 + LOD 压缩**，目的是让整个"可见草片选择"的决策都发生在 GPU 上。

## 问题分解

实时草地的两大瓶颈都和"绘制了太多看不见的东西"有关：
1. **Overdraw / VPC 瓶颈**：大量窄而重叠的三角形把 viewport culling（VPC）阶段打爆。
2. **LOD 的分布稳定性**：要远处稀近处密，但如果随便"每隔 N 个采样一次"就会出现成团和空洞。

Marco 的切入点是先解决第二条——**只要底层点分布本身支持"任取前 K 个点都仍是好的蓝噪声"，LOD 就变成选 K 的问题**，而 culling 只剩下"整块瓦片要不要"。

## Blue noise 瓦片预烘焙

草的位置来自预烘焙的蓝噪声瓦片，由 [[alan-zucconi|Alan Wolfe]] 给的 C++ 代码生成。每块瓦片 10000 个点，共 100 块，每个点是瓦片内归一化坐标 [0, 1]。蓝噪声的性质保证"任意前缀子集仍保留良好分布"——LOD 直接取前 K 个点即可，不需要任何重采样或抖动。生成代价很大（6 核 / 12 线程跑 3 小时），但只需要跑一次，结果以二进制烘焙进资产。这是典型的**一次离线换无数次在线**。

## Vertex shader expansion，不用 geometry/tessellation

Marco 有头发 expansion 的老经验（见博客 hair 文），加上 geometry shader 在现代硬件上向来慢、tessellation 对 grass 来说成本也偏高，所以直接把 **"1 instance → 一片 4 顶点 + 2 三角形的草叶"** 的展开逻辑写在 vertex shader 里，基础着色器参考 Roystan 的 Unity 草教程。风的效果采 distortion map，**按 UV.y（顶点离地高度）偏移采样**，越靠叶尖偏得越大，于是一片草像鞭子一样有"尖部先动、根部滞后"的动态，这个 trick 来自 Freek Hoekstra 的建议。首版在大约 1.5ms 内渲染 1400 万顶点，但 profile 立刻指出 VPC 是最大瓶颈，**不剔除是没活路的**。

## GPU culling + 间接绘制

剔除放在 compute shader 里，两步：
1. **Vote**：每个 thread 处理一个瓦片，算它对主相机（不是当前 active 相机，方便 debug flythrough）的 frustum 交集，写出一个"要/不要"标志。
2. **Compact**：存活瓦片压到一个连续数组里，配合 draw indirect buffer 的 instance count 字段，一个 draw call 把整片草画完。

Marco 特别提了一条经验：**draw indirect buffer 的 barrier 要用专门的 indirect transition**，不是普通的 write-read barrier。他最初漏了这一点，表现为随机闪烁。这类细节是 GPU driven 管线的常见陷阱，和 [[gpu-hazard-tracking]] 里讨论的是同一类问题。

Intel iGPU 上还遇到一个疑似编译器 bug 的 culling 失效，他录了"culling 出错"的 gif 做对比。

## LOD：四路 scan 压缩

剔除和 LOD 在同一个 compute pass 里做。LOD 计算就是最简单的"相机到瓦片中心的距离分桶"，得到 0~3 四档。接着对每一档各做一次 scan（前缀和）把同档瓦片压到一个连续段，四段结果写进同一个大数组，用偏移区分。最后一个小 compute shader 读 scan 结果、填 4 个 indirect draw buffer、顺便清 atomic counter。

Vertex shader 拿到 LOD 编号以后，用它反查"这个 instance 对应哪块瓦片的哪片草叶"，每档 LOD 的"每瓦片草叶数"是可运行期调的参数。因为蓝噪声保持前缀稳定，**LOD 间过渡时草叶数量变化不会闪烁、不会重分布**——这是整个方案最关键的视觉卖点。

后续还有两个没落地的优化：
- **低 LOD 只画叶尖**（Freek 的另一条建议），进一步压顶点。
- **Mesh shader 版本**：Marco 明确说整个架构是奔着 mesh shader 设计的，一旦铺开就可以把 culling / LOD / geometry 生成合进单个 mesh shader pipeline，省掉 scan / indirect / 多 pass 的那一整套 boilerplate。

## 收益

profile 对比三档（无剔除 / 只剔除 / 剔除 + LOD）：
- 无剔除：一半 shader 时间在生成"最终被早 z / 视锥剔掉的顶点"，绿条拉满。
- 只剔除：绿条缩短但 fragment 工作量涨了（变成 overdraw bound）。
- 剔除 + LOD：顶点更少，fragment 稍多，**整体 shader 快 3×**。VPC 仍是瓶颈但已经能接受。

MSAA 当时没做，作者自嘲"谁不喜欢一片闪烁的锯齿呢"。

## 和其它方案的对比
- [[deferred-grass-shader]]：同题但走 tessellation + geometry shader + 延迟 alpha cutout，单个 shader 自洽，易接 Unity 既有管线；Marco 的方案要自建 compute/indirect 基建，但可扩展性与性能上限更高。
- [[draw-procedural-gpu]] / [[compute-vs-raster-points]]：把"生成大量小几何体"变成 compute + indirect 是同一哲学家族。
- [[culling]] / [[occlusion-culling]]：瓦片级 frustum vote 是 GPU driven culling 的最简形态。
- [[fizzle-lod-fading]]：LOD 切换时的视觉连续性问题，这里靠蓝噪声前缀稳定性天然解决。
- [[gpu-instanced-grass-urp]]：同题的 Unity URP + Shader Graph + `RenderMeshIndirect` 实用版；技术栈完全不同，但 compute frustum cull + AppendBuffer + CopyCount 的 GPU 端数据流同构。

## Sources

- [[sources/giordi91-grass-shader]]
- [[sources/c0de517e-vegetation-cod-bo4]] — 编辑时生成 vs 运行时 GPU 生成的对比视角
