---
tags: [source, opengl, opengles, ios, powervr, gpu-hang, 调试]
date: 2026-04-19
sources: 1
---

# What Does gpus_ReturnGuiltyForHardwareRestart Mean?（Ben Supnik）

[[ben-supnik|Ben Supnik]] 2013-08-25 的 iOS OpenGL ES 2.0 调试笔记，拆解 PowerVR SGX 上一个让一代 iOS 开发者抓狂的崩溃回调。

## 摘要

在 iPhone 上用 OpenGL ES，偶尔会在 `glBufferData` 或其他看似无关的 GL 调用上死在 `gpus_ReturnGuiltyForHardwareRestart`，call stack 经过 `libGPUSupportMercury` → `IMGSGX543GLDriver` → `GLEngine`。Supnik 声明以下是 *speculative engineering*，但解释惊人自洽：硬件加速的 `glDrawElements` 不做 CPU-side 边界检查，GPU 自己 fetch 顶点时如果索引越界，会留便条等下次驱动进门——下次的 GL 调用（完全无辜的那个）就接到账单并触发崩溃。**崩溃点 ≠ 闯祸点、崩溃时机依赖 CPU 与 GPU 时序**，注释代码 bisect 只会让崩溃漂移。他的修复：写一个 debug 例程，**draw 前**校验全部索引 / VBO 字节范围，当场抓到他自己的真实 bug——一次 client-array draw 没 unbind VBO，沿着上一次留的 VBO 绑定读出范围外数据。

## 关键要点

- 硬件加速 GL 路径不做 CPU-side 边界检查，异步越界故障在"下次碰 GPU 的 CPU 调用"触发。
- 标准 bisect 调试对这种异步故障无效，反而让现象漂移。
- 在自己的 `glDraw*` 宏里加 debug-only 索引 / VBO 范围断言是一次性投入的正确纪律。
- 该模式在 D3D TDR / Vulkan device lost / Metal GPUError 上同构重现。

## 链接到的概念

- [[gpu-hang-deferred-fault-debugging]]
- [[opengl-ext-vs-arb-fast-path-leak]]
- [[race-condition-debug]]
- [[opengl-builtin-attribute-aliasing]]
- [[gpu-queues-vs-dispatch-execution]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2013/08/what-does-gpusreturnguiltyforhardwarere.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-08-25_what-does-gpus-returnguiltyforhardwarerestart-mean.md`
