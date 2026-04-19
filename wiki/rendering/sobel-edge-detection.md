---
tags: [rendering, shader, post-processing, edge-detection, convolution, image-processing]
date: 2026-04-14
sources: 1
---

# Sobel-Feldman 边缘检测

**Sobel 算子**是一对 3x3 [[image-convolution-kernel|卷积核]]，分别在水平和竖直方向上估算图像的亮度梯度——哪里梯度大，哪里就是"边"。在屏幕空间里，它是最便宜的一种**非几何边缘检测**手段：不读深度、不读法线、不碰几何，只看颜色变化就能描出物体轮廓。超级马里奥奥德赛 Snapshot Mode 的 *Line Drawing* / *Neon* 两种滤镜就是在此之上做的。

## 两个核必须分开算

Sobel 的两个核长这样：

```
Gx = [-1  0  1]        Gy = [-1 -2 -1]
     [-2  0  2]             [ 0  0  0]
     [-1  0  1]             [ 1  2  1]
```

Gx 在水平方向做差分（左列减右列），Gy 在竖直方向做差分（上行减下行）。两个核**不能合并**成一个 3x3 矩阵：它们对应两个独立的方向梯度，必须分别卷积完再合成。合成方法是把两个梯度看成一个 2D 向量 `(Gx, Gy)`，取其模长 `sqrt(Gx² + Gy²)`——这正是勾股定理——作为当前像素的"边缘强度"。

不像 [[separable-gaussian-blur|可分离高斯]]，Sobel 的两个核无法进一步拆成 1D，所以每像素都要做满 9 次纹理采样乘以 2 次方向 = 约 12 次有效采样（中间行/列系数为 0 可略过）。3x3 的固定尺寸足够小，所以大部分实现直接把 12 条 `tex2D + 常数乘` 展开为硬编码，不写循环。

## 与 HSV / 饱和度 / Bloom 的组合玩法

- **Line Drawing** 只把 Sobel 强度反相作为灰度输出，就是手绘线稿；
- **Neon** 把原图乘以 Sobel 强度当掩膜——边缘有色、内部变黑——再通过 `rgb2hsv` 把饱和度和明度钉到 1.0 让颜色炸出来；
- 最后叠一层 [[bloom-threshold-blur-composite|简易 Bloom]] 让高亮像素发光，就得到 Snapshot Mode 的 Neon 效果。

这种组合是一个**形态学滤镜**（边缘检测）被当作掩膜驱动**颜色滤镜**（HSV 饱和度推满）再叠加**光学后处理**（bloom），典型的 image effect 链式结构——对应 [[unity-image-effect-basics|Unity image effect 骨架]]下的"多个相机组件叠加，从上到下依次 Blit"。

## 用作边缘检测之外的注意

Sobel 看的是颜色变化，**会把阴影边当作物体边**来描——如果不想要就得在场景里关掉实时阴影或把它作为风格元素拥抱。更健壮的做法是改用 depth/normal 缓冲里的差分（URP 的 ScreenSpace Outline、Breath of the Wild 式的描边），但那已经不属于纯 image effect 的范畴。

## 相关

- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[depth-texture-silhouette]] —— 基于深度差分的剪影描边，Ilett 同系列早篇
- [[bloom-threshold-blur-composite]]
- [[unity-image-effect-basics]]
- [[image-effect-colour-transform]]
- [[surface-angle-silhouette]] —— Steven Sell 同系列的前篇：基于 `dot(V, N)` 的剪影，对平面失效，导致作者改用 Sobel
- [[fullscreen-shader-graph-urp]] —— 屏幕空间颜色+法线双梯度 outline 在 URP Fullscreen Graph 下的 Shader Graph 实现

## Sources

- [[sources/danielilett-image-effects-edge-detection-bloom]]
- [[sources/vertexfragment-sobel-outline-unity]] — Steven Sell 的 Unity post-processing v2 stack 实现，深度+法线双 Sobel 合成，含 `OutlineOcclusionCamera` 和 `normal.w = 0` 两种几何排除技巧，以及 Sobel 作屏幕模糊和 height→normal 的副作用应用
- [[sources/danielilett-snapshot2-outline]] —— 三通道（color/depth/normal）屏幕空间 edge detection 的产品化实现
