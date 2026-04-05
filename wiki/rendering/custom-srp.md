---
tags: [unity, 渲染, srp]
date: 2026-04-05
sources: 1
---

# Custom SRP（Catlike Coding 教程系列）

Catlike Coding 的 **Custom SRP** 是一个 Unity [[scriptable-render-pipeline|Scriptable Render Pipeline]] 的教程系列，作者 [[jasper-flick|Jasper Flick]]。6.1.0 版本基于 Unity 6000.3.11f1，承接 6.0.0 版本。

## 6.1.0 版本主题

本版本专注于**颜色 LUT 的调试可视化**：

1. **修复 Camera Target Texture**：当相机设置了 `targetTexture` 时，使用它而不是默认的 backbuffer，让 Multiple Cameras 场景能正确渲染到纹理。
2. **Color LUT 调试显示**：在 Rendering Debugger 里新增「Show Color LUT」开关，把生成的 [[color-lut|颜色 LUT]] 显示在屏幕底部。

## 关键架构变化

- 在 `CameraRendererTextures` 里新增 `cameraTarget` 字段，把相机目标的选择集中到一处。
- `PostFXPass.Record` 现在返回 `TextureHandle colorLUT`，让 `DebugPass` 能拿到它。
- `DebugPass.Record` 接收 color LUT 的 resolution 和 texture handle。
- `CameraDebugger.Render` 新增对 color LUT 的绘制分支。

## 相关概念

- [[color-lut]]
- [[scriptable-render-pipeline]]
- [[render-graph]]
- [[debug-visualization]]
- [[rendering-api-depth]]

## 作者

- [[jasper-flick]]

## Sources

- [[sources/custom-srp-6-1-0]]
