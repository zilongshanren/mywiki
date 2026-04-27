---
tags: [source, demoscene, 工具, 压缩exe, directx, hlsl, c99]
date: 2026-04-27
sources: 1
---

# Graphics Demo Programming（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 发表于 2011 年 9 月的短文，回顾了他历时约十年维护一个 demoscene 演示骨架程序的经历，记录从 DX8 到 DX10、从 Windows XP 到 Windows 7 的演变，以及最终将可执行文件压缩至 838 字节的实验结果。

## 摘要

Engel 约在 2000 年前后开始为 demoscene 准备一个最小化的 Windows/DirectX demo 骨架，目标是在遵守 Windows 资源释放规则的前提下尽量减小 exe 体积。他最初使用 Visual Studio 进行构建，但发现每换一个新版本 exe 反而会变大，最终切换到遵循 C99 标准的免费编译器 **Pelles C**，最终实现 838 字节的可执行文件。实验过程中他还发现一个有趣现象：HLSL 代码在某些情况下比等价的 CPU C 代码编译出更小的二进制——这让他产生了"用极小的 CPU stub 做程序骨架、然后在 HLSL 里展开逻辑"的想法。他在 DirectX 9 阶段还额外嵌入了一个小型 GPU 粒子系统，而 exe 大小并未显著增加。

## 关键要点

- **838 字节 exe**：使用 Pelles C（C99 编译器），在不违反 Windows 资源释放规则的前提下得到的极限体积
- HLSL 二进制在某些情况比 C 更紧凑，提示"CPU 只做 stub，逻辑搬到着色器"的架构思路
- GPU 粒子系统被内嵌进骨架但几乎不增加体积
- 代码公开在 Google Code（`graphicsdemoskeleton`）
- 对比参考：Inigo Quilez 也有一套完整的 1k/4k demo 框架

## 链接到的概念

- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/09/graphics-demo-programming.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-09-18_graphics-demo-programming.md`
