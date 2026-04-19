---
tags: [source, unity, urp, shader, voronoi, 程序化材质]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Voronoi Lava（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Voronoi Lava** 参数手册——一个把两层 PBR 纹理按 Voronoi cell 到边距离交织的程序化材质。

## 摘要

Voronoi Lava 的核心观察：把一张 [[worley-voronoi-noise|Voronoi]] 划分结果当作**两层纹理的 mask 分配器**——cell 中心附近走第一层贴图（熔岩块），cell 之间的边界区域走第二层贴图（发光裂缝）。这一步依赖 Shader Toolbox 的 **Better Voronoi** subgraph 输出「到 cell 间边距离」而非默认 Voronoi 节点的「到中心距离」。参数分四段：*Surface Options* 与 [[danielilett-toolbox-urp-base-lit|Base Lit]] 共享（Metallic/Specular workflow、Opaque/Transparent、Render Face、Alpha Clip、Receive Shadows）；*Voronoi Properties* 四旋钮控制分层形态——*Voronoi Density*（cell 密度）、*Voronoi Angle Offset*（cell 生成参数，正值避免退化）、*Voronoi Thickness*（边缘带宽度，直接决定 Layer 1/Layer 2 像素比例）、*Voronoi Falloff*（两层之间平滑过渡区宽度）；*First Layer / Second Layer Properties* 是完整的 PBR 参数表面（Base Color + Base Texture、Metallic 或 Specular Color、Smoothness + Convert From Roughness、Normal Map、Heightmap、AO、Emission Color），两层几乎对称——本层的 tiling/offset 跟随 Base Texture。典型用法：Layer 1 暗岩石 + 低 emission、Layer 2 亮熔岩贴图 + 高 emission，就得到发光的熔岩纹路。

## 关键要点

- **核心算法就一个合成表达式**：`mix(Layer1, Layer2, smoothstep(Thickness - Falloff, Thickness, distToEdge))`
- Thickness / Falloff 分两档控制：Thickness 决定"裂缝有多宽"，Falloff 决定"裂缝和岩石边界硬不硬"
- 两层都是完整 Lit 材质而不是 albedo 颜色——意味着 normal/heightmap/AO/emission 都能各走一张贴图，适合写实熔岩流
- Density 增加会让 cell 变小变碎，但也会加大纹理反复度——动画化（随时间偏移 Voronoi 坐标）可以模拟流动
- 依赖 [[danielilett-toolbox-urp-subgraph-library|Better Voronoi subgraph]] 提供 "distance to edge" 输出；这是它与 Shader Graph 内建 Voronoi 节点的关键差异
- 从 [[voronoi-lava-shader]] 出发还可衍生：干涸河床（颜色/粗糙度反转）、蛋壳裂纹（Layer2=透明边）、玻璃碎裂（Layer2=镜面高 smooth）

## 链接到的概念

- [[voronoi-lava-shader]]
- [[worley-voronoi-noise]]
- [[physically-based-shading]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/voronoi-lava/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-voronoi-lava.md`
