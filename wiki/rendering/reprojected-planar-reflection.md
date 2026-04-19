---
tags: [渲染, ssr, 反射, 重投影, taa, motion-vectors, 时域]
date: 2026-04-19
sources: 1
---

# 反射的正确重投影（Reprojected Planar Reflection）

[[screenspace-reflections|SSR]] 一旦和 [[temporal-antialiasing|TAA]] 叠在一起就会冒出一类独特的麻烦：**反射是视角依赖的**，直接拿 shading point 的 [[motion-vectors|motion vector]] 去查历史帧，会得到"反射被糊成一条尾巴"的拖影——Uncharted 4 里地面反射的常见 artifact 就是这个。原因很直白：motion vector 描述的是 **shading surface 的投影运动**，反射目标（打到的另一个点）在屏幕上投影运动方向和大小**完全不同**。

## 正确做法的射线几何

Jp 在 Stingray 博客里给出了一张光线图的精确步骤，目标是把当前帧 shading point `v0` 上反射出来的点 `p0`，正确对应到上一帧那个 shading point `v1` 上反射出的点 `r`：

1. 用 `v0` 的表面 motion vector `ms` 把 shading point 投回上一帧位置 `ss_p0`，再用 **history depth buffer** 重建它的 view-space 位置 `v1`。
2. 用反射命中点 `p0` 的 motion vector `mr` 把反射目标投回上一帧位置 `ss_p1`，同样重建 view-space 位置 `p1`。
3. 用上一帧的 view 矩阵把世界法线变到上一帧 view-space，得到 `n1`。
4. 把相机位置 `eye` 和 `p1` **投影到以 `v1` 为支点、`n1` 为法线的平面**上（这就是上一帧的反射面局部切平面）。
5. 在这个平面上解出满足入射 / 反射关系的反射采样点 `r`。
6. 用上一帧 view-projection 矩阵把 `r` 投到屏幕空间，采样上一帧的反射缓冲。

核心工具是一个 `find_reflection_incident_point` ——它把两个点按"到平面的符号距离"反向加权求出平面交点，闭式解算。代码不到 30 行 HLSL。

**这条流程要求引擎持有两张"历史"**：history depth buffer（`TEX2D(input_texture5, ...)`）和上一帧 view / view-projection 矩阵。两者结合才能把屏幕空间坐标反解到上一帧的 world / view 空间——任何想做反射重投影、SS refraction 时域累积的工程都绕不开它。

## 更实用的妥协：多候选 + 最短向量

严格几何解的代价是两次 depth sample + 矩阵变换 + 平面交点，每像素几十 ALU。实际落地的第二版是一个有趣的启发式：**生成一组候选重投影向量，取长度最短的那个**。

候选包括：

- shading point 的 motion vector
- 反射命中点的 motion vector
- **视差修正后**的 shading motion vector
- 视差修正后的反射 motion vector

视差修正来自 Tomasz Stachowiak 2015 年 Siggraph 的 *Stochastic Screen-Space Reflections*：

```hlsl
float2 parallax_velocity =
    velocity * saturate(1.0 - total_ray_length * PARALLAX_FACTOR);
```

`total_ray_length` 越长，说明反射目标离 shading point 越远（在摄像机运动下投影位移更小），motion vector 要按比例缩掉。`PARALLAX_FACTOR` 是手动 tweak 的魔数，Jp 在博客里坦承"不敢保证它完全正确"。

"取最短向量"的直觉是：**最短的有效重投影就是最可能命中的重投影**。一个像素上所有候选向量的终点如果都落在深度 / 颜色相近的历史像素，那几乎肯定是同一个表面点，选最短的能最大化历史命中率并最小化 [[temporal-antialiasing|neighborhood clamping]] 的误差。

对于每像素多条射线的随机 SSR，还能把所有成功重投影向量做加权平均，进一步降噪。

## 和 SSR 的系统位置

SSR 里时域累积几乎是必须的，不然 ray march 本身的噪声会漫天飞。但简单 temporal 把"反射在镜子上被拖成尾巴"；严格几何重投影又太贵。所以 Jp 的两条路线分别对应：

- **"对"的版本**：history depth + prev VP 矩阵的反解，做离线参考 / 高端路线。
- **"够用"的版本**：多候选向量 + min 长度 + parallax factor，游戏里跑得起，效果接近。

这两种做法在 2017 年之后被 Frostbite、id Tech、CryEngine 各家独立实现，是实时反射 "TAA 化" 的公共基线。它也是 2020 年代 **ReSTIR 反射**、**ray-traced reflection denoising** 之前，纯屏幕空间能做到的极限。

## 相关

- [[screenspace-reflections]] — SSR 的三类先天缺陷 + 稳定化工具链
- [[temporal-antialiasing]] — neighborhood clamping / 历史复用
- [[temporal-supersampling]]
- [[motion-vectors]] — 本文的输入
- [[parallax-corrected-cubemap]] — 视差修正在 cubemap 一侧的同名思想
- [[hybrid-raytracing-pipeline]] — 硬件 RT 后的反射路线
- [[niklas-frykholm]]

## Sources
- [[sources/bitsquid-reprojecting-reflections]]
(already links to [[sources/bitsquid-reprojecting-reflections]] — no patch needed)
