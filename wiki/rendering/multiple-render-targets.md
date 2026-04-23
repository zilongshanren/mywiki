---
tags: [渲染, shader, gpu, deferred, g-buffer]
date: 2026-04-14
sources: 1
---

# 多渲染目标（Multiple Render Targets, MRT）

**MRT** 指片元着色器在一次 draw call 中同时向多个色彩附件写入不同数据。[[xor-shader-artist|Xor]] 在 GM Shaders 的短篇里用一句话概括：把 GLSL 里的 `gl_FragColor` 换成 `gl_FragData[0..3]`，并在宿主端把最多 4 张 surface 绑到同一个 render target slot 上，这次 draw 就会一次性产出 4 份输出。底层的硬件能力早已存在，但它真正的价值不是「多一倍带宽」，而是**让每一次几何提交可以产出任意多的『看得见』与『看不见』的数据**——这正是 [[deferred-rendering]] 的前提，也是许多画面外效果的基础。

## 使用场景

最经典的用途就是延迟渲染的 **G-Buffer**：albedo、normal、roughness/metallic、emissive、motion vectors 各占一张 RT，几何 pass 一次写完之后，光照 pass 按像素读回做统一的 shading。没有 MRT，G-Buffer 方案就必须把几何画 N 遍——这在 2000 年代早期就是 early deferred 的真实成本，直到 DX9 / OpenGL 2.0 引入多输出能力后才被彻底摊平。

Xor 在自家 idle game [*Constructor*] 里演示了另一种非典型用途：**Object ID buffer**。每个物体输出一个独特的 ID 色（`vec3(i, 0, 0) / 255`），画完主图的同时第二张 surface 上是按物体分块的 ID 图；随后的 outline pass 只要比较邻域的 ID 是否相同即可画轮廓，而被 highlight 的物体也能靠 ID 精确筛选。一次几何提交同时产出了「画面」「ID 图」两种视图，完美对应「MRT = 同几何多视图」的思维模型。

另一条路是**自建 depth**：GameMaker 当时没开放 depth buffer，但用 `gl_FragData[1]` 手写一个 float depth 到额外 surface，就能让 SSAO、阴影图这类需要深度的后处理工作起来。

## 代价与限制

- **平台兼容性**：HTML5 对 MRT 的支持长期缺失；某些低端移动 GPU 即便支持也跑不动多 RT。Xor 直言在低端设备上分多次 draw 可能反而更快——这再次说明 MRT 的前提是「带宽管够」。
- **最多 4 张**：GM 以及大量老 API 硬卡在 1–4 之间，现代 D3D12 / Vulkan 能到 8，但「越多越好」的思路会撞上下面的 VRAM 问题。
- **VRAM 代价**：一块 RT 的大小 = 分辨率 × 每像素字节。4 张全 HD 的 RGBA8 是约 32 MB；升级成 `surface_rgba32float` 立刻翻到 128 MB。作者给的最朴素建议就是：**能用 `r8unorm` 就别用 `rgba32float`**，按需选格式。[[compact-vertex-format|紧凑顶点格式]]的那一套思想在 RT 选型上同样适用。
- **输出共享 rasterization 状态**：所有 RT 共享同一份顶点、同一份 MVP、同一份 `discard`——你没办法让 RT0 剪掉一个像素而 RT1 保留它。
- **2D 游戏可以 `surface_depth_disable(true)`** 关掉隐含的 depth buffer，省一半 surface VRAM。

## 为什么值得单独拎出来

MRT 是一种**控制反转**：原本「每个 draw call 一张图片」的假设被彻底拆开，画面变成「一次采样几何，多次投影出不同用途的数据」。一旦接受这种 mental model，你会发现它不仅解锁了延迟渲染，也让很多奇怪需求（对象 ID、motion vector、velocity buffer、画面外的 height field）都变成「再加一个输出通道」的廉价改动。

## 相关
- [[deferred-rendering]] —— MRT 最主要的消费者，G-Buffer 是 MRT 的典型结构
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[ping-pong-surfaces]] —— 多趟反馈是 MRT 的"时间维度"对照版
- [[d3d12-resource-binding]] —— 现代 API 里 RT 的绑定抽象
- [[tiled-light-prepass]] —— thin G-Buffer + 二次几何的对立路线
- [[visibility-buffer]] —— 现代把 G-Buffer 压到 1 张 + 后续 compute shading 的演进
- [[xor-shader-artist]]
- [[xplane-gbuffer-format]] —— 4 张 MRT / 16 字节的实战布局，配套 GLSL 片段展示了 `gl_FragData[0..3]` 的用法

## Sources

- [[sources/xor-mini-mrt]]
