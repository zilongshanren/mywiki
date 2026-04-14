---
tags: [source, 渲染, unity, shader, mask, sdf]
date: 2026-04-14
sources: 1
---

# My take on shaders: Custom masks (Part II) (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列第五篇（2017-06-14），承接 [[custom-mask-shaders|Custom masks Part I]] 的圆盘 mask，把同一套技术改成**圆环 mask**，为下一篇的 [[shockwave-effect|冲击波]] 铺路。

## 摘要

文章只在圆盘 shader 的基础上改了三行：先算 `rd = _Thickness/2` 表示半厚，再算 `rc = _Radius - rd` 表示圆环中心带到圆心的距离，最后把 `saturate(dist / _Radius)` 改成 `saturate(abs(dist - rc) / _Thickness)`。关键的 mental model 是「`_Radius` 不是外半径，而是圆环最暗那一圈的半径」——所以判定一个像素是否在环上等价于「`dist` 距 `rc` 的偏离不超过 `_Thickness`」，用 `abs` 把环内外两侧合并、再归一化为柔边。Alisavakis 用了相当长的篇幅（自嘲「pseudo-pseudo-pseudocode」）把这个表达式从「dist 在 (rc, rc + thickness) 区间」一步步推到 `abs(dist - rc) < _Thickness`，把推导过程而不是结论放在前面，是这篇的教学价值所在。

## 关键要点

- 圆环 mask = 圆盘 mask 把「`dist < r`」改成「`|dist - r|` 小」的指示函数；同一族距离场表达式的两种取阈值方式。
- 新增 `_Thickness` 一个属性即可控制环的宽窄，其余参数（圆心 / 硬度 / 反转 / aspect 校正）和圆盘版完全一致。
- `_Radius` 的物理意义是「圆环最暗那一圈所在的半径」，不是外沿——文章用图说明，避免后续脚本控制 `_Radius` 时算错位。
- 这是 [[shockwave-effect|冲击波 shader]] 的直接前置。
- Alisavakis 重复了「单独看几乎没用，必须组合」的评论，强调它的价值在于积木属性。

## 链接到的概念

- [[custom-mask-shaders]]
- [[shockwave-effect]]
- [[sdf-2d-primitives]]
- [[image-effect-mask-blend]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-custom-masks-part-ii/>
- 本地：`raw/articles/halisavakis.com/2017-06-14_my-take-on-shaders-custom-masks-part-ii.md`
