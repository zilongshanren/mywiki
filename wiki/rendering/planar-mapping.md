---
tags: [渲染, shader, uv, 纹理, unity]
date: 2026-04-14
sources: 1
---

# 平面映射（Planar Mapping）

**Planar mapping** 是最简单的一种**程序生成 UV**：直接把顶点位置的两个坐标分量（例如 `xz`）当成 UV 用。它回答的是「我没有 UV，或者我想忽略模型自带的 UV，怎么给这张贴图一个合理的映射方式」这类需求，也常常是更高级映射技术（triplanar、decals、屏幕空间映射）的起点。

## 问题来源

Unity 的 mesh 导入之后通常带一组 UV，但并不是所有情况都能直接用：

- **程序化生成的几何体**没有 UV（例如 marching cubes、体素 meshing、procedural meshes）。
- **多物体希望共享同一张贴图**且无缝拼接——模型各自的 UV 空间不相关，简单 tiling 无法对齐。
- **地形、墙面**这种大面积平面，希望贴图按世界尺寸 tile，而不是按物体大小缩放。
- **贴花、印花效果**需要在表面上「投影」一张图片，而不是沿着原 UV 铺开。

Planar mapping 给最后几类问题一个最简答案：**把世界坐标（或局部坐标）的某两个分量当 UV**，映射就从「跟着模型走」变成「跟着空间走」。

## 三个阶段

Ronja 的教程把 planar mapping 分成三个循序渐进的版本：

1. **局部坐标 planar**：在顶点着色器里用 `v.vertex.xz` 作为 UV。贴图像是从头顶压下来贴到模型上。好处是简单，缺点是模型移动 / 旋转时贴图会跟着模型一起转动——因为 UV 坐标本身在物体的局部空间里。
2. **加上 TRANSFORM_TEX**：让材质面板的 tiling/offset 生效。Unity 的 `TRANSFORM_TEX(uv, _MainTex)` 宏会读取 `_MainTex_ST` 并做 `uv * ST.xy + ST.zw`——这其实是所有 shader 的标准动作，不写就无法响应 inspector 里的缩放设置。
3. **世界坐标 planar**：`mul(unity_ObjectToWorld, v.vertex)` 先把顶点变到世界空间，再取 `xz`。此时贴图就钉在世界上了，移动物体相当于从贴图「窗口」后面滑过去——这是大多数地形 / 墙面应用要的行为。

## 局限与延伸

planar mapping 最明显的问题是 **垂直面会被拉伸**：如果贴图垂直于平面方向（例如 `xz` 映射下的竖直墙面），一整条 UV 会被压缩成一条线，贴图变成拉长的条纹。解决办法有几种：

- **Triplanar mapping**：从 X、Y、Z 三个方向各做一次 planar 映射，然后按法线方向做加权混合。法线朝上用 `xz`，朝前用 `xy`，朝侧用 `yz`，缝隙处自然过渡。这是地形 shader 的标配。
- **Box mapping**：triplanar 的简化版，只按法线主方向选一个轴。
- **程序化替代**：如果本质上只是需要「空间中一致的噪声」，用 noise 函数替代采样贴图更灵活。

planar mapping 还是 [[sdf-2d-primitives|2D SDF]] 教程的前置——SDF 示例里直接取 `worldPos.xz` 当 2D 坐标，本质就是一次退化版 planar mapping。

## 相关

- [[coordinate-spaces]] —— 局部 / 世界 / 裁剪空间的区分
- [[mvp-transform]]
- [[fragment-shader]]
- [[sdf-2d-primitives]] —— 用世界坐标喂 SDF 函数
- [[normal-map-blending]] —— triplanar 中不同方向采样的法线合并
- [[triplanar-mapping]] —— 三轴投影 + 法线加权混合，解决平面映射在垂直面上的拉伸

## Sources

- [[sources/ronja-planar-mapping]]
