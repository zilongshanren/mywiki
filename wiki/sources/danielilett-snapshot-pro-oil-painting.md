---
tags: [source, 渲染, unity, urp, 后处理, kuwahara, stylized, non-photo-realistic]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Oil Painting（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍基于 Kuwahara 滤镜的油画风格后处理。

## 摘要

Oil Painting 是 [[kuwahara-filter|Kuwahara 滤镜]]的产品化封装：对全屏做一次保边去噪，去掉纹理细节但保留边缘，出来就是平坦色块+锐利过渡的"油画/笔触"效果，和 [[sources/danielilett-image-effects-kuwahara|Image Effects Part 6]] 同算法。参数只暴露一个 `Kernel Size`——既控制效果强度、也控制每像素采样次数（每像素要扫四个重叠子区域，`4*(r+1)²` 次采样，3x3 就是 36 次，5x5 就是 100 次，代价随 kernel 平方增长）。比其它 Snapshot Pro 档要贵得多，移动端慎用。场景选型上，纹理杂乱高对比的画面效果最好（每笔都能"找到"稳定色块），平坦场景就退化成普通均值模糊。

## 关键要点

- 单参数 `Kernel Size`——同时控制强度与每像素代价
- 代价是 `O(r²)` 级，不可分离（区域选择依赖方差比较）
- 移动端限制：`Kernel Size` 建议 3 或 5 封顶
- 适合纹理丰富高对比场景，平坦画面退化成均值模糊
- 不处理各向异性方向感——进一步风格化可上 anisotropic Kuwahara（Papari 2007）

## 链接到的概念

- [[kuwahara-filter]]
- [[separable-gaussian-blur]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/oil-painting/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-oil-painting.md`
