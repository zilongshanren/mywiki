---
tags: [人物, 作者]
date: 2026-04-14
sources: 2
---

# Apoorva Joshi

**Apoorva Joshi** 是一位常驻丹麦的图形程序员，前 Activision 的 path tracing 工程师。个人博客 [apoorvaj.io](https://apoorvaj.io/) 从 2015 年写到今天，话题横跨实时渲染、图像处理、低层系统、工具链、业余项目随笔。代表作品是 **Papaya**——一个开源的 GPU 加速 2D 图像编辑器，用 C++ + OpenGL + [Dear ImGui](https://github.com/ocornut/imgui) 从零实现，GitHub 仓库 `ApoorvaJ/Papaya`。

## 风格

- **从具体 bug 切入**：一篇讲调用约定的文章起因是他漏写 `WINAPI` 宏、32 位编译挂了；一篇讲笔刷性能的文章起因是他想做一个比 GIMP 快的图像编辑器。问题导向，少口号。
- **爱做 minimal repro**：解释 `cdecl/stdcall/fastcall` 时直接 `gcc -S -m32 main.c` 做三路 diff；解释笔刷性能时 `__rdtsc()` + `QueryPerformanceCounter` 给量化数字。
- **小项目主义**：Papaya、taxman.dk 这类副业都倾向于「业余晚上手写一遍、去掉框架依赖」。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| The experiment | [[calling-conventions-x86]] |
| Zooming and panning | [[gpu-image-editor-brush]] |
| What is OpenGL loading? | [[opengl-loader]] |
| Normal Mapping | [[tangent-space-normal-mapping]] |

## 相关

- [[calling-conventions-x86]]
- [[gpu-image-editor-brush]]
- [[fragment-shader]]
- [[opengl-loader]]
- [[tangent-space-normal-mapping]]

## Sources

- [[sources/apoorvaj-calling-conventions]]
- [[sources/apoorvaj-zooming-and-panning]]
- [[sources/apoorvaj-opengl-loading]]
- [[sources/apoorvaj-normal-mapping]]
