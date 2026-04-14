---
tags: [source, 渲染, matcap, lit-sphere, fresnel, 风格化]
date: 2026-04-14
sources: 1
---

# World of Warcraft: Balloon（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年 1 月的 Game Art Tricks 短文，从《魔兽世界：熊猫人之谜》的热气球入手，讲了一项现在被广泛称作 **MatCap / Lit Sphere Shading** 的技术。

## 摘要

Simon 对熊猫人之谜里的热气球印象很深——气球中央有一团黄色的「热源辉光」，**无论你从什么角度看，这团辉光都保持在气球正中**，意味着它不可能是画在材质表面上的。他一开始猜是 [[fresnel-effect|Fresnel]] + mask，但用 DirectX Ripper 和 WoW Model Viewer 抓到资产后，发现 diffuse 贴图的 **alpha 通道**是一张二维径向渐变——这正是给 lit sphere shader 用的 lookup texture。技术由 Neox 确认为 **Lit Sphere Shading**：用物体法线在屏幕空间的 `(x, y)` 当 UV 直接采样预渲染球面图像，所以面向相机的表面采样到纹理中心的辉光，掠射处采样到外圈的暗色。这和 ZBrush 里的 matcap 是同一件事。后续一位叫 Charles Hollemeersch 的读者补上了**反向 Fresnel**的替代代码，把 lit sphere 的 2D 查找表简化成「`dot(N, V)` 作为辉光强度 + 一张 mask 定形状」的参数化版本，更便宜但表达能力略弱。评论里还提到 Half-Life 2 的 Antlion（酸蚁）和 Bioshock Infinite 的大气球都用过同一思路。

## 关键要点

- Lit Sphere / MatCap = 用 view-space normal 的 `xy` 作为 UV 去采样一张预渲染球图
- 面向相机的法线采样到纹理中心，掠射法线采样到纹理边缘——辉光永远在视觉中心
- 和 Fresnel 的关系：Fresnel 是 1D `dot(N, V)`，lit sphere 是 2D 全向——前者是后者的特例
- 反向 Fresnel 版本（`fresnel * color + bias * color * mask`）是 lit sphere 的低内存替代
- Half-Life 2 的 Antlion、WoW 热气球、Bioshock Infinite 的大气球都是同一家族
- 适用范围：物体**自身发光**、不需要响应场景光照时；接外光照就不合适

## 链接到的概念

- [[lit-sphere-matcap-shading]]
- [[fresnel-effect]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/world-of-warcraft-balloon/
- 本地：`raw/articles/simonschreibt.de/2013-01-24_simonschreibt.md`
