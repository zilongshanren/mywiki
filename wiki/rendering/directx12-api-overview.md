---
tags: [渲染, DirectX12, 图形API, HLSL, 命令队列, 描述符堆, 微软]
date: 2026-04-27
sources: 1
---

# DirectX 12 API 概览

DirectX 12 是 Microsoft 为 Windows 和 Xbox 平台维护的现代低级图形 API，设计哲学与 [[vulkan-explicit-performance]]、Metal 一脉相承：**将驱动复杂性转移到应用层**，让开发者直接控制命令队列、管线状态、资源屏障和内存分配，从而实现更低的 CPU overhead 和更好的多线程扩展性。

## 核心抽象

**设备与命令队列**：`ID3D12Device` 是 API 入口，负责创建所有资源。`ID3D12CommandQueue` 接受批量命令列表并向 GPU 提交，`ID3D12CommandAllocator` + `ID3D12GraphicsCommandList` 负责命令录制。与 DX11 的 DeviceContext 最大区别是：命令录制与提交分离，天然支持多线程录制。

**同步原语**：`ID3D12Fence` 让 CPU 侧可以在提交后轮询或等待 GPU 完成某帧。`ResourceBarrier`（资源屏障）则向驱动声明资源的状态转换，例如从 `PRESENT` → `RENDER_TARGET` → `PRESENT`，驱动据此排查 hazard，省去了 DX11 中隐式追踪的开销。关于 barrier 的更宏观视角见 [[gpu-hazard-tracking]]。

**描述符堆**：`ID3D12DescriptorHeap` 统一管理 CBV/SRV/UAV 以及 RTV/DSV 的描述符内存，避免驱动在每次绑定时重新分配。详见 [[d3d12-resource-binding]] 和 [[d3d12-root-signature]]。

**内存管理**：Heap（`ID3D12Heap`）+ CommittedResource 允许应用层控制 GPU 内存的分配粒度；Upload Heap 用于 CPU→GPU 传输，Readback Heap 用于结果回读。[[d3d12-resource-alignment]] 记录了对齐要求细节。

## 渲染流程六步

1. **初始化**：Factory（含 Debug Controller） → Adapter → Device → CommandQueue → CommandAllocator → CommandList
2. **帧缓冲**：SwapChain（`IDXGISwapChain3`）→ 创建 RTV DescriptorHeap → 为每帧 back buffer 建立 RTV；创建 Fence 用于帧同步
3. **资源上传**：通过 Upload Heap 将顶点/索引数据写入 GPU 内存，利用 Fence 等待拷贝完成
4. **管线构建**：Root Signature → 编译 HLSL（推荐 DXC 工具链）→ PSO（`ID3D12PipelineState`），一次性烘焙所有管线状态
5. **命令录制与提交**：Reset → 设置 RootSignature / DescriptorHeap → ResourceBarrier（PRESENT→RT）→ 录制 draw call → ResourceBarrier（RT→PRESENT）→ Close → ExecuteCommandLists → Present → Signal Fence
6. **销毁**：调用 `Release()` 或 `ComPtr<T>` 自动回收

## 与 DX11 的关键差异

DX11 的 `DeviceContext` 承担了隐式命令排队和驱动端同步，代价是 [[dx11-driver-overhead]]。DX12 将这些职责交还应用层，使得批量提交、异步计算（[[async-compute]]）、多线程命令录制（[[frames-in-flight]]）变得可行。[[render-graph]] 是在 DX12/Vulkan 之上管理这一复杂度的常见架构模式。

DX12 还扩展至 GPGPU 领域（[[gpgpu-compute-simt-model]]）和硬件光线追踪（`DirectX Raytracing` / DXR，见 [[bvh-traversal-hardware]]），以及 DirectML 用于机器学习推断。

## Sources

- [[sources/alain-raw-dx12]]
- [[sources/asawicki-dx12-all-sources]]
