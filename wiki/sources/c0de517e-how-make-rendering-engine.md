---
tags: [source, rendering, game-engines, draw-call, sort-key]
date: 2026-04-27
sources: 1
---

# How to make a rendering engine（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2014 年 4 月的文章，汇总了"无状态渲染 + sort-key"架构的核心资源，并回答了围绕该设计的常见疑问。

## 摘要

文章的核心观点是：现代渲染引擎不应使用 scene graph 或状态机，而应将每次 draw 所需的全部状态编码为一个固定位宽的排序键（sort key），通过排序来最小化状态切换，并保证内存访问的局部性。Pesce 收集了 Christer Ericson、Aras Pranckevicius、BGFX、Intel Nulstein、MT Framework 等多个参考实现，并逐一回答了常见 FAQ：

- 排序键中的位通常是数组下标或直接 API 指针，排序的魔力在于将随机访问变为线性访问
- 应使用"桶"（bucket）按 render target/pass 分组，避免单一全局排序
- 桶内可并行生成 draw，先踢第一个 pass 的 GPU，再处理后续 pass，降低延迟
- 不同 pass（shadowmap、deferred G-buffer）可用不同 key 编码和不同解码循环
- 变换层级（transform hierarchy）只需要针对骨骼动画，不应成为整个渲染系统的基础
- scene graph 的根本问题：每帧大量指针跳转 + 无序访问，与 GPU driver 吞吐量争夺 CPU

## 关键要点

- "指针间接跳转让 DX11 渲染代码 CPU bound"是性能基线诊断
- Sort key 架构：全状态编码为 bit string → 排序 → 线性解码 → 提交 GPU 命令
- Bucket 策略：per render target/pass 一个列表，分别排序后合并
- 并行化友好：各线程各自生成 key 列表，唯一同步点在 merge，之后并行生成 GPU command list
- 对于 Fifa 这类固定场景的游戏，完全知道绘制顺序，可绕过整个架构

## 链接到的概念

- [[rendering/draw-call]]
- [[rendering/render-graph]]
- [[rendering/stingray-sort-key-bit-layout]]
- [[rendering/rendering-pipeline]]
- [[game-engines/scene-graph-unnecessary-in-engine]]
- [[game-engines/immediate-vs-retained-mode]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/04/how-to-make-rendering-engine.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-04-08_how-to-make-a-rendering-engine.md`
