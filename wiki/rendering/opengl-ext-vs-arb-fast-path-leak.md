---
tags: [opengl, driver, fast-path, fbo, leaky-abstraction]
date: 2026-04-19
sources: 2
---

# EXT vs ARB：驱动 Fast Path 的隐式契约

[[ben-supnik]] 2011 年 6 月在 X-Plane 调 Linux/ATI G-Buffer 时撞见的一组典型「规范从入口分叉」问题，串起了 OpenGL 扩展版本语义与驱动 fast path 的两面。

## EXT 与 ARB 变体不是同一条规则

X-Plane 混用 RGBA8 与 RG16F 做 MRT 时，ATI 驱动返回 `GL_FRAMEBUFFER_INCOMPLETE`。Supnik 的第一反应是驱动 bug，更新到 Catalyst 11-5 后其他阴影问题的确修好，但这条 FBO 不完整错误仍在——因为规范真的这么写：`GL_EXT_framebuffer_object` 要求所有 color attachment 的 internal type 一致，`GL_ARB_framebuffer_object` 放宽了这一条。同一个 FBO 对象，从 `glGenFramebuffersEXT` 进还是 `glGenFramebuffers` 进，驱动用的是两套规则。驱动写手必须**按入口点跟踪对象的「变体」**并应用不同的完整性检查，否则混用会行为未定义。这件事的代价被悄悄转嫁给了驱动工程师——从 API 设计角度看，EXT 到 ARB 的「柔性升级」其实把历史包袱永久写进了驱动实现。X-Plane 的应对是沿用 [[opengl-extension-bucket-strategy]] 的粗粒度桶：要上 DX10 级硬件就整体切换 ARB 入口点，不在同一个 FBO 上混入口。

## Fast path 是文档外的 if 瀑布

另一篇同日随笔用伪代码揭示了驱动内部是怎么决定「这个 VBO 走加速路径还是 fallback」的：结构体对齐是否是某个模的倍数、源是否在 AGP、size 是否落在某个区间、命令缓冲还有多少空闲、甚至 `FIX_STALL_BUG` 分支里写着「今天不是 AGP 星期二」的时间条件——层层 `&&` 过后，几十个条件才能共同决定是否进 fast path。从 OpenGL API 表面看不出这些条件，它们就是 Joel Spolsky 意义上的 leaky abstraction：抽象掩盖不了性能侧的实现细节。

Supnik 给的实证是 X-Plane 在 Apple Instruments 2.x Time Profiler 里的一次 trace：某帧 67% 时间卡在 `glCopyTexSubImage2D` 上——其中 57% 花在 `gldFinish`（Apple 请求 nVidia 完成像素 fill 的同步），8% 落在 `glgProcessPixelsWithProcessor`（CPU 做像素操作）。Driver Monitor 的两个指标同时报警：**time spent waiting in user code** 非零（本该非阻塞的调用阻塞了），**texture page off bytes** 非零（VRAM 被拖回 host）。根因是代码里用 `glCopyTexImage2D` 把 RGBA16F 表面回读到 RGBA8 纹理以处理 gamma 不匹配——驱动完全有权对这种格式转换 punt（退化到 CPU 路径）。把两面改成同格式并走 FBO 后 stall 消失。这个案例就是 [[api-fast-path-design]] 里「快路径需要被公开承诺」的反面教材：当驱动只在内部维护 fast path 条件、不在文档里声明，客户端只能通过 profiler 反推契约。

## 两面一体

这两篇博文讲的其实是同一件事的上下半场：**OpenGL 规范把「哪条路径快、哪种格式合法」藏在了驱动实现里**。上半场 EXT/ARB 语义分叉让客户端必须理解扩展版本对应的语义细节；下半场 fast path 条件让客户端必须通过 profile 才能找到驱动未公开的偏好。X-Plane 长期的应对策略——把 FBO/VBO/GLSL 等扩展做成细粒度可开关（[[opengl-extension-bucket-strategy]]），并在每个关键上传路径上做端到端 profiler 验证——正是把这类隐式契约显性化的工程手段。

## 相关

- [[api-fast-path-design]]
- [[opengl-extension-bucket-strategy]]
- [[xplane-gbuffer-format]]
- [[agp-vs-vram-streaming]]

## Sources

- [[sources/supnik-ext-vs-arb-fine-print]]
- [[sources/supnik-guessing-fine-print]]
