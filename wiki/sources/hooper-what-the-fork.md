---
tags: [source, 工具, 构建系统, 产品页]
date: 2026-04-19
sources: 1
---

# What The Fork（产品页，Daniel Hooper）

[[daniel-chase-hooper]] 为 [[build-process-visualization|构建可视化工具]] *What The Fork* 写的产品落地页（2026-01-01 快照），内容短但提供了一些[[sources/hooper-build-visualizer|技术介绍文]]里没有的产品形态细节。

## 摘要

*What The Fork* 是 Hooper 基于前述构建监听技术做成的商业产品：跨平台（macOS / Linux / Windows）、支持任何构建系统与自定义构建脚本、进程从 `fork()` 的瞬间流式画到时间轴、单个进程可看完整 duration / cwd / argv / 访问过的文件；纳秒级时间精度；录像可保存后续复盘或分享团队；**数据完全不离开本机**（隐私关切）。早期 access 阶段一次性买断（终身 license）并能获得定制化新 feature。页面里一条用户引述：rebuild time 35s → 3.3s，与技术文里的 CI 加速案例一致。作者身份：independent developer、前 Apple 工程师、设计工具 Principle 作者。

## 关键要点

- 产品形态：CLI `wtf <build-cmd>` + UI，跨三大桌面平台
- 录像功能：能保存构建记录供事后分析或共享同事
- 数据不离开本机——这是针对企业 CI 的关键卖点
- 支持任何构建系统（make / cargo / bazel / gradle / xcodebuild / zig / custom script）
- 商业模式：早期 access 阶段终身 license 买断 + 定制化反馈循环
- 用户背书：Delta、Mozilla、Apple 的工程师在自家项目上试用，每个都找到意外问题

## 链接到的概念

- [[build-process-visualization]]
- [[ci-cost-optimization-asg]]

## 原文

- 链接：<https://danielchasehooper.com/wtf/>
- 本地：`raw/articles/danielchasehooper.com/2026-01-01_what-the-fork.md`
