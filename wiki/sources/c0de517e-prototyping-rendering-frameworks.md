---
tags: [source, 渲染, 工具链, 原型框架]
date: 2026-04-27
sources: 1
---

# Prototyping Frameworks (Rendering)（C0DE517E）

[[angelo-pesce]] 发表于 2012 年 1 月的文章，整理他实际使用及调研过的渲染原型框架，是当年图形程序员工具链的一份快照。

## 摘要

Pesce 将渲染原型工具分为三档：日常使用的、看起来有前途的、其他备选。文章并不追求新颖技术，而是记录了一个 AAA 图形程序员在 2012 年前后对各种 shader/渲染原型环境的实际评价，包括工具的优点、崩溃情况和停更状态。

## 关键要点

- **FX Composer**（NVIDIA）：Pesce 仍在使用，但 2.5 和 1.8 版本各有 bug，文档稀少，部分功能需要用 ILSpy 反射才能理解。
- **Mathematica / Python/IPython**：数学验证首选，Mathematica 语言对程序员友好（类 Lisp）；Python（Anaconda）是轻量替代。
- **SharpDX / SlimDX**：C# 封装 DirectX，Pesce 喜欢 C#；配合 SharpDevelop 可不依赖最新 Visual Studio。
- **Processing**：适合 2D 原型，生态库丰富，支持 Eclipse live-coding。
- **ShaderToy**：在线便捷，适合快速小测试，但大 shader 容易因编译超时崩溃。
- **MJP (Matt Pettineo) 的 C++ 框架**：干净、简单，Pesce 有自己的 fork，被多人推荐。
- **Humus Framework 3**：比引擎轻，附大量演示，Humus 的 demo 代码被视为高质量参考。
- **值得关注的新兴工具**：MiniEngine（Microsoft DX12 示例）、BGFX（跨 API 统一封装，含 Vulkan）、Threejs（WebGL）。

## 链接到的概念

- [[shader-prototyping-tools]]
- [[shadertoy-basics]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/01/prototyping-frameworks.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-01-18_prototyping-frameworks-rendering.md`
