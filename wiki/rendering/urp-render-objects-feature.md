---
tags: [shader, urp, render-feature, pipeline, unity, x-ray, 分层渲染]
date: 2026-04-19
sources: 1
---

# URP 的 Render Objects Renderer Feature

URP 的 **Renderer Feature** 系统让用户向 Universal Renderer 的固定渲染循环里注入自定义 Pass，不需要改 pipeline 源码、不需要写 C# 脚本。**Render Objects** 是其中最通用的一个——把"选一批物体、在某个时机、用某个 override material / 深度测试 / stencil 重画一次"打包成一个面板可配置的 feature。它的核心价值是**无代码**就能做 X-ray 透视、物体 mask（给描边用）、按层排序修正等常见需求。

## 如何加一个 Render Objects

1. 在 Project 里找到 *Universal Renderer Data*（URP 3D 模板默认在 `Assets/Settings/PC_Renderer`，没找到就在 Project 搜索里按 Type 过滤 `Universal Renderer Data`）。
2. Inspector 底部 `Add Renderer Feature → Render Objects`。
3. 配置面板上的几个关键字段。

## 面板字段

**Event** —— 在 URP 渲染循环的 14 个时机之一插入：

```
BeforeRenderingPrePasses      (DepthOnly 等之前)
AfterRenderingPrePasses
BeforeRenderingGBuffer        (Deferred 的 G-Buffer 填充之前)
AfterRenderingGBuffer
BeforeRenderingDeferredLights
AfterRenderingDeferredLights
BeforeRenderingOpaques
AfterRenderingOpaques
BeforeRenderingSkybox
AfterRenderingSkybox
BeforeRenderingTransparents
AfterRenderingTransparents
BeforeRenderingPostProcessing
AfterRenderingPostProcessing
AfterRendering
```

X-ray 通常用 `AfterRenderingOpaques`——所有 opaque 画完（深度填满）后再画一次被 override 的目标物体。

**Filters**：

- **Queue**：Opaque / Transparent —— 只抓这个队列的物体。
- **Layer Mask**：只对指定 Unity layer 生效——x-ray 前要为目标物体建专用 layer（如 `Xray`）。
- **Light Modes** / **Render Passing Name**：只画 shader 里带这些 tag 的 Pass（高级用途）。

**Overrides**（覆盖原材质的渲染状态）：

- **Material**：用另一个 material 画——x-ray 换成红色 unlit；描边 mask 换成纯白 unlit。
- **Depth**：`Write Depth` + `Depth Test`（Less/LEqual/Greater/…）——x-ray 关键点是 `Depth Test = Greater`，只在被遮挡（当前 z > buffer z）时画。
- **Stencil**：完整的 stencil 状态覆盖，可做复杂 masking。
- **Camera**：FOV / offset 覆盖。

## X-ray 的典型配置

```
Event:     AfterRenderingOpaques
Queue:     Opaque
LayerMask: Xray
Overrides:
  Material:    M_XrayRed (unlit 红色)
  Depth Test:  Greater
  Write Depth: 不勾（无所谓）
```

部分可见 + 部分被墙挡 → 可见部分由主 Pass 正常渲染；被挡部分由这个 Render Objects pass 以红色画出（因为深度 > buffer）。整个效果零 C#。

## 与其它 Renderer Feature 的配合

- **Render Objects** 本质是"重新跑一遍标准渲染但换参数"；适合 90% 的"多渲染一遍"需求。
- **[[blit-render-feature|Blit Renderer Feature]]** 处理**全屏 post-process**——不筛选物体，而是把 camera color 复制到一张 RT、跑一次 fullscreen shader、写回。
- 自写 `ScriptableRendererFeature` 可以做任意事（compute dispatch、自定义 buffer 绑定等），但门槛高。

## Toon Outline 里的 mask 渲染就是它

[[sources/danielilett-toon-shaders-pro-outline-post|Toon Outline Post Process]] 的 *Masked Object Outlines* 算法——把某 layer 的物体以简化 material 画进一张 mask RT，后续 post-process 在 mask 上做 edge detection——底层就是一个 Render Objects feature 的变体（只是 asset 里封装了自己的 Blit + mask 资源管理）。

## 相关

- [[urp-depth-prepass-passes]] —— Event 列表里提到的 `PrePasses`
- [[blit-render-feature]] —— 全屏路径的对应物
- [[stencil-buffer]] —— Stencil override 的支撑
- [[early-z-late-z]] —— Depth Test `Greater` 依赖的前提

## Sources

- [[sources/danielilett-shader-code-depth-buffer]]
