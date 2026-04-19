---
tags: [source, unity, urp, hdrp, shader, hologram, glitch, fresnel]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Glitch（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的纯 glitch 变体参数手册，对应 Godot 版的 Glitch 子 shader。

## 摘要

Glitch 变体不附加任何主视觉装饰，主体就是两类几何 glitch 的叠加：**Vertex Glitches**——按 *Glitch Sensitivity* 阈值随机挑顶点，沿法线方向外推 *Glitch Strength* 距离，*Glitch Normal Multiplier*（如 `(1,0,1)`）限制推移平面，*Glitch Offset* 给出相位差使多实例不同步，*Glitch Frequency* 控制触发频率；**Segment Glitches**——沿 Y 轴扫描宽 *Slice Width* 的水平切片，切片内顶点沿 *Slice Direction* 被整体平移 *Slice Duration* 时间，*Slice Speed / Frequency / Jitter* 分别控制扫描速度、触发频率与抖动幅度（默认封顶 0.2 防闪屏）。PBR 底座与 Fresnel（*Fresnel Power / Color*、*Use Scene Intersections + Intersection Power*）与其余 Pro 变体一致。参数对齐 Godot 版，本页仅作产品文档归档。

## 关键要点

- Glitch 变体定位为"故障感但不要几何装饰"的场景——没有 dot/grid/gradient 叠加
- Vertex vs Segment 两个 glitch 子系统**正交且可独立开关**，是 Ilett 把美术特效模块化的样板
- "可调概率 + 可调强度 + 可调相位"三件套（Sensitivity / Strength / Offset）在两类 glitch 里都体现——产品化随机特效的核心接口
- Fresnel 子模块在所有 Pro 变体中完全一致，包含 [[depth-intersection-subgraph|深度相交]] 辉光

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[fresnel-edge-highlight]]
- [[depth-intersection-subgraph]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/glitch/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-glitch.md`
