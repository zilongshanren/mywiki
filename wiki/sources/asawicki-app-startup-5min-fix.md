---
tags: [source, Windows, 性能, DLL加载, 开发环境]
date: 2026-04-27
sources: 1
---

# How I Fixed My App Taking 5 Minutes to Start（Adam Sawicki）

[[adam-sawicki]] 发表于 2025 年 12 月的文章，记录了排查 Unreal Engine 游戏首次启动耗时近 5 分钟问题的全过程，最终定位到 Windows Smart App Control 功能。

## 摘要

Sawicki 在新 Windows PC 上发现，基于 Unreal Engine 的游戏首次启动总要等将近 5 分钟才能看到任何画面，重启后重复发生。他依次排查了 PDB 符号加载、杀毒软件（关闭了实时防护也无效）、并行预热 DLL 等方向均无结果，最终偶然读到一篇介绍 Smart App Control 的文章，立刻关闭该功能后问题彻底消失。该功能默认在全新 Windows 安装上启用，会在每个 DLL 加载时扫描（可能上传服务器校验），加之 UE5 编辑器需加载 914 个 exe/dll，累积延迟极为显著。Smart App Control 关闭后不可再开启。

## 关键要点

- Windows Smart App Control 会在每次 DLL 加载时执行扫描，可能涉及网络请求
- 在 Unreal Engine 工程中需加载 914 个 exe/dll，导致延迟叠加到不可接受的程度
- 在单进程内多线程并行调用 `LoadLibrary` 并无帮助，内部似乎有 mutex 串行化
- 拆分到多个进程并行加载有所改善（可作为临时 workaround）但不根治
- 对于开发者而言关闭 Smart App Control 是合理选择，对普通用户该功能仍有安全价值
- 调试手段：Visual Studio 输出面板观察 DLL 加载消息、Very Sleepy profiler、Concurrency Visualizer

## 链接到的概念

- [[windows-startup-dll-scan]]

## 原文

- 链接：https://asawicki.info/news_1796_how_i_fixed_my_app_taking_5_minutes_to_start
- 本地：`raw/articles/asawicki.info/2025-12-22_how-i-fixed-my-app-taking-5-minutes-to-start.md`
