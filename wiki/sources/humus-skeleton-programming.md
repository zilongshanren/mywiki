---
tags: [source, demoscene, compute-shader, 工具, c99]
date: 2026-04-27
sources: 1
---

# Visual Studio 2013 / Demo Skeleton Programming（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 于 2013 年 11 月发表的简短工具更新通知，记录其 Google Code 上的 demoscene 演示骨架（graphics demo skeleton）升级到 VS2013 的过程。

## 摘要

文章内容极短，主要记录三处更新：将项目切换到 Visual Studio 2013（后者部分支持 C99，因此现有代码得以直接编译）；对 compute shader 示例进行小幅修改；以及将 Crinkler（demoscene 常用的可执行文件压缩工具）升级到 1.4 版本。Crinkler 可将 compute shader 编译成的 header 文件与主程序一起压缩，最终可执行文件大小为 2,955 字节。这是一篇工具维护通知，不包含独立的图形技术内容。

## 关键要点

- VS2013 部分支持 C99，解除了部分旧式 C 代码的编译障碍
- compute shader 可以编译为 header 文件，再由 Crinkler 作为数据段压缩，进一步减小 demo 体积
- Crinkler 1.4 使整体压缩至 2,955 字节

## 链接到的概念

- [[rendering/gcn-compute-tgsm-patterns]] — Engel 对 compute shader 的更深入优化实践

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2013/11/visual-studio-2013-demo-skeleton.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2013-11-07_visual-studio-2013-demo-skeleton-programming.md`
