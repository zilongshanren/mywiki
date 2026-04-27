---
tags: [source, 渲染, DirectX11, 图形API, HLSL, alain.xyz]
date: 2026-04-27
sources: 1
---

# Raw DirectX 11（Alain Galvan / alain.xyz）

[[alain-galvan]] 发表于 2021 年 10 月的文章，通过一个完整的 Hello Triangle 程序逐步拆解 DirectX 11 初始化与渲染流程。

## 摘要

文章以 C++ 代码片段为主体，覆盖 DX11 渲染的五个阶段：API 初始化（Factory/Adapter/Device/DeviceContext）、SwapChain 与 RenderTargetView 设置、顶点/索引/常量 Buffer 创建与着色器编译、Pipeline State 描述、以及帧循环中的命令执行与 Present。作者指出 DX11 相比 DX12 等现代 API 在使用上更简单，代价是失去了多线程提交等性能空间，并推荐绿地项目直接考虑 DX12。文章使用 CrossWindow 库处理跨平台窗口，`ComPtr<T>` 作为 RAII 包装器管理 COM 对象生命周期。

## 关键要点

- DX11 以 `ID3D11Device`（工厂）+ `ID3D11DeviceContext`（执行器）为核心二元组
- 所有 Buffer（顶点、索引、常量）均为 `ID3D11Buffer`，通过 `BindFlags` 区分用途
- ConstantBuffer 更新用 `Map(WRITE_DISCARD)` + `memcpy` + `Unmap` 三步走
- Pipeline State 拆分为 InputLayout、DepthStencilState、RasterizerState 等独立对象
- 命令执行是立即式：调用 `DeviceContext` 系列方法后驱动隐式排队执行

## 链接到的概念

- [[rendering/directx11-api-overview]]
- [[rendering/directx12-api-overview]]
- [[rendering/d3d12-resource-binding]]
- [[rendering/dx11-driver-overhead]]

## 原文

- 链接：https://alain.xyz/blog/raw-directx11
- 本地：`raw/articles/alain.xyz/2021-10-23_raw-directx-11.md`
