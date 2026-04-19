---
tags: [unity, urp, built-in-rp, 迁移, 速查]
date: 2026-04-19
sources: 1
---

# URP 与 Built-in RP 特性映射

Unity 从 Built-in RP 迁到 [[scriptable-render-pipeline]] / URP 时，很多日常 API 都换了接口。Unity 官方 *Feature Comparison* 表只给了"是/否支持"，但真正上手要的是**"Built-in 这么写，URP 怎么写"**的一一对照。Ming Wai Chan 的这份速查（基于 Unity 2020.2.2f1 + URP 10.2.2）把常用的几类替换记了下来。

## 相机生命周期回调

Built-in RP 用 **MonoBehaviour 钩子**：`OnPreCull` / `OnPreRender` / `OnPostRender` / `OnRenderImage`。

URP 用 `RenderPipelineManager` 的**静态事件**：

- `beginFrameRendering` / `endFrameRendering`
- `beginCameraRendering` / `endCameraRendering`

这就意味着后处理不能再靠 `OnRenderImage` 自动触发——得写 `ScriptableRendererFeature`（见 [[blit-render-feature]]）或订阅 `beginCameraRendering`。

## 命令缓冲注入点

Built-in 的 `Camera.AddCommandBuffer(CameraEvent, cmd)` / `Light.AddCommandBuffer(LightEvent, cmd)` 在 URP 完全不生效。URP 的对应物是 `ScriptableRenderPass.renderPassEvent = RenderPassEvent.XXX`，挂到一个 `RendererFeature` 里，再把这个 feature 加到 **ForwardRendererData** asset 上。注入点的命名也变了（`BeforeRenderingOpaques` / `AfterRenderingTransparents` / `BeforeRenderingPostProcessing` 等），不再是 Built-in 的 `CameraEvent.AfterForwardOpaque` 这套。

## Shader 模板与 LightMode 标签

**Project → Create → Shader** 菜单里：

- Built-in 给 *Standard Surface Shader* / *Unlit Shader* / *Image Effect Shader*；
- URP 多一套 *Universal Render Pipeline* 子菜单，**主推 Shader Graph**（不再有 surface shader）。

每个 Pass 的 `Tags { "LightMode" = "..." }` 标签名换了：

| Built-in | URP |
|---|---|
| `ForwardBase` / `ForwardAdd` | `UniversalForward` |
| `ShadowCaster` | `ShadowCaster`（保持） |
| `Deferred` | `UniversalGBuffer` |
| `Meta` | `Meta`（保持） |
| — | `DepthOnly` / `DepthNormals` / `Universal2D`（URP 新增） |

写自定义 shader 时漏掉 `UniversalForward` 意味着这物体在 URP 主 pass 里根本不画。URP 还要求 shader 提供单独的 `DepthOnly` / `DepthNormals` pass 才能正确写入 [[depth-texture-silhouette]] 那类相机深度/法线贴图。

## 标准材质属性名

Legacy Standard shader 用 `_Color` / `_MainTex`，URP 的 Lit shader 改名为 `_BaseColor` / `_BaseMap`。老脚本里 `material.SetColor("_Color", ...)` 迁到 URP 要挨个改，否则默默失败。

## 相机深度 / 法线 / 运动向量

Built-in 通过 `Camera.depthTextureMode` 全部开关，**按位叠**，内置暴露 `_CameraDepthTexture` / `_CameraDepthNormalsTexture` / `_CameraMotionVectorsTexture`。

URP 改成两个**管线 asset 级别 checkbox**：

- *Depth Texture* → 提供 `_CameraDepthTexture`（不再有合成的 DepthNormals 纹理，自己写 `DepthNormals` pass）；
- *Opaque Texture* → 提供 `_CameraOpaqueTexture`（Built-in 里需要自己 Blit 才能拿到"当前帧不透明已画完"的颜色缓冲）。

不开 *Opaque Texture* 的话像扭曲、玻璃这类 refraction shader 完全失效。

## Sources

- [[sources/cmwdexint-urp-builtin-feature-mapping]]
