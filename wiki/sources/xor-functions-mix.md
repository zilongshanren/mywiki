---
tags: [source, 渲染, shader, glsl, 插值]
date: 2026-04-19
sources: 1
---

# Functions: Mix（Xor）

[[xor-shader-artist|Xor]] 2025 年 8 月「Functions」系列第二篇，讲 `mix(x, y, a) = x*(1-a) + y*a` 的常用和不常用用法。

## 摘要

数学上 mix 就是线性插值，但 `a` **不强制在 [0, 1]**——这是被忽略的特性，让 mix 天然支持**extrapolation**。Xor 列了几个实用场景：(1) **saturation 控制**：`mix(vec3(luma), col, S)`，S=0 变灰度、S=1 原色、S>1 过饱和、S<0 取反色相；(2) **brightness + contrast**：`mix(vec3(B), col, C)`，把 B 写成三元组就是 per-channel gain，足以做色温调节；(3) **动画插值**：`mix(POS1, POS2, time)` + 缓动函数做运动；(4) **径向模糊**：`mix(uv, vec2(0.5), i*0.2)` 把 UV 拉向焦点——可读性远优于手写加法；(5) **texture atlas uv**：`mix(uvs.xy, uvs.zw, norm_uv)` 把标准化 uv 映到 atlas 子矩形；(6) **remap 函数**：`(x-a)/(b-a)*(d-c) + c`——可看成 mix 的反向+组合。最后提醒：RGB 空间的 mix **感知不均匀**，两种彩色相 mix 常变浑浊，改用 OkLab 空间做 mix 才视觉上均匀。

## 关键要点

- `a` **可以超出 [0, 1]** 做 extrapolation —— mix 的隐藏特性。
- **saturation / brightness / contrast** 都能一行 mix 写出。
- **mix 2.0** 即 remap：`(x-a)/(b-a)*(d-c) + c`。
- **感知均匀 mix** 需要切 OkLab。

## 链接到的概念

- [[glsl-mix-function]]
- [[oklab-color-space]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/func-mix
- 本地：`raw/articles/mini.gmshaders.com/2025-08-30_functions-mix.md`
