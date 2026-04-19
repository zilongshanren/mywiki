---
tags: [渲染, 后处理, uv-distortion, polar-coordinates, urp]
date: 2026-04-19
sources: 1
---

# 漩涡扭曲后处理（Vortex Distortion）

漩涡扭曲把屏幕图像围绕一个中心点做**旋转量随半径变化**的 UV 位移，视觉上像水面被搅动、传送门开启、或是魂系游戏里玩家被吸入 boss 召唤阵——一个非常廉价的"空间被卷曲"信号。Daniel Ilett 的 *Snapshot Shaders Pro* 把它做成一个 URP Volume override，参数只有三个：`Strength`、`Center`、`Offset`。

## 数学：极坐标下加一个半径相关的角度

直角坐标下做旋转扭曲并不直观，转成**极坐标**后就是一行代数。给定中心 `c`，屏幕 UV 经过 `uv - c` 后变成以中心为原点的向量 `p`，令：

```
r     = length(p)
theta = atan2(p.y, p.x)
theta = theta + strength * f(r)      // 关键一步
p'    = float2(cos(theta), sin(theta)) * r
uv'   = p' + c
```

`f(r)` 是漩涡的"形状函数"——最常见是 `f(r) = r`（线性，外圈比内圈转得多）或 `f(r) = 1/r`（内圈急转、外圈平缓，更像真实流体的 [Rankine vortex](https://en.wikipedia.org/wiki/Rankine_vortex)）。Snapshot Pro 的 `Strength` 参数就是在调这个乘数，`Offset` 把 `p` 预先偏移（相当于同时旋转和平移）。

## 为什么走屏幕空间

漩涡本身是**纯 2D 的 UV 重映射**——不需要场景深度、不需要法线、不需要几何变形，只要把屏幕缓冲当作一张贴图重采样就够。这也是 [[urp-volume-post-processing|URP Volume]] override 的典型用法：一个 fragment 通路、一张 screen color 输入、一张改过 UV 的输出。

代价是"假得彻底"——漩涡不会把物体边缘真的弯曲（屏幕里边缘像素外的信息没了），贴近屏幕边缘时会出现**拉边伪影**，常见的遮丑方式是在外圈做 `vignette`（径向衰减到未扭曲的原图）或让漩涡占满屏幕中央一块、边缘保留原画面。

## 和相关效果的关系

- [[underwater-post-effect]] 的 flow map 是**非均匀**的 UV 扭曲，位移由贴图决定；漩涡是**结构化**的 UV 扭曲，位移由极坐标公式决定——两者可以叠加。
- [[chromatic-aberration-post]] 常被搭配在漩涡上——给 R/G/B 三通道各自用略微不同的 `Strength`，产生"漩涡越强、色差越明显"的效果。
- Portal 风格、穿越动画、受击镜头都可用 `Strength` 随时间插值来驱动一次性漩涡脉冲。

## 相关

- [[urp-volume-post-processing]] —— 所依附的 Volume 系统
- [[underwater-post-effect]] —— UV 扭曲的另一路径（flow map）
- [[chromatic-aberration-post]] —— 与漩涡叠加常见

## Sources

- [[sources/danielilett-snapshot-pro-vortex]]
