---
tags: [source, 渲染, vulkan, 同步, cpu-gpu, timeline-semaphore]
date: 2026-04-19
sources: 1
---

# Frames In Flight Explained（Erfan Ahmadi / Nabla）

[[people/erfan-ahmadi|Erfan Ahmadi]] 2017 年写的一篇把 "Frames In Flight" 讲透的文章。动机是行业术语乱——"FramesInFlight"同一个词不同人有不同意思，有人以为是"多帧并行在 GPU 上跑"。Ahmadi 的明确定义是：**CPU 在 GPU 还没做完当前帧的时候，提前录制下一帧的命令**，仅此而已；不涉及 GPU 并行执行多帧。

## 摘要

从最蠢的"submit → 阻塞等 fence → 继续"同步开始讲起：CPU 和 GPU 谁也没重叠。原因是 Vulkan 规定 command buffer 在 pending 状态下不得修改，所以 CPU 想录下一帧就必须等 GPU 用完这块 buffer。改进是加 K 个 command buffer 轮换，每帧用 `frameNumber % K`，`blockForSemaphores` 等 K 帧前的那次 submit 完成即可安全复用——K 就是 FramesInFlight。单帧多 submit（compute / graphics / swapchain-present）时，每个 submit 的 command buffer 都要在录制前 block 一次。另一个容易忽视的限制是 swapchain：`AcquireNextImage` 只能 signal binary semaphore，Nabla 用 binary 模拟 timeline 导致"在飞的 acquire"有硬上限 `imageCount + 2`。因此实际的 framesInFlight 必须 `min(MaxFramesInFlight, swapchain->getMaxAcquiresInFlight())`，而且窗口 resize 重建 swapchain 时可能变，每帧都要重新取不能缓存。

## 关键要点

- 常见误解：以为 FramesInFlight 意味着 GPU 并行多帧——其实只是 CPU 领先 GPU 录制
- 多帧并行在 GPU 上不可行：要复制所有动态资源 + 后续帧抢占前帧执行单元 + VRAM 压力
- Vulkan spec：command buffer 在 pending 状态禁止修改 —— 这是为什么必须等 fence
- Timeline semaphore 是理想的表达工具：单调计数器，自然支持"等 K 帧前的那次 submit"
- 每个独立 submit 都要自己的 block 逻辑（六次 submit 就有六处）
- swapchain 可用 image 数也是 frames-in-flight 的硬上限；必须动态取，不要缓存
- 输入延迟与 frame pacing：CPU 领先太多会让手感变糊

## 链接到的概念

- [[frames-in-flight]]
- [[gpu-fence-timeline-semaphore]]
- [[streaming-staging-texture-upload]]
- [[async-compute]]
- [[linear-allocator]]
- [[people/erfan-ahmadi]]

## 原文

- 链接：<https://erfan-ahmadi.github.io/blog/Nabla/fif>
- 本地：`raw/articles/erfan-ahmadi.github.io/2017-03-01_frames-in-flight-explained.md`
