---
tags: [gpu, ios, gpgpu, opengl-es, historical]
date: 2026-04-14
sources: 1
---

# OpenGL ES Transform Feedback 的 GPGPU 滥用

这是一段**已经过时但仍有启发**的 iOS 早期 GPGPU 技巧：在 A7 芯片 + OpenGL ES 3.0 的年代，Apple 还没开放 Metal compute、也没公开 OpenCL，[[bartosz-ciechanowski|Bartosz Ciechanowski]] 发现可以用 **Transform Feedback** 把 vertex shader 当成通用计算器——让 shader 输出直接写回 buffer，绕过光栅化。

## 核心做法

整套魔法只有三步：

1. 链接 program 前调用 `glTransformFeedbackVaryings` 声明要捕获哪些 vertex shader 的 `out` 变量。
2. 画 `GL_POINTS` 时开 `GL_RASTERIZER_DISCARD`——告诉硬件「我压根不要光栅化，也不要 fragment shader」。
3. `glBeginTransformFeedback(GL_POINTS) → glDrawArrays(...) → glEndTransformFeedback()`，vertex shader 的输出进 `GL_TRANSFORM_FEEDBACK_BUFFER` 绑定的那块 buffer。

CPU 可通过 `glMapBufferRange` 直接读这块内存，因为 iOS 是**统一内存架构**，没有 RAM↔VRAM 拷贝开销——这和桌面 CUDA 的 [[cuda-memory-hierarchy|显式 host/device 传输]]完全相反。

## 什么情况下能赢

作者的基准测试给出三档非常清晰的画像：

- **线性 `3.4*x+10.2`**：CPU 三倍碾压 GPU。clang `-Ofast` 会把它变成 NEON 向量 FMA，GPU 启动开销赚不回来。这是典型 [[latency-vs-throughput|低算术强度]]场景。
- **`2*exp(-3x)*(sin(0.4x)+cos(-1.7x))+3.7`**：输入 ≥ 2^16 后 GPU 开始领先，在大规模输入上达到 5× 加速。
- **中心引力场 Euler 积分 100 步**：GPU 快 **64×**。迭代算法对 GPU 特别友好——每个数据项在寄存器里连续跑 100 步，不走内存；CPU 版本只能一个一个解算。

结论三条：**数据集要大、算术强度要高、要迭代。**三者缺一就别折腾 GPU。

## `vec4` 纪律

shader 里把标量合并成 `vec4` 操作比分散的 `float` 快 3.5×——A7 的 ALU 本来就是 4 宽向量机。A7 平台硬上限：`MAX_VERTEX_ATTRIBS = 16` 个输入 `vec4`，`GL_MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS = 64` 也就是 16 个输出 `vec4`。超过这个就没得玩。

## 精度注意事项

GLSL ES 的 `highp` 名义上是 IEEE 754 float，但**舍入模式没在 spec 里规定**。单纯的算式只差 1 ULP；迭代 100 步的物理积分最坏可以攒到 100 ULP 差——对游戏和可视化完全够用，对科学计算就不行了。

## 为什么说「过时」

作者自己在文首加了醒目的 historical-reference 提示。现代 iOS 上应该用 **Metal compute shader**（见 [[metal-api-overview]] 与 [[metal-shading-language-basics]]），可读可写、有原子操作、没有这些 `GL_RASTERIZER_DISCARD` 式的 hack。但作为一段**在 API 缝隙里榨取硬件**的故事，它仍然是每个想理解图形 API 演化的工程师该读的——它告诉你为什么 Khronos 后来非得推 compute shader，为什么 Apple 要从 OpenGL ES 彻底切到 Metal。

相似的「用渲染 API 偷做计算」思路也能在 [[gpgpu-json-parsing]] 和 [[gpgpu-string-unescaping]] 上看到，只不过那两者用的是 fragment shader + float texture 写回。

## Sources

- [[sources/ciechanow-exploring-gpgpu-ios]]
