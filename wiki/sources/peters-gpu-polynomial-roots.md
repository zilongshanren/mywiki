---
tags: [source, 渲染, GPU, 数值方法, 着色器优化]
date: 2026-04-14
sources: 1
---

# Finding Real Polynomial Roots on GPUs（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2023 年 10 月发表的一篇「数值算法 × GPU 性能工程」双线记录：他在做一个 VMV 2023 论文里的**球谐 glyph 可视化**时，需要在 shader 中求解度 10–26 的实系数多项式的所有实根。这篇博客讲了算法选型（为什么抛弃 Laguerre 改用 Cem Yuksel 的 bracketed Newton bisection）以及**为了让它在 GLSL 里跑快**而做的一系列反寄存器溢出设计。

## 摘要

多项式求根是古老问题，离线方案很成熟，但 GPU 上实现极少。Peters 先试了 Laguerre 方法——能找复根，但所有运算是复数、每次多项式评估贵 4×，而且重根边界会出现实/虚判定模糊；整体比"100 步 ray marching 粗糙近似"还慢。于是他转向 Cem Yuksel 2022 的 **bracketed Newton bisection**：每步把 Newton 步和 bisection 混合，用区间包住根、Newton 跳出就 fallback 到中点。要找"恰好一根"的区间就先递归求 $p'(x)$ 的根——直到二次公式收尾。C++ 实现是递归的，但 Peters 彻底展平：用一个 `d+1` 长度的一维数组按位置编码所有层级的根，前后两个元素就是 bracket。**整套代码的最大敌人不是算法本身，而是寄存器溢出。**任何"循环下标当数组下标"的地方都会强制把数组降级到 local memory，严重的时候能让度 18 shader 慢 **255×**。Peters 的解法：该 `[[unroll]]` 的地方 unroll、不该展的地方 `[[loop]]`；阶乘表和动态数组索引全部通过数学重写（积分迭代 + $\binom{j+k}{k}$ 替换 $k!$）避开。最终 RTX 2070 Super 上度 10 多项式求根 **1.46 ms**、度 18 **10.4 ms**，Nsight 报 FMA pipe 吞吐率 78%——健康状态。

## 关键要点

- **度 ≥ 5 无闭式解**，必须迭代。闭式只有 cubic / quartic。
- **Laguerre vs bracketed Newton bisection**：前者靠谱但强制复数运算，后者便宜 2.7×。
- **bracket + 导数递归** 保证每次迭代区间里只有一个根，可以放心 Newton。
- **数据结构的精巧**：一维数组按位置存所有层级根，新一层恰好覆盖不再需要的根。代码对所有导数阶复用同一段。
- **寄存器 = GPU 的生命线**：寄存器带宽比 VRAM 快 ~718×。一旦数组被动态索引访问，编译器会 spill 到 local memory。
- **展开规则**：凡循环下标做数组下标的地方必须 `[[unroll]]`，其它用 `[[loop]]`；过度展开会撑爆 instruction cache。
- **阶乘表也是动态查表**：Peters 改用 $\tfrac{1}{k!} p^{(k)}(x)$，系数用**从上一层反向积分**的方式递推，完全免除查表。
- **溢出的数量级**：度 10 慢 3.3×，度 18 慢 **255×**——几乎确定 spill 穿透到 VRAM。
- **稳定性**：单精度 + 良好坐标原点下，度 ≤ 18 视觉无瑕疵；度 22 开始有噪点；度 26 崩坏。这不是算法锅，是根对系数的天然敏感。

## 链接到的概念

- [[polynomial-root-finding-gpu]]
- [[register-spilling-avoidance]]
- [[gpu-printf-debugging]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/GPUPolynomialRoots.html
- 本地：`raw/articles/momentsingraphics.de/2023-10-31_finding-real-polynomial-roots-on-gpus.md`
