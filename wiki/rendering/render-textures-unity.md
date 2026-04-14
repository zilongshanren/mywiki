---
tags: [unity, 渲染, 纹理, gpu, shader]
date: 2026-04-14
sources: 1
---

# Render Texture（Unity 的运行时贴图）

**Render Texture** 是 Unity 里专门为「在运行时被相机或 shader 写入」准备的特殊贴图。它和普通 `Texture2D` 最大的区别是：内容存在 **GPU** 上、由渲染管线在帧内填充，而不是从磁盘载入的静态资产。它是 Unity 做后处理、镜面、Portal、监控屏、粒子轨迹（雪地脚印、水面涟漪、草地交互）等一切「需要 GPU 中间结果」效果的基础设施。

## 三种生产方式

最常见的用法是给一个 **Camera** 设置 `Target Texture`：相机原本写到 backbuffer 的内容现在写到 RT。配合 **Culling Mask** 限制图层（比如只渲染某个特殊层的粒子），就能把「世界里某些东西」拿出来当贴图用，而不污染主相机的画面。第二种是在 C# 里用 `RenderTexture` 构造函数手动 new 一张——这种方式更灵活，但要记得显式 `Release()`，否则 GPU 显存会泄漏。第三种是通过 `Graphics.Blit` / Renderer Feature 的临时 RT，由命令缓冲区管理生命周期，这对应 [[blit-render-feature|Blit Render Feature]] 的全屏后处理路径。

## Color Format 命名解码

RT 的 `Color Format` 选项看起来像一堆乱码——`R8G8B8A8_UNORM`、`R16_SFLOAT`、`R32G32_UINT`——但其实是 Vulkan/D3D12 风格的 GPU 格式命名规范：

- 数字部分指通道数和每通道位深：`R8G8B8A8` = 4 个 8 位通道；`R16` = 单个 16 位红通道。
- 后缀决定数值的解释方式：**UNORM** 解码为 `[0, 1]`、**SNORM** 为 `[-1, 1]`、**UINT/SINT** 为整数原值、**SFLOAT/UFLOAT** 为浮点、**SRGB** 为带 sRGB 解码的 UNORM（alpha 仍然线性）。HDR 渲染需要 `16` 或 `32` bit `SFLOAT`；想存负值（比如运动矢量、SDF）就得用带符号格式。

不同平台对格式的支持度不同，所以 RT 面板上有个 `Enable Compatible Color Format` 选项做兜底回退。**不需要的通道一定要砍**：`R8_UNORM` 比 `R8G8B8A8_UNORM` 省 4 倍显存，对手游和移动端尤其重要。

## 在 CPU 上读 RT：`AsyncGPUReadback` 的存在意义

RT 的数据正常情况下不应该跨过 GPU/CPU 边界——但有时候逃不掉，比如游戏逻辑要根据「玩家脚下的 RT 像素颜色」决定是否生成水花粒子。两条路：

- `Texture2D.ReadPixels`：把当前 active RT 拷到 `Texture2D`，**同步阻塞 CPU**，会把渲染管线的延迟全暴露出来。对单帧偶尔一次还能接受，每帧调用基本不可用。
- **`AsyncGPUReadback.Request`**：异步请求，提交后 1-3 帧后才能拿到结果，但不阻塞 CPU。这是 Unity 给「需要 RT 数据但又不想付管线 stall 代价」的官方答案——非常重要的一个 API。

异步读回有两种使用模式：自己维护一个 `Queue<AsyncGPUReadbackRequest>`，每帧 poll `request.done`；或者用带 callback 的 overload，请求完成时直接调函数。回读支持指定一个矩形子区域（包括单像素），但**不会**告诉你查询用的坐标——如果需要追踪，得把坐标包成自定义对象一起入队。Cyan 在自己水面交互项目里就用 `RequestPixel(x, y)` 单像素读回，根据玩家世界坐标算出 RT 上对应的像素位置。

API 还有几个坑：`SNORM` 格式的 RT 在 `AsyncGPUReadback` 上会报错；HDRP 的相机如果开了 PostProcess，写入 RT 时负值会被 clamp 掉，必须在 Custom Frame Settings 里关掉 PostProcess override 才能保留负数。

## 和别的概念的关系

Render Texture 是 Unity 早期 image effect 的载体——`Camera.OnRenderImage` 会传入 source/dest 两张 RT，让你写 `Graphics.Blit` 链。后来 [[urp-volume-post-processing|URP PPv3]] 改用 CommandBuffer + Renderer Feature 路径，但 RT 仍是底层货币：[[blit-render-feature|Blit Render Feature]] 内部就是申请临时 RT 做 ping-pong（见 [[ping-pong-surfaces]]）。把 RT 当 shader 输入也很常见——shader 里声明一个 `Texture2D` property，C# 端 `material.SetTexture` 把 RT 塞进去即可，从 shader 视角它和普通贴图无异。

## 相关

- [[blit-render-feature]]
- [[urp-volume-post-processing]]
- [[ping-pong-surfaces]]
- [[scene-color-depth-nodes]]
- [[unorm-float-conversion]]

## Sources

- [[sources/cyan-render-textures]]
