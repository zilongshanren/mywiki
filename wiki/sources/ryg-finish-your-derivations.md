---
tags: [source, 数学, 着色器, 优化, ryg]
date: 2026-04-14
sources: 1
---

# Finish your derivations, please（ryg / The ryg blog）

[[fabian-giesen]] 在 2010 年 10 月写的一份简短檄文，主题是：大多数「这段 math 代码很慢」的场景，根本问题不是缺 SIMD 或缺 intrinsics，而是**作者没把推导做完**就把代码提交了。

## 摘要

ryg 列了一份「第一版代码能跑之后，再花 5 分钟回头看一次」的检查单：利用问题的**对称性**；问题若是几何的就**画图**，避免纯代数推导丢失几何意义；**避免角度**，尤其是绝对角度（会 wrap、要 trig）；**绝不在反三角后直接接 sin/cos**——那是世界上最贵的 2D 向量归一化；**矩阵乘法预先符号展开**，别运行时反复乘；**正交矩阵用转置代替逆**；**别到处用 4×4 矩阵**——仿射变换 3×4 就够；**别做数值微分**——解析函数就该求解析导数。文章核心的案例来自一个 Oren-Nayar shader 的早期简化版：`max(acos(dot(v,n)), acos(dot(l,n)))` + `sin/tan` 的代码在套用三角恒等式 `sin(acos(x)) = √(1−x²)` 和「acos 单调递减」后，可以化简成一个只含 dot product + sqrt + max 的形式——**不再需要 LUT**，还**精度更高**。评论区有人请求展开推导，ryg 亲自把每一步都讲了一遍。文末另一位评论者补充「**迭代自校正方法优于直接方法**」——即便 Gaussian elimination 也需要迭代精化来应对病态输入；像三次方程闭式解这种「漂亮代码」往往在数值上最脆弱。

## 关键要点

- **对称性**：若问题有对称中心/轴，先挪过去
- **几何 > 代数**：几何解的中间量有物理含义，debug 时能做 sanity check
- **避开角度**：特别是绝对角度——会 wrap，要 trig，伪影多
- **反三角接 sin/cos 是臭代码味**：`atan2/sin/cos` 是最贵的 2D 归一化；`acos(dot)` 接 `sin`/`tan` 几乎总能用恒等式消掉
- **Oren-Nayar 示例**：`sin(alpha)*tan(beta)` 化简为 `sqrt((1−vdotn²)(1−ldotn²))/max(vdotn, ldotn)`，不需要 LUT，精度反而更高
- **符号矩阵乘**：把变换链连乘结果**预先展开**，运行时直接套公式，注释里写清楚顺序和方向
- **转置代替逆**：对 orthonormal 矩阵成立；术语上 `orthogonal matrix` 已蕴含 `Q^T Q = I`
- **别用 4×4 矩阵**：除了投影矩阵，大多数变换是仿射的，3×4 就够
- **别做数值微分**：解析函数直接求解析导数；记得用链式法则处理 warp
- **迭代法 > 直接法**：中间误差几乎不重要，总能靠残差回修
- 文案金句：「每发布一段半吊子数学代码，上帝就把一只小猫喂给脾气糟糕的熊猫」

## 链接到的概念

- [[hlsl-derivation-correctness]]
- [[faster-math-functions]]
- [[shader-vector-math-primer]]
- [[normalised-blinn-phong-shader]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/21/finish-your-derivations-please/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-21_finish-your-derivations-please.md`
