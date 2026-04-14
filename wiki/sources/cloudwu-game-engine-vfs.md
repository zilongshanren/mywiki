---
tags: [source, 游戏引擎, 资源管理, 文件系统]
date: 2026-04-14
sources: 1
---

# 实现一个简单的虚拟文件系统（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 4 月的博客，记录他为开发中的 3D 引擎重写资源管理子模块的思考——想把它改成一个简化版的 Linux VFS。

## 摘要

开篇先回顾游戏资源打包的历史（Allegro、Doom/Quake、星际）和包格式接口一旦定下就难以改动的事实，并举了个有趣对比：网易的升级补丁 95% 时间在下载，而暴雪的补丁大部分时间在 patching——可见包格式对 patch 性能影响极大。云风反省自己 2006 年为新引擎设计的"资源按 ID 关联、带依赖关系信息"方案：理论漂亮，实际上因为新程序员理解成本高、误用负面效应大，反而不如"保持一般惯例"。他由此反感 C++ 的 all-in-one 哲学，偏好 C 那种"积木零件"的设计。第二半给出新方案：仿 Linux VFS 的简化版，一个独立于具体 FS 的树管理层（负责文件名、目录项、cache），一组可挂载的具体 FS（本地、内存、zip、自定义包），支持嵌套包的多级路径访问。和 Linux VFS 的一个分歧：他需要"zip 里找不到自动回落到本地"的行为，解法是专门写一个 `auto` FS，按顺序尝试 `/zip`、`/os`，成功后在自己的子树上创建**软链接**指向命中位置——既不污染 mount 语义，也天然带 cache。

## 关键要点

- 游戏包格式与 patch 性能强相关；接口一旦定下就锁死工具链。
- "过度设计比惯例差"：新程序员理解成本 > 精心设计带来的性能好处。
- 借 Linux VFS 的概念降低沟通成本——别自创词汇。
- 只读语义大幅简化 VFS 设计。
- 树管理独立于具体 FS；具体 FS 按 mount 挂到挂载点下。
- fallback 用"auto FS + 软链接延迟绑定"，比"loader 注册表轮询"更优雅、天然带 cache。

## 链接到的概念

- [[game-engine-vfs]]
- [[interface-vs-implementation]]
- [[cognitive-load]]
- [[modular-design]]
- [[abstraction]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/04/
- 本地：`raw/articles/blog.codingnow.com/2010-04-12_yun-feng-de-blog.md`
