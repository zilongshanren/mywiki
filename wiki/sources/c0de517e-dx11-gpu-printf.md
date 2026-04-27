---
tags: [source, graphics, debugging, gpu, dx11]
date: 2026-04-27
sources: 1
---

# DX11: GPU "printf"（c0de517e / Angelo Pesce）

[[angelo-pesce]] 发表于 2013 年 7 月的文章，介绍用 DX11 append buffer 在像素/计算 shader 中实现类 printf 调试可视化。

## 摘要

Pesce 和同事 Maurizio Cerrato 在 MJP 的 SampleFramework11 基础上实现了一套 GPU printf 工具。核心思路：在 shader 中调用 `AppendStructuredBuffer.Append()` 写入调试记录（线段端点 + 颜色 + 标志位），只对特定像素坐标或网格位置触发，帧末用 geometry shader 把记录渲染成屏幕上的线条和数字字形。字形用折线字体手动编码，GS `maxvertexcount` 限制了每条调用最多能显示的有效数字位数（三个浮点数时每个只有 4 位精度，一个浮点时可达 12 位）。GPU 端用一个小 compute shader 把 `CopyStructureCount` 的结果乘以 2（线段两端点），再通过 `DrawInstancedIndirect` 发起 draw，完全避免 CPU 回读计数。

## 关键要点

- 过滤宏是核心：`IsDebuggedPixel()` 检查当前 `sv_position` 是否等于目标坐标，只有命中的 invocation 才 append，保证 buffer 不溢出
- 支持调试模式 1（特定像素）和模式 2（每 100px 的网格），通过 cbuffer 参数切换，无需重编 shader
- GS maxvertexcount 是硬约束，需要把字体设计为 `DigitFontMaxLinesPerDigit=5` 线段/位，精心权衡了精度与顶点数
- 与 draw indirect 配合：CS 读取 append count 后乘 2 写入 `RWBuffer`，GS 读同一 structured buffer 按 `PrimitiveID` 取记录——避免 IA 阶段传入顶点数据
- 2013 年时 shader 热重载 + GPU printf 已足以覆盖大量调试场景

## 链接到的概念

- [[gpu-printf-debugging]]
- [[debug-visualization]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/07/dx11-gpu-printf.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-07-14_dx11-gpu-printf.md`
