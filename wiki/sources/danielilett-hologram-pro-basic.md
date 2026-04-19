---
tags: [source, unity, urp, hdrp, shader, hologram, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro — Basic（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders Pro*（Unity URP/HDRP 商业插件）文档中最简形态的产品规格——Basic 变体。

## 摘要

Basic 是 Hologram Shaders Pro 的 Unity 版本入门款：只提供 PBR 基础参数（*Base Color / Texture / Normal / Metallic / Smoothness / Ambient Occlusion / Alpha Clip*）加一个 fresnel 边缘发光，不带任何 glitch、scanline、noise、dot/grid 装饰。相对 [[godot-hologram-shader-effects|Godot 版]] 的四种变体，Basic 展示了"底座共享参数"具体是什么。值得注意的技术差异：Unity 版额外暴露 *Metallic / Smoothness / Ambient Occlusion*，而 Godot 版没有，因为 Godot 的 material 底层处理方式不同。这个差异本身并不构成新的技术概念，只是 URP/HDRP 移植。

## 关键要点

- URP/HDRP 版本暴露 *Metallic / Smoothness / AO*，Godot 版未暴露。
- Fresnel 子模块与 Godot 版参数完全一致，说明作者保持了跨引擎 API 一致性。
- Basic 变体本身不包含任何 glitch / scanline / 装饰层，是最便宜的版本。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/basic/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-basic.md`
