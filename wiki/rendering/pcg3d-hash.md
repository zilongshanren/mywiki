---
tags: [哈希, 程序化纹理, gpu, 噪声]
date: 2026-04-14
sources: 1
---

# PCG3D 哈希（GPU-friendly 3D→3D integer hash）

**PCG3D** 是 Mark Jarzynski 和 Marc Olano 在 JCGT 2020 年的论文《Hash Functions for GPU Rendering》中为 GPU 渲染场景挑选并推荐的整数哈希函数。它一次性吃进 `uint3`、吐出 `uint3`，是典型的「小输入、高频次、SIMD/GPU 友好」哈希，专门针对现代 GPU 上整数乘法廉价的假设而设计，是 [[non-cryptographic-hash]] 家族里面向渲染流水线的代表之一。

## 核心代码

```c
uint3 hash_pcg3d(uint3 v) {
  v = v * 1664525u + 1013904223u;
  v.x += v.y * v.z;
  v.y += v.z * v.x;
  v.z += v.x * v.y;
  v = v ^ (v >> 16);
  v.x += v.y * v.z;
  v.y += v.z * v.x;
  v.z += v.x * v.y;
  return v;
}
```

寥寥几行包含两次「mul-add-xor-shift」混合：先做 LCG 推进，再用「分量相互乘加」让三个通道交叉污染、最后统一 xor-shift 做雪崩。算法对 GPU 流处理器和现代 CPU 都友好——没有表、没有分支、没有非对齐读。

## 和老式哈希的对比

和上一代常用的 Bob Jenkins **Lookup3**（1997）相比，PCG3D 的优势很直接：

- Lookup3 为了避开昂贵乘法大量使用 shift/xor/rotate，代码又臭又长；PCG3D 把「廉价的整数乘法」当作一等原语，短且快。
- 要算 3D 哈希时 Lookup3 需要「拼三次」（`hash(x,y,z)`、`hash(x,y,z,1)`、`hash(x,y,z,2)`），PCG3D 一次搞定。
- 在现代 CPU 上实测大约快 4 倍（[[aras-pranckevicius]] 在 Blender Voronoi 节点上测得）。

这是哈希函数设计假设随硬件变迁的典型案例：「1990 年代的哈希函数」今天往往既慢又丑。

## 经典应用：[[worley-voronoi-noise]] / Voronoi 节点

Worley 噪声要对周围 27 个格子（3D 情况）各算一次伪随机偏移，3D→3D 哈希恰好是需要的形态。Blender 5.0 就把 Voronoi 节点底层从 Lookup3 换成了 PCG3D，获得 2-3 倍性能提升（但 Voronoi 图样本身发生了可见变化，这也是等到 5.0 主版本号才切换的原因）。

## 在 [[open-shading-language-limits|OSL]] 里的变体

Open Shading Language 在 2025 年仍然**没有 unsigned int、也没有 float↔int bitcast**。PCG3D 可以用 signed int 照抄一份，最后一步 `& 0x7FFFFFFF` 去掉符号位即可；Voronoi 再把输入从 `float3 cell` 改成 `int3 cellCoords` 绕开 bitcast。代价是必须把 Voronoi 内部逻辑一起改成吃整数格子坐标。

## 相关

- [[non-cryptographic-hash]]
- [[worley-voronoi-noise]]
- [[rapidhash]]
- [[shader-prototyping-tools]]

## Sources

- [[sources/aras-voronoi-hashing-osl]]
