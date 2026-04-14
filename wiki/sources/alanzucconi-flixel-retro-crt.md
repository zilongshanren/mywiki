---
tags: [source, vfx, 复古, crt, flixel, as3, 后处理]
date: 2026-04-14
sources: 1
---

# Retro CRT Distortion Effect in Flixel 2.5（Alan Zucconi）

[[alan-zucconi]] 2012 年 1 月发表的早期博客文章，记录他给 [Flixel](http://flixel.org)（一个用 ActionScript 3 写的 Flash 时代 2D 游戏框架）做的一个轻量 **CRT 通道偏移**后处理类 `RetroEffect`。这是站点最早的技术帖之一，比他后来在 Unity 上的 Surface Shader 教程系列早了好几年，内容相对单薄但思路与今天 [[crt-shader-effects|CRT shader 拆解]]中"RGB 子像素错位"那一节是同一类做法——只是当时没有 GPU shader 可用，全部在 CPU 上的 `BitmapData` 上跑。

## 摘要

文章灵感来自 Cadin Batrack 在 ActiveTuts+ 上的一篇 "Create a retro CRT distortion effect using RGB shifting" 教程。Batrack 的版本依赖 [Tweener](http://hosted.zeh.com.br/tweener/docs/en-us/) 缓动库做通道运动，效果好但开销大。Zucconi 的改进版去掉 Tweener，用一个简单的 `sinusoid(_counter + phase, min, max, freq)` 让三个通道沿正弦轨迹**自驱动振荡**，在 60 FPS 下也能跑得动。实现思路是：用 `BitmapData.copyChannel` 分别提取相机帧缓冲的 R、G、B 三个通道到一张临时 buffer，每个通道配一个稍微不同的 `Matrix`（缩放分量 `a`、`d` 用相位错开 1/5、2/5 的正弦在 `[0.99, 1.00]` 与 `[1, 1.01]` 之间漂移），然后用 `BlendMode.SCREEN` 把三个通道叠回 `_output` BitmapData 上。R 通道用 normal blend 打底，G/B 用 SCREEN 累加。最终把这张 BitmapData 当作 sprite 加入 FlxG.camera 之上。

整篇文章 100 多行，附带可下载的 `.rar` 源码包（已失效或仅在 archive 上）。它的价值不在算法新颖，而在记录了 **shader 时代之前、CPU bitmap 像素拷贝时代** 复古效果的典型实现：在没有 fragment shader 的 Flash 平台上，用 `copyChannel` + `Matrix` + 软件 blend mode 就是当时唯一能做的事。

## 关键要点

- **本质同 CRT shader**：把单帧拆成 R/G/B 三通道、各自做轻微仿射偏移再叠回去，正是今天 fragment shader 里 RGB split / chromatic aberration 的 CPU 等价物，参考 [[chromatic-aberration-post]]、[[crt-shader-effects]]
- **CPU bitmap pipeline**：`BitmapData.copyChannel` + `BitmapData.draw(_, matrix, _, blendMode)`——Flash 时代 2D 框架的"软件后处理"标配，后来的 Stage3D 才让 Flash 也能跑 GPU shader
- **Matrix 缩放代替偏移**：通道错位是通过缩放矩阵 `a` / `d` 的小幅振荡（±1%）实现，而不是直接平移——这等价于让通道从中心往外微微"呼吸"
- **正弦相位错开**：三通道用 `_counter + 0/5`、`_counter + 1/5`、`_counter + 2/5` 三个相位采样同一个 `sinusoid()`，是最便宜的"自动循环动效"做法
- **alpha 抖动**：`_bitmap.alpha = randRange(8, 10) / 10`——每帧给通道随机一点 0.8~1.0 的 alpha，模拟老 CRT 的亮度不稳定
- **BlendMode.SCREEN 叠通道**：因为通道是单色 R/G/B，加性叠加（SCREEN ≈ inverse-multiply）刚好还原成三通道彩色图

## 局限 / 历史定位

文章本身没有讨论扫描线、CRT 弯曲、子像素结构、滚动条等更完整的 CRT 视觉元素，只有最基本的"通道错位 + alpha 闪烁"。从今天角度看更像是 [[chromatic-aberration-post|色差后处理]]的雏形，而不是完整的 CRT 模拟。它的意义在于补完了 [[alan-zucconi]] 早期作为 Flash 游戏开发者的轨迹——他后来转向 Unity / shader 教学的整条线索从这里就能看到端倪。

## 链接到的概念

- [[crt-shader-effects]]
- [[chromatic-aberration-post]]
- [[alan-zucconi]]

## 原文

- 链接：<https://www.alanzucconi.com/2012/01/31/retro-crt-distortion-effect-in-flixel-2-5/>
- 本地：`raw/articles/alanzucconi.com/2012-01-31_retro-crt-distortion-effect-in-flixel-2-5-alan-zucconi.md`
