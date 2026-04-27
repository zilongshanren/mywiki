---
tags: [source, DirectX12, HLSL, 文档, 图形API]
date: 2026-04-27
sources: 1
---

# All Sources of DirectX 12 Documentation（Adam Sawicki / asawicki.info）

[[adam-sawicki]] 于 2025 年 11 月的文章，系统梳理 DirectX 12 官方文档的所有来源，并对其碎片化现状发表批评。

## 摘要

与 Vulkan 拥有一份权威、完整的规范不同，D3D12 的文档分散在多个独立渠道：Microsoft Learn（主文档）、GitHub DirectX-Specs 仓库（含 DXR、Work Graphs 等新特性）、DirectXShaderCompiler Wiki（DXC 与 HLSL 扩展）、新版 HLSL 规范（microsoft.github.io/hlsl-specs/）、DirectX Developer Blog，以及 DirectX Landing Page 汇总页。Sawicki 以康威定律（Conway's Law）解释这一现象：各团队（Agility SDK、DXC 等）分别维护自己的文档出口，缺乏统一的用户体验负责人。他对 HLSL 正式规范的新进展持谨慎乐观态度。

## 关键要点

- D3D12 文档至少涵盖六个独立来源，无统一入口
- learn.microsoft.com 是主文档，但不含最新 Agility SDK 特性
- 新特性（DXR、Work Graphs、Shader Model 6.x）在 GitHub DirectX-Specs 仓库
- HLSL 语言本身有专属的 DXC Wiki 和新版 hlsl-specs 站点
- DirectX Developer Blog 是追踪新版本公告的最佳渠道
- DirectSR 已被悄悄从 Agility SDK 中移除

## 链接到的概念

- [[directx12-api-overview]]
- [[d3d12-work-graphs]]
- [[hlsl-cooperative-vectors-tensor-cores]]

## 原文

- 链接：https://asawicki.info/news_1794_all_sources_of_directx_12_documentation
- 本地：`raw/articles/asawicki.info/2025-11-25_all-sources-of-directx-12-documentation.md`
