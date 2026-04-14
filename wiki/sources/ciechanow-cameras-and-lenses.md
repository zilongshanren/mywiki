---
tags: [source, 渲染, 相机, 光学]
date: 2026-04-14
sources: 1
---

# Cameras and Lenses（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2020 年 12 月发表的长文，从「一个裸 sensor 拍出来就是一片糊」开始，一步步搭出针孔相机 → 薄透镜 → 光圈 → 景深 → 像差的完整物理链条。

## 摘要

文章先建立裸 sensor 的失败——每个像素收到来自全场景的光，图像不成立。然后用盒子 + 小孔建立**针孔模型**，解释图像倒置、field of view 随距离变化、以及 **cosine-fourth-power natural vignetting** 的四重推导。接着指出针孔的两个致命问题（效率低、无景深控制），用 Snell 定律推出折射 → 引入薄透镜方程 `1/so + 1/si = 1/f` → 讨论焦距、光圈、f-number、circle of confusion、景深、bokeh 形状。最后一节讲物理世界的麻烦：球差、彗差、像散、场曲、畸变、色差，以及高端镜头如何用多片组和非球面玻璃矫正。

## 关键要点

- **针孔是极限情形**：f-number 极大时的薄透镜就退化成针孔。
- **FoV = 2·atan(sensor/(2·distance))**：投影矩阵的 fovY 就是这个几何量。
- **cos⁴(α) 自然暗角**：来自 inverse-square + 针孔斜视椭圆化 + sensor Lambert 余弦的叠加。
- **f-number 同时控制曝光和景深**：因为它控制了光锥的张角。
- **Circle of confusion** = 离焦点光线在 sensor 上的圆斑，景深就是它小到一个像素的范围。
- **Bokeh 形状 = 光圈孔形状**：多叶片光圈产生多边形 bokeh。
- **像差的根源**是 paraxial approximation 在边缘失效——近轴假设的代价。

## 链接到的概念

- [[pinhole-camera]]
- [[thin-lens-model]]
- [[mvp-transform]]
- [[coordinate-spaces]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/cameras-and-lenses/
- 本地：`raw/articles/ciechanow.ski/2020-12-07_cameras-and-lenses-bartosz-ciechanowski.md`
