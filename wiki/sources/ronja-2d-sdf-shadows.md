---
tags: [source, rendering, shader, sdf, 阴影, raymarching]
date: 2026-04-14
sources: 1
---

# 2D SDF Shadows（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 12 月发表的 Ronja SDF 系列进阶篇，讲如何在一个用 SDF 描述的 2D 场景里对每个像素 raymarch 到光源方向，得到硬阴影与软阴影。

## 摘要

硬阴影部分展示了标准的 sphere tracing 结构：对每个像素从光源方向发射射线，沿着 `t += scene(p + dir * t)` 推进——这个步长保证永不跳过最近物体。命中（`d <= 0`）返回 0，越过光源返回 1，耗尽 `SAMPLES = 32` 的预算返回 0 作兜底。软阴影的升级只需一行改动：把 `return 1` 换成 `saturate(min_over_ray(shadow))`——沿射线取最小 scene 距离作为阴影量，等同于 [iq 的经典 soft shadow trick](https://iquilezles.org/articles/rmshadows/) 的 2D 版。初版会出现「齿状 artefact」和「均匀软度」两个问题，Ronja 用两处调整修好：`hardness * d` 收紧软边并配合 `d / rayProgress` 让阴影**在起点锐、远端软**——这对应真实物理里 penumbra 随距离加宽的现象。还有一个细节：在 `rayProgress` 上加最小步长 `max(d, 0.02)` 防止光源贴近几何时 raymarch 空转出虚假阴影圈。多光源就是简单地对每盏灯独立 raymarch 再线性叠加。全篇最漂亮的点是**不需要任何滤波**——柔边是从 `min(d / t)` 这个单变量里自然涌现的，单次 raymarch 就算完。

## 关键要点

- **sphere tracing 在 2D 降维一样成立**：`t += d` 保证步长不跨越最近物体。
- **SDF 软阴影的单行技巧**：`shadow = min(shadow, hardness * sceneDist / rayProgress)`——沿射线最小距离 + 随距离软化，几乎零额外成本。
- **除以 `rayProgress` 是关键**：起点紧致、末端渐软，模拟 penumbra 随距离扩张的物理现象。
- **最小步长 `max(sceneDist, 0.02)`** 防止光源贴近几何时 raymarch 陷入空转。
- **多光源 = 独立 raymarch + 线性叠加**：简单粗暴但 O(lights)——适合 2D 灯数少的场景。
- 算法**可原样升维到 3D SDF 场景**——只改类型和场景函数，是 SDF 家族罕见的「2D 即 3D」一致性。

## 链接到的概念

- [[sdf-ray-marched-shadows]]
- [[sdf-2d-primitives]]
- [[shadow-mapping-basics]]
- [[jump-flooding-algorithm]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/037-2d-shadows/>
- 本地：`raw/articles/ronja-tutorials.com/2018-12-01_2d-sdf-shadows.md`
