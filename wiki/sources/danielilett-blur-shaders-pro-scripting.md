---
tags: [source, unity, post-processing, volume, scripting, urp, hdrp]
date: 2026-04-19
sources: 1
---

# Blur Shaders Pro — Scripting Guide（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为自家 *Blur Shaders Pro* 资产写的一页脚本接入指南，说明如何在 Unity 三条渲染管线里从脚本访问和修改挂载到 Volume 上的 Blur 效果参数。

## 摘要

文档按 URP、HDRP、Built-in 三个管线分别给出一段最简脚本示例。URP 和 HDRP 都用 `UnityEngine.Rendering.Volume` + `volume.profile.TryGet(out effect)` 的模式，区别仅在于 URP 按约定给每个 effect 类名加 `Settings` 后缀（`Blur` → `BlurSettings`）。Built-in 管线则回退到 Post Processing Stack v2 的 `UnityEngine.Rendering.PostProcessing` 命名空间，使用 `PostProcessVolume` 和 `volume.profile.TryGetSettings(out effect)`。示例都是拿到 effect 后直接修改 `strength.value` 和 `stepSize.value` 这类参数。文档本身是"产品手册"性质，内容薄，但把三管线 Volume API 访问范式的差异并列到一起很有参考价值。

## 关键要点

- URP / HDRP 共用 `UnityEngine.Rendering.Volume` + `TryGet`，API 对称但 URP 类名后缀 `Settings`（命名歧义来源）。
- Built-in 走 PPv2 `PostProcessVolume` + `TryGetSettings`——这是历史上 URP 抛弃的老系统（见 [[urp-volume-post-processing]]）。
- 参数修改统一走 `.value`，因为每个 parameter 都是 `VolumeParameter<T>` 的包装（为了支持 Volume 之间的插值混合）。
- 获取 effect 前必须保证挂载的 Volume 的 Profile 上已经有该 effect override；`TryGet` 失败时 `effect` 保持 `null`。

## 链接到的概念

- [[urp-volume-post-processing]]

## 原文

- 链接：https://danielilett.com/blur-shaders-pro/scripting-guide/
- 本地：`raw/articles/danielilett.com/2026-01-01_blur-shaders-pro-scripting-guide.md`
