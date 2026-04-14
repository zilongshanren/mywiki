---
tags: [source, 自动微分, 优化, 机器学习, 编译器, 可微编程]
date: 2026-04-14
sources: 1
---

# Differentiable Programming from Scratch（Max Slater）

[[max-slater|Max Slater]] 2022 年 7 月发表的长文（**3Blue1Brown Summer of Math Exposition 2 honorable mention**）：从微积分定义起步，一路推到 forward / backward autodiff 和 JAX 的「梯度即图变换」视角，最后用 30 行自写的 autodiff 框架解一个 **图像反模糊** 问题。

## 摘要

文章的前半部分是 **微分的几何重述**：导数不是「斜率」而是「把输入处的向量映射到输出处的向量的线性算子」。在这个视角下，1D 导数是标量、梯度是行向量、Jacobian 是矩阵——**链式法则就是矩阵乘法**。这一观察是后面所有 autodiff 的基础。然后讲 **优化** 和 **梯度下降**：批评朴素步长选择带来的发散与局部极小，作为后面 demo 的铺垫。

中段比较 **三种程序求导技术**：(1) 数值微分，简单但每个方向都要单独跑 $f$，高维不可行；(2) 符号微分，Mathematica 式的代数变换，但 `Times` 求导后表达式至少翻倍——Slater 用归纳证明 $f^\prime$ 的大小是 $f$ 的指数；(3) **autodiff**，既精确又不爆炸，是真正的现代算法。

下半部分讲 autodiff 的两种模式。**Forward mode** 用 **dual number** $a + b\epsilon$（$\epsilon^2 = 0$），把 `Float` 替换成 `(value, dual)` 二元组、重载所有运算，跑一遍原函数即可。每次评估只算 Jacobian 的一列，适合「少输入、多输出」。**Backward mode** 是反向传播：先 forward pass 算 primal 并记录 DAG（tape），再按逆拓扑序 backward pass 把每个节点的 grad 按局部偏导推回输入边。本质是「**链式法则 + 动态规划**」，时间复杂度等同 $f$ 自身，但要存所有中间值——所以有 checkpointing 和图分割两种工程优化。

最后是 Slater 自己的「第三种视角」：把 $\nabla f$ 自身建成另一张图——只要在 $f$ 的图上添加 $O(1)$ 个 grad 节点。**$\nabla f$ 也是图意味着可以再求导得到 Hessian**，统一了 forward / backward，更容易并行和 JIT，**这就是 JAX 的设计**。文末用自写框架对一张被 3×3 box-blur 模糊后的图像跑梯度下降反模糊——纯 autodiff，不依赖任何 ML 框架。

## 关键要点

- **导数 = 输入向量到输出向量的线性算子**——这一视角让链式法则、梯度下降、autodiff 三件事自然连贯。
- **梯度是「最陡上升方向」** 因为它是使方向导数最大化的 $\mathbf{v}$。
- **符号微分的指数爆炸** 来自 `Times` 求导规则，是为什么不能用 Mathematica 训神经网络的硬数学原因。
- **Forward mode = dual number** 重载，**只算 Jacobian 一列**，适合多输出函数。
- **Backward mode = 记录 DAG + 反向遍历**，**只算 Jacobian 一行**，适合多输入单输出（即 ML loss）。
- **反向传播的时间复杂度与 $f$ 同阶**，但 **空间复杂度** 是它的痛点——所以现代框架做 checkpointing 和图分割。
- **JAX 的「梯度即图变换」** 把 forward 和 backward 统一成「在 $f$ 的图上添加 $O(1)$ grad 节点」，自动支持高阶导数与并行编译。
- **可微编程 ≠ ML**：可微渲染、可微物理、neural representation 都依赖同一套 autodiff，文章里图像反模糊的 demo 就是非 ML 应用的最小样本。

## 链接到的概念

- [[automatic-differentiation]]
- [[functions-as-vectors]]
- [[higher-order-functions]]
- [[probabilistic-algorithms]]
- [[spherical-harmonics]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Autodiff/
- 本地：`raw/articles/thenumb.at/2022-07-31_differentiable-programming-from-scratch.md`
