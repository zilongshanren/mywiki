---
tags: [source, color, clustering, image-processing, python, opencv]
date: 2026-04-14
sources: 1
---

# How to find the main colours in an image（Alan Zucconi）

[[alan-zucconi]] 于 2015 年 5 月发表的 Python/OpenCV 教程，讲怎么从一张截图里提取若干"主色"——为他后来按颜色排序 #ScreenshotSaturday 截图所做的前置工作。

## 摘要

文章把"找图片主色"当成一个聚类问题：每个像素是 RGB 三维空间里的一个点，K-Means 把它们分成 `k` 团，每团的质心就是一种主色。实现几乎完全套 scikit-learn：`image.reshape((-1, 3))` 把图片拍平成点集，`KMeans(n_clusters=3).fit(...)` 跑一下就拿到 `cluster_centers_`。预处理只有一步——用 OpenCV 把图像按长边缩到 100px，聚类开销立刻下降两个数量级而主色分布几乎不变。接着借用 [Adrian Rosebrock](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/) 的 `centroid_histogram` 辅助函数，数每个 cluster 里有多少像素作为"重要度"，按大小排序 centroid 列表。最关键也是多数同类教程略过的一步是 **cluster 数估计**：K-Means 的 `k` 是人给的超参，如果图只有两种主色但你传了 `k=5`，结果会被硬拆坏。作者用 scikit 的 `silhouette_score` 评估 `k=2..10`，选分数最高的 `k`——这是一种小范围搜索式的启发 hyperparameter 选择。文章也指出：在 RGB 空间聚类的结果视觉上未必最好，LAB 空间可能更贴近人眼感知。

## 关键要点

- K-Means 把"图片主色"转化为"RGB 三维空间里的聚类问题"，比读 histogram peak 更鲁棒
- 在 K-Means 跑之前**先缩图**（长边 100px）是几乎零成本的优化：主色分布对分辨率不敏感
- 两条隐藏假设：(1) 某色主导 = 像素多；(2) 色差 = RGB 欧氏距离——后者是所有 RGB 聚类的先天缺陷，换到 LAB / [[oklab-color-space|OkLab]] 通常更好
- Adrian Rosebrock 的 `centroid_histogram`：用 `np.histogram(labels, bins)` 统计每 cluster 占比，再与 `cluster_centers_` 打包排序
- **[Silhouette 系数](https://en.wikipedia.org/wiki/Silhouette_(clustering))** 用来自动估计 `k`：系数 ∈ [-1, +1]，越接近 +1 说明 cluster 内部紧、cluster 之间远。循环 `k=2..10` 取最大
- 作者在两张示例图上得到的最佳 `k` 不同：第一张 0RBITALIS 截图最佳 `k=2`，*Proteus* 截图最佳 `k=8`，反映了图本身的色彩复杂度
- 本文是 Zucconi 三部曲"按颜色排序 #ScreenshotSaturday"的第二篇，前后衔接 image scraping 与颜色排序算法

## 链接到的概念

- [[color-quantization-kmeans]]（本文新建的概念页）
- [[color-space]]
- [[color-quantization-retro]]
- [[oklab-color-space]]
- [[alan-zucconi]]

## 原文

- 链接：https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/
- 本地：`raw/articles/alanzucconi.com/2015-05-24_how-to-find-the-main-colours-in-an-image-alan-zucconi.md`
