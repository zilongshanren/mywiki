---
tags: [shader, 数学, 向量, 入门]
date: 2026-04-14
sources: 1
---

# Shader 向量数学启蒙

写 shader 时真正需要的线性代数只是一小块：向量加减、点乘、叉乘、归一化、4×4 矩阵乘向量。Linden Reid 的 *Basic Math for Shaders* 把这些概念按"能做什么"而不是"公式是什么"组织起来——这也是 shader 新手真正能消化的那种讲法。

## 向量的三种身份

在 shader 里，同一个 `float3` 可能代表三种完全不同的东西：

- **位置**：相对某个原点（见 [[coordinate-spaces]]）的 `[x, y, z]` 偏移。
- **方向**：比如光线方向、视线方向、表面法线。长度通常无意义，所以需要**归一化**。
- **颜色**：RGB 分量。

这三种身份在代码里长得完全一样，区别只在语义，所以 shader bug 的一大来源就是搞混"这是 world-space 方向还是 view-space 位置"。

## 减法 = 两点之间的射线

向量减法的真正用途不是"做减法"，而是**构造从 B 指向 A 的向量**：`A - L` 给你光源 L 到顶点 A 的射线。再取长度 `length(A - L)` 就是距离。几乎所有光照、distance field、rim 光计算都从这里开始。

## 点乘 = 夹角信息

两个**归一化**向量的点乘是夹角余弦，落在 `[-1, 1]`：

- `1`：同向
- `0`：垂直
- `-1`：反向

这让你不用真的去算 `acos` 就能"知道角度"。经典用法：

- `dot(N, L)` —— Lambert 漫反射光照强度（见 [[microfacet-brdf]] 的几何项）。
- `dot(forward, toEnemy) > 0` —— 敌人在玩家前方还是后方。
- `dot(viewDir, reflectDir)` —— 高光。

> 关键前提：**两个向量都必须归一化**，否则得到的是 `|a||b|cos(t)`，夹角信息被长度污染。

## 叉乘 = 垂直方向

两个不平行 3D 向量 `A × B` 给出**同时垂直于两者**的新向量。shader 里最常见的用途是**从两条边算出表面法线**：任取三角形的两条边做叉乘即可。新手通常不需要手算这个——`RecalculateNormals` 或 mesh 导出工具已经做过了——但理解它的几何意义对读懂 normal map 推导至关重要。

## 归一化：丢掉长度、保留方向

```
n = N / length(N)
```

法线、光线方向、视线方向都**应当以归一化形式存储**，因为上面所有基于 `dot` 的推导都依赖 `|N| = 1`。存非归一化向量是常见的 shader bug 源头。

## 矩阵 × 向量 = 换坐标系

4×4 矩阵在 shader 里几乎只做一件事：**把一个向量从一个 [[coordinate-spaces|坐标空间]] 搬到另一个**。最高频的组合是 [[mvp-transform|MVP]]：把 object-space 顶点变到 clip space。Unity 里这一步被封装成 `UnityObjectToClipPos` / `UNITY_MATRIX_MVP`——新手几乎不需要亲手构造矩阵，只需要知道"这个 `mul(M, v)` 的几何意义是把 v 换了个参考系"。

## 为什么"看得见的数学"更容易学

Reid 自己的观察：她大学数学挂过，但图形数学学得很好。区别在于**可视化**——向量减法不是抽象符号，而是纸上画的一条箭头；点乘不是公式，而是两条箭头的"相似度"。这也是她推荐 *3D Math Primer for Graphics and Game Development* 作为续读的原因：那本书同样走几何直觉路线。

## 相关

- [[coordinate-spaces]]
- [[mvp-transform]]
- [[3d-rotation-math]]
- [[fragment-shader]]
- [[microfacet-brdf]]
- [[linden-reid]]
- [[diffuse-lighting-lambertian]] —— 点乘在 Lambert 光照里的经典用法

## Sources

- [[sources/lindenreid-basic-math-for-shaders]]
