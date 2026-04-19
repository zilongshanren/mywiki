---
tags: [unity, urp, srp, 性能, 批处理, cbuffer]
date: 2026-04-19
sources: 1
---

# SRP Batcher 与 `UnityPerMaterial` CBUFFER

Unity 的 **SRP Batcher** 是 URP / HDRP 相对内建 RP 的一个"免费"性能加成——合法使用时它把大批**共享 shader 的物体**合并到少数几个 draw call 里，显著降低 CPU→GPU 数据传输成本。代价只有一条：**shader 要走特定声明格式**。Ilett 在 Shader Code Basics 02 把这个格式讲到够用的深度。

## 门票：把 property 封进 CBUFFER

SRP Batcher 要求 shader 里所有 material-level property（就是 ShaderLab `Properties` 块里声明的、每个 material 可以有不同值的那些）**必须放在一个名叫 `UnityPerMaterial` 的 constant buffer 里**：

```hlsl
CBUFFER_START(UnityPerMaterial)
    float4 _BaseColor;
    float4 _BaseTexture_ST;
    float2 _ScrollSpeed;
CBUFFER_END
```

`CBUFFER_START` / `CBUFFER_END` 是 Unity 提供的跨 API 宏，在 DX11 / DX12 下展开为 `cbuffer UnityPerMaterial { ... };`，在 Vulkan / Metal 上映射到各自的 constant buffer 概念。

**纹理资源（`TEXTURE2D` / `SAMPLER`）不进 CBUFFER**——它们在 shader 里走 descriptor binding 的路径，不是 uniform data，放进去反而会编译错。

## 为什么 SRP Batcher 会快

内建 RP 一次绘制物体时需要：
1. CPU 把 material property 打包成一个 shader constant buffer；
2. 上传到 GPU；
3. 发 draw call。

**每切一次 material 就重复一遍 1-3**。material 一多，CPU 就卡在打包和提交上。

SRP Batcher 的 trick 是：**共享同一个 shader variant 的物体，可以共享同一个 CBUFFER layout**——GPU 一侧的 constant buffer 只需要在第一次 bind shader 时上传一次，后续同 shader 的物体只需要修改 CBUFFER 里少量 material-specific 的常量（或者换一个 per-material CBUFFER handle），不必每次重新打包整个 CBUFFER。于是 draw call 之间 CPU 侧的工作量大幅减少。

"免费"的前提是 shader 满足 CBUFFER 约束——否则 Unity 自动 fallback 到传统的 non-batched 路径，而你可能直到 profiling 之前都不知道。

## 如何验证

两个手段：

1. **Inspector**：点 shader 资源，在底部面板里 Unity 会显示一行 "**SRP Batcher: compatible**" 或 "**not compatible: <reason>**"，并指出阻拦的 property 名字。Ilett 截图里 `HelloWorld` shader 不兼容（没加 CBUFFER），`BasicTexturing` 加了之后就 compatible。
2. **Frame Debugger**（*Window → Analysis → Frame Debugger*）：展开 `DrawOpaqueObjects`，SRP Batcher 合法的物体会聚在一次 **`DrawSRPBatcher`** 下面（一次绘制所有），不合法的则分散在多个独立 `Draw` 里。这也是最直观的方法看一个 scene 里的 batching 效率。

## 不兼容的常见原因

- Property 未包在 CBUFFER 里（最常见，新手忘记了）；
- CBUFFER 里放了非常量 data（比如 `StructuredBuffer`）；
- shader 用了 `MaterialPropertyBlock` 传数据——SRP Batcher 不和 MPB 合作（想用 MPB 传不同值得接受 batcher 失效的代价，或改用 GPU Instancing）。

## 和 GPU Instancing 的关系

SRP Batcher 不是 GPU Instancing。前者的加速靠**共享 shader 的 CBUFFER 复用**，每个物体仍是一次 draw call；后者靠**一次 draw call 画多个 mesh 实例**（共享 mesh + material）。两者解决不同场景，有时甚至需要都开。现代 URP 对两者都有自动支持，配置路径不同。

## 相关

- [[hlsl-texture-sampling-basics]] —— 同一份教程里的纹理采样入门
- [[shaderlab-hlsl-basics]]
- [[custom-srp]]
- [[batching]]
- [[draw-call]]

## Sources

- [[sources/danielilett-shader-code-textures-uvs]]
