---
tags: [source, 2d, 反射, 像素美术, 老游戏]
date: 2026-04-14
sources: 1
---

# Divine Divinity: 2D 反射（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 2013 年写的一篇短文，印象派地夸一下 *Divine Divinity* 在 2D 画面里做出看起来很不可思议的**水面反射**——连小兔子这样的动态物体都能被反射出来。这是 Simon 博客里少有的「我也不知道是怎么做的」文章，技术讨论停留在读者互相猜测的层面。

## 摘要

Divine Divinity 是一款斜 45° 2.5D 视角的 ARPG，水面上可以看到岸边物体被倒影。Simon 没看到过其他 2D 游戏这么做。评论区里一位读者给出了看起来最合理的猜测：**地图在水面位置留了「洞」，把物体的 sprite 以 pivot 为轴垂直镜像一份放在洞的背后；再在上面叠一层「水纹」tile、并用一个类似 Genesis 时代的行扫描变形让水面有波动**。Simon 自己只能说「看起来很聪明」，承认没有更多证据。后面也有读者指出 *Tales of Phantasia*（SNES）更早就做过类似效果——所以这不是 Divine Divinity 的原创，只是 Simon 第一次注意到。

文章的价值不在于拿出一个确切的技术答案，而在于展示 [[simon-trumpler|Simon]] 博客的**典型工作流**：看到一个好看的细节 → 在博客上晒出来 → 邀请读者 / 原作者在评论区补齐真相。本批次其他文章几乎都是这种「多方拼图」的姿态。

## 关键要点

- 2D 游戏也能做出说服力很强的反射，用的不是 shader 而是**美术资产的空间组织**：sprite 镜像 + 额外 tile 层 + 像素变形
- 动态对象（玩家、小动物）之所以能被反射，是因为 sprite 系统直接复制运行时的 sprite 位置
- 没有所有元素都反射——石头、草等做了剔除，和 3D 渲染里为性能放过次要对象是同一思路
- *Tales of Phantasia*（SNES）是更早的已知案例，说明这是 16/32-bit 时代的「传承技巧」

## 缺口 / 未解明

- Simon 未能联系上 Larian Studios 的原作者求证，讨论停留在推测
- 水面变形的具体实现（quadrant 分块 vs. 纯逐行扫描）未定论

## 链接到的概念

- [[planar-mapping]]
- [[alpha-blending]]

## 原文

- 链接：https://simonschreibt.de/gat/divine-divinity-2d-reflexion/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-4.md`
