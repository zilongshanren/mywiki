---
tags: [unity, 渲染, srp]
date: 2026-04-05
sources: 1
---

# Scriptable Render Pipeline（SRP）

Unity 的 **Scriptable Render Pipeline** 允许用 C# 控制完整的渲染流程，而不是依赖内置管线。

## 在 Custom SRP 中的关键概念

从 [[custom-srp]] 6.1.0 教程中涉及的 SRP API：

- **`CameraRenderer`**：每个相机的渲染协调器，组合各个 Pass。
- **Pass 类型**：`SetupPass`、`PostFXPass`、`FinalPass`、`GizmosPass`、`DebugPass` 等，每个 Pass 都有静态 `Record(renderGraph, ...)` 方法。
- **`CameraRendererTextures`**：一个 struct，持有 `colorAttachment`、`depthAttachment`、`colorCopy`、`depthCopy`、`cameraTarget` 等 `TextureHandle`，统一管理一帧内使用的纹理。
- **`RenderTexture targetTexture`**：相机可选的目标纹理。如果设置了，就用它替代 `BuiltinRenderTextureType.CameraTarget`。

## Camera Target 的决策集中

6.1.0 解决的一个设计问题：原本每处需要相机目标的地方都用 `BuiltinRenderTextureType.CameraTarget`，当相机设置 `targetTexture` 时行为不对。修复方式是把 target 的选择集中到 `SetupPass.Record` 里：

```csharp
RenderTexture targetTexture = camera.targetTexture;
TextureHandle target = renderGraph.ImportBackbuffer(
    targetTexture ? targetTexture : BuiltinRenderTextureType.CameraTarget);
```

其他 Pass 都通过 `textures.cameraTarget` 使用。这是一次**消除 [[change-amplification]]** 的小规模重构——把「相机目标选择」这份知识集中到一处。

## 相关
- [[custom-srp]]
- [[render-graph]]
- [[color-lut]]
- [[urp-volume-post-processing]] —— URP 的 Volume 后处理系统（PPv3）
- [[blit-render-feature]] —— URP 自定义后处理的补救路径
- [[cyanilux]]
- [[urp-builtin-feature-mapping]] —— Built-in RP → URP 的 API 迁移速查（相机回调、LightMode 标签、材质属性、深度/不透明纹理）

## Sources

- [[sources/custom-srp-6-1-0]]
- [[sources/cyan-urp-post-processing]]
