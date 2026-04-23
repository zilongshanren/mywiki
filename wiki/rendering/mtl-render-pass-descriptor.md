---
tags: [渲染, metal, apple, tbdr, render-pass, 带宽]
date: 2026-04-19
sources: 1
---

# MTLRenderPassDescriptor：把 TBDR 的 load/store 写到 API 面上

`MTLRenderPassDescriptor` 是 Metal 强制你在**开始 render encoder 之前**回答的一组问题：这次 pass 画哪几张 attachment？每张 attachment 一开始是 **load、clear 还是 dontCare**？结束时是 **store、discard 还是 resolve**？没有缺省——你**必须**回答，`renderCommandEncoderWithDescriptor:` 才能给你 encoder。

## 为什么这在 PowerVR 上特别重要

PowerVR / Apple Silicon 是 [[tbdr-vs-imr|TBDR]]：整个渲染表面被切成 32×32 之类的小 tile，**每个 tile 在片上 cache 里完成整个 pass 的所有 primitive**，然后回写 DRAM。架构存在的理由是**省带宽**——移动端没有桌面那种 VRAM + 宽总线，带宽就是功耗。

但要真的省下来，驱动必须**知道一个 render pass 的范围**：

- **pass 开始**——tile memory 是要从 DRAM 里 **load** 旧内容（继续在之前画的帧上 overlay）？还是 **clear** 到某个颜色（pass 要覆盖所有 pixel）？还是 **dontCare**（反正马上会覆盖）？
- **pass 结束**——tile 里的结果要 **store** 回 DRAM（color buffer 你想留下）？还是 **discard**（depth 只用来做 HSR，不需要写回，省一次 DRAM 写）？要 **resolve**（MSAA 的多采样样本合成单样本存储）？

每一对 load/store 节省的是**每 tile × 每 pass × 每 attachment** 的 DRAM 访问，整帧下来是巨量的带宽。

## GL ES 为什么做不到这么好

OpenGL ES 里**绑定一个新 framebuffer 并不告诉驱动这次 pass 的意图**。驱动只能：

- **假设 load** ——保险起见把旧内容从 DRAM 加载到 tile（如果接下来发现有 `glClear`，这次 load 就白做了）。
- **追踪每一次 draw** 以猜测 pass 范围和 store 时机。
- 依赖 `glInvalidateFramebuffer` / `glDiscardFramebufferEXT` 等**后验**机制告诉驱动「其实不用写回」——但应用很少正确调用这些扩展。

Metal 把这个问题**前置到 descriptor**——你绕不过去，驱动直接有完整信息。

## 与 PSO 的分工

- **[[mtl-render-pipeline-state|MTLRenderPipelineState]]**：锁死**一个 shader + 一套状态**的计算配方——跨 pass 可复用。
- **`MTLRenderPassDescriptor`**：锁死**这次 pass 的 attachment 读写行为**——每次开 encoder 都要一个，通常一帧里只有少数几个不同组合。

两个对象职责互补。一个控「shader / blend / vertex format」，一个控「tile memory ↔ DRAM 的通行规则」。合在一起，把 GL 里驱动靠推断维持的不变式**全部搬到 API**。

## 使用后果

- **Deferred Rendering**：G-buffer attachment 的 store 可以设 `dontCare`——它们只在 tile 里做 lighting subpass 用，不需要写回 DRAM。这是移动端延迟管线省带宽的关键。
- **Shadow depth pass**：color attachment 的 store 设 `dontCare`、depth attachment 的 store 设 `store`。
- **UI overlay pass**：color load 设 `load`（叠加前一 pass 的结果），store 设 `store`。

## 相关
- [[metal-api-overview]]
- [[hsr-tbdr]]
- [[tbdr-vs-imr]]
- [[mtl-render-pipeline-state]]
- [[render-pass-orchestration]]
- [[deferred-rendering]]
- [[cached-shadowmaps]]

## Sources
- [[sources/supnik-powervr-via-metal]]
