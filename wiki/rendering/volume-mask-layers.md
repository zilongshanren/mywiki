---
tags: [unity, urp, volume, 后处理, mask, renderer-feature]
date: 2026-04-19
sources: 1
---

# URP Volume 后处理的 Layer Mask 机制

全屏后处理默认对整张 framebuffer 生效——Bloom 作用于所有像素、Glitch 作用于所有像素。想实现"只让角色 glitch、背景保持清晰"就需要**按对象过滤**的 mask 纹理。Daniel Ilett 在 *Snapshot Shaders 2* 里把这个机制做成了 pack 全局组件，[[urp-volume-post-processing|URP Volume]] 的每个 effect 都能挂载同一份 mask 配置。

## 四维过滤条件

Mask 的核心是生成一张「哪些像素算在内」的单通道 render texture——可见的对象被写成白、其他写成黑，后处理 shader 采样这张 mask 决定每像素是否走 effect。过滤「哪些对象进 mask」由四个独立维度共同决定：

1. **Layer Mask**：Unity 标准的 GameObject Layer（32 个 bit，每个对象只能归属一个 Layer）——最常用的粗粒度筛选。
2. **Rendering Layer Mask**：URP 2022+ 引入的独立于 Layer 的 32-bit 渲染标记，挂在 Renderer 组件上。允许更细的分组（"这个对象既属于 Player 层也参与描边渲染层"）。
3. **Light Modes**：按 shader **pass tag** 过滤。Unity shader 在 `Tags { "LightMode" = "..." }` 里声明自己适用于哪种渲染 pass——`UniversalForward`（Lit 路径）、`UniversalForwardOnly`（强制 Forward 的 custom shader）、`SRPDefaultUnlit`（默认 Unlit）、`UniversalGBuffer`（Deferred）、`Universal2D`（2D Renderer）、`ShadowCaster` / `DepthOnly` / `DepthNormals` / `DepthNormalsOnly`（专用 pass）、`Meta`（lightmap baking 专用，**build 时被 strip**）。按 LightMode 过滤使得"只对我写的 custom Forward shader 渲染的对象 mask"成为可能——这是 Layer 或 Rendering Layer 做不到的粒度。
4. **Render Queue**：Opaque / Transparent / All——决定走 opaque 还是透明物体队列。

再加上两个独立开关：**Draw Skybox To Mask**（skybox 是否算在 mask 内）和 **Invert Mask**（在 mask **外部**跑 effect——例如"模糊背景不模糊角色"）。

## Local vs Global：性能拓扑

Snapshot Shaders 2 暴露两种 mask 作用域：

- **Local Mask**：每个 effect 独立生成一张自己的 mask——配置简单、互不耦合，但多 effect 用同一过滤条件时会**重复生成同内容的 mask 纹理**，浪费带宽。
- **Global Mask**：在 volume profile 里加一个 `Global Mask` volume component，它在某个 Render Pass Event 生成**单张共享 mask**，之后所有选择 Global 模式的 effect 读这张纹理。一个 profile 只能有一个 Global Mask。

Global Mask 的 *Render Pass Event* 必须早于或等于任何使用它的 effect——这和 [[blit-render-feature|Blit Render Feature]] 的渲染顺序约束同构。

## 实现层的推测

原文没写实现细节，但从暴露的参数反推：

- Mask 是通过 [[draw-renderer-list-mask-urp|DrawRendererList]] API 在一个独立 pass 里把过滤条件命中的对象绘制到 single-channel RenderTexture
- DrawRendererList 原生支持 Layer Mask、Rendering Layer Mask、Light Mode 多 tag、Render Queue 范围——这些参数一一对应
- "Draw Skybox To Mask" 需要一次单独的 skybox 绘制（skybox 不走常规 renderer）
- "Invert Mask" 可以在读 mask 时做 `1 - mask`、也可以在生成时把 clear color 和绘制颜色互换，二者等价

## 典型用途

- **局部 glitch**：boss 进场时让 boss 自己 glitch，背景保持稳定（mask = boss 所在 layer）
- **背景模糊**：主角对话时虚化背景，主角保持锐利（Invert Mask + 主角 layer）
- **水下效果限定**：只对水下物体应用 caustics，水面以上不加（mask = 水下 layer）
- **描边限定**：只描游戏对象不描 UI（mask = 非 UI layer）
- **隐身单位穿透**：[[mgs-stealth-camo-shader|隐身迷彩]] 的 stencil 式 mask 的 Volume 版——`UniversalForwardOnly` 自定义 shader + 专属 rendering layer

## 相关

- [[urp-volume-post-processing]] —— 这个 mask 机制所依附的系统
- [[draw-renderer-list-mask-urp]] —— 实现层的底层 API
- [[custom-mask-shaders]] —— 同类 mask 思路的另一角度
- [[image-effect-mask-blend]]
- [[blit-render-feature]]

## Sources

- [[sources/danielilett-snapshot2-masking-layers]]
