---
tags: [渲染, 性能, gpu, compute-shader]
date: 2026-04-14
sources: 1
---

# 点光栅化：硬件 vs Compute Shader

**渲染数百万到数千万的「单像素点」时，固定功能光栅化往往不是最快的路径**——一个朴素的 compute shader 配合 atomic add 在所有主流 GPU 上都能跑赢内置点光栅化 1.5-10 倍。这个反直觉的结论来自 Aras Pranckevičius 2025 年做的一次跨 30+ 显卡的 WebGPU 实测。

## 故事的起点

Blender VSE 的 waveform/parade/vectorscope 三种「示波器」需要把每个像素根据亮度或 YUV 投到一张二维图上，再做 alpha 累加。原本完全在 CPU 上跑——4K 分辨率下慢得难以接受。直觉是搬到 GPU：每个输入像素发一个点 sprite，让光栅化硬件 + alpha blending 来负责累加。

实现简单，PC 上也快了。但在 M4 Max 上，**vectorscope 慢到 2 FPS**。8M 个点对一颗 M4 Max 来说本应轻松，问题出在哪？

## 病因 1：所有像素都堆在屏幕中心

Vectorscope 把点按 YUV 的 (U, V) 分量投到二维平面上。绝大多数自然图像的像素都在「不饱和」区域，**所有点都落在原点附近的几个像素里**——一张全灰图甚至会让所有点完全重叠。这是一个极端的 [[overdraw|过度绘制]] 病例：每像素几十万次 fragment 写入，串行的 alpha blending 队列直接爆掉。

## 病因 2：固定功能 blending 是串行的

GPU 的 ROP（Raster Operations）/blend 单元必须保证**同一像素 fragment 按提交顺序串行执行**——否则 alpha-over 不再具有正确的语义。这意味着 ROP 后端有一条容量有限的「待 blend 队列」。当太多 fragment 同时落在同一像素时，所有线程在这条队列上排队。详见 [Fabian Giesen《A trip through the Graphics Pipeline 2011, part 9》](https://fgiesen.wordpress.com/2011/07/12/a-trip-through-the-graphics-pipeline-2011-part-9/)。

## 病因 3：单像素点的 quad overshading

GPU 永远以 2×2 quad 为最小单位执行 fragment shader——这是为了跨 lane 计算导数（[[fragment-shader|fragment shader]] 默认行为）。一个单像素点会触发 4 次 shader 执行，其中 3 次的 coverage mask 为 0 被丢弃。Fabian Giesen 称之为 [Counting Quads](https://blog.selfshadow.com/2012/11/12/counting-quads/) 现象。这本身只贡献 4 倍的固定开销，但叠在前两个病因上就放大了。

## 病因 4：Apple GPU 没有固定功能 blending

Apple Silicon 的 fragment 阶段做 alpha blending 时，**shader 自己读旧像素值再写回**——没有专门的 ROP 硬件。要保证 in-order，整条 fragment 流水都得排进某种顺序队列。这解释了为什么所有 GPU 在「点全堆在 5×5 像素」场景下都会慢 2-5 倍，而 Apple GPU 慢 12-19 倍——它没有专门硬件来缓冲并行度。

## Compute Shader 的解法

朴素到不能再朴素的实现：

1. 三张 R/G/B `uint` 缓冲（每像素一个）。
2. 每个点用 `atomicAdd` 把定点颜色加到对应像素。
3. 最后一个 fragment shader pass 把 R/G/B 缓冲解析回可见颜色。

没有 wave/subgroup tricks，没有 tile 化，没有 prefix sum。结果是：

- **正常密度**（4M 点散布在 460×460 区域，每像素约 20 点）：所有 GPU 上 1.5-2× 比内置点光栅化更快；AMD 上夸张到 10×。
- **极端密度**（4M 点堆在 5×5 区域，每像素 16 万点）：跨平台均 ~5× 更快。

## 为什么原子加比硬件 blending 还快

直觉上「16 万次 atomic add 同一地址」应该比「16 万次 in-order blending」更糟才对——atomic 的争用是全局的，而 ROP 只需要保证局部顺序。但实测反过来。Aras 的猜测是：**ROP 队列容量比 L2 atomic 单元的吞吐小得多**，且 ROP 必须保证完整的 in-order 语义，而 atomic add 天然可交换，只需保证 read-modify-write 原子性即可。

这暗示了一个更大的趋势：**alpha-over 这种顺序敏感的合成原语，对 compute-based rendering 非常友好；改成 atomic add（或 64 位 atomic min/max）之后，「顺序」这个约束就消失了**。这正是 Media Molecule《Dreams》和 Unreal Nanite 的软件光栅化路径所利用的核心洞察（参考 [Rendering Point Clouds with Compute Shaders](https://arxiv.org/abs/2104.07526)）。

## 隐藏好处：更好的 blending 函数

一旦点累加是在自己的 R/G/B 缓冲里完成，最终的 resolve pass 可以自由选用任何映射函数——非线性的 alpha 曲线、感知均匀的色调映射、对数压缩……这些都是固定功能 blending 做不到的。Blender 5.0 里的 GPU 示波器就利用了这一点，看起来比 4.5 版本更清晰。

## 经验教训

- **「GPU 一定比 CPU 快」是个假设，不是定理**。如果工作负载击中了 ROP/blend 队列、tile 缓冲、quad overshading 这些隐藏瓶颈，硬件路径反而更慢。
- **profiler 不一定能指出真凶**。Xcode 的 Metal frame capture 在这个例子里只会说「fragment shader 慢」，但真实瓶颈是 blending 队列——这是 [[bottleneck-analysis]] 的「unknown unknown」典型案例（参考 [[unknown-unknowns]]）。
- **「贴近硬件」的 compute shader 经常能赢**。哪怕是最朴素的实现，跳过 ROP、跳过 quad、跳过 in-order 约束之后，性能就回来了。

## 相关

- [[overdraw]]
- [[fragment-shader]]
- [[rasterization]]
- [[alpha-blending]]
- [[tbdr-vs-imr]]
- [[bottleneck-analysis]]
- [[draw-procedural-gpu]] —— 另一种 GPU-driven 渲染路径：compute 写 buffer、DrawProcedural 直接消费

## Sources

- [[sources/aras-gpu-point-rasterization]]
