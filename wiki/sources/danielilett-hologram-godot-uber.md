---
tags: [source, godot, shader, hologram, uber-shader, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Uber（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版的"全功能"变体：把 Scanline、Glitch、Noise 三种子模块合并到同一份 shader 里，配合布尔开关按需启用。

## 摘要

Uber 变体把此前分散在各单独 shader 中的三个主装饰层——扫描线、glitch（顶点 + 切片）、胶片噪点——塞进同一份材质，每个子系统都带 *Use XXX* 布尔开关以允许美术从同一材质实例切换不同风格组合。作者明确指出：单独 shader 仍然保留，因为"只要一种效果时，单独 shader 更便宜"——这是把 **uber shader vs 多 shader 变体** 的经典取舍摆到了产品化层面（参见 [[shader-combination-strategies]]）。Uber 额外引入一个并非视觉装饰但工程上重要的子系统——*Use Unscaled Time*：当 `Time.timeScale` 被改动（慢动作、暂停菜单）时，shader 是否依然按真实时间滚动。Godot/Unity 都没有内置 unscaled time uniform，必须由脚本每帧推送——这个细节在任何"暂停时依然要 UI 全息动画"的场景都绕不开。

## 关键要点

- **Uber shader 取舍**：通用 + 一键切换 vs 每种变体独立编译更便宜。
- *Use Unscaled Time* 是**脚本 → shader 约定**，不是 shader 能自给自足的数据。
- 所有子系统（scanline / vertex glitch / segment glitch / noise）都有独立启用开关，配合 [[shader-combination-strategies|关键字组合策略]] 可退化为更便宜的 shader。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[godot-visual-shaders]]
- [[shader-combination-strategies]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/uber/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-uber.md`
