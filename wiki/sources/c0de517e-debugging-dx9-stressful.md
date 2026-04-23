---
tags: [source, 工具, 调试, directx, pix, 历史]
date: 2026-04-19
sources: 1
---

# Debugging DirectX9 is so stressful!（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 3 月的一篇发泄式短文，切片记录了 2011 年 PC DX9 端 GPU 调试工具的惨淡景观。非系统性教程，但作为「那个年代到底有多难用」的一手口述史料有价值。

## 摘要

在主机上做了五年游戏图形的 Pesce，新项目需要他顺手处理 PC 端 DX9 构建，结果被调试环境折磨到几近病倒。他对当时 PC DX9 工具链做了一轮快速点评：

- **PIX for Windows**——玩笑般的水平，但已经是他能用的最好的 DX9 工具；窗口不刷新、像素调试总掉、不支持 INTZ 纹理格式、drawcall 列表组织混乱。
- **NVIDIA PerfHUD**——基本没用；评论里有人说它 profile 更好，但 PIX 当时根本无法做 profile。
- **Intel GPA**——捕获要 20 分钟、结果怪异；但后续更新后 Pesce 反倒把它作为 DX9 首选。
- **apitrace**——新工具，早期版本不支持 DX9，后来补齐。
- **AMD GPU PerfStudio**——DX9 版已弃用，新版只支持 DX10/11。
- **NVIDIA Parallel NSight（Nexus）/ AMD GPU PerfStudio 2**——都 DX10/11 only，PC DX9 再次被抛弃。

评论区形成一张有价值的「2011 平台阴阳榜」：Xbox 360 最好，D3D9 其次，PC OpenGL 工具贫瘠，PS3 曾经最惨但 `gcmhud` 已可实时分析。Daniel 吐槽「PS3 文档翻译过来的英文」，Pesce 反驳说至少 PS3 是单 GPU、学会一次就一劳永逸；PC 虽然 API 有文档，但 GPU 家家不同、驱动各有脾气，综合起来反而最模糊。

## 关键要点

- **2011 年 PC DX9 的调试工具空白**：主流厂商工具都已转向 DX10/11，DX9 处于「维护断档」。
- **PIX for Windows 的历史位置**：与 PIX for Xbox 360 的盛名构成鲜明反差，一度是「最好的烂工具」。
- **平台阴阳榜**（评论区众声一致意见）：Xbox 360 > D3D9 > OpenGL/PS3 工具链——但「单平台熟悉成本」与「多平台驱动多样性」的权衡让排序其实不稳。
- **apitrace 早期定位**：2011 年的新选项，是后来跨平台 API 追踪的雏形。
- **pixel shader 调试** 是当时 PIX 最常用又最不稳的功能：一个「Out of video memory」就能废掉整次排查。

## 链接到的概念

- [[angelo-pesce]]
- [[pix-api-and-dxdmp]] —— 2026 年 Sawicki 评 GDC：「PC GPU 调试终于要赶上 Xbox」——这条时间线的源头就是 Pesce 2011 年的痛苦
- [[pesce-pix-is-great-but|c0de517e-pix-is-great-but]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/03/debugging-directx9-is-so-stressful.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-03-26_debugging-directx9-is-so-stressful.md`
