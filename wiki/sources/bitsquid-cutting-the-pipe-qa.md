---
tags: [source, bitsquid, tooling, architecture]
date: 2026-04-19
sources: 1
---

# Cutting the Pipe: Achieving Sub-Second Iteration Times（Niklas / Bitsquid）

[[niklas-frykholm]] 2012 年 3 月对前一次 GDC 讲座 *Cutting the Pipe* 的一组问答。原 raw 文件只抓到了评论区的 Q&A 片段，没有正文；但问答本身把 Bitsquid 工具链的一条核心取舍讲得比讲稿更直接。

## 摘要

问题一：工具和引擎共享多少代码？Niklas 的回答是**一行都不共享**——工具写在 C#，引擎写在 C++，两边几乎不用 RTTI / 反射。在他看来 RTTI 和自动反射虽然上手快，但会在"内存布局 / 磁盘格式 / GUI 布局"之间建立起致命的强耦合，日后迭代都要付利息。工具和引擎靠**可读、可 merge 的 JSON 文件**通信，JSON 由编辑器写、由引擎读。引擎会把 JSON 再编译成自家的高性能 blob 格式，但**编辑器完全看不到 blob 这一层**。这就是 Bitsquid [[decoupled-tool-engine-json-rpc]] 的早期声明。

问题二：能不能做到多个编辑器 UI 统一？Bitsquid 的做法是所有 C# 编辑器共用一个**共享库**实现基础功能；统一观感不依赖"塞进一个 exe"。

## 关键要点

- **工具 / 引擎零代码共享**是 Bitsquid 的一贯立场，JSON 作为接口层把双方完全隔离。
- RTTI / 反射在 Niklas 看来是短期便利、长期耦合的典型案例。
- 统一 UI 观感通过共用基础库解决，与工具是否同进程无关。

## 链接到的概念

- [[decoupled-tool-engine-json-rpc]]
- [[minimal-markup-pipeline]]
- [[interface-vs-implementation]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/03/cutting-pipe-achieving-sub-second.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-03-12_cutting-the-pipe-achieving-sub-second-iteration-times.md`
- 注：raw 文件只包含评论区，未抓到原讲稿正文；本摘要基于 Niklas 在评论区的澄清。
