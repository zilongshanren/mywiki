---
tags: [source, unity, urp, post-processing, npr, 阴影, shader]
date: 2026-04-19
sources: 1
---

# Mystery Dungeon Sketches in Unity URP（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 9 月的教程：在 Unity URP 里复刻 **Pokémon Mystery Dungeon: Rescue Team DX** 的阴影渲染——阴影区域被替换为铅笔素描纹理、且素描会略微**超出**实际阴影范围。效果看着简单，实际串起了 URP 后处理里最复杂的一条链条：Screen Space Shadows、depth-aware blur、triplanar mapping、normals texture、`ScriptableRendererFeature`。

## 摘要

开头用 Frame Debugger 分析游戏——阴影区域被一张 sketch 贴图 mask 替换，town 场景里允许 sketch 轻微溢出阴影边界。作者决定全在 post-process 里做（而不是在每个物体 shader 里），这样不侵入 asset。

核心管线：

1. 打开 URP 的 **Screen Space Shadows** Renderer Feature，把主光阴影转成屏幕空间的 `_ScreenSpaceShadowmapTexture`。
2. 自己写一个 `ScriptableRendererFeature`（Sketch.cs + SketchSettings.cs）把上述 shadowmap blit 到自己的 RTHandle。
3. 跑两 pass **depth-aware Gaussian blur**——常规可分离 Gaussian + 额外逻辑：如果样本像素和中心像素的深度差超过阈值就跳过，防止阴影"溢出"物体边界。再加 `_BlurStepSize` 稀疏采样步长，让大 kernel（最高 500）仍能跑动。
4. sketch pass 从 `_CameraDepthTexture` + `UNITY_MATRIX_I_VP` 反推每像素世界坐标，用 `_CameraNormalsTexture` 拿世界法线，做 **triplanar sampling** 采 sketch 贴图（三个 `xz / xy / yz` 投影，按法线加权）。
5. `smoothstep(thresholds.x, thresholds.y, blurredShadow)` 得到软 mask，`lerp(cameraColor, sketchColor, mask * sketchAlpha)` 合成。

文章中段大量篇幅讨论 URP 的 **Renderer Feature 四件套**（Settings / Pass / Feature / Shader）、Volume system 参数类型（`TextureParameter / ClampedFloatParameter / BoolParameter` 等）、`RenderPassEvent.BeforeRenderingPostProcessing` 的时机选择、`ReAllocateIfNeeded` 的 RTHandle 管理、以及 `cmd.Blit` 和 `Blitter.BlitCameraTexture` 两套 API 并存的混乱（从 `RenderTexture` blit 到 `RTHandle` 只有老 API 能跑，编译有 warning）。

结尾作者承认这个实现"过度设计"——有更简单的做法——但这个走法把很多 URP 特性串在了一起，作为教学样本价值更高。

## 关键要点

- **Screen Space Shadows Renderer Feature** 是 URP 里"我要在 post-process 里用阴影"的标准入口，免费把光源空间 shadowmap 转成屏幕 UV 可直接采样的 `_ScreenSpaceShadowmapTexture`。
- **Depth-aware blur** 的思想：除了采目标纹理，同时采深度纹理；深度差超过阈值的样本丢弃，**同时从分母里扣掉它的权重**——保证边界像素正确归一化、不会骤暗。
- **稀疏核 `_BlurStepSize`** 让大半径 Gaussian 跑得动：`for (x = lower; x <= upper; x += stepSize)`，`stepSize = 2/4` 对大核的视觉影响很轻。
- **Post-process 里没有 mesh UV**——替代方案是从深度反推世界坐标 + 从 normals texture 拿世界法线 + **triplanar sampling**。这是所有"要在后处理里模拟对象空间采样"的标准套路。
- `ConfigureInput(ScriptableRenderPassInput.Normal)` 让 URP 帮你生成 `_CameraNormalsTexture`——相当于免费拿到 G-buffer 风格的法线通道，哪怕 forward rendering 下也能用。
- **URP 的 Blit API 新旧并存、不互通**：老 `cmd.Blit`（RenderTexture）+ 新 `Blitter.BlitCameraTexture`（RTHandle）。想从 `_ScreenSpaceShadowmapTexture`（RT）拷到 RTHandle，目前只有老 API，有 warning 但工作。
- 作者对 Unity 6 兼容性留了坑，当前实现在 Unity 2022 URP 上测试——这也暴露 Unity 每个大版本升级都会动 post-process API。
- `smoothstep(a, b, x)` 在这条管线里用了至少三次——**边缘柔化的瑞士军刀**。
- 这个例子也展示了 `_DepthSensitivity` 这种"每场景调"的参数最好暴露给 volume，让美术调而不是程序员重编译。

## 链接到的概念

- [[mystery-dungeon-sketch-shadows]]
- [[screen-space-shadow-map-urp]]
- [[depth-aware-gaussian-blur]]
- [[triplanar-mapping]]
- [[blit-render-feature]]
- [[urp-volume-post-processing]]
- [[cel-shading-pipeline]]
- [[separable-gaussian-blur]]
- [[shadow-mapping-basics]]

## 原文

- 链接：<https://danielilett.com/2024-09-27-tut7-15-mystery-dungeon-sketch-urp/>
- 本地：`raw/articles/danielilett.com/2024-09-27_mystery-dungeon-sketches-in-unity-urp.md`
