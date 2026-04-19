---
tags: [unity, urp, terrain, shader-graph, splatmap, 渲染]
date: 2026-04-19
sources: 1
---

# Terrain Splatmap 与 Shader Graph 手工复刻

Unity 的 Terrain 在 URP 下长期缺官方 Shader Graph 支持（Terrain Shader Graph 排在 roadmap 上从 2021 拖到 Unity 6.3 才落地）。但 Terrain 和 shader 之间其实用的是**一套非常简单的 splatmap 约定**，手工在 Shader Graph 里复刻并不难，Ilett 的 Shader Graph Basics Part 11 给出了完整路径。

## Splatmap 的五张贴图

翻开 URP 的 `TerrainLit` shader，顶部「set by terrain engine」的 property 组里一共五张：

- **`_Control`** —— 一张 RGBA 四通道控制图，每个通道编码**一个图层在该点的权重**（R=layer0、G=layer1、B=layer2、A=layer3）。约定四个通道的和为 1，保证混合是归一化的。
- **`_Splat0` / `_Splat1` / `_Splat2` / `_Splat3`** —— 四个图层各自的 albedo 贴图（基础地形只支持四层，更多需要 `TerrainLitAdd` 多次 blend）。

核心逻辑就一行：

```
finalColor = Splat0 * Control.r + Splat1 * Control.g + Splat2 * Control.b + Splat3 * Control.a
```

在 Shader Graph 里 `Sample Texture 2D` 四次 splat + 一次 control，把 control 的四个通道拆出来各自乘 splat 的 RGBA，四条结果加起来喂 `Base Color` 就完成了——比 `TerrainLitPasses.hlsl` 里的 `SplatmapMix` 函数干净很多，缺失的只是 normal map blend（`NormalMapMix`），想要正常法线得再接四张 normal splat。

## Reference 名字必须完全对齐

Shader Graph 里要让 Terrain 系统**自动把数据塞进来**，每个 property 的 **Reference** 字符串必须和 `TerrainLit` 完全一致：带下划线前缀、数字紧跟字母——`_Control` / `_Splat0` / `_Splat1`（不是 `_Splat_0`）。Reference 字段不对的话 Unity 不会报错，但 Terrain 会静默把默认白贴图塞进去，调了半天发现没反应。同时这些 property **不必 Expose**——让 Terrain 系统写就行。

另外要勾上 **Use Tiling and Offset**，这样每一层 Terrain 图层在 Terrain 组件里改平铺尺寸时，Shader Graph 才会用到对应的 `_ST`。

## 基于法线 y 分量的自动岩石层

Ilett 再往上加了一步："在陡坡处自动画岩石"。思路非常简单：物体表面法线的 **世界空间 y 分量** 越接近 1，说明越水平（草/雪更合适），接近 0 说明是立面（画岩石）。

```
rockBlend = Smoothstep(normalStart, normalEnd, normalY)
splat0 = Lerp(rockTexture, grassTexture, rockBlend)   // A=rock, B=grass
```

两个 slider（`Normal Start` = 0.5、`Normal End` = 0.6）给出过渡边界，`Smoothstep` 的好处是在 edge1 和 edge2 之间自动插值，避免硬切。这一步把**艺术家手绘岩石层的成本直接省掉**——在 Terrain 上只需画草、沙、雪三层，陡坡自动覆盖岩石。

这个技巧不是 Unity Terrain 独有，任何有法线的 mesh 都能用——Breath of the Wild 式的 triplanar + 陡坡岩石也是同一思路的进化版。

## 相关
- [[world-scan-shader-effect]] —— Ilett 在同一张 terrain graph 上加的 emissive 扫描波
- [[shader-graph-lighting-primer]]
- [[custom-mask-shaders]]
- [[retro-rendering-techniques]]
- [[banjo-kazooie-vertex-color-terrain]] —— N64 风格的「顶点色即 splat」，比 `_Control` 贴图约定更暴力但零带宽

## Sources

- [[sources/danielilett-shader-graph-terrains]]
