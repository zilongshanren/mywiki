---
tags: [渲染, 法线贴图, 纹理混合]
date: 2026-04-14
sources: 1
---

# 法线贴图混合（Normal Map Blending）

**如何把两张切线空间法线贴图合成为一张**——是材质系统里反复出现的小问题：把基础法线和细节法线叠加、在不同材质之间过渡、做皱纹 / 局部形变。核心困难是**法线是方向向量，不能像 albedo 一样通道独立地 lerp**，否则会抹平两张贴图本身的强度、并在「一张是平法线 $[0,0,1]$」的退化情况下得到错误答案。

[[stephen-hill|Stephen Hill]] 和 Colin Barré-Brisebois 2012 年的 *Blending in Detail* 对这个问题做了系统比较，提出了**Reoriented Normal Mapping**（RNM）。

## 常见方案与它们的问题

| 方法 | 核心运算 | 毛病 |
|---|---|---|
| **Linear** | `normalize(n1 + n2)` | 类似求平均，两张贴图的强度都被拉平；平法线不是单位元 |
| **Overlay** | Photoshop overlay 公式 | 通道独立处理，本质上和 linear 一样没有几何依据 |
| **Partial Derivative (PD)** | `(n1.xy*n2.z + n2.xy*n1.z, n1.z*n2.z)` | 等价于把两张法线转成高度场的偏导再相加；对 material fade 友好，但细节在斜面上被压扁 |
| **Whiteout** | `(n1.xy + n2.xy, n1.z*n2.z)` | AMD Ruby 演示里用的简化版，细节保留好；几何意义有点模糊 |
| **UDN** | `(n1.xy + n2.xy, n1.z)` | Unreal 文档版本，最便宜，平坦基底上会损失细节 |
| **Unity (2012)** | 用基底旋转矩阵乘 `n2` | 当 $n_1$ 偏离 $\pm z$ 时基矩阵不再正交，退化 |

## Reoriented Normal Mapping

思路：把细节法线当作「定义在切线空间里的向量」，用一个**把 $[0,0,1]$ 旋转到基础法线 $t$** 的最短弧四元数把它重定向，使细节跟随基础法线的朝向。这正是切线空间法线变换到物体 / 世界空间时已经在做的事。

用最短弧四元数 $\hat q = [s\times t, s\cdot t + 1]/\sqrt{2(s\cdot t + 1)}$，代入 $s=[0,0,1]$ 化简后得到一个非常紧凑的 GPU 版本：

```hlsl
float3 t = tex2D(texBase,   uv).xyz * float3( 2,  2, 2) + float3(-1, -1,  0);
float3 u = tex2D(texDetail, uv).xyz * float3(-2, -2, 2) + float3( 1,  1, -1);
float3 r = normalize(t * dot(t, u) - u * t.z);
```

三行代码（加法 / 点积 / 法化各一次）就完成几何上干净的混合：基础法线平坦时输出等于细节法线，细节法线平坦时输出等于基础法线（identity），两张贴图的强度都被保留，不抹平。

## 和 Unity 版本的区别

Unity（Zioma 2012 GDC）用的是一种**基底矩阵**：把 `n1` 绕 y 和 x 轴各转 $\pm 90^\circ$ 构造三个正交向量。当 `n1` 偏离 $\pm z$ 时这三个向量不再正交，整个变换退化——在演示图里，一圈均匀的上半球向量被压成一条线。RNM 不存在这个退化。

## 成本与取舍

Hill 在 SM3.0 虚拟指令集上的对照：Linear / UDN 约 5 条，PD / Whiteout 约 7 条，**RNM 含 normalize 约 8 条**，Unity 基底版 8 条。在现代 GPU 上这点差异基本可以忽略。法线真正的热点在纹理采样、编码 / 解码和带宽，不在混合函数本身。

注意：RNM 的输出 $z$ 不保证 $\geq 0$——如果管线后续要压缩成两通道法线格式（重建假设 $z\geq 0$），需要在压缩前 clamp 并 renormalise。

## 相关

- [[stephen-hill]]
- [[3d-rotation-math]] — 最短弧四元数正是 3D 旋转的一种表示
- [[normal-decal-edge-blending]] —— 用独立几何层承载 normal map 来掩盖低多边形 mesh 的硬边过渡

## Sources

- [[sources/selfshadow-blending-in-detail]]
