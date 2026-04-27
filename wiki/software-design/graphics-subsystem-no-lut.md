---
tags: [图形, 软件设计, 图形子系统, 查找表, 设计原则, 带宽]
date: 2026-04-27
sources: 1
---

# 图形子系统设计原则：避免查找表

这是 Wolfgang Engel（Humus 博客系列"Rules for Designing Graphics Sub-systems"第二条原则）提出的图形系统设计法则。核心主张是：**现代图形管线应尽量用算术指令替代查找表（lookup table）**，无论是传统的 sin/cos 数学 LUT，还是 lightmap、radiosity map、shadow 贴图这类预烘焙数据。

## 原则背景

GPU 在每一代迭代中，算术吞吐量的提升速度持续超越内存带宽的提升速度。这个趋势在 2000 年代末至 2010 年代初尤为明显。传统上，"打表"是用来换取计算时间的经典手段，但当算术几乎"免费"而带宽成为稀缺资源时，这个权衡方向就反转了。此外，从存储介质（DVD、蓝光）到 PCI-Express 总线都存在带宽瓶颈，任何需要在运行时传输的预烘焙数据都有上传代价。

## 典型的"查找表"模式

Engel 列出的应当警惕的 LUT 类型：

- 把光照方程预计算后存入 2D/Cube/3D 贴图（经典的 radiosity lightmap）
- Megatexture：大块地形纹理，texture synthesis 通常更高效
- 签名距离场（SDF），若其不支持 24 小时动态光照/阴影循环
- 体素数据，若每帧必须重新读取大量数据且不支持动态光照
- 任何锁定了几何体「不可破坏」的贴图：一旦数据烘焙到纹理上，对应几何就难以动态形变

## 折中方案：GPU 内存缓存

并非所有中间数据都必须实时计算。Engel 提出的折中是**将中间结果缓存在 GPU 显存中**，而非每帧重传或预先离线烘焙。配合若干启发式规则来决定何时需要重新生成：

- **可见性剔除驱动**：只有用户能看到的数据才需要生成——对象太小或不在屏幕上时，其关联的阴影/光照数据不必更新。
- **级联方案**：[[cascaded-shadow-maps]] 按距离分配阴影分辨率；Cascaded Reflective Shadow Maps 把同样思路推广到全局光照（一次漫反射弹射、AO 等）。
- **屏幕空间技术**：对于远距离或小尺寸对象，[[screenspace-reflections|Screen-Space GI]] 或类似技术可以用 G-Buffer（延迟渲染已有的结构）提供低成本的近似。

## 与其他设计原则的关系

这条原则是 Engel 子系统设计系列的一部分，与 [[graphics-subsystem-even-error-distribution|均匀误差分布]] 原则及 Screen-Space 原则并列。三条原则共同指向同一目标：设计一个在各种硬件档次上可以优雅降级（graceful degradation）的图形子系统。[[image-quality-philosophy]] 在更宏观的层面上也讨论了类似的质量-性能取舍哲学。

## Sources

- [[sources/humus-no-lut-rules]]
