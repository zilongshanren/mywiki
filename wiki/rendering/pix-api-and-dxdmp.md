---
tags: [D3D12, 调试, PIX, GPU工具, GDC2026]
date: 2026-04-19
sources: 1
---

# PIX API、DirectX Dump Files 与"主机级 PC 调试"

GDC 2026 上 Microsoft 的 "DirectX: Bringing Console-Level Developer Tools to Windows" 是 [[adam-sawicki|Adam Sawicki]] 眼里**本届最重要的公告**——PC 端 GPU 调试终于要接近 Xbox 的水平。他的评注从应用开发者的痛点出发，诚实到近乎尖刻。

## 当前 PC GPU 调试的"石器时代"

- 崩溃（TDR，Timeout Detection and Recovery）几乎没得调——帧捕获工具要求 `Present()` 成功
- Debug Layer、GPU-Based Validation、[DRED](https://microsoft.github.io/DirectX-Specs/d3d/DeviceRemovedExtendedData.html)、Nvidia Aftermath、Radeon GPU Detective 各家一套，能用时好，不能用时一堆 GPU 寄存器十六进制
- Shader 调试只有 RenderDoc 的 CPU 模拟——"模拟"会掩盖竞态、barrier 缺失、shader 编译器 bug

## Microsoft 的四件套

### 1. DirectX Dump Files（.dxdmp）

- GPU 崩溃瞬间的状态快照，可以在 PIX 中打开
- 四家 GPU 厂商（AMD/Intel/Nvidia/Qualcomm）同台站台，罕见的"行业统一"信号
- 有"开销 vs 可操作性"开关——low overhead 模式可以一直开着给玩家收集
- 通过 Watson 上报给 Microsoft，或手动收集
- **Sawicki 的担心**：从演示截图看，不同厂商展示的内容差别很大，怕只是个通用壳，里面填的还是厂商专属的寄存器 dump，游戏开发者**读不懂几千页十六进制**

### 2. PIX API

- C++/C#/Python 访问 PIX capture 与 dump 的数据
- 直接后果：**RenderDoc 已经有了 Python API，PIX 只是追上了**
- 真正的未来向：可以写 MCP server，让 AI agent 直接读 capture 做调试/性能分析

### 3. HLSL `DebugBreak()` 内建函数

- 规范：[HLSL Spec 0039](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0039-debugbreak.md)
- 等价 CPU 的 `assert`——触发瞬间崩溃，定位到具体 frame / draw / pixel/thread
- 替代 Sawicki 自己写的 hacky [ShaderCrashingAssert](https://github.com/sawickiap/ShaderCrashingAssert)
- **Sawicki 的抱怨**：没有参数！就算只能传 `uint` 或 `uint4` 到 dump 里也好；更希望顺带标准化 **HLSL printf**（目前只有 Chris Bieneman 那篇非官方提案）

### 4. PIX Events 透传到驱动

- 长期以来 `PIX_BEGIN/END` 事件、`SetName` 这些只停在 Microsoft runtime 这一层，**不会往下传到驱动**
- 后果：AMD 工具只能通过 ETW 或 AGS 库 workaround（见 RGD 文档），不稳定
- 新的 [PIX Markers 规范](https://microsoft.github.io/DirectX-Specs/d3d/D3D12PIXMarkers.html) 让事件和 `SetName` 透到 DDI，**驱动端工具**（Radeon Developer Tools 家族）终于能直接看到名字
- Sawicki 还在盼望把 `SetPrivateData` 一起透传——那样就不用每次都改 API

### 5. "Real-time, on-chip shader debugging"（2027 目标）

- 主机级 shader 调试：断点、单步、看 local 变量
- **最大技术障碍**：GPU 没有 CPU 那种"暂停进程而系统继续"的能力——单次 draw call 就占满整颗芯片
- 可行思路：远程机器上挂 debugger（类似 WinDbg kernel debugging），或用集显跑桌面、独显停机
- **另一个大问题**：shader 高度内联、无 call stack——要在 DXIL/SPIR-V → GPU ISA 所有阶段保留 HLSL/GLSL 源行号与变量映射

## 对比：Vulkan 的 layer

Sawicki 多次抱怨 Microsoft 没有 Vulkan 那样正式的 **API layer 注入机制**——PIX、RenderDoc、GfxReconstruct、GPU Reshape 各造一套 hook，都和 DX12 runtime 打架。Nvidia Streamline 是个尝试，但被视为厂商方案，别家不买账。Slang 着色语言倒有希望推动这件事。

## 相关

- [[adam-sawicki]]
- [[dxr-tier-2-clas-ptlas]]
- [[advanced-shader-delivery]]
- [[d3d12-work-graphs]]
- [[hlsl-cooperative-vectors-tensor-cores]]
- [[d3d12-resource-binding]]

## Sources

- [[sources/asawicki-dx12-gdc-2026-comments]]
