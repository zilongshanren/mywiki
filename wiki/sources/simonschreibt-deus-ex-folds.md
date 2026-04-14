---
tags: [source, 渲染, parallax, 布料, deus-ex]
date: 2026-04-14
sources: 1
---

# Deus Ex 3: Folds（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年 1 月的 Game Art Tricks 短文，逆向研究《Deus Ex: Human Revolution》开场那面**缓缓滚动褶皱**的奥运风旗，最后在评论区的帮助下得出：没有顶点动画、没有 UV 动画，而是**带动画噪声的 parallax mapping**。

## 摘要

Simon 第一眼以为是 UV 动画 + 滚动法线贴图，用 Intel GPA 抓帧后发现 wireframe 几乎没有顶点切分，UV 也基本不动。往内存里掏贴图、打开 debug 选项「关掉纹理过滤」后，他意外看到一张**非常低分辨率**的灰度噪声，像一堆大像素块。结合 JacqueChoi（polycount 上的留言者）的指点，他明白了：旗面 shader 是一个以**静态 object-space normal map 做底 + 动画的灰度噪声做高度场**的 parallax（bump offset）pipeline，**把高频细节交给双线性过滤而不是高分辨率贴图**。整套 trick 的成本是「每像素一次 parallax 采样」，却能在正面观看时骗出「布料正在被风吹」的感觉——代价是**从侧面看立刻穿帮**，mesh 是平的、没有任何厚度动画。评论区还把同类效果的同时代例子串了起来：Batman: Arkham City 的旗帜、Mirror's Edge 的脚手架防尘布（PhysX 关闭时走 animated parallax 路径，开启时切换到真布料模拟）。

## 关键要点

- 动画 parallax = 静态 object-space normal + 动画灰度 height noise + 运行时 bump offset
- 小尺寸 noise 依靠双线性过滤糊成「连续 half-sphere 凸起」，不需要烘焙高分辨率贴图
- Wireframe 和 UV 都是静态的——唯一在动的是采样用的高度场
- 侧面观看穿帮（没有真实的 silhouette 位移）
- Arkham City 的同类效果额外对 silhouette 做了 mask 修正；Mirror's Edge 根据 PhysX 开关切换 trick / 真模拟

## 链接到的概念

- [[animated-parallax-cloth-fold]]
- [[simon-trumpler]]
- [[parallax-occlusion-mapping]]

## 原文

- 链接：https://simonschreibt.de/gat/deus-ex-3-folds/
- 本地：`raw/articles/simonschreibt.de/2013-01-22_simonschreibt.md`
