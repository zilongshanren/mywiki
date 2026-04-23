---
tags: [渲染, vulkan, 同步, cpu-gpu, timeline-semaphore, swapchain]
date: 2026-04-19
sources: 1
---

# Frames In Flight

**一句话定义**（Erfan Ahmadi）："CPU 告诉 GPU：你先渲这一帧，我趁你忙的时候给你准备下一帧。"

注意：**这不是多帧在 GPU 上并行执行**。多帧并行需要对所有动态资源做副本（否则会触发 WAR/WAW/RAW hazard），VRAM 吃不消，而且更多占用率并不等价于更高吞吐——后面一帧只会去抢前一帧的执行单元，反倒让前一帧完成得更晚。"Frames in flight" 说的始终是 **CPU 在多帧前面准备录制工作**这件事。

## 最蠢的同步：每帧一个 command buffer

```
cmdbuf->begin();
// record
cmdbuf->end();
queue->submit(cmdbuf, wait=N, signal=N+1);
device->blockForSemaphores(N+1);
frameNumber++;
```

为什么非得 CPU 阻塞？因为 Vulkan spec 明说："command buffer 处于 pending 状态时不得修改它。"CPU 想 record 下一帧，就必须等 GPU 真的用完这个 buffer。结果：**CPU 录制时 GPU 空转，GPU 执行时 CPU 空转**。

## 多 command buffer 的重叠

给一组 K 个 command buffer 轮流用：

```
const uint32_t FramesInFlight = 3;
auto cmdbuf = commandBuffers[frameNumber % FramesInFlight];
if (frameNumber >= FramesInFlight) {
    // 等 K 帧之前的那次 submit 完成
    device->blockForSemaphores({.semaphore=sema, .value=(frameNumber-FramesInFlight)+1});
}
cmdbuf->begin(); /* record */ cmdbuf->end();
queue->submit(cmdbuf, wait=frameNumber, signal=frameNumber+1);
frameNumber++;
```

"FramesInFlight = 3" 意味着 CPU 可以比 GPU 领先最多 3 帧进行录制。[[gpu-fence-timeline-semaphore|timeline semaphore]] 正好用来表达"第 N-K 帧的 submit 是否完成"这个问题——一个单调计数器就够了。

## 单帧多 submit 的推广

实际项目一帧往往不止一次 submit（compute-only、graphics-only、依赖 swapchain 的 present-submit）。规则是：**每个 submit 的 command buffer 都要在录制之前 block 一次**，确认它在 K 帧前的那次使用已完成。六次 submit 就会有六处几乎一模一样的 `blockForSemaphores`。

## swapchain acquire 才是真正的瓶颈

单看 command buffer 数量会让你以为 `MaxFramesInFlight` 可以任意大，但 swapchain 会反过来卡你。

`AcquireNextImage` 给你一个 image index，但**不保证这张 image 立刻可用**——它会 signal 一个 semaphore，submit 时必须 wait 这个 semaphore 才真正安全。Vulkan 的 [acquire 规定](https://registry.khronos.org/vulkan/specs/1.3-extensions/man/html/vkAcquireNextImageKHR.html)它**只能 signal binary semaphore**，因此在 Nabla 这种用 binary semaphore 模拟 timeline 的实现里，可在飞的 acquire 数量有硬上限——`swapchain->getMaxAcquiresInFlight()` 当前返回 `imageCount + 2`。

实际的 frames-in-flight 需要**取 min**：

```
const uint32_t framesInFlight = min(MaxFramesInFlight, swapchain->getMaxAcquiresInFlight());
```

- `MaxFramesInFlight` 用来**索引 command buffer**（这是你自己声明的上限）
- `framesInFlight`（动态、可能被 swapchain recreate 改变）用来**决定要 block 几帧**

例子：8 个 command buffer + 3 张 swapchain image → `min(8, 3+2) = 5`，每次最多 5 帧在飞。窗口 resize 会重建 swapchain、image count 可能变，所以必须每帧重新问一次，不能缓存。

## 和输入延迟的权衡

如果 CPU 极快地 poll 输入 → record → submit，CPU 可能已经跑到 5 帧之后，屏幕上显示的帧其实对应 5 帧之前的输入，**手感变糊**。故意 CPU sleep 一下、让 CPU 紧跟 GPU，可以降低感知延迟——这就是很多游戏引擎做的 "frame pacing"。

## 相关
- [[gpu-fence-timeline-semaphore]]
- [[streaming-staging-texture-upload]] —— Nabla 的 staging 用同一套节奏
- [[linear-allocator]] —— 每帧一段的 ring 内存
- [[async-compute]] —— 跨队列 submit 也走这套同步
- [[simplified-pipeline-barriers]]
- [[people/erfan-ahmadi]]
- [[cpu-gpu-pipelining-input-lag]] —— 同一机制的 2011 独立开发视角版本

## Sources

- [[sources/erfan-ahmadi-frames-in-flight]]
