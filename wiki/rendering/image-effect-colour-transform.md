---
tags: [rendering, shader, post-processing, color, unity]
date: 2026-04-14
sources: 1
---

# 颜色变换类 Image Effect（Greyscale / Sepia）

图像后处理里最简单的一类：**逐像素独立**地把 RGB 映射成另一组 RGB，不需要访问邻居像素、不需要深度、也不需要额外 buffer。这类效果是学习 fragment shader 的最佳起点，因为它把"特效"压缩成了"一次小线性代数"。Daniel Ilett 在 *Image Effects Part 1* 里用灰度和棕褐色两个例子把这层抽象讲透。

## 灰度：RGB → 单亮度

灰度不是"三通道平均"——绿通道对观感亮度贡献最大，所以标准的 Rec.601 系数是：

```
lum = 0.3 * R + 0.59 * G + 0.11 * B
result = float4(lum, lum, lum, alpha)
```

本质是把 RGB 向量和一个常量亮度系数向量**点乘**。这个系数反映的是人眼三种视锥细胞对波长的敏感度——同一亮度下人对绿色最敏感，这也是为什么 [[color-space|颜色空间]] 转换、Bayer 传感器、视频编码（Y'CbCr）里绿色通道都拿最大权重。

## Sepia：RGB → 带交叉项的 RGB

Sepia 不是 RGB → 单通道，而是 RGB → RGB 的非对角映射——输出红通道要读入入的红绿蓝、输出绿也要、输出蓝也要。系数组成一个 3×3 矩阵，例如 Ilett 给的经典套路：

```
sepia = [0.393 0.349 0.272]
        [0.769 0.686 0.534]   * rgb
        [0.189 0.168 0.131]
```

HLSL 里一句 `mul(tex.rgb, sepiaVals)` 就完事。这个例子揭示了一个更一般的规律：**任何线性色调映射（color grading / white balance / LMS 校正）都可以写成 3×3 矩阵乘法**，而 GPU 对 3×3 mul 的吞吐是白给的。这也是为什么一整套 [[color-lut|Color LUT]] 体系之外还有"直接存矩阵"的实现路径——代价小、参数少、连续可调。

## 为什么从这里开始学

这个类别的后处理有三个教学价值：

1. **Fragment shader 是逐像素独立函数**的事实被放大到极致——没有邻居、没有状态，唯一变量是 uv 和 `_MainTex` 的一次 `tex2D` 采样。任何能写成"像素颜色的纯函数"的效果（对比度、亮度、伽马、posterize、inversion）都是同一套模板。
2. **矩阵就是 GPU 的原生语言**——HLSL 里 `half3x3`、`mul`、`float4` 构造器、swizzle（`.rgb`、`.xyz`、`.a`）都在这种小例子里自然出现，比先讲矩阵数学再写 shader 直观得多。
3. **为下一步做对照**——下一课的 [[depth-texture-silhouette|Silhouette 深度剪影]]、再下一课的 [[separable-gaussian-blur|Gaussian Blur]] 都开始打破"逐像素独立"的假设：Silhouette 需要多采样一张深度纹理，Blur 需要采样邻居。把颜色变换当起点，后续的"多采样"才看得出代价。

## 相关

- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[color-space]]
- [[color-lut]]
- [[depth-texture-silhouette]]
- [[separable-gaussian-blur]]

## Sources

- [[sources/danielilett-image-effects-colour-transforms]]
