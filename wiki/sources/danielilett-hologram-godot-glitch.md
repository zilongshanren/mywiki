---
tags: [source, godot, shader, hologram, glitch, fresnel]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Glitch（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版四种变体之一，把"纯故障感"作为主视觉，不叠加 dot / grid / gradient 中的任何屏幕装饰。

## 摘要

Glitch 变体在共享 PBR 基座之上只保留两件事：**Vertex Glitches**（按顶点随机概率把顶点沿法线外推 *Glitch Strength*，可用 *Glitch Normal Multiplier* 限制在特定平面，*Glitch Time Offset* 让不同材质实例相位错开）和 **Segment Glitches**（沿 Y 轴扫过一条 *Slice Width* 高的水平切片，把切片内顶点沿 *Slice Direction* 短暂平移）。再加 **Fresnel** 边缘辉光，可开 *Use Scene Intersections* 在贴近其他不透明物体时叠加 intersection glow。形态上非常接近"电视信号出错 + 低带宽全息"的科幻画面。

## 关键要点

- Vertex + Segment glitch 是全系变体共享的骨架模块。
- Segment glitch 的"扫描 + 抖动"组合用 Slice Speed / Slice Jitter / Slice Duration 控制。
- Fresnel + Intersection 是[[fresnel-edge-highlight|菲涅尔边缘]]与[[depth-intersection-subgraph|深度相交]]的产品化组合。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[fresnel-edge-highlight]]
- [[depth-intersection-subgraph]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/glitch/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-glitch.md`
