---
tags: [渲染, 着色器编译, dxc, dxil, directx, hlsl, 微软]
date: 2026-04-19
sources: 1
---

# DXC / DXIL 与 dxil.dll 代码签名之谜

DirectX 的 shader 编译链条在 DX12 / SM6 时代长成了一堆历史包袱叠加的形状，理解它是理解 [[mach-dxcompiler-static-build]] 为什么要存在的前提。

## 工具链层层堆叠

- **FXC**（D3D11 及以前）：老 Effects Compiler，编译慢、codegen 差，被社区诟病多年，在 DX12 时代被正式弃用，但仍作为 Windows 自带工具可用。
- **DXC**（DX12 / SM6 时代）：微软在 `microsoft/DirectXShaderCompiler` 开源，本质上是 **LLVM/Clang 3.7 的 Microsoft 分支**，加了 HLSL 前端。代码里每一处修改都用 `// HLSL Change Start/End` 注释标出归属。
- **DXBC**：DX9-11 时代驱动吃的 byte code 格式，未公开规格，只在微软和 IHV 之间流通。
- **DXIL**：DX12 时代的格式，本质就是 "微软 fork 的 LLVM 3.7 在跑完 codegen+optimization passes 之后吐出来的 bitcode + 一层小 container"，没文档——"文档就是我们的编译器实际吐什么"。
- **DXIR**：2019 年微软提过的"高层未优化 IR"，准备给 Rust 之类的 compiler 当 target，但 2021 年已经从文档中把所有相关描述删光。

## IHV 的真实合约

IHV（Intel/AMD/NVIDIA）驱动看的就是 DXIL。Apple 的 Metal 是行业里唯一能直接编到目标硬件原生二进制的平台（因为自己一手捏到硬件）。SPIR-V 虽然比文本 shading language 低，但仍然可能没做过优化，所以 Valve 搞 [Fossilize](https://github.com/ValveSoftware/Fossilize) 给每个 (GPU, 驱动版本) 组合缓存真正驱动编译后的二进制，玩家才不会开游戏时卡 shader 编译。

## 抽象层的真实困境

[[webgpu-intro|WebGPU]] 实现（Dawn、wgpu、Bevy 渲染后端）都面临一个 runtime 问题：

1. WGSL → HLSL（文本翻译）
2. HLSL → DXBC/DXIL（需要 HLSL 编译器，FXC 或 DXC）
3. 交给驱动继续下沉

选 FXC 还是 DXC？Bevy 文档说得直白：**FXC 老、慢、不维护，但不用随应用分发 dll**；DXC 新、快、维护中，但要带上 `dxcompiler.dll` 和 `dxil.dll` 一起发。结果很多引擎默认选 FXC——所以社区长期不能用 SM6.0+ 的功能。

## dxil.dll 是专有签名 blob

从 `DirectXShaderCompiler` 源码 build **不会**生成 `dxil.dll`，它只在 Microsoft 的 Release 里以二进制发布，且只有 Windows (x86/arm) + Linux (x86) 三种组合。这个 dll 承担的是 **shader 代码签名/校验**：

> D3D12 will only accept signed shaders. That means that if any patching or runtime optimizations are performed, such as constant folding, the shader must be re-validated and re-signed, which is non-trivial.
> — D3D12 Shader Cache API Spec

Shader Model 6.8 的 preview release 更进一步：预览版 DXC 不配套发 `dxil.dll`，意味着 6.8 的 DXIL 无法被签名，无法在非 Developer Mode 的 Windows 上运行。换句话说——**微软用 `dxil.dll` 作为控制什么能跑什么不能跑的闸门**。所谓"开源编译器"实际上依赖一个不开源的平台特定 blob，并且这个 blob 不覆盖 macOS、不覆盖 Linux aarch64，直接堵死了"在 Mac 上 / ARM Linux CI 里离线编 shader"这条路。

## 相关

- [[mach-dxcompiler-static-build]]
- [[sysgpu-webgpu-successor]]
- [[webgpu-intro]]
- [[slang-shader-language]]

## Sources

- [[sources/hexops-dxcompiler-better-than-microsoft]]
