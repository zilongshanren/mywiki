---
tags: [线性代数, 渲染, 坐标变换, 矩阵]
date: 2026-04-19
sources: 2
---

# 矩阵作为基向量（Change of Basis 与 Basis Projection）

[[ben-supnik|Supnik]] 在 2010 年连写两篇短文，用一套「预制件」比喻把 3x3 变换矩阵讲清楚：矩阵既能**解码**也能**编码**，同一块 9 个 float 根据你从列还是从行去读，含义完全对称。

## 列 = 解码：每一列是一根新坐标轴

考虑一个 3x3 矩阵 T，列向量分别是 (a,b,c)、(d,e,f)、(g,h,i)。当它乘上 (x,y,z) 时，x 提取第 1 列若干份、y 提取第 2 列若干份、z 提取第 3 列若干份——**x、y、z 是「订单数量」，矩阵的列是「预制零件」**。这些列可以直接解读为**旧坐标系的三根轴在新坐标系里的表达**。

当这三根基向量都满足「长度为 1」且「两两正交」时，矩阵就是**正交矩阵（orthogonal matrix）**，对应的基叫**标准正交基**。几何后果：模型既不会被拉伸也不会被斜切，能直接用于法线变换。

补上平移就成 **affine matrix**：左上 3x3 是线性部分（通常取正交），第 4 列是位移，最后一行 0 0 0 1。Supnik 特别注明：**affine 不强制左上是正交的**，只需要线性即可；但 X-Plane 选择只用 affine-orthogonal 的子集，因为能享受一连串性质——转置即逆、两个这样的矩阵相乘仍是同型、法线可以直接被左上 3x3 变换而不变长。

## 行 = 编码：把世界空间的点投影回模型空间

既然矩阵列是「旧基在新坐标系里的长相」，那**行**又是什么？Supnik 的第二篇给出答案：因为正交矩阵的转置等于它的逆，所以**同一个矩阵的行，恰好是新基在旧坐标系里的长相**——也就是 **encode 用的投影算子**。

物理过程：若要把世界空间里的一个顶点 V 编码回模型空间，你做的是 `V · basis_i`——分别与三根模型基做点积。这正是「把 basis 塞到行里」的矩阵所做的事。所以一个 orthogonal matrix 在列视角下是 decoder，在行视角下是 encoder，两者互为转置、互为逆。

## 为什么这对相机 billboarding 很有用

相机变换是模型变换的反向：先反向旋转，再反向平移。model-view 矩阵里藏着所有相机朝向信息——

- **相机各个方向轴在世界坐标系下的表达**就在左上 3x3 的**行**里（因为行是 encoder，而 view matrix 的作用是 world → eye 编码）。第 1、2、3 行分别是 eye-space 的 X、Y、Z 轴在世界空间里的表达——这三根轴就是 billboard 需要的右向量、上向量、前向量。
- **相机在世界空间中的位置**没法直接从右列读出，因为 view matrix 的平移已经被「预旋转」过了；正确做法是用左上 3x3 的转置乘以右列再取负。

这就是为什么 X-Plane 能用极少量算术从 model-view 矩阵推出 camera 位置与 billboard 方向——所有几何事实都躺在矩阵里，只需要懂从列还是从行去读。

## glScale 被排除在外

标准正交基不能被 uniform scale 以外的操作破坏，否则要么基向量不再 unit-length、要么不再正交。X-Plane 明确禁止 `glScale`：不需要非均匀缩放，而且「左上 3x3 是正交的」这一性质能让法线变换省掉重新归一化。mirror（行列式为 -1）不会破坏正交性，但会翻转 triangle winding，所以也不用——为了 back-face cull 的正确性。

## 相关

- [[coordinate-spaces]]
- [[mvp-transform]]
- [[matrix-multiplication-ordering]]
- [[huge-world-coordinate-precision]] —— X-Plane 另一个 world → model 变换被迫触发的场景
- [[ben-supnik]]

## Sources

- [[sources/supnik-change-of-basis-revisited]]
- [[sources/supnik-basis-projection]]
