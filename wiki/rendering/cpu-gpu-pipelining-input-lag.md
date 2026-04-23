---
tags: [渲染, cpu-gpu, 延迟, 输入滞后, vsync, triple-buffering]
date: 2026-04-19
sources: 1
---

# CPU/GPU 1 帧流水线与输入滞后

[[joost-van-dongen|Joost van Dongen]] 2011 年写 Awesomenauts 做性能分析时，发现自己读完 OpenGL Red Book 也没读到的一件事：**他以为的 CPU/GPU 时序是错的**。他问了一圈 Ronimo 外的资深图形程序员，大多数也没意识到——于是写了这篇"为什么没人告诉我"的帖子。

## 直觉上的错误模型

初学者脑中 CPU/GPU 串行模型是这样：CPU 开始派发 draw call → GPU 立即处理 → 一帧命令发完后 CPU 在 `SDL_GL_SwapBuffers` / `D3DPresent` 里阻塞等 GPU 完成 → 然后下一帧。这个模型里 **GPU 空等 CPU、CPU 空等 GPU**——两头互相浪费，看起来很"蠢"。

Joost 在 PS3/Xbox360/PC 三平台都加了 timer 测量，确实看到 CPU 在 swap 里花了大量时间。他于是做了一套多线程方案，让等待发生在别的线程，下一帧 gameplay 可以并行跑。结果：**三平台 FPS 都没动**。

## 实际上的模型：GPU 永远落后 1 帧

真实行为是：**`SwapBuffers` 里等的不是当前帧的 GPU 完成，而是前一帧**。也就是 CPU 在记录第 N 帧命令时，GPU 还在渲第 N-1 帧。GPU 只要一直有活干（GPU-bound），就不会再空等——CPU 发出的命令直接进 GPU command buffer 等着。

这就是为什么 Joost 的多线程优化没用——当时 Awesomenauts 本来就 GPU-bound，CPU 优化对总 FPS 无益。**第一件事永远是先判断瓶颈。**这和 [[frame-pipeline-latency|Pesce 从引擎架构角度数 stage]]、[[frames-in-flight|Erfan Ahmadi 从 Vulkan 同步角度讲]] 是同一件事的三个侧面：一个从驱动行为、一个从 stage 累计、一个从 command buffer 轮换。

## 代价：至少一帧输入滞后

好处是高吞吐，代价是**用户输入要多等一帧才出画**——game state update 和 "结果上屏" 之间多了一帧 GPU 延迟。Joost 认为这是值得的交易，因为 FPS 提升带来的好处远大于这点滞后。

## Max Prerendered Frames 陷阱

PC 驱动有时会让 GPU 落后不止 1 帧，而是 2/3 甚至更多（NVIDIA 控制面板里 "Maximum Pre-Rendered Frames" 默认就是 3）。30fps + 3 帧 prerender ≈ **100 ms 输入滞后**——Joost 的读者在评论里看到这个数字当场惊呆。Ogre 论坛里有人用户报告巨大输入滞后，就是因为 CPU 太轻、驱动让 GPU 落后很多帧。Proun 的 Linux/Wine 版也出现过类似现象。

问题天然有上限：GPU command buffer 填满后 CPU 就会被阻塞。若需要精确控制，可以用 **fence**（DirectX/OpenGL 的显式同步原语）强制 GPU 不落后超过 1 帧——这和 [[gpu-fence-timeline-semaphore|timeline semaphore]] 做的事一样，只是具体 API 不同。

## 不同平台行为不一

Joost 问了一圈同事整理出一张对照图：PC / PS3 / Xbox360 默认行为有差异，有些平台会更积极地让 GPU 异步下去。**"写一套代码多平台跑"时不能假设等待模式一致**，这是后来做 Awesomenauts 跨平台优化的重要教训。

## VSync 与 Triple Buffering 的位置

Joost 把 VSync 画在"render frame"这一块里——开着 VSync 时 render 这一段变长，因为要等 scanout。VSync 让 GPU idle，若 CPU 本来就在等 GPU，两边都会 idle。Double buffer 下无解：前 buffer 在 scanout、后 buffer 已排好队等 flip，**没有地方画下一帧**。

Triple buffering 的作用是给「下一帧」开第三块 buffer——但**只在帧时间抖动大时才有用**。恒定帧率下多一块 buffer 不会让你超过 VSync 上限，反而徒增滞后；而波动下它能把 14 ms + 18 ms 两帧摊到两个 16.7 ms 槽里，避免把 18 ms 帧降到 30fps。

读者提醒的一个实用细节：`glFinish()` 强制 CPU 等当前帧完成，**等于把你打回错误的直觉模型**——浪费大量 CPU/GPU 空闲时间，不要用它来实现 VSync。

## 相关

- [[frame-pipeline-latency]] —— Pesce 从引擎 stage 累计视角看同一问题
- [[frames-in-flight]] —— Vulkan/现代 API 里 timeline semaphore 的表达
- [[bottleneck-analysis]] —— 先确定是 CPU-bound 还是 GPU-bound 再优化
- [[gpu-fence-timeline-semaphore]] —— fence 限制落后帧数
- [[pc-gpu-driver-compat-qa]] —— Proun 的 PC 驱动血泪（同一作者）
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-gpu-one-frame-behind]]
