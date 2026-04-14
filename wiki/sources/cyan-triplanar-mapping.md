---
tags: [source, shader, shadergraph, uv, 纹理]
date: 2026-04-14
sources: 1
---

# World Space UVs & Triplanar Mapping（Cyan）

[[cyanilux|Cyan]] 2020 年 1 月发表的 Shader Graph 教程，先讲用 **Position 节点**取代 mesh UV 通道做世界坐标平面映射，再过渡到 **Triplanar Mapping**——按法线方向混合三次平面投影解决垂直面拉伸问题。

## 摘要

文章先讲世界空间 UV 的最简版本：`Position`（World 空间）的 X、Z 分量直接当 `Sample Texture 2D` 的 UV，得到从 Y 轴投影的「贴图从天上压下来」效果。这种方式让多个独立 mesh 共享同一张贴图时无缝拼接（位置/旋转/缩放都不影响），适合水面、地形、墙面等需要「跟着空间走而不是跟着物体走」的场景。注意 URP 的 `World` 和 `Absolute World` 是同一个；HDRP 的 `World` 是 camera-relative，会让贴图跟相机飘，必须用 `Absolute World`。

世界空间 UV 在 3D 物体上的明显缺陷是**垂直于投影方向的面会被拉伸成条纹**——立方体的四个侧面就是典型反例。**Triplanar mapping** 是解法：从 X、Y、Z 三个方向各做一次平面投影，按法线方向加权混合：

```
blend = pow(abs(Normal), k); blend /= dot(blend, 1)
Out = sampleX * blend.x + sampleY * blend.y + sampleZ * blend.z
```

Shader Graph 自带 Triplanar 节点，但只接受一个纹理输入；想要不同轴用不同贴图（顶面草、侧面石），要么重新搭 graph 用三个 `Sample Texture 2D` + 法线 mask + Lerp，要么写 Custom Function。文章给了两种实现的完整 graph 截图和一份 8 行的 HLSL Custom Function。Custom Function 路径有个 Shader Graph 限制：传进去的 `Texture2D` 拿不到原本的 `SamplerState`（Filter / Wrap mode），必须额外传一个 `SamplerState` 输入，留空就用默认 Linear + Repeat。

文章末尾提醒：triplanar 是「采样次数三倍」的代价，再加 normal map / metallic / roughness 各一份 triplanar，shader 性能很快爆炸。如果只需要「Y 朝上 vs 其它」二分，更便宜的做法是单次 triplanar + 一次普通采样 + Lerp。

## 关键要点

- 世界空间 UV 最简版本：取 `Position(World).xz` 当 UV，多物体之间纹理无缝对齐。
- HDRP 的 `World` 是 camera-relative，必须用 `Absolute World` 否则贴图跟相机飘。
- Triplanar = 三次平面投影按 `pow(abs(N), k)` 加权混合；除以分量和归一化保持亮度。
- Shader Graph 内置 Triplanar 节点只支持单纹理；多纹理需要自己搭 graph 或 Custom Function。
- Custom Function 拿不到 Texture 自带的 SamplerState，必须额外传 SamplerState 输入。
- 性能代价：单层 triplanar 是 3× 普通采样，PBR 多层叠加后非常贵。

## 链接到的概念

- [[triplanar-mapping]]
- [[planar-mapping]]
- [[uv-manipulation-nodes]]
- [[normal-map-blending]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/01/28/worldspace-uvs-triplanar-mapping/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-01-28_world-space-uvs-triplanar-mapping.md`
