---
tags: [source, 渲染, 法线贴图, 纹理混合]
date: 2026-04-14
sources: 1
---

# Blending in Detail（Stephen Hill & Colin Barré-Brisebois）

[[stephen-hill|Stephen Hill]] 与 Colin Barré-Brisebois 2012 年发表于 selfshadow.com 的技术短文，系统对比「如何把两张切线空间法线贴图混合」的多种方案，并提出作者们自己的 **Reoriented Normal Mapping（RNM）**。

## 摘要

法线是方向向量，不能像颜色一样通道独立地 lerp——但实践中很多引擎恰恰就在这么做。文章列了六种常见混合方法：Linear、Photoshop Overlay、Partial Derivative、Whiteout（AMD Ruby 用的）、UDN（Unreal 文档版）、Unity 基底版（Zioma 2012 GDC），比较它们在视觉和数学上的表现，特别关注三个性质：**几何意义清晰**、**处理单位元（平法线）**、**保持两张输入的强度不被压扁**。

Linear / Overlay 通道独立处理，本质不对；Partial Derivative 等价于「先转成高度偏导再相加」，对 material fade 合适但在斜面上细节被抹平；Whiteout / UDN 是实用的近似。Unity 用绕 x / y 轴各 $90^\circ$ 构造基矩阵，只有 $n_1 = \pm z$ 时才是正交的，偏离就崩塌。

作者提出的 RNM 用**最短弧四元数**把切线空间的 $[0,0,1]$ 旋到基础法线 $t$，再把细节法线 $u$ 应用这个旋转。代入 $s=[0,0,1]$ 化简后得到非常紧凑的 3 行 HLSL：`normalize(t*dot(t,u) - u*t.z)`——几何上干净、平法线是单位元、两张贴图的强度都被保留。SM3.0 上约 8 条指令，和 Unity 版本持平。文章附完整推导、WebGL 演示、RenderMonkey 工程和 GPU 优化代码。

## 关键要点

- **法线是方向不是颜色**：逐通道 lerp 会「flatten」掉两张贴图本身的 bumpiness。
- **Identity 测试**：一张平法线 + 一张真法线应该等于那张真法线——Linear / Overlay 都过不了这一条。
- **Reoriented Normal Mapping**：三行代码，最短弧四元数推导出来的紧凑形式。
- **Unity 基底退化**：`nBasis` 矩阵只在 $n_1 = \pm z$ 时正交，演示图里上半球均匀点集在基矩阵偏转时被压成一条直线。
- **指令成本大同小异**：Linear / UDN 约 5 条，Whiteout / PD 约 7 条，RNM / Unity 约 8 条——现代 GPU 上不是性能瓶颈。
- **注意 $z$ 符号**：RNM 输出不保证 $z\geq 0$，如果要压缩成两通道法线格式需要 clamp 并 renormalise。

## 链接到的概念

- [[normal-map-blending]]
- [[3d-rotation-math]]
- [[stephen-hill]]

## 原文

- 链接：https://blog.selfshadow.com/publications/blending-in-detail/
- 本地：`raw/articles/blog.selfshadow.com/2012-07-10_blending-in-detail.md`
