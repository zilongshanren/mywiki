---
tags: [source, 渲染, vulkan, 资源上传, nabla, staging-buffer]
date: 2026-04-19
sources: 1
---

# Uploading Textures to GPU - The Good Way（Erfan Ahmadi / Nabla）

[[people/erfan-ahmadi|Erfan Ahmadi]] 发表于 2015 年（URL path 在 [[Nabla|Nabla]] 子目录下）的博客，讲他在 Nabla 框架里写的 **streaming 纹理上传工具**——用一块固定大小的 staging buffer 反复分批地把大贴图送上 GPU，顺便完成格式转换，同时保持对 Vulkan `optimalBufferCopy*` 对齐、`minImageTransferGranularity`、binary semaphore 模拟 timeline 等繁琐约束的 conformance。

## 摘要

入门教程的"一图一 staging"做法在真实引擎里立刻崩——独显的 `HOST_VISIBLE + DEVICE_LOCAL` 堆只有 256 MB 左右，一张 MEGA 贴图就能把它榨干；即使用 VulkanMemoryAllocator 之类池化工具，也绕不过堆上限和分配峰值不可预测的问题。Ahmadi 的方案是：开一块固定 64 MB 的 staging buffer，套一个 `GeneralpurposeAddressAllocator` 返回 `(offset, size)`，然后按 "array layer → 3D slice → row → block" 的优先级尽量多塞、塞不下就 submit + 等 fence 回收，下一轮继续。`ImageRegionIterator` 是一个可暂停可恢复的 region 游标。格式转换也流式完成——把 mapped staging memory 伪装成 `ICPUBuffer`，直接对它跑 Convert / Swizzle image filter。

## 关键要点

- 生产级 staging 一定是**固定大小 + 反复复用**，不能"每张贴图申请一次堆"
- 批次优先级：array layer → depth slice → row → block
- 多线程上传支持：range allocator 的"释放"挂在 fence / semaphore hit 上
- 格式流式转换：staging memory 直接当做 `ICPUBuffer` 喂给 filter，零额外 CPU 拷贝
- 接口设计：用户拿 command buffer / fence 给工具，工具内部可能插多次 submit——但 waitSemaphore 只在首次生效、signalSemaphore 只在最后生效
- Vulkan 必须照顾的常量：`optimalBufferCopyRowPitchAlignment`、`optimalBufferCopyOffsetAlignment`、`minImageTransferGranularity`、`nonCoherentAtomSize`

## 链接到的概念

- [[streaming-staging-texture-upload]]
- [[linear-allocator]]
- [[gpu-fence-timeline-semaphore]]
- [[frames-in-flight]]
- [[buffer-renaming]]
- [[people/erfan-ahmadi]]

## 原文

- 链接：<https://erfan-ahmadi.github.io/blog/Nabla/imageupload>
- 本地：`raw/articles/erfan-ahmadi.github.io/2015-01-01_uploading-textures-to-gpu-the-good-way.md`
