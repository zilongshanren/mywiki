---
tags: [source, 图形, metal, apple, osx, 内存模型]
date: 2026-04-19
sources: 1
---

# OS X Metal - Raw Notes（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015-06 看完 WWDC 2015 Metal 桌面版 session 后的粗略笔记，覆盖内存模型、缺失功能、与 Mantle 的对比判断。

## 摘要

Metal 上桌面的主要问题：分立 GPU 上 CPU / GPU 各有内存。Apple 的选择是给四档 `MTLResourceOptions`——**Shared**（一份在 AGP，command buffer 边界一致）、**Managed**（CPU+GPU 各一份，`didModifyRange:` / `synchronizeResource:` 显式同步）、**Private**（仅 GPU 侧，最快的 tiled/swizzled layout，只能 blit encoder 访问）、**Auto**（iOS 变 Shared、OS X 变 Managed，用来写跨平台）。桌面 Metal 加了 instancing、正经 constant buffer、texture barrier、occlusion query、draw-indirect；缺失 transform feedback / geometry shader / tessellation（评论提出**用 compute shader 做 transform feedback 替代**，这条后来成了主流）。与 Mantle 对比：Mantle 暴露多条并行 queue、需要手动声明 command queue 引用的资源、提供 memory pool 让你自己分配——Metal **全部隐藏**，因此更简单但放弃了 pool allocator 模式（Ben 推测 AAA 开发者会不满）。桌面 Metal 仍明显快于 OpenGL，但 Ben 指出这不等于「driver 管资源一致性」是免费的——得拿 Mantle 做对照才能量化。唯一 Mantle-like 的口子：`newBufferWithBytesNoCopy:` 能直接从 VM page 建 buffer，但这与 Mantle 的池不同。商业判断：Metal on OS X 是 Apple 把移动游戏往桌面迁的桥——比用更现代的 OpenGL 把 PC 移过来更可行（「少一个 DirectX clone 就无解」）。

## 关键要点

- **四档存储选项** Shared / Managed / Private / Auto——替代 Mantle 风格的 pool allocator。
- **Managed 的写回是排队的**——`synchronizeResource:` 放在 blit encoder 上，不是立即。
- **Private 是 framebuffer / VRAM 资源的默认位置**——驱动选最快的 tiled/swizzled 布局。
- **没有暴露并行 queue**——Metal 可能内部把 blit offload 到 DMA queue。
- **没有 reference pool 声明**——Mantle 要求显式声明，Metal 不用。
- **缺失功能**：transform feedback、geometry shader、tessellation。评论：**compute shader 可替代 transform feedback**（写 private buffer + graphics 读）。
- **直通 VM**：`newBufferWithBytesNoCopy:` 是唯一 Mantle-like 口子，零拷贝。
- 商业定位：**从 iOS 游戏往 OS X 迁，比从 PC 迁更现实**。

## 链接到的概念

- [[osx-metal-memory-model]]
- [[metal-api-overview]]
- [[mtl-render-pipeline-state]]
- [[mtl-render-pass-descriptor]]
- [[vulkan-explicit-performance]]
- [[agp-vs-vram-streaming]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/06/os-x-metal-raw-notes.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-06-10_os-x-metal-raw-notes.md`
