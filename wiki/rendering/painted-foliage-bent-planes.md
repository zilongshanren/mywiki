---
tags: [渲染, 树木, 植被, alpha, 美术技巧, diablo]
date: 2026-04-14
sources: 1
---

# 画在弯折 Plane 上的植被（Painted Foliage on Bent Planes）

**Diablo 3 的树**被 Simon Trümpler 单独拎出来讲，不是因为它用了什么特别复杂的 shader，而是因为它的**剪影**——也就是树枝和树干在画面上与背景相接的那条边——细到几乎看不到锯齿，而同一画面里用「正经 3D 模型」的物体反而 aliasing 明显。Blizzard 美术的解法看起来非常古典：**用两张三角形，贴一张带 alpha8 遮罩的画**。

## 为什么 2D 贴面反而比 3D 模型看起来更好

树的复杂之处不在体积，而在**外轮廓**——每一根细枝在天空上的那条边。如果用几何来表示，要几千个三角形才能把那些细碎的缺口刻出来，然后还要担心光照、LOD、draw call。而用一张手绘贴图，把树枝直接画在 alpha 通道里，**轮廓的细节被压进了纹理分辨率**；只要 [[sampler-filter-wrap-modes|bilinear 采样]] 够好，甚至比几何边多了一点天然的抗锯齿过渡。两张三角形的代价——两次顶点变换、一次纹理采样——远低于几千个面。

Diablo 3 的做法是把这两张 quad **稍微弯折**一下，让它们不是纯粹的平面，而是一个轻微 cylindrical 的壳。从 ARPG 固定的斜俯角看过去，弯折让树有一点体积感，同时因为镜头**不旋转不放大**，玩家永远不会看到它从侧面或背面崩穿。这是一个典型的「**gameplay 约束反哺艺术技巧**」的案例：Blizzard 知道这是 isometric ARPG，相机不动，于是就敢把 3D 简化成一张画。

## 细节的来源

Simon 从 MPQ 里导出 Diablo 3 的 `.APP` 模型后发现，每个树都不是「一张大 plane」，而是若干个小弯片拼起来的：树干一段弧、几段主枝一段弧、一些叶簇各一段弧。美术显然是先搭一个低多边形基础，再在上面反复绘制、并复用纹理 atlas 里的叶片块。这意味着这种技巧并不是「bake highpoly to plane」，而是一种「**先是雕塑，然后把雕塑抹成绘画**」的工作流。

## 代价与约束

这种技巧有两个硬约束：

1. **静态视角**——一旦相机可以自由旋转或者显著缩放，贴片之间就会穿帮。Diablo 3 的相机非常克制。
2. **静态光照**——因为树只是一张画，它没有真的几何来接受动态光。动态光会让画面与场景脱离。讨论区里就有人问「如果有动态光怎么办」，Simon 的回答是：只能接受静态光照，或者额外准备一套 shadow geometry（可能是把同一弯片根据光源方向内部旋转一次）来投阴影。

这两条约束在 ARPG / RTS / 固定镜头解谜里几乎是免费的，在第一人称 / 第三人称游戏里就变成毒药——这也解释了为什么即便 Diablo 3 展示得如此之好，这种做法并没有在其他品类流行起来。

## 与其它「不画几何」的技巧的家族关系

这是**「用纹理 / 绘画替代几何细节」**这一大类美术技巧里的一员，亲戚包括：

- **impostor / billboard**：远处的树塌缩成一张朝向相机的平面，仍是 3D 流程
- **parallax / relief mapping**：用 heightmap 把 flat 几何在 pixel shader 里「拱」出凹凸
- [[normal-decal-edge-blending|法线 decal 覆盖硬边]]：低多边形几何的硬边用贴片+normal map 隐藏
- [[deferred-grass-shader|延迟草的 vertex billboard]]：在顶点着色器里展开 quad

区别在于 Diablo 3 的做法**彻底放弃了动态视角**换取剪影质量，而 impostor 等仍在为「能转相机」服务。

## 相关

- [[dither-alpha-clipping]] — alpha test / clipping 是这类贴面渲染的标准配件
- [[normal-decal-edge-blending]]
- [[planar-mapping]]

## Sources

- [[sources/simonschreibt-diablo3-trees]]
