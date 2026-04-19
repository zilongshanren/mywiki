---
tags: [渲染, GPU, 几何管线, 剔除, D3D12, mesh-shader]
date: 2026-04-14
sources: 1
---

# Meshlets 与 Mesh Shaders

Mesh shader 是 2018 年 NVidia Turing 先引入、后来 AMD RDNA2 跟进的几何管线演化。它把 **Input Assembler、Tessellator、Vertex/Domain/Geometry Shader** 这一长串固定功能单元砍掉，换成两个可编程阶段：**Amplification (Task) Shader** 和 **Mesh Shader**。内核想法是把老管线里那些"CPU 难以喂饱、IA 又不能绕过"的瓶颈交给 shader 代码直接处理。

## 为什么需要它

即便 GPU 变得越来越"宽"，固定功能部件（尤其是 Primitive Assembler 和 Input Assembler）仍然可能成为瓶颈。传统做法是**在 CPU 做 per-mesh 的 [[culling]]**——用包围盒或者 CPU occlusion([Intel Masked Software Occlusion](https://www.intel.com/content/www/us/en/developer/articles/technical/masked-software-occlusion-culling.html)) 把整个 mesh 剔掉。但 mesh 粒度太粗：[St Miguel](...) 场景里，一棵树可能就是**单个 mesh**，frustum 只要覆盖树的任意一角就全保留。

**Meshlet** 是把原始 mesh 再切成 32–128 顶点的小簇（Kostas 用的是 [meshoptimizer](https://github.com/zeux/meshoptimizer) 生成）。同一棵树被切成几十个 meshlet 之后，frustum 能把远离相机一侧的那半棵树全 cull 掉。

## 数据布局

meshoptimizer 为每个 mesh 输出三个 buffer：

- `mesh_vertices`：去重后的顶点索引（指向原始顶点 buffer）；
- `mesh_triangles`：每个 meshlet 的三角形索引（指向 `mesh_vertices`）；
- `meshlets`：每个 meshlet 的 vertex/triangle count 与 offset。

注意这里有一层**间接**：`mesh_triangles → mesh_vertices → 原 vertex buffer`。如果不想吃这层间接的带宽，可以为每个 meshlet 复制一份本地顶点流（冗余换连续）。原来的 index buffer 不再需要。

## Mesh shader 本体

它长得像 compute shader——有 threadgroup、有 `groupshared`，通过 `DispatchMesh()` 启动，每个 group 处理**一个 meshlet**。先调用 `SetMeshOutputCounts(verts, prims)` 声明顶点和三角形数量——**超出是 UB**（GPU 不保证 clamp）。然后分两个 phase：

1. **Vertex phase**：每个线程处理若干顶点（`VertLoopCount` 取决于 threadgroup vs meshlet vertex count），计算 position / normal / uv 写入 `verts[index]`；
2. **Triangle phase**：每个线程写若干三角形索引到 `tris[index]`，格式是 `uint3`。

一个**实测的坑**：为了防越界，很多示例写 `if (index < meshlet.VertCount) { ... }`。Kostas 发现这个分支在 RTX 3080 mobile 上因为 wave 内发散非常贵；改成 `index = min(index, VertCount-1)`（重复处理少量顶点）**把 2.78 ms 降到相同配置下的 2.78 ms，而 if-branch 版本是 3.36 ms**。对 divergence 的规避比重复计算重要。

## Threadgroup / meshlet 尺寸的三角权衡

DX12 spec 规定上限：最多 256 顶点、256 三角形、128 threads/group。实际调参要平衡：

- **meshlet 大→顶点复用高**（不用重复 shade）
- **meshlet 小→culling 效率高**（更细粒度丢弃）
- **threadgroup size 最好对齐 meshlet vertex count**，避免 vertex phase 阶段的线程浪费

Kostas 在 St Miguel 上的实测：

| 顶点 | 三角形 | 线程组 | 全 PS 成本 | 无 PS 成本 |
|---|---|---|---|---|
| 32 | 64 | 32 | 2.83 ms | 2.53 ms |
| **64** | **124** | **64** | **2.78 ms** | **2.46 ms** |
| 128 | 256 | 64 | 3.46 ms | 2.59 ms |
| 128 | 256 | 128 | 3.43 ms | 2.53 ms |

对照组：原 vertex shader 管线同视角是 2.87 ms / 2.42 ms。在这个 GPU+ 场景组合里，**64 顶点 / 124 三角形 / 64 线程**是甜点；再大就赔钱。NVidia 官方建议 64/126，AMD 建议 128/256——**没有普适值**，要 profile。

有意思的是 **depth-only pass**（无 PS 绑定）里，mesh shader pipeline **不管配置怎么选都比 vertex pipeline 慢**。这说明在几何瓶颈不明显的场景里，传统管线的固定功能单元仍然有优势。

## Amplification Shader 做 meshlet 剔除

真正能把 mesh shader 拉开差距的是加上 amplification shader (AS) 做 **per-meshlet 剔除**：

```hlsl
[NumThreads(32, 1, 1)]
void ASMain(uint dtid : SV_DispatchThreadID)
{
    bool visible = (dtid < MeshletCount) && IsVisible(MeshletCullData[dtid]);
    if (visible) {
        uint idx = WavePrefixCountBits(visible);
        g_Payload.MeshletIndices[idx] = dtid;
    }
    uint visibleCount = WaveActiveCountBits(visible);
    DispatchMesh(visibleCount, 1, 1, g_Payload);
}
```

每个 thread 处理一个 meshlet，计算可见性（frustum 包围球 / hi-z 遮挡 / cone backface），然后用 wave intrinsics (`WavePrefixCountBits` + `WaveActiveCountBits`) 压缩到 payload，传给下游 mesh shader。**不需要**像老的 compute + indirect 那样做 compaction pass——剔除和 dispatch 发生在同一次 wave 内。

meshoptimizer 的 `meshlet_computeMeshletBounds()` 会同时产出 bounding sphere 和 normal cone 用于背面 cluster cull。

## 性能收益

还是 St Miguel：

| 管线 | gbuffer (ms) | z-prepass (ms) |
|---|---|---|
| Vertex shader + 仅 CPU frustum | 2.87 | 2.41 |
| Mesh shader, 无 AS, 纯直通 | 2.78 | 2.46 |
| Mesh shader + AS frustum 剔除 | 2.43 | — |
| Mesh shader + AS frustum + hi-z occlusion | 1.64 | 1.24 |
| **同上，meshlet 换 32v/64tri** | **1.59** | — |

**gbuffer 降 44%、z-prepass 降 48%**——真正的胜利来自遮挡剔除，不是 mesh shader 本身。Bistro 场景同样配置降 30%，印证了收益高度依赖内容。

一个反直觉的点：**有了 AS occlusion 之后，meshlet 要尽量小**。虽然 32v/64tri 在 pass-through 模式里略差，但小包围球 → 更多 meshlet 被 hi-z 剔除 → 总成本反而是所有配置里最低的。

## GPU Trace 能看到的变化

Kostas 对 NSight 的分析揭示 mesh shader 的几条硬件路径：

- **Primitive Distributor (PD)** 吞吐几乎为零——被 bypass。
- **Vertex Attribute Fetch (VAF)** 完全不用。
- **VGT (Vertex-Tess-Geo)** 的 active warps/cycle 增加到约 **6×**。
- 但这同时给 **Inter-Stage Buffer Entry (ISBE) memory** 增加了压力——shaded 顶点数据要在更多的 warp 间流转，warp launch stall 变得更频繁。
- 最终 SM (Streaming Multiprocessor) 的 occupancy 与 unallocated warps 都朝好的方向移动。

VPC（clipping/culling）和 ZCULL（coarse z）的工作量显著下降——正是 AS 剔除的直接产物。

## 和已有方案的对比

Mesh shader 不是做 meshlet cull 的唯一方式：**Frostbite 在 GDC 2016 就演示过** compute shader + ExecuteIndirect 的等价管线。但 mesh shader 的优势是：

- 管线更简单（一次 pipeline state，不需要 indirect args buffer）；
- **不需要 compaction pass** 去压紧"空 drawcall"；
- 剔除结果直接以 payload 形式交给下游 mesh shader，**不走 memory roundtrip**、不需要 UAV barrier——这点和 [[d3d12-work-graphs]] 想解决的问题是同构的。

## 相关
- [[culling]] — frustum / occlusion / backface 的上位概念
- [[gpu-based-occlusion-culling]] — Kostas 把 hi-z occlusion 移植到 mesh shader 的前身
- [[multidraw-indirect-occlusion-culling]] — compute shader 路径的先驱
- [[hierarchical-z-buffer]] — AS 遮挡剔除依赖的数据结构
- [[compact-vertex-format]] — meshlet 本地化需要考虑的顶点压缩
- [[d3d12-work-graphs]] — 同样想取消 indirect/barrier 循环的新机制
- [[bottleneck-analysis]] — 判定 PD/VAF 是不是真正的瓶颈
- [[vertex-shader-export-bottleneck]] —— 传统 VS export 路径的 ISBE/PE/TRAM 成本，是改 mesh shader 的动机之一
- [[variable-sized-work-pattern]] —— AS 剔除里 `WavePrefixCountBits + WaveActiveCountBits` 是同类
- [[mesh-shader-vulkan-hlsl-per-primitive]] — HLSL + Vulkan 下 PerPrimitiveEXT 必须手动补的恶性跨厂商坑

## Sources

- [[sources/interplay-meshlets-mesh-shaders]]
