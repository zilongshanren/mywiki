---
tags: [source, unity, urp, built-in-rp, 迁移]
date: 2026-04-19
sources: 1
---

# URP and Built-in RP feature mapping（cmwdexint）

[[ming-wai-chan]] 发表于 2021 年 1 月的一张**从 Built-in RP 迁到 URP 的 API 对照表**，基于 Unity 2020.2.2f1 + URP 10.2.2。

## 摘要

作者把 Unity 官方 *Universal RP Feature Comparison* 那张只讲"支不支持"的清单补上了"**Built-in 这样写、URP 换成怎么写**"的用法映射。涵盖相机生命周期回调（从 `OnPreRender` 等 MonoBehaviour 钩子换到 `RenderPipelineManager.beginCameraRendering` 事件）、命令缓冲注入点（从 `Camera.AddCommandBuffer` 换到 `ScriptableRenderPass` + `RendererFeature`）、shader 模板与 `LightMode` 标签（`ForwardBase` → `UniversalForward`、`Deferred` → `UniversalGBuffer`，并新增 `DepthOnly` / `DepthNormals` / `Universal2D`）、标准材质属性名（`_Color` → `_BaseColor`）、相机深度/不透明纹理（从 `DepthTextureMode` 位标志换到 pipeline asset 的 Depth Texture / Opaque Texture 勾选）等常见迁移点。

## 关键要点

- 相机生命周期改成 `RenderPipelineManager` 静态事件，`OnRenderImage` 不再自动触发，后处理得走 RendererFeature。
- Command buffer 注入点换成 `RenderPassEvent` 枚举，要挂到 `ForwardRendererData` asset 的 RendererFeature 列表上。
- LightMode 标签重命名：`ForwardBase/ForwardAdd` → `UniversalForward`，`Deferred` → `UniversalGBuffer`，新增 `DepthOnly/DepthNormals/Universal2D`。
- Lit shader 主属性从 `_Color` 改为 `_BaseColor`，老脚本 `SetColor` 会静默失败。
- 深度 / 不透明纹理不再靠 `Camera.depthTextureMode`，改在 URP Pipeline Asset 上勾选，对应 shader 采样变量是 `_CameraDepthTexture` / `_CameraOpaqueTexture`。

## 链接到的概念

- [[urp-builtin-feature-mapping]]
- [[scriptable-render-pipeline]]

## 原文

- 链接：https://cmwdexint.com/2021/01/15/urp-and-built-in-rp-feature-mapping/
- 本地：`raw/articles/cmwdexint.com/2021-01-15_urp-and-built-in-rp-feature-mapping.md`
