---
tags: [source, unity, 渲染, 纹理, gpu]
date: 2026-04-14
sources: 1
---

# Render Textures（Cyan）

[[cyanilux|Cyan]] 2019 年 7 月发表的 Unity 入门博客，系统讲解 **Render Texture** 对象的创建、配置、color format 含义，以及通过 **`AsyncGPUReadback`** 异步把 RT 数据从 GPU 拉回 CPU 的标准做法。

## 摘要

Render Texture 是 Unity 里专门用于 GPU-side 中间结果的特殊贴图。最常见的创建方式是给 Camera 设 Target Texture，配合 Culling Mask 限制只渲染特定层；也可以在 C# 里 `new RenderTexture(...)`，但要记得 `Release()` 否则显存泄漏。Color Format 命名遵循 Vulkan/D3D 风格：`R8G8B8A8_UNORM` 表示 4 个 8 位通道、解码到 `[0, 1]`；后缀 UNORM/SNORM/UINT/SINT/SFLOAT/UFLOAT/SRGB 分别决定数值的解释方式。HDR 渲染需要 16 或 32 bit SFLOAT；负值需要带符号格式。Enable Compatible Color Format 选项做平台 fallback。

文章后半重点讲在 CPU 上读 RT 数据的两条路：`Texture2D.ReadPixels` 同步阻塞（基本不能逐帧用），`AsyncGPUReadback.Request` 异步但有 1-3 帧延迟（推荐路径）。给出一份完整的 Queue-based 示例代码：每帧 poll `request.done`、`hasError`，完成后 `GetData<Color32>` 拿数据。也支持读单像素或子矩形（通过 mip / x / y / w / h / z / d / format 参数）。坑点：`SNORM` 不被 `AsyncGPUReadback` 支持；HDRP 的 PostProcess override 会 clamp 掉 RT 中的负值。Cyan 自己的应用是水面交互——根据玩家世界坐标算出 RT 像素位置然后单像素读回，判断是否在水里以决定是否生成涟漪粒子。

## 关键要点

- Render Texture 是 Unity 专门为「GPU 中间结果」准备的资产，由相机或 Blit/CommandBuffer 在帧内填充。
- Color Format 命名是 Vulkan/D3D 风格：`R8G8B8A8_UNORM` = 4×8 位通道、`[0,1]` 解码；不需要的通道砍掉省显存。
- HDR 用 16/32 bit SFLOAT；带符号格式才能存负数。
- `Texture2D.ReadPixels` 同步阻塞——只能偶尔用一次。
- `AsyncGPUReadback.Request` 异步无 stall，1-3 帧延迟，是逐帧读 RT 的官方路径。
- `Request` 也支持单像素 / 子矩形读回，但不会自动追踪请求坐标，要自己包装。
- HDRP + 写负值到 RT：必须在 Custom Frame Settings 里关掉 PostProcess override。

## 链接到的概念

- [[render-textures-unity]]
- [[blit-render-feature]]
- [[ping-pong-surfaces]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2019/07/08/render-textures/
- 本地：`raw/articles/cyangamedev.wordpress.com/2019-07-08_render-textures.md`
