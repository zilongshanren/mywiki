---
tags: [source, rendering, 延迟, 并行, 引擎架构]
date: 2026-04-19
sources: 1
---

# Threads, buffers and latency（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 8 月的短札，由 Digital Foundry 对下一作《极品飞车》的技术访谈引出：**那一作决定回到单线程、不拆 sim / render**，理由是 30fps 下那一帧 sim-render 缓冲在手感里明显。

## 摘要

Pesce 自问：**你的引擎有几帧延迟？** 他列出自己当时至少能数到的三层——sim → render、render → worker jobs、jobs → GPU——而且明言「还有我没管到的子系统」。这是一篇**提问式**的笔记，不给答案，指向一个普遍盲区：多数工程师不知道自己引擎实际累积了多少层 flight，因为每个子系统作者只对自己那段 double-buffer 负责。

文章的隐含判断是：**高帧率下多 stage 能被吸收，30fps 下每层 33ms 很快就超过玩家可感阈值**，因此「不拆」在低帧率目标下反而是正确选择。

## 关键要点

- **多级 buffer = 多级延迟**。每一层 double-buffer 都要多算一帧在总延迟里。
- **下一作 NFS 单线程不拆 sim/render**——选择权衡倾向延迟而非吞吐。
- **Pesce 自己三层**：sim → render、render → jobs、jobs → GPU，还不算子系统。
- 没给具体测量方法，是纯**提问式 poke**——但正因如此这个问题对每个工程师都成立。
- 对应现代讨论见 [[frames-in-flight]]：把 flight 深度做成可配置、按平台 / 模式调。

## 链接到的概念

- [[frame-pipeline-latency]]
- [[frames-in-flight]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/08/threads-buffers-and-latency.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-08-10_threads-buffers-and-latency.md`
- 注：同目录另有一份 `2010-08-10_threads-buffers-and-latency-2.md` 是 2026-04-19 重抓的存档副本，内容完全一致，未另建 source 页。
