---
tags: [source, rendering, shader, unity, post-processing, color]
date: 2026-04-14
sources: 1
---

# Image Effects Part 1 — Colour Transforms（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 1 篇，用两支 fragment shader 演示如何把 RGB 逐像素地线性变换成灰度和旧照片色调。

## 摘要

文章把"颜色变换"这个概念落到两个最简后处理上：**灰度滤镜**与**棕褐色（Sepia Tone）滤镜**。灰度版本用人眼对三原色敏感度的经典系数 `lum = 0.3*R + 0.59*G + 0.11*B`——人眼对绿最敏感，所以 G 通道权重最大——把每像素压成一个亮度值再写回三个通道；Sepia 则需要一个 3×3 的系数矩阵，把输入 RGB 混合成带黄棕偏移的输出，用 HLSL 的 `mul(tex.rgb, sepiaVals)` 一次完成。作者顺便介绍了 `v2f_img` / `vert_img`——`UnityCG.cginc` 为 image effect 预设的通用结构体和 vertex shader，免去重复声明；并解释了 `float / half / fixed` 三种浮点精度在桌面 GPU 上基本等价，只有移动端才会真正降精度。整篇的价值在于建立"后处理 = 对每个像素独立做一次小矩阵运算"的直觉。

## 关键要点

- 灰度转换本质是点乘亮度系数向量；系数反映人眼 CIE 敏感度。
- Sepia 需要颜色通道之间的交叉项，所以用 3×3 矩阵；GPU 上用 `mul(rgb, matrix)` 一步搞定。
- `v2f_img` 和 `vert_img` 是 Unity 为 image effect 提供的免写样板。
- image effect 的 fragment shader 是**逐像素独立**的，不依赖邻居——这是后续模糊、边缘检测类特效的对照起点。
- `float / half / fixed` 精度差异在移动 GPU 才显著，桌面基本都是 32-bit。

## 链接到的概念

- [[image-effect-colour-transform]]
- [[unity-image-effect-basics]]
- [[color-space]]

## 原文

- 链接：https://danielilett.com/2019-05-01-tut1-1-smo-greyscale/
- 本地：`raw/articles/danielilett.com/2019-05-01_image-effects-part-1-colour-transforms.md`
