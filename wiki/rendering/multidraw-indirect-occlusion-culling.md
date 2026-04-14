---
tags: [渲染, gpu-driven, 剔除, multidraw, 批量绘制, dx11, mesh-lod]
date: 2026-04-14
sources: 1
---

# MultiDrawIndirect + Mesh LOD 的 GPU-driven 剔除

[[gpu-based-occlusion-culling|GPU 侧遮挡剔除]] 第一篇文章解决了「让 visibility 和 draw 全留在 GPU 上」——但留下两个明显的缺口：

1. **每个 prop mesh 仍需一次 `DrawIndexedInstancedIndirect`**——因为 DX11 原生没有 `MultiDrawInstancedIndirect`。
2. **完全没有 mesh LOD**——真实游戏里大量 mesh 会有 2–4 级 LOD，这是最基本的顶点 shader 成本优化。

[[kostas-anagnostou|Kostas Anagnostou]] 2018 年初的 Part 2 同时补掉这两个洞，代价是一系列 DX11 特有的 workaround。

## 用 NVAPI 撕开 DX11 的限制

`MultiDrawIndexedInstancedIndirect` 在 DX11 里不是 first-class，但 NVidia 和 AMD（不包括 Intel）通过 **IHV driver extension** 暴露出来：

```cpp
NvAPI_D3D11_MultiDrawIndexedInstancedIndirect(
    ctx, drawCount,
    argsBuffer, 0, 5 * sizeof(UINT));
```

Args buffer 的格式没变，仍然是 **每 drawcall 5 个 `UINT`**（IndexCountPerInstance / InstanceCount / StartIndexLocation / BaseVertexLocation / StartInstanceLocation）——MultiDraw 只是把「调 N 次」压成「调一次、循环 N 次」。Intel 不支持这条扩展时，作者明确给出了 fallback：就退回到 for-loop 里调 `DrawIndexedInstancedIndirect`——反正大量收益不在 draw 本身，而在**去掉了 draw 之间的 state setup**。

## 真正的重头戏：批量化（batching）一切

用 MultiDraw 的前提是整个场景的所有几何数据**放在同一组 buffer 里**。这意味着：

- **单一全局顶点 buffer**（per attribute：position / normal / uv 分别一个 typed buffer）。
- **单一全局 index buffer**（仍然保留常规 index buffer，为了保住 post-transform vertex cache——这是 typed buffer vertex fetch 做不到的）。
- **单一全局 instance buffer**（SoA 存 per-instance data）。
- **texture arrays** 按「所有 albedo 一组、所有 normal 一组」的思路组织——上限 2048 entries 要记牢。
- **constant buffer 做成数组**，用 mesh ID 索引；上限 4096 float4，溢出就转 structured buffer。

每个 drawcall 只保留**偏移量 + 计数**，所有真正的 state setup 都已经在 pipeline 外面完成。这也是为什么作者即便在 Intel fallback 路径上仍然建议走这条路——**绝大部分 draw 成本本来就是 setup 开销**，批量化把这些开销压成常量。

## 动手取顶点：programmable vertex fetching

因为所有 attribute 都以 typed buffer 形式存在，vertex shader 不能依赖 Input Assembler 的 offset——需要自己按 `SV_VertexID + vertexBufferOffset` 手动访存：

```hlsl
float3 pos = Positions[vertexIndex + vertexBufferOffset].xyz;
```

这叫做 **programmable vertex fetching**（[forum.beyond3d](https://forum.beyond3d.com) 和 Turánszki 都记录过这条路线），它的副作用很有意思：

- **GCN 上吞吐量更好**（NVidia 上收益模糊）。
- 可以根据距离 / 材质**动态决定是否采样 tangent**——远处不需要法线贴图就不要读 tangent buffer，省下 ALU 和带宽。
- 可以在 index buffer 里「偷位」存 per-vertex 的第二条 attribute 频率，比如要硬边时在同一个顶点上存多条法线。

## 最难的问题：DrawcallID 从哪来？

`MultiDrawIndexedInstancedIndirect` 在 OpenGL 里有 `gl_DrawID`——在 DX11 里**没有**。每个 drawcall 的 arguments 都写在同一个 buffer 里，但 shader 端拿不到「我现在是第几个 drawcall」这个关键信息，于是无法索引到自己这个 mesh 的材质常量。

Anagnostou 走的是一条颇为曲折的路，记录下了三种方案：

1. **把 DrawcallID 塞进 index buffer**——把 32-bit index 拆成 16+16：一半存 vertex index、一半存 drawcall ID。能用，但 index buffer 成本翻倍，而且要求 index 频率足够（每个 index 都能拿到正确的 drawcall ID）。附带一个合理的变体：如果实际 index 范围只需要 24 bit，拆成 24+8 是可以接受的。
2. **最终方案：塞进 instance buffer**——instance 频率比 vertex 粒度小得多。新建一个 16-bit 的 vertex buffer（按 instance step rate），走 Input Assembler 绑定。这样 `StartInstanceLocation` 在 args 里能正常生效，每个 instance 自己就知道 draw ID。这个 buffer 在 compute shader 做 stream compaction 的时候通过 UAV 写入——必须和 instance data 同步更新。

这个迂回方案的本质是：**DX11 IA + args buffer 对 instance 级别数据的支持是最完整的**，而 shader-manual 的方案总会缺一环。作者花了非常多篇幅讲清这一点，是全文最有 retrofit 味道的一段。

## Mesh LOD 怎么挂进来

LOD 的接入出乎意料地简洁：**每个 mesh LOD 当成一个独立 drawcall**——因为每个 LOD 的 vertex / index count 都不同，放进同一个 args buffer 里既自然又无需 padding。

实现细节：

- 所有 LOD 的 vertex / index data 都进全局 buffer，以 offset 区分。
- Instance data 按 **per-mesh-LOD 分组**——同一个 mesh 的 instance 分散在不同 LOD 的 slot 里，因为 draw 按 LOD 分别发射，每段 draw 需要连续的 instance 区域。
- 这带来一个副作用：**全局 instance 无法跨 mesh 按距离排序**（排序只在单 mesh 单 LOD 内部做）——这其实是 `DrawInstanced` 家族的共通限制。
- 某个 mesh 的某个 LOD 上没有任何 visible instance 时，它对应的 drawcall 变成**空 draw**，这是允许的——空 draw 在 MultiDraw 里几乎没有代价。
- 用一个 packed ID 同时编码 **meshID + lodID**，这样 material constant 可以按 mesh 粒度索引，而 LOD 粒度用于选择几何偏移。

## 「撤掉 NVAPI 还值得吗？」

文章最后自己问了一遍这个问题，答案是**绝大多数情况下 yes**：

> 即便 Intel 上必须退回到 for-loop 里调 N 次 DrawIndexedInstancedIndirect——**draw 本身的成本远不如 state setup 的成本**。batching 把所有 buffer、texture、shader 和 constant 的 state 切换都消掉了，这才是主要收益；MultiDraw 只是锦上添花。

这个结论和 [[batching]]、[[draw-call]] 的主线是一致的：2018 年前后很多 DX11 引擎都走过这条路——把所有 GPU state 压到最少、只剩 indirect args 和 instance data 两个 dynamic buffer 在走。

## 和 Part 1 的关系 / 后续

这是 Anagnostou GPU-driven 系列的**第二段**。Part 1（[[gpu-based-occlusion-culling]]）把 HZB + stream compaction 落地；本篇补 MultiDraw + LOD；之后 Part 3 把整套方案移植到 bgfx（换 API 验证），再之后 Digital Dragons 大会版把 instance 数推到 20K 做实测 profiling。Marco Giordano 的 [[gpu-driven-grass-tiles]] 就直接基于这条工作流。

## 相关

- [[gpu-based-occlusion-culling]] —— Part 1，HZB + stream compaction
- [[occlusion-culling]]
- [[stream-compaction]]
- [[batching]]
- [[draw-call]]
- [[indirect-draw]] —— `DrawIndexedInstancedIndirect` 家族
- [[bindless-rendering]] —— 更激进的绑定方案，最终目标方向
- [[gpu-driven-grass-tiles]] —— 引用本文技术的草地 demo
- [[compact-vertex-format]] —— packed attribute 的另一个案例
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-multidraw-indirect-occlusion]]
