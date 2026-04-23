---
tags: [人物, 作者, 渲染, bitsquid, stingray]
date: 2026-04-19
sources: 3
---

# Jean-Philippe Guertin (Jp)

蒙特利尔渲染工程师，Bitsquid / Autodesk Stingray 时期的渲染程序员。在 [[niklas-frykholm|Niklas]] 主导的 Bitsquid Blog 上发过数篇以"Jp"为笔名的文章，主要涉及**时间重投影、体积云、物理 lens flare、SSR reprojection** 等"把屏幕空间技术做对"的工程记录。

## 主要贡献

- **[[temporal-sao-reprojection|Temporal Reprojection and SAO]]**（2015）——把 SAO (Scalable Ambient Obscurance) 纳入 TAA 历史采样的工程细节。
- **[[stingray-volumetric-clouds-plugin|Stingray Volumetric Clouds plugin]]**（2016）——HZD 方法的 Stingray 开源实现，附带对 Bayer vs blue-noise 采样、天气系统、Beer-Powder 光照等的一手权衡。代码 [github.com/greje656/clouds](https://github.com/greje656/clouds) 可读。
- **[[reprojected-planar-reflection|SSR reprojection]]**（2017）——把 SSR 放进 TAA 管线时需要做的重投影修复。
- **[[physically-based-lens-flare|物理 lens flare]]**（2017）——Hullin et al. 论文在 Stingray 里的实现。

## 风格

Jp 的博客在 Bitsquid 那一批里偏"方法复刻 + 权衡暴露"——不发明新算法，但把业界公开方法在真实引擎里落地时踩的每一个坑都写出来（tiling artifact 怎么调、Bayer 为什么比 blue noise 适合 cache、每 ray step 采样 weather map 贵在哪里）。这种"复刻档案"在缺乏中间层工程细节的图形论文文献里格外有价值。

## 相关

- [[niklas-frykholm]]
- [[stingray-data-driven-render-config]]
- [[temporal-sao-reprojection]]
- [[stingray-volumetric-clouds-plugin]]

## Sources

- [[sources/bitsquid-volumetric-clouds]]
- [[sources/bitsquid-temporal-sao]]
- [[sources/bitsquid-reprojecting-reflections]]
