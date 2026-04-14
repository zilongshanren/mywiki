---
tags: [unity, 渲染, render-graph]
date: 2026-04-05
sources: 1
---

# Render Graph

Unity 的 **Render Graph** 是 SRP 的声明式渲染编排系统。用户声明 Pass 及其资源依赖，Render Graph 负责调度与资源管理。

## 在 Custom SRP 中用到的 API

从 [[custom-srp]] 6.1.0 教程中出现的 Render Graph API：

- **`renderGraph.AddUnsafePass<T>`**：创建一个 UnsafePass，允许直接操作命令缓冲。
- **`IUnsafeRenderGraphBuilder`**：构建 Pass 的 builder 接口，允许声明依赖。
- **`builder.UseBuffer(...)`**、**`builder.UseTexture(...)`**：声明 Pass 使用某个资源。
- **`builder.AllowPassCulling(false)`**：阻止 Pass 被剔除。
- **`builder.SetRenderFunc<T>(...)`**：设置 Pass 的实际渲染函数。
- **`renderGraph.ImportBackbuffer(...)`**：导入外部纹理到 Render Graph。
- **`TextureHandle`**：Render Graph 管理的纹理句柄，可通过 `.IsValid()` 检查。
- **`default`**：用 `default` 值表示无效的 TextureHandle（如没有后处理时的 colorLUT）。

## 设计视角的观察

Render Graph 是典型的 [[deep-modules|深模块]] 思想：

- **接口**：声明 Pass、声明资源使用、设置执行函数。
- **实现**：资源生命周期跟踪、Pass 依赖排序、内存 aliasing、GPU 同步——调用者完全不可见。

Pass 作者只需说「我用这些纹理」「我要这样画」，不需要关心纹理的分配时机、释放时机、是否和别的 Pass 共享内存池。

## Custom SRP 6.1.0 的 DebugPass 例证

```csharp
using IUnsafeRenderGraphBuilder builder = renderGraph.AddUnsafePass(
    sampler.name, out DebugPass pass, sampler);
builder.UseBuffer(lightData.tilesBuffer);
if (colorLUT.IsValid())
{
    pass.colorLUTResolution = colorLUTResolution;
    builder.UseTexture(colorLUT);
}
else
{
    pass.colorLUTResolution = 0;
}
builder.AllowPassCulling(false);
builder.SetRenderFunc<DebugPass>(
    static (pass, context) => CameraDebugger.Render(
        context, pass.colorLUTResolution));
```

Pass 声明它使用的 buffer 和可选的 texture，然后提供一个静态 lambda 作为执行体。

## 相关

- [[custom-srp]]
- [[scriptable-render-pipeline]]
- [[rendering-api-depth]]
- [[deep-modules]]——Render Graph 作为深模块的例证
- [[d3d12-resource-binding]] —— 同样的「延迟决策到 Draw 前一刻」思路在 D3D12 封装层
- [[gpu-hazard-tracking]] —— render graph 要替人处理的核心问题
- [[sources/jasper-how-to-write-a-renderer]] —— Jasper 把 render pass 描述成 dataflow graph 的视角

## Sources

- [[sources/custom-srp-6-1-0]]
