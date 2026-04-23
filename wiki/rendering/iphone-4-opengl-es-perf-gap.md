---
tags: [opengl-es, mobile, iphone-4, 性能, tbdr, x-plane]
date: 2026-04-19
sources: 1
---

# iPhone 4 的 OpenGL ES 性能断崖

[[ben-supnik|Ben Supnik]] 2014 年底写 X-Plane 10 Mobile 的性能复盘：整个项目以 iPhone 4 作为最低机型，但这一代设备不是"慢 20%"——而是"代码在新机上正常跑，在 iPhone 4 上像要把自己撞死"的彻底断崖。相邻一代的 iPad 2 / iPhone 4S 都远优于它。最终 Chris 把最低 OS 抬到 iOS 8，直接剔除 iPhone 4。

## 三条可观测的症状

- **顶点数瓶颈**（唯独 iPhone 4 独有）。Tiler utilization 95%+、renderer utilization < 30%，减 fragment shader 复杂度完全不动指针；只有减 varying 数量和纯顶点数才能救。他们已经 LOD 掉能砍的一切，3D 驾驶舱里还是卡。
- **varying 对"如何打包"极其敏感**。把 fog 与 emissive light level 打进一个 `vec2` varying，比两个 scalar 显著加速；减 varying 总数提升最大。但大多数 varying 其实是在喂 texture lookup（UV），必须留在 `XY` ——**不能无脑塞满 `vec4`**。评论区 Mihai 追加一条：SGX543 上把 UV 解包放在 fragment shader 会变成 **dependent texture lookup**，比直接 varying 传进来慢得多。
- **orphaned VBO 池回收很贵**。帧每帧 discard + respecify VBO，驱动花在回收"孤儿 buffer"上的时间很可观。有意思的是，他后来意识到这条 bug 后回 profile 新设备，发现新机上 orphan 代价 < 1% ——要么硬件改好了，要么 iOS 8 驱动动了。**在老机上才能看出来的性能坑**。

## 为什么这条故事重要

Supnik 在文末点出 OpenGL / GLES 的深层问题：**规范只说 API 做什么，不说多快**。性能不是保证的、不是决定性的、常常只在 IHV 的 presentation 里才能找到。他特意提到 Metal（以及后来的 [[vulkan-explicit-performance|glNext/Vulkan]]）的一个核心卖点正是「**确定性性能**」——API 告诉你哪些路径贵、哪些不贵。这成为他三个月后评 Vulkan 时的核心论据之一。

## 与其它经验的接口

- [[vbo-double-buffering-orphaning]]、[[supnik-vbo-really-double-buffered]] —— VBO 孤儿机制在他早年的博客里反复出现，这次是它在 iPhone 4 上的代价。
- [[hsr-tbdr]]、[[tbdr-vs-imr]] —— PowerVR SGX 是 TBDR，tiler utilization 95% 的含义与 IMR 完全不同，顶点阶段是绑着 tiler 跑的。
- [[gpu-hang-deferred-fault-debugging]] —— 同系列 PowerVR 设备上他早先遇到的另一个延迟爆崩案例。

## 关键教训

Supnik 写这篇时已经把 iPhone 4 从支持列表剔掉。**他承认自己没有彻底搞清楚"为什么是 iPhone 4 这一代"——未解**，但留下了可复用的性能手术套路：减 varying 数、打包 varying、避免 UV 在 fragment shader 里做二次解包、别把 VBO 当一次性 buffer 用。

## Sources

- [[sources/supnik-iphone-4-perf-gap]]
