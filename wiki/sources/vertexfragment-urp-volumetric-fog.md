---
tags: [source, rendering, volumetric-fog, raymarching, urp, unity]
date: 2026-04-19
sources: 1
---

# Rendering Volumetric Fog Using Custom URP Render Pass（Steven Sell / Vertex Fragment）

[[steven-sell]] 2024 年 4 月放出的"手把手实现体积雾"长文。一边讲 URP 里怎么写一个自定义 `ScriptableRenderPass`（Feature + Pass + Settings 三件套），一边讲 fragment shader 怎么对球形 volume 做双 raycast + raymarch + 多层噪声 + 阴影累积。配套开源仓库 `UnityURPVolumetricFog`。

## 摘要

Feature 层实现 `ScriptableRendererFeature`、在 `Create()` 里 new 出 Pass，把 Pass enqueue 到主相机。Pass 层的 `OnCameraSetup` 做 resize/clear、把相机 near-plane 四个世界空间角点打包成 4×4 矩阵传进 shader——这是为了让 raymarch 用的 ray origin/direction 不受常见"forward 恒定向量"方案的边缘扭曲影响。`Execute` 再 foreach 每个注册的 `FogVolume`，`RasterizeColorToTarget` 用自定义的 `DrawMesh` 调用（因为 `Blit` 不接受 `MaterialPropertyBlock`）把它画到 **quarter-size offscreen buffer**，最后 `BlitBlendOntoCamera` 合成回主相机。

Fragment shader 四段：(1) **Setup + Raycast**——ray-sphere 双 cast（正向找入射、反向找出射），配合 scene depth 决定遮挡早退；相机在球内单独处理。(2) **Raymarch 准备**——50 步、线性 step；用 `Hash13` 给起始位置加随机偏移打散 banding；从 main light 取方向、算 `dotRaySun` 调色。(3) **Loop**——每步做 edge/height/proximity 三种 fade、用一张 4 通道 3D `CloudVolume64` 采样两次（低频 billow + 高频细雾）、首次遇到浓雾时把步长砍到 0.2× 并回退（adaptive step，且不再切回大步）、采 directional shadow 累加。(4) **Finalization**——关键一步是用 `accumulation / distanceMarched` 做"stylized accumulation"：不是物理正确的粒子密度，而是把分布 normalize 到 `[0, 1]`，让相机从高处俯视低洼时也有均匀雾，避免物理 accumulator 在那种场景下"踩空"的问题。

文末提到两个没实现但设计好了的扩展：任意形状 volume（改用 mesh front/back depth 代替 ray-sphere）、fog 中光源 bloom（单独 `LightSourceTexturePass` + bloom 式混合）。

## 关键要点

- URP 自定义 Pass 三件套：`ScriptableRendererFeature` + `ScriptableRenderPass` + 自定义 Settings 类。
- Near-plane corners 矩阵是 raymarch ray direction 的最稳方案，避免"常量 forward + 可变 right/up"的边缘扭曲。
- Quarter-size offscreen buffer 思路和 [[volumetric-cloud-quarter-res-upsample|云的 1/16 upsample]] 同源；但这里没做 temporal jitter，直接 bilinear upsample 够用（fog 容忍度高）。
- Adaptive step：浓度突破阈值时缩小步长并回退，代价是部分 step 被重算，收益是近端采样不被等权稀释。
- Stylized accumulator vs 物理 accumulator 的 tradeoff 讲得很实用：物理正确但视觉塌陷 → 强行 normalize 到 `[0, 1]`。

## 链接到的概念

- [[urp-volumetric-fog-raymarch]]
- [[urp-scriptable-render-pass]]
- [[volumetric-cloud-quarter-res-upsample]]
- [[volumetric-fog-raymarch-shadows]]
- [[volumetric-fog-froxels]]
- [[raymarching-intro]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/urp-volumetric-fog/
- 本地：`raw/articles/vertexfragment.com/2024-04-17_rendering-volumetric-fog-using-custom-urp-render-pass.md`
