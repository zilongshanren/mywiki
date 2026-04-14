---
tags: [游戏开发, 渲染, 深模块, aposd]
date: 2026-04-05
sources: 2
---

# 渲染 API 的深度

渲染系统是讨论 [[deep-modules|深模块]] 的绝佳案例，因为 GPU 编程细节的复杂度非常高。

## 浅的渲染接口

```csharp
// 暴露了 GPU 编程的所有细节
void SetVertexBuffer(VertexBuffer vb);
void SetIndexBuffer(IndexBuffer ib);
void SetShader(Shader shader);
void SetTexture(int slot, Texture tex);
void SetConstantBuffer(int slot, ConstantBuffer cb);
void DrawIndexed(int indexCount, int startIndex, int startVertex);
```

每个调用者都需要懂 D3D/Metal 的资源绑定模型——顶点缓冲、索引缓冲、常量缓冲、绑定槽位。**认知负荷**很高。

## 深的渲染接口

```csharp
// 隐藏了所有状态管理
void DrawMesh(Mesh mesh, Material material, Matrix4x4 transform);
```

调用者只需要说「在这个位置用这个材质画这个网格」。底层有大量渲染状态管理的复杂性，但暴露给游戏逻辑层的接口是高层次的。

Unity 的 `Graphics.DrawMesh` 和 Unreal 的 `DrawRenderState` 都朝这个方向设计。

## CommandBuffer 的深度示例

```csharp
public class CommandBuffer
{
    public void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material);
    public void SetRenderTarget(RenderTexture rt);
    public void Execute();

    // 实现：内部状态管理、命令排序、GPU 同步、内存管理，约500行
}
```

深度 ≈ 500/10 = 50。非常深，好设计。

## SRP 的情境

Catlike Coding 的 [[custom-srp]] 教程展示的是一种中间层设计：把底层的 SRP API（`renderGraph`、`TextureHandle`、`RenderGraphBuilder`）组合成中层的 Pass（`PostFXPass`、`DebugPass`、`CameraRenderer`）。这些 Pass 对使用管线的人来说是实现细节，对写管线的人来说是深度抽象——同一个系统在不同观察层次上的深度不同。

## 相关

- [[deep-modules]]
- [[interface-vs-implementation]]
- [[custom-srp]]
- [[rendering-pipeline]]
- [[draw-call]]
- [[buffer-renaming]] —— 老 API 的"深"与现代 API 的"浅"取舍
- [[gpu-hazard-tracking]] —— 同一问题的深浅两种 API 设计
- [[jasper-st-pierre]]

## Sources

- [[sources/aposd-day04]]
- [[sources/rtr-day02]]
- [[sources/jasper-how-to-write-a-renderer]]
