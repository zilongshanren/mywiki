---
tags: [source, 渲染, gpu, 架构, tbdr, 硬件]
date: 2026-04-14
sources: 1
---

# Tiled hardware (speculations)（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2017 年 8 月的一篇思辨性长文，起因是他在 SIGGRAPH 上和一些移动 GPU 工程师讨论 [[tbdr-vs-imr|TBDR vs IMR]]，回来后在博客里把自己（软件视角的）理解整理出来，邀请硬件侧的人打脸。评论区里 [[fabian-giesen|ryg]] 给出了一轮非常权威的修正，让这篇 post 成为关于 TBDR 内部权衡的一个经典对谈。

## 摘要

Pesce 从一个自嘲的免责声明开场（「我对硬件几乎一无所知」），然后用软件工程师能理解的语言把 TBDR 的流水线拆开：**先跑一遍（或至少部分跑）vertex shader 算出屏幕位置**，把每个三角形的位置和索引按 tile 分 bin、可能先做一轮 backface culling 压缩，然后每个 tile 内部做 **per-tile 可见性**（排序 + z-test），最后执行剩余的 vertex 工作和 fragment shader——实际上相当于在 tile 粒度上达到了「**完美剔除**」（除了可能多出的 quad helper 线程）。

**Pros（TBDR 的优点）**：
1. 硬件级的完美 [[culling]]，不浪费 [[fragment-shader]] 执行。
2. 所有 [[rendering-pipeline|render target]] 可以放进**片上 per-tile 小内存**里，低延迟、省带宽。
3. 这块片上内存实质上是一个**多 pass rendering 的 scratchpad**，让 deferred shading 的带宽成本几乎消失。
4. Tile 内 pixel shader wave 的屏幕区域被限定，某些常量可以从 vector 变 scalar（对 Forward+ 特别有用）。
5. Tile memory 快，**可编程 blending** 变得可行。
6. Vertex 数据在 tile 里驻留时可以被**多个 shader 回收使用**。

**Cons（为什么桌面不用 TBDR？）**：
1. 占用芯片面积，这块面积如果拿去放计算单元和 latency hiding，可能更有用。
2. IMR 并不是必须 overdraw——**做完整的 depth pre-pass + Early-Z 等价于拿到同样的完美剔除**，甚至可以配合 visibility query / compute 做逐三角形 culling。
3. 带宽权衡不对称：TBDR 写的是 per-tile 的三角形 bin，IMR 写的是压缩 z-buffer；当三角形越来越密集时，z-buffer 反而更省。
4. 软件可以做 adaptive 的 trade-off（部分 occluder prepass、reproject 上一帧 Z 等等），硬件方案是死的。
5. 最终差异其实是**功耗 vs 带宽 vs 墙钟性能**的三角：移动端优化功耗选 TBDR，桌面优化墙钟时间选 IMR 配 latency hiding。

Pesce 的结论带点「历史路径依赖 + 专利壁垒」的味道：两种架构在合适的工作负载下差距不大，现状更多是各家积累和法律壁垒造成的。**Post-scriptum** 里他点评了 NVIDIA / AMD 新出的「伪 tiled」：他认为这些本质上只是 render target 带宽优化，**不能真正用作多 pass scratchpad**，因此从软件侧看没那么有意思。

## 评论区：Fabian Giesen 的硬件侧修正

[[fabian-giesen|ryg]] 在评论里补了几个重要细节，值得单独记下：

- **三角形 bin 不是纯 per-tile 的存储**，而是一个「**unified scratch buffer**」，按块分配、可以流到 memory。溢出时会触发部分 flush（把当前 bin 渲出去），代价很高，必须尽量避免。Bin 内容是压缩的。
- **Vertex shader 分两段**确实可行，Omatic 就这么做过，但代价是：晚期（per-tile）的 vertex 工作对每个引用到该顶点的 tile 都要重跑；而如果把完整输出放 mem 里则只跑一次。更糟的是这种「late VS」的 index 次序已被排序打乱，memory access pattern 更差。
- **可编程 blending 的难点不是 memory 速度**，而是 fragment shader 最后 blending 阶段必须 in-order。固定大小的 tile（比如 32×32）配一个 16×16 quad 的 scoreboard 就能检测冲突，非常便宜；而 IMR 下你根本不知道要跟哪个其它 warp 同步，难得多。
- **Triangle count 才是 TBDR 的大敌**：假设 triangle 平均覆盖 5 像素、直径约 2.24 像素，一个 32×32 tile 大约有 14×14 = 225 个顶点，每顶点 32 字节 attribute payload（8 标量 float）就是 7.2k bytes / 1k pixels ≈ 56 bits/pixel。PC 带宽下勉强，**移动带宽下已经开始紧张**；再密一点或多几个 attribute 就爆。
- **Wave/warp 大小**：tiler 天生想要小 wave——32×16 的 tile 只有 512 pixels，一个 shader 最多 8 个 full GCN wave；现实里一个 tile 通常被 2-3 个 shader 触达，每个 shader 只有 3-4 个 wave，其中一个是半满的——**wave utilization 天然吃亏**，且 shader core 要更频繁地换 shader state。
- **关于 alpha test / blending 的破坏**：带 alpha test、真正的 blending、写 output Z 等都**不走 deferred 路径**，不享受完美 overdraw 消除。所以强烈建议「不透明先画，alpha/透明后画」。

另一位匿名评论者补充了一个移动端的观感：4K 分辨率全屏粒子 overdraw 在 TBDR 上「只要不 round-trip 到 memory 就几乎免费」，这是上一代主机 IMR 完全做不到的；pet peeve 是 GLES 2.0 iOS 只让 fragment shader 读 framebuffer color 而不给读 depth，虽然两者都在片上。

## 关键要点

- **TBDR 的真正杀手锏不是光「省带宽」**，而是**把 render target 变成可被软件复用的片上 scratchpad**——Pesce 认为这才是它对软件侧意义最大的地方，也是现代「伪 tiled」桌面 GPU 没提供的功能。
- **完美剔除不是 TBDR 独有的**：IMR 的 depth pre-pass + Early-Z 从结果看等价，Z pre-pass 的代价其实和 TBDR 的 bin 写回代价可比。
- **Triangle density 决定胜负**：三角形越密，TBDR 需要在内存里 shuttle 的 vertex data 越多；越稀疏，TBDR 越占便宜。
- **功耗 vs 墙钟时间是根本轴**：移动端愿意为了省电放面积做 tiling；桌面愿意为了墙钟时间砸 bandwidth 和 latency hiding。两种生态的分化不是偶然。
- **in-order blending 的调度**是 TBDR 能做可编程 blending 的真正原因——是 scheduling 问题，不是 memory 速度问题。
- **Alpha test / `discard` / 写 depth** 依然是 TBDR 的敌人（见 [[hsr-tbdr]]、[[early-z-late-z]]），这些路径走不到 deferred 通道。
- 这篇文章本身也是关于「**如何公开地思考自己不完全懂的东西**」的范例：Pesce 明确说自己会错，鼓励读者纠正，最终评论区给出的硬件侧信息比正文还有价值。

## 链接到的概念

- [[tbdr-vs-imr]]
- [[hsr-tbdr]]
- [[deferred-rendering]]
- [[early-z-late-z]]
- [[overdraw]]
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[culling]]
- [[angelo-pesce]]
- [[fabian-giesen]]

## 原文

- 链接：http://c0de517e.blogspot.com/2017/08/tiled-hardware-speculations.html
- 本地：`raw/articles/c0de517e.blogspot.com/2017-08-07_tiled-hardware-speculations.md`
- 相关：Apple *GPU family 4 / imageblocks* 文档（Metal）
