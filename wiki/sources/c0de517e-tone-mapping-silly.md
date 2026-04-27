---
tags: [source, graphics, 色调映射, 后处理, film-grain]
date: 2026-04-27
sources: 1
---

# More (silly) tone-mapping ideas（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2016 年 10 月的文章，续接上篇，介绍两个快速实验性的 tone mapping 技巧：自适应 ND 渐变滤镜和胶片颗粒的动态范围扩展效应。

## 摘要

第一个技巧是**自适应 ND 滤镜**：对图像做大半径高斯模糊，用模糊结果作为每像素曝光比例因子，再做全局 TM。与直接用 gaussian 做 bilateral TM 的区别在于：只要模糊半径足够大，就不会产生可见的 halo——人眼对极低频梯度几乎不敏感。这种方法等价于用 bloom/veil 的图像金字塔来驱动曝光，因此可以复用已有的 bloom pass，成本几乎为零。实测在 COD:AW 上室内效果尤为明显，可以减少自动曝光的用量。

第二个技巧是**胶片颗粒扩展高光/阴影**：真实胶片颗粒在纯白和纯黑区域（曝光饱和区）是均匀的，在中间调才有随机分布的颗粒。这意味着颗粒可以充当 dither，在高光和阴影区扩展有效比特深度——亮于白点的区域颗粒被减掉之后依然全白，使其看起来比没有颗粒时更"实心"，暗部类似。Pesce 修改了颗粒强度曲线，让中间调颗粒弱而两端颗粒强，从而在不明显增加中间调噪声的前提下增强了高光和阴影的细节感。

## 关键要点

- 极低频的曝光梯度（大半径高斯 ND）不会产生 halo，且可复用 bloom pass
- 胶片颗粒在高光/阴影的聚集行为本质上是 dithering，可以扩展感知动态范围
- 多种 TM 技巧可以叠加，每种只做小量压缩，合力实现大范围压缩
- 颗粒强度曲线应在中间调弱、极值区强，避免中间调过噪

## 链接到的概念

- [[local-tonemapping]]
- [[color-banding]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/10/more-silly-tone-mapping-ideas.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-10-01_more-silly-tone-mapping-ideas.md`
