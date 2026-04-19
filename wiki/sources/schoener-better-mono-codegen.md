---
tags: [source, unity, mono, 编译器, codegen, 性能]
date: 2026-04-19
sources: 1
---

# Better codegen for Unity games on Mono（Sebastian Schöner）

[[sebastian-schoener]] 2026 年 3 月的公告帖：他在把 Unity 的 Mono 运行时（Windows x64）改造得生成更好的机器码，面向**已经在用 Mono 的 Unity 游戏和 Unity Editor**，想把这个做成商业化服务。

## 摘要

Unity 长期依赖 Mono 跑 Editor 以及部分带 Mod 支持的游戏。Mono 的 codegen 经常输给 CoreCLR 与 IL2CPP。作者投入做的改良已经能让若干真实 Unity 代码（尤其 `float4`、DOTS、Entities Graphics 之类**结构体密集**的数学代码）在 Mono 上跑出接近一个数量级的提速。作者特意写过类似的 il2cpp 工具 [`cpp2better`](https://blog.s-schoener.com/2025-11-04-cpp2better-release/)——逻辑是「改 codegen 不等于改游戏帧率，只有 CPU compute-bound 的地方真的受益」；但 Mono 默认太烂以至于几乎任何想写性能代码的项目都会在某处撞到 compute bound。使用方式非常轻：**只需把新的 Mono 运行时 drop 进游戏构建，不改一行游戏代码**，Release 构建自行选择开启哪些 pass，Debug 自动关闭。

## 关键要点

- 受众：**无法马上升到 Unity 6.8 / CoreCLR** 的现有项目、必须用 Mono 跑以支持 Mod 的游戏、Unity Editor
- 擅长场景：仿真游戏、DOTS/Entities、任何大量使用 `Vector3` / `float4` 等值类型的代码
- `dot4` 案例：400+ 行原始汇编 → 约 30 行改良版，前者满是 `cvtss2sd`/`cvtsd2ss` 往返和冗余栈槽复制
- 改良版仍不完美（没用 vectorcall、还有部分不必要 spill），但足以比原版快一个数量级
- 零侵入：不修改游戏代码；开启哪些优化可按项目权衡 JIT 成本

## 链接到的概念

- [[mono-jit-pipeline]]
- [[pointer-alias-analysis]]
- [[dead-store-elimination]]

## 原文

- 链接：https://blog.s-schoener.com/2026-03-31-better-mono/
- 本地：`raw/articles/blog.s-schoener.com/2026-03-31_better-codegen-for-unity-games-on-mono-sebastian-schoner.md`
