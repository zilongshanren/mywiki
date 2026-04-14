---
tags: [shader, shadergraph, uv, 纹理, 渲染]
date: 2026-04-14
sources: 2
---

# Triplanar Mapping（按法线方向混合三次平面映射）

**Triplanar mapping** 是 [[planar-mapping|平面映射]] 的自然扩展：用世界坐标的 `xz`/`xy`/`yz` 各做一次平面投影，然后按表面法线方向加权混合。它的存在是为了解决平面映射唯一一个致命缺陷——**垂直于投影方向的面会被拉成线**。一座立方体如果只用 `xz` 平面映射，顶面和底面看起来正常，四个侧面贴图会被压成竖条纹。Triplanar 用三次采样换一份「在任何朝向上都不糟糕」的结果。

## 数学骨架

把世界坐标 `P` 分别取 `(z, y)`、`(x, z)`、`(x, y)` 当 UV，采样三次纹理得到 `Cx`、`Cy`、`Cz`。混合权重来自表面法线 `N`：

```
blend = pow(abs(N), k)
blend /= dot(blend, 1)        // 归一化到和为 1
Out = Cx * blend.x + Cy * blend.y + Cz * blend.z
```

`abs` 是因为我们要让正反两个方向用同一份贴图（朝下和朝上的面共享 `xz` 投影）；`pow(., k)` 控制三个轴之间的过渡硬度——`k = 1` 是平滑过渡，`k = 4` 起就接近硬选；除以分量和是必须的归一化，不归一化整体亮度会随法线方向波动。

## Shader Graph 里的实现

Shader Graph 自带一个 **Triplanar 节点**，但只接受一个 Texture 输入——意味着三个轴用同一张贴图。这对程序化噪声、岩石/泥土地面足够，但限制了多纹理需求。如果想要顶面用草、侧面用石、底面用土，有两条路：

- **绕开内置节点**：在 Shader Graph 里手动连出 `Position * Tile`、三个 `Sample Texture 2D`、`Absolute(Normal Vector)` + `Power` + 归一化、最后 `Lerp`/加权 `Add`。这个图很大但完全透明。
- **写 Custom Function**：参数列表 `(TextureA, TextureB, TextureC, SamplerState, Position, Normal, Tile, Blend)`，HLSL body 复刻上面的数学。代码更紧凑，但有一个 Shader Graph 的限制——通过 Custom Function 传进去的 `Texture2D` 拿不到它原本的 `SamplerState`（也就是 Filter / Wrap mode），必须额外传 `SamplerState`，否则就用默认的 Linear + Repeat。

```hlsl
void MultitextureTriplanar_float(
    Texture2D TextureA, Texture2D TextureB, Texture2D TextureC,
    SamplerState Sampler, float3 Position, float3 Normal,
    float Tile, float Blend, out float4 Out
){
    float3 UV = Position * Tile;
    float3 W = pow(abs(Normal), Blend);
    W /= dot(W, 1.0);
    float4 X = SAMPLE_TEXTURE2D(TextureA, Sampler, UV.zy);
    float4 Y = SAMPLE_TEXTURE2D(TextureB, Sampler, UV.xz);
    float4 Z = SAMPLE_TEXTURE2D(TextureC, Sampler, UV.xy);
    Out = X * W.x + Y * W.y + Z * W.z;
}
```

## 折中：和真正的「顶部 vs 侧面」区分

如果只想区分「Y 朝上 vs 其它」，根本不需要完整的 triplanar——可以只做一次 triplanar（或者甚至一次普通采样）拿到一份 base color，再用 `Normal.y` 走 `Lerp` 在 base color 和草地纹理之间过渡。一次 triplanar + 一次普通采样 = 4 次纹理 fetch；完整 triplanar 三套贴图 = 9 次 fetch；前者性能好得多。

## 代价与陷阱

Triplanar 最大的问题是**采样次数变三倍**：单层 albedo 就够贵，再加 normal map / metallic / roughness 各一层 triplanar，数字飞快爆炸（一个 PBR 材质可能从 4 次采样涨到 12 次）。在低端设备和移动端，这是一个明显的性能选择题。Normal map 的 triplanar 还有额外的 [[normal-map-blending|RNM]] 复杂度——三个轴的法线不能直接加权平均，必须先 reorient 到世界空间。

URP 的 Position 节点 `World` 和 `Absolute World` 在 URP 里是同一个东西；但在 HDRP 里 `World` 是 **camera-relative** 的（精度优化），用它做世界空间映射会让纹理跟相机一起飘，必须改用 `Absolute World`。

## 适用场景

triplanar 的甜区是 **没有可用 UV** 或 **UV 拉伸严重**的情况：

- **程序化生成几何**：marching cubes / voxel meshing / dual contouring 出来的网格通常没有合适的 UV。
- **大尺寸地形 / 岩壁 / 雕塑**：UV 拉伸或缝隙难以避免。
- **多个独立物体共享同一外观**：用世界坐标 UV 让它们的贴图自然对齐。
- **粒子和有机形态**：[[worley-voronoi-noise|Voronoi 噪声]] 等程序化噪声配合 triplanar 可以无缝铺到任意形状上。

## 相关

- [[planar-mapping]]
- [[coordinate-spaces]]
- [[normal-map-blending]]
- [[uv-manipulation-nodes]]
- [[fragment-shader]]
- [[ronja-bohm]] —— 2018 年第 010 篇教程：手写 vertex/fragment 版 triplanar，含 object→world 法线的逆转置矩阵推导

## Sources

- [[sources/cyan-triplanar-mapping]]
- [[sources/ronja-triplanar-mapping]]
