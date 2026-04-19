---
tags: [math, data-analysis, visualization, linear-algebra]
date: 2026-04-19
sources: 1
---

# PCA：主成分分析直觉入门

主成分分析（Principal Component Analysis, PCA）是把数据集的协方差矩阵做特征分解，挑出**方差最大的正交方向**作为新坐标轴。它既是经典降维工具，也是理解很多渲染与信号处理思想（球谐基、光照探针压缩、神经网络白化）的起点。[[alan-zucconi]] 的 *PCA for Programmers* 系列用可交互几何动画代替公式推导，适合当直觉入门。

## 一句话直觉

**旋转坐标系，使得前 k 根新轴上投影的方差最大**——剩下的方向信息噪声比最差，可以丢掉。这就是把数据拟合成椭球后，取它的前几个半轴作为新坐标系。

## 几何视角

- 把 N 个数据点看成 D 维空间里的一坨云；
- 求协方差矩阵 Σ（D×D）；
- 对 Σ 做特征分解：Σ = VΛVᵀ；
- 特征向量 **v₁, v₂, …, v_D** 是正交主成分，特征值 **λᵢ** 对应**该方向上的方差**；
- 把数据投影到前 k 个 vᵢ 构成的子空间，就完成了降维。

Zucconi 的 2D demo 直接让读者拖旋转角，眼看着投影方差（椭圆宽度）随角度起伏——最大值处就是第一主成分。这个图比任何公式都更能解释「为什么特征向量选的是椭球半轴」。

## 为什么在图形 / 渲染里也有用

- **球谐光照压缩**——radiance 场的 PCA 是一种主动压缩基，而 [[spherical-harmonics]] 是选定的正交基；两者都能降维，区别是后者对球面旋转不变。
- **光照探针压缩**——高维颜色数据用 PCA 做主成分截断可以压掉 80% 存储。
- **Mesh shape key / morph target** 压缩——Zucconi 在 *Face Tracking* 系列里就把面部动画数据 PCA 到低维。
- **动画 motion matching**——把姿态向量 PCA 后再做 KNN，kd-tree 查询更快。
- **相机降噪 / film grain 建模**——PCA 能分离主颜色成分与高频噪声。

## 方法论上的陷阱

1. **要先中心化**（减去均值），否则第一主成分会被整体偏移带偏；
2. **要标准化不同量纲**（Z-score），否则大量纲特征会主导 PC；
3. **PCA 是线性的**——对曲面流形数据（人脸姿势、文本 embedding）常常不够，需要 kernel PCA / t-SNE / UMAP；
4. **特征值截断的比例**由累积解释方差决定，常选 80-95%。

## 与本 wiki 其他主题的对接

- [[color-quantization-kmeans]]——另一种「压缩数据集」的方法，对比视角有趣：PCA 是连续降维、k-means 是离散聚类。
- [[functions-as-vectors]]——PCA 的抽象升级版：连续函数空间里也有主成分分解（Karhunen-Loève 展开）。
- [[spherical-harmonics]]——PCA 的「旋转不变」特殊形式。

## Sources

- [[sources/alanzucconi-pca-intro]]
