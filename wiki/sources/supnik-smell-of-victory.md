---
tags: [source, opengl, api-design, arb, buffer-storage]
date: 2026-04-19
sources: 1
---

# The Smell of Victory（Ben Supnik）

[[ben-supnik|Ben Supnik]] 2013-07-22 的一条短笔——庆祝他"这一派"终于打赢了一场嘴仗。

## 摘要

Supnik 抛出一条 `GL_ARB_buffer_storage` 规范原文：issue 9 里 ARB 自己承认 `CLIENT_STORAGE_BIT` 属于"那种蠢 hint"——应用会永远猜错，驱动会第二次猜，然后堆满启发式把 buffer 来回搬，最终 hint 设与不设没区别，"But hey, we tried."。他在此基础上建议 ARB 以后应该诚实命名这些 hint：`GL_REALLY_FAST_BIT` / `GL_NO_REALLY_THIS_BUFFER_NEEDS_TO_BE_FAST_BIT` / `GL_TRUST_ME_I_KNOW_WHAT_I_AM_DOING_BIT`。核心观点是：OpenGL 长年在 buffer usage hint 上依赖应用程序做全局视野决策，历史证明此方向失败——Vulkan / Metal 那种明示式 heap + 可查询对齐要求才是出路。

## 关键要点

- ARB 2014 年正式在规范里承认 hint bit 是失败设计（应用猜错 → 驱动忽略 hint）。
- `CLIENT_STORAGE_BIT` 并非完全无意义（非 UMA 平台下含义具体），但结局相同。
- 对工程师：看到 GL hint 枚举，默认按"驱动会忽略、靠实际模式启发式"的契约编码；想要确定性，必须走显式 API。

## 链接到的概念

- [[opengl-hint-bit-irrelevance]]
- [[opengl-ext-vs-arb-fast-path-leak]]
- [[opengl-pinned-memory-vbo-streaming]]
- [[glbuffersubdata-serialization]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2013/07/the-smell-of-victory.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-07-22_the-smell-of-victory.md`
