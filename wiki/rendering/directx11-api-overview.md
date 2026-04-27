---
tags: [渲染, DirectX11, 图形API, HLSL, 光栅化, 微软]
date: 2026-04-27
sources: 1
---

# DirectX 11 API 概览

DirectX 11 是 Microsoft 图形 API 的上一代版本，设计目标是在易用性与性能之间取得平衡。与 DX12/Vulkan 相比，它将驱动层的复杂性隐藏在抽象之后，适合绿地项目的入门以及通过 [DirectX 11 on 12](https://docs.microsoft.com/en-us/windows/win32/direct3d12/direct3d-11-on-12) 桥接层在 DX12 环境中继续使用。

## 核心对象模型

DX11 的对象模型以 `ID3D11Device`（资源工厂）和 `ID3D11DeviceContext`（命令执行器）为核心二元组。两者均通过 `D3D11CreateDevice` 一次性创建。`IDXGIFactory` 和 `IDXGIAdapter` 负责枚举可用 GPU 及其输出（显示器），`IDXGISwapChain` 管理后缓冲区的分配与呈现。

与 DX12 最显著的差异在于**无命令列表、无同步原语**。`DeviceContext` 承担了立即执行的角色：调用 `IASetVertexBuffers`、`VSSetShader`、`DrawIndexed` 等后直接排入驱动队列，驱动负责隐式同步。这简化了编程模型，却削弱了多线程提交和显式调度带来的性能空间。

## 渲染流程五步

1. **初始化 API**：创建 Factory → Adapter → Device + DeviceContext
2. **帧缓冲设置**：查询 AdapterOutput 的刷新率，创建 SwapChain，取得 back buffer `ID3D11Texture2D` 并建立 `ID3D11RenderTargetView`
3. **资源初始化**：上传 VertexBuffer / IndexBuffer，编译或加载 HLSL 着色器，建立 ConstantBuffer，描述 Pipeline State（DepthStencilState、RasterizerState）
4. **渲染帧**：更新 ConstantBuffer（`Map` → `memcpy` → `Unmap`），调用 `OMSetRenderTargets`、`DrawIndexed`，最后 `Present`
5. **销毁**：调用 `Release()` 或借助 `ComPtr<T>` RAII 自动回收

## 常量缓冲区与着色器参数传递

DX11 对常量缓冲区采用"先映射再 memcpy"的写法，`Map` 时指定 `D3D11_MAP_WRITE_DISCARD` 可让驱动在 GPU 未使用时直接重命名，避免 stall。关于这一模式的深入分析见 [[glbuffersubdata-serialization]]（OpenGL 端有类似机制）。

## HLSL 着色器编译

DX11 既支持运行时通过 `D3DCompileFromFile` 编译 HLSL，也可预编译为二进制 blob。[[dxc-dxil-signing]] 记录了更现代的 DXC/DXIL 工具链；[[hlsl-derivation-correctness]] 和 [[hlsl-texture-sampling-basics]] 为 HLSL 语义提供了补充上下文。

## 与 DX12 的关系

DX11 的隐式同步和驱动封装带来开发便利，代价是驱动端 overhead（见 [[dx11-driver-overhead]]）。现代 API（[[directx12-api-overview]]、[[vulkan-explicit-performance]]）通过暴露命令队列、围栏和描述符堆让应用程序掌控这些决策。[[directx11-early-pitfalls]] 记录了 DX11 早期部署时遇到的具体坑。

## Sources

- [[sources/alain-raw-dx11]]
- [[sources/humus-dx11-1-notes]]
