---
tags: [source, 图形, opengl, 驱动, 性能]
date: 2026-04-19
sources: 1
---

# OpenGL State Change Is Deferred（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015-04 的文章，拿 GL 驱动实际结构解释「为什么 `glDrawArrays` 看起来这么慢」。

## 摘要

在任何生产级 GL 驱动里，`glBindBuffer` / `glVertexAttribPointer` / `glEnable` 等**状态切换的真工作都延后到下一次 draw call** 才执行——函数返回时仅在 context 上记录「脏位」。根本原因是单独一次状态调用不够决定最终硬件配置：vertex format 要在 VS 前置里 patch 出 fetch 代码，必须等所有 `glVertexAttribPointer` 都进来才有意义；而驱动没有「改完了」通知，draw call 成了天然同步点。Supnik 给出标准的驱动侧伪代码——状态函数只改 context + dirty_bits，draw 函数检查 dirty_bits、按位同步硬件、清零。两条推论：一是 profile 上 `glDrawArrays` 80% CPU **多半是状态同步**，不是 draw 本身；二是**冗余状态切换**（循环里重复 `glEnable(GL_BLEND)`）**仍然代价巨大**——驱动不会替你去重，每次都会让脏位置位、每次 draw 都会重跑 blend sync。Apple 的 GL 栈拆 dylib，Instruments 里能看到 `sync_*` 子程序，调优时能直接定位；Windows 栈是 monolithic + stripped，看不到 back-trace，同样热点就得靠推理。

## 关键要点

- 状态调用**只做记账**（写 context + 标脏位），draw call **补齐同步**。
- 延迟的理由：**单个状态调用不足以决定硬件配置**（vertex layout 影响 shader 生成）。
- 驱动**不做去重** —— 冗余 `glEnable` 同样会污染 context、拖慢 draw call。
- **profile 误读警告**：把 `glDrawArrays` 占 80% 理解为「draw 本身贵」是错的，真正贵的是 setup。
- Apple 栈：多 dylib + debug symbol → Instruments 直接看到 sync 热点。Windows 栈相反。
- 推论方向性地指向 Metal/Vulkan 的显式 PSO（见 [[mtl-render-pipeline-state]]、[[vulkan-explicit-performance]]）。

## 链接到的概念

- [[opengl-state-change-deferral]]
- [[opengl-hardware-impedance-mismatch]]
- [[draw-call]]
- [[gl-draw-accumulator-batching]]
- [[mtl-render-pipeline-state]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/04/opengl-state-change-is-deferred.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-04-14_opengl-state-change-is-deferred.md`
