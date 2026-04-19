---
tags: [渲染, post-processing, urp, npr, 阴影, shader, unity]
date: 2026-04-19
sources: 1
---

# Mystery Dungeon 素描阴影（Unity URP 复刻）

《Pokémon Mystery Dungeon: Rescue Team DX》的视觉招牌是**阴影区域被渲染成铅笔素描纹理**——物体投影不是一块灰色，而是一片手绘风格的交叉排线，且排线会略微超出实际阴影范围（更接近手绘漫画的笔触，而不是几何精确的阴影边界）。[[daniel-ilett|Daniel Ilett]] 在 2024 年用 Unity URP + Renderer Feature + post-process 复刻了这个效果，把一堆看似无关的 Unity 特性串在了一起：screen-space shadow map、depth-aware blur、triplanar mapping、normals texture、volume post-process framework。

## 问题分解

视觉需求翻译成技术目标：

1. 素描只出现在**阴影里**——需要一个"这个像素在不在阴影里"的 mask。
2. 素描**略微超出阴影边界**（符合手绘感）——mask 需要被**外扩 / 模糊**。
3. 素描纹理**不随相机移动**（否则看起来像浮层 sticker）——不能用屏幕空间 UV，必须绑定世界坐标。
4. 物体表面朝向不同时素描角度看起来应该正确——需要按法线方向选择采样平面。

## 四个部件如何组合

**1. [[screen-space-shadow-map-urp|Screen Space Shadows Renderer Feature]]** 提供素材：它把 URP 的主光阴影贴图转成 `_ScreenSpaceShadowmapTexture`——一张屏幕分辨率的阴影 mask，免费拿到，单通道 R8。这解决了需求 1。

**2. [[depth-aware-gaussian-blur|Depth-aware Gaussian blur]]** 解决需求 2：在 Renderer Feature 的 `Execute` 里把 shadowmap 拷进自己管理的 `shadowmapHandle1` RTHandle，跑两 pass 横/竖模糊，kernel 高达 100+。关键是**深度感知**——如果只是普通 Gaussian，阴影会"溢出"到前景物体上（一个角色的阴影漏到角色身上画出素描，明显错误）。加了深度差阈值 `_DepthSensitivity` 后，模糊只在同一物体内部扩散、不跨过物体边缘。这同时开 `_BlurStepSize`（稀疏核）保持大半径下的性能。

**3. Triplanar Mapping** 解决需求 3、4：后处理 shader 没有 mesh UV 可用——这是 post-process 的根本限制。Ilett 用 `ComputeWorldSpacePosition(uv, depth, UNITY_MATRIX_I_VP)` 从深度重建世界坐标，再用 `_CameraNormalsTexture`（由 `ConfigureInput(ScriptableRenderPassInput.Normal)` 启用）拿到世界空间法线。世界坐标作为 `[[triplanar-mapping|triplanar 采样]]`的三套 UV（`xz`、`xy`、`yz`），按法线权重混合——等价于自动给每个像素选最合适的"贴图平面"。cross-hatching 模式就是再跑一遍 triplanar（数学上应该旋转 UV 90°，Ilett 承认代码里没真的旋转、是个留给读者的 TODO），两个采样合成十字排线。

**4. 最终合成** 在 sketch pass 里：`smoothstep(_SketchThresholds.x, _SketchThresholds.y, blurredShadow)` 把模糊后的阴影 mask 转成软 alpha，然后 `lerp(cameraColor, sketchColor * sketchTint, alpha * sketchAlpha)` 把素描 lerp 到原画面上。

## Renderer Feature 的骨架

URP 的 post-process 自定义 renderer feature 有四件套：

- **Settings**（extends `VolumeComponent`, `IPostProcessComponent`）—— 所有 volume 参数（`TextureParameter`, `ColorParameter`, `ClampedFloatParameter` 等），提供 `IsActive()` 门禁。
- **RenderPass**（extends `ScriptableRenderPass`）—— 持有材质和 RTHandle，在 `Configure` 里根据 cameraDescriptor 分配临时纹理，在 `Execute` 里做 blit 和 dispatch。
- **RendererFeature**（extends `ScriptableRendererFeature`）—— 在 `AddRenderPasses` 里检查 volume 激活状态，把 pass 入队。
- **Shader**（`.shader`）—— 多 pass HLSL，包含 `HLSLINCLUDE` 的共享 include + 分 pass 实现。

Ilett 选择在 `RenderPassEvent.BeforeRenderingPostProcessing` 注入——名字有点误导（自己也是 post processing），但"before"指的是 URP 内建的 Bloom / Tonemap 等 post-process，也就是"在内建 post 之前、geometry 之后"这个时机。

## 三张 RTHandle 的分工

- `tempTexHandle`：因为不能从 `cameraTargetHandle` blit 到自己，需要一个中转槽位。`cameraTargetHandle → tempTexHandle → cameraTargetHandle(+material)` 是标准的 "ping-pong" 套路。
- `shadowmapHandle1` 和 `shadowmapHandle2`：blur 的两张 ping-pong 纹理。横 blur 从 1→2，竖 blur 从 2→1，最后结果留在 1 里传给 sketch pass。它们用 `RenderTextureFormat.R8` 省带宽——阴影 mask 只需要一个灰度通道。

## URP Blit API 的混乱

Ilett 吐槽（合理）：URP 的 blit API **新旧并存且不互通**。老的 `cmd.Blit(src, dst)` 用 `RenderTexture`，新的 `Blitter.BlitCameraTexture(cmd, src, dst)` 用 `RTHandle`。但想把一张 `RenderTexture`（如 `_ScreenSpaceShadowmapTexture`）拷到一张 `RTHandle`，只有老 API 能做（会编译 warning 但能跑），新 API 没有直接桥梁。再加上 `RenderTexture.GetTemporary` vs `RenderingUtils.ReAllocateIfNeeded` 两套内存管理并行存在，这块是当前 URP post-process 最容易踩坑的地方。

## 为什么整条路径值得学

单独看每一部分都是 Unity 文档里能查到的 API，但**把它们拼成一个实际 NPR 效果**是大多数官方文档不会教的——具体哪个 RenderPassEvent 放在哪里、纹理格式怎么选省内存、哪些地方会撞上新旧 API 的 gap、triplanar 是解决 post-process 里"没有 UV"的标准出路。这条链条的每个节点都是任何非写实风格 post-process 会复用的。

## 和 cel shader 的关系

从视觉目标看，这和 [[cel-shading-pipeline|cel shading]] 都在做 NPR，但实现路线完全不同：cel shading 在 **forward pass 内部**自定义 lighting function，每个物体 shader 里处理阴影硬化、描边；这里的 sketch 是**纯 post-process**，任何已有 shader 都能接入、不需要修改 asset 的材质。trade-off 是 post-process 丢失了 mesh UV 和 per-object 灵活性、但换来了**全场景统一、零 asset 侵入**。两条路各有甜区。

## 相关

- [[daniel-ilett]]
- [[screen-space-shadow-map-urp]]
- [[depth-aware-gaussian-blur]]
- [[triplanar-mapping]]
- [[blit-render-feature]] — URP post-process renderer feature 的通用骨架
- [[urp-volume-post-processing]]
- [[cel-shading-pipeline]] — NPR 的另一条路径
- [[separable-gaussian-blur]]
- [[scene-color-depth-nodes]]
- [[coordinate-spaces]]

## Sources

- [[sources/danielilett-mystery-dungeon-sketches]]
