---
tags: [unity, urp, srp, 渲染管线, 自定义pass]
date: 2026-04-19
sources: 1
---

# URP ScriptableRenderPass 自定义渲染 Pass

URP 在 [[scriptable-render-pipeline|SRP]] 的基础上把"一次渲染动作"抽象成三个类搭配：**`ScriptableRendererFeature`** 作为外壳、**`ScriptableRenderPass`** 作为执行体、再加一个**任意 Settings 类**暴露给 Inspector。把三者注册到 `UniversalRendererData` 资源，相机运行时就会按注册顺序调用。

[[blit-render-feature]] 是这个框架的一个特化（全屏 Blit）。Steven Sell 在做体积雾时给出了另一个更完整的用例：16 个自定义 pass 同时存在——体积云 / 体积雾、透明物体深度、地形高度贴图、描边——都走同一套 feature + pass 骨架。

## 两方法的分工

每个自定义 pass 主要实现两个虚方法：

- **`OnCameraSetup(CommandBuffer cmd, ref RenderingData data)`**：每帧每相机调用一次，是做"相机相关"准备的地方。典型工作：分配/resize offscreen RT、在相机 resize 时重建 buffer、给 shader 压入相机常量（比如世界空间的近裁面四角）。
- **`Execute(ScriptableRenderContext ctx, ref RenderingData data)`**：真正的绘制。从 `CommandBufferPool.Get()` 拿一个 cmd buffer，包在 `ProfilingScope` 里便于 GPU profiler 看，然后把 draw/blit 命令塞进去。

`renderPassEvent` 字段（继承自 `ScriptableRenderPass`）决定 pass 插在管线哪一步——`BeforeRenderingPostProcessing`、`AfterRenderingOpaques`、`AfterRenderingTransparents` 是最常用的几个。

## CommandBuffer 的异步陷阱：MaterialPropertyBlock

URP 自定义 pass 的 draw 命令都进 `CommandBuffer`，而 command buffer 是**异步 enqueue，延迟执行**的——你 C# 这一帧里对 Material 做的 `SetVector` 不保证在 GPU 真正 dispatch 时仍是那个值。多 volume 共享一个 material 时尤其明显：循环中每次 `material.SetVector(bounds)` 再 `cmd.DrawMesh`，最后 GPU 跑起来所有 DrawMesh 看到的 bounds 都是最后一次设的值。

**解法是 `MaterialPropertyBlock`**——把 per-draw 的属性塞到 property block 里，`cmd.DrawMesh(mesh, matrix, material, 0, shaderPass, propertyBlock)`。command buffer 在 enqueue 时会**拷贝**一份 block 的内容，GPU 执行时用的是当时的快照。Unity 官方的 `Blit()` helper 没有接受 property block 的重载，所以 volumetric fog 作者写了自己的 `RasterizeColorToTarget` 用 `cmd.DrawMesh(fullscreenQuad, Matrix4x4.identity, material, pass, propertyBlock)` 代替 Blit。

## 近裁面四角：screen-space raymarch 的精度钥匙

屏幕空间 raymarch 的惯常写法是从相机的 right/up/forward 插值得到 ray direction，结果是**圆形 frustum**——forward 是常量，right/up 随 UV 缩放，远离屏幕中心时方向会"翘起"。这在 demo 里不明显，在玩家自由控制的相机下就是一种扭曲。

干净的替代方案：CPU 端把近裁面四角的世界位置打包到一个 `float4x4`（4 列 xyz），传到 shader；vertex shader 用 UV 在四角之间 bilinear 插值拿到"这个像素在近裁面上的世界坐标"；fragment 里 `rayOrigin = wsNearPlane`、`rayDir = normalize(rayOrigin - cameraPos)`——这是真正的 pinhole frustum，ray direction 沿着 frustum 边缘而不是被 forward 主导，远离中心不扭曲。

这块数据通过 `OnCameraSetup` 注入：`FogMaterialProperties.SetMatrix(ShaderIds.CameraNearPlaneCorners, camera.GetNearClipPlaneCornersMatrix())`。放在 `OnCameraSetup` 而不是 `Execute` 里，是为了让"相机参数"的更新时机和渲染分开。

## 生命周期与资源

- Pass 的 ctor 是 **per-application** 的：实例化 material、创建 MPB、置空 RT（等有相机尺寸再分配）。
- `OnCameraSetup` 里用一个 `HasCameraResized()` 辅助检查 RT 尺寸，变了就重建。多相机且尺寸不同时，给每个相机维护一张独立 RT 比反复 resize 便宜。
- Fog 之类"多个 volume 累积到一张 buffer"的效果，`Execute` 里 foreach 每个 volume：先 apply volume 的 params 到 MPB、然后 `RasterizeColorToTarget` 画一次 full-screen quad；所有 volume 画完再 **Blit 一次**把累积 buffer 混合到主相机。

## 运行时开关与多 renderer data

同一个项目通常有几个 `UniversalRendererData` 对应不同质量档——分配不同 feature 子集。次级相机（minimap、反射探针）只需要部分 feature，在它们的 renderer data 里不注册即可，`AddRenderPasses` 里还能 `if (cameraData.camera != Camera.main) return` 做进一步过滤。

## 相关

- [[scriptable-render-pipeline]]
- [[blit-render-feature]]
- [[urp-render-objects-feature]]
- [[urp-volumetric-fog-raymarch]]
- [[volumetric-cloud-quarter-res-upsample]] — Sell 的另一篇 ramble 也基于这个框架
- [[steven-sell]]

## Sources

- [[sources/vertexfragment-urp-volumetric-fog]]
