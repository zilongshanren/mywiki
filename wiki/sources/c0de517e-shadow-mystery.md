---
tags: [source, 渲染, 阴影, normalmap, 光照, 视觉幻觉]
date: 2026-04-27
sources: 1
---

# Shadow Mistery（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2017 年 5 月的短篇调查笔记，记录了一个令人困惑的 bug：法线贴图表面在阴影切换时看起来像「纹理移动了几像素」。

## 摘要

这篇帖子起因是一个工程师报告了一个奇怪的 bug——表面在光线切换时纹理似乎发生了位移。Pesce 用 Mental Ray 离线渲染验证，确认这是一个可复现的光学幻觉：在常量 albedo 的曲面上，表面的「纹理感」完全来自高光和阴影。当主光源被遮挡（进入阴影）后，主高光消失，而 ambient 光产生的对面高光开始主导——高光重心发生了跳变，人眼把它解读为纹理在「移动」。

关键放大因素有两个：其一，实时渲染的 ambient/GI 通常不带阴影（unshadowed），所以主光被遮时 ambient 高光没有相应的过渡；其二，shadow map 造成硬切，没有半影过渡来缓和高光方向的突变。Pesce 最终在真实物体上也复现了同样的幻觉，证明这是物理上真实存在的错觉，只是被实时渲染的两个近似（不遮蔽的 ambient 和硬阴影边缘）放大了。

## 关键要点

- 「纹理位移」幻觉本质是高光重心随光照状态跳变，与 normalmap 细节和人眼对高光的感知有关。
- 实时 ambient/GI 不参与阴影是放大因素：主光被遮时 ambient 高光独大，幻觉最明显。
- 软阴影（penumbra 区域）能缓解这一幻觉，因为高光方向的转变是渐进的而非硬切。
- 这是一个短小的「思考笔记」类文章，无深入推导，价值在于指出一个容易被当成 bug 的视觉感知问题。

## 链接到的概念

- [[shadow-mapping-basics]]
- [[normalmap-mipmap-aliasing]]
- [[cascaded-shadow-maps]]
- [[angelo-pesce]]

## 原文

- 链接：http://c0de517e.blogspot.com/2017/05/shadow-mistery.html
- 本地：`raw/articles/c0de517e.blogspot.com/2017-05-06_shadow-mistery.md`
