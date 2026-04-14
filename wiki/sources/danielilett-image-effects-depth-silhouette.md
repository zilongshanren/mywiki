---
tags: [source, rendering, shader, unity, depth-buffer, post-processing]
date: 2026-04-14
sources: 1
---

# Image Effects Part 2 — Getting Deep（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 2 篇，把 image effect 从"只看 framebuffer"推进到"同时使用深度缓冲"，实现 *Super Mario Odyssey* 的 Silhouette 剪影效果。

## 摘要

文章用"剪影"这个视觉例子引出 [[z-buffer|深度缓冲]] 的存在与用途：GPU 在光栅化时把每像素的深度值写入一张与 framebuffer 等尺寸的 2D 数组，用它做隐面消除；image effect 只要把这张 `_CameraDepthTexture` 当普通纹理采样，就能免费拿到场景深度信息。实现步骤为：`UNITY_SAMPLE_DEPTH(tex2D(_CameraDepthTexture, uv))` 拿到原始深度——此时是 1/z 的非线性值——再用 `Linear01Depth()` 映射到 `[0, 1]`，近平面是 0、远平面是 1；接着在 fragment shader 里 `lerp(_NearColour, _FarColour, depth)` 就得到按距离着色的剪影。作者顺便解释了相机视锥（frustum）、`near/far clip plane` 的作用、以及为什么深度值是 1/z 非线性分布——为远处精度让位给近处提供了 ~50% 的浮点余量。结尾点出 image effect 本身只画一个全屏 quad，所以不需要操心半透明物体的排序问题。

## 关键要点

- `_CameraDepthTexture` 是 Unity 在 image effect 上下文里自动暴露的深度纹理，不需要手动 enable。
- `UNITY_SAMPLE_DEPTH` 从深度采样的颜色值里提取 z，`Linear01Depth` 把非线性 z 变成 `[0, 1]` 的线性深度。
- 相机 far clip plane 的设置会直接影响剪影颜色分布——值过大则近处物体全挤在 0 附近。
- 用 `lerp(near, far, depth)` 就能实现 Silhouette / 彩色雾的效果；作者还建议用 `pow()` 调节对比度。
- 不透明物体可任意顺序绘制；半透明必须从后往前且通常不写深度——这是 image effect 不必操心的问题，因为它只画全屏 quad。

## 链接到的概念

- [[depth-texture-silhouette]]
- [[z-buffer]]
- [[scene-color-depth-nodes]]
- [[unity-image-effect-basics]]

## 原文

- 链接：https://danielilett.com/2019-05-04-tut1-2-smo-silhouette/
- 本地：`raw/articles/danielilett.com/2019-05-04_image-effects-part-2-getting-deep.md`
