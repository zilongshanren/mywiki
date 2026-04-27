---
tags: [source, testing, graphics, ray-tracing, integration-testing]
date: 2026-04-27
sources: 1
---

# Methods of Testing（16BPP.net）

[[people/16bpp]] 发表于 2021 年 7 月的文章，介绍如何为 [[psraytracing]] 搭建自动化测试基础设施，核心工具是 OpenImageIO 的 `idiff` 命令行工具，配合约 300 行 Python 测试脚本。

## 摘要

作者从「一个离线渲染器怎么做自动化测试？」这一问题出发，梳理了单元测试 vs 集成测试的哲学选择：PSRayTracing 优先选择集成测试，因为它测的是「已知正确渲染结果」，比白盒单元测试更能保护既有行为。测试流程分两阶段：先做一次「reference run」，把 350 个参数组合对应的渲染图存下来；之后任何代码改动都用 `idiff` 逐像素对比，非零 diff 即为失败。因为渲染器是完全确定性的（同种子同线程数同输出），像素级一致性测试是可靠的。除正确性外，测试脚本还记录每次渲染耗时（纳秒精度），用于追踪性能回归。作者特别指出：线程数不影响输出但影响性能，所以「同参数不同线程数应输出相同渲染图」本身也是一类可测假设。整套方案在作者的机器上 12 分钟跑完 350 个场景。

## 关键要点

- **`idiff`（OpenImageIO）**：逐像素比较两张图，返回标准退出码；可用 `-abs -o diff.jpg` 可视化差异区域
- **确定性是可测性的前提**：渲染器必须先做到「固定输入固定输出」，才能用像素对比做回归测试
- 350 个测试用例通过 `itertools.product()` 穷举参数组合后随机采样（每场景 10 个）生成，保存为 CSV
- 性能测试与正确性测试共用同一套跑步器：每条用例记录渲染时间，供代码改动前后对比
- 感知差异工具（Perceptual Image Diff）可作为 `idiff` 的补充，用于判断近似是否「视觉无差」
- 集成测试优先于单元测试的理由：继承大型代码库时往往不了解内部实现，但知道预期输出

## 链接到的概念

- [[render-integration-testing]]
- [[psraytracing]]
- [[automated-test-philosophy]]
- [[benchmark-methodology-end-to-end]]

## 原文

- 链接：https://16bpp.net/blog/post/automated-testing-of-a-ray-tracer/
- 本地：`raw/articles/16bpp.net/2021-07-08_methods-of-testing.md`
