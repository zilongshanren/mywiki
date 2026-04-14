---
tags: [source, directx, 历史, 入门]
date: 2026-04-14
sources: 1
---

# Introduction to DirectX 9 for Game Programmers（Jeremiah van Oosten）

[[jeremiah-van-oosten]] 2011 年的一篇 Direct3D 9 入门教程，用 Visual Studio 2008 一步步搭出第一个能旋转立方体的 Win32 + D3D9 应用。今天主要作为**历史文献**阅读：DirectX 9 已经被 D3D11/12 取代，DirectDraw、DirectSound、DirectInput、DirectPlay 等子模块大都已弃用。

## 摘要

文章先做了一段 DirectX 家族的"产品线漫游"：Direct3D（3D）、Direct2D（取代 DirectDraw）、XAudio2（取代 DirectSound）、XInput（取代 DirectInput）、Windows Sockets（取代 DirectPlay）。然后给出 D3D9 工程的标准搭法：装 SDK、配 VS include/library 路径、链接 `d3d9.lib` 和 `d3dx9.lib`、引入 `windows.h` / `d3d9.h` / `d3dx9.h` 三个头文件。核心代码段示范了 `IDirect3D9` 与 `IDirect3DDevice9` 这两个 COM 对象的生命周期（**只能用 `Release()` 释放，不能 `delete`**）、`IDirect3DVertexBuffer9` / `IDirect3DIndexBuffer9` 的创建与填充，以及一个可旋转的彩色立方体的渲染循环。

## 关键要点

- D3D9 是 **fixed-function pipeline 末期 + programmable 早期**的混合形态，文章里同时出现 `SetTransform(D3DTS_VIEW, …)`（FFP 思维）和 vertex/index buffer（programmable 思维）。
- COM 对象的释放语义是 D3D 老 API 的标志性陷阱，习惯了 D3D11 智能指针/D3D12 ComPtr 的人初次回看会很不适应。
- 文中提到的 `D3DXMATRIX` / `D3DXVECTOR3` 等 D3DX 辅助库本身在后续 SDK 里也被砍掉了，迁移到 DirectXMath。
- 历史价值：理解 D3D11/12 接口为什么仍然带着 `IDirect3D…` / `Release()` 这些 COM 残留，得回到 D3D9 时代看一眼。

## 链接到的概念

- [[rendering-api-depth]]
- [[d3d12-resource-binding]]
- [[jeremiah-van-oosten]]

## 原文

- 链接：https://www.3dgep.com/introduction-to-directx-for-game-programmers/
- 本地：`raw/articles/3dgep.com/2011-02-17_introduction-to-directx-9-for-game-programmers.md`
