---
tags: [source, 渲染, 法线贴图, 精度, X-Plane]
date: 2026-04-19
sources: 1
---

# The Limits of 8-bit Normal Maps（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2011 年 5 月 7 日的笔记，主题是为什么 8-bit 切线空间法线贴图在高 specular exponent 下会出现可见的法线量化台阶。

## 摘要

X-Plane 美术把 specular 高光收紧后，切线空间 RG8 法线贴图的角度精度开始成为瓶颈。Supnik 画出 `N·L` 衰减曲线在 `^128 / ^1024 / ^4096` 三个 exponent 下的形状：exponent 越高越像放大镜，把法线微小偏移放大到 2–8 个亮度级的跳变，表现为高光区的分档色带。线性光照会让问题在某些情形变严重，HDR specular 叠加后观感再坏 2–3 倍。Supnik 列出的缓解手段有四：CryTek best-fit normals 之类的 RGB8 压缩；升 RG16；把 B 通道当作指数让贴图变成「8.8 浮点」（Supnik 正在 X-Plane 上试这条路）；对 RG 加全局 gamma 曲线（他判断不会产品化）；以及最实诚的「告诉美术别这么用」。核心教训：切线空间贴图大多数像素扰动很小，**精度最需要堆在 near-zero 附近**——选择编码时要顺着这个分布走，而不是把动态范围均摊。

## 关键要点

- Specular exponent 是法线误差的放大器，`^4096` 下一个最小单位偏移就毁掉平滑 ramp
- Linear lighting + HDR 会再放大 2–3×
- 缓解路径：BFN / RG16 / B 通道存指数 / RG 全局 gamma / 劝退美术
- 设计原则：精度应偏向低扰动区（切线空间法线的真实分布）
- 与 G-Buffer 法线编码是独立问题：贴图侧和 G-Buffer 侧各自独立选

## 链接到的概念

- [[8-bit-normal-map-precision-limits]]
- [[compact-normal-encoding]]
- [[tangent-space-normal-mapping]]
- [[linear-lighting-pipeline]]
- [[color-banding]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/limits-of-8-bit-normal-maps.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-07_the-limits-of-8-bit-normal-maps.md`
