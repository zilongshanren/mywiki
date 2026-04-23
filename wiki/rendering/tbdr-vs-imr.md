---
tags: [渲染, gpu, 架构]
date: 2026-04-05
sources: 3
---

# TBDR vs IMR

两种 GPU 架构的对立：

| | **IMR** | **TBDR** |
|---|---|---|
| 全名 | Immediate Mode Rendering | Tile-Based Deferred Rendering |
| 典型硬件 | NVIDIA、AMD 桌面 GPU | Mali、Adreno、Apple Silicon GPU |
| 渲染方式 | 每个三角形立即处理 | 屏幕分 tile，分块处理 |
| 关键优势 | 简单直接、瓶颈可预测 | 带宽效率极高 |

## TBDR 的 Binning Pass

TBDR 在提交 DrawCall 后需要做两件事：

1. **Binning Pass**：执行 vertex shader，根据三角形覆盖分发到各个 tile 的 bin。
2. **Per-Tile Processing**：每个 tile 独立进行光栅化 + fragment shader，使用**片上内存**作为 framebuffer。
3. **Write Back**：tile 处理完才写回 DRAM。

副作用：**vertex shader 被执行两次**（一次 binning，一次渲染）。

## HSR：TBDR 独有优势

**Hidden Surface Removal**：在 tile 内可以在 fragment shader 前精确剔除被遮挡的三角形。**几乎消除 overdraw**——如果没有 `discard` 和 alpha test。

## 带宽差距

| 架构 | 带宽典型值 | 每帧预算 @ 60fps |
|---|---|---|
| RTX 4090 (IMR) | 1008 GB/s | ~16.8 GB |
| Adreno 730 (TBDR) | 40 GB/s | ~667 MB |

## MSAA 几乎免费（TBDR）

TBDR 下 MSAA 数据留在片上内存，写回时只写 resolve 结果——成本极低。IMR 下 MSAA 需要外部 framebuffer 加倍，带宽成本显著。

## 破坏 TBDR 的做法

- `discard` / alpha test：破坏 HSR，过度绘制成本恢复。
- `gl_FragDepth` 写入：破坏 Early-Z。
- RenderTarget 切换：迫使 tile 写回 + 读回，昂贵。
- 过多 subpass / framebuffer：放大移动端瓶颈。

## 相关
- [[rendering-pipeline]]
- [[early-z-late-z]]
- [[overdraw]]
- [[msaa-ssaa]]
- [[cached-shadowmaps]] —— 远级联阴影跨帧缓存的相干性优化
- [[mtl-render-pass-descriptor]] —— Metal 把 TBDR 的 tile load/store 暴露到 API

## Sources

- [[sources/rtr-day01]]
- [[sources/rtr-day05]]
- [[sources/rtr-day06]]
- [[sources/c0de517e-tiled-hardware-speculations]]
- [[sources/gameknife-tbdr-performance-tuning]] —— Bruce Merry 的 OpenGL Insights TBDR 调优章节中译本，覆盖 frame data、glDiscardFramebuffer、HSR 与 depth-only-pass 的实战权衡
