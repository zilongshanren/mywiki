---
tags: [image-compression, precomputed-lighting, pca, pvrtc, bilinear-interpolation]
date: 2026-04-19
sources: 1
---

# Moving Basis Decomposition（移动基分解）

**Moving Basis Decomposition (MBD)** 来自 Ari Silvennoinen 与 Peter-Pike Sloan 2021 年的论文 *Moving Basis Decomposition for Precomputed Light Transport*，原本用于把预计算光照传输（PRT）以很高的压缩比存进探针网格。[[pekka-vaananen]] 在 *Moving basis decomposition for images* 中把它简化到 2D 图像上当玩具实验：可以把它视为 [[pca-image-compression|全局 PCA 颜色压缩]] 和 **PVRTC** 纹理压缩的混合体——**基向量也在空间上变化**，不像 PCA 用同一组主方向管整张图。

## 表示方式

- 一张**稀疏**的基向量张量 `B`，形状 `[N × M × L × D]`：在 `N×M` 低分辨率格子上每格存 `L` 个 `D=3` 维主色方向；
- 一张**稠密**的系数张量 `c`，形状 `[H × W × L]`：每像素（或稍稍下采样）存 `L` 个权重；
- 解码：两个张量都**双线性上采样**到输出分辨率，再按 `pixel = Σ_l c_l · B_l` 做加权和，等价于每像素"用它周围插值出来的两条色轴重建出 RGB"。

与 PVRTC 的关系：PVRTC 是两张 4×4 块低分辨率 RGB 图 + 双线性插值得两个「端点图」，再按每像素权重线性混；MBD 把这个结构一般化——端点数量变成 `L`，权重是连续浮点、可优化而非 1-bit 量化。

## 优化流程（2D 玩具版）

1. **初始化**：全图做 PCA 得 `L=2` 条主方向，把 `B` 的每个格子都填同一份；`c` 初始化为小图上 PCA 投影；
2. **损失函数**：`MSE(reconstruct(B, c), y) + λ ||c||²`，`c` 上加权重衰减是为让方程定义好（否则 `B` 和 `c` 可以同时缩放抵消）；
3. **优化器**：`torchmin` 的 `newton-cg`（SGD 收敛太慢），只需一次 `optimizer.step(closure)` 内循环 50 步。

## 读数与陷阱

- 稠密 `c` 若只下采样 2×，基本无损；下采样 4× 起线性插值痕迹就明显，所以 MBD 这类技术更适合**平滑变化的信号**（间接光照、辉度、AO），对锐利边缘（例子里是霓虹字）会非常丑。
- 原论文还做了 `c` 的熵编码、非线性激活、自适应 basis 数量等，作者的玩具版全部省去。
- 这是一条和 [[neural-lighting]] / [[spherical-harmonics]] 不同的预计算光照压缩路线：不学非线性 MLP，而是老老实实做**空间变化的线性基**，解码端口负担几乎与 PVRTC 相同。

## 相关

- [[pca-image-compression]] —— 全局单组基的退化版
- [[pca-intro]]
- [[spherical-harmonics]]
- [[coordinate-spaces]]

## Sources

- [[sources/30fps-mbd-images]]
