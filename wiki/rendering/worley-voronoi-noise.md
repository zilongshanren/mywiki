---
tags: [程序化纹理, 噪声, shader]
date: 2026-04-14
sources: 5
---

# Worley / Voronoi 噪声

**Worley 噪声**（Steven Worley, 1996）是程序化纹理里最常见的「细胞状」噪声之一。许多引擎和节点系统把它封装成 **Voronoi 节点**——Blender、Unity Shader Graph、Houdini、Substance 都是。它可以生成石板、龟裂、水面焦散、金属颗粒、泡沫、细胞组织等大量有机外观的底层纹理。

## 算法骨架

空间被分成均匀整数网格。每个格子内放一个伪随机「特征点」，着色点读取时：

1. 把当前位置 `p` 落到它所在的整数格子 `cell`；
2. 遍历相邻 3×3（2D）或 3×3×3（3D）或 3×3×3×3（4D）个格子；
3. 对每个邻居格子，用哈希函数由格子坐标生成一个 `[0,1]^n` 随机偏移，得到特征点位置 `f = neighbor + hash(neighbor)`；
4. 计算到各个特征点的距离，取最近（F1）、次近（F2）、或它们的差作为输出。

由此派生的常见变体有：F1（细胞中心到边界的距离场）、F2-F1（细胞边缘线）、Voronoi cells（按最近特征点 ID 染色）等。这也是一种低成本近似的 **Voronoi diagram** 栅格化，只看邻近几个格子所以能在 shader 里高速求值。

## 为什么哈希函数关键

3D 情况下，每个像素求值一次要跑 **27 次哈希**，这在 Cycles、EEVEE 这样的场景里直接主宰了噪声节点的开销。用 1997 年的 Jenkins Lookup3 还是 2020 年的 [[pcg3d-hash|PCG3D]]，实测相差 2-3 倍——也就是说，节点是否跑得起来，可能取决于哈希函数有没有换代。

## 与 [[layered-grid-noise]] / Perlin 的对比

- Perlin/Simplex 噪声是「梯度混合」型，结果连续光滑，看起来像云雾。
- Worley 是「距离场」型，结果天然带有断线、边缘、单元格结构，看起来像龟裂或细胞。
- 两者常叠加使用，或用 Worley 作为 mask/edge，Perlin 作为 body。

## 在节点式 DCC 里的实现隐形复杂度

Blender 的 Voronoi 节点需要在 **四处**同时维持行为一致：Cycles C++（编译到 CPU + CUDA/Metal/HIP/oneAPI）、EEVEE 的 GLSL、Blender C++ compositor/geometry nodes、以及 Cycles 的 Open Shading Language 后端。任何一次底层改动（比如换哈希函数）都要同步四份代码并让测试套件全绿——这是大型节点式着色系统的隐形工程成本。

## 相关

- [[pcg3d-hash]]
- [[non-cryptographic-hash]]
- [[layered-grid-noise]]
- [[sdf-2d-primitives]]
- [[cellular-texture-generation]] —— ryg 在 Werkkzeug3 里总结的**离线**细胞纹理生成：为什么树反而最慢，以及空间递归细分如何做到近似 O(|pixels|)
- [[cyanilux|Cyan]] 的 [Voronoi 教程](https://cyangamedev.wordpress.com/2019/07/16/voronoi/) 把 Unity Shader Graph 内置 Voronoi 节点的 30 行 HLSL 拆给入门者看，并给了两种 cell 边缘（F2-F1 与两次循环法）的 Custom Function 实现
- [[alan-zucconi]] 的 [To Voronoi and Beyond](https://www.alanzucconi.com/2015/02/24/to-voronoi-and-beyond/) 教程——用 Minkowski 距离统一 Euclidean/Manhattan，演示 shader 里 brute-force `_Points[100]` 数组 + O(N) 每像素扫描的朴素实现，并引用 Chris Wellons 的 cone projection 做 O(N) 的替代方案
- [[classic-shader-noise]] —— Xor 的 Mini: Noise 两篇把 Worley/Voronoi 和 value/Perlin/fractal 放在同一手写骨架下对比
- [[sources/danielilett-toolbox-urp-glitter]] —— Voronoi 噪声直接当 glitter 粒子排布：Spot Thresholds 用 smoothstep 把细胞切成圆斑或锯齿片，Noise Rotation Speed 让每个 cell 的随机向量随时间旋转以产生 sparkle 闪烁；glitter 可见性通过 Fresnel 门控

## Sources

- [[sources/aras-voronoi-hashing-osl]]
- [[sources/ryg-cellular-textures-1]]
- [[sources/ryg-cellular-textures-2]]
- [[sources/cyan-voronoi]]
- [[sources/alanzucconi-to-voronoi-beyond]]
- [[sources/xor-mini-noise-2]] —— Xor：Worley 的 3×3 邻域距离场写法，以及从 Worley 派生 Voronoi 的单处改动
- [[sources/danielilett-toolbox-urp-glitter]] —— Voronoi cell 作为 glitter particle 的位置排布
