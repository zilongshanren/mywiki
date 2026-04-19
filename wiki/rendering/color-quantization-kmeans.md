---
tags: [color, clustering, image-processing, k-means, palette-extraction]
date: 2026-04-14
sources: 1
---

# K-Means 主色提取

**K-Means 主色提取**（color palette extraction via K-Means clustering）是把一张图缩减到 `k` 种代表色的最常见做法。把每个像素看成 RGB 三维空间里的一个点，K-Means 会找到 `k` 个质心让"每点到它所属质心的平方距离之和"最小——这些质心就是这张图的"主色"。它在截图按色调排序、生成调色板、像素艺术压缩、主题色提取等场景都被反复用到。

与另一种含义的"[[color-quantization-retro|色彩量化]]"不同：后者把每通道强制砍到 `N` 级去模仿老主机；而 K-Means 主色提取是在**连续**颜色空间里找到一小撮代表色，与分辨率无关、与图内容高度相关。

## 核心流程

1. **缩图**——把长边缩到 ~100px。主色分布对分辨率不敏感，但聚类开销随像素数线性增长，这步几乎零损失换两个数量级 speedup。
2. **Reshape**——`image.reshape((-1, 3))` 把 H×W×3 展平成 N×3 的点集。
3. **Fit K-Means**——`KMeans(n_clusters=k).fit(points)`。返回 `cluster_centers_`（k 种主色）和 `labels_`（每像素所属 cluster）。
4. **按像素数排序**——用 `np.histogram(labels_)` 数每个 cluster 占比，再和 centroid zip 起来按占比降序排。第 0 个就是最主导的颜色。

Python/scikit 最小实现可以压到 10 行以内，OpenCV 也有自带的 `cv2.kmeans`。

## 为什么 `k` 不能乱定

K-Means 的 `k` 是强约束——如果一张图里真正只有 2 种主色，你逼它分 5 团，多余的 centroid 会被硬塞进同一片颜色里，结果既浪费又误导。多数教程略过这一点，这也是入门者最容易吃亏的地方。

推荐的自适应做法：**[Silhouette 系数](https://en.wikipedia.org/wiki/Silhouette_(clustering))**。它对每个点算 `(b - a) / max(a, b)`——其中 `a` 是点到同 cluster 其它点的平均距离、`b` 是点到最近"异族" cluster 的平均距离——再对全图取均值。值 ∈ [-1, +1]：

- +1：cluster 内紧、cluster 间远，聚类漂亮
- 0：cluster 边界模糊
- 负：点被错分了

扫一圈 `k = 2..10`，取 silhouette 最高的那个 `k`，就是这张图上 K-Means 能给出的最佳分层。Zucconi 在 0RBITALIS 截图上得到 `k=2`，在 *Proteus* 截图上得到 `k=8`——图越花 `k` 越大，符合直觉。

## 隐藏陷阱：RGB 欧氏距离不是感知距离

K-Means 的距离默认就是欧氏。但人眼对 RGB 分量的感知不均匀：蓝色通道的一步和绿色通道的一步在感知上相差很大。纯 RGB 聚类出来的主色经常"数学正确、视觉不对"。

改进路径：

- 换到 **LAB** 或 **[[oklab-color-space|OkLab]]** 空间跑 K-Means——距离更接近感知差
- 用 **[[color-space|HSV / HSL]]** 做前置分拆——先按 Hue 聚类得到色相分组，再在每个组里按亮度分
- 更激进：直接用 [Earth Mover's Distance / Wasserstein](https://en.wikipedia.org/wiki/Wasserstein_metric) 在分布层面比较调色板

Eddie Bell 在 Lyst 的 [color detection](http://developers.lyst.com/data/images/2014/02/22/color-detection/) 一文里对比过 RGB vs LAB 的主色提取差异，大面积背景图里 LAB 明显更合理。

## 相关
- [[color-quantization-retro]] —— 另一种"颜色量化"：每通道砍级数模仿老主机，互补而非替代
- [[color-space]]
- [[oklab-color-space]]
- [[color-banding]]
- [[color-lut]]
- [[perceptual-colormaps]]
- [[vector-quantization-tilemap]] —— 把 K-Means 推到「块级」，得到瓦片图 + 码本
- [[color-quantization-som]] —— 用 1D SOM 得到有序调色板（ScreenToGif NeuralQuantizer 的原理）

## Sources

- [[sources/alanzucconi-main-colours-kmeans]]
