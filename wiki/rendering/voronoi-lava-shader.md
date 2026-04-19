---
tags: [渲染, shader, voronoi, 程序化材质, 风格化, unity]
date: 2026-04-19
sources: 1
---

# Voronoi Lava Shader（两层纹理按 Voronoi 边距分配）

Voronoi Lava 是一个把两套 PBR 贴图按 **[[worley-voronoi-noise|Voronoi]] 细胞边界**分层的程序化材质模板——典型用途是**发光熔岩**（暗岩块 + 亮裂缝），但同一算法也能做干涸河床、蛋壳裂纹、玻璃碎裂、细胞组织。核心不在 PBR 部分，而在**"到 cell 边的距离"这一特殊量的用法**。

## 为什么需要"到边距离"

Shader Graph 内建 Voronoi 节点输出的是**"到最近 cell 中心的距离"**——这是生成点状花纹或散点的好用量，但画不出"裂缝"，因为"中心"和"边"在空间上不重合：中心附近距离最小，边上距离较大，但 cell 间的夹角处距离会突然跳变。想把 mask 画在"cell 与 cell 之间"的薄带上，需要另一种量：**到两个最近中心的距离差的绝对值**，或直接的**像素到最近 cell 间边界的距离**。Ilett 的 Shader Toolbox 通过自定义的 **Better Voronoi** [[danielilett-toolbox-urp-subgraph-library|subgraph]] 暴露这第二个输出，才能构造 Lava shader。

## 合成公式

有了"到边距离" `d_edge`，分层逻辑是一个 `smoothstep`：

```hlsl
float mask = smoothstep(Thickness - Falloff, Thickness, d_edge);
// mask = 1 → 在 cell 内部（Layer 1，熔岩岩块）
// mask = 0 → 在 cell 边上（Layer 2，发光裂缝）
float3 albedo = lerp(Layer2.albedo, Layer1.albedo, mask);
float3 normal = lerp(Layer2.normal, Layer1.normal, mask);
// ...同理 metallic / smoothness / emission / AO / heightmap 全部 lerp
```

两个关键参数：

- **Thickness** 控制 mask = 0 的区域宽度——裂缝有多宽，直观对应"熔岩流中的发光部分占多少"
- **Falloff** 是两层间 smoothstep 的过渡宽度——Thickness 是硬阈值、Falloff 决定阈值两侧多宽区间做渐变。Falloff → 0 得到锐利边（像碎玻璃），Falloff 较大得到平滑过渡（像粘稠熔岩）

## 两层都是完整 Lit 材质

Voronoi Lava 没有把 Layer 2 简化为纯色或单张纹理，而是让**两层都暴露完整的 PBR 参数表面**（Base Color + Texture、Metallic/Specular、Smoothness、Normal Map、Heightmap、AO、Emission）。这是它比朴素"两张贴图混色"强的地方：

- 岩块层 (Layer 1) 用低 emission + 普通 normal map
- 熔岩层 (Layer 2) 用高 emission color + 不同的 normal map（可以用法线图做流动感）+ 更高的 smoothness

结果是裂缝区域自然发光、粗糙度和法线都与岩块不同。两层共享 Base Texture 的 tiling/offset（避免两层错位），但其他贴图独立。

## 动画化

静态 Voronoi 是瓷砖花纹，动起来才像熔岩：

- **时变 UV**：给 Voronoi 的 input 坐标加 `_Time.y * velocity`，让 cell 缓慢漂移——得到流动的熔岩
- **时变 Thickness**：用 `sin(_Time.y * f)` 轻微调制 Thickness，裂缝宽度周期性呼吸
- **Emission 脉动**：Layer 2 的 emission intensity 叠一个 perlin noise × _Time.y

不过 Voronoi 节点在坐标变化时会有**瞬时 cell 重组**造成的跳变伪影（中心位置会突然切换到另一个最近中心）——缓解手段是把 Voronoi 密度降低 + 使用 jittered 坐标而非线性偏移，或引入一个极低频的 domain warp 把跳变抹平。

## 不止 Lava

同样的"两层 + 到边距离 mask"结构可以换皮：

- **干涸河床**：Layer 1 = 干土、Layer 2 = 深黑缝（Thickness 小、Falloff 0）
- **蛋壳/陶瓷裂纹**：Layer 1 = 瓷釉、Layer 2 = 透明（用 alpha clip）
- **玻璃碎裂**：Layer 2 = 高 smoothness 的反射面
- **细胞壁 / 有机组织**：Layer 1 = 细胞质、Layer 2 = 发光细胞壁（emission）
- **龟裂金箔**：Layer 1 = 金、Layer 2 = 暗底 + 额外法线

本质是把 **Voronoi 细胞分区**当作**两个任意 shader 的混合 mask**，这一抽象思路在 [[worley-voronoi-noise]] 原条目里已有铺垫，但 Voronoi Lava 是它最成熟的成品化示例。

## 相关

- [[worley-voronoi-noise]] —— Voronoi 的数学基础
- [[danielilett-toolbox-urp-subgraph-library]] —— Better Voronoi subgraph 的来源
- [[cellular-texture-generation]] —— 同类 cell 系程序化纹理
- [[classic-shader-noise]]
- [[physically-based-shading]]
- [[fractal-texturing]]

## Sources

- [[sources/danielilett-toolbox-urp-voronoi-lava]]
