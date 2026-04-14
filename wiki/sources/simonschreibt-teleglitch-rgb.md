---
tags: [source, 后处理, 色差, 屏幕效果, vfx]
date: 2026-04-14
sources: 1
---

# Teleglitch: RGB Flickering（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 2013 年的 Game Art Tricks，拆解 *Teleglitch* 传送器的**三通道独立偏移**故障特效。原作者（Deadlight 团队的同一位美术）出现在评论区亲自说明实现。

## 摘要

Teleglitch 在使用传送器的瞬间，全屏闪一下——红、绿、蓝三个通道**独立**地偏移，看起来像一台 CRT 故障或者一盘磁带失步。Simon 观察到 *Deadlight* 也用了类似的效果（右上角水箱位置）但作者未在 The Art of Deadlight 演讲里讲细节。

最有价值的内容在评论区：

- 一位读者给出技术命名上的区分——**光学色差**（模拟镜头）走黄/青、绿/品红对色，是径向确定性的；而 Teleglitch 这种**数字 RGB 错位**更接近 VHS / CRT 故障艺术，可以无规律闪烁
- Deadlight 的后处理作者本人现身说法：实现极其简单，就是让每个通道按不同 offset 采样；**偏移强度随像素到屏幕中心的距离增大**，用一张径向 gradient 做权重调制——屏幕中心保真、边缘加强，这意外地和真实镜头色差的视觉行为相符
- Crytek 的水面 shader 用它做「光的分离」，Black Mesa 把它当作受伤反馈

整篇文章体现 Simon 博客的典型价值：**作者本人在评论区给出真实答案**——这比纯粹的逆向拆解更权威。

## 关键要点

- RGB 通道独立偏移是最便宜的「故障艺术」后处理——三次纹理采样 + 一个径向权重
- 用径向梯度调制偏移强度能让数字化的故障特效意外地获得类似光学色差的自然感
- 光学色差（由折射率差导致）和数字 RGB 失步是两种视觉语言，配色和动态都不一样
- 游戏里这种效果常被用作「设备出错 / 角色受伤 / 跨维度跳跃」等非现实语境的视觉符号

## 链接到的概念

- [[chromatic-aberration-post]]
- [[crt-shader-effects]]
- [[urp-volume-post-processing]]

## 原文

- 链接：https://simonschreibt.de/gat/teleglitch-rgb-flickering/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-6.md`
