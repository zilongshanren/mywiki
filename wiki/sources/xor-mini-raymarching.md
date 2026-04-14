---
tags: [source, 渲染, shader, raymarching, sdf]
date: 2026-04-14
sources: 1
---

# Raymarching（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 9 月的一篇，入门级介绍 **sphere-assisted ray marching**——shader 爱好者最常用的 raycasting 算法之一。以一个 8 行的 raymarcher 为核心，外加 SDF 基础、射线方向构造、SDF 合成技巧的速写。

## 摘要

Raymarching 的基础是 **Signed Distance Field**：`sphere_distance(p) = length(p) - 1.0` 这样一个「返回到最近表面距离」的函数。单球、多球、反相、差集、无限复制全部通过 `min`、`max`、`mod` 的函数组合完成。有了 SDF 就能实现 sphere tracing——每次迭代把步长设为当前 SDF 值，保证永远不穿越表面，100 次循环已经足够逼近大部分表面。文章给出了完整的 `raymarch()` 函数（包括 `EPS` 早停和 `MAX` 截断）、ray direction 的构造（像素坐标 + focal = resolution.y）、以及可视化深度的最小示例。文末的 SDF 小技巧清单（反相、无限复制、iq 的基元库链接）让读者能立刻搭出自己的场景，是非常典型的 Xor 式「一页纸讲清楚一个技术」的教程。

## 关键要点

- **SDF = 距离函数**，外部正、表面零、内部负；`min` 并，`max` 交，`max(a, -b)` 差。
- **Sphere tracing**：`d += distance_field(pos + dir*d)`，每步走一个安全球半径；100 次迭代足够。
- **早停优化**：`if (step_dist < EPS || d > MAX) break;`
- **Ray 方向**：`normalize(vec3(pixel.xy - 0.5*res.xy, res.y))`，`res.y` 作为焦距决定 FOV。
- **SDF 组合技巧**：无限平铺 = `length(mod(p, 8.0) - 4.0) - 0.5`，反相 = `30.0 - length(p)`。
- **下一步**：法线（SDF gradient 中心差分）、soft shadow（iq 的 `min(shadow, k*d/t)`）、glow、AO——都超出本教程但列出参考链接。
- 推荐深入阅读：[Inigo Quilez 的 distfunctions 文章](https://iquilezles.org/articles/distfunctions/)。

## 链接到的概念

- [[raymarching-intro]]
- [[sdf-2d-primitives]]
- [[sdf-ray-marched-shadows]]
- [[volumetric-raymarching-intro]]
- [[fragment-shader]]
- [[pinhole-camera]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-raymarching-1351092
- 本地：`raw/articles/mini.gmshaders.com/2022-09-16_raymarching.md`
