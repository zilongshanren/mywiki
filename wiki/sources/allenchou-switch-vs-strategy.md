---
tags: [source, strategy-pattern, refactoring, software-design, allen-chou]
date: 2026-04-14
sources: 1
---

# Switch vs Strategy（Allen Chou, 2011）

[[allen-chou|Allen Chou]] 2011 年 2 月发布的一篇小小的重构笔记，用他 Bunnyhill 引擎里 blend mode 模块的真实代码演示如何把 `switch` 版替换成 Strategy Pattern 版。

## 摘要

作者先给出 `switch` 版：`BlendMode` 里三个字符串常量（`ADD` / `ALPHA` / `NORMAL`），`RenderEngine.setBlendMode(value)` 内部按值分派三种配置逻辑。看起来合理，但他引用 Martin Fowler 《Refactoring》的观点指出：每加一种 blend mode 都要同时改两个地方（`BlendMode` 加常量、`RenderEngine` 加 case），是典型的代码坏味道。重构做法是引入 `IBlendMode` 接口，让每种 blend mode 变成独立的小类自己负责配置；`BlendMode` 改为持有策略对象实例，`RenderEngine.setBlendMode` 退化为一行 `value.setupBlendMode(this)`。对调用方 API 完全不变，但**扩展代价从"改两个文件"降到"加一个类"**。评论区追问性能与权衡，作者的回答很实在：Strategy 不保证更快；选择取决于这段代码会不会频繁扩展、是否在热路径上——不是瓶颈时就优先清洁度。

## 关键要点

- "Replace Type Code with Strategy" 是 Fowler 经典重构项之一，对应的坏味道是"类型码驱动 switch"。
- Switch 版的问题不是运行慢，而是**改动放大**：一个逻辑变更变成两处物理改动。
- Strategy 版把"每种情况"变成一个类，扩展只需新增文件，原有代码不动；对调用方 API 可保持完全不变。
- 不要盲目套用：紧内循环里 `switch`（编译器能展开跳转表）可能更快；扩展需求不存在时抽象也就白抽。
- 作者原话：决策取决于"run once vs 每帧 10000 次"和代码清洁度的权衡。

## 链接到的概念

- [[strategy-vs-switch]]
- [[change-amplification]]
- [[modular-design]]
- [[cpp-multi-paradigm-discipline]]

## 原文

- 链接：https://allenchou.net/2011/02/switch-vs-strategy/
- 本地：`raw/articles/allenchou.net/2011-02-18_switch-vs-strategy-ming-lun-allen-chou-zhou-ming-lun.md`
