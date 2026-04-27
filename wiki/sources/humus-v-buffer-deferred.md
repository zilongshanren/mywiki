---
tags: [source, 渲染, visibility-buffer, deferred-rendering, light-prepass]
date: 2026-04-27
sources: 1
---

# V Buffer – Deferred Lighting Re-Thought（Wolfgang Engel）

[[people/wolfgang-engel]] 于 2015 年 5 月发表的文章，一句话主题：从 2008 年 Light Pre-Pass 出发，梳理 Tiled Deferred、Clustered、Forward+ 各管线的演化路径，论证 G-Buffer 在 4K / 高 DPI 设备上已不可行，并引出 Burns & Hunt 的 Visibility Buffer 作为下一步方向。

## 摘要

文章从 Engel 2008 年提出的 Light Pre-Pass 起笔：该方案在 Rockstar 多款游戏中使用，后被 S.T.A.L.K.E.R.、Naughty Dog 等采纳。其后 Tiled Deferred（Battlefield 3）通过 tile 排序大幅降低带宽，但静态开销抬高了盈亏平衡点（需数十盏灯才合算），而带阴影的灯又回到高带宽状态。Clustered Shading 进一步解决了"光源 overdraw"问题，而 Forward+ 则以重复提交几何为代价换取透明物体与不透明物体的光照一致性。Engel 的核心论点是：所有基于 G-Buffer 的方案在 1080p 以上分辨率都面临几何提交与像素 overdraw 的双重压力，根本出路是把**可见性判断与着色彻底分离**——以 Visibility Buffer（thin G-Buffer：per-pixel instance id + triangle id）替代传统 G-Buffer，只对真正可见的像素做一次材质 shading。

## 关键要点

- Light Pre-Pass 在 2008 年为 720p 时代设计，4K 时代其 G-Buffer 带宽代价成倍放大
- MSAA 进一步放大 G-Buffer 存储成本，而 Visibility Buffer 对 MSAA 的额外成本相对可控
- Tiled Deferred 的静态 tile 排序开销使其在少量灯光场景下得不偿失
- Clustered Shading 解决了三维光源分布，但几何提交问题未变
- Forward+ 以"几何提交多次"换"光照一致性"，高密度几何场景代价显著
- Visibility Buffer 把第一遍光栅化的开销压缩到极致（只写 id），完全杜绝 overdraw 浪费

## 链接到的概念

- [[visibility-buffer]]
- [[deferred-rendering]]
- [[tiled-light-culling]]
- [[tiled-light-prepass]]
- [[overdraw]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2015/05/v-buffer-deferred-lighting-re-thought.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2015-05-27_v-buffer-deferred-lighting-re-thought.md`
