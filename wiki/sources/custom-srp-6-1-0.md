---
tags: [source, unity, 渲染, 教程]
date: 2026-04-05
sources: 1
---

# Custom SRP 6.1.0（Jasper Flick / Catlike Coding）

Catlike Coding 的 Unity Custom SRP 教程 6.1.0 版本，作者 [[jasper-flick]]。基于 Unity 6000.3.11f1，承接 6.0.0。

## 摘要

本版本添加了颜色 LUT 的调试可视化：在 Rendering Debugger 里新增「Show Color LUT」开关，把每个相机的颜色 LUT 显示为屏幕底部的条带。同时修复了一个相机 targetTexture 相关的 bug——当相机设置了 targetTexture 时，不再错误地使用 backbuffer。

## 关键要点

- **Camera Target 集中化**：引入 `CameraRendererTextures.cameraTarget` 字段，统一在 `SetupPass.Record` 里决定相机目标（`targetTexture` 或 `BuiltinRenderTextureType.CameraTarget`），其他 Pass 通过 `textures.cameraTarget` 使用。
- **PostFXPass 返回 colorLUT**：让 `DebugPass` 能访问颜色 LUT 的 `TextureHandle`。
- **CameraDebugger.Render 新增 LUT 分支**：以 `_ColorLUTResolution` 和 `_ColorGradingLUT` 作为输入，用新的 shader pass 画一个矩形。
- **Shader 细节**：按 `vertexID` 生成 4 个顶点的矩形，用 `_ProjectionParams.x` 处理 Y 翻转，高度按 `2 * bufferHeight/bufferWidth / ColorLUTResolution` 计算。
- **IsActive 重新定义**：`(showTiles && opacity > 0f) || showColorLUT`——LUT 显示不受 opacity 影响。

## 链接到的概念

- [[custom-srp]]
- [[color-lut]]
- [[scriptable-render-pipeline]]
- [[render-graph]]
- [[debug-visualization]]
- [[jasper-flick]]
- [[rendering-api-depth]]

## 原文

- 链接到：[[raw/articles/Custom SRP 6.1.0]]
- 来源：https://catlikecoding.com/unity/custom-srp/6-1-0/
- 图片：![[raw/assets/tutorial-image.jpg]]
