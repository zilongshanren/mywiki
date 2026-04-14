---
tags: [source, gpu, ios, gpgpu, opengl-es]
date: 2026-04-14
sources: 1
---

# Exploring GPGPU on iOS（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年 1 月发表的早期文章（后被作者自己标注为「historical reference」），介绍了在 OpenCL 未开放的年代，如何在 A7 芯片 + OpenGL ES 3.0 上**滥用 Transform Feedback** 把 GPU 当通用计算器用。

## 摘要

文章的核心发现是 OpenGL ES 3.0 的 Transform Feedback 配合 `GL_RASTERIZER_DISCARD`，可以让 vertex shader 的输出直接写回 buffer，绕过光栅化和 framebuffer，把 shader 变成数据流处理器。配套的三组基准（线性函数 → CPU 赢；exp/sin/cos 混合 → 输入大到 2^16 时 GPU 反超；中心引力场 Euler 积分 → GPU 快 **64 倍**）展示了 GPGPU 真正赢面在于**大数据集 + 非平凡算术 + 迭代**。文章还讨论了 iOS 的统一内存架构让 `glMapBufferRange` 的读写零拷贝、`vec4` 向量化比标量 `float` 快 3.5 倍、以及 GPU vs CPU 的 ULP/相对误差分析（最大 100 ULP 出现在 100 步迭代累积）。对现代 iOS 开发者已过时，但作为一段**在 API 缝隙里榨取硬件**的历史样本依然有趣。

## 关键要点

- **Transform Feedback 技巧**：`glTransformFeedbackVaryings` + `GL_RASTERIZER_DISCARD` + `glBeginTransformFeedback(GL_POINTS)`，vertex shader 输出直接写到 buffer。
- **三条性能规律**：简单 FMA → CPU 靠自动向量化反而赢；复杂标量函数 → 交叉点在 2^16；迭代物理 → GPU 加速 64×。
- **统一内存的福利**：iOS 没有 RAM→VRAM 拷贝开销，可以边算边读。
- **向量化纪律**：一次 `vec4` 比四次 `float` 快 3.5 倍；`MAX_VERTEX_ATTRIBS = 16` 和 `GL_MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS = 64` 是 A7 的输入/输出上限。
- **精度警告**：GLSL ES 的舍入模式未定义，100 步迭代可累积 100 ULP 差异。
- **已过时声明**：作者本人在文首写明现代 iOS 应用 Metal compute shader。

## 链接到的概念

- [[gpgpu-transform-feedback-ios]]
- [[gpgpu-json-parsing]]
- [[gpgpu-string-unescaping]]
- [[metal-api-overview]]
- [[cuda-memory-hierarchy]]
- [[latency-vs-throughput]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/exploring-gpgpu-on-ios/
- 本地：`raw/articles/ciechanow.ski/2014-01-05_exploring-gpgpu-on-ios-bartosz-ciechanowski.md`
