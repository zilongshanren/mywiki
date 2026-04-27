---
tags: [source, 图形, DirectX, API, 渲染]
date: 2026-04-27
sources: 1
---

# DirectX 11.1 Notes（Wolfgang Engel）

[[wolfgang-engel]] 发表于 2011 年 9 月的文章，对 DirectX 11.1 新增特性的早期整理笔记。

## 摘要

本文写于 DX11.1 正式发布前，是一篇从 MSDN 预览文档中提炼的功能清单式笔记。DX11.1 相对 DX11 的升级集中在四个方向：为 Metro 风格应用提供完整 Direct3D 11.x 支持（无 D3D9）；扩展 UAV 到每个管线阶段（vs/hs/ds/gs/cs/ps 均可绑定）；在 Render Target 上支持逻辑操作；以及面向低功耗设备（移动 / ARM）的优化（HLSL shader 精度 hint、tile-based 渲染优化、4bpp DXGI 格式 565/5551/4444）。文章还记录了 `D3D11_FEATURE_DATA_ARCHITECTURE_INFO`（识别 tile-based GPU）、`D3D11_FEATURE_DATA_SHADER_MIN_PRECISION_SUPPORT`、DXGI 格式扩展（视频格式可通过 SRV/RTV/UAV 在 shader 中处理）、以及 Windows 8 SDK 中新增的 HLSL FXC、Debug Layers、REF 设备。Engel 特别关注 shader tracing（当时认为是新的性能测量途径）和全 pipeline stage UAV 这两点。

## 关键要点

- UAV 扩展到所有管线阶段（DX11 仅 CS，DX11.1 推广至 VS/HS/DS/GS/PS）
- Render Target 逻辑操作（logical blending op）
- Shader tracing：新的性能测量工具（当时细节尚不公开）
- 低功耗优化：shader 精度 hint（half-precision HLSL）、tile-based 渲染 hint、4bpp 格式
- `D3D_FEATURE_LEVEL_11_1` 新增硬件 Feature Level
- WARP（软件光栅）在 Windows 8 上支持 FL 11.0 + DXGI 1.2 16bpp 格式
- D3DX9/10/11 在 Metro 风格应用中不被支持，需迁移至 DirectXTex 等
- 写作时无公开驱动/硬件支持 FL 11.1，内容来自 MSDN 预览文档

## 链接到的概念

- [[directx11-api-overview]]
- [[async-compute]]
- [[multiple-render-targets]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/09/directx-111-notes.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-09-14_directx-11-1-notes.md`
