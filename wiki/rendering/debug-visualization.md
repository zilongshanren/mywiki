---
tags: [unity, 渲染, 调试]
date: 2026-04-05
sources: 1
---

# 渲染调试可视化

Unity 的 **Rendering Debugger** 提供运行时可切换的调试视图。Custom SRP 通过 `CameraDebugger` 类集成到这个系统。

## Custom SRP 6.1.0 中的做法

在 `CameraDebugger` 中通过 `DebugUI.BoolField` 添加 toggle：

```csharp
new DebugUI.BoolField
{
    displayName = "Show Color LUT",
    tooltip = "Whether the color lookup texture is shown.",
    getter = static () => showColorLUT,
    setter = static value => showColorLUT = value
}
```

触发的渲染通过 `DrawProcedural` 画一个覆盖下方的矩形（6 个顶点的两个三角形），用一个专用的 shader pass（`Blend One Zero`，不混合）采样 `_ColorGradingLUT`。

## 关键 Shader 技巧

**顶点位置在 clip space**：左右 −1 到 1，上下根据 `_ProjectionParams.x` 确定：

```hlsl
float bottom, top;
if (_ProjectionParams.x < 0.0)
{
    bottom = 1.0;
    top = 1.0 - height;
}
else
{
    bottom = -1.0;
    top = height - 1.0;
}
```

**高度计算**：

```hlsl
float height = 2.0 * _CameraBufferSize.y * _CameraBufferSize.z;
height /= _ColorLUTResolution;
```

前半段把高度调整到等于宽度的宽高比（乘 2 因为 clip space 宽度是 2 单位），然后除以 LUT 分辨率得到条带的最终高度。

**按 VertexID 生成顶点**：

```hlsl
if (vertexID == 0) { ... }             // 左下
else if (vertexID == 1 || vertexID == 4) { ... }  // 左上（两个三角形共用）
else if (vertexID == 2 || vertexID == 3) { ... }  // 右下
else { ... }                            // 右上
```

## 设计视角

调试可视化本身是一个小规模的深模块：调用者只需 `showColorLUT = true`，底层处理状态检查、参数绑定、draw 调用、shader pass 选择——实现细节被隐藏。

## 相关

- [[color-lut]]
- [[custom-srp]]
- [[scriptable-render-pipeline]]

## Sources

- [[sources/custom-srp-6-1-0]]
