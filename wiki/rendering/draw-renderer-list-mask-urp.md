---
tags: [unity, urp, 渲染, renderer-feature, mask]
date: 2026-04-19
sources: 1
---

# DrawRendererList + Layer Mask：URP 自绘遮罩 RT

URP 做很多效果（描边、时之逆转、局部灰度）都需要一张「**只包含某些特定物体**的遮罩纹理」。在 URP 里想拿到这张 RT，最干净的路径是**让一个 `ScriptableRenderPass` 重新跑一遍场景的部分绘制**，但用自己指定的 override material 和 layer mask 过滤——这就是 `DrawRendererList` / `RendererList` API 的用法。Daniel Ilett 在 Zelda Recall 教程里把这套模式完整跑了一遍，可以作为模板。

## 四个过滤器叠在一起

一次 `RendererList` 创建由四样东西同时约束绘制目标：

1. **`FilteringSettings`** 指定 **渲染队列范围**（Opaque / Transparent / all）和 **layer mask**（只画 `RecallSettings.objectMask.value` 这一层的物体）。
2. **`ShaderTagId`** 指定要画的 pass 标签。URP 里常用的有 **`UniversalForward`**（代表 lit 主 pass）和 **`SRPDefaultUnlit`**（当 shader pass 没写 `LightMode` 标签时 URP 自动给它的 fallback）。**要覆盖所有物体就得两次绘制各一遍**——只跑 `UniversalForward` 会漏掉 unlit shader 的物体。
3. **`SortingSettings`** 用相机给出的 sort key（前后顺序、不透明/透明队列）。
4. **`DrawingSettings.overrideMaterial`** 替换每个物体原本的 material——这是做 mask 的关键：不管场景里这个物体原本用什么 shader，`DrawRendererList` 走的时候都改用这个统一的"写白"shader。

拼好后交给 `context.CreateRendererList(ref rendererParams)` 拿到 `RendererList`，再 `cmd.DrawRendererList(rendererList)` 发给 GPU。

## 为什么 override shader 里还要做手动深度测试

当 `DrawRendererList` 在一个**后期插入的 pass**（如 `BeforeRenderingPostProcessing`）里重绘场景子集，虽然深度缓冲里已经有正确的不透明深度，但物体本身不会被自动剪裁——它们会把自己**画在原本已经被遮挡的区域**，导致 mask 扩出画面外的真实轮廓。Ilett 的 `MaskObject.shader` 里手工解决了这个问题：

- vertex 里把 `-mul(UNITY_MATRIX_MV, v.positionOS).z * _ProjectionParams.w` 作为线性深度传给 fragment；
- fragment 用 `VPOS` 语义拿到 pixel space screenUV，从 `_CameraDepthTexture` 取该像素的真实深度；
- 用 `step(i.depth - epsilon, screenDepth)` 只在"自己的深度 ≤ 深度缓冲"的像素写白。

换句话说，override shader 自己承担了**深度测试 + mask 输出**两件事。这个细节非常容易被新手漏掉。

## R8 省带宽

因为只需要 0/1 掩码，目标 RT 可以用 `RenderTextureFormat.R8`——单通道 8bit，一张全屏 RT 在 1080p 下只要 2MB。`RenderingUtils.ReAllocateIfNeeded` 会跟随屏幕尺寸自动伸缩。

## 和 [[blit-render-feature]] 的关系

Blit Render Feature 只做「全屏纹理→shader→全屏纹理」的 ping-pong，不能让特定物体参与。`DrawRendererList` 正是 Blit feature 的互补面：它负责**在 shader pipeline 外把场景按过滤器再画一次到自有 RT**。实战中两者经常串起来——先 `DrawRendererList` 出 mask，再 Blit 做后处理时把 mask 作为 shader 输入。

## 和 Unity 6 Render Graph 的关系

Ilett 强调这套代码是 Unity 2022.3 URP 的写法，Unity 6 的 Render Graph 对 pass 依赖和 resource allocation 做了重构，`RTHandle` + `ReAllocateIfNeeded` 都被 Render Graph 的 builder 接管——老代码需要打开 compatibility mode 才能跑，这个兼容模式最终会被移除。

## 相关

- [[blit-render-feature]]
- [[urp-volume-post-processing]]
- [[depth-texture-silhouette]]
- [[stencil-buffer]] —— 另一条「标出哪些像素属于目标物体」的路径，不用额外 RT
- [[render-textures-unity]]
- [[custom-mask-shaders]]

## Sources

- [[sources/danielilett-zelda-recall-rune]]
