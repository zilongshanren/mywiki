---
tags: [渲染, 后处理, unity, 体积雾, 光束, 阴影贴图]
date: 2026-04-14
sources: 1
---

# 在 Unity 里搭多步后处理管线（2015）

[[kostas-anagnostou|Kostas Anagnostou]] 2015 年重拾 Unity（当时刚开放免费版的低层图形接口），用它实现一个「体积光束 + 屏幕着色」的多步后处理 pipeline，作为 shader 原型工具的一次再评估。这篇文章既是一份 Unity 特定 API 的清单（`OnRenderImage`、`PostEffectsBase`、`Graphics.Blit`、`_CameraDepthTexture`、`_CameraGBufferTextureN`、`CommandBuffer`、`unity_World2Shadow[]`），也是一个值得记住的**最小可用体积雾 pipeline 骨架**。

## Unity 这一侧的基础设施

最轻量的自定义后处理类继承 `PostEffectsBase`，绑一个 `Shader` 字段和一个 `Material`；引擎在主场景渲染完后调用 `OnRenderImage(source, destination)`，开发者用 `Graphics.Blit(source, destination, material)` 触发全屏 pass。Shader 里 `_MainTex` 会被自动绑为输入纹理，加后缀 `_TexelSize` 能拿到 `float4(1/w, 1/h, w, h)`，非常方便。多个后处理脚本挂在同一个相机上会按顺序串起来，拼一条流水线非常省事。

Deferred shading 下，引擎把 [[gbuffer-layouts|g-buffer]] 暴露成 4 张全局纹理 `_CameraGBufferTexture0..3`（diffuse / specular+roughness / world normal / emission+lighting），深度则在 `_CameraDepthTexture`。但**访问阴影贴图**要更绕一点——需要给光源挂一个 `CommandBuffer`，在 `LightEvent.AfterShadowMap` 时用 `SetGlobalTexture("MyShadowMap", BuiltinRenderTextureType.CurrentActive)` 把当前活动 RT 暴露成全局名字，shader 端才能采样。

## 体积光束 pipeline 的五个步骤

技术上借鉴 Toth et al. 的屏幕空间光束 raymarching（见 [[volumetric-raymarching-intro]] 和 [[volumetric-fog-froxels]]），Anagnostou 把它压到一个四分之一分辨率 pipeline 里：

1. **降采样深度**到四分之一分辨率、R32F 格式。关键：**depth 降采样只能用 min 或 max，不能取平均**——平均会在几何边缘造出「虚假中间深度」。
2. **低分辨率 raymarching 算雾**。每一步做 shadow map 采样（cascade 分裂的 shadow coord 根据 `_LightSplitsNear/Far` 加权合并）、累加透射率 `transmittance *= exp(-extinction * stepSize)` 和 in-scattering `result += scattering * transmittance * stepSize * fColour`。用 2D 噪声纹理调制密度增加随机感；shadow term 在 `litFogColour` 和 `ShadowedFogColour` 之间插值，阴影区也能留下一点雾色，廉价近似多次散射。
3. **Interleaved sampling**。在 8×8 像素网格上把 ray start offset 错开 `(1/64) * stepSize`，相当于把 32 个样本摊到 64 个像素上，得到 2048 个「虚拟样本」的效果，显著抑制 aliasing。
4. **双向高斯模糊 + bilateral 深度权重**。7-tap Gaussian 可分为两个 1×7 / 7×1 pass 连做 4 次。朴素高斯会糊掉几何边缘——用低分辨率深度差做指数权重 `w = exp(-(Δz * falloff)^2)`，depth 跳变处权重迅速衰减到 0，效果边缘保持良好。
5. **Nearest-depth 上采样 + 合成**。采低分辨率 fog 纹理到全分辨率时，在 hi-res 像素邻域查 low-res depth：若四邻 depth 接近 hi-res depth 则走 bilinear，否则取深度最接近的那一个。最后 `colour * fogSample.a + fogSample.rgb`（`.a` 存的是透射率）。

## 为什么这条 pipeline 值得留一份记录

- 它是 [[volumetric-fog-froxels|frustum-aligned 3D 体积雾]] 前那一代的**screen-space 屏幕空间体积光束**的典型实现——一条纯 2D 的 raymarching pipeline，几乎不依赖 compute shader，DX11 class 的 GPU 就能跑。
- 它完整展示了「低分辨率 + interleaved + bilateral upsample」这一套**降成本三件套**的每一个坑位：为什么 depth 降采样要用 min；为什么要 interleaved 而不是直接加 sample；为什么 Gaussian 必须换成 bilateral；为什么上采样要 nearest-depth 而不是 bilinear。这三件套在 SSAO、SSR、volumetric fog、soft shadow 里反复出现。
- 它也是 Anagnostou 评估 Unity 是否可作为 shader 原型环境的结论：**有了低层访问后，Unity 完全可以**——省掉了自己写 DX11 初始化、资源绑定、shadow pipeline 的时间。

## 相关

- [[volumetric-raymarching-intro]] —— 体积 raymarching 的通用算法骨架
- [[volumetric-fog-froxels]] —— 下一代 compute-based 3D 体积雾
- [[bilateral-filter]] —— 边缘感知滤波的通用工具
- [[depth-aware-upsampling]] —— nearest-depth 上采样的专门讨论
- [[shadow-mapping-basics]] —— cascaded shadow map 的 cascade 切分
- [[unity-image-effect-basics]] —— Unity 图像特效脚本的基础
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-unity-postprocessing]]
