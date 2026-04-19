---
tags: [source, godot, shader, hologram, gradient, unscaled-time]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Gradient（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版四种变体之一，主视觉是**沿 Y 轴的双色渐变**。

## 摘要

Gradient 变体把 Base Color 与 Base Color 2 沿 *Gradient Space*（Object、World 或 Screen）之一的 Y 轴在 *Gradient MinMax Y* 两阈值之间线性插值——底色到顶色，外加可独立设置的 *Fresnel Color 2* 给 Fresnel 边缘同样做双色渐变。另一个值得注意的参数是 **Use Unscaled Time**：Godot/Unity 都没有直接向 shader 提供 unscaled time，需要从脚本每帧推一个 `_UnscaledTime` uniform 上去；打开这个开关后即使游戏调低了 `Time.timeScale`（例如进入子弹时间），全息的 glitch 扫描依然按真实秒数节奏进行，不会"慢动作化"。

## 关键要点

- 渐变空间三选一（Object / World / Screen）——同一套美术资源能在不同观察方式下复用。
- Fresnel 也支持双色渐变，使边缘辉光与主体颜色统一。
- **Unscaled Time** 问题：引擎未内置，必须脚本注入；慢动作场景不想被一起变慢的效果都要这条路。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/gradient/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-gradient.md`
