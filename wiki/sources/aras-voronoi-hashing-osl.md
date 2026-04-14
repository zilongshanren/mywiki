---
tags: [source, 渲染, 哈希, 程序化纹理, osl]
date: 2026-04-14
sources: 1
---

# Voronoi, Hashing and OSL（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2025 年 6 月的文章，记录他把 Blender 的 Voronoi/Worley 噪声节点底层哈希函数从 1997 年的 Jenkins Lookup3 换成 2020 年的 PCG3D 的过程。原本只是想给 Cycles 渲染器加点 SIMD，结果发现换哈希函数带来的收益远大于 SIMD，最终变成 Blender 5.0 的 Voronoi 节点 2-3 倍提速。

## 摘要

Voronoi（实际上是 Worley 噪声）节点的一次 3D 求值需要对周围 27 个格子计算伪随机偏移，也就是 27 次哈希。Blender 原本用 Jenkins Lookup3（1997 年）「假装」把 `float3` 和 `float4` 输入 hash 一遍再组合成 3D 输出，既慢又冗长。换成 PCG3D（Jarzynski & Olano 2020 的 JCGT 论文）后，一个函数直接吃 3 个 uint 吐 3 个 uint，整块代码干净得多且快 4 倍。接下来的改动要同时同步到 Cycles C++、EEVEE GLSL、Blender C++ compositor 三处——又发现测试里还有第四处：Open Shading Language（OSL）后端。OSL 居然**没有 unsigned int、也没有 float↔int 的 bitcast**，作者不得不把 PCG3D 改写成 signed int 版，并把 Voronoi 内部改成「直接哈希整数格子坐标」以绕开 bitcast。PR 被并入 Blender 5.0。副作用是确实改变了具体噪声图样——但行为等价，5.0 主版本号正好合适。

## 关键要点

- **1990 年代哈希函数的假设已过时**：当年为了规避昂贵的整数乘法而大量使用 shift/xor/add；今天的 CPU 和 GPU 上，整数乘法便宜得多，专门为 GPU 设计的 PCG3D 反而更快、更简洁。
- **PCG3D**（3D→3D 整数哈希）一次调用顶原来的三次 Lookup3，适合 Voronoi 这种「小格子大循环」的场景，是 [[non-cryptographic-hash]] 家族里针对 GPU 的代表作。
- **OSL 的数据类型局限**：在 2025 年仍然没有 unsigned int 和 bit cast；只能用 signed int 版本的 PCG3D（最后一步 `& 0x7FFFFFFF`），以及让 Voronoi 代码直接吃整数格子坐标。
- **一份算法四处实现**：Cycles C++（CPU+CUDA/Metal/HIP/oneAPI）、EEVEE GLSL、Blender C++ compositor、Cycles OSL 后端——需要四处同时同步，这是大型节点式着色系统的隐形复杂度。
- **更换哈希函数 ≠ 无副作用**：Voronoi 图案本身会变，但只要语义等价、在主版本号内切换即可被接受。
- 作者反讽：本来是来调 SIMD 的，最后根本没碰 SIMD。

## 链接到的概念

- [[non-cryptographic-hash]]
- [[pcg3d-hash]]
- [[worley-voronoi-noise]]
- [[shader-prototyping-tools]]

## 原文

- 链接：https://aras-p.info/blog/2025/06/13/Voronoi-Hashing-and-OSL/
- 本地：`raw/articles/aras-p.info/2025-06-13_voronoi-hashing-and-osl-aras-website.md`
