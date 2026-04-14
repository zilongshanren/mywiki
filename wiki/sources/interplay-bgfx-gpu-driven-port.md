---
tags: [source, 渲染, gpu-driven, 剔除, bgfx, 跨平台]
date: 2026-04-14
sources: 1
---

# Porting GPU driven occlusion culling to bgfx（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2018 年 3 月应 Branimir Karadžić（bgfx 作者）邀请，把自己的 [[gpu-based-occlusion-culling|GPU-driven occlusion culling]] 示例移植到跨平台渲染库 [bgfx](https://bkaradzic.github.io/bgfx/)。本文是一次移植笔记——技术没变，但换 API 暴露出了 DX11 原生写法依赖的一串设施在 bgfx 里缺席。

## 摘要

bgfx 是一个 deferred submission 的跨平台图形库：一个线程提交命令，另一个线程消费。它的 shader 语言像 GLSL，但加了跨平台抽象。最大的麻烦是 **bgfx 不直接支持 structured buffer**；可读可写 buffer 需要通过 vertex / index buffer 的 variant（static vs dynamic、带 `BGFX_BUFFER_COMPUTE_READ_WRITE` 标志）来借壳实现。作者因此把原本几个 structured buffer 都改成了 index/vertex buffer，数据内容不变。

其他移植时踩到的点：indirect buffer 不能从 CPU 写，于是 occluder pass 退回 regular instancing 一次一 draw；null pixel shader 不被支持，于是加一个 dummy pixel shader；`CopyResource` 不暴露，downscaling compute shader 顺手做 depth → R32 的复制。最后 stream compaction 之后「填 indirect args buffer」这一步只能在 compute shader 里用 bgfx 的 `drawIndexedIndirect` helper 完成，因为 CPU 不能写。渲染阶段从原先的 *vertex pull*（shader 手动按 VertexID 访 typed buffer）切回 *vertex push*（走 IA offset）——作者自述是出于简化考虑。材质系统做了一个最小的调色板 demo：每个 prop 有 Material ID，通过**塞进 per-instance world transform 的空位**避免新开一个 vertex stream。作者对 bgfx 的评价很正面，认为去掉了 toy-engine 的杂乱之后，这段技术的可读性提高了；shader 迭代体验稍差，因为需要外部工具编译。

## 关键要点

- bgfx 不支持 structured buffer，需要用 vertex/index buffer 加 `COMPUTE_READ_WRITE` flag 替代。
- 不支持 CPU 写 indirect buffer、不支持 null pixel shader、不支持 `CopyResource`——均有对应的 workaround。
- Occlusion pass 四步结构不变：rendering occluders → HZB mip chain → 遮挡测试 + stream compaction → indirect draw。
- 材质 ID 塞进 per-instance world matrix 的空位，是一个非常紧凑的 trick，避免开新 vertex stream。
- 从 vertex pull 切回 vertex push：bgfx 下 VertexID 手动 fetch 的方案不如 IA offset 直观；代价是失去了 AMD GCN 上的潜在收益。
- 跨 API 移植的总体感受：**bgfx 把抽象做得足够干净，但跨平台的最大公约数导致某些 DX11-specific 的「直写」方案必须绕路**。

## 链接到的概念

- [[gpu-based-occlusion-culling]]
- [[multidraw-indirect-occlusion-culling]]
- [[stream-compaction]]
- [[indirect-draw]]
- [[hierarchical-z-buffer]]
- [[rendering-api-depth]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2018/03/05/porting-gpu-driven-occlusion-culling-to-bgfx/
- 本地：`raw/articles/interplayoflight.wordpress.com/2018-03-05_porting-gpu-driven-occlusion-culling-to-bgfx.md`
