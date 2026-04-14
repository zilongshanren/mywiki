---
tags: [rendering, shader, post-processing, convolution, image-processing]
date: 2026-04-14
sources: 1
---

# 图像卷积核（Convolution Kernel）

**卷积（convolution）**是把一个奇数边长的小矩阵（kernel）在图像上逐像素滑过，每个位置上用矩阵值加权周围像素颜色、求和、再除以矩阵元素总和，得到中心像素的新颜色。模糊、锐化、边缘检测、浮雕——几乎所有"看邻居"的 image effect 都是某个特定核的卷积。

## 数学骨架

设核为 `K`（NxN，N 奇数），半径 `r = (N-1)/2`，则输出像素

```
out(x, y) = Σ_{i=-r..r} Σ_{j=-r..r} K(i, j) * in(x+i, y+j)    /  Σ K
```

除法（归一化）保证核的整体能量是 1——否则图像整体会变亮或变暗。不同的 K 决定效果类型：

| 核类型 | 示例 | 作用 |
|---|---|---|
| 全 1 | Box Blur | 均匀模糊 |
| 中央高，边缘低 | Gaussian | 平滑模糊 |
| 中央正、邻居负 | Sobel / Laplacian | 边缘检测 |
| 中央大正、邻居小负 | Unsharp Mask | 锐化 |

## 在 fragment shader 里怎么写

GPU 没有"卷积原语"——所有卷积都得在 fragment shader 里用 for loop 手动采样 `tex2D` 累加。Unity 提供一个叫 `_MainTex_TexelSize` 的自动变量，分量 `xy = (1/width, 1/height)`，把像素偏移换算回 uv 空间：

```hlsl
int r = (_KernelSize - 1) / 2;
fixed3 sum = 0;
for (int x = -r; x <= r; ++x)
    for (int y = -r; y <= r; ++y) {
        float2 off = float2(_MainTex_TexelSize.x * x, _MainTex_TexelSize.y * y);
        sum += K(x, y) * tex2D(_MainTex, i.uv + off).rgb;
    }
sum /= kernelSum;
```

对 NxN 的核，每像素要做 N² 次纹理采样——3x3 还能接受，15x15 就已经是 225 次/像素。这是 [[separable-gaussian-blur|可分离卷积]] 存在的直接动机：能拆成横+竖两次 1D 卷积的核（Box、Gaussian、Sobel），可以把 N² 降到 2N。

## 边界行为由 wrap mode 决定

卷积在图像边缘会采样到 `[0, 1]` uv 区间之外的"幻像素"，行为取决于纹理的 [[sampler-filter-wrap-modes|wrap mode]]：

- **Clamp**（默认）：边缘像素颜色被复制到外侧，画面边缘稳定但不对称的核会"偏向"边缘颜色。
- **Repeat**：图像平铺，另一边的颜色会"bleed"过来——对后处理通常是灾难。
- **Mirror**：镜像延拓，边缘区域的卷积结果更自然但略慢。

Image effect 默认沿用 Clamp，一般不需要改。

## 为什么 image effect 常用 3x3 而不是更大

除了"N² 采样爆炸"的性能账，更根本的原因是：大卷积核的 **有效半径翻倍等于时间代价翻倍**，而人类视觉对"更大的模糊半径"的感知是亚线性的——实务上想扩大模糊半径，常用的办法是**先下采样到半分辨率再用小核卷积**（`Dual Kawase`、`Bloom pyramid`），这比直接把 kernel 加大划算得多。

## 相关

- [[separable-gaussian-blur]]
- [[sampling-theorem-sinc]]
- [[image-resampling-filters]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[sampler-filter-wrap-modes]]

## Sources

- [[sources/danielilett-image-effects-blurring]]
