---
tags: [unity, urp, 后处理, shadergraph, 渲染]
date: 2026-04-14
sources: 2
---

# Blit Render Feature（URP 自定义后处理的补救路径）

URP 早期（v7–v8）的 **Volume 后处理系统**（见 [[urp-volume-post-processing]]）不向用户开放扩展点——想做一个自己写的全屏效果，官方没有合法入口。Cyan 推广的解决办法是写一个 **`ScriptableRendererFeature`**，在 Forward Renderer 的 pass 链里插入一次自定义 **Blit**：把当前相机颜色拷贝到一张临时 RT，同时用一个带 shader 的 Material 处理一遍，再拷回来。这条路径本质上是"假装自己是一个后处理效果"，但工作在 SRP 的渲染图外围。

## 最小结构

一个 Blit feature 由两个类组成：

- **`ScriptableRendererFeature`**（外壳）：持有 `BlitSettings`（Material、pass index、`RenderPassEvent`、目标选择等），在 `Create()` 里实例化一个 `BlitPass`，在 `AddRenderPasses()` 里把它 `EnqueuePass` 进渲染器。
- **`ScriptableRenderPass`**（执行者）：在 `Execute()` 里拿一个 `CommandBuffer`，通过 `cmd.GetTemporaryRT` 分配临时 RT，然后两次 `Blit`——先把 `source` 处理到临时 RT、再拷回 `source`。这种"双 blit"是必须的，因为**同一张纹理不能同时作为读端和写端**。

关键细节：`opaqueDesc.depthBufferBits = 0`——临时 RT 不需要深度附件；`RenderPassEvent` 通常设为 `AfterRenderingOpaques` 或 `BeforeRenderingPostProcessing`，决定这次 Blit 出现在帧时间线的哪个节点。

## Shader 端的约定

自定义 shader（通常是 Unlit Shader Graph）必须包含一个引用名为 **`_MainTex`** 的 `Texture2D` property——这是 Blit feature 默认把 source RT 塞进 Material 时用的名字。Master 节点必须是 **Unlit** 模式：整个处理发生在屏幕空间，PBR 光照没有意义。

Shader Graph 会为一张图生成**多个 pass**（含 shadow caster 等），这对 Blit 是个陷阱：如果 `blitShaderPassIndex = -1` 让所有 pass 都跑一遍，shadow caster pass 的输出会在屏幕上砸出一个巨大的黑矩形。正确做法是把 pass index 显式设为 `0`，只跑主 pass。

## 实战场景

这条路径在 URP 社区里支撑起了很多"Volume 做不到"的效果：

- **[[crt-shader-effects|复古 CRT shader]]**：Spherize 弯曲 + scanlines + 静电噪声。
- **描边 / 轮廓线**：通常需要两次 Blit——第一次用 override material 重绘场景提取法线到 RT，第二次用 outline shader 结合深度和法线生成边缘。
- **像素化 / 低分辨率复古滤镜**：Blit 到低分 RT 再拉回。

## 运行时开关与性能代价

Renderer Feature 天生是设计期对象，但想在运行时启用/禁用，可以通过 `ScriptableRenderer.GetRendererFeature<T>()` 拿到引用然后 `.SetActive(false)`。一个 Blit 大致要多烧一张屏幕尺寸的 RT 分配 + 两次全屏拷贝 + 一次 shader 采样，对于移动端并不便宜——在 TBDR 架构上这种"全屏写回主内存再读回"的 pattern 会打断 [[hsr-tbdr|tile-based 延迟渲染]] 的优化。

## 历史演进

Unity 2022 开始 URP 内建了 **Fullscreen Graph** 和 **Fullscreen Pass Renderer Feature**，填上了这个扩展点。Cyan 在 2020 年原版文章里的代码是面向 Unity 2019/2020 写的，新版本应该以官方组件或者他维护的 [`URP_BlitRenderFeature`](https://github.com/Cyanilux/URP_BlitRenderFeature) 仓库为准。

## 相关

- [[urp-volume-post-processing]]
- [[scriptable-render-pipeline]]
- [[render-graph]]
- [[crt-shader-effects]]
- [[scene-color-depth-nodes]]

## Sources

- [[sources/cyan-urp-post-processing]]
- [[sources/cyan-retro-crt-shader]]
