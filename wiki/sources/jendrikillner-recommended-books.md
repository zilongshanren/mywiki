---
tags: [source, graphics, books, 阅读清单]
date: 2026-04-19
sources: 1
---

# My recommended Books（Jendrik Illner）

[[jendrik-illner]] 于 2025 年 1 月整理的个人推荐书单，面向从入门到进阶的图形程序员，覆盖渲染、碰撞、引擎、数据导向设计、算法与知识管理。

## 摘要

书单按主题分为六类。渲染类推荐 *GPU Zen 3*（含 Assassin's Creed Mirage 的 GPU-driven 场景表达、Skull and Bones 的跨平台 MIP 反馈方案、虚拟阴影贴图、Slang 可微图形等）、*Real-Time Rendering 4e*（入门到参考书）、*Physically Based Rendering 4e*（pbr-book.org 免费可读）。碰撞类推荐 Ericson 的 *Real-Time Collision Detection*。引擎类三本：*Foundations of Game Engine Development Vol.1 Mathematics*（引入 Grassmann/几何代数，解释为何法向量变换"反常"）、*Vol.2 Rendering*（面向中级图形程序员，补齐 Gregory 对渲染覆盖不足的部分）、*Game Engine Architecture 3e*（Naughty Dog 实战视角，除渲染外覆盖最广）。另推荐 Fabian 的 *Data-Oriented Design*（超越 cache-miss 视角）、*Grokking Algorithms 2e*（面试复习友好），以及德文原版的 *Zettelkasten-Prinzip*（作者称其改变了其知识管理方式）。

## 关键要点

- GPU Zen 3 是 2024 年末发布的进阶渲染合集，重点关注 GPU-driven 渲染与 CPU/GPU 共享场景表达。
- Skull and Bones 以写回 CPU 可读的 MIP 访问信息解决 GPU-driven 下的纹理流式加载难题。
- FGED Vol.1 引入几何代数，用以更自然地解释法向量在变换下的行为。
- PBR 4e 可在 pbr-book.org 免费在线阅读。
- 作者将 Zettelkasten 方法作为个人知识管理的基础。

## 链接到的概念

- [[gpu-driven-rendering]]
- [[virtual-shadow-maps]]
- [[texture-streaming]]
- [[data-oriented-design]]
- [[physically-based-rendering]]

## 原文

- 链接：https://www.jendrikillner.com/books/
- 本地：`raw/articles/jendrikillner.com/2025-01-01_my-recommended-books.md`
