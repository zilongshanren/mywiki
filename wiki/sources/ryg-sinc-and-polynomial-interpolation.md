---
tags: [source, 信号处理, 数学, 采样定理]
date: 2026-04-14
sources: 1
---

# sinc and Polynomial interpolation（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2010 年 10 月发表的短篇笔记，回答一个困扰他多年的「哲学」问题：傅里叶理论里出现的几乎都是三角多项式（正弦/余弦的有限组合），那么 [[sampling-theorem-sinc|采样定理]] 公式里的 `sinc(x) = sin(πx)/(πx)`——分母里怎么突然冒出一个 `x`？

## 摘要

ryg 的答案绕开了傅里叶变换的标准证明，而是从 **Euler 的无穷乘积公式** `sin(πx)/π = x · ∏ (1 − x²/k²)` 出发。简单的代数变换之后可以看到：`sinc(x − j)` 形式上恰好就是「**所有整数节点上的 Lagrange 基本多项式**」在节点数趋于无穷时的极限。换句话说：

> sinc 插值不是一个特殊的「频域」概念，而是「无穷多等距点的多项式插值」的解析极限。

文章末尾的评论补充了对偶视角：用「带限函数的傅里叶谱可以在频域周期延拓」一句话，再反 FT 回来也能直接得到 sinc 平移族——两条路通向同一个公式。

## 关键要点

- **sinc 插值 = 无穷节点 Lagrange 插值的极限**。这是把「连续的 sinc 重建」和「离散的多项式插值」连在一起的桥。
- **Euler 乘积**是关键身份：`sin(πx) = πx · ∏(1 − x²/k²)`。
- **两套视角等价**：傅里叶（频域 rect 反 FT）和多项式（无穷节点 Lagrange）给出同一族 sinc 平移。
- 一个反复出现的母题：**「神秘公式 = 熟悉对象的某种极限」**。Lanczos、Mitchell、bicubic 这些工程近似都可以理解成「有限 Lagrange / B-样条核去近似无穷节点的极限」。

## 链接到的概念

- [[sampling-theorem-sinc]]
- [[aliasing]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/25/sinc-and-polynomial-interpolation/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-25_sinc-and-polynomial-interpolation.md`
