---
tags: [source, 渲染, shader, 后处理]
date: 2026-04-14
sources: 1
---

# Mini: Texels and Pixels（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 8 月的 Mini 系列首篇，用放大镜后处理作例子讲**纹素（texel）和像素（pixel）之间的坐标换算**——在 fragment shader 里反复要做的一件事。

## 摘要

片元 shader 拿到的 UV 是 `[0,1]` 的归一化纹理坐标，而距离、半径这些视觉效果天然是**以像素为单位**思考的。Xor 给出最朴素的换算方案：在 CPU 侧传入 `u_texel = (1/room_width, 1/room_height)` 作为"一个纹素占多少归一化空间"的 uniform，shader 里用 `UV / u_texel` 换算成像素坐标做效果，再乘回 `u_texel` 去采样。教程拿放大镜做 demo：计算像素到鼠标的矢量、按距离做线性衰减、把这个偏移加回像素坐标。整套数学只涉及一次除法和一次乘法，但把"到底在哪个坐标空间里"这件事讲透了。文末指出复杂场景（旋转、缩放、图集纹理）要走矩阵和逆矩阵，不在本教程范围内。

## 关键要点

- **pixel = 屏幕空间单位**，**texel = 纹理空间单位**，一般情况不等价。
- `u_texel = 1 / screen_size` 是最简换算因子。
- `pixel = UV / u_texel`，反向 `UV = pixel * u_texel`。
- 放大镜伪代码：`to_mouse = pixel - u_mouse; attenuation = max(1 - length/100, 0); pixel -= to_mouse * attenuation * 0.5;`。
- 旋转、倾斜、纹理图集情况要靠矩阵换算，不是简单除法能搞定的。

## 链接到的概念

- [[texel-pixel-conversion]]
- [[fragment-shader]]
- [[coordinate-spaces]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-texels-and-pixels-1308242
- 本地：`raw/articles/mini.gmshaders.com/2022-08-12_mini-texels-and-pixels.md`
