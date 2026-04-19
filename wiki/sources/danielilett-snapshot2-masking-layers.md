---
tags: [source, unity, urp, volume, mask, 后处理]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders 2 - Masking Layers（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Snapshot Shaders 2* 撰写的 **Masking Layers** 参数手册——pack 全局的效果 mask 机制，允许把任何后处理只作用于特定对象集合。

## 摘要

全屏后处理默认作用于整张 framebuffer，**想只 glitch 角色、不 glitch 场景**需要一个 mask 机制。Snapshot Shaders 2 给 pack 里每个效果都加了统一的 Masking 子面板，按四个维度筛选「哪些对象进 mask 纹理」：*Layer Mask*（Unity 标准对象 Layer）、*Rendering Layer Mask*（URP 的 Rendering Layer，8 位独立标记）、*Light Modes*（按 shader pass tag 过滤——`UniversalForward` 即 Lit、`SRPDefaultUnlit`、`UniversalGBuffer`、`Universal2D`、`ShadowCaster`、`DepthOnly`、`DepthNormals`、`Meta` 等）、*Render Queue*（Opaque / Transparent / All）。加上 *Draw Skybox To Mask* 和 *Invert Mask* 两个开关。Mask 模式分两种：**Local Mask** 每个效果自己生成自己的 mask 贴图，互不共享；**Global Mask** 需要往 Volume Profile 加一个 `Global Mask` volume component，把生成的 mask 共享给同 profile 下所有选择 Global 模式的效果——一次生成、多次复用。Global Mask 的 *Render Pass Event* 必须早于或等于任何使用它的效果，否则读取时还没写。限制：一个 profile 只能有一个 Global Mask。

## 关键要点

- **Light Modes 过滤是 URP 的 "shader pass tag"**——它不是 render layer 也不是 GameObject layer，而是 shader 的 SubShader/Pass 里 `Tags { "LightMode" = "..." }` 字段；这让"只遮罩自己写的 custom shader 的对象"成为可能
- `Meta` light mode 会在 build 时被 strip——运行期不可用于 masking，只在 lightmap baking 阶段存在
- `UniversalGBuffer` 只在 Deferred 路径有效；`UniversalForwardOnly` 则专为需要 Forward 渲染但主管线在 Deferred 的 shader 设计
- Local vs Global 是**一次生成一份 vs 一次生成多用**的性能权衡——多个效果共用同一过滤条件就切 Global
- Render Pass Event 排序约束是"mask 必须早于使用者"——这与 [[blit-render-feature|Blit Render Feature]] 的 event 序列问题同构
- *Invert Mask* 是产品化细节——没有它的话"只 glitch 场景不 glitch 角色"就得另建一层 Layer
- 与 Unity 引擎原生的 [[draw-renderer-list-mask-urp|DrawRendererList + Renderer Mask]] 是同类机制，Snapshot 2 做的是高层包装

## 链接到的概念

- [[volume-mask-layers]]
- [[urp-volume-post-processing]]
- [[draw-renderer-list-mask-urp]]
- [[custom-mask-shaders]]

## 原文

- 链接：https://danielilett.com/snapshot-shaders-2/masking-layers/
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-2-masking-layers.md`
